from __future__ import annotations

import gc
import weakref
from dataclasses import replace
from pathlib import Path
from typing import cast

import numpy as np
import pytest

import xid.sim.g2 as g2_module
from xid.sim.g2 import (
    G2Stream,
    RawBaseNormals,
    TestRngNamespace,
    build_cell,
    filter_ar1_date,
    homogeneous_lambda,
    load_g2_contract,
    symmetric_modal_map,
    transform_date,
)

_TEST_SEED = 1729


def _root() -> Path:
    return Path(__file__).parents[1]


def test_ar1_filter_uses_stationary_first_draw_and_scaled_innovations() -> None:
    raw = np.asarray([[1.0, -2.0], [3.0, 4.0], [-1.0, 0.5]], dtype=np.float64)

    filtered = filter_ar1_date(raw, phi=0.6)

    np.testing.assert_allclose(
        filtered,
        np.asarray([[1.0, -2.0], [3.0, 2.0], [1.0, 1.6]], dtype=np.float64),
        rtol=0.0,
        atol=5e-16,
    )


def test_ar1_phi_zero_is_byte_identity_and_each_date_resets() -> None:
    first = np.asarray([[1.0], [2.0], [3.0]], dtype=np.float64)
    second = np.asarray([[10.0], [20.0], [30.0]], dtype=np.float64)

    np.testing.assert_array_equal(filter_ar1_date(first, phi=0.0), first)
    np.testing.assert_array_equal(filter_ar1_date(second, phi=0.0), second)
    separately = np.concatenate(
        (filter_ar1_date(first, phi=0.6), filter_ar1_date(second, phi=0.6)),
        axis=0,
    )
    incorrectly_crossed = filter_ar1_date(np.concatenate((first, second), axis=0), phi=0.6)
    assert separately[3, 0] == 10.0
    assert incorrectly_crossed[3, 0] != 10.0


def test_symmetric_modal_map_preserves_both_eigenspaces() -> None:
    market = np.ones(3, dtype=np.float64) / np.sqrt(3.0)
    raw = np.asarray([[1.0, 2.0, 3.0], [-1.0, 0.0, 1.0]], dtype=np.float64)

    mapped = symmetric_modal_map(
        raw,
        market_variance=9.0,
        orthogonal_variance=4.0,
        market_vector=market,
    )

    np.testing.assert_allclose(
        mapped,
        np.asarray([[4.0, 6.0, 8.0], [-2.0, 0.0, 2.0]], dtype=np.float64),
        rtol=0.0,
        atol=2e-15,
    )
    np.testing.assert_allclose(mapped @ market, 3.0 * (raw @ market), rtol=0.0, atol=2e-15)
    raw_perp = raw - np.outer(raw @ market, market)
    mapped_perp = mapped - np.outer(mapped @ market, market)
    np.testing.assert_allclose(mapped_perp, 2.0 * raw_perp, rtol=0.0, atol=3e-15)


def test_homogeneous_lambda_has_registered_entries_and_modes() -> None:
    n_assets = 30
    diagonal = 0.29
    offdiagonal = 0.0046
    market = np.ones(n_assets, dtype=np.float64) / np.sqrt(float(n_assets))
    orthogonal = np.zeros(n_assets, dtype=np.float64)
    orthogonal[:2] = (1.0, -1.0)

    matrix = homogeneous_lambda(n_assets, diagonal, offdiagonal)

    np.testing.assert_array_equal(np.diag(matrix), np.full(n_assets, diagonal))
    np.testing.assert_allclose(
        matrix[~np.eye(n_assets, dtype=bool)],
        offdiagonal,
        rtol=0.0,
        atol=2e-18,
    )
    np.testing.assert_allclose(
        matrix @ market,
        (diagonal + (n_assets - 1) * offdiagonal) * market,
        rtol=0.0,
        atol=3e-16,
    )
    np.testing.assert_allclose(
        matrix @ orthogonal,
        (diagonal - offdiagonal) * orthogonal,
        rtol=0.0,
        atol=3e-16,
    )


