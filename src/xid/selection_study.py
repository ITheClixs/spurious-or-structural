"""Where cross-validation actually lands on the sealed penalty grid.

The registered protocol requires fold paths to warm-start but every outer refit
to begin at zero, and from zero the smallest sealed ratio fails at the
10,000-sweep cap. Whether that ever matters depends on whether cross-validation
ever selects a penalty in the failing region.

The selection rule takes the *first* ratio within tolerance of the pooled
minimum, which biases toward large penalties and therefore low indices, so the
failing region may never be reached. This module measures it rather than
assuming either way.

It changes no registered numeric and opens no registered stream. Parallelism is
across independent blocks and specifications, which alters nothing about any
individual result.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from dataclasses import dataclass
from multiprocessing import get_context
from pathlib import Path
from typing import Any

# The sealed configuration pins single-threaded BLAS; workers must match it
# before NumPy is imported anywhere in the child process.
for _variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ.setdefault(_variable, "1")

import numpy as np  # noqa: E402
from numpy.typing import NDArray  # noqa: E402

FIXTURE_SEED = 1729
SAMPLED_BLOCKS = (0, 4, 9)
SAMPLED_SPECS = ("CI_1", "CI_I", "CI_CC")
FAILING_REGION_THRESHOLD = 39

SCOPE = "deterministic measurement on a synthetic panel at test seed 1729; not a market claim"


@dataclass(frozen=True, slots=True)
class CellResult:
    """Selected ratio indices for one block and specification."""

    block_index: int
    specification: str
    selected_indices: tuple[int, ...]
    outer_refit_failures: int
    fold_solve_failures: int
    responses_skipped: int


def synthetic_panel(root: Path) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Build the same synthetic issued panel the assembly tests use."""
    from xid.sim.g2 import load_g2_contract

    contract = load_g2_contract(root)
    assets = contract.n_assets
    levels = contract.n_levels
    bins = contract.bins_per_date
    rng = np.random.default_rng(FIXTURE_SEED)
    common = rng.normal(size=(bins, 1))
    level_flows = 0.6 * common[:, :, None] + rng.normal(size=(bins, assets, levels)) * 0.4
    best = level_flows[:, :, contract.paper_reconstruction.best_level_index]
    returns = 0.3 * best + 0.5 * common + rng.normal(size=(bins, assets)) * 0.2
    return (
        np.ascontiguousarray(level_flows, dtype=np.float64),
        np.ascontiguousarray(returns, dtype=np.float64),
    )


