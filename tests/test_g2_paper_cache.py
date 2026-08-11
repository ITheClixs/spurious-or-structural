from __future__ import annotations

import hashlib
import inspect
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from xid.models import g2_paper_cache as paper_cache
from xid.models.g2_paper_cache import PaperResearchDateCache
from xid.models.g2_resource import load_resource_config

ROOT = Path(__file__).parents[1]
ORDER_MANIFEST_SHA256 = "8810471ce6c0747af7cdda48299989303cd85a9c7def7c681f2a57f93348a083"


def test_research_paper_cache_index_map_matches_hand_derived_sentinels() -> None:
    contract = load_resource_config(ROOT)
    matrix = paper_cache.PaperCacheMatrixField
    loss = paper_cache.PaperCacheLossField

    expected_matrix_indices = (
        ("PI_1_direct", 0, 0, 0),
        ("PI_1_direct", 29, 29, 899),
        ("PI_I_direct", 0, 0, 900),
        ("CI_1_direct", 29, 29, 2_699),
        ("CI_I_direct", 0, 0, 2_700),
        ("CI_I_direct", 7, 19, 2_929),
        ("CI_I_direct", 29, 29, 3_599),
        ("CI_CC_full_response", 29, 29, 7_199),
        ("cc_mean_projection_p_perp", 0, 0, 7_200),
        ("cc_mean_projection_p_perp", 29, 29, 8_099),
    )
    for matrix_name, row, column, expected in expected_matrix_indices:
        matrix_field = matrix(matrix_name, row, column)
        assert paper_cache.research_paper_cache_index(matrix_field, contract=contract) == expected
        assert paper_cache.research_paper_cache_field(expected, contract=contract) == matrix_field

    expected_loss_indices = (
        ("PI_1", 0, "sse", 8_100),
        ("PI_1", 0, "sst", 8_101),
        ("CI_I", 7, "sse", 8_294),
        ("CI_I", 7, "sst", 8_295),
        ("CI_CC", 29, "sse", 8_458),
        ("CI_CC", 29, "sst", 8_459),
    )
    for specification, response, kind, expected in expected_loss_indices:
        loss_field = loss(specification, response, kind)
        assert paper_cache.research_paper_cache_index(loss_field, contract=contract) == expected
        assert paper_cache.research_paper_cache_field(expected, contract=contract) == loss_field


def test_recovery_map_is_compact_ci_i_projection_not_a_research_prefix() -> None:
    contract = load_resource_config(ROOT)
    matrix = paper_cache.PaperCacheMatrixField
    loss = paper_cache.PaperCacheLossField

    coefficient = matrix("CI_I_direct", 7, 19)
    sse = loss("CI_I", 7, "sse")
    sst = loss("CI_I", 7, "sst")

    assert paper_cache.recovery_paper_cache_index(coefficient, contract=contract) == 229
    assert paper_cache.research_paper_cache_index(coefficient, contract=contract) == 2_929
    assert paper_cache.recovery_paper_cache_index(sse, contract=contract) == 914
    assert paper_cache.recovery_paper_cache_index(sst, contract=contract) == 915
    assert paper_cache.research_paper_cache_index(sse, contract=contract) == 8_294
    assert paper_cache.research_paper_cache_index(sst, contract=contract) == 8_295

    assert paper_cache.recovery_paper_cache_field(0, contract=contract) == matrix(
        "CI_I_direct", 0, 0
    )
    assert paper_cache.recovery_paper_cache_field(899, contract=contract) == matrix(
        "CI_I_direct", 29, 29
    )
    assert paper_cache.recovery_paper_cache_field(900, contract=contract) == loss("CI_I", 0, "sse")
    assert paper_cache.recovery_paper_cache_field(959, contract=contract) == loss("CI_I", 29, "sst")


