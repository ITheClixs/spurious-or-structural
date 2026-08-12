"""Execution cost under low-rank confounding.

This module implements the A029 derivation in
``docs/derivations/EXECUTION_COST_UNDER_CONFOUNDING.md``: the quadratic impact
cost, the rank-``K`` cost error and its immune subspace, the identified cost
interval induced by the partial-identification result, and the closed-form
minimax-cost schedule.

It is a static one-period impact model. There is no dynamic schedule, decay
kernel, risk aversion, or timing risk here, and nothing in this module supports
a profitability claim. It contains deterministic linear algebra only, opens no
registered stream, and reads no market data.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from xid.models.identification import identification_scale

__all__ = (
    "confounding_null_space",
    "cost_error",
    "cost_interval",
    "factor_exposure",
    "impact_cost",
    "minimax_cost_schedule",
    "worst_case_cost",
)

Matrix = NDArray[np.float64]
Vector = NDArray[np.float64]


def _check_vector(name: str, x: Vector, n: int | None = None) -> int:
    if not isinstance(x, np.ndarray) or type(x) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray")
    if x.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {x.dtype}")
    if x.ndim != 1:
        raise ValueError(f"{name}: expected a one-dimensional vector")
    if not np.isfinite(x).all():
        raise ValueError(f"{name}: expected finite entries")
    if n is not None and x.shape[0] != n:
        raise ValueError(f"{name}: expected shape ({n},), got {x.shape}")
    return int(x.shape[0])


def _check_matrix(name: str, m: Matrix, n: int | None = None) -> int:
    if not isinstance(m, np.ndarray) or type(m) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray")
    if m.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {m.dtype}")
    if m.ndim != 2 or m.shape[0] != m.shape[1]:
        raise ValueError(f"{name}: expected a square matrix, got shape {m.shape}")
    if not np.isfinite(m).all():
        raise ValueError(f"{name}: expected finite entries")
    if n is not None and m.shape[0] != n:
        raise ValueError(f"{name}: expected shape ({n}, {n}), got {m.shape}")
    return int(m.shape[0])


def impact_cost(x: Vector, m: Matrix) -> float:
    """Expected impact cost ``x' M x`` of executing trade ``x``."""
    n = _check_vector("x", x)
    _check_matrix("m", m, n)
    return float(x @ m @ x)


def cost_error(x: Vector, gap: Matrix) -> float:
    """Cost of trading on the estimate instead of the truth, Eq. (2)."""
    n = _check_vector("x", x)
    _check_matrix("gap", gap, n)
    return float(x @ gap @ x)


def factor_exposure(x: Vector) -> float:
    """Equal-weight factor exposure ``1' x`` of a trade."""
    _check_vector("x", x)
    return float(x.sum())


def confounding_null_space(gap: Matrix, rtol: float = 1e-10) -> Matrix:
    """Orthonormal basis of the trade directions immune to the confounding gap.

    Returns the right singular vectors of ``gap`` whose singular values fall
    below ``rtol`` times the largest. Any trade in this span has exactly zero
    cost error by Theorem 6, whatever the magnitude of the spurious entries.
    """
    n = _check_matrix("gap", gap)
    if rtol <= 0.0:
        raise ValueError("rtol: expected a positive relative tolerance")
    _, singular, vt = np.linalg.svd(gap)
    if singular.size == 0 or singular[0] == 0.0:
        return np.eye(n, dtype=np.float64)
    keep = singular <= singular[0] * rtol
    basis: Matrix = np.ascontiguousarray(vt[keep].T)
    return basis


def cost_interval(
    x: Vector,
    n: int,
    s_q: float,
    s_r: float,
    a_diag: float,
    a_off: float,
) -> tuple[float, float]:
    """Sharp identified interval for execution cost, Proposition 7.

    The half-width is ``(T/N)(1'x)^2``, so a dollar-neutral trade has a
    degenerate interval: its cost is point-identified even though the impact
    matrix is not.
    """
    _check_vector("x", x, n)
    half_width = identification_scale(n, s_q, s_r, a_diag, a_off) / n
    exposure = factor_exposure(x)
    a = (a_diag - a_off) * np.eye(n) + a_off * np.ones((n, n))
    centre = impact_cost(x, np.asarray(a, dtype=np.float64))
    spread = half_width * exposure**2
    return (centre - spread, centre + spread)


def worst_case_cost(x: Vector, a_sym: Matrix, penalty: float) -> float:
    """Upper end of the identified cost interval, Eq. (8)."""
    n = _check_vector("x", x)
    _check_matrix("a_sym", a_sym, n)
    if penalty < 0.0:
        raise ValueError("penalty: expected a nonnegative robustness penalty")
    return float(x @ a_sym @ x) + penalty * factor_exposure(x) ** 2


def minimax_cost_schedule(
    a_sym: Matrix,
    c: Vector,
    q: float,
    penalty: float,
) -> Vector:
    """Minimise worst-case cost subject to ``c' x = q``, Proposition 8.

    ``penalty = 0`` returns the naive schedule. At ``penalty = T/N`` this is the
    minimax-cost schedule, whose factor exposure is weakly smaller. When the
    constraint already pins the factor exposure the two coincide, which is
    Corollary 8.1 rather than a defect.
    """
    n = _check_matrix("a_sym", a_sym)
    _check_vector("c", c, n)
    if not np.isfinite(q):
        raise ValueError("q: expected a finite target level")
    if penalty < 0.0:
        raise ValueError("penalty: expected a nonnegative robustness penalty")
    ones = np.ones(n, dtype=np.float64)
    m = a_sym + penalty * np.outer(ones, ones)
    inverse = np.linalg.inv(m)
    denominator = float(c @ inverse @ c)
    if abs(denominator) < 1e-12:
        raise ValueError("c: degenerate target direction for this cost matrix")
    schedule: Vector = (q / denominator) * (inverse @ c)
    return schedule
