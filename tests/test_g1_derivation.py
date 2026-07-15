from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.sim.g1 import (
    analytic_targets,
    analytic_targets_via_reduced_form,
    build_fixture,
    canonical_target_hashes,
    load_g1_config,
    max_relative_discrepancy,
)


def _config_path() -> Path:
    return Path(__file__).parents[1] / "configs/g1.toml"


def test_frozen_fixture_matches_every_preregistered_analytic_anchor() -> None:
    config = load_g1_config(_config_path())
    fixture = build_fixture(config)
    targets = analytic_targets(fixture)
    hashes = canonical_target_hashes(targets, digits=config.analytic_round_digits)

    assert fixture.lambda_matrix.shape == (30, 30)
    assert fixture.gamma.shape == (30, 3)
    for covariance in (
        fixture.sigma_f,
        fixture.sigma_epsilon,
        fixture.sigma_u,
        fixture.sigma_v,
    ):
        assert np.min(np.linalg.eigvalsh(covariance)) > 0.0

    spectral_radius = float(
        np.max(np.abs(np.linalg.eigvals(fixture.feedback @ fixture.lambda_matrix)))
    )
    assert spectral_radius == pytest.approx(0.4104240453618892, rel=1e-12)
    assert float(
        np.linalg.cond(np.eye(30) - fixture.feedback @ fixture.lambda_matrix)
    ) == pytest.approx(1.696168836181463, rel=1e-12)
    assert float(np.min(targets.ols)) == pytest.approx(0.7724315312916856, rel=1e-12)
    assert float(np.max(targets.ols)) == pytest.approx(0.9138344677534321, rel=1e-12)
    assert float(np.min(targets.controlled)) == pytest.approx(0.7719001593131405, rel=1e-12)
    assert float(np.max(targets.controlled)) == pytest.approx(0.920182158950651, rel=1e-12)
    assert hashes.ols == config.ols_target_sha256
    assert hashes.controlled == config.proxy_target_sha256
    assert hashes.combined == config.combined_target_sha256


def test_primitive_bias_and_reduced_form_covariance_paths_agree() -> None:
    fixture = build_fixture(load_g1_config(_config_path()))

    primitive = analytic_targets(fixture)
    reduced_form = analytic_targets_via_reduced_form(fixture)

    np.testing.assert_allclose(primitive.ols, reduced_form.ols, rtol=0.0, atol=2e-13)
    np.testing.assert_allclose(primitive.controlled, reduced_form.controlled, rtol=0.0, atol=2e-13)


def test_preregistered_fixture_detects_missing_terms_and_transpose() -> None:
    config = load_g1_config(_config_path())
    fixture = build_fixture(config)
    targets = analytic_targets(fixture)

    omit_ols_simultaneity = fixture.lambda_matrix + targets.ols_confounding_bias
    omit_controlled_simultaneity = fixture.lambda_matrix + targets.controlled_confounding_bias
    omit_ols_confounding = fixture.lambda_matrix + targets.ols_simultaneity_bias
    omit_controlled_confounding = fixture.lambda_matrix + targets.controlled_simultaneity_bias

    assert max_relative_discrepancy(omit_ols_simultaneity, targets.ols) > config.relative_tolerance
    assert (
        max_relative_discrepancy(omit_controlled_simultaneity, targets.controlled)
        > config.relative_tolerance
    )
    assert max_relative_discrepancy(omit_ols_confounding, targets.ols) > config.relative_tolerance
    assert (
        max_relative_discrepancy(omit_controlled_confounding, targets.controlled)
        > config.relative_tolerance
    )
    assert max_relative_discrepancy(targets.ols.T, targets.ols) > config.relative_tolerance
    assert (
        max_relative_discrepancy(targets.controlled.T, targets.controlled)
        > config.relative_tolerance
    )

    identity = np.eye(fixture.n_assets, dtype=np.float64)
    reduced_form = np.linalg.solve(
        identity - fixture.feedback @ fixture.lambda_matrix,
        identity,
    )
    factor_flow = reduced_form @ (fixture.feedback @ fixture.gamma + fixture.delta_f)
    innovation_flow = reduced_form @ fixture.feedback
    flow_noise = reduced_form
    proxy_variance = fixture.sigma_f + fixture.sigma_epsilon
    rowwise_reliability = np.diag(np.diag(fixture.sigma_f) / np.diag(proxy_variance))
    wrong_residual_factor = rowwise_reliability @ fixture.sigma_f
    wrong_partial_flow = (
        factor_flow @ wrong_residual_factor @ factor_flow.T
        + innovation_flow @ fixture.sigma_u @ innovation_flow.T
        + flow_noise @ fixture.sigma_v @ flow_noise.T
    )
    wrong_numerator = (
        fixture.gamma @ wrong_residual_factor @ factor_flow.T + fixture.sigma_u @ innovation_flow.T
    )
    wrong_scalar_reliability_target = (
        fixture.lambda_matrix
        + np.linalg.solve(
            wrong_partial_flow.T,
            wrong_numerator.T,
        ).T
    )
    wrong_scalar_error = max_relative_discrepancy(
        wrong_scalar_reliability_target,
        targets.controlled,
    )
    assert wrong_scalar_error == pytest.approx(0.0076651747094962554, rel=1e-11)
    assert wrong_scalar_error > config.relative_tolerance


def test_perfect_proxy_removes_confounding_but_not_feedback_bias() -> None:
    fixture = build_fixture(load_g1_config(_config_path()))
    perfect_proxy = replace(fixture, sigma_epsilon=np.zeros_like(fixture.sigma_epsilon))

    targets = analytic_targets(perfect_proxy)

    np.testing.assert_allclose(targets.controlled_confounding_bias, 0.0, rtol=0.0, atol=1e-13)
    assert float(np.max(np.abs(targets.controlled_simultaneity_bias))) > 1e-4
    assert not np.allclose(targets.controlled, fixture.lambda_matrix, rtol=0.0, atol=1e-6)


def test_no_feedback_and_perfect_proxy_recovers_lambda() -> None:
    fixture = build_fixture(load_g1_config(_config_path()))
    identified = replace(
        fixture,
        feedback=np.zeros_like(fixture.feedback),
        sigma_epsilon=np.zeros_like(fixture.sigma_epsilon),
    )

    targets = analytic_targets(identified)

    np.testing.assert_allclose(targets.controlled, fixture.lambda_matrix, rtol=0.0, atol=1e-12)


def test_relative_discrepancy_has_no_zero_denominator_escape_hatch() -> None:
    estimate: NDArray[np.float64] = np.ones((2, 2), dtype=np.float64)
    target = estimate.copy()
    target[0, 0] = 0.0

    with pytest.raises(ValueError, match="target contains zero"):
        max_relative_discrepancy(estimate, target)


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ("n_samples = 10_000_000", "n_samples = 10_000_001", "divisible"),
        ("coefficient_count = 1800", "coefficient_count = 1799", "coefficient_count"),
        (
            'checkpoint_directory = "data/checkpoints/g1"',
            'checkpoint_directory = "../escape"',
            "stay below",
        ),
    ],
)
def test_load_g1_config_rejects_incoherent_contract(
    tmp_path: Path,
    old: str,
    new: str,
    message: str,
) -> None:
    config_path = tmp_path / "g1.toml"
    config_path.write_text(
        _config_path().read_text(encoding="utf-8").replace(old, new),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=message):
        load_g1_config(config_path)
