from __future__ import annotations

import gc
import math
import weakref
from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import numpy as np
import pytest

import xid.models.g2_smooth as smooth_module
from xid.models.g2_smooth import (
    ConditionRidgeResult,
    G2FlowView,
    HomogeneousResult,
    SmoothAggregateMoments,
    SmoothBasePanelMoments,
    SmoothCellPanelMoments,
    aggregate_contract_smooth_moments,
    aggregate_smooth_moments,
    build_cell_date_moments,
    build_contract_cell_date_moments,
    build_contract_smooth_date_design,
    build_smooth_date_design,
    extract_condition_ridge_moments,
    extract_homogeneous_moments,
    fit_condition_ridge,
    fit_homogeneous_ols,
    integrate_ofi_pc1,
    pack_symmetric_upper,
    solve_condition_ridge,
    solve_pooled_homogeneous,
    stack_base_moments,
    stack_cell_moments,
    stack_contract_base_moments,
    stack_contract_cell_moments,
    unpack_symmetric_upper,
    validate_aggregate_response_map,
)
from xid.sim.g2 import (
    G2Stream,
    TestRngNamespace,
    build_cell,
    load_g2_contract,
    transform_date,
)


def _root() -> Path:
    return Path(__file__).parents[1]


def _repeated_levels(flow: np.ndarray, n_levels: int = 2) -> np.ndarray:
    return np.repeat(flow[:, :, None], n_levels, axis=2).astype(np.float64)


def _fit_analytic_ridge(
    aggregate: SmoothAggregateMoments,
    *,
    flow_view: G2FlowView,
    reliability: float,
) -> ConditionRidgeResult:
    contract = load_g2_contract(_root())
    moments = extract_condition_ridge_moments(
        aggregate,
        flow_view=flow_view,
        reliability=reliability,
    )
    return solve_condition_ridge(
        moments.flow_covariance,
        moments.response_flow_covariance,
        contract=contract,
    )


def _fit_analytic_homogeneous(
    aggregate: SmoothAggregateMoments,
    *,
    reliability: float,
) -> HomogeneousResult:
    contract = load_g2_contract(_root())
    moments = extract_homogeneous_moments(aggregate, reliability=reliability)
    return solve_pooled_homogeneous(
        moments.slope_covariance,
        moments.slope_response_covariance,
        predictor_means=moments.predictor_means,
        response_mean=moments.response_mean,
        contract=contract,
    )


