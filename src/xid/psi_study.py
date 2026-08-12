"""Confirmatory size and power study for the A030 low-rank departure test.

Running ``python -m xid.psi_study --out DIR`` writes ``psi_study.json``. The
run is deterministic given its registered seeds, but it is slow by design, so
the committed artifact is the object the test suite checks rather than
something regenerated on every invocation.

The design, seeds, replicate counts, and predictions are frozen in
``docs/predictions/PSI_NULL.md``. This module opens no registered stream, reads
no market data, and uses only test seeds.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from xid.models.rank_diagnostic import null_projection, psi_k

Matrix = NDArray[np.float64]

N_ASSETS = 30
N_FACTORS = 3
FIXTURE_SEED = 1729
CONFIRMATORY_SEED = 314159
PILOT_SEED = 9191
REPLICATES = 199
BOOTSTRAP_DRAWS = 199
SIZE_REPLICATES = 150
POWER_REPLICATES = 100
ALPHA = 0.05
FLOW_SHARE = 0.2827
SAMPLE_SIZES = (500, 1000, 2000, 5000)
POWER_SAMPLE_SIZE = 5000
POWER_GRID = (0.05, 0.10, 0.20, 0.40)

SCOPE = (
    "Monte Carlo rejection rates under a homoskedastic, serially independent, "
    "correctly specified sampling model; not a claim about market data"
)


def _regressor_covariance() -> Matrix:
    q1 = N_ASSETS * FLOW_SHARE
    q0 = (N_ASSETS - q1) / (N_ASSETS - 1)
    m = np.full(N_ASSETS, 1.0 / np.sqrt(N_ASSETS))
    sigma: Matrix = q0 * np.eye(N_ASSETS) + (q1 - q0) * np.outer(m, m)
    return sigma


def _null_matrix() -> Matrix:
    rng = np.random.default_rng(FIXTURE_SEED)
    diagonal = np.diag(rng.uniform(0.2, 0.4, N_ASSETS))
    low_rank = (
        rng.normal(size=(N_ASSETS, N_FACTORS)) @ rng.normal(size=(N_FACTORS, N_ASSETS)) * 0.05
    )
    return np.asarray(diagonal + low_rank, dtype=np.float64)


def _perturbation() -> Matrix:
    rng = np.random.default_rng(FIXTURE_SEED)
    _ = rng.uniform(0.2, 0.4, N_ASSETS)
    _ = rng.normal(size=(N_ASSETS, N_FACTORS))
    _ = rng.normal(size=(N_FACTORS, N_ASSETS))
    pert = rng.normal(size=(N_ASSETS, N_ASSETS))
    pert -= np.diag(np.diag(pert))
    return np.asarray(pert / np.linalg.norm(pert), dtype=np.float64)


def _rejection_rate(
    population: Matrix,
    sample_size: int,
    replicates: int,
    seed: int,
    error_scale: float,
) -> float:
    chol = np.linalg.cholesky(np.linalg.inv(_regressor_covariance()))
    rng = np.random.default_rng(seed)

    def draw(scale: float) -> Matrix:
        step: Matrix = (scale / np.sqrt(sample_size)) * (
            rng.normal(size=(N_ASSETS, N_ASSETS)) @ chol.T
        )
        return step

    rejections = 0
    for _ in range(replicates):
        estimate = population + draw(1.0)
        projected = null_projection(estimate, N_FACTORS)
        bootstrap = [
            psi_k(projected + draw(error_scale), N_FACTORS) for _ in range(BOOTSTRAP_DRAWS)
        ]
        critical = float(np.quantile(bootstrap, 1.0 - ALPHA))
        if psi_k(estimate, N_FACTORS) > critical:
            rejections += 1
    return rejections / replicates


def _monte_carlo_standard_error(replicates: int) -> float:
    return float(np.sqrt(ALPHA * (1.0 - ALPHA) / replicates))


def build_study() -> dict[str, Any]:
    """Run the confirmatory size and power study at the registered seeds."""
    population = _null_matrix()
    pert = _perturbation()
    dimension = N_ASSETS + N_FACTORS * (2 * N_ASSETS - N_FACTORS)
    inflation = float(np.sqrt(N_ASSETS**2 / (N_ASSETS**2 - dimension)))

    size_rows = []
    for index, sample_size in enumerate(SAMPLE_SIZES):
        plug_in = _rejection_rate(
            population, sample_size, SIZE_REPLICATES, CONFIRMATORY_SEED + index, 1.0
        )
        inflated = _rejection_rate(
            population,
            sample_size,
            SIZE_REPLICATES,
            CONFIRMATORY_SEED + 100 + index,
            inflation,
        )
        size_rows.append(
            {
                "sample_size": sample_size,
                "observations_per_parameter": round(sample_size / N_ASSETS**2, 4),
                "plug_in_size": plug_in,
                "inflated_size": inflated,
            }
        )

    power_rows = []
    for index, eps in enumerate(POWER_GRID):
        rate = _rejection_rate(
            population + eps * pert,
            POWER_SAMPLE_SIZE,
            POWER_REPLICATES,
            CONFIRMATORY_SEED + 200 + index,
            1.0,
        )
        power_rows.append({"epsilon": eps, "power": rate})

    return {
        "scope": SCOPE,
        "assets": N_ASSETS,
        "factors": N_FACTORS,
        "alpha": ALPHA,
        "bootstrap_draws": BOOTSTRAP_DRAWS,
        "size_replicates": SIZE_REPLICATES,
        "power_replicates": POWER_REPLICATES,
        "confirmatory_seed": CONFIRMATORY_SEED,
        "manifold_dimension": dimension,
        "free_parameters": N_ASSETS**2,
        "variance_inflation_factor": round(inflation, 6),
        "variance_inflation_adopted": False,
        "size_monte_carlo_standard_error": round(_monte_carlo_standard_error(SIZE_REPLICATES), 6),
        "power_monte_carlo_standard_error": round(_monte_carlo_standard_error(POWER_REPLICATES), 6),
        "size": size_rows,
        "power": power_rows,
        "power_sample_size": POWER_SAMPLE_SIZE,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    payload = build_study()
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    (args.out / "psi_study.json").write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
