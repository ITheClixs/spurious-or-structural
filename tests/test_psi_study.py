from __future__ import annotations

import json
from itertools import pairwise
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from xid.models.rank_diagnostic import (
    null_projection,
    psi_k,
    psi_test,
    select_factor_count,
)

ROOT = Path(__file__).parents[1]
STUDY = ROOT / "docs" / "pre_results" / "generated" / "psi_study.json"

N = 30
K = 3


def _study() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(STUDY.read_text())
    return loaded


def _size_by_sample() -> dict[int, dict[str, Any]]:
    return {row["sample_size"]: row for row in _study()["size"]}


def _power_by_epsilon() -> dict[float, float]:
    return {row["epsilon"]: row["power"] for row in _study()["power"]}


# --- committed confirmatory study vs the A030 predictions ---------------------


def test_study_artifact_is_committed() -> None:
    assert STUDY.is_file()


def test_manifold_dimension_matches_the_derivation() -> None:
    study = _study()
    assert study["manifold_dimension"] == N + K * (2 * N - K)
    assert study["free_parameters"] == N * N
    assert abs(study["variance_inflation_factor"] - 1.134704) < 1e-5


def test_prediction_1_size_is_controlled_at_the_usable_sample_size() -> None:
    assert abs(_size_by_sample()[5000]["plug_in_size"] - 0.05) <= 0.045


def test_prediction_2_small_samples_over_reject() -> None:
    assert _size_by_sample()[500]["plug_in_size"] > 0.15


def test_prediction_3_size_improves_with_sample_size() -> None:
    rows = _size_by_sample()
    standard_error = _study()["size_monte_carlo_standard_error"]
    sizes = [rows[t]["plug_in_size"] for t in (500, 1000, 2000, 5000)]
    assert all(a >= b - standard_error for a, b in pairwise(sizes)), sizes


def test_prediction_4_variance_inflation_over_corrects() -> None:
    """Registered as not adopted: it removes all power."""
    assert all(row["inflated_size"] < 0.01 for row in _study()["size"])
    assert _study()["variance_inflation_adopted"] is False


def test_prediction_5_power_at_the_usable_sample_size() -> None:
    power = _power_by_epsilon()
    assert power[0.20] > 0.80
    assert power[0.05] <= 0.20


def test_power_is_nondecreasing_in_the_alternative() -> None:
    power = [row["power"] for row in _study()["power"]]
    assert all(a <= b for a, b in pairwise(power)), power


def test_study_scope_disclaims_market_relevance() -> None:
    assert "not a claim about market data" in _study()["scope"]


# --- fast component tests -----------------------------------------------------


def _one_spike_covariance() -> np.ndarray:
    q1 = N * 0.2827
    q0 = (N - q1) / (N - 1)
    m = np.full(N, 1.0 / np.sqrt(N))
    return q0 * np.eye(N) + (q1 - q0) * np.outer(m, m)


def _null_matrix() -> np.ndarray:
    rng = np.random.default_rng(1729)
    return np.asarray(
        np.diag(rng.uniform(0.2, 0.4, N))
        + rng.normal(size=(N, K)) @ rng.normal(size=(K, N)) * 0.05,
        dtype=np.float64,
    )


def test_null_projection_lands_in_the_null_set() -> None:
    projected = null_projection(_null_matrix(), K)
    assert psi_k(projected, K) < 1e-8


def test_factor_count_rule_recovers_the_true_count() -> None:
    """The registered Ahn-Horenstein rule, fixed before use."""
    assert select_factor_count(_null_matrix()) == K


def test_factor_count_rule_rejects_an_out_of_range_maximum() -> None:
    with pytest.raises(ValueError, match="k_max"):
        select_factor_count(_null_matrix(), k_max=N)


def test_psi_test_does_not_reject_a_matrix_drawn_from_the_null() -> None:
    rng = np.random.default_rng(1729)
    result = psi_test(_null_matrix(), K, _one_spike_covariance(), 5000, rng, 99)
    assert result.reject is False
    assert result.statistic >= 0.0
    assert result.critical_value > 0.0
    assert "plug-in bootstrap" in result.method


def test_psi_test_rejects_a_large_structural_alternative() -> None:
    rng = np.random.default_rng(1729)
    pert = np.random.default_rng(9191).normal(size=(N, N))
    pert -= np.diag(np.diag(pert))
    pert /= np.linalg.norm(pert)
    alternative = _null_matrix() + 0.6 * pert
    result = psi_test(alternative, K, _one_spike_covariance(), 5000, rng, 99)
    assert result.reject is True


def test_psi_test_rejects_a_bad_level() -> None:
    rng = np.random.default_rng(1729)
    with pytest.raises(ValueError, match="alpha"):
        psi_test(_null_matrix(), K, _one_spike_covariance(), 5000, rng, 99, alpha=1.0)


def test_psi_test_rejects_a_nonpositive_sample_size() -> None:
    rng = np.random.default_rng(1729)
    with pytest.raises(ValueError, match="sample_size"):
        psi_test(_null_matrix(), K, _one_spike_covariance(), 0, rng, 99)
