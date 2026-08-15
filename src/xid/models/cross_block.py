"""Exact cross-block rank restrictions on a cross-impact coefficient matrix.

If the structural impact matrix is diagonal, same-bin feedback is absent, and
at most ``K`` latent factors confound the regression, then the coefficient
matrix is diagonal plus rank ``K``. Choosing row and column index sets that are
**disjoint** removes every diagonal entry from the resulting submatrix, so the
submatrix equals the low-rank part exactly and inherits its rank bound.

That makes the restriction exact and testable with one singular value
decomposition, with no nuisance diagonal to estimate and no nonconvex
minimisation. See ``docs/derivations/CROSS_BLOCK_RANK.md``; the alternating
projection that the distance statistic relies on is documented there as
start-dependent, which is the defect this module exists to avoid.

Deterministic linear algebra only. No random-number generator, no registered
stream, no market data.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
from numpy.typing import NDArray

__all__ = (
    "CrossBlockResult",
    "cross_block",
    "cross_block_rank",
    "tetrad_residuals",
    "violation_ratio",
)

Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class CrossBlockResult:
    """Singular spectrum of one disjoint cross-block."""

    rows: tuple[int, ...]
    columns: tuple[int, ...]
    singular_values: Matrix
    numerical_rank: int
    violation_ratio: float


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


def _check_indices(rows: tuple[int, ...], columns: tuple[int, ...], n: int) -> None:
    for name, idx in (("rows", rows), ("columns", columns)):
        if not idx:
            raise ValueError(f"{name}: expected at least one index")
        if len(set(idx)) != len(idx):
            raise ValueError(f"{name}: expected distinct indices")
        if any(i < 0 or i >= n for i in idx):
            raise ValueError(f"{name}: index outside 0..{n - 1}")
    overlap = set(rows) & set(columns)
    if overlap:
        raise ValueError(
            "rows and columns must be disjoint; the diagonal enters the block "
            f"otherwise, and indices {sorted(overlap)} appear in both"
        )


def cross_block(a: Matrix, rows: tuple[int, ...], columns: tuple[int, ...]) -> Matrix:
    """Return the submatrix ``a[rows, columns]`` for disjoint index sets."""
    n = _validate(a)
    _check_indices(rows, columns, n)
    block: Matrix = np.ascontiguousarray(a[np.ix_(list(rows), list(columns))])
    return block


def violation_ratio(singular_values: Matrix, k: int) -> float:
    """Return ``sigma_{k+1} / sigma_1``, the scale-free restriction violation.

    Zero under the maintained null. Returns zero when the block is smaller than
    ``k + 1``, since the restriction is then vacuous rather than satisfied.
    """
    if k < 0:
        raise ValueError("k: expected a nonnegative factor count")
    if singular_values.size <= k:
        return 0.0
    leading = float(singular_values[0])
    if leading == 0.0:
        return 0.0
    return float(singular_values[k] / leading)


def cross_block_rank(
    a: Matrix,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    k: int,
    rtol: float = 1e-10,
) -> CrossBlockResult:
    """Singular spectrum and rank of one disjoint cross-block.

    Under the maintained null the numerical rank is at most ``k`` and the
    violation ratio is zero.
    """
    block = cross_block(a, rows, columns)
    singular = np.linalg.svd(block, compute_uv=False)
    leading = float(singular[0]) if singular.size else 0.0
    rank = int((singular > leading * rtol).sum()) if leading > 0.0 else 0
    return CrossBlockResult(
        rows=rows,
        columns=columns,
        singular_values=np.ascontiguousarray(singular),
        numerical_rank=rank,
        violation_ratio=violation_ratio(singular, k),
    )


def tetrad_residuals(
    a: Matrix,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
) -> Matrix:
    """All two-by-two minors of a disjoint cross-block.

    These are the ``K = 1`` restrictions of Corollary 9.1: each entry is
    ``a[i,j] a[k,l] - a[i,l] a[k,j]`` for distinct ``i, k`` in ``rows`` and
    distinct ``j, l`` in ``columns``. They vanish exactly when a single latent
    factor generates the whole block.
    """
    block = cross_block(a, rows, columns)
    if block.shape[0] < 2 or block.shape[1] < 2:
        raise ValueError("tetrads need at least two rows and two columns")
    values = [
        float(block[i, j] * block[p, q] - block[i, q] * block[p, j])
        for i, p in combinations(range(block.shape[0]), 2)
        for j, q in combinations(range(block.shape[1]), 2)
    ]
    return np.ascontiguousarray(values, dtype=np.float64)