def test_cell_parameters_reproduce_sealed_upper_endpoint_anchors() -> None:
    contract = load_g2_contract(_root())
    cell = build_cell(contract, target_index=16)

    assert cell.offdiagonal == 0.0046
    assert cell.q1 == 8.481
    assert cell.q0 == pytest.approx(0.7420344827586206, rel=0.0, abs=1e-15)
    assert cell.r1 == 9.6
    assert cell.r0 == pytest.approx(0.7034482758620689, rel=0.0, abs=1e-15)
    assert cell.gamma == pytest.approx(1.5395102172741495, rel=0.0, abs=5e-15)
    assert cell.market_return_shock_variance == pytest.approx(
        2.082896495599317,
        rel=0.0,
        abs=5e-15,
    )
    assert cell.orthogonal_return_shock_variance == pytest.approx(
        0.6430072224124138,
        rel=0.0,
        abs=5e-15,
    )
    assert cell.market_return_shock_variance > 0.0
    assert cell.orthogonal_return_shock_variance > 0.0
    assert not cell.market_vector.flags.writeable
    assert not cell.lambda_matrix.flags.writeable


def test_all_seventeen_cells_reproduce_independent_population_moment_oracles() -> None:
    contract = load_g2_contract(_root())
    identity = np.eye(contract.n_assets, dtype=np.float64)

    for target_index in range(17):
        cell = build_cell(contract, target_index=target_index)
        market = cell.market_vector
        market_projector = np.outer(market, market)
        flow_covariance = cell.q0 * identity + (cell.q1 - cell.q0) * market_projector
        return_noise_covariance = (
            cell.orthogonal_return_shock_variance * identity
            + (cell.market_return_shock_variance - cell.orthogonal_return_shock_variance)
            * market_projector
        )
        return_flow_covariance = (
            cell.lambda_matrix @ flow_covariance + cell.gamma * cell.hq * market_projector
        )
        return_covariance = (
            cell.lambda_matrix @ flow_covariance @ cell.lambda_matrix.T
            + cell.gamma**2 * market_projector
            + cell.gamma
            * cell.hq
            * (cell.lambda_matrix @ market_projector + market_projector @ cell.lambda_matrix.T)
            + return_noise_covariance
        )
        expected_return_covariance = cell.r0 * identity + (cell.r1 - cell.r0) * market_projector
        market_cross_covariance = float(market @ return_flow_covariance @ market)
        observed_alignment = market_cross_covariance / np.sqrt(cell.q1 * cell.r1)

        np.testing.assert_allclose(
            return_covariance,
            expected_return_covariance,
            rtol=0.0,
            atol=1e-14,
        )
        assert float(market @ flow_covariance @ market) == pytest.approx(
            cell.q1,
            rel=0.0,
            abs=3e-15,
        )
        assert float(np.trace(flow_covariance)) == pytest.approx(
            float(contract.n_assets),
            rel=0.0,
            abs=2e-14,
        )
        assert float(np.trace(return_covariance)) == pytest.approx(
            float(contract.n_assets),
            rel=0.0,
            abs=2e-13,
        )
        assert cell.q1 / float(contract.n_assets) == contract.flow_pc1_share
        assert cell.r1 / float(contract.n_assets) == contract.return_pc1_share
        assert observed_alignment == pytest.approx(
            contract.factor_alignment,
            rel=0.0,
            abs=2e-15,
        )
        assert 1.0 / (1.0 + (1.0 / contract.confirmatory_reliability - 1.0)) == pytest.approx(
            contract.confirmatory_reliability,
            rel=0.0,
            abs=2e-16,
        )
        assert (547.0 / 3953.0) / float(contract.n_levels) == pytest.approx(
            contract.level_average_error_variance,
            rel=0.0,
            abs=2e-18,
        )