def test_paper_cache_index_maps_are_bijective_over_the_sealed_field_counts() -> None:
    contract = load_resource_config(ROOT)

    research_fields = tuple(
        paper_cache.research_paper_cache_field(index, contract=contract) for index in range(8_460)
    )
    recovery_fields = tuple(
        paper_cache.recovery_paper_cache_field(index, contract=contract) for index in range(960)
    )

    assert len(research_fields) == len(set(research_fields)) == 8_460
    assert len(recovery_fields) == len(set(recovery_fields)) == 960
    assert tuple(
        paper_cache.research_paper_cache_index(field, contract=contract)
        for field in research_fields
    ) == tuple(range(8_460))
    assert tuple(
        paper_cache.recovery_paper_cache_index(field, contract=contract)
        for field in recovery_fields
    ) == tuple(range(960))


def test_paper_cache_index_maps_reject_type_range_variant_and_contract_drift() -> None:
    contract = load_resource_config(ROOT)
    matrix = paper_cache.PaperCacheMatrixField
    loss = paper_cache.PaperCacheLossField

    for bad_index in (-1, 8_460, True, 1.0):
        with pytest.raises((TypeError, ValueError), match="index|range"):
            paper_cache.research_paper_cache_field(bad_index, contract=contract)
    for bad_index in (-1, 960, False, 1.0):
        with pytest.raises((TypeError, ValueError), match="index|range"):
            paper_cache.recovery_paper_cache_field(bad_index, contract=contract)

    bad_fields = (
        matrix("CI_I_direct", True, 0),
        matrix("CI_I_direct", -1, 0),
        matrix("CI_I_direct", 0, 30),
        matrix("not_a_matrix", 0, 0),
        loss("CI_I", True, "sse"),
        loss("CI_I", 30, "sse"),
        loss("CI_I", 0, "mse"),
        loss("not_a_specification", 0, "sse"),
    )
    for field in bad_fields:
        with pytest.raises((TypeError, ValueError), match="field|index|matrix|loss|range"):
            paper_cache.research_paper_cache_index(field, contract=contract)

    with pytest.raises(ValueError, match="recovery|CI_I"):
        paper_cache.recovery_paper_cache_index(matrix("PI_1_direct", 0, 0), contract=contract)
    with pytest.raises(ValueError, match="recovery|CI_I"):
        paper_cache.recovery_paper_cache_index(loss("PI_1", 0, "sse"), contract=contract)
    with pytest.raises(TypeError, match="field"):
        paper_cache.research_paper_cache_index(("CI_I_direct", 0, 0), contract=contract)

    altered = replace(contract, authority="A022+A023+A024+A025+A026")
    with pytest.raises(ValueError, match="sealed|A027|contract"):
        paper_cache.research_paper_cache_field(0, contract=altered)


def test_order_manifest_bytes_are_canonical_and_match_the_independent_seal() -> None:
    contract = load_resource_config(ROOT)

    manifest = paper_cache.paper_cache_order_manifest_bytes(contract=contract)

    assert type(manifest) is bytes
    assert manifest.isascii()
    assert len(manifest) == 1_057
    assert manifest.endswith(b"\n")
    assert not manifest.endswith(b"\n\n")
    assert hashlib.sha256(manifest).hexdigest() == ORDER_MANIFEST_SHA256


def _research_payload() -> PaperResearchDateCache:
    matrices = []
    for matrix_index in range(9):
        matrix = np.empty((30, 30), dtype=np.float64, order="F")
        for row in range(30):
            for column in range(30):
                matrix[row, column] = 1_000_000 * matrix_index + 1_000 * row + column
        matrices.append(matrix)

    losses = np.empty((6, 30, 2), dtype=np.float64)
    for specification in range(6):
        for response in range(30):
            losses[specification, response, 0] = 10_000_000 + 10_000 * specification + 10 * response
            losses[specification, response, 1] = (
                20_000_000 + 10_000 * specification + 10 * response + 1
            )

    return paper_cache.PaperResearchDateCache(
        matrices[0],
        matrices[1],
        matrices[2],
        matrices[3],
        matrices[4],
        matrices[5],
        matrices[6],
        matrices[7],
        matrices[8],
        losses,
    )


