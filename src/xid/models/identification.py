"""Pure-algebra identification results for the simultaneous impact system.

This module implements the A028 derivation in
``docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md``: the probability limits
of Theorem 1, the confounding gap and its Theorem 2 rank bound, and the
permutation-invariant one-spike specialization used for the closed-form
identified interval.

It contains deterministic linear algebra only. It constructs no random-number
generator, reads no configuration, writes no artifact, and touches no
registered stream.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = (
    "confounding_gap",
    "gap_rank_bound",
    "identification_scale",
    "numerical_rank",
    "one_spike_covariance",
    "one_spike_eigenvalues",
    "one_spike_gap_per_entry",
    "plim_ols",
    "plim_proxy",
    "sharp_offdiag_interval",
)

Matrix = NDArray[np.float64]


def _check(name: str, arr: Matrix, shape: tuple[int, ...]) -> Matrix:
    """Fail closed on anything but a finite float64 array of the exact shape."""
    if not isinstance(arr, np.ndarray):
        raise ValueError(f"{name}: expected numpy.ndarray, got {type(arr).__name__}")
    if type(arr) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray, not a subclass")
    if arr.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {arr.dtype}")
    if arr.shape != shape:
        raise ValueError(f"{name}: expected shape {shape}, got {arr.shape}")
    if not np.isfinite(arr).all():
        raise ValueError(f"{name}: expected finite entries")
    return arr


def _validate(
    lam: Matrix,
    b: Matrix,
    gam: Matrix,
    df: Matrix,
    sf: Matrix,
    su: Matrix,
    sv: Matrix,
) -> tuple[int, int]:
    if not isinstance(gam, np.ndarray) or gam.ndim != 2:
        raise ValueError("gam: expected a two-dimensional numpy.ndarray")
    n, k = gam.shape
    _check("lam", lam, (n, n))
    _check("b", b, (n, n))
    _check("gam", gam, (n, k))
    _check("df", df, (n, k))
    _check("sf", sf, (k, k))
    _check("su", su, (n, n))
    _check("sv", sv, (n, n))
    return n, k


def _reduced_form(
    lam: Matrix,
    b: Matrix,
    gam: Matrix,
    df: Matrix,
) -> tuple[Matrix, Matrix, Matrix]:
    """Return the reduced-form flow maps ``(P, U, V)`` of the G1 derivation."""
    n = lam.shape[0]
    h = np.linalg.inv(np.eye(n) - b @ lam)
    p: Matrix = h @ (b @ gam + df)
    u: Matrix = h @ b
    return p, u, h


def confounding_gap(
    lam: Matrix,
    b: Matrix,
    gam: Matrix,
    df: Matrix,
    sf: Matrix,
    su: Matrix,
    sv: Matrix,
) -> Matrix:
    """Return ``plim OLS - Lambda``, the confounding-plus-simultaneity gap.

    This is Eq. (3) of the A028 derivation. Its rank is bounded by
    :func:`gap_rank_bound`.
    """
    _validate(lam, b, gam, df, sf, su, sv)
    p, u, v = _reduced_form(lam, b, gam, df)
    sqq = p @ sf @ p.T + u @ su @ u.T + v @ sv @ v.T
    inv = np.linalg.inv(sqq)
    gap: Matrix = gam @ sf @ p.T @ inv + su @ u.T @ inv
    return gap


def plim_ols(
    lam: Matrix,
    b: Matrix,
    gam: Matrix,
    df: Matrix,
    sf: Matrix,
    su: Matrix,
    sv: Matrix,
) -> Matrix:
    """Population coefficient of the regression of returns on flows."""
    _validate(lam, b, gam, df, sf, su, sv)
    total: Matrix = lam + confounding_gap(lam, b, gam, df, sf, su, sv)
    return total


def plim_proxy(
    lam: Matrix,
    b: Matrix,
    gam: Matrix,
    df: Matrix,
    sf: Matrix,
    su: Matrix,
    sv: Matrix,
    se: Matrix,
) -> Matrix:
    """Population coefficient on flow after controlling for a noisy proxy."""
    _, k = _validate(lam, b, gam, df, sf, su, sv)
    _check("se", se, (k, k))
    rf = sf - sf @ np.linalg.inv(sf + se) @ sf
    p, u, v = _reduced_form(lam, b, gam, df)
    qh = p @ rf @ p.T + u @ su @ u.T + v @ sv @ v.T
    inv = np.linalg.inv(qh)
    total: Matrix = lam + gam @ rf @ p.T @ inv + su @ u.T @ inv
    return total


def gap_rank_bound(k: int, b: Matrix) -> int:
    """Return the Theorem 2 bound ``K + rank(B)`` on the confounding gap rank."""
    if not isinstance(k, int) or isinstance(k, bool):
        raise ValueError("k: expected an int factor count")
    if k < 0:
        raise ValueError("k: expected a nonnegative factor count")
    if not isinstance(b, np.ndarray) or b.ndim != 2 or b.shape[0] != b.shape[1]:
        raise ValueError("b: expected a square two-dimensional numpy.ndarray")
    _check("b", b, b.shape)
    return k + int(np.linalg.matrix_rank(b))


def numerical_rank(m: Matrix, rtol: float = 1e-10) -> int:
    """Count singular values above ``rtol`` times the largest singular value."""
    if not isinstance(m, np.ndarray) or m.ndim != 2:
        raise ValueError("m: expected a two-dimensional numpy.ndarray")
    if m.dtype != np.float64:
        raise ValueError("m: expected float64")
    if not np.isfinite(m).all():
        raise ValueError("m: expected finite entries")
    if rtol <= 0.0:
        raise ValueError("rtol: expected a positive relative tolerance")
    sv = np.linalg.svd(m, compute_uv=False)
    if sv.size == 0 or sv[0] == 0.0:
        return 0
    return int((sv > sv[0] * rtol).sum())


def one_spike_eigenvalues(n: int, share: float) -> tuple[float, float]:
    """Return the ``(leading, residual)`` eigenvalues of a one-spike correlation.

    ``share`` is the fraction of total variance explained by the leading
    principal component, so the leading eigenvalue is ``n * share`` and the
    remaining ``n - 1`` eigenvalues are equal by the maximum-entropy convention.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n: expected an int asset count")
    if n < 2:
        raise ValueError("n: expected at least two assets")
    if not 0.0 < share < 1.0:
        raise ValueError("share: expected a value strictly inside (0, 1)")
    leading = n * share
    residual = (n - leading) / (n - 1)
    if residual <= 0.0:
        raise ValueError("share: expected a residual spectrum that stays positive")
    return leading, residual


