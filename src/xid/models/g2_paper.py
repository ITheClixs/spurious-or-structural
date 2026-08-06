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


@dataclass(frozen=True, slots=True)
class PaperLassoProblem:
    """Training-centered and residualized paper LASSO problem."""

    y_mean: float
    x_means: NDArray[np.float64]
    pre_fwl_rms: NDArray[np.float64]
    active_columns: NDArray[np.bool_]
    y_centered: NDArray[np.float64]
    x_centered: NDArray[np.float64]
    factor_mean: float | None
    factor_sum_squares: float | None
    factor_centered: NDArray[np.float64] | None
    y_res: NDArray[np.float64]
    x_res: NDArray[np.float64]
    lambda_max: float


@dataclass(frozen=True, slots=True)
class PaperLinearCoefficients:
    """Original-unit coefficients reconstructed from a paper LASSO solve."""

    intercept: float
    factor_coefficient: float | None
    penalized_coefficients: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class PaperPcaFit:
    """Training-mean PCA fit and diagnostics for paper feature maps."""

    training_means: NDArray[np.float64]
    loading: NDArray[np.float64]
    orthogonal_projector: NDArray[np.float64]
    covariance_trace: float
    leading_eigenvalue: float
    eigengap: float
    loading_l1_norm: float


@dataclass(frozen=True, slots=True)
class PaperCrossSectionProjection:
    """Cross-sectional PCA score and residual block."""

    scores: NDArray[np.float64]
    residuals: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class PaperOlsResult:
    """Full-rank OLS coefficients and numerical rank metadata."""

    coefficients: NDArray[np.float64]
    rank: int
    rcond: float


def _readonly_c_float64(values: NDArray[np.float64]) -> NDArray[np.float64]:
    out = np.asarray(values, dtype=np.float64, order="C").copy()
    out.setflags(write=False)
    return out


def _readonly_c_bool(values: NDArray[np.bool_]) -> NDArray[np.bool_]:
    out = np.asarray(values, dtype=np.bool_, order="C").copy()
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


def _assert_all_finite(value: NDArray[np.float64] | np.float64, *, name: str) -> None:
    if not np.all(np.isfinite(value)):
        raise FloatingPointError(f"{name} produced nonfinite intermediate arithmetic")


def fit_paper_pca(
    training_values: NDArray[np.float64],
    *,
    contract: G2Contract,
) -> PaperPcaFit:
    """Fit the sealed paper PCA convention from training rows only."""
    validate_g2_contract(contract)
    values = _require_float64_array(training_values, name="training_values", ndim=2)
    if values.shape[0] < 2 or values.shape[1] < 2:
        raise ValueError("training_values must have at least two rows and feature columns")

    row_count = np.float64(values.shape[0])
    means = np.asarray(np.mean(values, axis=0), dtype=np.float64, order="C")
    centered = np.asarray(values - means, dtype=np.float64, order="C")
    covariance = np.asarray((centered.T @ centered) / row_count, dtype=np.float64, order="C")
    _assert_all_finite(means, name="PCA training means")
    _assert_all_finite(centered, name="PCA centering")
    _assert_all_finite(covariance, name="PCA covariance")

    trace = np.float64(np.trace(covariance))
    if not np.isfinite(trace) or trace <= 0.0:
        raise ValueError("PCA covariance trace must be positive and finite")
    try:
        eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    except np.linalg.LinAlgError as exc:
        raise np.linalg.LinAlgError("PCA eigen decomposition failed") from exc
    eigenvalues = np.asarray(eigenvalues, dtype=np.float64, order="C")
    eigenvectors = np.asarray(eigenvectors, dtype=np.float64, order="C")
    _assert_all_finite(eigenvalues, name="PCA eigenvalues")
    _assert_all_finite(eigenvectors, name="PCA eigenvectors")
    leading_eigenvalue = np.float64(eigenvalues[-1])
    second_eigenvalue = np.float64(eigenvalues[-2])
    loading = np.asarray(eigenvectors[:, -1], dtype=np.float64, order="C")
    _assert_all_finite(leading_eigenvalue, name="PCA leading eigenpair")
    _assert_all_finite(loading, name="PCA leading eigenpair")
    if leading_eigenvalue <= 0.0:
        raise ValueError("PCA leading eigenvalue must be positive and finite")

    sign_index = int(np.argmax(np.abs(loading)))
    if loading[sign_index] < 0.0:
        loading = np.asarray(-loading, dtype=np.float64, order="C")
    loading_l1 = np.float64(np.sum(np.abs(loading)))
    _assert_all_finite(loading_l1, name="PCA loading L1 norm")
    if loading_l1 <= 0.0:
        raise ValueError("PCA loading L1 norm must be positive and finite")

    eigengap = np.float64(leading_eigenvalue - second_eigenvalue)
    gap_floor = np.float64(contract.paper_reconstruction.pca_top_eigengap_min_trace_ratio * trace)
    if not np.isfinite(eigengap) or eigengap <= gap_floor:
        raise ValueError("PCA eigengap must exceed the sealed trace-scaled threshold")

    identity = np.eye(values.shape[1], dtype=np.float64)
    projector = np.asarray(identity - np.outer(loading, loading), dtype=np.float64, order="C")
    _assert_all_finite(projector, name="PCA orthogonal projector")

    return PaperPcaFit(
        training_means=_readonly_c_float64(means),
        loading=_readonly_c_float64(loading),
        orthogonal_projector=_readonly_c_float64(projector),
        covariance_trace=float(trace),
        leading_eigenvalue=float(leading_eigenvalue),
        eigengap=float(eigengap),
        loading_l1_norm=float(loading_l1),
    )


