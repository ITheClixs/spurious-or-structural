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

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

__all__ = (
    "PsiTestResult",
    "decompose",
    "null_projection",
    "psi_k",
    "psi_test",
    "select_factor_count",
)

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


@dataclass(frozen=True)
class PsiTestResult:
    """Outcome of the A030 low-rank departure test."""

    statistic: float
    critical_value: float
    reject: bool
    factor_count: int
    replicates: int
    alpha: float
    method: str


def null_projection(a: Matrix, k: int) -> Matrix:
    """Project ``a`` onto the diagonal-plus-rank-``k`` set."""
    diagonal_part, low_rank = decompose(a, k)
    projected: Matrix = diagonal_part + low_rank
    return projected


def select_factor_count(a: Matrix, k_max: int = 10) -> int:
    """Ahn-Horenstein eigenvalue-ratio rule on the off-diagonal part.

    Registered before use by A030 so that the factor count cannot be chosen
    after observing a rejection.
    """
    n = _validate(a, 0, 1, 0.0)
    if k_max < 1 or k_max >= n:
        raise ValueError(f"k_max: expected 1 <= k_max < {n}, got {k_max}")
    singular = np.linalg.svd(a - np.diag(np.diag(a)), compute_uv=False)
    floor = max(float(singular[0]) * 1e-14, 1e-300)
    ratios = [float(singular[i]) / max(float(singular[i + 1]), floor) for i in range(k_max)]
    return int(np.argmax(ratios)) + 1


def _sampling_draw(
    rng: np.random.Generator,
    chol: Matrix,
    sample_size: int,
    scale: float,
) -> Matrix:
    n = chol.shape[0]
    draw: Matrix = (scale / np.sqrt(sample_size)) * (rng.normal(size=(n, n)) @ chol.T)
    return draw


def psi_test(
    a: Matrix,
    k: int,
    regressor_covariance: Matrix,
    sample_size: int,
    rng: np.random.Generator,
    replicates: int = 199,
    alpha: float = 0.05,
    error_scale: float = 1.0,
) -> PsiTestResult:
    """Parametric plug-in bootstrap test of the diagonal-plus-rank-``k`` null.

    Rejection is evidence **against** pure confounding and therefore for genuine
    structural cross-impact. The test is not valid at small samples; see
    ``docs/derivations/PSI_NULL_DISTRIBUTION.md`` for the size study and the
    stated minimum sample size.
    """
    n = _validate(a, k, DEFAULT_ITERATIONS, DEFAULT_TOLERANCE)
    if regressor_covariance.shape != (n, n):
        raise ValueError("regressor_covariance: expected shape matching a")
    if sample_size < 1:
        raise ValueError("sample_size: expected a positive sample size")
    if replicates < 1:
        raise ValueError("replicates: expected at least one replicate")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha: expected a level strictly inside (0, 1)")
    if error_scale <= 0.0:
        raise ValueError("error_scale: expected a positive scale")

    chol = np.linalg.cholesky(np.linalg.inv(regressor_covariance))
    projected = null_projection(a, k)
    draws = np.array(
        [
            psi_k(projected + _sampling_draw(rng, chol, sample_size, error_scale), k)
            for _ in range(replicates)
        ]
    )
    critical = float(np.quantile(draws, 1.0 - alpha))
    statistic = psi_k(a, k)
    return PsiTestResult(
        statistic=statistic,
        critical_value=critical,
        reject=bool(statistic > critical),
        factor_count=k,
        replicates=replicates,
        alpha=alpha,
        method=(
            "parametric plug-in bootstrap on the diagonal-plus-rank-K null, "
            "ordinary-least-squares sampling law, upper empirical quantile"
        ),
    )
