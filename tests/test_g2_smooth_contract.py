from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import pytest

import xid.sim.g2 as g2_module
from xid.sim.g2 import load_g2_contract, validate_g2_contract


def _root() -> Path:
    return Path(__file__).parents[1]


def test_g2_contract_projects_every_smooth_estimator_threshold() -> None:
    contract = load_g2_contract(_root())

    assert contract.ridge_condition_cap == 10_000.0
    assert contract.ridge_floor_trace_ratio == 1e-6
    assert contract.ridge_negative_eigen_roundoff_multiplier == 100.0
    assert contract.ridge_post_condition_slack_multiplier == 1_000.0
    assert contract.pca_top_eigengap_min_trace_ratio == 1e-10
    assert contract.pooled_rank_multiplier == 3.0
    assert contract.pooled_condition_number_max == 1e12


@pytest.mark.parametrize(
    ("field", "replacement"),
    (
        ("ridge_condition_cap", 9_999.0),
        ("ridge_floor_trace_ratio", 0.0),
        ("ridge_negative_eigen_roundoff_multiplier", 101.0),
        ("ridge_post_condition_slack_multiplier", 999.0),
        ("pca_top_eigengap_min_trace_ratio", 1e-9),
        ("pooled_rank_multiplier", 4.0),
        ("pooled_condition_number_max", 1e11),
    ),
)
def test_g2_contract_rejects_changed_smooth_estimator_thresholds(
    field: str,
    replacement: float,
) -> None:
    contract = load_g2_contract(_root())

    with pytest.raises(ValueError, match="estimator numerics"):
        validate_g2_contract(replace(contract, **cast(Any, {field: replacement})))


def test_g2_contract_rejects_equality_compatible_estimator_types() -> None:
    contract = load_g2_contract(_root())

    with pytest.raises(ValueError, match="scalar fields changed representation"):
        validate_g2_contract(replace(contract, ridge_condition_cap=cast(Any, 10_000)))


def test_g2_contract_rejects_changed_text_encoded_numerical_rule(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_directory = tmp_path / "configs"
    config_directory.mkdir()
    original_config = (_root() / "configs" / "g2.toml").read_bytes()
    altered_config = original_config.replace(
        b"machine_epsilon_times_three_times_largest_singular_value",
        b"machine_epsilon_times_four_times_largest_singular_value",
    )
    assert altered_config != original_config
    (config_directory / "g2.toml").write_bytes(altered_config)
    (config_directory / "g2_population_targets.json").write_bytes(
        (_root() / "configs" / "g2_population_targets.json").read_bytes()
    )
    monkeypatch.setattr(
        g2_module,
        "FROZEN_G2_SEALS",
        replace(
            g2_module.FROZEN_G2_SEALS,
            config_sha256=hashlib.sha256(altered_config).hexdigest(),
        ),
    )

    with pytest.raises(ValueError, match="changed its sealed numerical rule"):
        load_g2_contract(tmp_path)
