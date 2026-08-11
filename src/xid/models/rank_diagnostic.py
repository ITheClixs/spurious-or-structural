"""Diagonal-plus-rank-K specification diagnostic.

Corollary 2.1 of ``docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md`` states
that under a diagonal structural impact matrix with no same-bin feedback and
``K`` latent factors, the population return-on-flow coefficient matrix lies
exactly in the diagonal-plus-rank-``K`` set. The statistic here measures the
relative Frobenius distance from that set, so a materially nonzero value is
evidence against pure confounding and therefore for genuine structural
cross-impact.

The module is deterministic linear algebra. It constructs no random-number
generator, reads no configuration, and touches no registered stream.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = ("decompose", "psi_k")

Matrix = NDArray[np.float64]

DEFAULT_ITERATIONS = 500
DEFAULT_TOLERANCE = 1e-14


def _validate(a: Matrix, k: int, iters: int, tol: float) -> int:
    if not isinstance(a, np.ndarray):
        raise ValueError(f"a: expected numpy.ndarray, got {type(a).__name__}")
    if type(a) is not np.ndarray:
        raise ValueError("a: expected exactly numpy.ndarray, not a subclass")
    if a.dtype != np.float64:
        raise ValueError(f"a: expected float64, got {a.dtype}")
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError(f"a: expected a square matrix, got shape {a.shape}")
    if not np.isfinite(a).all():
        raise ValueError("a: expected finite entries")
    if not isinstance(k, int) or isinstance(k, bool):
        raise ValueError("k: expected an int factor count")
    if k < 0 or k > a.shape[0]:
        raise ValueError(f"k: expected 0 <= k <= {a.shape[0]}, got {k}")
    if iters < 1:
        raise ValueError("iters: expected at least one iteration")
    if tol < 0.0:
        raise ValueError("tol: expected a nonnegative tolerance")
    return int(a.shape[0])


def decompose(
    a: Matrix,
    k: int,
    iters: int = DEFAULT_ITERATIONS,
    tol: float = DEFAULT_TOLERANCE,
) -> tuple[Matrix, Matrix]:
    """Split ``a`` into a diagonal part and a rank-``k`` part.

    Alternating projection: with the low-rank block fixed the exact Frobenius
    minimiser over diagonals is ``diag(a - r)``, and with the diagonal fixed the
    exact minimiser over rank-``k`` matrices is the truncated singular value
    decomposition. Each half-step is optimal over its own block, so the
    objective is nonincreasing and bounded below and therefore converges. The
    limit is a stationary point, not a certified global minimum, so the
    residual is an upper bound on the true distance.
    """
    _validate(a, k, iters, tol)
    low_rank: Matrix = np.zeros_like(a)
    diagonal_part: Matrix = np.diag(np.diag(a))
    previous = np.inf
    for _ in range(iters):
        diagonal_part = np.diag(np.diag(a - low_rank))
        residual = a - diagonal_part
        u, s, vt = np.linalg.svd(residual)
        truncated = s.copy()
        truncated[k:] = 0.0
        low_rank = (u * truncated) @ vt
        current = float(np.linalg.norm(a - diagonal_part - low_rank))
        if previous - current <= tol:
            break
        previous = current
    return np.diag(np.diag(a - low_rank)), low_rank


def psi_k(
    a: Matrix,
    k: int,
    iters: int = DEFAULT_ITERATIONS,
    tol: float = DEFAULT_TOLERANCE,
) -> float:
    """Relative Frobenius distance of ``a`` from the diagonal-plus-rank-``k`` set.

    Returns zero when ``a`` carries no off-diagonal energy at all, since the
    normalisation is then undefined and the matrix is trivially in the set.
    """
    _validate(a, k, iters, tol)
    scale = float(np.linalg.norm(a - np.diag(np.diag(a))))
    if scale == 0.0:
        return 0.0
    diagonal_part, low_rank = decompose(a, k, iters, tol)
    return float(np.linalg.norm(a - diagonal_part - low_rank) / scale)
