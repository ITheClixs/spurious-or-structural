"""Size and power of the date-cluster cross-block test.

Generates the Section 2 and Section 3 tables of
``docs/derivations/CROSS_BLOCK_INFERENCE.md``: the size of the date-cluster
bootstrap against the procedure that treats bins as independent, and the power
curve against dense off-diagonal alternatives.

The independent-bin scheme is implemented here for one purpose — to show it
rejects a true null in every replication. It is not offered as an option.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from xid.models.cross_block_inference import (
    DateStatistics,
    accumulate_dates,
    cross_block_pvalue,
    weighted_coefficients,
)

__all__ = (
    "SimulationDesign",
    "independent_bin_pvalue",
    "rejection_rate",
    "simulate_panel",
)

Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class SimulationDesign:
    """One simulated panel design."""

    assets: int = 20
    factors: int = 2
    dates: int = 50
    bins: int = 100
    persistence: float = 0.6
    """AR(1) coefficient within a date. Dates are independent of one another."""

    cross_impact: float = 0.0
    """Largest off-diagonal entry added to a diagonal ``Lambda``; zero is the null."""

    def __post_init__(self) -> None:
        if not 0.0 <= self.persistence < 1.0:
            raise ValueError("persistence: expected a value in [0, 1)")
        if self.cross_impact < 0.0:
            raise ValueError("cross_impact: expected a nonnegative alternative size")
        if self.dates < 2 or self.bins < 1 or self.assets < 2 or self.factors < 1:
            raise ValueError("expected at least two dates, two assets, one bin, one factor")


def _persistent(rng: np.random.Generator, bins: int, width: int, rho: float) -> Matrix:
    innovations = rng.normal(size=(bins, width))
    series = np.zeros((bins, width))
    for t in range(1, bins):
        series[t] = rho * series[t - 1] + innovations[t]
    return series


def simulate_panel(design: SimulationDesign, rng: np.random.Generator) -> DateStatistics:
    """Simulate ``r = Lambda q + Gamma f + u``, ``q = Delta f + v`` with within-date AR(1)."""
    n, k = design.assets, design.factors
    impact = np.diag(rng.uniform(0.2, 0.4, n))
    if design.cross_impact > 0.0:
        offdiagonal = rng.normal(size=(n, n))
        np.fill_diagonal(offdiagonal, 0.0)
        impact = impact + design.cross_impact * offdiagonal / np.abs(offdiagonal).max()
    priced = rng.normal(size=(n, k)) * 0.5
    loading = rng.normal(size=(n, k)) * 0.5

    returns = np.empty((design.dates, design.bins, n))
    flow = np.empty((design.dates, design.bins, n))
    for d in range(design.dates):
        factors = _persistent(rng, design.bins, k, design.persistence)
        flow[d] = factors @ loading.T + _persistent(rng, design.bins, n, design.persistence)
        returns[d] = (
            flow[d] @ impact.T
            + factors @ priced.T
            + _persistent(rng, design.bins, n, design.persistence)
        )
    return accumulate_dates(np.ascontiguousarray(returns), np.ascontiguousarray(flow))


def independent_bin_pvalue(
    statistics: DateStatistics,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    k: int,
    generator: np.random.Generator,
    bins: int,
    draws: int = 299,
) -> float:
    """The p-value implied by treating bins, not dates, as the sampling unit.

    Reported only to demonstrate its failure: under within-day dependence it
    rejects a true null in essentially every replication.
    """
    observed_block = weighted_coefficients(statistics)[np.ix_(list(rows), list(columns))]
    left, singular, right = np.linalg.svd(observed_block)
    observed = float(singular[k])
    truncated = singular.copy()
    truncated[k:] = 0.0
    null_block = (left[:, : truncated.size] * truncated) @ right

    dates = statistics.date_count
    uniform = np.full(dates, 1.0 / dates)
    exceedances = 0
    for _ in range(draws):
        weights = generator.multinomial(dates * bins, uniform) / float(bins)
        block = weighted_coefficients(statistics, weights)[np.ix_(list(rows), list(columns))]
        resampled = float(np.linalg.svd(null_block + block - observed_block, compute_uv=False)[k])
        if resampled >= observed:
            exceedances += 1
    return exceedances / draws


def rejection_rate(
    design: SimulationDesign,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    replications: int,
    level: float = 0.05,
    scheme: str = "date",
    seed: int = 4242,
    panel_seed: int = 9000,
    draws: int = 299,
) -> float:
    """Monte Carlo rejection rate of the cross-block test at ``level``."""
    if scheme not in {"date", "independent-bin"}:
        raise ValueError(f"scheme: expected 'date' or 'independent-bin', got {scheme!r}")
    if not 0.0 < level < 1.0:
        raise ValueError("level: expected a nominal level strictly between zero and one")
    if replications < 1:
        raise ValueError("replications: expected at least one replication")
    bootstrap_rng = np.random.default_rng(seed)
    rejections = 0
    for replication in range(replications):
        statistics = simulate_panel(design, np.random.default_rng(panel_seed + replication))
        if scheme == "date":
            p_value = cross_block_pvalue(
                statistics, rows, columns, design.factors, bootstrap_rng, draws=draws
            ).p_value
        else:
            p_value = independent_bin_pvalue(
                statistics, rows, columns, design.factors, bootstrap_rng, design.bins, draws=draws
            )
        if p_value <= level:
            rejections += 1
    return rejections / replications
