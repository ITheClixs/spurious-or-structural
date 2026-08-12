from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.execution import (
    confounding_null_space,
    cost_error,
    cost_interval,
    factor_exposure,
    impact_cost,
    minimax_cost_schedule,
    worst_case_cost,
)
from xid.models.identification import confounding_gap, identification_scale

N = 30
K = 3

# Registered source-matched one-spike calibration.
S_Q = 0.2827
S_R = 0.32
D_DIAG = 0.29
O_OFF = 0.0046
GAMMA = 0.7


def _general_fixture() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """A028 draw order, diagonal structural truth, zero feedback."""
    rng = np.random.default_rng(1729)

    def psd(n: int) -> NDArray[np.float64]:
        a = rng.normal(size=(n, n))
        return np.asarray(a @ a.T / n + np.eye(n) * 0.5, dtype=np.float64)

    _ = rng.normal(scale=0.1, size=(N, N))
    gam = rng.normal(size=(N, K))
    df = rng.normal(size=(N, K))
    sf, su, sv = psd(K), psd(N), psd(N)

    truth_rng = np.random.default_rng(1729)
    truth = np.diag(truth_rng.uniform(0.2, 0.4, N))
    gap = confounding_gap(truth, np.zeros((N, N)), gam, df, sf, su, sv)
    return truth, gap


def _trades(gap: NDArray[np.float64]) -> dict[str, NDArray[np.float64]]:
    """Frozen trades, drawn seed 9191 in the order random then neutral."""
    rng = np.random.default_rng(9191)
    index = np.full(N, 1.0 / np.sqrt(N))
    random = rng.normal(size=N)
    random /= np.linalg.norm(random)
    basis = confounding_null_space(gap)
    neutral = basis @ (basis.T @ rng.normal(size=N))
    neutral /= np.linalg.norm(neutral)
    return {"index": index, "random": random, "neutral": neutral}


def _one_spike() -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """Return (truth, gap, g) in the registered permutation-invariant geometry."""
    m = np.full(N, 1.0 / np.sqrt(N))
    q1 = N * S_Q
    q0 = (N - q1) / (N - 1)
    h_q = float(np.sqrt(q1 - q0))
    g = GAMMA * h_q / (N * q1)
    truth = (D_DIAG - O_OFF) * np.eye(N) + N * O_OFF * np.outer(m, m)
    gap = g * np.ones((N, N))
    return truth, gap, g


# --- Theorem 6: the immune subspace -------------------------------------------


def test_null_space_has_the_predicted_dimension() -> None:
    """A029 prediction 1: at most K of N trade directions are mispriced."""
    _, gap = _general_fixture()
    basis = confounding_null_space(gap)
    assert basis.shape == (N, N - K)


def test_confound_neutral_trade_has_exactly_zero_cost_error() -> None:
    """A029 prediction 1: the immune subspace is immune to machine precision."""
    truth, gap = _general_fixture()
    neutral = _trades(gap)["neutral"]
    # Structural errors in this fixture are of order 1e-2, so 1e-13 still
    # separates an exact zero from a real effect by eleven orders.
    assert abs(cost_error(neutral, gap)) < 1e-13
    assert abs(cost_error(neutral, gap) / impact_cost(neutral, truth)) < 1e-12


@pytest.mark.parametrize(
    ("trade", "expected_relative"),
    [("index", -9.8113), ("random", -9.7661), ("neutral", 0.0000)],
)
def test_general_fixture_cost_errors(trade: str, expected_relative: float) -> None:
    """A029 prediction 2, general fixture."""
    truth, gap = _general_fixture()
    x = _trades(gap)[trade]
    relative = 100.0 * cost_error(x, gap) / impact_cost(x, truth)
    assert abs(relative - expected_relative) < 1e-3


# --- Corollary 6.2: the exposure law ------------------------------------------


