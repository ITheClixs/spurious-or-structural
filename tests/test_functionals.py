from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.functionals import (
    confounding_directions,
    identified_width,
    is_point_identified,
    width_attaining_loading,
)

N = 20
K = 3
SEED = 1729
DRAWS = 200
RADIUS = 1.0

Matrix = NDArray[np.float64]


def _geometry(seed: int = SEED, n: int = N, k: int = K) -> tuple[Matrix, Matrix, Matrix]:
    """Return ``(W, A, orthonormal basis of col(W))``."""
    rng = np.random.default_rng(seed)
    delta = rng.normal(size=(n, k))
    noise = rng.normal(size=(n, n))
    idiosyncratic = noise @ noise.T / n + np.eye(n) * 0.6
    flow_covariance = np.ascontiguousarray(delta @ delta.T + idiosyncratic)
    w = confounding_directions(flow_covariance, np.ascontiguousarray(delta))
    basis, _ = np.linalg.qr(w)
    a = np.ascontiguousarray(rng.normal(size=(n, n)))
    return w, a, np.ascontiguousarray(basis)


def _identified_set(a: Matrix, w: Matrix, seed: int, draws: int = DRAWS) -> list[Matrix]:
    rng = np.random.default_rng(seed)
    return [a - rng.normal(size=w.shape) @ w.T for _ in range(draws)]


def _spread(values: list[float]) -> float:
    return max(values) - min(values)


def _orthogonalise(vector: Matrix, basis: Matrix) -> Matrix:
    return np.ascontiguousarray(vector - basis @ (basis.T @ vector))


# --- A035 prediction 1: the flow argument decides linear functionals ----------


def test_prediction_1_linear_functional_is_pinned_when_flow_is_orthogonal() -> None:
    w, a, basis = _geometry()
    rng = np.random.default_rng(4242)
    left, right = rng.normal(size=N), _orthogonalise(rng.normal(size=N), basis)
    members = _identified_set(a, w, seed=77)
    assert _spread([float(left @ m @ right) for m in members]) < 1e-12


def test_prediction_1_linear_functional_moves_when_flow_is_free() -> None:
    w, a, basis = _geometry()
    rng = np.random.default_rng(4242)
    left, right = rng.normal(size=N), rng.normal(size=N)
    members = _identified_set(a, w, seed=77)
    assert _spread([float(left @ m @ right) for m in members]) > 1.0


# --- A035 prediction 2: the asymmetry is real ---------------------------------


def test_prediction_2_orthogonalising_the_response_argument_buys_nothing() -> None:
    """Theorem A constrains ``b`` only; a confounding-orthogonal ``a`` does not help."""
    w, a, basis = _geometry()
    rng = np.random.default_rng(4242)
    left, right = _orthogonalise(rng.normal(size=N), basis), rng.normal(size=N)
    members = _identified_set(a, w, seed=77)
    assert _spread([float(left @ m @ right) for m in members]) > 1.0


# --- A035 prediction 3: quadratic costs ---------------------------------------


def test_prediction_3_cost_is_pinned_for_a_confounding_orthogonal_trade() -> None:
    w, a, basis = _geometry()
    trade = _orthogonalise(np.random.default_rng(31337).normal(size=N), basis)
    members = _identified_set(a, w, seed=77)
    assert _spread([float(trade @ m @ trade) for m in members]) < 1e-12
    assert is_point_identified(w, trade)


def test_prediction_3_cost_moves_for_a_free_trade() -> None:
    w, a, _ = _geometry()
    trade = np.ascontiguousarray(np.random.default_rng(31337).normal(size=N))
    members = _identified_set(a, w, seed=77)
    assert _spread([float(trade @ m @ trade) for m in members]) > 1.0
    assert not is_point_identified(w, trade)


# --- A035 prediction 4: the one-spike corollary is this theorem's instance ----


