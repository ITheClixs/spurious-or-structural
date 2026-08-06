"""Deterministic paper-reconstruction LASSO kernels for sealed S0004 G2.

The module contains no RNG constructor and no registered execution authority.
It operates only on already residualized/scaled in-memory arrays under the
paper thresholds validated by the sealed G2 contract.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from xid.sim.g2 import G2Contract, validate_g2_contract


def _module_source_sha256() -> str:
    digest = hashlib.sha256()
    with Path(__file__).open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


_XID_LOADED_SOURCE_SHA256 = _module_source_sha256()


@dataclass(frozen=True, slots=True)
class LassoRatioSelection:
    """Fold-pooled CV MSE vector and selected sealed LASSO ratio."""

    selected_index: int
    selected_ratio: float
    pooled_mse: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class LassoCoordinateDescentResult:
    """Coordinate-descent coefficients and convergence diagnostics."""

    coefficients: NDArray[np.float64]
    sweeps: int
    maximum_update: float
    maximum_kkt_violation: float


def _readonly_c_float64(values: NDArray[np.float64]) -> NDArray[np.float64]:
    out = np.asarray(values, dtype=np.float64, order="C").copy()
    out.setflags(write=False)
    return out


def _require_float64_array(
    value: object,
    *,
    name: str,
    ndim: int,
) -> NDArray[np.float64]:
    if type(value) is not np.ndarray:
        raise TypeError(f"{name} must be an exact numpy.ndarray")
    array = value
    if array.dtype != np.dtype(np.float64):
        raise TypeError(f"{name} must use exact float64 representation")
    if array.ndim != ndim:
        raise ValueError(f"{name} must have {ndim} dimensions")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def select_lasso_ratio(
    fold_sse: NDArray[np.float64],
    *,
    contract: G2Contract,
) -> LassoRatioSelection:
    """Select the first sealed ratio within tolerance of the pooled CV minimum."""
    validate_g2_contract(contract)
    sse = _require_float64_array(fold_sse, name="fold_sse", ndim=2)
    expected_shape = (
        len(contract.paper_reconstruction.cv_validation_ranges),
        contract.paper_reconstruction.lambda_grid_size,
    )
    if sse.shape != expected_shape:
        raise ValueError("fold_sse must have the sealed CV-fold and ratio-grid shape")
    if np.any(sse < 0.0):
        raise ValueError("fold_sse entries must be nonnegative")

    pooled = np.empty(expected_shape[1], dtype=np.float64)
    denominator = np.float64(contract.paper_reconstruction.fit_window_bins)
    for ratio_index in range(expected_shape[1]):
        total = np.float64(0.0)
        for fold_index in range(expected_shape[0]):
            with np.errstate(over="ignore", invalid="ignore"):
                total = np.float64(total + sse[fold_index, ratio_index])
            if not np.isfinite(total):
                raise FloatingPointError("fold-SSE pooling produced nonfinite overflow")
        pooled[ratio_index] = np.float64(total / denominator)
        if not np.isfinite(pooled[ratio_index]):
            raise FloatingPointError("fold-SSE pooling produced nonfinite arithmetic")

    minimum = np.float64(np.min(pooled))
    tolerance = np.float64(contract.paper_reconstruction.selected_ratio_tolerance)
    selected_index = 0
    for ratio_index, pooled_mse in enumerate(pooled):
        if pooled_mse <= np.float64(minimum + tolerance):
            selected_index = ratio_index
            break

    return LassoRatioSelection(
        selected_index=selected_index,
        selected_ratio=contract.lasso_ratio_grid[selected_index],
        pooled_mse=_readonly_c_float64(pooled),
    )


def _soft_threshold(value: np.float64, penalty: np.float64) -> np.float64:
    if value > penalty:
        return np.float64(value - penalty)
    if value < -penalty:
        return np.float64(value + penalty)
    return np.float64(0.0)


def _maximum_kkt_violation(
    x_res: NDArray[np.float64],
    residual: NDArray[np.float64],
    coefficients: NDArray[np.float64],
    lambda_value: np.float64,
    row_count: np.float64,
) -> float:
    maximum = np.float64(0.0)
    for column_index in range(x_res.shape[1]):
        correlation = np.float64(np.dot(x_res[:, column_index], residual) / row_count)
        coefficient = coefficients[column_index]
        if coefficient == 0.0:
            violation = np.float64(max(float(np.abs(correlation) - lambda_value), 0.0))
        else:
            violation = np.float64(
                np.abs(correlation - np.float64(lambda_value * np.sign(coefficient)))
            )
        maximum = np.float64(max(float(maximum), float(violation)))
    return float(maximum)


def solve_lasso_coordinate_descent(
    x_res: NDArray[np.float64],
    y_res: NDArray[np.float64],
    *,
    lambda_value: float,
    contract: G2Contract,
) -> LassoCoordinateDescentResult:
    """Solve sealed paper LASSO from zero by ascending-coordinate sweeps."""
    validate_g2_contract(contract)
    x = _require_float64_array(x_res, name="x_res", ndim=2)
    y = _require_float64_array(y_res, name="y_res", ndim=1)
    if x.shape[0] != y.shape[0]:
        raise ValueError("x_res and y_res must have matching rows")
    if x.shape[0] == 0 or x.shape[1] == 0:
        raise ValueError("x_res must have positive rows and columns")
    if type(lambda_value) is not float or not math.isfinite(lambda_value):
        raise TypeError("lambda_value must be an exact finite Python float")
    if lambda_value < 0.0:
        raise ValueError("lambda_value must be nonnegative")

    row_count = np.float64(x.shape[0])
    denominators = np.empty(x.shape[1], dtype=np.float64)
    cutoff = np.float64(
        contract.paper_reconstruction.post_fwl_zero_norm_multiplier * np.finfo(np.float64).eps
    )
    for column_index in range(x.shape[1]):
        denominator = np.float64(np.dot(x[:, column_index], x[:, column_index]) / row_count)
        if not np.isfinite(denominator) or denominator <= cutoff:
            raise ValueError("active column norm must exceed the sealed post-FWL cutoff")
        denominators[column_index] = denominator

    coefficients = np.zeros(x.shape[1], dtype=np.float64)
    residual = np.asarray(y, dtype=np.float64, order="C").copy()
    penalty = np.float64(lambda_value)
    tolerance = np.float64(contract.paper_reconstruction.coordinate_descent_tolerance)
    kkt_tolerance = np.float64(contract.paper_reconstruction.kkt_tolerance)

    final_update = math.inf
    final_kkt = math.inf
    for sweep in range(1, contract.paper_reconstruction.maximum_iterations + 1):
        maximum_update = np.float64(0.0)
        for column_index in range(x.shape[1]):
            column = x[:, column_index]
            old = coefficients[column_index]
            rho = np.float64(
                (np.dot(column, residual) / row_count) + denominators[column_index] * old
            )
            new = np.float64(_soft_threshold(rho, penalty) / denominators[column_index])
            if new == 0.0:
                new = np.float64(0.0)
            update = np.float64(new - old)
            if not np.isfinite(rho) or not np.isfinite(new) or not np.isfinite(update):
                raise FloatingPointError("coordinate descent produced nonfinite arithmetic")
            if update != 0.0:
                residual = np.asarray(residual - update * column, dtype=np.float64, order="C")
                if not np.all(np.isfinite(residual)):
                    raise FloatingPointError("coordinate descent produced nonfinite arithmetic")
                coefficients[column_index] = new
            maximum_update = np.float64(max(float(maximum_update), float(np.abs(update))))

        max_abs_beta = np.float64(np.max(np.abs(coefficients)))
        kkt_violation = _maximum_kkt_violation(x, residual, coefficients, penalty, row_count)
        final_update = float(maximum_update)
        final_kkt = kkt_violation
        if not math.isfinite(final_update) or not math.isfinite(final_kkt):
            raise FloatingPointError("coordinate descent produced nonfinite arithmetic")
        if (
            maximum_update <= np.float64(tolerance * np.float64(1.0 + max_abs_beta))
            and kkt_violation <= kkt_tolerance
        ):
            return LassoCoordinateDescentResult(
                coefficients=_readonly_c_float64(coefficients),
                sweeps=sweep,
                maximum_update=final_update,
                maximum_kkt_violation=final_kkt,
            )

    raise RuntimeError(
        "coordinate descent failed to converge "
        f"after {contract.paper_reconstruction.maximum_iterations} sweeps "
        f"(maximum_update={final_update}, maximum_kkt_violation={final_kkt})"
    )