def one_spike_covariance(n: int, share: float) -> Matrix:
    """Permutation-invariant one-spike correlation matrix with unit trace mean."""
    leading, residual = one_spike_eigenvalues(n, share)
    m = np.full(n, 1.0 / np.sqrt(n))
    sigma: Matrix = residual * np.eye(n) + (leading - residual) * np.outer(m, m)
    return sigma


def one_spike_gap_per_entry(gamma: float, h_q: float, n: int, q1: float) -> float:
    """Common entry of the rank-one confounding gap, Eq. (11) of the derivation."""
    if n < 2:
        raise ValueError("n: expected at least two assets")
    if q1 <= 0.0:
        raise ValueError("q1: expected a positive leading eigenvalue")
    return float(gamma * h_q / (n * q1))


def identification_scale(
    n: int,
    s_q: float,
    s_r: float,
    a_diag: float,
    a_off: float,
) -> float:
    """Return ``T`` of Eq. (14): the sharp bound on the rescaled gap ``t``.

    Raises ``ValueError`` when ``r_1 < q_1 a_1^2``, meaning no structural tuple
    in the one-spike class reproduces the supplied second moments.
    """
    q1, q0 = one_spike_eigenvalues(n, s_q)
    r1, _ = one_spike_eigenvalues(n, s_r)
    a1 = a_diag + (n - 1) * a_off
    numerator = r1 - q1 * a1**2
    if numerator < 0.0:
        raise ValueError("identification_scale: infeasible moments, r_1 is below q_1 a_1^2")
    return float(np.sqrt(numerator * (q1 - q0) / (q1 * q0)))


def sharp_offdiag_interval(
    n: int,
    s_q: float,
    s_r: float,
    a_diag: float,
    a_off: float,
) -> tuple[float, float]:
    """Closed-form identified interval for the structural off-diagonal, Eq. (15)."""
    scale = identification_scale(n, s_q, s_r, a_diag, a_off)
    half_width = scale / n
    return (a_off - half_width, a_off + half_width)