def test_transform_date_satisfies_every_registered_structural_map() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, _TEST_SEED)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=4,
        date_index=3,
    )
    cell = build_cell(contract, target_index=16)

    generated = transform_date(
        base,
        cell,
        contract=contract,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )

    market = cell.market_vector
    expected_v = np.sqrt(cell.q0) * generated.filtered.flow_innovation
    expected_q = cell.hq * generated.filtered.factor[:, None] * market[None, :] + expected_v
    expected_u = symmetric_modal_map(
        generated.filtered.return_innovation,
        market_variance=cell.market_return_shock_variance,
        orthogonal_variance=cell.orthogonal_return_shock_variance,
        market_vector=market,
    )
    expected_r = (
        expected_q @ cell.lambda_matrix.T
        + cell.gamma * generated.filtered.factor[:, None] * market[None, :]
        + expected_u
    )
    expected_z = (
        generated.filtered.factor
        + np.sqrt(1.0 / contract.confirmatory_reliability - 1.0) * generated.filtered.proxy_noise
    )
    expected_x = expected_q[:, :, None] + np.sqrt(547.0 / 3953.0) * (generated.filtered.level_noise)

    for raw, filtered in (
        (base.factor, generated.filtered.factor),
        (base.flow_innovation, generated.filtered.flow_innovation),
        (base.return_innovation, generated.filtered.return_innovation),
        (base.level_noise, generated.filtered.level_noise),
        (base.proxy_noise, generated.filtered.proxy_noise),
    ):
        np.testing.assert_array_equal(
            filtered,
            filter_ar1_date(raw, phi=contract.confirmatory_ar1),
        )
    np.testing.assert_array_equal(generated.v, expected_v)
    np.testing.assert_array_equal(generated.q, expected_q)
    np.testing.assert_array_equal(generated.u, expected_u)
    np.testing.assert_array_equal(generated.r, expected_r)
    np.testing.assert_array_equal(generated.z, expected_z)
    np.testing.assert_array_equal(generated.x, expected_x)
    assert generated.q.shape == (330, 30)
    assert generated.r.shape == (330, 30)
    assert generated.z.shape == (330,)
    assert generated.x.shape == (330, 30, 10)
    for values in (generated.q, generated.r, generated.z, generated.x):
        assert values.dtype == np.float64
        assert values.flags.c_contiguous
        assert np.all(np.isfinite(values))


def test_common_random_numbers_change_only_declared_deterministic_maps() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, _TEST_SEED)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=8,
        date_index=2,
    )
    low_cell = build_cell(contract, target_index=0)
    high_cell = build_cell(contract, target_index=16)

    low = transform_date(base, low_cell, contract=contract, phi=0.6, reliability=0.95)
    high = transform_date(base, high_cell, contract=contract, phi=0.6, reliability=0.99)
    recovery_base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_PAPER_RECOVERY,
        n_dates=252,
        panel_index=0,
        date_index=2,
    )
    recovery = transform_date(
        recovery_base,
        high_cell,
        contract=contract,
        phi=0.6,
        reliability=0.99,
        paper_recovery=True,
    )

    np.testing.assert_array_equal(low.filtered.factor, high.filtered.factor)
    np.testing.assert_array_equal(low.q, high.q)
    np.testing.assert_array_equal(low.x, high.x)
    assert not np.array_equal(high.filtered.factor, recovery.filtered.factor)
    np.testing.assert_array_equal(
        recovery.r,
        recovery.q @ high_cell.lambda_matrix.T + recovery.u,
    )
    with pytest.raises(ValueError, match="paper-recovery RNG namespace"):
        transform_date(
            base,
            high_cell,
            contract=contract,
            phi=0.6,
            reliability=0.99,
            paper_recovery=True,
        )
    assert not np.array_equal(low.r, high.r)
    assert not np.array_equal(low.z, high.z)

    with pytest.raises(TypeError, match="RawBaseNormals"):
        transform_date(
            cast(RawBaseNormals, high.filtered),
            high_cell,
            contract=contract,
            phi=0.6,
            reliability=0.99,
        )
    with pytest.raises(ValueError, match="cell scalars"):
        transform_date(
            base,
            replace(high_cell, gamma=0.0),
            contract=contract,
            phi=0.6,
            reliability=0.99,
        )
    forged_lambda = np.eye(contract.n_assets, dtype=np.float64)
    forged_lambda.setflags(write=False)
    with pytest.raises(ValueError, match="lambda_matrix"):
        transform_date(
            base,
            replace(high_cell, lambda_matrix=forged_lambda),
            contract=contract,
            phi=0.6,
            reliability=0.99,
        )
    forged_provenance = replace(
        base.provenance,
        stream=G2Stream.VALIDATION_PAPER_RECOVERY,
        phase_id=25,
        scenario_id=4,
        panel_index=0,
    )
    with pytest.raises(ValueError, match="provenance"):
        transform_date(
            replace(base, provenance=forged_provenance),
            high_cell,
            contract=contract,
            phi=0.6,
            reliability=0.99,
            paper_recovery=True,
        )
    with pytest.raises(ValueError, match="not licensed"):
        transform_date(
            base,
            high_cell,
            contract=contract,
            phi=0.4,
            reliability=0.99,
        )


