from __future__ import annotations

from itertools import pairwise

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.cross_block import (
    cross_block,
    cross_block_rank,
    tetrad_residuals,
    violation_ratio,
)

N = 30
K = 3
ROWS = tuple(range(0, 10))
COLUMNS = tuple(range(15, 25))
PERTURBATION_GRID = (0.0, 0.01, 0.05, 0.20)


def _diagonal_plus_low_rank(
    seed: int = 1729, k: int = K, n: int = N
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return ``(A, R)`` with ``A = D + R`` and ``rank(R) = k``."""
    rng = np.random.default_rng(seed)
    diagonal = np.diag(rng.uniform(0.2, 0.4, n))
    low_rank = rng.normal(size=(n, k)) @ rng.normal(size=(k, n)) * 0.05
    return (
        np.ascontiguousarray(diagonal + low_rank, dtype=np.float64),
        np.ascontiguousarray(low_rank, dtype=np.float64),
    )


def _dense_offdiagonal_perturbation(seed: int = 9191) -> NDArray[np.float64]:
    rng = np.random.default_rng(seed)
    pert = rng.normal(size=(N, N))
    pert -= np.diag(np.diag(pert))
    return np.ascontiguousarray(pert / np.linalg.norm(pert), dtype=np.float64)


# --- A032 prediction 1: the diagonal never enters a disjoint block ------------


def test_prediction_1_block_equals_the_low_rank_part_exactly() -> None:
    a, low_rank = _diagonal_plus_low_rank()
    block = cross_block(a, ROWS, COLUMNS)
    reference = low_rank[np.ix_(list(ROWS), list(COLUMNS))]
    assert np.abs(block - reference).max() == 0.0


def test_prediction_1_numerical_rank_is_the_factor_count() -> None:
    a, _ = _diagonal_plus_low_rank()
    result = cross_block_rank(a, ROWS, COLUMNS, K)
    assert result.numerical_rank == K


# --- A032 prediction 2: the violation responds to structure ------------------


def test_prediction_2_violation_is_zero_under_the_null() -> None:
    a, _ = _diagonal_plus_low_rank()
    assert cross_block_rank(a, ROWS, COLUMNS, K).violation_ratio < 1e-12


def test_prediction_2_violation_increases_with_perturbation() -> None:
    a, _ = _diagonal_plus_low_rank()
    pert = _dense_offdiagonal_perturbation()
    ratios = [
        cross_block_rank(np.ascontiguousarray(a + eps * pert), ROWS, COLUMNS, K).violation_ratio
        for eps in PERTURBATION_GRID
    ]
    assert all(x < y for x, y in pairwise(ratios)), ratios


# --- A032 prediction 3: tetrads discriminate the factor count ----------------


def test_prediction_3_tetrads_vanish_at_one_factor() -> None:
    a, _ = _diagonal_plus_low_rank(seed=99, k=1)
    residuals = tetrad_residuals(a, tuple(range(0, 8)), tuple(range(15, 23)))
    assert residuals.size == 784
    scale = float(np.abs(cross_block(a, tuple(range(0, 8)), tuple(range(15, 23)))).max())
    assert float(np.abs(residuals).max()) / scale**2 < 1e-12


def test_prediction_3_same_tetrads_do_not_vanish_at_three_factors() -> None:
    a, _ = _diagonal_plus_low_rank()
    residuals = tetrad_residuals(a, tuple(range(0, 8)), tuple(range(15, 23)))
    assert float(np.abs(residuals).max()) > 1e-3


# --- A032 prediction 4: disjointness is load-bearing -------------------------


def test_prediction_4_overlapping_index_sets_are_refused() -> None:
    """The restriction only holds when the diagonal is excluded."""
    a, _ = _diagonal_plus_low_rank()
    with pytest.raises(ValueError, match="disjoint"):
        cross_block(a, (0, 1, 2), (2, 3, 4))


def test_prediction_4_overlapping_block_would_break_the_rank_bound() -> None:
    """Formed directly, an overlapping block exceeds the factor count."""
    a, _ = _diagonal_plus_low_rank()
    overlapping = np.ascontiguousarray(a[np.ix_(list(range(10)), list(range(10)))])
    singular = np.linalg.svd(overlapping, compute_uv=False)
    assert int((singular > singular[0] * 1e-10).sum()) > K


# --- fail-closed --------------------------------------------------------------


def test_rejects_non_float64() -> None:
    a, _ = _diagonal_plus_low_rank()
    with pytest.raises(ValueError, match="float64"):
        cross_block(a.astype(np.float32), ROWS, COLUMNS)


def test_rejects_repeated_indices() -> None:
    a, _ = _diagonal_plus_low_rank()
    with pytest.raises(ValueError, match="distinct"):
        cross_block(a, (0, 0, 1), COLUMNS)


def test_rejects_out_of_range_indices() -> None:
    a, _ = _diagonal_plus_low_rank()
    with pytest.raises(ValueError, match="outside"):
        cross_block(a, (0, 1, N), COLUMNS)


def test_rejects_empty_index_set() -> None:
    a, _ = _diagonal_plus_low_rank()
    with pytest.raises(ValueError, match="at least one index"):
        cross_block(a, (), COLUMNS)


def test_violation_ratio_is_zero_for_a_vacuous_block() -> None:
    """A block with fewer than k+1 singular values cannot violate the bound."""
    assert violation_ratio(np.array([1.0, 0.5]), 5) == 0.0


def test_tetrads_need_a_two_by_two_block() -> None:
    a, _ = _diagonal_plus_low_rank()
    with pytest.raises(ValueError, match="at least two"):
        tetrad_residuals(a, (0,), COLUMNS)
