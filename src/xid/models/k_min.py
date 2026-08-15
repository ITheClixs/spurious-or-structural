"""The minimum confounding dimension and its certified lower bound.

``K_min(A)`` is the smallest latent dimension that could rationalise an
observed cross-impact coefficient matrix using diagonal structural impact
alone. Pure confounding is falsified when ``K_min`` exceeds the factor budget
the order flow supports, so falsification needs a **lower** bound.

Disjoint cross-blocks certify one: a submatrix drawn from disjoint row and
column sets contains no diagonal entry, so its rank bounds ``K_min`` from
below. That direction needs only a singular value decomposition. The opposite
bound would require the completion documented in
``docs/derivations/CROSS_BLOCK_RANK.md`` as start-dependent, and is not
provided here.

**The exact-rank bound saturates under arbitrarily small noise** and is a
population object, not an estimator. See ``docs/derivations/K_MIN.md`` Section
2. ``spectral_gap_ratio`` exposes the shape that survives noise, but calibrating
a cut to a sampling distribution is a separate problem this module does not
solve.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from xid.models.cross_block import cross_block, cross_block_rank

__all__ = (
    "KMinBound",
    "balanced_disjoint_splits",
    "k_min_lower_bound",
    "spectral_gap_ratio",
)

Matrix = NDArray[np.float64]
Split = tuple[tuple[int, ...], tuple[int, ...]]


@dataclass(frozen=True, slots=True)
class KMinBound:
    """Certified lower bound on the minimum confounding dimension."""

    lower_bound: int
    binding_split: Split
    splits_examined: int
    max_gap_ratio: float
    saturated: bool


def balanced_disjoint_splits(n: int, count: int, seed: int) -> tuple[Split, ...]:
    """Random balanced partitions of ``0..n-1`` into two disjoint halves."""
    if n < 4:
        raise ValueError("n: need at least four assets to form two halves")
    if count < 1:
        raise ValueError("count: expected at least one split")
    rng = np.random.default_rng(seed)
    splits: list[Split] = []
    for _ in range(count):
        order = rng.permutation(n)
        half = n // 2
        splits.append(
            (
                tuple(sorted(int(i) for i in order[:half])),
                tuple(sorted(int(i) for i in order[half:])),
            ),
        )
    return tuple(splits)


def spectral_gap_ratio(a: Matrix, rows: tuple[int, ...], columns: tuple[int, ...], k: int) -> float:
    """Return ``sigma_{k+1} / sigma_k`` for a disjoint block.

    Scale-free, and unlike an exact rank it tracks the noise level rather than
    saturating. Zero under the maintained null when ``k`` is the true rank.
    """
    if k < 1:
        raise ValueError("k: expected a positive factor count")
    singular = np.linalg.svd(cross_block(a, rows, columns), compute_uv=False)
    if singular.size <= k:
        return 0.0
    denominator = float(singular[k - 1])
    if denominator == 0.0:
        return 0.0
    return float(singular[k] / denominator)


def k_min_lower_bound(
    a: Matrix,
    splits: tuple[Split, ...],
    rtol: float = 1e-10,
) -> KMinBound:
    """Certified lower bound on ``K_min`` over a family of disjoint splits.

    The bound is exact in population. On noisy input it saturates at the block
    dimension, which ``KMinBound.saturated`` reports; a saturated bound carries
    no information and must not be read as evidence of high latent dimension.
    """
    if not splits:
        raise ValueError("splits: expected at least one disjoint split")
    best = 0
    binding = splits[0]
    worst_gap = 0.0
    smallest_block = min(min(len(i), len(j)) for i, j in splits)
    for rows, columns in splits:
        result = cross_block_rank(a, rows, columns, 0, rtol)
        if result.numerical_rank > best:
            best = result.numerical_rank
            binding = (rows, columns)
        if best >= 1:
            worst_gap = max(worst_gap, spectral_gap_ratio(a, rows, columns, best))
    return KMinBound(
        lower_bound=best,
        binding_split=binding,
        splits_examined=len(splits),
        max_gap_ratio=worst_gap,
        saturated=bool(best >= smallest_block),
    )
