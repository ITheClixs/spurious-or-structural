"""Sharpness of the rank bound on the confounding gap.

Theorem 2 bounds the gap by ``rank(G) <= K + rank(B)``. A bound that is never
tight would make the low-rank contamination story vacuous, so this module
supplies the factorisation that turns the inequality into an equality:

```
G = L R,   L = [Gamma | Sigma_uu B_R'],   R = [C_1 ; B_L' M' Sigma_qq^{-1}],
```

with inner dimension ``K + rank(B)``. When ``K + rank(B) <= N`` and the
regularity conditions of Theorem 10 hold, both factors have full rank and
Sylvester's rank inequality forces equality. Above that the generic value is
``N``, established by genericity with numerical witnesses rather than proof.

See ``docs/derivations/GENERIC_GAP_RANK.md``. Deterministic linear algebra
only. No random-number generator, no registered stream, no market data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from xid.models.identification import numerical_rank

__all__ = (
    "GapFactorisation",
    "gap_factorisation",
    "generic_gap_rank",
)

Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class GapFactorisation:
    """The gap written as a product through ``K + rank(B)`` inner columns."""

    left: Matrix
    """``[Gamma | Sigma_uu B_R']``, of shape ``(N, K + rank(B))``."""

    right: Matrix
    """``[C_1 ; B_L' M' Sigma_qq^{-1}]``, of shape ``(K + rank(B), N)``."""

    feedback_rank: int
    """``rank(B)``, the number of feedback directions the gap can carry."""

    @property
    def inner_dimension(self) -> int:
        """``K + rank(B)``, the ceiling Theorem 2 places on the gap's rank."""
        return int(self.left.shape[1])

    @property
    def gap(self) -> Matrix:
        """The confounding gap ``G = L R`` itself."""
        product: Matrix = np.ascontiguousarray(self.left @ self.right)
        return product


def _check(name: str, value: object, rows: int, columns: int) -> Matrix:
    if not isinstance(value, np.ndarray) or type(value) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray")
    if value.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {value.dtype}")
    if value.shape != (rows, columns):
        raise ValueError(f"{name}: expected shape {(rows, columns)}, got {value.shape}")
    if not np.isfinite(value).all():
        raise ValueError(f"{name}: expected finite entries")
    return value


def _positive_definite(name: str, value: Matrix) -> None:
    symmetric = (value + value.T) / 2.0
    smallest = float(np.linalg.eigvalsh(symmetric).min())
    if smallest <= max(1.0, float(np.abs(symmetric).max())) * 1e-12:
        raise ValueError(
            f"{name}: expected a positive definite matrix; the smallest eigenvalue "
            f"is {smallest:.3e}"
        )


def generic_gap_rank(k: int, b: Matrix) -> int:
    """Return ``min(N, K + rank(B))``, the generic rank of the confounding gap.

    Equal to the Theorem 2 bound whenever that bound does not exceed the
    cross-section size. When it does, the gap is generically of full rank and
    carries no low-rank restriction at all.
    """
    if not isinstance(k, int) or isinstance(k, bool):
        raise ValueError("k: expected an int factor count")
    if k < 0:
        raise ValueError("k: expected a nonnegative factor count")
    if not isinstance(b, np.ndarray) or b.ndim != 2 or b.shape[0] != b.shape[1]:
        raise ValueError("b: expected a square two-dimensional numpy.ndarray")
    n = int(b.shape[0])
    _check("b", b, n, n)
    return min(n, k + numerical_rank(b))


def gap_factorisation(
    lam: Matrix,
    b: Matrix,
    gam: Matrix,
    df: Matrix,
    sf: Matrix,
    su: Matrix,
    sv: Matrix,
    rtol: float = 1e-9,
) -> GapFactorisation:
    """Factor the confounding gap through ``K + rank(B)`` inner columns.

    The product ``left @ right`` reproduces
    :func:`xid.models.identification.confounding_gap`. Its shape is what makes
    the Theorem 2 bound visible, and Theorem 10 shows both factors attain full
    rank away from an exceptional set of measure zero.
    """
    n = int(lam.shape[0]) if isinstance(lam, np.ndarray) and lam.ndim == 2 else 0
    if n == 0:
        raise ValueError("lam: expected a square two-dimensional numpy.ndarray")
    k = int(gam.shape[1]) if isinstance(gam, np.ndarray) and gam.ndim == 2 else 0
    if k == 0:
        raise ValueError("gam: expected a two-dimensional numpy.ndarray with columns")
    _check("lam", lam, n, n)
    _check("b", b, n, n)
    _check("gam", gam, n, k)
    _check("df", df, n, k)
    _check("sf", sf, k, k)
    _check("su", su, n, n)
    _check("sv", sv, n, n)
    for name, matrix in (("su", su), ("sv", sv)):
        _positive_definite(name, matrix)

    identity = np.eye(n)
    feedback = identity - b @ lam
    if numerical_rank(np.ascontiguousarray(feedback)) < n:
        raise ValueError(
            "b, lam: expected I - B Lambda to be invertible; the system has no "
            "reduced form at these primitives"
        )
    m = np.linalg.inv(feedback)
    p = m @ (b @ gam + df)
    sqq = p @ sf @ p.T + m @ b @ su @ b.T @ m.T + m @ sv @ m.T
    _positive_definite("implied flow covariance", np.ascontiguousarray(sqq))
    sqq_inv = np.linalg.inv((sqq + sqq.T) / 2.0)

    left_singular, singular, right_singular = np.linalg.svd(b)
    rank_b = int((singular > singular[0] * rtol).sum()) if singular[0] > 0.0 else 0
    b_left = left_singular[:, :rank_b] * singular[:rank_b]
    b_right = right_singular[:rank_b]

    left = np.concatenate([gam, su @ b_right.T], axis=1)
    right = np.concatenate([sf @ p.T @ sqq_inv, b_left.T @ m.T @ sqq_inv], axis=0)
    return GapFactorisation(
        left=np.ascontiguousarray(left),
        right=np.ascontiguousarray(right),
        feedback_rank=rank_b,
    )