def _cell(args: tuple[str, int, str]) -> CellResult:
    """Run one block-and-specification cell in a worker process."""
    root_text, block_index, specification = args
    root = Path(root_text)

    from xid.models.g2_assembly import _factor, _penalized
    from xid.models.g2_paper import (
        apply_paper_feature_transform,
        fit_paper_feature_transform,
        prepare_lasso_problem,
        reconstruct_lasso_coefficients,
        select_lasso_ratio,
        solve_lasso_coordinate_descent,
    )
    from xid.sim.g2 import load_g2_contract

    contract = load_g2_contract(root)
    paper = contract.paper_reconstruction
    width = paper.fit_window_bins
    grid = contract.lasso_ratio_grid
    level_flows, returns = synthetic_panel(root)

    train = slice(block_index * width, (block_index + 1) * width)
    raw_train = np.ascontiguousarray(level_flows[train])
    y_train = np.ascontiguousarray(returns[train])

    folds = []
    for start, stop in paper.cv_validation_ranges:
        mask = np.ones(width, dtype=bool)
        mask[start:stop] = False
        fold_transform = fit_paper_feature_transform(
            np.ascontiguousarray(raw_train[mask]), contract=contract
        )
        folds.append(
            (
                apply_paper_feature_transform(
                    fold_transform, np.ascontiguousarray(raw_train[mask]), contract=contract
                ),
                np.ascontiguousarray(y_train[mask]),
                apply_paper_feature_transform(
                    fold_transform, np.ascontiguousarray(raw_train[~mask]), contract=contract
                ),
                np.ascontiguousarray(y_train[~mask]),
            )
        )

    outer_transform = fit_paper_feature_transform(raw_train, contract=contract)
    outer_block = apply_paper_feature_transform(outer_transform, raw_train, contract=contract)

    selected: list[int] = []
    failures = 0
    fold_failures = 0
    skipped = 0
    for response in range(contract.n_assets):
        fold_sse = np.zeros((len(folds), len(grid)), dtype=np.float64)
        for fold_index, (fit_block, fit_y, valid_block, valid_y) in enumerate(folds):
            problem = prepare_lasso_problem(
                np.ascontiguousarray(fit_y[:, response]),
                _penalized(specification, fit_block),
                factor=_factor(specification, fit_block),
                contract=contract,
            )
            warm: NDArray[np.float64] | None = None
            for ratio_index, ratio in enumerate(grid):
                try:
                    solution = solve_lasso_coordinate_descent(
                        problem.x_res,
                        problem.y_res,
                        lambda_value=float(ratio) * float(problem.lambda_max),
                        initial_coefficients=warm,
                        contract=contract,
                    )
                except RuntimeError:
                    # A nonconverged fold solve is the measurement, not an
                    # error to hide. Mark the cell and stop this fold path.
                    fold_failures += 1
                    fold_sse[fold_index, ratio_index:] = np.inf
                    break
                warm = solution.coefficients
                linear = reconstruct_lasso_coefficients(
                    problem, solution.coefficients, contract=contract
                )
                mask = np.asarray(problem.active_columns) != 0
                flows = np.zeros(contract.n_assets, dtype=np.float64)
                coefficients = linear.penalized_coefficients
                if coefficients.shape[0] == contract.n_assets:
                    flows[:] = coefficients
                else:
                    flows[mask] = coefficients
                prediction = linear.intercept + _penalized(specification, valid_block) @ flows
                if linear.factor_coefficient is not None:
                    factor = _factor(specification, valid_block)
                    assert factor is not None
                    prediction = prediction + linear.factor_coefficient * factor
                residual = np.ascontiguousarray(valid_y[:, response]) - prediction
                fold_sse[fold_index, ratio_index] = float(residual @ residual)

        if not np.isfinite(fold_sse).all():
            # select_lasso_ratio cannot rank a path containing a failure.
            skipped += 1
            continue
        selection = select_lasso_ratio(fold_sse, contract=contract)
        selected.append(selection.selected_index)

        # The registered outer refit begins at zero; record whether it survives.
        outer = prepare_lasso_problem(
            np.ascontiguousarray(y_train[:, response]),
            _penalized(specification, outer_block),
            factor=_factor(specification, outer_block),
            contract=contract,
        )
        try:
            solve_lasso_coordinate_descent(
                outer.x_res,
                outer.y_res,
                lambda_value=selection.selected_ratio * float(outer.lambda_max),
                initial_coefficients=None,
                contract=contract,
            )
        except RuntimeError:
            failures += 1

    return CellResult(
        block_index=block_index,
        specification=specification,
        selected_indices=tuple(selected),
        outer_refit_failures=failures,
        fold_solve_failures=fold_failures,
        responses_skipped=skipped,
    )


def run_study(root: Path, workers: int) -> dict[str, Any]:
    """Measure the selected-ratio distribution over the sampled cells."""
    from xid.sim.g2 import load_g2_contract

    contract = load_g2_contract(root)
    jobs = [
        (str(root), block, specification)
        for block in SAMPLED_BLOCKS
        for specification in SAMPLED_SPECS
    ]
    context = get_context("spawn")
    with context.Pool(processes=workers) as pool:
        results = pool.map(_cell, jobs)

    counts: Counter[int] = Counter()
    failures = 0
    fold_failures = 0
    skipped = 0
    per_cell = []
    for result in sorted(results, key=lambda r: (r.block_index, r.specification)):
        counts.update(result.selected_indices)
        failures += result.outer_refit_failures
        fold_failures += result.fold_solve_failures
        skipped += result.responses_skipped
        per_cell.append(
            {
                "block": result.block_index,
                "specification": result.specification,
                "max_selected_index": (
                    max(result.selected_indices) if result.selected_indices else None
                ),
                "outer_refit_failures": result.outer_refit_failures,
                "fold_solve_failures": result.fold_solve_failures,
                "responses_skipped": result.responses_skipped,
            }
        )

    grid_size = len(contract.lasso_ratio_grid)
    histogram = [int(counts.get(index, 0)) for index in range(grid_size)]
    observed = sorted(counts) or [-1]
    total = max(int(sum(histogram)), 1)
    return {
        "scope": SCOPE,
        "sampled_scope": {
            "blocks": list(SAMPLED_BLOCKS),
            "specifications": list(SAMPLED_SPECS),
            "responses": contract.n_assets,
            "cells_evaluated": total,
        },
        "grid_size": grid_size,
        "selected_index_counts": histogram,
        "min_selected_index": int(observed[0]),
        "max_selected_index": int(observed[-1]),
        "mean_selected_index": round(
            sum(index * count for index, count in counts.items()) / total, 6
        ),
        "failing_region_threshold": FAILING_REGION_THRESHOLD,
        "selections_in_failing_region": int(counts.get(FAILING_REGION_THRESHOLD, 0)),
        "outer_refit_failures": failures,
        "fold_solve_failures": fold_failures,
        "responses_skipped_for_fold_failure": skipped,
        "per_cell": per_cell,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=9)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    payload = run_study(args.root, args.workers)
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    (args.out / "selection_study.json").write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
