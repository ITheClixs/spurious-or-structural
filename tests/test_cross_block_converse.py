from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.cross_block_converse import (
    cross_block_minors,
    minor_tangent_dimension,
    rank_one_completion,
    restriction_has_content,
)

Matrix = NDArray[np.float64]

TANGENT_CASES = ((5, 1), (6, 1), (7, 1), (8, 1), (6, 2), (7, 2), (8, 2), (8, 3), (9, 3))
CONTENT_CASES = (
    (5, 1, True),
    (5, 3, False),
    (8, 3, True),
    (8, 5, True),
    (10, 7, False),
    (30, 3, True),
    (30, 23, True),
)


def _generic_point(n: int, k: int, seed: int = 7) -> Matrix:
    """A generic ``D + rank-k`` matrix: the model point the converse is tested at."""
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(n, k)) @ rng.normal(size=(n, k)).T
    return np.ascontiguousarray(a + np.diag(rng.normal(size=n)))


# --- A038 prediction 1: the content boundary ----------------------------------


@pytest.mark.parametrize(("n", "k", "expected"), CONTENT_CASES)
def test_prediction_1_content_boundary_matches_the_table(n: int, k: int, expected: bool) -> None:
    assert restriction_has_content(n, k) is expected


@pytest.mark.parametrize("n", (5, 8, 10, 20, 30))
def test_prediction_1_counting_agrees_with_the_square_root_form(n: int) -> None:
    """``k(2n-k) < n^2-n`` and ``k < n - sqrt(n)`` are the same condition."""
    for k in range(1, n + 1):
        assert restriction_has_content(n, k) is bool(k < n - np.sqrt(n))


# --- A038 prediction 2: the constructive converse at one factor ---------------


@pytest.mark.parametrize("n", (4, 5, 6, 8, 12))
def test_prediction_2_rank_one_completion_is_recovered_from_off_diagonals(n: int) -> None:
    rng = np.random.default_rng(11)
    left, right = rng.normal(size=n), rng.normal(size=n)
    a = np.outer(left, right).copy()
    np.fill_diagonal(a, rng.normal(size=n))
    a = np.ascontiguousarray(a)

    completion = rank_one_completion(a)
    assert completion.offdiagonal_error < 1e-14

    completed = a.copy()
    np.fill_diagonal(completed, completion.diagonal)
    singular = np.linalg.svd(completed, compute_uv=False)
    assert int((singular > singular[0] * 1e-9).sum()) == 1


def test_prediction_2_the_original_diagonal_is_never_read() -> None:
    """The construction uses off-diagonal entries only."""
    rng = np.random.default_rng(11)
    a = np.ascontiguousarray(np.outer(rng.normal(size=6), rng.normal(size=6)))
    first = rank_one_completion(a)
    perturbed = a.copy()
    np.fill_diagonal(perturbed, np.arange(6, dtype=np.float64) * 100.0)
    second = rank_one_completion(np.ascontiguousarray(perturbed))
    assert np.abs(first.diagonal - second.diagonal).max() < 1e-12


# --- A038 prediction 3: below four assets there is nothing to say -------------


def test_prediction_3_three_assets_admit_no_disjoint_tetrad() -> None:
    assert cross_block_minors(_generic_point(3, 1), 1).size == 0


def test_prediction_3_completion_refuses_below_four_assets() -> None:
    with pytest.raises(ValueError, match="at least four assets"):
        rank_one_completion(_generic_point(3, 1))


# --- A038 prediction 4: tangent dimensions agree ------------------------------


@pytest.mark.parametrize(("n", "k"), TANGENT_CASES)
def test_prediction_4_tangent_dimension_equals_the_rank_k_off_diagonal_dimension(
    n: int, k: int
) -> None:
    """Corollary 11.1: the converse holds locally at generic model points."""
    a = _generic_point(n, k)
    assert float(np.abs(cross_block_minors(a, k)).max()) < 1e-8
    assert minor_tangent_dimension(a, k) == k * (2 * n - k)


# --- A038 prediction 5: the forward implication, constructively ---------------


@pytest.mark.parametrize(("n", "k"), TANGENT_CASES)
def test_prediction_5_model_points_satisfy_every_minimal_minor(n: int, k: int) -> None:
    minors = cross_block_minors(_generic_point(n, k, seed=99), k)
    assert minors.size > 0
    assert float(np.abs(minors).max()) < 1e-8


# --- the open case is not silently claimed ------------------------------------


def test_a_matrix_off_the_model_violates_the_restriction() -> None:
    """Sanity: the minors are not vacuously zero on arbitrary matrices."""
    dense = np.ascontiguousarray(np.random.default_rng(5).normal(size=(8, 8)))
    assert float(np.abs(cross_block_minors(dense, 2)).max()) > 1e-3


# --- fail-closed ---------------------------------------------------------------


def test_rejects_non_float64() -> None:
    with pytest.raises(ValueError, match="float64"):
        cross_block_minors(np.eye(5, dtype=np.float32), 1)


def test_rejects_a_non_square_matrix() -> None:
    with pytest.raises(ValueError, match="square"):
        cross_block_minors(np.ones((4, 5)), 1)


def test_rejects_a_bool_factor_count() -> None:
    with pytest.raises(ValueError, match="int factor count"):
        restriction_has_content(10, True)


def test_rejects_a_zero_anchor_entry() -> None:
    a = _generic_point(6, 1)
    a[0, 1] = 0.0
    with pytest.raises(ValueError, match="nonzero anchor"):
        rank_one_completion(np.ascontiguousarray(a))


def test_tangent_dimension_refuses_an_empty_restriction() -> None:
    with pytest.raises(ValueError, match="restriction is empty"):
        minor_tangent_dimension(_generic_point(3, 1), 1)


def test_tangent_dimension_rejects_a_nonpositive_step() -> None:
    with pytest.raises(ValueError, match="positive finite-difference step"):
        minor_tangent_dimension(_generic_point(5, 1), 1, step=0.0)
