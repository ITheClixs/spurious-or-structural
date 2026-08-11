from __future__ import annotations

from itertools import pairwise

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.identification import confounding_gap
from xid.models.rank_diagnostic import decompose, psi_k

N = 30
K = 3
PERTURBATION_GRID = (0.0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3)


def _diagonal_plus_rank_k(seed: int) -> NDArray[np.float64]:
    rng = np.random.default_rng(seed)
    diagonal = np.diag(rng.uniform(0.2, 0.4, N))
    low_rank = rng.normal(size=(N, K)) @ rng.normal(size=(K, N)) * 0.05
    return np.asarray(diagonal + low_rank, dtype=np.float64)


def _unit_offdiagonal_perturbation(seed: int) -> NDArray[np.float64]:
    rng = np.random.default_rng(seed)
    pert = rng.normal(size=(N, N))
    pert -= np.diag(np.diag(pert))
    return np.asarray(pert / np.linalg.norm(pert), dtype=np.float64)


def test_exact_structure_gives_zero_statistic() -> None:
    """A028 prediction 2: the pure-confounding null has population value zero."""
    assert psi_k(_diagonal_plus_rank_k(1729), K) < 1e-8


def test_population_confounded_coefficient_matrix_passes_the_null() -> None:
    """The actual plim under a diagonal truth must sit in the diagonal+rank-K set."""
    rng = np.random.default_rng(1729)

    def psd(n: int) -> NDArray[np.float64]:
        a = rng.normal(size=(n, n))
        return np.asarray(a @ a.T / n + np.eye(n) * 0.5, dtype=np.float64)

    _ = rng.normal(scale=0.1, size=(N, N))
    gam = rng.normal(size=(N, K))
    df = rng.normal(size=(N, K))
    sf, su, sv = psd(K), psd(N), psd(N)
    diagonal_truth = np.diag(rng.uniform(0.2, 0.4, N))
    zero_b = np.zeros((N, N))
    coefficient = diagonal_truth + confounding_gap(diagonal_truth, zero_b, gam, df, sf, su, sv)
    assert psi_k(coefficient, K) < 1e-8


def test_statistic_increases_strictly_with_structural_perturbation() -> None:
    """A028 prediction 3: strict monotonicity over the frozen grid."""
    base = _diagonal_plus_rank_k(1729)
    pert = _unit_offdiagonal_perturbation(9191)
    values = [psi_k(base + eps * pert, K) for eps in PERTURBATION_GRID]
    assert all(a < b for a, b in pairwise(values)), values


def test_statistic_is_permutation_invariant() -> None:
    """A028 prediction 5: relabelling assets cannot change the statistic."""
    rng = np.random.default_rng(9191)
    a = _diagonal_plus_rank_k(1729) + 0.05 * rng.normal(size=(N, N))
    perm = rng.permutation(N)
    assert abs(psi_k(a, K) - psi_k(a[np.ix_(perm, perm)], K)) < 1e-12


def test_statistic_is_scale_free() -> None:
    a = _diagonal_plus_rank_k(1729) + 0.05 * _unit_offdiagonal_perturbation(9191)
    assert abs(psi_k(a, K) - psi_k(7.5 * a, K)) < 1e-12


def test_higher_assumed_factor_count_weakens_the_test() -> None:
    """Overstating K shrinks the statistic mechanically; the memo must say so."""
    a = _diagonal_plus_rank_k(1729) + 0.1 * _unit_offdiagonal_perturbation(9191)
    assert psi_k(a, K + 3) < psi_k(a, K)


def test_decompose_reconstructs_within_residual() -> None:
    a = _diagonal_plus_rank_k(1729)
    diagonal_part, low_rank_part = decompose(a, K)
    assert float(np.linalg.norm(a - diagonal_part - low_rank_part)) < 1e-8
    assert int(np.linalg.matrix_rank(low_rank_part)) <= K
    off_diagonal = diagonal_part - np.diag(np.diag(diagonal_part))
    assert float(np.abs(off_diagonal).max()) == 0.0


def test_full_rank_budget_absorbs_everything() -> None:
    rng = np.random.default_rng(314159)
    a = np.asarray(rng.normal(size=(N, N)), dtype=np.float64)
    assert psi_k(a, N) < 1e-8


def test_rejects_rank_larger_than_dimension() -> None:
    with pytest.raises(ValueError, match="k"):
        psi_k(_diagonal_plus_rank_k(1729), N + 1)


def test_rejects_negative_rank() -> None:
    with pytest.raises(ValueError, match="k"):
        psi_k(_diagonal_plus_rank_k(1729), -1)


def test_rejects_non_float64() -> None:
    with pytest.raises(ValueError, match="float64"):
        psi_k(_diagonal_plus_rank_k(1729).astype(np.float32), K)


def test_rejects_nonfinite() -> None:
    a = _diagonal_plus_rank_k(1729)
    a[0, 0] = np.inf
    with pytest.raises(ValueError, match="finite"):
        psi_k(a, K)


def test_rejects_non_square() -> None:
    with pytest.raises(ValueError, match="square"):
        psi_k(np.zeros((N, N - 1)), K)


def test_purely_diagonal_matrix_has_zero_offdiagonal_energy() -> None:
    assert psi_k(np.diag(np.linspace(0.2, 0.4, N)), K) == 0.0