def test_prediction_4_one_spike_confounding_space_is_the_market_direction() -> None:
    n, rho, h = 25, 0.3, 0.8
    market = np.ones((n, 1)) / np.sqrt(n)
    flow_covariance = np.ascontiguousarray((1.0 - rho) * np.eye(n) + rho * n * (market @ market.T))
    w = confounding_directions(flow_covariance, np.ascontiguousarray(h * market))
    cosine = abs(float(w[:, 0] @ market[:, 0]) / np.linalg.norm(w))
    assert abs(cosine - 1.0) < 1e-10
    assert is_point_identified(w, _orthogonalise(np.arange(n, dtype=np.float64) - 12.0, market))


# --- A035 prediction 5: the closed-form width is attained ---------------------


@pytest.mark.parametrize("scale", (0.25, 0.5, 1.0, 2.0))
def test_prediction_5_width_matches_the_value_attained_at_the_maximiser(scale: float) -> None:
    w, _, basis = _geometry()
    rng = np.random.default_rng(1729)
    trade = _orthogonalise(rng.normal(size=N), basis) + scale * (basis @ np.ones(K))
    verdict = identified_width(w, np.ascontiguousarray(trade), RADIUS)
    optimum = width_attaining_loading(w, np.ascontiguousarray(trade), RADIUS)
    attained = 2.0 * float(trade @ optimum @ (w.T @ trade))
    assert abs(np.linalg.norm(optimum) - RADIUS) < 1e-12
    assert abs(verdict.width - attained) <= abs(attained) * 1e-10


def test_prediction_5_width_is_the_product_not_the_exposure_alone() -> None:
    """The trade norm enters; ratios to ``||W'x||`` alone are not constant."""
    w, _, basis = _geometry()
    rng = np.random.default_rng(1729)
    ratios = []
    for scale in (0.25, 0.5, 1.0, 2.0):
        trade = _orthogonalise(rng.normal(size=N), basis) + scale * (basis @ np.ones(K))
        verdict = identified_width(w, np.ascontiguousarray(trade), RADIUS)
        ratios.append(verdict.width / verdict.exposure)
    assert _spread(ratios) > 1.0


def test_width_is_zero_for_a_confounding_orthogonal_trade() -> None:
    w, _, basis = _geometry()
    trade = _orthogonalise(np.random.default_rng(5).normal(size=N), basis)
    verdict = identified_width(w, np.ascontiguousarray(trade), RADIUS)
    assert verdict.point_identified
    assert verdict.width < 1e-12


# --- fail-closed --------------------------------------------------------------


def test_rejects_non_float64() -> None:
    w, _, _ = _geometry()
    with pytest.raises(ValueError, match="float64"):
        is_point_identified(w, np.ones(N, dtype=np.float32))


def test_rejects_length_mismatch() -> None:
    w, _, _ = _geometry()
    with pytest.raises(ValueError, match="expected length"):
        is_point_identified(w, np.ones(N + 1))


def test_rejects_zero_flow_argument() -> None:
    w, _, _ = _geometry()
    with pytest.raises(ValueError, match="nonzero"):
        is_point_identified(w, np.zeros(N))


def test_rejects_singular_flow_covariance() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        confounding_directions(np.zeros((4, 4)), np.ones((4, 1)))


def test_rejects_loading_with_wrong_row_count() -> None:
    with pytest.raises(ValueError, match="to match the flow covariance"):
        confounding_directions(np.eye(4), np.ones((3, 1)))


def test_rejects_negative_radius() -> None:
    w, _, _ = _geometry()
    with pytest.raises(ValueError, match="nonnegative"):
        identified_width(w, np.ones(N), -1.0)


def test_maximiser_is_refused_when_the_cost_is_already_identified() -> None:
    w, _, basis = _geometry()
    trade = _orthogonalise(np.random.default_rng(5).normal(size=N), basis)
    with pytest.raises(ValueError, match="point identified"):
        width_attaining_loading(w, np.ascontiguousarray(trade), RADIUS)
