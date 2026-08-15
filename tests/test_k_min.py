from __future__ import annotations

from itertools import pairwise

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.k_min import (
    balanced_disjoint_splits,
    k_min_lower_bound,
    spectral_gap_ratio,
)

N = 30
SPLITS = balanced_disjoint_splits(N, 6, seed=3)
NOISE_GRID = (0.0, 1e-6, 1e-4, 1e-2, 0.1)


def _matrix(k: int, seed: int = 1729) -> NDArray[np.float64]:
    rng = np.random.default_rng(seed)
    return np.ascontiguousarray(
        np.diag(rng.uniform(0.2, 0.4, N)) + rng.normal(size=(N, k)) @ rng.normal(size=(k, N)) * 0.05
    )


def _perturbation(seed: int = 9191) -> NDArray[np.float64]:
    rng = np.random.default_rng(seed)
    pert = rng.normal(size=(N, N))
    pert -= np.diag(np.diag(pert))
    return np.ascontiguousarray(pert / np.linalg.norm(pert))


@pytest.mark.parametrize("k", [1, 2, 3, 5, 8, 12, 15])
def test_prediction_1_bound_is_exact_in_population(k: int) -> None:
    """A033 prediction 1."""
    assert k_min_lower_bound(_matrix(k), SPLITS).lower_bound == k


def test_prediction_2_bound_never_exceeds_the_block_dimension() -> None:
    """It is a lower bound, so it cannot exceed what a block can express."""
    bound = k_min_lower_bound(_matrix(3), SPLITS)
    assert bound.lower_bound <= min(min(len(i), len(j)) for i, j in SPLITS)


def test_prediction_3_exact_rank_saturates_under_tiny_noise() -> None:
    """A033 prediction 3: the honest limitation, asserted rather than hidden."""
    noisy = np.ascontiguousarray(_matrix(3) + 1e-6 * _perturbation())
    bound = k_min_lower_bound(noisy, SPLITS)
    assert bound.lower_bound == 15
    assert bound.saturated is True


def test_prediction_4_gap_ratio_grows_with_noise() -> None:
    """A033 prediction 4: the shape survives where the rank does not."""
    base, pert = _matrix(3), _perturbation()
    rows, columns = tuple(range(15)), tuple(range(15, 30))
    ratios = [
        spectral_gap_ratio(np.ascontiguousarray(base + eps * pert), rows, columns, 3)
        for eps in NOISE_GRID
    ]
    assert ratios[0] < 1e-12
    assert all(x < y for x, y in pairwise(ratios)), ratios


def test_prediction_5_overlapping_splits_are_refused() -> None:
    with pytest.raises(ValueError, match="disjoint"):
        k_min_lower_bound(_matrix(3), (((0, 1, 2), (2, 3, 4)),))


def test_unsaturated_bound_is_flagged_as_informative() -> None:
    assert k_min_lower_bound(_matrix(3), SPLITS).saturated is False


def test_rejects_empty_split_family() -> None:
    with pytest.raises(ValueError, match="at least one disjoint split"):
        k_min_lower_bound(_matrix(3), ())


def test_gap_ratio_rejects_nonpositive_k() -> None:
    with pytest.raises(ValueError, match="k"):
        spectral_gap_ratio(_matrix(3), tuple(range(15)), tuple(range(15, 30)), 0)


def test_splits_are_disjoint_and_cover_the_universe() -> None:
    for rows, columns in SPLITS:
        assert not set(rows) & set(columns)
        assert len(set(rows) | set(columns)) == N


def test_splits_reject_a_tiny_universe() -> None:
    with pytest.raises(ValueError, match="four assets"):
        balanced_disjoint_splits(3, 2, seed=1)
