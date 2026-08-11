from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.identification import (
    confounding_gap,
    gap_rank_bound,
    identification_scale,
    numerical_rank,
    one_spike_covariance,
    one_spike_gap_per_entry,
    plim_ols,
    plim_proxy,
    sharp_offdiag_interval,
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


# --- A028 Section 3: permutation-invariant one-spike geometry -----------------

D_DIAG = 0.29
S_Q = 0.2827
S_R = 0.32
GAMMA = 0.7


def _observed_one_spike(o: float) -> tuple[float, float]:
    """Return the observed (A_diag, A_off) implied by a structural (d, o, gamma)."""
    q1 = N * S_Q
    q0 = (N - q1) / (N - 1)
    h_q = float(np.sqrt(q1 - q0))
    gap = one_spike_gap_per_entry(GAMMA, h_q, N, q1)
    return D_DIAG + gap, o + gap


def test_one_spike_reproduces_published_pairwise_correlation() -> None:
    """Capponi-Cont report 0.26; the one-spike law gives 0.2579655."""
    sigma = one_spike_covariance(N, S_Q)
    assert abs(float(sigma[0, 1]) - 0.2579655) < 1e-6
    assert abs(float(np.trace(sigma)) - N) < 1e-10


def test_one_spike_gap_is_constant_across_every_entry() -> None:
    """A028 prediction 6: the rank-one gap adds one constant to all N^2 entries."""
    q1 = N * S_Q
    q0 = (N - q1) / (N - 1)
    h_q = float(np.sqrt(q1 - q0))
    m = np.full(N, 1.0 / np.sqrt(N))
    sigma_qq = one_spike_covariance(N, S_Q)
    gap = (GAMMA * m)[:, None] @ (h_q * m)[None, :] @ np.linalg.inv(sigma_qq)
    expected = one_spike_gap_per_entry(GAMMA, h_q, N, q1)
    assert float(np.abs(gap - expected).max()) < 1e-12


@pytest.mark.parametrize(
    ("o", "expected_a_off", "expected_scale", "expected_lo", "expected_hi"),
    [
        (0.0029, 0.0105537, 2.8291865, -0.083753, 0.104860),
        (0.0046, 0.0122537, 2.7125872, -0.078166, 0.102673),
    ],
)
def test_sharp_interval_matches_registered_prediction(
    o: float,
    expected_a_off: float,
    expected_scale: float,
    expected_lo: float,
    expected_hi: float,
) -> None:
    """A028 prediction 4: the closed-form interval at the registered calibration."""
    a_diag, a_off = _observed_one_spike(o)
    assert abs(a_off - expected_a_off) < 1e-6
    assert abs(identification_scale(N, S_Q, S_R, a_diag, a_off) - expected_scale) < 1e-6
    lo, hi = sharp_offdiag_interval(N, S_Q, S_R, a_diag, a_off)
    assert abs(lo - expected_lo) < 1e-5
    assert abs(hi - expected_hi) < 1e-5


@pytest.mark.parametrize("o", [0.0029, 0.0046])
def test_identified_set_contains_zero_and_the_truth(o: float) -> None:
    """Corollary 4.1: the structural off-diagonal is not even sign-identified."""
    a_diag, a_off = _observed_one_spike(o)
    lo, hi = sharp_offdiag_interval(N, S_Q, S_R, a_diag, a_off)
    assert lo < 0.0 < hi
    assert lo < o < hi


def test_identified_halfwidth_dwarfs_the_observed_coefficient() -> None:
    a_diag, a_off = _observed_one_spike(0.0046)
    lo, hi = sharp_offdiag_interval(N, S_Q, S_R, a_diag, a_off)
    half_width = (hi - lo) / 2.0
    assert abs(half_width - 0.0904196) < 1e-6
    assert half_width / a_off > 7.0


def test_sharp_interval_matches_a_bisection_over_the_psd_boundary() -> None:
    """A028 prediction 4: closed form agrees with the exact PSD frontier."""
    a_diag, a_off = _observed_one_spike(0.0046)
    q1 = N * S_Q
    q0 = (N - q1) / (N - 1)
    r1 = N * S_R
    r0 = (N - r1) / (N - 1)
    h_q = float(np.sqrt(q1 - q0))
    m = np.full(N, 1.0 / np.sqrt(N))
    sigma_qq = one_spike_covariance(N, S_Q)
    sigma_rr = r0 * np.eye(N) + (r1 - r0) * np.outer(m, m)

    def min_eigenvalue(t: float) -> float:
        gap = t / N
        dd, oo = a_diag - gap, a_off - gap
        lam1 = dd + (N - 1) * oo
        gamma = t * q1 / h_q
        lam = (dd - oo) * np.eye(N) + N * oo * np.outer(m, m)
        sigma_u = (
            sigma_rr
            - lam @ sigma_qq @ lam.T
            - (2.0 * gamma * h_q * lam1 + gamma**2) * np.outer(m, m)
        )
        return float(np.linalg.eigvalsh(sigma_u).min())

    closed_form = identification_scale(N, S_Q, S_R, a_diag, a_off)
    lo, hi = closed_form * 0.9, closed_form * 1.1
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if min_eigenvalue(mid) >= 0.0:
            lo = mid
        else:
            hi = mid
    assert abs(closed_form - lo) / closed_form < 1e-10


def test_infeasible_calibration_is_rejected() -> None:
    """r_1 < q_1 a_1^2 means no structural tuple reproduces the moments."""
    with pytest.raises(ValueError, match="infeasible"):
        identification_scale(N, S_Q, S_R, 5.0, 5.0)


def test_one_spike_covariance_rejects_degenerate_share() -> None:
    with pytest.raises(ValueError, match="share"):
        one_spike_covariance(N, 0.0)
    with pytest.raises(ValueError, match="share"):
        one_spike_covariance(N, 1.0)
