"""Semantic paper-matrix assembly for one date.

This module implements the A031 derivation in
``docs/derivations/GATE_G2_PAPER_ASSEMBLY.md``: the composition from the already
implemented paper kernels to the nine cached matrices and the six-by-thirty
SSE/SST table that the A027 codec consumes.

It composes existing kernels and adds no estimator. It constructs no
random-number generator, reads no market data, writes no artifact, and opens no
registered stream. A date that cannot be assembled cleanly fails; no cell is
dropped, averaged over, or filled.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from xid.models.g2_paper import (
    PaperFeatureBlock,
    PaperFeatureTransform,
    PaperLassoProblem,
    apply_paper_feature_transform,
    fit_full_rank_ols,
    fit_paper_feature_transform,
    prepare_lasso_problem,
    reconstruct_lasso_coefficients,
    select_lasso_ratio,
    solve_lasso_coordinate_descent,
)
from xid.models.g2_paper_cache import PaperResearchDateCache
from xid.sim.g2 import G2Contract

Matrix = NDArray[np.float64]
Vector = NDArray[np.float64]

PAPER_ASSEMBLY_SPEC_ORDER = ("PI_1", "PI_I", "CI_1", "CI_I", "PI_CC", "CI_CC")
_OWN_FLOW_SPECS = frozenset({"PI_1", "PI_I", "PI_CC"})
_LASSO_SPECS = frozenset({"CI_1", "CI_I", "CI_CC"})

__all__ = (
    "PAPER_ASSEMBLY_SPEC_ORDER",
    "PaperDatePanel",
    "assemble_paper_date",
)


@dataclass(frozen=True, slots=True)
class PaperDatePanel:
    """One date of issued level flows and returns, in sealed bin order."""

    level_flows: NDArray[np.float64]
    returns: NDArray[np.float64]


def _require(name: str, array: NDArray[np.float64], shape: tuple[int, ...]) -> None:
    if not isinstance(array, np.ndarray) or type(array) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray")
    if array.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {array.dtype}")
    if array.shape != shape:
        raise ValueError(f"{name}: expected shape {shape}, got {array.shape}")
    if not np.isfinite(array).all():
        raise ValueError(f"{name}: expected finite entries")


def _validate_panel(panel: PaperDatePanel, contract: G2Contract) -> None:
    bins = contract.bins_per_date
    assets = contract.n_assets
    levels = contract.n_levels
    paper = contract.paper_reconstruction
    required = paper.fit_window_bins * (paper.eligible_fit_blocks_per_date + 1)
    if bins != required:
        raise ValueError("contract bins per date disagree with the block schedule")
    if getattr(panel.returns, "shape", None) != (bins, assets):
        raise ValueError(
            f"returns: expected {bins} bins by {assets} assets, "
            f"got {getattr(panel.returns, 'shape', None)}"
        )
    _require("level_flows", panel.level_flows, (bins, assets, levels))
    _require("returns", panel.returns, (bins, assets))


def _features(
    transform: PaperFeatureTransform,
    level_flows: Matrix,
    contract: G2Contract,
) -> PaperFeatureBlock:
    return apply_paper_feature_transform(transform, level_flows, contract=contract)


def _design(spec: str, block: PaperFeatureBlock, response: int) -> Matrix:
    rows = block.best_level_flows.shape[0]
    ones = np.ones((rows, 1), dtype=np.float64)
    if spec == "PI_1":
        return np.hstack((ones, block.best_level_flows[:, response : response + 1]))
    if spec == "PI_I":
        return np.hstack((ones, block.integrated_flows[:, response : response + 1]))
    if spec == "PI_CC":
        return np.hstack(
            (
                ones,
                block.cross_section_factor.reshape(rows, 1),
                block.cross_section_residuals[:, response : response + 1],
            )
        )
    raise ValueError(f"spec {spec} is not an ordinary-least-squares specification")


def _penalized(spec: str, block: PaperFeatureBlock) -> Matrix:
    if spec == "CI_1":
        return np.ascontiguousarray(block.best_level_flows)
    if spec == "CI_I":
        return np.ascontiguousarray(block.integrated_flows)
    if spec == "CI_CC":
        return np.ascontiguousarray(block.cross_section_residuals)
    raise ValueError(f"spec {spec} is not a penalized specification")


def _factor(spec: str, block: PaperFeatureBlock) -> Vector | None:
    if spec == "CI_CC":
        return np.ascontiguousarray(block.cross_section_factor)
    return None


def _scatter(problem: PaperLassoProblem, active: Vector, n_assets: int) -> Vector:
    """Place active-column coefficients back into the full flow vector."""
    mask = np.asarray(problem.active_columns) != 0
    full = np.zeros(n_assets, dtype=np.float64)
    if active.shape[0] == n_assets:
        full[:] = active
        return full
    full[mask] = active
    return full


def _lasso_fit(
    spec: str,
    train: PaperFeatureBlock,
    y_train: Vector,
    response: int,
    contract: G2Contract,
    fold_blocks: list[tuple[PaperFeatureBlock, Matrix, PaperFeatureBlock, Matrix]],
) -> tuple[float, Vector, float]:
    """Return ``(intercept, flow coefficients, factor coefficient)``."""
    grid = contract.lasso_ratio_grid
    n_assets = contract.n_assets
    fold_sse = np.zeros((len(fold_blocks), len(grid)), dtype=np.float64)

    for fold_index, (f_train, fy_all, f_valid, vy_all) in enumerate(fold_blocks):
        fy = np.ascontiguousarray(fy_all[:, response])
        vy = np.ascontiguousarray(vy_all[:, response])
        problem = prepare_lasso_problem(
            fy,
            _penalized(spec, f_train),
            factor=_factor(spec, f_train),
            contract=contract,
        )
        warm: Vector | None = None
        for ratio_index, ratio in enumerate(grid):
            solution = solve_lasso_coordinate_descent(
                problem.x_res,
                problem.y_res,
                lambda_value=float(ratio) * float(problem.lambda_max),
                initial_coefficients=warm,
                contract=contract,
            )
            warm = solution.coefficients
            linear = reconstruct_lasso_coefficients(
                problem, solution.coefficients, contract=contract
            )
            flows = _scatter(problem, linear.penalized_coefficients, n_assets)
            prediction = linear.intercept + _penalized(spec, f_valid) @ flows
            if linear.factor_coefficient is not None:
                factor = _factor(spec, f_valid)
                assert factor is not None
                prediction = prediction + linear.factor_coefficient * factor
            residual = vy - prediction
            fold_sse[fold_index, ratio_index] = float(residual @ residual)

    selection = select_lasso_ratio(fold_sse, contract=contract)
    outer = prepare_lasso_problem(
        y_train,
        _penalized(spec, train),
        factor=_factor(spec, train),
        contract=contract,
    )
    solution = solve_lasso_coordinate_descent(
        outer.x_res,
        outer.y_res,
        lambda_value=selection.selected_ratio * float(outer.lambda_max),
        initial_coefficients=None,
        contract=contract,
    )
    linear = reconstruct_lasso_coefficients(outer, solution.coefficients, contract=contract)
    flows = _scatter(outer, linear.penalized_coefficients, n_assets)
    factor_coefficient = (
        0.0 if linear.factor_coefficient is None else float(linear.factor_coefficient)
    )
    return float(linear.intercept), flows, factor_coefficient


def assemble_paper_date(
    panel: PaperDatePanel,
    *,
    contract: G2Contract,
    _sst_from_scored_mean: bool = False,
    _average_before_product: bool = False,
) -> PaperResearchDateCache:
    """Assemble one date into the sealed nine-matrix, six-loss-table cache.

    The two leading-underscore switches exist solely so the registered A031
    predictions can demonstrate that the benchmark rule and the
    product-before-averaging order are load-bearing. They are not part of the
    contract and must never be enabled in a registered run.
    """
    _validate_panel(panel, contract)
    paper = contract.paper_reconstruction
    n_assets = contract.n_assets
    width = paper.fit_window_bins
    n_blocks = paper.eligible_fit_blocks_per_date

    sums: dict[str, Matrix] = {
        name: np.zeros((n_assets, n_assets), dtype=np.float64)
        for name in (
            "PI_1",
            "PI_I",
            "CI_1",
            "CI_I",
            "PI_CC_purged",
            "CI_CC_purged",
            "PI_CC_full",
            "CI_CC_full",
        )
    }
    projection_sum = np.zeros((n_assets, n_assets), dtype=np.float64)
    purged_blocks: dict[str, list[Matrix]] = {"PI_CC": [], "CI_CC": []}
    factor_blocks: dict[str, list[Vector]] = {"PI_CC": [], "CI_CC": []}
    projections: list[Matrix] = []
    losses = np.zeros((len(PAPER_ASSEMBLY_SPEC_ORDER), n_assets, 2), dtype=np.float64)

    for block_index in range(n_blocks):
        train = slice(block_index * width, (block_index + 1) * width)
        score = slice((block_index + 1) * width, (block_index + 2) * width)
        transform = fit_paper_feature_transform(
            np.ascontiguousarray(panel.level_flows[train]), contract=contract
        )
        train_block = _features(transform, np.ascontiguousarray(panel.level_flows[train]), contract)
        score_block = _features(transform, np.ascontiguousarray(panel.level_flows[score]), contract)
        y_train = np.ascontiguousarray(panel.returns[train])
        y_score = np.ascontiguousarray(panel.returns[score])

        fold_cache: list[tuple[PaperFeatureBlock, Matrix, PaperFeatureBlock, Matrix]] = []
        raw_train = np.ascontiguousarray(panel.level_flows[train])
        for start, stop in paper.cv_validation_ranges:
            mask = np.ones(width, dtype=bool)
            mask[start:stop] = False
            fold_transform = fit_paper_feature_transform(
                np.ascontiguousarray(raw_train[mask]), contract=contract
            )
            fold_cache.append(
                (
                    _features(fold_transform, np.ascontiguousarray(raw_train[mask]), contract),
                    np.ascontiguousarray(y_train[mask]),
                    _features(fold_transform, np.ascontiguousarray(raw_train[~mask]), contract),
                    np.ascontiguousarray(y_train[~mask]),
                )
            )

        block_purged: dict[str, Matrix] = {
            "PI_CC": np.zeros((n_assets, n_assets), dtype=np.float64),
            "CI_CC": np.zeros((n_assets, n_assets), dtype=np.float64),
        }
        block_factor: dict[str, Vector] = {
            "PI_CC": np.zeros(n_assets, dtype=np.float64),
            "CI_CC": np.zeros(n_assets, dtype=np.float64),
        }

        for spec_index, spec in enumerate(PAPER_ASSEMBLY_SPEC_ORDER):
            for response in range(n_assets):
                y_tr = np.ascontiguousarray(y_train[:, response])
                y_sc = np.ascontiguousarray(y_score[:, response])

                if spec in _LASSO_SPECS:
                    intercept, flows, factor_coefficient = _lasso_fit(
                        spec, train_block, y_tr, response, contract, fold_cache
                    )
                    prediction = intercept + _penalized(spec, score_block) @ flows
                    if spec == "CI_CC":
                        prediction = (
                            prediction + factor_coefficient * score_block.cross_section_factor
                        )
                else:
                    result = fit_full_rank_ols(
                        _design(spec, train_block, response), y_tr, contract=contract
                    )
                    coefficients = np.asarray(result.coefficients, dtype=np.float64)
                    prediction = _design(spec, score_block, response) @ coefficients
                    intercept = float(coefficients[0])
                    flows = np.zeros(n_assets, dtype=np.float64)
                    if spec == "PI_CC":
                        factor_coefficient = float(coefficients[1])
                        flows[response] = float(coefficients[2])
                    else:
                        factor_coefficient = 0.0
                        flows[response] = float(coefficients[1])

                if not np.isfinite(prediction).all():
                    raise ValueError(f"{spec} response {response}: nonfinite prediction")

                benchmark = float(np.mean(y_sc)) if _sst_from_scored_mean else float(np.mean(y_tr))
                residual = y_sc - prediction
                deviation = y_sc - benchmark
                sse = float(residual @ residual)
                sst = float(deviation @ deviation)
                if not np.isfinite(sse) or not np.isfinite(sst):
                    raise ValueError(f"{spec} response {response}: nonfinite loss")
                losses[spec_index, response, 0] += sse
                losses[spec_index, response, 1] += sst

                if spec in ("PI_CC", "CI_CC"):
                    block_purged[spec][response, :] = flows
                    block_factor[spec][response] = factor_coefficient
                else:
                    sums[spec][response, :] += flows

        loading = np.asarray(transform.cross_section_fit.loading, dtype=np.float64).reshape(
            n_assets
        )
        p_perp = np.eye(n_assets, dtype=np.float64) - np.outer(loading, loading)
        projection_sum += p_perp
        projections.append(p_perp)
        for spec in ("PI_CC", "CI_CC"):
            key = f"{spec}_purged"
            sums[key] += block_purged[spec]
            purged_blocks[spec].append(block_purged[spec].copy())
            factor_blocks[spec].append(block_factor[spec].copy())
            if not _average_before_product:
                sums[f"{spec}_full"] += block_purged[spec] @ p_perp + np.outer(
                    block_factor[spec], loading
                )

    divisor = float(n_blocks)
    if _average_before_product:
        mean_projection = projection_sum / divisor
        mean_loading = np.zeros(n_assets, dtype=np.float64)
        for block in projections:
            mean_loading += np.sqrt(np.clip(np.diag(np.eye(n_assets) - block), 0.0, None))
        mean_loading /= divisor
        for spec in ("PI_CC", "CI_CC"):
            mean_purged = sums[f"{spec}_purged"] / divisor
            mean_factor = np.mean(np.vstack(factor_blocks[spec]), axis=0)
            sums[f"{spec}_full"] = divisor * (
                mean_purged @ mean_projection + np.outer(mean_factor, mean_loading)
            )

    if float(np.min(losses[:, :, 1])) <= 0.0:
        raise ValueError("assembly: an sst of zero leaves the loss ratio undefined")

    def _mean(key: str) -> Matrix:
        return np.ascontiguousarray(sums[key] / divisor, dtype=np.float64)

    cache = PaperResearchDateCache(
        pi_1_direct=_mean("PI_1"),
        pi_i_direct=_mean("PI_I"),
        ci_1_direct=_mean("CI_1"),
        ci_i_direct=_mean("CI_I"),
        pi_cc_purged=_mean("PI_CC_purged"),
        ci_cc_purged=_mean("CI_CC_purged"),
        pi_cc_full_response=_mean("PI_CC_full"),
        ci_cc_full_response=_mean("CI_CC_full"),
        cc_mean_projection_p_perp=np.ascontiguousarray(projection_sum / divisor, dtype=np.float64),
        losses=np.ascontiguousarray(losses, dtype=np.float64),
    )
    for name in (
        "pi_1_direct",
        "pi_i_direct",
        "ci_1_direct",
        "ci_i_direct",
        "pi_cc_purged",
        "ci_cc_purged",
        "pi_cc_full_response",
        "ci_cc_full_response",
        "cc_mean_projection_p_perp",
        "losses",
    ):
        if not np.isfinite(getattr(cache, name)).all():
            raise ValueError(f"assembly: {name} contains a nonfinite entry")
    return cache