def test_research_pack_uses_semantic_row_column_order_and_is_immutable() -> None:
    contract = load_resource_config(ROOT)
    payload = _research_payload()

    packed = paper_cache.pack_research_paper_cache(payload, contract=contract)

    assert type(packed) is np.ndarray
    assert packed.dtype == np.dtype(np.float64)
    assert packed.shape == (8_460,)
    assert packed.flags.c_contiguous
    assert packed.flags.owndata
    assert not packed.flags.writeable
    assert packed[0] == 0.0
    assert packed[29] == 29.0
    assert packed[30] == 1_000.0
    assert packed[899] == 29_029.0
    assert packed[900] == 1_000_000.0
    assert packed[2_929] == 3_007_019.0
    assert packed[7_199] == 7_029_029.0
    assert packed[7_200] == 8_000_000.0
    assert packed[8_099] == 8_029_029.0
    assert packed[8_100] == 10_000_000.0
    assert packed[8_101] == 20_000_001.0
    assert packed[8_294] == 10_030_070.0
    assert packed[8_295] == 20_030_071.0
    assert packed[8_459] == 20_050_291.0

    before = packed.copy()
    payload.pi_1_direct[0, 0] = -999.0
    payload.losses[0, 0, 0] = -999.0
    np.testing.assert_array_equal(packed, before)
    with pytest.raises(ValueError, match="read-only|assignment destination"):
        packed[0] = -1.0


def test_recovery_pack_is_compact_ci_i_and_not_the_research_prefix() -> None:
    contract = load_resource_config(ROOT)
    research_payload = _research_payload()
    recovery_payload = paper_cache.PaperRecoveryDateCache(
        research_payload.ci_i_direct.copy(order="C"),
        research_payload.losses[3].copy(order="C"),
    )

    research = paper_cache.pack_research_paper_cache(research_payload, contract=contract)
    recovery = paper_cache.pack_recovery_paper_cache(recovery_payload, contract=contract)

    assert recovery.shape == (960,)
    assert recovery.dtype == np.dtype(np.float64)
    assert recovery.flags.c_contiguous
    assert recovery.flags.owndata
    assert not recovery.flags.writeable
    assert recovery[0] == research[2_700] == 3_000_000.0
    assert recovery[229] == research[2_929] == 3_007_019.0
    assert recovery[899] == research[3_599] == 3_029_029.0
    assert recovery[900] == research[8_280] == 10_030_000.0
    assert recovery[914] == research[8_294] == 10_030_070.0
    assert recovery[915] == research[8_295] == 20_030_071.0
    assert recovery[959] == research[8_339] == 20_030_291.0
    assert not np.array_equal(recovery, research[:960])