def apply_integrated_level_pca(
    fit: PaperPcaFit,
    values: NDArray[np.float64],
    *,
    contract: G2Contract,
) -> NDArray[np.float64]:
    """Apply a stored integrated-level PCA fit using its training means."""
    validate_g2_contract(contract)
    if type(fit) is not PaperPcaFit:
        raise TypeError("fit must use exact PaperPcaFit")
    array = _require_float64_array(values, name="values", ndim=2)
    if array.shape[1] != fit.training_means.shape[0]:
        raise ValueError("values shape must match the PCA loading width")
    l1_norm = np.float64(fit.loading_l1_norm)
    if not np.isfinite(l1_norm) or l1_norm <= 0.0:
        raise ValueError("PCA loading L1 norm must be positive and finite")
    centered = np.asarray(array - fit.training_means, dtype=np.float64, order="C")
    scores = np.asarray((centered @ fit.loading) / l1_norm, dtype=np.float64, order="C")
    _assert_all_finite(centered, name="PCA application centering")
    _assert_all_finite(scores, name="integrated PCA scores")
    return _readonly_c_float64(scores)


def apply_cross_sectional_pca(
    fit: PaperPcaFit,
    values: NDArray[np.float64],
    *,
    contract: G2Contract,
) -> PaperCrossSectionProjection:
    """Apply a stored cross-sectional PCA fit using its training means."""
    validate_g2_contract(contract)
    if type(fit) is not PaperPcaFit:
        raise TypeError("fit must use exact PaperPcaFit")
    array = _require_float64_array(values, name="values", ndim=2)
    if array.shape[1] != fit.training_means.shape[0]:
        raise ValueError("values shape must match the PCA loading width")
    centered = np.asarray(array - fit.training_means, dtype=np.float64, order="C")
    scores = np.asarray(centered @ fit.loading, dtype=np.float64, order="C")
    residuals = np.asarray(centered - np.outer(scores, fit.loading), dtype=np.float64, order="C")
    _assert_all_finite(centered, name="cross-sectional PCA centering")
    _assert_all_finite(scores, name="cross-sectional PCA scores")
    _assert_all_finite(residuals, name="cross-sectional PCA residuals")
    return PaperCrossSectionProjection(
        scores=_readonly_c_float64(scores),
        residuals=_readonly_c_float64(residuals),
    )


def fit_full_rank_ols(
    design: NDArray[np.float64],
    response: NDArray[np.float64],
    *,
    contract: G2Contract,
) -> PaperOlsResult:
    """Fit OLS through the sealed full-rank least-squares call."""
    validate_g2_contract(contract)
    x = _require_float64_array(design, name="design", ndim=2)
    y = _require_float64_array(response, name="response", ndim=1)
    if x.shape[0] != y.shape[0]:
        raise ValueError("design and response must have matching rows")
    if x.shape[0] == 0 or x.shape[1] == 0:
        raise ValueError("design must have positive rows and columns")

    rcond = float(np.finfo(np.float64).eps * max(x.shape))
    try:
        coefficients, _, rank, _ = np.linalg.lstsq(x, y, rcond=rcond)
    except np.linalg.LinAlgError as exc:
        raise np.linalg.LinAlgError("OLS least-squares solve failed") from exc
    coefficients = np.asarray(coefficients, dtype=np.float64, order="C")
    _assert_all_finite(coefficients, name="OLS coefficients")
    rank_int = int(rank)
    if rank_int != x.shape[1]:
        raise ValueError("OLS design lost full column rank")

    return PaperOlsResult(
        coefficients=_readonly_c_float64(coefficients),
        rank=rank_int,
        rcond=rcond,
    )


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


