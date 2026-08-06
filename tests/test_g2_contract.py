from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest

from xid.sim.g2 import (
    FROZEN_G2_SEALS,
    G2Seals,
    PaperReconstructionContract,
    PaperSpecificationContract,
    TestRngNamespace,
    float64_le_sha256,
    load_g2_contract,
    semantic_target_bytes,
    validate_g2_contract,
    validate_g2_seals,
)

_TEST_SEED = 1729


def _root() -> Path:
    return Path(__file__).parents[1]


def test_s0004_contract_reproduces_all_four_a005_seals() -> None:
    contract = load_g2_contract(_root())

    assert contract.seals == FROZEN_G2_SEALS
    assert contract.seals == G2Seals(
        config_sha256="f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc",
        target_raw_sha256="f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59",
        target_semantic_sha256=("f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a"),
        lasso_ratio_sha256=("1da884c55b3f6e7bf79012973bddf092a92efb1ea098cd2717a804645a62c9a0"),
    )
    assert contract.config_schema_version == 3
    assert contract.target_schema_version == 3
    assert contract.target_config_schema_version == 3
    assert contract.design_id == "S0004"
    assert contract.target_design_id == "S0004"
    assert len(contract.population_targets) == 17
    assert len(contract.lasso_ratio_grid) == 40


def test_raw_and_semantic_target_seals_have_distinct_roles() -> None:
    raw = (_root() / "configs/g2_population_targets.json").read_bytes()
    value = json.loads(raw)
    canonical = semantic_target_bytes(value, digits=12)
    whitespace_only = json.dumps(value, indent=2, sort_keys=False).encode("utf-8") + b"\n"

    assert len(canonical) == 12_926
    assert hashlib.sha256(raw).hexdigest() == FROZEN_G2_SEALS.target_raw_sha256
    assert hashlib.sha256(whitespace_only).hexdigest() != FROZEN_G2_SEALS.target_raw_sha256
    assert hashlib.sha256(canonical).hexdigest() == FROZEN_G2_SEALS.target_semantic_sha256
    reformatted_semantic = semantic_target_bytes(json.loads(whitespace_only), digits=12)
    assert hashlib.sha256(reformatted_semantic).hexdigest() == (
        FROZEN_G2_SEALS.target_semantic_sha256
    )

    changed = json.loads(raw)
    changed["targets"][0]["lambda_offdiag"] += 1e-9
    assert hashlib.sha256(semantic_target_bytes(changed, digits=12)).hexdigest() != (
        FROZEN_G2_SEALS.target_semantic_sha256
    )


def test_lasso_ratio_literals_are_exact_binary64_data() -> None:
    contract = load_g2_contract(_root())
    ratios = np.asarray(contract.lasso_ratio_grid, dtype="<f8")

    assert ratios.shape == (40,)
    assert ratios.flags.c_contiguous
    assert np.all(np.isfinite(ratios))
    assert np.all(np.diff(ratios) < 0.0)
    assert ratios[0] == 1.0
    assert ratios[-1] == 0.0001
    assert float64_le_sha256(contract.lasso_ratio_grid) == FROZEN_G2_SEALS.lasso_ratio_sha256


