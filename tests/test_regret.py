from __future__ import annotations

from itertools import pairwise

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.regret import (
    execution_regret,
    optimal_trade,
    regret_leading_constant,
)

Matrix = NDArray[np.float64]

N = 20
SEED = 1729
EPS_GRID = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625)
LEADING_CONSTANT = 0.003388738


def _geometry(seed: int = SEED, n: int = N) -> tuple[Matrix, Matrix, Matrix]:
    """Return ``(Lambda_s, G_s, c)`` with the gap of unit Frobenius norm."""
    rng = np.random.default_rng(seed)
    noise = rng.normal(size=(n, n))
    truth = np.ascontiguousarray(noise @ noise.T / n + np.eye(n) * 0.8)
    gap = rng.normal(size=(n, n))
    gap = (gap + gap.T) / 2.0
    return truth, np.ascontiguousarray(gap / np.linalg.norm(gap)), rng.normal(size=n)


def _regrets(truth: Matrix, gap: Matrix, constraint: Matrix) -> list[float]:
    return [
        execution_regret(truth, np.ascontiguousarray(truth + eps * gap), constraint).regret
        for eps in EPS_GRID
    ]


# --- A037 prediction 1: the exact identity ------------------------------------


def test_prediction_1_regret_equals_the_true_cost_of_the_trade_error() -> None:
    truth, gap, constraint = _geometry()
    for eps in EPS_GRID:
        result = execution_regret(truth, np.ascontiguousarray(truth + eps * gap), constraint)
        quadratic = float(result.trade_error @ truth @ result.trade_error)
        assert abs(result.regret - quadratic) < 1e-15


def test_prediction_1_the_trade_error_stays_on_the_constraint() -> None:
    truth, gap, constraint = _geometry()
    result = execution_regret(truth, np.ascontiguousarray(truth + 0.2 * gap), constraint)
    assert abs(float(constraint @ result.trade_error)) < 1e-12


# --- A037 prediction 2: regret is never negative ------------------------------


def test_prediction_2_regret_is_non_negative_on_the_grid() -> None:
    truth, gap, constraint = _geometry()
    assert all(r >= 0.0 for r in _regrets(truth, gap, constraint))


def test_prediction_2_regret_is_non_negative_for_random_gaps() -> None:
    truth, _, constraint = _geometry()
    rng = np.random.default_rng(808)
    for _ in range(200):
        draw = rng.normal(size=(N, N))
        draw = (draw + draw.T) / 2.0
        believed = np.ascontiguousarray(truth + 0.05 * draw / np.linalg.norm(draw))
        assert execution_regret(truth, believed, constraint).regret >= 0.0


# --- A037 prediction 3: the leading constant ----------------------------------


def test_prediction_3_ratio_rises_to_the_predicted_constant() -> None:
    truth, gap, constraint = _geometry()
    predicted = regret_leading_constant(truth, gap, constraint)
    assert abs(predicted - LEADING_CONSTANT) < 1e-8
    ratios = [r / eps**2 for r, eps in zip(_regrets(truth, gap, constraint), EPS_GRID, strict=True)]
    assert all(x < y for x, y in pairwise(ratios)), ratios
    assert abs(ratios[-1] - predicted) / predicted < 0.02


# --- A037 prediction 4: halving the gap quarters the loss ---------------------


def test_prediction_4_successive_halvings_approach_a_factor_of_four() -> None:
    truth, gap, constraint = _geometry()
    regrets = _regrets(truth, gap, constraint)
    ratios = [a / b for a, b in pairwise(regrets)]
    assert all(3.8 < r < 4.0 for r in ratios), ratios
    assert all(x < y for x, y in pairwise(ratios)), ratios


# --- A037 prediction 5: gaps the trader does not feel -------------------------


@pytest.mark.parametrize("alpha", (-0.5, 0.6, 2.0))
def test_prediction_5_a_rescaling_of_the_true_matrix_costs_nothing(alpha: float) -> None:
    """The argmin is scale invariant, so this gap never moves the trade."""
    truth, _, constraint = _geometry()
    believed = np.ascontiguousarray(truth * (1.0 + alpha))
    assert execution_regret(truth, believed, constraint).regret < 1e-14
    assert regret_leading_constant(truth, np.ascontiguousarray(alpha * truth), constraint) < 1e-14


def test_prediction_5_a_generic_gap_does_cost_something() -> None:
    """Compared inside the admissible region; see the correction in the derivation."""
    truth, gap, constraint = _geometry()
    believed = np.ascontiguousarray(truth + 0.05 * gap)
    assert execution_regret(truth, believed, constraint).regret > 1e-8


def test_a_generic_gap_scaled_like_the_rescalings_has_no_admissible_trade() -> None:
    """Why the original prediction 5 was ill-posed: the believed matrix goes indefinite."""
    truth, gap, constraint = _geometry()
    believed = np.ascontiguousarray(truth + 0.6 * float(np.linalg.norm(truth)) * gap)
    assert float(np.linalg.eigvalsh(believed).min()) < 0.0
    with pytest.raises(ValueError, match="positive definite"):
        execution_regret(truth, believed, constraint)


# --- supporting behaviour ------------------------------------------------------


def test_optimal_trade_satisfies_the_constraint_and_beats_its_neighbours() -> None:
    truth, _, constraint = _geometry()
    trade = optimal_trade(truth, constraint)
    assert abs(float(constraint @ trade) - 1.0) < 1e-12
    best = float(trade @ truth @ trade)
    rng = np.random.default_rng(11)
    for _ in range(50):
        step = rng.normal(size=N)
        step -= constraint * float(constraint @ step) / float(constraint @ constraint)
        other = trade + 0.01 * step
        assert float(other @ truth @ other) >= best


def test_only_the_symmetric_part_of_the_cost_matrix_matters() -> None:
    truth, _, constraint = _geometry()
    skew = np.random.default_rng(3).normal(size=(N, N))
    skew = np.ascontiguousarray(skew - skew.T)
    assert (
        np.abs(optimal_trade(truth, constraint) - optimal_trade(truth + skew, constraint)).max()
        < 1e-12
    )


def test_relative_regret_reports_the_fraction_of_the_optimal_cost() -> None:
    truth, gap, constraint = _geometry()
    result = execution_regret(truth, np.ascontiguousarray(truth + 0.2 * gap), constraint)
    assert abs(result.relative_regret - result.regret / result.optimal_cost) < 1e-15
    assert 0.0 < result.relative_regret < 0.01


# --- fail-closed ---------------------------------------------------------------


def test_rejects_an_indefinite_cost_matrix() -> None:
    _, _, constraint = _geometry()
    with pytest.raises(ValueError, match="positive definite"):
        optimal_trade(np.zeros((N, N)), constraint)


def test_rejects_a_zero_constraint() -> None:
    truth, _, _ = _geometry()
    with pytest.raises(ValueError, match="nonzero"):
        optimal_trade(truth, np.zeros(N))


def test_rejects_a_constraint_of_the_wrong_length() -> None:
    truth, _, _ = _geometry()
    with pytest.raises(ValueError, match="to match the constraint"):
        optimal_trade(truth, np.ones(N + 1))


def test_rejects_non_float64() -> None:
    truth, _, constraint = _geometry()
    with pytest.raises(ValueError, match="float64"):
        optimal_trade(truth.astype(np.float32), constraint)


def test_rejects_a_gap_of_the_wrong_shape() -> None:
    truth, _, constraint = _geometry()
    with pytest.raises(ValueError, match="expected a numpy.ndarray of shape"):
        regret_leading_constant(truth, np.eye(N - 1), constraint)