def prepare_lasso_problem(
    y_values: NDArray[np.float64],
    penalized_values: NDArray[np.float64],
    *,
    factor: NDArray[np.float64] | None,
    contract: G2Contract,
) -> PaperLassoProblem:
    """Center, scale, optionally factor-residualize, and license active columns."""
    validate_g2_contract(contract)
    y = _require_float64_array(y_values, name="y_values", ndim=1)
    x = _require_float64_array(penalized_values, name="penalized_values", ndim=2)
    if y.shape[0] != x.shape[0]:
        raise ValueError("y_values and penalized_values must have matching rows")
    if y.shape[0] == 0:
        raise ValueError("paper LASSO training arrays must have positive rows")

    n_rows = np.float64(y.shape[0])
    y_mean = np.float64(np.mean(y))
    x_means = np.asarray(np.mean(x, axis=0), dtype=np.float64, order="C")
    y_centered = np.asarray(y - y_mean, dtype=np.float64, order="C")
    x_centered = np.asarray(x - x_means, dtype=np.float64, order="C")
    _assert_all_finite(y_mean, name="y centering")
    _assert_all_finite(x_means, name="x centering")
    _assert_all_finite(y_centered, name="y centering")
    _assert_all_finite(x_centered, name="x centering")

    with np.errstate(over="ignore", invalid="ignore"):
        pre_fwl_rms = np.asarray(
            np.sqrt(np.sum(x_centered * x_centered, axis=0) / n_rows),
            dtype=np.float64,
            order="C",
        )
    _assert_all_finite(pre_fwl_rms, name="pre-FWL RMS")
    pre_scale_active = pre_fwl_rms != 0.0
    x_scaled = np.empty_like(x_centered)
    x_scaled[:, pre_scale_active] = x_centered[:, pre_scale_active] / pre_fwl_rms[pre_scale_active]
    x_scaled[:, ~pre_scale_active] = np.float64(0.0)
    _assert_all_finite(x_scaled, name="pre-FWL scaling")

    factor_mean: float | None = None
    factor_sum_squares: float | None = None
    factor_centered: NDArray[np.float64] | None = None
    y_res = y_centered.copy()
    x_res_all = x_scaled.copy()
    if factor is not None:
        factor_values = _require_float64_array(factor, name="factor", ndim=1)
        if factor_values.shape[0] != y.shape[0]:
            raise ValueError("factor must have matching rows")
        factor_mean_value = np.float64(np.mean(factor_values))
        centered_factor = np.asarray(factor_values - factor_mean_value, dtype=np.float64, order="C")
        with np.errstate(over="ignore", invalid="ignore"):
            factor_ss = np.float64(np.dot(centered_factor, centered_factor))
        _assert_all_finite(factor_mean_value, name="factor centering")
        _assert_all_finite(centered_factor, name="factor centering")
        if not np.isfinite(factor_ss) or factor_ss <= 0.0:
            raise ValueError("factor variance sum of squares must be positive and finite")
        y_factor_slope = np.float64(np.dot(centered_factor, y_centered) / factor_ss)
        y_res = np.asarray(
            y_centered - y_factor_slope * centered_factor,
            dtype=np.float64,
            order="C",
        )
        active_scaled = x_scaled[:, pre_scale_active]
        x_factor_slopes = np.asarray(
            (centered_factor @ active_scaled) / factor_ss,
            dtype=np.float64,
            order="C",
        )
        x_res_all[:, pre_scale_active] = np.asarray(
            active_scaled - np.outer(centered_factor, x_factor_slopes),
            dtype=np.float64,
            order="C",
        )
        _assert_all_finite(y_factor_slope, name="factor FWL")
        _assert_all_finite(x_factor_slopes, name="factor FWL")
        _assert_all_finite(y_res, name="factor FWL")
        _assert_all_finite(x_res_all, name="factor FWL")
        factor_mean = float(factor_mean_value)
        factor_sum_squares = float(factor_ss)
        factor_centered = _readonly_c_float64(centered_factor)

    with np.errstate(over="ignore", invalid="ignore"):
        post_fwl_squared_norm = np.asarray(
            np.sum(x_res_all * x_res_all, axis=0) / n_rows,
            dtype=np.float64,
            order="C",
        )
    _assert_all_finite(post_fwl_squared_norm, name="post-FWL squared norm")
    cutoff = np.float64(
        contract.paper_reconstruction.post_fwl_zero_norm_multiplier * np.finfo(np.float64).eps
    )
    active_columns = np.asarray(pre_scale_active & (post_fwl_squared_norm > cutoff), dtype=np.bool_)
    x_res = np.asarray(x_res_all[:, active_columns], dtype=np.float64, order="C")
    _assert_all_finite(x_res, name="active post-FWL design")
    if x_res.shape[1] == 0:
        lambda_max = 0.0
    else:
        correlations = np.asarray((x_res.T @ y_res) / n_rows, dtype=np.float64, order="C")
        _assert_all_finite(correlations, name="lambda_max")
        lambda_max = float(np.max(np.abs(correlations)))
        if not math.isfinite(lambda_max):
            raise FloatingPointError("lambda_max produced nonfinite intermediate arithmetic")

    return PaperLassoProblem(
        y_mean=float(y_mean),
        x_means=_readonly_c_float64(x_means),
        pre_fwl_rms=_readonly_c_float64(pre_fwl_rms),
        active_columns=_readonly_c_bool(active_columns),
        y_centered=_readonly_c_float64(y_centered),
        x_centered=_readonly_c_float64(x_centered),
        factor_mean=factor_mean,
        factor_sum_squares=factor_sum_squares,
        factor_centered=factor_centered,
        y_res=_readonly_c_float64(y_res),
        x_res=_readonly_c_float64(x_res),
        lambda_max=lambda_max,
    )


