from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.identification import (
    confounding_gap,
    gap_rank_bound,
    numerical_rank,
    plim_ols,
    plim_proxy,
)

N = 30
K = 3

Fixture = tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
]


def _fixture(rank_b: int) -> Fixture:
    """Build the A028 frozen fixture in its registered draw order."""
    rng = np.random.default_rng(1729)

    def psd(n: int) -> NDArray[np.float64]:
        a = rng.normal(size=(n, n))
        return np.asarray(a @ a.T / n + np.eye(n) * 0.5, dtype=np.float64)

    lam = rng.normal(scale=0.1, size=(N, N))
    gam = rng.normal(size=(N, K))
    df = rng.normal(size=(N, K))
    if rank_b == 0:
        b = np.zeros((N, N))
    elif rank_b >= N:
        b = rng.normal(scale=0.02, size=(N, N))
    else:
        b = rng.normal(size=(N, rank_b)) @ rng.normal(size=(rank_b, N)) * 0.05
    return lam, b, gam, df, psd(K), psd(N), psd(N)


@pytest.mark.parametrize(
    ("rank_b", "expected_rank"),
    [(0, 3), (1, 4), (2, 5), (30, 30)],
)
def test_gap_rank_matches_registered_prediction(rank_b: int, expected_rank: int) -> None:
    """A028 prediction 1: the Theorem 2 bound holds and binds where it can."""
    lam, b, gam, df, sf, su, sv = _fixture(rank_b)
    gap = confounding_gap(lam, b, gam, df, sf, su, sv)
    assert numerical_rank(gap) == expected_rank
    assert numerical_rank(gap) <= gap_rank_bound(K, b)


def test_diagonal_truth_yields_exactly_rank_k_dense_gap() -> None:
    """A028 prediction 2: zero true cross-impact still gives a dense gap."""
    rng = np.random.default_rng(1729)
    _, _, gam, df, sf, su, sv = _fixture(0)
    diagonal_truth = np.diag(rng.uniform(0.2, 0.4, N))
    gap = confounding_gap(diagonal_truth, np.zeros((N, N)), gam, df, sf, su, sv)
    assert numerical_rank(gap) == K
    off_diagonal = gap - np.diag(np.diag(gap))
    assert np.abs(off_diagonal).max() > 0.2


def test_plim_ols_equals_truth_plus_gap() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(1)
    expected = lam + confounding_gap(lam, b, gam, df, sf, su, sv)
    assert np.allclose(plim_ols(lam, b, gam, df, sf, su, sv), expected, atol=0.0)


def test_perfect_proxy_removes_factor_confounding_when_feedback_is_absent() -> None:
    """Corollary check: zero proxy noise and no feedback recovers the truth."""
    lam, _, gam, df, sf, su, sv = _fixture(0)
    zero_b = np.zeros((N, N))
    zero_noise = np.zeros((K, K))
    recovered = plim_proxy(lam, zero_b, gam, df, sf, su, sv, zero_noise)
    assert np.abs(recovered - lam).max() < 1e-10


def test_useless_proxy_converges_to_uncontrolled_coefficient() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(1)
    huge_noise = np.eye(K) * 1e12
    controlled = plim_proxy(lam, b, gam, df, sf, su, sv, huge_noise)
    uncontrolled = plim_ols(lam, b, gam, df, sf, su, sv)
    assert np.abs(controlled - uncontrolled).max() < 1e-6


def test_gap_rank_bound_counts_feedback_rank() -> None:
    assert gap_rank_bound(3, np.zeros((N, N))) == 3
    rank_two = np.zeros((N, N))
    rank_two[0, 0] = 1.0
    rank_two[1, 1] = 1.0
    assert gap_rank_bound(3, rank_two) == 5


def test_numerical_rank_of_zero_matrix_is_zero() -> None:
    assert numerical_rank(np.zeros((N, N))) == 0


def test_plim_ols_rejects_non_float64() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(0)
    with pytest.raises(ValueError, match="float64"):
        plim_ols(lam.astype(np.float32), b, gam, df, sf, su, sv)


def test_plim_ols_rejects_nonfinite() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(0)
    corrupted = lam.copy()
    corrupted[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        plim_ols(corrupted, b, gam, df, sf, su, sv)


def test_plim_ols_rejects_shape_mismatch() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(0)
    with pytest.raises(ValueError, match="shape"):
        plim_ols(lam[:-1, :-1], b, gam, df, sf, su, sv)


def test_plim_proxy_rejects_wrong_proxy_noise_dimension() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(0)
    with pytest.raises(ValueError, match="shape"):
        plim_proxy(lam, b, gam, df, sf, su, sv, np.eye(K + 1))