def test_upper_packing_is_row_major_exact_and_fail_closed() -> None:
    matrix = np.asarray(
        [[1.0, 2.0, 3.0], [2.0, 4.0, 5.0], [3.0, 5.0, 6.0]],
        dtype=np.float64,
    )

    packed = pack_symmetric_upper(matrix)

    np.testing.assert_array_equal(packed, np.asarray([1, 2, 3, 4, 5, 6], dtype=np.float64))
    np.testing.assert_array_equal(unpack_symmetric_upper(packed, size=3), matrix)
    assert packed.flags.c_contiguous
    assert not packed.flags.writeable
    with pytest.raises(ValueError, match="symmetric"):
        pack_symmetric_upper(np.asarray([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64))
    with pytest.raises(ValueError, match="packed"):
        unpack_symmetric_upper(np.ones(5, dtype=np.float64), size=3)


def test_integrated_pc1_centers_orients_and_l1_normalizes() -> None:
    a = np.asarray([-3.0, -1.0, 1.0, 3.0], dtype=np.float64)
    one_asset = np.column_stack((-a, 2.0 * a))
    levels = one_asset[:, None, :]

    result = integrate_ofi_pc1(levels, eigengap_ratio=1e-10)
    shifted = integrate_ofi_pc1(
        levels + np.asarray([100.0, -7.0], dtype=np.float64)[None, None, :],
        eigengap_ratio=1e-10,
    )
    permutation = np.asarray([2, 0, 3, 1])
    permuted = integrate_ofi_pc1(levels[permutation], eigengap_ratio=1e-10)

    np.testing.assert_allclose(
        result.loadings[0],
        np.asarray([-1.0, 2.0], dtype=np.float64) / math.sqrt(5.0),
        rtol=0.0,
        atol=3e-16,
    )
    np.testing.assert_allclose(result.scores[:, 0], (5.0 / 3.0) * a, rtol=0.0, atol=2e-15)
    np.testing.assert_allclose(shifted.scores, result.scores, rtol=0.0, atol=2e-14)
    np.testing.assert_allclose(permuted.loadings, result.loadings, rtol=0.0, atol=3e-16)
    np.testing.assert_allclose(
        permuted.scores,
        result.scores[permutation],
        rtol=0.0,
        atol=2e-15,
    )
    assert result.covariance_traces[0] == pytest.approx(25.0, rel=0.0, abs=1e-15)
    assert not result.scores.flags.writeable
    assert not result.loadings.flags.writeable


def test_integrated_pc1_uses_first_index_tie_and_rejects_weak_or_bad_inputs() -> None:
    a = np.asarray([-3.0, -1.0, 1.0, 3.0], dtype=np.float64)
    tied_loading = np.column_stack((a, -a))[:, None, :]

    result = integrate_ofi_pc1(tied_loading, eigengap_ratio=1e-10)

    np.testing.assert_allclose(
        result.loadings[0],
        np.asarray([1.0, -1.0], dtype=np.float64) / math.sqrt(2.0),
        rtol=0.0,
        atol=3e-16,
    )
    np.testing.assert_allclose(result.scores[:, 0], a, rtol=0.0, atol=2e-15)

    isotropic = np.asarray([[1, 0], [-1, 0], [0, 1], [0, -1]], dtype=np.float64)[:, None, :]
    with pytest.raises(ValueError, match="eigengap"):
        integrate_ofi_pc1(isotropic, eigengap_ratio=1e-10)
    with pytest.raises(ValueError, match="trace"):
        integrate_ofi_pc1(np.zeros((4, 1, 2), dtype=np.float64), eigengap_ratio=1e-10)
    nonfinite = tied_loading.copy()
    nonfinite[0, 0, 0] = np.nan
    with pytest.raises(ValueError, match="nonfinite"):
        integrate_ofi_pc1(nonfinite, eigengap_ratio=1e-10)


def _ridge_fixture_panels() -> tuple[
    SmoothBasePanelMoments,
    SmoothCellPanelMoments,
    np.ndarray,
]:
    contract = load_g2_contract(_root())
    z = np.asarray([1.0, 1.0, -1.0, -1.0], dtype=np.float64)
    q = np.asarray([[3, 0], [1, -2], [-1, 0], [-3, 2]], dtype=np.float64)
    r = np.asarray([[18, 6], [8, 0], [0, 14], [2, 24]], dtype=np.float64)
    designs = []
    cells = []
    for date_index, rows in enumerate((slice(0, 2), slice(2, 4))):
        design = build_smooth_date_design(
            date_index=date_index,
            factor=z[rows],
            proxy_noise=np.zeros(2, dtype=np.float64),
            oracle_flow=q[rows],
            level_flows=_repeated_levels(q[rows]),
            eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
        )
        designs.append(design)
        cells.append(build_cell_date_moments(design, r[rows]))
    return stack_base_moments(designs), stack_cell_moments(cells), r


def test_analytic_stackers_snapshot_stateful_sequences_once() -> None:
    class SwitchingSequence:
        def __init__(self, first: tuple[object, ...], later: tuple[object, ...]) -> None:
            self._first = first
            self._later = later
            self.traversals = 0

        def __len__(self) -> int:
            return len(self._first)

        def __getitem__(self, index: int) -> object:
            if index >= len(self._first):
                raise IndexError(index)
            if index == 0:
                self.traversals += 1
            values = self._first if self.traversals == 1 else self._later
            return values[index]

    contract = load_g2_contract(_root())
    factor = np.asarray([1.0, -1.0], dtype=np.float64)
    designs = []
    cells = []
    substitute_bases = []
    substitute_cells = []
    for date_index in range(2):
        q = np.asarray(
            [[1.0 + date_index, -1.0], [-1.0 - date_index, 1.0]],
            dtype=np.float64,
        )
        design = build_smooth_date_design(
            date_index=date_index,
            factor=factor,
            proxy_noise=np.zeros(2, dtype=np.float64),
            oracle_flow=q,
            level_flows=_repeated_levels(q),
            eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
        )
        cell = build_cell_date_moments(design, q)
        zero_base = np.zeros_like(design.base_moments.x0tx0_upper)
        zero_base.setflags(write=False)
        zero_cell = np.zeros_like(cell.x0ty)
        zero_cell.setflags(write=False)
        designs.append(design)
        cells.append(cell)
        substitute_bases.append(replace(design.base_moments, x0tx0_upper=zero_base))
        substitute_cells.append(replace(cell, x0ty=zero_cell))

    base_sequence = SwitchingSequence(
        tuple(designs),
        tuple(substitute_bases),
    )
    cell_sequence = SwitchingSequence(
        tuple(cells),
        tuple(substitute_cells),
    )

    base_panel = stack_base_moments(base_sequence)  # type: ignore[arg-type]
    cell_panel = stack_cell_moments(cell_sequence)  # type: ignore[arg-type]

    assert base_sequence.traversals == 1
    assert cell_sequence.traversals == 1
    np.testing.assert_array_equal(
        base_panel.x0tx0_upper,
        np.stack([design.base_moments.x0tx0_upper for design in designs], axis=0),
    )
    np.testing.assert_array_equal(
        cell_panel.x0ty,
        np.stack([cell.x0ty for cell in cells], axis=0),
    )


def test_ridge_uses_global_centering_proxy_schur_and_response_by_flow_orientation() -> None:
    base_panel, cell_panel, _ = _ridge_fixture_panels()
    aggregate = aggregate_smooth_moments(
        base_panel,
        cell_panel,
        np.ones(2, dtype=np.float64),
    )

    result = _fit_analytic_ridge(
        aggregate,
        flow_view=G2FlowView.ORACLE,
        reliability=1.0,
    )

    expected = np.asarray([[2.0, 3.0], [-1.0, 4.0]], dtype=np.float64) / 1.000001
    np.testing.assert_allclose(result.coefficients, expected, rtol=0.0, atol=3e-15)
    assert aggregate.row_mass == 4.0
    assert result.penalty_condition == 0.0
    assert result.penalty_floor == pytest.approx(1e-6, rel=0.0, abs=3e-21)
    assert result.penalty == result.penalty_floor


def test_oracle_and_observable_ridge_select_distinct_flow_blocks() -> None:
    contract = load_g2_contract(_root())
    z = np.asarray([1, 1, 1, 1, -1, -1, -1, -1], dtype=np.float64)
    q = np.column_stack(
        (
            np.asarray([1, 1, -1, -1, 1, 1, -1, -1], dtype=np.float64),
            np.asarray([1, -1, 1, -1, 1, -1, 1, -1], dtype=np.float64),
        )
    )
    coefficient = np.asarray([[2.0, 3.0], [-1.0, 4.0]], dtype=np.float64)
    response = q @ coefficient.T + np.outer(z, np.asarray([0.7, -0.2]))
    design = build_smooth_date_design(
        date_index=0,
        factor=z,
        proxy_noise=np.zeros(8, dtype=np.float64),
        oracle_flow=q,
        level_flows=_repeated_levels(2.0 * q),
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    aggregate = aggregate_smooth_moments(
        stack_base_moments((design,)),
        stack_cell_moments((build_cell_date_moments(design, response),)),
        np.ones(1, dtype=np.float64),
    )

    oracle = _fit_analytic_ridge(
        aggregate,
        flow_view=G2FlowView.ORACLE,
        reliability=1.0,
    )
    observable = _fit_analytic_ridge(
        aggregate,
        flow_view=G2FlowView.OBSERVABLE,
        reliability=1.0,
    )

    np.testing.assert_allclose(
        oracle.coefficients,
        coefficient / 1.000001,
        rtol=0.0,
        atol=3e-15,
    )
    np.testing.assert_allclose(
        observable.coefficients,
        coefficient / (2.0 * 1.000001),
        rtol=0.0,
        atol=2e-15,
    )
    assert oracle.penalty_floor == pytest.approx(1e-6, rel=0.0, abs=3e-21)
    assert observable.penalty_floor == pytest.approx(4e-6, rel=0.0, abs=2e-20)


def test_aggregation_rejects_cell_moments_from_another_design() -> None:
    contract = load_g2_contract(_root())
    q_a = np.asarray([[-3.0, -1.0], [-1.0, 2.0], [1.0, -2.0], [3.0, 1.0]])
    q_b = 2.0 * q_a
    factor = np.asarray([1.0, -1.0, 1.0, -1.0], dtype=np.float64)
    proxy_noise = np.asarray([-1.0, -1.0, 1.0, 1.0], dtype=np.float64)
    design_a = build_smooth_date_design(
        date_index=0,
        factor=factor,
        proxy_noise=proxy_noise,
        oracle_flow=q_a,
        level_flows=_repeated_levels(q_a),
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    design_b = build_smooth_date_design(
        date_index=0,
        factor=factor,
        proxy_noise=proxy_noise,
        oracle_flow=q_b,
        level_flows=_repeated_levels(q_b),
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )

    with pytest.raises(ValueError, match="design|provenance"):
        aggregate_smooth_moments(
            stack_base_moments((design_a,)),
            stack_cell_moments((build_cell_date_moments(design_b, q_b),)),
            np.ones(1, dtype=np.float64),
        )


def test_contract_builder_rejects_forged_transformed_date() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=3,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    forged_provenance = replace(
        date.filtered.provenance,
        phase_id=999,
        scenario_id=999,
    )
    forged = replace(
        date,
        filtered=replace(
            date.filtered,
            provenance=forged_provenance,
            provenance_token="forged",
        ),
    )

    with pytest.raises(ValueError, match="receipt|provenance|issued"):
        build_contract_smooth_date_design(forged, contract=contract)


def test_contract_builder_rejects_mutated_transformed_content() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=3,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    date.q.setflags(write=True)
    date.q[0, 0] = np.nextafter(date.q[0, 0], math.inf)
    date.q.setflags(write=False)

    with pytest.raises(ValueError, match="content|receipt"):
        build_contract_smooth_date_design(date, contract=contract)


def test_contract_builder_rejects_response_map_relabeling() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=3,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    relabeled = replace(
        date,
        response_map=replace(date.response_map, target_index=0),
    )

    with pytest.raises(ValueError, match="receipt|response-map|issued"):
        build_contract_smooth_date_design(relabeled, contract=contract)


def test_contract_cell_builder_rejects_replaced_design_x0() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=4,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    design = build_contract_smooth_date_design(date, contract=contract)
    altered_x0 = np.array(design.x0, dtype=np.float64, order="C", copy=True)
    altered_x0[:, 3] += 1_000.0
    altered_x0.setflags(write=False)
    forged = replace(design, x0=altered_x0)

    with pytest.raises(ValueError, match="design|issued|receipt"):
        build_contract_cell_date_moments(forged, date, contract=contract)


def test_contract_cell_builder_rejects_ndarray_subclass_dispatch() -> None:
    class HostileArray(np.ndarray):
        pass

    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=4,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    design = build_contract_smooth_date_design(date, contract=contract)
    hostile_x0 = design.x0.view(HostileArray)
    hostile_x0.setflags(write=False)
    object.__setattr__(design, "x0", hostile_x0)

    with pytest.raises(ValueError, match="array|design|issued"):
        build_contract_cell_date_moments(design, date, contract=contract)


def test_private_design_kernel_cannot_mint_contract_authority_from_copied_receipt() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=0,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    issued = build_contract_smooth_date_design(date, contract=contract)
    assert issued.source_receipt is not None
    forged_receipt = replace(
        issued.source_receipt,
        provenance=replace(
            issued.source_receipt.provenance,
            n_dates=1,
            date_index=0,
        ),
    )
    forged = smooth_module._build_smooth_date_design(
        date_index=0,
        factor=date.filtered.factor,
        proxy_noise=date.filtered.proxy_noise,
        oracle_flow=date.q,
        level_flows=date.x,
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
        source_receipt=forged_receipt,
    )

    with pytest.raises(ValueError, match="issued|contract"):
        stack_contract_base_moments((forged,))


def test_smooth_contract_design_requires_canonical_reliability_anchor() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=0,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=1.0,
    )

    with pytest.raises(ValueError, match="canonical reliability anchor"):
        build_contract_smooth_date_design(date, contract=contract)


def test_callable_generic_issuance_registrar_is_absent() -> None:
    assert not hasattr(smooth_module, "_register_issued")


def test_contract_moments_preserve_response_identity_and_reject_other_base() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=4,
    )
    low_date = transform_date(
        base,
        build_cell(contract, target_index=0),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    high_date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    design = build_contract_smooth_date_design(low_date, contract=contract)
    high_design = build_contract_smooth_date_design(high_date, contract=contract)

    assert design.source_receipt is not None
    assert high_design.source_receipt is not None
    assert design.source_receipt.base_identity == high_design.source_receipt.base_identity
    assert design.source_receipt.response_map != high_design.source_receipt.response_map
    np.testing.assert_array_equal(design.x0, high_design.x0)
    np.testing.assert_array_equal(
        design.base_moments.x0tx0_upper,
        high_design.base_moments.x0tx0_upper,
    )
    assert design.design_sha256 == high_design.design_sha256
    assert smooth_module._design_token(design) != smooth_module._design_token(high_design)
    analytic_design = build_smooth_date_design(
        date_index=low_date.filtered.provenance.date_index,
        factor=low_date.filtered.factor,
        proxy_noise=low_date.filtered.proxy_noise,
        oracle_flow=low_date.q,
        level_flows=low_date.x,
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    np.testing.assert_array_equal(design.x0, analytic_design.x0)
    assert design.design_sha256 != analytic_design.design_sha256

    high_moments = build_contract_cell_date_moments(
        design,
        high_date,
        contract=contract,
    )

    assert high_moments.response_receipt is not None
    assert high_moments.design_receipt is not None
    assert high_moments.design_receipt.base_identity == high_moments.response_receipt.base_identity
    assert high_moments.design_receipt.response_map.target_index == 0
    assert high_moments.response_receipt.response_map.target_index == 16

    other_base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=5,
    )
    other_date = transform_date(
        other_base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    with pytest.raises(ValueError, match="base provenance"):
        build_contract_cell_date_moments(design, other_date, contract=contract)


def test_contract_panel_rejects_incomplete_declared_date_range() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    cell = build_cell(contract, target_index=16)
    designs = []
    for date_index in (0, 1):
        base = namespace.draw_base_normals(
            stream=G2Stream.VALIDATION_SIZE,
            n_dates=252,
            panel_index=1,
            date_index=date_index,
        )
        date = transform_date(
            base,
            cell,
            contract=contract,
            phi=contract.confirmatory_ar1,
            reliability=contract.confirmatory_reliability,
        )
        designs.append(build_contract_smooth_date_design(date, contract=contract))

    with pytest.raises(ValueError, match="omitted"):
        stack_contract_base_moments(designs)


def test_issued_base_moment_rejects_writable_state_mutation() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=2,
        date_index=0,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    design = build_contract_smooth_date_design(date, contract=contract)
    design.base_moments.x0tx0_upper.setflags(write=True)

    with pytest.raises(ValueError, match="issued|contract"):
        stack_contract_base_moments((design.base_moments,))


def test_contract_base_moment_issuance_releases_dead_design() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=2,
        date_index=0,
    )
    date = transform_date(
        base,
        build_cell(contract, target_index=16),
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    design = build_contract_smooth_date_design(date, contract=contract)
    key = id(design.base_moments)
    reference = weakref.ref(design.base_moments)

    assert smooth_module._CONTRACT_BASE_DATE_REGISTRY[key][0]() is design.base_moments
    del design
    gc.collect()

    assert reference() is None
    assert key not in smooth_module._CONTRACT_BASE_DATE_REGISTRY


def test_complete_issued_frontier_path_fits_all_smooth_estimators() -> None:
    class HostileMass(float):
        def __rtruediv__(self, other: object) -> float:
            return 999.0

    class SwitchingCellSequence:
        def __init__(
            self,
            issued: list[smooth_module.SmoothCellDateMoments],
            substitutes: tuple[smooth_module.SmoothCellDateMoments, ...],
        ) -> None:
            self._issued = issued
            self._substitutes = substitutes
            self.traversals = 0

        def __len__(self) -> int:
            return len(self._issued)

        def __getitem__(self, index: int) -> smooth_module.SmoothCellDateMoments:
            if index >= len(self._issued):
                raise IndexError(index)
            if index == 0:
                self.traversals += 1
            values = self._issued if self.traversals <= 2 else self._substitutes
            return values[index]

    class SwitchingBaseSequence:
        def __init__(
            self,
            issued: list[smooth_module.SmoothBaseDateMoments],
            substitutes: tuple[smooth_module.SmoothBaseDateMoments, ...],
        ) -> None:
            self._issued = issued
            self._substitutes = substitutes
            self.traversals = 0

        def __len__(self) -> int:
            return len(self._issued)

        def __getitem__(self, index: int) -> smooth_module.SmoothBaseDateMoments:
            if index >= len(self._issued):
                raise IndexError(index)
            if index == 0:
                self.traversals += 1
            values = self._issued if self.traversals == 1 else self._substitutes
            return values[index]

    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    cell = build_cell(contract, target_index=16)
    base_moments = []
    cell_moments = []
    mixed_cell_moments = []
    for date_index in range(48):
        base = namespace.draw_base_normals(
            stream=G2Stream.VALIDATION_DATE_FRONTIER,
            n_dates=48,
            panel_index=0,
            date_index=date_index,
        )
        date = transform_date(
            base,
            cell,
            contract=contract,
            phi=contract.confirmatory_ar1,
            reliability=contract.confirmatory_reliability,
        )
        design = build_contract_smooth_date_design(date, contract=contract)
        response_moments = build_contract_cell_date_moments(
            design,
            date,
            contract=contract,
        )
        base_moments.append(design.base_moments)
        cell_moments.append(response_moments)
        mixed_cell_moments.append(response_moments)
        if date_index == 47:
            other_date = transform_date(
                base,
                build_cell(contract, target_index=0),
                contract=contract,
                phi=contract.confirmatory_ar1,
                reliability=contract.confirmatory_reliability,
            )
            mixed_cell_moments[-1] = build_contract_cell_date_moments(
                design,
                other_date,
                contract=contract,
            )

    with pytest.raises(ValueError, match="omitted"):
        stack_contract_cell_moments(cell_moments[:-1])
    missing_middle = cell_moments[:23] + cell_moments[24:] + [cell_moments[-1]]
    with pytest.raises(ValueError, match="complete ordered panel|provenance"):
        stack_contract_cell_moments(missing_middle)
    with pytest.raises(ValueError, match="response-map"):
        stack_contract_cell_moments(mixed_cell_moments)

    response_receipts = []
    for moment in cell_moments:
        assert moment.response_receipt is not None
        response_receipts.append(moment.response_receipt)
    mixed_panel_receipts = list(response_receipts)
    mixed_panel_receipts[-1] = replace(
        mixed_panel_receipts[-1],
        provenance=replace(
            mixed_panel_receipts[-1].provenance,
            panel_index=1,
        ),
    )
    with pytest.raises(ValueError, match="complete ordered panel|provenance"):
        smooth_module._validate_complete_contract_receipts(
            mixed_panel_receipts,
            require_common_response_map=True,
        )

    mixed_stream_receipts = list(response_receipts)
    mixed_stream_receipts[-1] = replace(
        mixed_stream_receipts[-1],
        provenance=replace(
            mixed_stream_receipts[-1].provenance,
            stream=G2Stream.VALIDATION_SIZE,
        ),
    )
    with pytest.raises(ValueError, match="complete ordered panel|provenance"):
        smooth_module._validate_complete_contract_receipts(
            mixed_stream_receipts,
            require_common_response_map=True,
        )

    original_cell_cross = cell_moments[0].x0ty
    changed_cell_cross = np.array(original_cell_cross, copy=True)
    changed_cell_cross[0, 0] = math.nextafter(changed_cell_cross[0, 0], math.inf)
    changed_cell_cross.setflags(write=False)
    object.__setattr__(cell_moments[0], "x0ty", changed_cell_cross)
    with pytest.raises(ValueError, match="not issued|content changed"):
        stack_contract_cell_moments(cell_moments)
    object.__setattr__(cell_moments[0], "x0ty", original_cell_cross)

    substituted_base_moments = []
    for base_moment in base_moments:
        zero_gram = np.zeros_like(base_moment.x0tx0_upper)
        zero_gram.setflags(write=False)
        substituted_base_moments.append(replace(base_moment, x0tx0_upper=zero_gram))
    switching_bases = SwitchingBaseSequence(
        base_moments,
        tuple(substituted_base_moments),
    )
    base_panel = stack_contract_base_moments(
        cast(
            Sequence[smooth_module.SmoothDateDesign | smooth_module.SmoothBaseDateMoments],
            switching_bases,
        )
    )
    np.testing.assert_array_equal(
        base_panel.x0tx0_upper,
        np.stack([base_moment.x0tx0_upper for base_moment in base_moments], axis=0),
    )
    assert switching_bases.traversals == 1

    substituted_cell_moments = []
    for moment in cell_moments:
        zero_cross = np.zeros_like(moment.x0ty)
        zero_cross.setflags(write=False)
        substituted_cell_moments.append(replace(moment, x0ty=zero_cross))
    switching_cells = SwitchingCellSequence(
        cell_moments,
        tuple(substituted_cell_moments),
    )
    snapshot_panel = stack_contract_cell_moments(
        cast(Sequence[smooth_module.SmoothCellDateMoments], switching_cells)
    )
    snapshot_aggregate = aggregate_contract_smooth_moments(
        base_panel,
        snapshot_panel,
        np.ones(48, dtype=np.float64),
    )
    np.testing.assert_array_equal(
        snapshot_panel.x0ty,
        np.stack([moment.x0ty for moment in cell_moments], axis=0),
    )
    assert switching_cells.traversals == 1
    del snapshot_aggregate
    del snapshot_panel

    cell_panel = stack_contract_cell_moments(cell_moments)

    original_base_panel_gram = base_panel.x0tx0_upper
    changed_base_panel_gram = np.array(original_base_panel_gram, copy=True)
    changed_base_panel_gram[0, 0] = math.nextafter(changed_base_panel_gram[0, 0], math.inf)
    changed_base_panel_gram.setflags(write=False)
    object.__setattr__(base_panel, "x0tx0_upper", changed_base_panel_gram)
    with pytest.raises(ValueError, match="not issued|content changed"):
        aggregate_contract_smooth_moments(
            base_panel,
            cell_panel,
            np.ones(48, dtype=np.float64),
        )
    object.__setattr__(base_panel, "x0tx0_upper", original_base_panel_gram)

    original_cell_panel_cross = cell_panel.x0ty
    changed_cell_panel_cross = np.array(original_cell_panel_cross, copy=True)
    changed_cell_panel_cross[0, 0, 0] = math.nextafter(
        changed_cell_panel_cross[0, 0, 0],
        math.inf,
    )
    changed_cell_panel_cross.setflags(write=False)
    object.__setattr__(cell_panel, "x0ty", changed_cell_panel_cross)
    with pytest.raises(ValueError, match="not issued|content changed"):
        aggregate_contract_smooth_moments(
            base_panel,
            cell_panel,
            np.ones(48, dtype=np.float64),
        )
    object.__setattr__(cell_panel, "x0ty", original_cell_panel_cross)

    aggregate = aggregate_contract_smooth_moments(
        base_panel,
        cell_panel,
        np.ones(48, dtype=np.float64),
    )
    response_receipt = cell_moments[0].response_receipt
    assert response_receipt is not None
    anchor_map = response_receipt.response_map
    alternate_reliability_map = replace(anchor_map, reliability=1.0)

    oracle = fit_condition_ridge(
        aggregate,
        flow_view=G2FlowView.ORACLE,
        reliability=contract.confirmatory_reliability,
        expected_response_map=anchor_map,
        contract=contract,
    )
    observable = fit_condition_ridge(
        aggregate,
        flow_view=G2FlowView.OBSERVABLE,
        reliability=1.0,
        expected_response_map=alternate_reliability_map,
        contract=contract,
    )
    homogeneous = fit_homogeneous_ols(
        aggregate,
        reliability=contract.confirmatory_reliability,
        expected_response_map=anchor_map,
        contract=contract,
    )

    assert (
        validate_aggregate_response_map(
            aggregate,
            expected=alternate_reliability_map,
            reliability=1.0,
        )
        == anchor_map
    )
    with pytest.raises(ValueError, match="structural response map"):
        validate_aggregate_response_map(
            aggregate,
            expected=replace(alternate_reliability_map, target_index=0),
            reliability=1.0,
        )
    with pytest.raises(ValueError, match="fit reliability"):
        validate_aggregate_response_map(
            aggregate,
            expected=alternate_reliability_map,
            reliability=contract.confirmatory_reliability,
        )

    structural_relabels = (
        replace(anchor_map, target_index=0),
        replace(anchor_map, paper_recovery=not anchor_map.paper_recovery),
        replace(anchor_map, phi=math.nextafter(anchor_map.phi, math.inf)),
    )
    for relabeled_map in structural_relabels:
        with pytest.raises(ValueError, match="structural response map"):
            fit_condition_ridge(
                aggregate,
                flow_view=G2FlowView.ORACLE,
                reliability=contract.confirmatory_reliability,
                expected_response_map=relabeled_map,
                contract=contract,
            )
        with pytest.raises(ValueError, match="structural response map"):
            fit_homogeneous_ols(
                aggregate,
                reliability=contract.confirmatory_reliability,
                expected_response_map=relabeled_map,
                contract=contract,
            )

    for field, wrong_value in (
        ("n_rows", aggregate.n_rows + 1),
        ("n_assets", aggregate.n_assets + 1),
        ("n_levels", aggregate.n_levels + 1),
    ):
        original_value = getattr(aggregate, field)
        object.__setattr__(aggregate, field, wrong_value)
        with pytest.raises(
            ValueError,
            match="not issued|content changed|sealed G2 design",
        ):
            fit_condition_ridge(
                aggregate,
                flow_view=G2FlowView.ORACLE,
                reliability=contract.confirmatory_reliability,
                expected_response_map=anchor_map,
                contract=contract,
            )
        with pytest.raises(
            ValueError,
            match="not issued|content changed|sealed G2 design",
        ):
            fit_homogeneous_ols(
                aggregate,
                reliability=contract.confirmatory_reliability,
                expected_response_map=anchor_map,
                contract=contract,
            )
        object.__setattr__(aggregate, field, original_value)

    assert oracle.coefficients.shape == (30, 30)
    assert observable.coefficients.shape == (30, 30)
    assert homogeneous.slopes.shape == (3,)
    assert np.all(np.isfinite(oracle.coefficients))
    assert np.all(np.isfinite(observable.coefficients))
    assert np.all(np.isfinite(homogeneous.slopes))

    original_mass = aggregate.row_mass
    object.__setattr__(aggregate, "row_mass", HostileMass(original_mass))
    with pytest.raises((TypeError, ValueError), match="row_mass|schema|float"):
        smooth_module._aggregate_token(aggregate)
    object.__setattr__(aggregate, "row_mass", original_mass)

    fake_response_receipts = tuple(
        SimpleNamespace(
            provenance=receipt.provenance,
            base_identity=receipt.base_identity,
            response_map=receipt.response_map,
            date_content_sha256=receipt.date_content_sha256,
        )
        for receipt in aggregate.response_receipts
        if receipt is not None
    )
    object.__setattr__(aggregate, "response_receipts", fake_response_receipts)
    with pytest.raises((TypeError, ValueError), match="receipt|provenance"):
        fit_condition_ridge(
            aggregate,
            flow_view=G2FlowView.ORACLE,
            reliability=contract.confirmatory_reliability,
            expected_response_map=anchor_map,
            contract=contract,
        )
    object.__setattr__(aggregate, "response_receipts", tuple(response_receipts))

    cell_moment_key = id(cell_moments[0])
    cell_moment_reference = weakref.ref(cell_moments[0])
    base_panel_key = id(base_panel)
    base_panel_reference = weakref.ref(base_panel)
    cell_panel_key = id(cell_panel)
    cell_panel_reference = weakref.ref(cell_panel)
    aggregate_key = id(aggregate)
    aggregate_reference = weakref.ref(aggregate)

    del cell_moments
    del mixed_cell_moments
    del missing_middle
    del switching_cells
    del substituted_cell_moments
    del switching_bases
    del substituted_base_moments
    del base_panel
    del cell_panel
    del aggregate
    gc.collect()

    assert cell_moment_reference() is None
    assert cell_moment_key not in smooth_module._CONTRACT_CELL_DATE_REGISTRY
    assert base_panel_reference() is None
    assert base_panel_key not in smooth_module._CONTRACT_BASE_PANEL_REGISTRY
    assert cell_panel_reference() is None
    assert cell_panel_key not in smooth_module._CONTRACT_CELL_PANEL_REGISTRY
    assert aggregate_reference() is None
    assert aggregate_key not in smooth_module._CONTRACT_AGGREGATE_REGISTRY


def test_panel_order_and_bootstrap_weight_contract_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_panel, cell_panel, _ = _ridge_fixture_panels()
    contract = load_g2_contract(_root())
    q = np.asarray([[1.0, 2.0], [2.0, 1.0]], dtype=np.float64)
    earlier = build_smooth_date_design(
        date_index=0,
        factor=np.asarray([1.0, -1.0], dtype=np.float64),
        proxy_noise=np.zeros(2, dtype=np.float64),
        oracle_flow=q,
        level_flows=_repeated_levels(q),
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    later = build_smooth_date_design(
        date_index=1,
        factor=np.asarray([1.0, -1.0], dtype=np.float64),
        proxy_noise=np.zeros(2, dtype=np.float64),
        oracle_flow=q,
        level_flows=_repeated_levels(q),
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    with pytest.raises(ValueError, match="ascending"):
        stack_base_moments((later, earlier))

    bad_weights: tuple[np.ndarray, ...] = (
        np.asarray([1.0, -0.0], dtype=np.float64),
        np.asarray([0.5, 1.5], dtype=np.float64),
        np.asarray([1.0, 0.0], dtype=np.float64),
        np.asarray([1.0, np.nan], dtype=np.float64),
        np.asarray([1, 1], dtype=np.int64),
    )
    for bad in bad_weights:
        with pytest.raises((TypeError, ValueError)):
            aggregate_smooth_moments(base_panel, cell_panel, bad)

    matmul_calls: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    original_matmul = np.matmul

    def recording_matmul(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        matmul_calls.append((left.shape, right.shape))
        return cast(np.ndarray, original_matmul(left, right))

    monkeypatch.setattr("xid.models.g2_smooth.np.matmul", recording_matmul)
    weighted = aggregate_smooth_moments(
        base_panel,
        cell_panel,
        np.asarray([0.0, 2.0], dtype=np.float64),
    )
    assert matmul_calls == [
        ((2,), base_panel.x0tx0_upper.shape),
        ((2,), (2, cell_panel.x0_width * cell_panel.n_assets)),
        ((2,), cell_panel.yty_upper.shape),
    ]
    np.testing.assert_allclose(
        weighted.x0tx0,
        2.0
        * unpack_symmetric_upper(
            base_panel.x0tx0_upper[1],
            size=base_panel.x0_width,
        ),
        rtol=0.0,
        atol=0.0,
    )
    np.testing.assert_allclose(weighted.x0ty, 2.0 * cell_panel.x0ty[1], rtol=0.0, atol=0.0)
    np.testing.assert_allclose(
        weighted.yty,
        2.0
        * unpack_symmetric_upper(
            cell_panel.yty_upper[1],
            size=cell_panel.n_assets,
        ),
        rtol=0.0,
        atol=0.0,
    )
    assert base_panel.x0tx0_upper.flags.c_contiguous
    assert cell_panel.x0ty.flags.c_contiguous
    assert cell_panel.yty_upper.flags.c_contiguous
    assert not base_panel.x0tx0_upper.flags.writeable
    assert not cell_panel.x0ty.flags.writeable
    assert not cell_panel.yty_upper.flags.writeable


def test_condition_ridge_rejects_constant_proxy_after_global_centering() -> None:
    contract = load_g2_contract(_root())
    q = np.asarray([[-3.0, -1.0], [-1.0, 2.0], [1.0, -2.0], [3.0, 1.0]])
    design = build_smooth_date_design(
        date_index=0,
        factor=np.zeros(4, dtype=np.float64),
        proxy_noise=np.zeros(4, dtype=np.float64),
        oracle_flow=q,
        level_flows=_repeated_levels(q),
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    aggregate = aggregate_smooth_moments(
        stack_base_moments((design,)),
        stack_cell_moments((build_cell_date_moments(design, q),)),
        np.ones(1, dtype=np.float64),
    )

    with pytest.raises(ValueError, match="proxy variance"):
        _fit_analytic_ridge(
            aggregate,
            flow_view=G2FlowView.ORACLE,
            reliability=1.0,
        )


def test_condition_ridge_condition_branch_and_positive_floor() -> None:
    contract = load_g2_contract(_root())
    asymmetric = np.asarray([[1.0, 1e-8], [-1e-8, 20_000.0]], dtype=np.float64)

    result = solve_condition_ridge(asymmetric, np.eye(2, dtype=np.float64), contract=contract)

    assert result.penalty_condition == pytest.approx(1.000100010001, rel=0.0, abs=3e-15)
    assert result.penalty_floor == pytest.approx(0.0100005, rel=0.0, abs=3e-18)
    np.testing.assert_allclose(
        np.diag(result.coefficients),
        np.asarray([0.49997499874993756, 4.999749987499375e-05]),
        rtol=0.0,
        atol=2e-16,
    )
    assert result.post_condition_number <= contract.ridge_condition_cap * (
        1.0 + contract.ridge_post_condition_slack_multiplier * np.finfo(np.float64).eps
    )

    floor = solve_condition_ridge(
        np.diag(np.asarray([1.0, 10_000.0], dtype=np.float64)),
        np.eye(2, dtype=np.float64),
        contract=contract,
    )
    assert floor.penalty_condition == 0.0
    assert floor.penalty_floor == pytest.approx(0.0050005, rel=0.0, abs=2e-18)
    assert floor.penalty > 0.0


def test_condition_ridge_retains_closed_roundoff_boundary_and_fails_beyond_it() -> None:
    contract = load_g2_contract(_root())
    tolerance = contract.ridge_negative_eigen_roundoff_multiplier * np.finfo(np.float64).eps
    boundary = np.diag(np.asarray([-tolerance, 1.0], dtype=np.float64))

    accepted = solve_condition_ridge(boundary, np.eye(2, dtype=np.float64), contract=contract)

    assert accepted.smallest_eigenvalue == -tolerance
    with pytest.raises(ValueError, match="negative"):
        solve_condition_ridge(
            np.diag(np.asarray([np.nextafter(-tolerance, -np.inf), 1.0], dtype=np.float64)),
            np.eye(2, dtype=np.float64),
            contract=contract,
        )
    with pytest.raises(ValueError, match="largest"):
        solve_condition_ridge(
            np.zeros((2, 2), dtype=np.float64),
            np.eye(2, dtype=np.float64),
            contract=contract,
        )
    nonfinite = np.eye(2, dtype=np.float64)
    nonfinite[0, 0] = np.nan
    with pytest.raises(ValueError, match="nonfinite"):
        solve_condition_ridge(nonfinite, np.eye(2, dtype=np.float64), contract=contract)


def test_pooled_homogeneous_matches_explicit_stack_and_recovers_offdiagonal() -> None:
    contract = load_g2_contract(_root())
    q = np.asarray([[1, 2, 4], [2, 0, 1], [-1, 3, 2]], dtype=np.float64)
    z = np.asarray([0.0, 1.0, -1.0], dtype=np.float64)
    r = np.asarray([[-11, -6, 4], [10, 0, 5], [-16, 4, -1]], dtype=np.float64)
    design = build_smooth_date_design(
        date_index=0,
        factor=z,
        proxy_noise=np.zeros(3, dtype=np.float64),
        oracle_flow=q,
        level_flows=_repeated_levels(q),
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    aggregate = aggregate_smooth_moments(
        stack_base_moments((design,)),
        stack_cell_moments((build_cell_date_moments(design, r),)),
        np.ones(1, dtype=np.float64),
    )

    result = _fit_analytic_homogeneous(aggregate, reliability=1.0)

    np.testing.assert_allclose(result.slopes, np.asarray([2.0, -3.0, 4.0]), rtol=0.0, atol=2e-14)
    assert result.intercept == pytest.approx(5.0, rel=0.0, abs=2e-14)
    assert result.offdiagonal == pytest.approx(-3.0, rel=0.0, abs=2e-14)

    explicit_rows = []
    explicit_y = []
    for row in range(q.shape[0]):
        total = float(np.sum(q[row]))
        for asset in range(q.shape[1]):
            explicit_rows.append((1.0, q[row, asset], total - q[row, asset], z[row]))
            explicit_y.append(r[row, asset])
    explicit_beta = np.linalg.solve(
        np.asarray(explicit_rows).T @ np.asarray(explicit_rows),
        np.asarray(explicit_rows).T @ np.asarray(explicit_y),
    )
    np.testing.assert_allclose(
        np.concatenate(([result.intercept], result.slopes)),
        explicit_beta,
        rtol=0.0,
        atol=2e-14,
    )


def test_pooled_solver_rank_and_condition_boundaries_are_strict() -> None:
    contract = load_g2_contract(_root())
    response = np.ones(3, dtype=np.float64)
    means = np.zeros(3, dtype=np.float64)

    accepted = solve_pooled_homogeneous(
        np.diag(np.asarray([1.0, 1.0, 1e-12], dtype=np.float64)),
        response,
        predictor_means=means,
        response_mean=0.0,
        contract=contract,
    )
    assert accepted.condition_number == pytest.approx(1e12, rel=0.0, abs=1e-3)

    with pytest.raises(ValueError, match="condition"):
        solve_pooled_homogeneous(
            np.diag(np.asarray([1.0, 1.0, np.nextafter(1e-12, 0.0)], dtype=np.float64)),
            response,
            predictor_means=means,
            response_mean=0.0,
            contract=contract,
        )
    with pytest.raises(ValueError, match="rank"):
        solve_pooled_homogeneous(
            np.diag(np.asarray([1.0, 1.0, 0.0], dtype=np.float64)),
            response,
            predictor_means=means,
            response_mean=0.0,
            contract=contract,
        )


def test_test_seed_single_date_smoke_exercises_all_three_estimators_without_target_claim() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=0,
    )
    cell = build_cell(contract, target_index=16)
    date = transform_date(
        base,
        cell,
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )
    contract_design = build_contract_smooth_date_design(date, contract=contract)
    contract_cell = build_contract_cell_date_moments(
        contract_design,
        date,
        contract=contract,
    )
    assert contract_design.source_receipt is not None
    assert contract_cell.response_receipt is not None
    assert contract_cell.response_receipt.response_map.target_index == 16

    design = build_smooth_date_design(
        date_index=0,
        factor=date.filtered.factor,
        proxy_noise=date.filtered.proxy_noise,
        oracle_flow=date.q,
        level_flows=date.x,
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
    )
    aggregate = aggregate_smooth_moments(
        stack_base_moments((design,)),
        stack_cell_moments((build_cell_date_moments(design, date.r),)),
        np.ones(1, dtype=np.float64),
    )
    copied_receipt_forgery = replace(
        aggregate,
        source_receipts=(contract_design.source_receipt,),
        response_receipts=(contract_cell.response_receipt,),
        design_sha256s=(contract_design.design_sha256,),
    )

    oracle = _fit_analytic_ridge(
        aggregate,
        flow_view=G2FlowView.ORACLE,
        reliability=contract.confirmatory_reliability,
    )
    observable = _fit_analytic_ridge(
        aggregate,
        flow_view=G2FlowView.OBSERVABLE,
        reliability=contract.confirmatory_reliability,
    )
    homogeneous = _fit_analytic_homogeneous(
        aggregate,
        reliability=contract.confirmatory_reliability,
    )

    with pytest.raises(ValueError, match="issued|contract"):
        fit_condition_ridge(
            aggregate,
            flow_view=G2FlowView.ORACLE,
            reliability=contract.confirmatory_reliability,
            expected_response_map=contract_cell.response_receipt.response_map,
            contract=contract,
        )
    with pytest.raises(ValueError, match="issued|contract"):
        fit_homogeneous_ols(
            aggregate,
            reliability=contract.confirmatory_reliability,
            expected_response_map=contract_cell.response_receipt.response_map,
            contract=contract,
        )
    with pytest.raises(ValueError, match="issued|contract"):
        fit_condition_ridge(
            copied_receipt_forgery,
            flow_view=G2FlowView.OBSERVABLE,
            reliability=contract.confirmatory_reliability,
            expected_response_map=contract_cell.response_receipt.response_map,
            contract=contract,
        )

    assert oracle.coefficients.shape == (30, 30)
    assert observable.coefficients.shape == (30, 30)
    assert homogeneous.slopes.shape == (3,)
    assert np.all(np.isfinite(oracle.coefficients))
    assert np.all(np.isfinite(observable.coefficients))
    assert np.all(np.isfinite(homogeneous.slopes))
