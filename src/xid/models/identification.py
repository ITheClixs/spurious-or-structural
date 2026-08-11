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
    "numerical_rank",
    "plim_ols",
    "plim_proxy",
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