def test_pack_unpack_round_trips_without_source_or_output_aliasing() -> None:
    contract = load_resource_config(ROOT)
    research_payload = _research_payload()
    recovery_payload = paper_cache.PaperRecoveryDateCache(
        research_payload.ci_i_direct.copy(),
        research_payload.losses[3].copy(),
    )

    research_vector = paper_cache.pack_research_paper_cache(research_payload, contract=contract)
    recovery_vector = paper_cache.pack_recovery_paper_cache(recovery_payload, contract=contract)
    unpacked_research = paper_cache.unpack_research_paper_cache(
        research_vector,
        contract=contract,
    )
    unpacked_recovery = paper_cache.unpack_recovery_paper_cache(
        recovery_vector,
        contract=contract,
    )

    repacked_research = paper_cache.pack_research_paper_cache(
        unpacked_research,
        contract=contract,
    )
    repacked_recovery = paper_cache.pack_recovery_paper_cache(
        unpacked_recovery,
        contract=contract,
    )
    np.testing.assert_array_equal(repacked_research, research_vector)
    np.testing.assert_array_equal(repacked_recovery, recovery_vector)

    research_arrays = (
        unpacked_research.pi_1_direct,
        unpacked_research.pi_i_direct,
        unpacked_research.ci_1_direct,
        unpacked_research.ci_i_direct,
        unpacked_research.pi_cc_purged,
        unpacked_research.ci_cc_purged,
        unpacked_research.pi_cc_full_response,
        unpacked_research.ci_cc_full_response,
        unpacked_research.cc_mean_projection_p_perp,
        unpacked_research.losses,
    )
    for array in (*research_arrays, unpacked_recovery.ci_i_direct, unpacked_recovery.losses):
        assert array.dtype == np.dtype(np.float64)
        assert array.flags.c_contiguous
        assert array.flags.owndata
        assert not array.flags.writeable
        assert not np.shares_memory(array, research_vector)
        assert not np.shares_memory(array, recovery_vector)
    for left_index, left in enumerate(research_arrays):
        for right in research_arrays[left_index + 1 :]:
            assert not np.shares_memory(left, right)


def test_pack_unpack_rejects_wrong_type_dtype_shape_nonfinite_and_variant() -> None:
    contract = load_resource_config(ROOT)
    valid = _research_payload()

    wrong_dtype = replace(valid, pi_1_direct=valid.pi_1_direct.astype(np.float32))
    with pytest.raises(TypeError, match="float64"):
        paper_cache.pack_research_paper_cache(wrong_dtype, contract=contract)

    wrong_shape = replace(valid, ci_i_direct=valid.ci_i_direct[:29])
    with pytest.raises(ValueError, match="shape"):
        paper_cache.pack_research_paper_cache(wrong_shape, contract=contract)

    nonfinite_losses = valid.losses.copy()
    nonfinite_losses[3, 7, 1] = np.nan
    with pytest.raises(ValueError, match="finite"):
        paper_cache.pack_research_paper_cache(
            replace(valid, losses=nonfinite_losses),
            contract=contract,
        )

    with pytest.raises(TypeError, match="PaperResearchDateCache"):
        paper_cache.pack_research_paper_cache(object(), contract=contract)
    with pytest.raises(TypeError, match="PaperRecoveryDateCache"):
        paper_cache.pack_recovery_paper_cache(valid, contract=contract)

    research = np.zeros(8_460, dtype=np.float64)
    recovery = np.zeros(960, dtype=np.float64)
    with pytest.raises(ValueError, match="shape|research"):
        paper_cache.unpack_research_paper_cache(recovery, contract=contract)
    with pytest.raises(ValueError, match="shape|recovery"):
        paper_cache.unpack_recovery_paper_cache(research, contract=contract)
    with pytest.raises(TypeError, match="float64"):
        paper_cache.unpack_research_paper_cache(
            research.astype(np.float32),
            contract=contract,
        )
    nonfinite_vector = research.copy()
    nonfinite_vector[2_929] = np.inf
    with pytest.raises(ValueError, match="finite"):
        paper_cache.unpack_research_paper_cache(nonfinite_vector, contract=contract)
    with pytest.raises(TypeError, match="numpy.ndarray"):
        paper_cache.unpack_recovery_paper_cache([0.0] * 960, contract=contract)


def test_a027_module_exposes_no_rng_path_serializer_fixture_or_execution_authority() -> None:
    source = inspect.getsource(paper_cache)

    assert "numpy.random" not in source
    assert "SeedSequence" not in source
    assert "default_rng" not in source
    assert "from pathlib" not in source
    assert "np.save" not in source
    assert "np.load" not in source
    assert ".npy" not in source
    assert not any(
        token in name.lower()
        for name in paper_cache.__all__
        for token in ("path", "write", "save", "load", "fixture", "bootstrap", "rng", "root")
    )