@pytest.mark.parametrize(
    ("trade", "expected_relative"),
    [("index", 54.2302), ("random", 5.4183), ("neutral_pair", 0.0000)],
)
def test_one_spike_cost_errors(trade: str, expected_relative: float) -> None:
    """A029 prediction 2, one-spike geometry where m is the confounding direction."""
    truth, gap, _ = _one_spike()
    rng = np.random.default_rng(9191)
    random = rng.normal(size=N)
    random /= np.linalg.norm(random)
    neutral_pair = np.zeros(N)
    neutral_pair[0], neutral_pair[1] = 1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)
    x = {
        "index": np.full(N, 1.0 / np.sqrt(N)),
        "random": random,
        "neutral_pair": neutral_pair,
    }[trade]
    relative = 100.0 * cost_error(x, gap) / impact_cost(x, truth)
    assert abs(relative - expected_relative) < 1e-3


def test_exposure_law_ratio_is_constant() -> None:
    """A029 prediction 3: the error is exactly proportional to squared exposure."""
    _, gap, g = _one_spike()
    m = np.full(N, 1.0 / np.sqrt(N))
    rng = np.random.default_rng(9191)
    ratios = []
    for _ in range(8):
        x = rng.normal(size=N)
        ratios.append(cost_error(x, gap) / float(m @ x) ** 2)
    # Relative, not absolute: the ratio is a reduction over 900 float64 terms
    # and its last digits depend on BLAS blocking. 1e-9 relative is three times
    # the largest observed cross-platform spread and six orders below any
    # structural effect.
    scale = abs(N * g)
    assert (max(ratios) - min(ratios)) / scale < 1e-9
    assert abs(ratios[0] - N * g) / scale < 1e-9
    assert abs(N * g - 0.2296108639) < 1e-9


def test_dollar_neutral_trade_is_immune_in_the_one_spike_geometry() -> None:
    _, gap, _ = _one_spike()
    neutral = np.zeros(N)
    neutral[0], neutral[1] = 1.0, -1.0
    assert cost_error(neutral, gap) == 0.0
    assert abs(factor_exposure(neutral)) < 1e-15


# --- Proposition 7: the identified cost interval ------------------------------


def test_cost_interval_halfwidth_matches_the_closed_form() -> None:
    """A029 prediction 4."""
    _, gap, g = _one_spike()
    a_diag, a_off = D_DIAG + g, O_OFF + g
    scale = identification_scale(N, S_Q, S_R, a_diag, a_off) / N
    assert abs(scale - 0.0904195732) < 1e-9
    x = np.full(N, 1.0 / np.sqrt(N))
    lower, upper = cost_interval(x, N, S_Q, S_R, a_diag, a_off)
    assert abs((upper - lower) / 2.0 - scale * factor_exposure(x) ** 2) < 1e-12
    assert lower < upper


def test_dollar_neutral_cost_is_point_identified() -> None:
    """The striking consequence: unidentified matrix, identified cost."""
    _, _, g = _one_spike()
    neutral = np.zeros(N)
    neutral[0], neutral[1] = 1.0, -1.0
    lower, upper = cost_interval(neutral, N, S_Q, S_R, D_DIAG + g, O_OFF + g)
    assert upper - lower == 0.0


# --- Proposition 8: the minimax-cost schedule ---------------------------------


def _scheduling_setup() -> tuple[NDArray[np.float64], float]:
    _, gap, g = _one_spike()
    a_diag, a_off = D_DIAG + g, O_OFF + g
    a = (a_diag - a_off) * np.eye(N) + a_off * np.ones((N, N))
    penalty = identification_scale(N, S_Q, S_R, a_diag, a_off) / N
    return np.asarray((a + a.T) / 2.0, dtype=np.float64), penalty


def _targets() -> dict[str, NDArray[np.float64]]:
    rng = np.random.default_rng(1729)
    neutral = np.zeros(N)
    neutral[0], neutral[1] = 1.0, -1.0
    return {
        "index": np.ones(N),
        "neutral": neutral,
        "general": rng.normal(size=N),
    }