def reconstruct_lasso_coefficients(
    problem: PaperLassoProblem,
    active_coefficients: NDArray[np.float64],
    *,
    contract: G2Contract,
) -> PaperLinearCoefficients:
    """Map active scaled/FWL LASSO coefficients back to original linear units."""
    validate_g2_contract(contract)
    if type(problem) is not PaperLassoProblem:
        raise TypeError("problem must use exact PaperLassoProblem")
    coefficients = _require_float64_array(active_coefficients, name="active_coefficients", ndim=1)
    active_count = int(np.count_nonzero(problem.active_columns))
    if coefficients.shape != (active_count,):
        raise ValueError("active_coefficients shape must match active columns")

    penalized = np.zeros(problem.x_means.shape[0], dtype=np.float64)
    if active_count:
        penalized[problem.active_columns] = (
            coefficients / problem.pre_fwl_rms[problem.active_columns]
        )
    _assert_all_finite(penalized, name="coefficient reconstruction")

    factor_coefficient: float | None = None
    if problem.factor_centered is not None:
        if problem.factor_sum_squares is None or problem.factor_mean is None:
            raise ValueError("problem factor metadata is incomplete")
        factor_ss = np.float64(problem.factor_sum_squares)
        if not np.isfinite(factor_ss) or factor_ss <= 0.0:
            raise ValueError("problem factor variance sum of squares must be positive and finite")
        residual_after_penalized = np.asarray(
            problem.y_centered - problem.x_centered @ penalized,
            dtype=np.float64,
            order="C",
        )
        factor_value = np.float64(
            np.dot(problem.factor_centered, residual_after_penalized) / factor_ss
        )
        _assert_all_finite(residual_after_penalized, name="factor coefficient reconstruction")
        _assert_all_finite(factor_value, name="factor coefficient reconstruction")
        if factor_value == 0.0:
            factor_value = np.float64(0.0)
        factor_coefficient = float(factor_value)

    intercept = np.float64(problem.y_mean - np.dot(penalized, problem.x_means))
    if factor_coefficient is not None:
        if problem.factor_mean is None:
            raise ValueError("problem factor metadata is incomplete")
        intercept = np.float64(intercept - np.float64(factor_coefficient * problem.factor_mean))
    _assert_all_finite(intercept, name="intercept reconstruction")

    return PaperLinearCoefficients(
        intercept=float(intercept),
        factor_coefficient=factor_coefficient,
        penalized_coefficients=_readonly_c_float64(penalized),
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
