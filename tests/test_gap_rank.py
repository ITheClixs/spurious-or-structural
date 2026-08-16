from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.gap_rank import gap_factorisation, generic_gap_rank
from xid.models.identification import confounding_gap, numerical_rank

Matrix = NDArray[np.float64]

RTOL = 1e-9
DRAWS = 40
VIOLATION_DRAWS = 30

# (N, K, rank(B)) with the Section 3 expected rank appended.
CONFIGURATIONS = (
    (20, 3, 0, 3),
    (20, 3, 2, 5),
    (20, 3, 5, 8),
    (20, 1, 0, 1),
    (20, 1, 1, 2),
    (8, 3, 4, 7),
    (8, 3, 6, 8),
    (8, 5, 5, 8),
    (6, 4, 4, 6),
    (30, 10, 15, 25),
)
UNCAPPED = tuple(cfg for cfg in CONFIGURATIONS if cfg[1] + cfg[2] <= cfg[0])


def _positive_definite(n: int, rng: np.random.Generator) -> Matrix:
    noise = rng.normal(size=(n, n))
    return np.ascontiguousarray(noise @ noise.T / n + np.eye(n) * 0.6)


Primitives = tuple[Matrix, Matrix, Matrix, Matrix, Matrix, Matrix, Matrix]


def _primitives(n: int, k: int, rank_b: int, seed: int, violation: str = "none") -> Primitives:
    """Return ``(lam, b, gam, df, sf, su, sv)``, optionally breaking a hypothesis."""
    rng = np.random.default_rng(seed)
    lam = np.diag(rng.uniform(0.2, 0.4, n))
    gam = rng.normal(size=(n, k))
    df = rng.normal(size=(n, k))
    b_left, b_right = rng.normal(size=(n, rank_b)), rng.normal(size=(rank_b, n))
    b = b_left @ b_right * 0.02 if rank_b > 0 else np.zeros((n, n))
    sf, su, sv = (_positive_definite(d, rng) for d in (k, n, n))

    if violation == "gamma_zero":
        gam = np.zeros((n, k))
    elif violation == "gamma_rank_deficient":
        gam[:, k - 1] = gam[:, 0]
    elif violation == "column_overlap":
        gam[:, 0] = su @ b_right.T[:, 0]
    elif violation == "singular_factor_covariance":
        sf[:, k - 1] = 0.0
        sf[k - 1, :] = 0.0
    elif violation == "no_flow_loading":
        df, b = np.zeros((n, k)), np.zeros((n, n))

    contiguous = [np.ascontiguousarray(x, dtype=np.float64) for x in (lam, b, gam, df, sf, su, sv)]
    return (
        contiguous[0],
        contiguous[1],
        contiguous[2],
        contiguous[3],
        contiguous[4],
        contiguous[5],
        contiguous[6],
    )


# --- A036 prediction 1: the factorisation reproduces the gap ------------------


@pytest.mark.parametrize(("n", "k", "rank_b", "expected"), CONFIGURATIONS)
def test_prediction_1_factorisation_reproduces_the_gap(
    n: int, k: int, rank_b: int, expected: int
) -> None:
    for seed in range(1000, 1000 + DRAWS):
        primitives = _primitives(n, k, rank_b, seed)
        reference = confounding_gap(*primitives)
        product = gap_factorisation(*primitives).gap
        scale = max(1.0, float(np.abs(reference).max()))
        assert float(np.abs(product - reference).max()) / scale < 1e-12


# --- A036 prediction 2: the generic rank is min(N, K + rank(B)) ---------------


@pytest.mark.parametrize(("n", "k", "rank_b", "expected"), CONFIGURATIONS)
def test_prediction_2_observed_rank_equals_the_generic_value(
    n: int, k: int, rank_b: int, expected: int
) -> None:
    assert expected == min(n, k + rank_b)
    observed = set()
    for seed in range(1000, 1000 + DRAWS):
        primitives = _primitives(n, k, rank_b, seed)
        factors = gap_factorisation(*primitives)
        assert factors.feedback_rank == rank_b
        assert factors.inner_dimension == k + rank_b
        assert generic_gap_rank(k, primitives[1]) == expected
        observed.add(numerical_rank(factors.gap, rtol=RTOL))
    assert observed == {expected}


