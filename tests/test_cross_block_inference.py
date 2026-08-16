from __future__ import annotations

import os
from itertools import pairwise

import numpy as np
import pytest

from xid.crossblock_study import SimulationDesign, rejection_rate, simulate_panel
from xid.models.cross_block_inference import (
    DateStatistics,
    accumulate_dates,
    cross_block_pvalue,
    weighted_coefficients,
)

ROWS = (0, 1, 2, 3, 4, 5)
COLUMNS = (10, 11, 12, 13, 14, 15)
SLOW = pytest.mark.skipif(
    os.environ.get("XID_RUN_SLOW_INFERENCE") != "1",
    reason="size and power study is minutes; set XID_RUN_SLOW_INFERENCE=1",
)


def _small(cross: float = 0.0, dates: int = 12) -> SimulationDesign:
    return SimulationDesign(assets=8, factors=1, dates=dates, bins=25, cross_impact=cross)


def _statistics(design: SimulationDesign, seed: int = 5) -> DateStatistics:
    return simulate_panel(design, np.random.default_rng(seed))


# --- the reduction to per-date statistics is exact ----------------------------


def test_accumulated_statistics_reproduce_the_pooled_coefficients() -> None:
    rng = np.random.default_rng(3)
    returns = np.ascontiguousarray(rng.normal(size=(6, 20, 5)))
    flow = np.ascontiguousarray(rng.normal(size=(6, 20, 5)))
    pooled_r = returns.reshape(-1, 5)
    pooled_q = flow.reshape(-1, 5)
    direct = np.linalg.solve((pooled_q.T @ pooled_q).T, (pooled_r.T @ pooled_q).T).T
    assert np.abs(weighted_coefficients(accumulate_dates(returns, flow)) - direct).max() < 1e-10


def test_statistic_is_invariant_to_the_order_of_dates() -> None:
    """A038 prediction 5: date order carries no information."""
    design = _small()
    statistics = _statistics(design)
    shuffled = DateStatistics(
        return_flow=np.ascontiguousarray(statistics.return_flow[::-1]),
        flow=np.ascontiguousarray(statistics.flow[::-1]),
    )
    first = cross_block_pvalue(statistics, (0, 1), (4, 5), 1, np.random.default_rng(1), draws=25)
    second = cross_block_pvalue(shuffled, (0, 1), (4, 5), 1, np.random.default_rng(1), draws=25)
    assert first.statistic == pytest.approx(second.statistic, abs=1e-12)


def test_p_value_is_reproducible_at_a_fixed_seed() -> None:
    statistics = _statistics(_small())
    args = (statistics, (0, 1), (4, 5), 1)
    first = cross_block_pvalue(*args, np.random.default_rng(77), draws=40)
    second = cross_block_pvalue(*args, np.random.default_rng(77), draws=40)
    assert first.p_value == second.p_value


def test_result_reports_the_panel_length_alongside_the_p_value() -> None:
    """A short panel has little power, so D travels with the verdict."""
    result = cross_block_pvalue(
        _statistics(_small(dates=9)), (0, 1), (4, 5), 1, np.random.default_rng(2), draws=30
    )
    assert result.date_count == 9
    assert result.draws == 30
    assert 0.0 <= result.p_value <= 1.0


def test_a_large_alternative_produces_a_small_p_value() -> None:
    statistics = _statistics(_small(cross=0.8, dates=30), seed=6)
    result = cross_block_pvalue(statistics, (0, 1), (4, 5), 1, np.random.default_rng(4), draws=199)
    assert result.p_value < 0.05


# --- registered size and power, opt-in ----------------------------------------


@SLOW
def test_prediction_1_date_cluster_bootstrap_holds_its_level() -> None:
    design = SimulationDesign()
    assert 0.01 <= rejection_rate(design, ROWS, COLUMNS, 200, level=0.05) <= 0.09
    assert 0.05 <= rejection_rate(design, ROWS, COLUMNS, 200, level=0.10) <= 0.15


@SLOW
def test_prediction_2_treating_bins_as_independent_invalidates_the_test() -> None:
    rate = rejection_rate(
        SimulationDesign(), ROWS, COLUMNS, 200, level=0.05, scheme="independent-bin"
    )
    assert rate > 0.5


@SLOW
def test_prediction_3_power_increases_with_the_alternative() -> None:
    rates = [
        rejection_rate(SimulationDesign(cross_impact=c), ROWS, COLUMNS, 150)
        for c in (0.0, 0.05, 0.10, 0.20)
    ]
    assert all(a < b for a, b in pairwise(rates)), rates
    assert rates[2] >= 0.8


@SLOW
def test_prediction_4_a_longer_panel_detects_a_smaller_alternative() -> None:
    short = rejection_rate(SimulationDesign(cross_impact=0.05), ROWS, COLUMNS, 150)
    long = rejection_rate(SimulationDesign(dates=200, cross_impact=0.05), ROWS, COLUMNS, 150)
    assert long - short >= 0.3


# --- fail-closed ---------------------------------------------------------------


def test_rejects_overlapping_index_sets() -> None:
    with pytest.raises(ValueError, match="disjoint"):
        cross_block_pvalue(
            _statistics(_small()), (0, 1), (1, 2), 1, np.random.default_rng(0), draws=5
        )


def test_rejects_a_block_too_small_to_carry_the_restriction() -> None:
    with pytest.raises(ValueError, match="vacuous"):
        cross_block_pvalue(
            _statistics(_small()), (0, 1), (4, 5), 2, np.random.default_rng(0), draws=5
        )


def test_rejects_a_panel_with_one_date() -> None:
    with pytest.raises(ValueError, match="at least two dates"):
        accumulate_dates(np.zeros((1, 5, 3)), np.zeros((1, 5, 3)))


def test_rejects_mismatched_returns_and_flow() -> None:
    with pytest.raises(ValueError, match="agree in shape"):
        accumulate_dates(np.zeros((3, 5, 3)), np.zeros((3, 5, 4)))


def test_rejects_negative_weights() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        weighted_coefficients(_statistics(_small()), -np.ones(12))


def test_rejects_a_non_generator() -> None:
    with pytest.raises(ValueError, match="numpy.random.Generator"):
        cross_block_pvalue(_statistics(_small()), (0, 1), (4, 5), 1, 12345, draws=5)  # type: ignore[arg-type]


def test_rejects_an_impossible_persistence() -> None:
    with pytest.raises(ValueError, match="persistence"):
        SimulationDesign(persistence=1.0)


def test_rejects_an_unknown_scheme() -> None:
    with pytest.raises(ValueError, match="expected 'date' or 'independent-bin'"):
        rejection_rate(_small(), (0, 1), (4, 5), 1, scheme="wild")