def test_raw_base_validation_rejects_rewrapped_or_mixed_components() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, _TEST_SEED)
    cell = build_cell(contract, target_index=16)
    power = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=0,
        date_index=0,
    )
    other_date = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=0,
        date_index=1,
    )
    generated = transform_date(
        power,
        cell,
        contract=contract,
        phi=0.6,
        reliability=0.95,
    )
    rewrapped_filtered = RawBaseNormals(
        provenance=power.provenance,
        provenance_token=power.provenance_token,
        factor=generated.filtered.factor,
        flow_innovation=generated.filtered.flow_innovation,
        return_innovation=generated.filtered.return_innovation,
        level_noise=generated.filtered.level_noise,
        proxy_noise=generated.filtered.proxy_noise,
    )

    with pytest.raises(ValueError):
        transform_date(
            rewrapped_filtered,
            cell,
            contract=contract,
            phi=0.6,
            reliability=0.95,
        )
    with pytest.raises(ValueError):
        transform_date(
            replace(power, factor=other_date.factor),
            cell,
            contract=contract,
            phi=0.6,
            reliability=0.95,
        )

    recovery = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_PAPER_RECOVERY,
        n_dates=252,
        panel_index=0,
        date_index=0,
    )
    research = namespace.draw_base_normals(
        stream=G2Stream.RESEARCH,
        n_dates=252,
        panel_index=0,
        date_index=0,
    )
    mixed_recovery = replace(
        recovery,
        factor=research.factor,
        flow_innovation=research.flow_innovation,
        return_innovation=research.return_innovation,
        level_noise=research.level_noise,
        proxy_noise=research.proxy_noise,
    )
    with pytest.raises(ValueError):
        transform_date(
            mixed_recovery,
            cell,
            contract=contract,
            phi=0.6,
            reliability=0.95,
            paper_recovery=True,
        )
    repackaged_recovery = g2_module._make_raw_base_normals(
        provenance=recovery.provenance,
        factor=research.factor,
        flow_innovation=research.flow_innovation,
        return_innovation=research.return_innovation,
        level_noise=research.level_noise,
        proxy_noise=research.proxy_noise,
    )
    with pytest.raises(ValueError, match="draw_base_normals"):
        transform_date(
            repackaged_recovery,
            cell,
            contract=contract,
            phi=0.6,
            reliability=0.95,
            paper_recovery=True,
        )

    tampered = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=0,
        date_index=2,
    )
    tampered.factor.setflags(write=True)
    tampered.factor[0] += 1.0
    tampered.factor.setflags(write=False)
    retokened = replace(
        tampered,
        provenance_token=g2_module._base_provenance_token(
            tampered.provenance,
            stage="raw",
            factor=tampered.factor,
            flow_innovation=tampered.flow_innovation,
            return_innovation=tampered.return_innovation,
            level_noise=tampered.level_noise,
            proxy_noise=tampered.proxy_noise,
        ),
    )
    with pytest.raises(ValueError, match="issuance"):
        transform_date(
            retokened,
            cell,
            contract=contract,
            phi=0.6,
            reliability=0.95,
        )


def test_raw_issuance_registry_releases_dead_base() -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=0,
        date_index=9,
    )
    key = id(base)
    reference = weakref.ref(base)

    assert g2_module._RAW_BASE_REGISTRY[key][0]() is base
    del base
    gc.collect()

    assert reference() is None
    assert key not in g2_module._RAW_BASE_REGISTRY


def test_iid_stream_requires_zero_phi_and_modal_helper_rejects_nonfinite() -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, _TEST_SEED)
    base = namespace.draw_base_normals(
        stream=G2Stream.VALIDATION_IID,
        n_dates=252,
        panel_index=0,
        date_index=0,
    )
    cell = build_cell(contract, target_index=16)

    generated = transform_date(
        base,
        cell,
        contract=contract,
        phi=0.0,
        reliability=0.95,
    )
    np.testing.assert_array_equal(generated.filtered.factor, base.factor)
    with pytest.raises(ValueError, match="not licensed"):
        transform_date(
            base,
            cell,
            contract=contract,
            phi=0.6,
            reliability=0.95,
        )
    nonfinite = np.ones((2, 3), dtype=np.float64)
    nonfinite[0, 0] = np.nan
    market = np.ones(3, dtype=np.float64) / np.sqrt(3.0)
    with pytest.raises(ValueError, match="finite"):
        symmetric_modal_map(
            nonfinite,
            market_variance=1.0,
            orthogonal_variance=1.0,
            market_vector=market,
        )