# --- A036 prediction 3: Sylvester's hypothesis holds where it is used ---------


@pytest.mark.parametrize(("n", "k", "rank_b", "expected"), UNCAPPED)
def test_prediction_3_both_factors_have_full_rank_in_the_uncapped_regime(
    n: int, k: int, rank_b: int, expected: int
) -> None:
    """Theorem 10 consumes exactly this; above the cap it no longer holds."""
    for seed in range(1000, 1000 + DRAWS):
        factors = gap_factorisation(*_primitives(n, k, rank_b, seed))
        assert numerical_rank(factors.left, rtol=RTOL) == expected
        assert numerical_rank(factors.right, rtol=RTOL) == expected


# --- A036 prediction 4: every hypothesis is load-bearing ----------------------


@pytest.mark.parametrize(
    ("violation", "expected"),
    (
        ("none", 7),
        ("gamma_zero", 4),
        ("gamma_rank_deficient", 6),
        ("column_overlap", 6),
        ("singular_factor_covariance", 6),
        ("no_flow_loading", 0),
    ),
)
def test_prediction_4_violating_a_hypothesis_lowers_the_rank(violation: str, expected: int) -> None:
    observed = {
        numerical_rank(gap_factorisation(*_primitives(20, 3, 4, seed, violation)).gap, rtol=RTOL)
        for seed in range(2000, 2000 + VIOLATION_DRAWS)
    }
    assert observed == {expected}


# --- A036 prediction 5: the two channels contribute separately ----------------


def test_prediction_5_without_priced_risk_only_feedback_remains() -> None:
    for seed in range(2000, 2000 + VIOLATION_DRAWS):
        primitives = _primitives(20, 3, 4, seed, "gamma_zero")
        assert numerical_rank(gap_factorisation(*primitives).gap, rtol=RTOL) == 4


def test_prediction_5_without_feedback_only_the_factor_channel_remains() -> None:
    for seed in range(2000, 2000 + VIOLATION_DRAWS):
        primitives = _primitives(20, 3, 0, seed)
        assert numerical_rank(gap_factorisation(*primitives).gap, rtol=RTOL) == 3


# --- fail-closed --------------------------------------------------------------


def test_rejects_non_float64() -> None:
    lam, b, gam, df, sf, su, sv = _primitives(6, 2, 1, 5)
    with pytest.raises(ValueError, match="float64"):
        gap_factorisation(lam, b, gam.astype(np.float32), df, sf, su, sv)


def test_rejects_shape_mismatch() -> None:
    lam, b, gam, df, sf, su, sv = _primitives(6, 2, 1, 5)
    with pytest.raises(ValueError, match="expected shape"):
        gap_factorisation(lam, b, gam, df[:, :1], sf, su, sv)


def test_rejects_indefinite_residual_covariance() -> None:
    lam, b, gam, df, sf, su, _ = _primitives(6, 2, 1, 5)
    with pytest.raises(ValueError, match="positive definite"):
        gap_factorisation(lam, b, gam, df, sf, su, np.zeros((6, 6)))


def test_rejects_a_system_with_no_reduced_form() -> None:
    lam, _, gam, df, sf, su, sv = _primitives(6, 2, 1, 5)
    singular_feedback = np.ascontiguousarray(np.linalg.inv(lam))
    with pytest.raises(ValueError, match="no reduced form"):
        gap_factorisation(lam, singular_feedback, gam, df, sf, su, sv)


def test_generic_rank_caps_at_the_cross_section_size() -> None:
    assert generic_gap_rank(30, np.eye(8)) == 8
    assert generic_gap_rank(0, np.zeros((8, 8))) == 0


def test_generic_rank_rejects_a_bool_factor_count() -> None:
    with pytest.raises(ValueError, match="int factor count"):
        generic_gap_rank(True, np.eye(4))