def test_paper_reconstruction_contract_projects_every_solver_threshold() -> None:
    contract = load_g2_contract(_root())
    paper = contract.paper_reconstruction

    assert type(paper) is PaperReconstructionContract
    assert paper.names == ("PI_1", "PI_I", "CI_1", "CI_I", "PI_CC", "CI_CC")
    assert paper.label == "paper_protocol_reconstruction"
    assert paper.fit_window_bins == 30
    assert paper.test_window_bins == 30
    assert paper.eligible_fit_blocks_per_date == 10
    assert paper.cv_validation_ranges == ((0, 6), (6, 12), (12, 18), (18, 24), (24, 30))
    assert paper.best_level_index == 0
    assert paper.lambda_grid_size == 40
    assert paper.lambda_min_ratio == 0.0001
    assert paper.selected_ratio_tolerance == 1e-12
    assert paper.post_fwl_zero_norm_multiplier == 100.0
    assert paper.coordinate_descent_tolerance == 1e-10
    assert paper.kkt_tolerance == 1e-9
    assert paper.maximum_iterations == 10_000
    assert paper.pca_top_eigengap_min_trace_ratio == 1e-10
    assert paper.bootstrap_replicates == 499
    assert paper.specifications == (
        PaperSpecificationContract(
            name="PI_1",
            feature_map="own_best_level_ofi",
            estimator="ols",
            unpenalized=("intercept", "own_best_level_ofi"),
            penalized=(),
        ),
        PaperSpecificationContract(
            name="PI_I",
            feature_map="own_integrated_top10_ofi",
            estimator="ols",
            unpenalized=("intercept", "own_integrated_top10_ofi"),
            penalized=(),
        ),
        PaperSpecificationContract(
            name="CI_1",
            feature_map="all_assets_best_level_ofi",
            estimator="lasso_per_response",
            unpenalized=("intercept",),
            penalized=("all_30_best_level_flows",),
        ),
        PaperSpecificationContract(
            name="CI_I",
            feature_map="all_assets_integrated_top10_ofi",
            estimator="lasso_per_response",
            unpenalized=("intercept",),
            penalized=("all_30_integrated_flows",),
        ),
        PaperSpecificationContract(
            name="PI_CC",
            feature_map="best_level_cross_section_pc1_plus_own_orthogonal_residual",
            estimator="ols",
            unpenalized=("intercept", "cross_section_pc1", "own_residual_flow"),
            penalized=(),
        ),
        PaperSpecificationContract(
            name="CI_CC",
            feature_map="best_level_cross_section_pc1_plus_all_orthogonal_residuals",
            estimator="lasso_per_response",
            unpenalized=("intercept", "cross_section_pc1"),
            penalized=("all_30_residual_flows",),
        ),
    )


def test_paper_reconstruction_contract_projects_cache_and_aggregation_rules() -> None:
    contract = load_g2_contract(_root())
    paper = contract.paper_reconstruction

    assert paper.coefficient_aggregation == "equal_mean_within_date_then_equal_mean_across_dates"
    assert paper.prediction_aggregation == "pooled_next_block_sse_and_sst"
    assert paper.bootstrap_aggregation == (
        "cached_date_level_operator_sse_sst_summaries_with_shared_date_weights"
    )
    assert paper.bootstrap_refit is False
    assert paper.date_cache_matrices == (
        "PI_1_direct",
        "PI_I_direct",
        "CI_1_direct",
        "CI_I_direct",
        "PI_CC_purged",
        "CI_CC_purged",
        "PI_CC_full_response",
        "CI_CC_full_response",
        "cc_mean_projection_p_perp",
    )
    assert paper.date_cache_losses == "six_specs_times_thirty_responses_times_sse_and_sst"
    assert paper.reported_coefficient_maps == (
        "first_eight_date_cache_matrices_all_7200_entries_with_model_restriction_zeros_explicit_"
        "and_each_with_named_normal_and_basic_date_bootstrap_intervals"
    )
    assert paper.reported_oos_values == (
        "six_specs_times_thirty_response_level_r_squared_180_each_with_named_normal_and_basic_"
        "date_bootstrap_intervals"
    )
    assert paper.cache_only_fields == (
        "cc_mean_projection_p_perp_and_360_sse_sst_components_are_internal_inputs_not_"
        "separately_claimed_numbers"
    )


def test_paper_reconstruction_contract_rejects_value_and_representation_drift() -> None:
    contract = load_g2_contract(_root())
    paper = contract.paper_reconstruction
    altered_contracts = (
        replace(
            contract,
            paper_reconstruction=replace(paper, coordinate_descent_tolerance=1e-9),
        ),
        replace(
            contract,
            paper_reconstruction=replace(paper, selected_ratio_tolerance=-1e-12),
        ),
        replace(
            contract,
            paper_reconstruction=replace(paper, maximum_iterations=True),
        ),
        replace(
            contract,
            paper_reconstruction=replace(
                paper,
                cv_validation_ranges=cast(Any, list(paper.cv_validation_ranges)),
            ),
        ),
        replace(
            contract,
            paper_reconstruction=replace(
                paper,
                specifications=paper.specifications[:-1],
            ),
        ),
        replace(
            contract,
            paper_reconstruction=replace(
                paper,
                specifications=cast(Any, list(paper.specifications)),
            ),
        ),
        replace(
            contract,
            paper_reconstruction=replace(
                paper,
                date_cache_matrices=cast(Any, list(paper.date_cache_matrices)),
            ),
        ),
        replace(
            contract,
            paper_reconstruction=replace(paper, bootstrap_refit=cast(Any, 0)),
        ),
    )

    for altered in altered_contracts:
        with pytest.raises(ValueError, match="sealed G2 contract"):
            validate_g2_contract(altered)


