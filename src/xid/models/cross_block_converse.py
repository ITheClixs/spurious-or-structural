"""How far the cross-block rank restriction characterises the model.

Theorem 9 is a one-way implication: a diagonal-plus-rank-``K`` matrix has every
disjoint cross-block of rank at most ``K``. Whether the converse holds decides
what a *non*-rejection is worth. This module supplies the three pieces that are
settled — the boundary below which the restriction constrains anything at all,
a constructive converse at one factor, and the tangent-space computation that
establishes the general case locally.

The global converse for ``K >= 2`` is open and is not claimed anywhere here.

See ``docs/derivations/CROSS_BLOCK_CONVERSE.md``. Deterministic linear algebra
only. No random-number generator, no registered stream, no market data.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
from numpy.typing import NDArray

__all__ = (
    "RankOneCompletion",
    "cross_block_minors",
    "minor_tangent_dimension",
    "rank_one_completion",
    "restriction_has_content",
)

Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class RankOneCompletion:
    """A rank-one completion recovered from off-diagonal entries alone."""

    left: Matrix
    right: Matrix
    diagonal: Matrix
    """``D_ii = x_i y_i``, the entries the off-diagonal data implies."""

    offdiagonal_error: float
    """``max |A_ij - x_i y_j|`` over ``i != j``."""


def restriction_has_content(n: int, k: int) -> bool:
    """Whether disjoint cross-block rank bounds constrain anything at ``(n, k)``.

    True exactly when ``k (2n - k) < n^2 - n``, equivalently ``k < n - sqrt(n)``:
    off-diagonals of rank-``k`` matrices must occupy strictly less than the full
    off-diagonal space for the restriction to exclude any pattern.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n: expected a positive int cross-section size")
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError("k: expected a nonnegative int factor count")
    return k * (2 * n - k) < n * n - n


def _validate(a: Matrix) -> int:
    if not isinstance(a, np.ndarray) or type(a) is not np.ndarray:
        raise ValueError("a: expected exactly numpy.ndarray")
    if a.dtype != np.float64:
        raise ValueError(f"a: expected float64, got {a.dtype}")
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError(f"a: expected a square matrix, got shape {a.shape}")
    if not np.isfinite(a).all():
        raise ValueError("a: expected finite entries")
    return int(a.shape[0])


def cross_block_minors(a: Matrix, k: int) -> Matrix:
    """Every minimal disjoint cross-block ``(k+1)``-minor of ``a``.

    These generate the restriction: they vanish identically on
    diagonal-plus-rank-``k`` matrices, and they are the equations whose
    Jacobian :func:`minor_tangent_dimension` differentiates.
    """
    n = _validate(a)
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError("k: expected a nonnegative int factor count")
    size = k + 1
    values = [
        float(np.linalg.det(a[np.ix_(rows, columns)]))
        for rows in combinations(range(n), size)
        for columns in combinations(range(n), size)
        if not set(rows) & set(columns)
    ]
    return np.ascontiguousarray(values, dtype=np.float64)


def minor_tangent_dimension(a: Matrix, k: int, step: float = 1e-6, rtol: float = 1e-6) -> int:
    """Dimension of the tangent space to the cross-block variety at ``a``.

    Differentiates :func:`cross_block_minors` with respect to the off-diagonal
    entries and returns ``(n^2 - n) - rank(J)``. At a generic
    diagonal-plus-rank-``k`` matrix this equals ``k (2n - k)``, the dimension of
    the off-diagonals of rank-``k`` matrices, which is what makes the converse
    hold locally.

    The rank is numerical, read from a finite-difference Jacobian; it is not an
    exact algebraic rank.
    """
    n = _validate(a)
    if step <= 0.0:
        raise ValueError("step: expected a positive finite-difference step")
    if rtol <= 0.0:
        raise ValueError("rtol: expected a positive relative tolerance")
    offdiagonal = [(i, j) for i in range(n) for j in range(n) if i != j]
    base = cross_block_minors(a, k)
    if base.size == 0:
        raise ValueError(
            f"no disjoint cross-block of size {k + 1} exists at n = {n}; the "
            "restriction is empty and has no tangent space"
        )
    jacobian = np.empty((base.size, len(offdiagonal)), dtype=np.float64)
    for column, (i, j) in enumerate(offdiagonal):
        shifted = a.copy()
        shifted[i, j] += step
        jacobian[:, column] = (cross_block_minors(shifted, k) - base) / step
    singular = np.linalg.svd(jacobian, compute_uv=False)
    rank = int((singular > singular[0] * rtol).sum()) if singular[0] > 0.0 else 0
    return len(offdiagonal) - rank


def rank_one_completion(a: Matrix) -> RankOneCompletion:
    """Recover the rank-one completion implied by off-diagonal entries.

    Implements the construction of Theorem 11: ``x_i = A_{i1}``,
    ``y_j = A_{0j}/A_{01}``, with ``x_1`` and ``y_0`` recovered through a third
    index. Requires ``n >= 4`` and nonzero anchors ``A_{01}``, ``A_{12}``,
    ``A_{20}``; the diagonal of ``a`` is never read.
    """
    n = _validate(a)
    if n < 4:
        raise ValueError(
            f"a: expected at least four assets, got {n}; below four no two disjoint "
            "index pairs exist and the tetrad family is empty"
        )
    anchors = {"a[0,1]": a[0, 1], "a[1,2]": a[1, 2], "a[2,0]": a[2, 0]}
    scale = float(np.abs(a).max())
    for name, value in anchors.items():
        if abs(float(value)) <= scale * 1e-12:
            raise ValueError(
                f"{name}: expected a nonzero anchor entry; the Theorem 11 "
                "construction does not cover sparse off-diagonal support"
            )
    left = np.array([a[i, 1] for i in range(n)], dtype=np.float64)
    right = np.array([a[0, j] / a[0, 1] for j in range(n)], dtype=np.float64)
    left[1] = a[1, 2] / right[2]
    right[0] = a[2, 0] / left[2]
    error = max(
        abs(float(a[i, j] - left[i] * right[j])) for i in range(n) for j in range(n) if i != j
    )
    return RankOneCompletion(
        left=np.ascontiguousarray(left),
        right=np.ascontiguousarray(right),
        diagonal=np.ascontiguousarray(left * right),
        offdiagonal_error=error,
    )