@pytest.mark.parametrize(
    ("target", "expected_improvement"),
    [("index", 0.0), ("neutral", 0.0), ("general", 3.1095)],
)
def test_minimax_schedule_improvement(target: str, expected_improvement: float) -> None:
    """A029 prediction 5, including the two registered degenerate cases."""
    a_sym, penalty = _scheduling_setup()
    c = _targets()[target]
    naive = minimax_cost_schedule(a_sym, c, 1.0, 0.0)
    robust = minimax_cost_schedule(a_sym, c, 1.0, penalty)
    naive_wc = worst_case_cost(naive, a_sym, penalty)
    robust_wc = worst_case_cost(robust, a_sym, penalty)
    improvement = 100.0 * (naive_wc - robust_wc) / naive_wc
    assert abs(improvement - expected_improvement) < 1e-3


def test_robust_schedule_weakly_reduces_factor_exposure() -> None:
    a_sym, penalty = _scheduling_setup()
    for c in _targets().values():
        naive = minimax_cost_schedule(a_sym, c, 1.0, 0.0)
        robust = minimax_cost_schedule(a_sym, c, 1.0, penalty)
        assert abs(factor_exposure(robust)) <= abs(factor_exposure(naive)) + 1e-12


def test_schedule_satisfies_the_target_constraint_exactly() -> None:
    a_sym, penalty = _scheduling_setup()
    for c in _targets().values():
        x = minimax_cost_schedule(a_sym, c, 2.5, penalty)
        assert abs(float(c @ x) - 2.5) < 1e-10


def test_closed_form_matches_a_grid_search() -> None:
    """A029 prediction 5: the closed form is the optimum, not an approximation."""
    a_sym, penalty = _scheduling_setup()
    c = _targets()["general"]
    robust = minimax_cost_schedule(a_sym, c, 1.0, penalty)
    best = worst_case_cost(robust, a_sym, penalty)
    rng = np.random.default_rng(314159)
    for _ in range(20000):
        z = rng.normal(size=N)
        z = z + (1.0 - float(c @ z)) / float(c @ c) * c
        best = min(best, worst_case_cost(z, a_sym, penalty))
    assert worst_case_cost(robust, a_sym, penalty) - best < 1e-10


# --- fail-closed validation ---------------------------------------------------


def test_impact_cost_rejects_non_float64() -> None:
    with pytest.raises(ValueError, match="float64"):
        impact_cost(np.ones(N, dtype=np.float32), np.eye(N))


def test_cost_error_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="shape"):
        cost_error(np.ones(N - 1), np.eye(N))


def test_minimax_schedule_rejects_infeasible_target() -> None:
    a_sym, penalty = _scheduling_setup()
    with pytest.raises(ValueError, match="degenerate"):
        minimax_cost_schedule(a_sym, np.zeros(N), 1.0, penalty)


def test_minimax_schedule_rejects_an_indefinite_cost_matrix() -> None:
    """Proposition 8 assumes a_sym is PSD; an indefinite input is a saddle."""
    _, penalty = _scheduling_setup()
    indefinite = np.diag(np.linspace(-1.0, 1.0, N))
    with pytest.raises(ValueError, match="positive semidefinite"):
        minimax_cost_schedule(indefinite, np.ones(N), 1.0, penalty)


def test_minimax_schedule_accepts_the_registered_calibration() -> None:
    """The registered A_s is PSD, so the new gate must not fire on it."""
    a_sym, penalty = _scheduling_setup()
    assert float(np.linalg.eigvalsh(a_sym).min()) > 0.0
    schedule = minimax_cost_schedule(a_sym, np.ones(N), 1.0, penalty)
    assert np.isfinite(schedule).all()


def test_minimax_schedule_rejects_negative_penalty() -> None:
    a_sym, _ = _scheduling_setup()
    with pytest.raises(ValueError, match="penalty"):
        minimax_cost_schedule(a_sym, np.ones(N), 1.0, -1.0)