def test_stale_or_mixed_g2_schema_is_non_executable() -> None:
    contract = load_g2_contract(_root())
    altered_contracts = (
        replace(contract, config_schema_version=2),
        replace(contract, target_schema_version=2),
        replace(contract, target_config_schema_version=2),
        replace(contract, design_id="S0003"),
        replace(contract, target_design_id="S0003"),
    )

    for altered in altered_contracts:
        with pytest.raises(ValueError, match="sealed G2 contract"):
            validate_g2_contract(altered)


def test_every_executable_contract_family_is_revalidated() -> None:
    contract = load_g2_contract(_root())
    changed_target = replace(contract.population_targets[0], gamma=0.0)
    one_ulp_target = replace(
        contract.population_targets[0],
        gamma=float(np.nextafter(contract.population_targets[0].gamma, np.inf)),
    )
    string_streams = tuple(
        (stream.value, phase, scenario) for stream, phase, scenario in contract.phase_scenarios
    )
    integer_shape_components = tuple(
        (int(component), shape) for component, shape in contract.draw_shapes
    )
    altered_contracts = (
        replace(contract, n_assets=31),
        replace(contract, n_assets=cast(Any, 30.0)),
        replace(contract, config_schema_version=cast(Any, 3.0)),
        replace(contract, confirmatory_ar1=0.4),
        replace(contract, iid_ar1=-0.0),
        replace(contract, confirmatory_reliability=0.90),
        replace(contract, registered_seeds=(1, 2, 3)),
        replace(
            contract,
            registered_seeds=cast(
                Any,
                (
                    float(contract.registered_seeds[0]),
                    *contract.registered_seeds[1:],
                ),
            ),
        ),
        replace(contract, phase_scenarios=contract.phase_scenarios[:-1]),
        replace(contract, phase_scenarios=cast(Any, string_streams)),
        replace(contract, draw_shapes=contract.draw_shapes[:-1]),
        replace(contract, draw_shapes=cast(Any, integer_shape_components)),
        replace(contract, lasso_ratio_grid=contract.lasso_ratio_grid[:-1]),
        replace(contract, lasso_ratio_grid=cast(Any, list(contract.lasso_ratio_grid))),
        replace(contract, population_targets=cast(Any, list(contract.population_targets))),
        replace(
            contract,
            population_targets=(changed_target, *contract.population_targets[1:]),
        ),
        replace(
            contract,
            population_targets=(one_ulp_target, *contract.population_targets[1:]),
        ),
    )

    for altered in altered_contracts:
        with pytest.raises(ValueError, match="sealed G2 contract"):
            validate_g2_contract(altered)


def test_draw_authority_revalidates_contract_before_seedsequence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, master_seed=_TEST_SEED)
    address = namespace.dgp_address(
        stream=next(stream for stream, phase, _ in contract.phase_scenarios if phase == 20),
        n_dates=252,
        panel_index=0,
        date_index=0,
        component=next(component for component, value in contract.component_ids if value == 1),
    )
    object.__setattr__(namespace, "contract", replace(contract, design_id="S0003"))

    def forbidden_seed_sequence(*args: object, **kwargs: object) -> None:
        raise AssertionError("RNG was reached before contract validation")

    monkeypatch.setattr(np.random, "SeedSequence", forbidden_seed_sequence)
    with pytest.raises(ValueError, match="sealed G2 contract"):
        namespace.draw_standard_normal(address)


def test_seal_validation_names_the_corrupted_role() -> None:
    for field in (
        "config_sha256",
        "target_raw_sha256",
        "target_semantic_sha256",
        "lasso_ratio_sha256",
    ):
        altered = replace(FROZEN_G2_SEALS, **{field: "0" * 64})
        with pytest.raises(ValueError, match=field):
            validate_g2_seals(altered)
