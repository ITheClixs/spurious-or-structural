"""Deterministic A027 paper-cache field order and in-memory representation.

This module contains no RNG constructor, filesystem path, artifact writer, or
registered execution entry point. It only maps already-computed semantic
paper fields to the sealed A027 in-memory vector order and back.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from xid.models.g2_resource import (
    FROZEN_RESOURCE_CONFIG_SHA256,
    FROZEN_RESOURCE_CONFIG_TYPE_TREE_SHA256,
    ResourceConfig,
)

PAPER_CACHE_ORDER_NAMESPACE = "xid-g2-paper-cache-order-v1"
PAPER_CACHE_ORDER_MANIFEST_NAMESPACE = "xid-g2-paper-cache-order-manifest-v1"
PAPER_CACHE_ORDER_MANIFEST_SHA256 = (
    "8810471ce6c0747af7cdda48299989303cd85a9c7def7c681f2a57f93348a083"
)
PAPER_CACHE_MATRIX_ORDER = (
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
PAPER_CACHE_LOSS_SPEC_ORDER = ("PI_1", "PI_I", "CI_1", "CI_I", "PI_CC", "CI_CC")
PAPER_CACHE_LOSS_KIND_ORDER = ("sse", "sst")
PAPER_CACHE_RESEARCH_FIELD_COUNT = 8_460
PAPER_CACHE_RECOVERY_FIELD_COUNT = 960

__all__ = (
    "PAPER_CACHE_LOSS_KIND_ORDER",
    "PAPER_CACHE_LOSS_SPEC_ORDER",
    "PAPER_CACHE_MATRIX_ORDER",
    "PAPER_CACHE_ORDER_MANIFEST_NAMESPACE",
    "PAPER_CACHE_ORDER_MANIFEST_SHA256",
    "PAPER_CACHE_ORDER_NAMESPACE",
    "PAPER_CACHE_RECOVERY_FIELD_COUNT",
    "PAPER_CACHE_RESEARCH_FIELD_COUNT",
    "PaperCacheField",
    "PaperCacheLossField",
    "PaperCacheMatrixField",
    "PaperRecoveryDateCache",
    "PaperResearchDateCache",
    "pack_recovery_paper_cache",
    "pack_research_paper_cache",
    "paper_cache_order_manifest_bytes",
    "recovery_paper_cache_field",
    "recovery_paper_cache_index",
    "research_paper_cache_field",
    "research_paper_cache_index",
    "unpack_recovery_paper_cache",
    "unpack_research_paper_cache",
)

_ASSET_COUNT = 30
_MATRIX_FIELD_COUNT = _ASSET_COUNT * _ASSET_COUNT
_RESEARCH_MATRIX_FIELD_COUNT = len(PAPER_CACHE_MATRIX_ORDER) * _MATRIX_FIELD_COUNT
_LOSS_SPEC_FIELD_COUNT = _ASSET_COUNT * len(PAPER_CACHE_LOSS_KIND_ORDER)
_RECOVERY_MATRIX_NAME = "CI_I_direct"
_RECOVERY_LOSS_SPECIFICATION = "CI_I"
_EXPECTED_AUTHORITY = "A022+A023+A024+A025+A026+A027"
_EXPECTED_TYPE_TREE_SHA256 = FROZEN_RESOURCE_CONFIG_TYPE_TREE_SHA256
_EXPECTED_RAW_SHA256 = FROZEN_RESOURCE_CONFIG_SHA256

_ORDER_MANIFEST_VALUE: dict[str, object] = {
    "namespace": PAPER_CACHE_ORDER_NAMESPACE,
    "matrix_order": list(PAPER_CACHE_MATRIX_ORDER),
    "matrix_row_axis": "response_or_output_asset_index_ascending_zero_through_29",
    "matrix_column_axis": "flow_or_input_asset_index_ascending_zero_through_29",
    "matrix_value_order": "matrix_then_row_then_column",
    "matrix_payload": (
        "original_unit_slope_operator_only_no_intercept_or_factor_coefficient_except_p_perp_"
        "is_the_asset_space_operator"
    ),
    "loss_spec_order": list(PAPER_CACHE_LOSS_SPEC_ORDER),
    "loss_response_axis": "response_asset_index_ascending_zero_through_29",
    "loss_kind_order": list(PAPER_CACHE_LOSS_KIND_ORDER),
    "loss_value_order": "spec_then_response_then_kind",
    "research_layout": "nine_matrices_then_all_loss_pairs",
    "recovery_layout": "ci_i_direct_matrix_then_ci_i_loss_pairs",
    "recovery_relation": "distinct_compact_semantic_projection_not_research_prefix",
    "research_field_count": PAPER_CACHE_RESEARCH_FIELD_COUNT,
    "recovery_field_count": PAPER_CACHE_RECOVERY_FIELD_COUNT,
}


@dataclass(frozen=True, slots=True)
class PaperCacheMatrixField:
    """One original-unit matrix entry in response/output-by-flow/input orientation."""

    matrix_name: str
    response_or_output_index: int
    flow_or_input_index: int


@dataclass(frozen=True, slots=True)
class PaperCacheLossField:
    """One response-level out-of-sample SSE or SST component."""

    specification_name: str
    response_index: int
    loss_kind: str


type PaperCacheField = PaperCacheMatrixField | PaperCacheLossField


@dataclass(frozen=True, slots=True)
class PaperResearchDateCache:
    """Nine paper matrices and six-by-thirty SSE/SST pairs for one date."""

    pi_1_direct: NDArray[np.float64]
    pi_i_direct: NDArray[np.float64]
    ci_1_direct: NDArray[np.float64]
    ci_i_direct: NDArray[np.float64]
    pi_cc_purged: NDArray[np.float64]
    ci_cc_purged: NDArray[np.float64]
    pi_cc_full_response: NDArray[np.float64]
    ci_cc_full_response: NDArray[np.float64]
    cc_mean_projection_p_perp: NDArray[np.float64]
    losses: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class PaperRecoveryDateCache:
    """Compact CI_I matrix and its thirty response-level SSE/SST pairs."""

    ci_i_direct: NDArray[np.float64]
    losses: NDArray[np.float64]


def _canonical_manifest_bytes() -> bytes:
    encoded = json.dumps(
        [PAPER_CACHE_ORDER_MANIFEST_NAMESPACE, _ORDER_MANIFEST_VALUE],
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("ascii")
    return encoded + b"\n"


_ORDER_MANIFEST_BYTES = _canonical_manifest_bytes()
if hashlib.sha256(_ORDER_MANIFEST_BYTES).hexdigest() != PAPER_CACHE_ORDER_MANIFEST_SHA256:
    raise RuntimeError("compiled A027 paper-cache order manifest seal is inconsistent")


def _validate_contract(contract: ResourceConfig) -> None:
    if type(contract) is not ResourceConfig:
        raise TypeError("contract must use exact ResourceConfig")
    if (
        contract.raw_sha256 != _EXPECTED_RAW_SHA256
        or contract.type_tree_sha256 != _EXPECTED_TYPE_TREE_SHA256
        or contract.authority != _EXPECTED_AUTHORITY
    ):
        raise ValueError("sealed A027 resource contract identity drift")

    order = contract.artifacts.paper_cache_order
    observed = {
        "namespace": order.namespace,
        "matrix_order": list(order.matrix_order),
        "matrix_row_axis": order.matrix_row_axis,
        "matrix_column_axis": order.matrix_column_axis,
        "matrix_value_order": order.matrix_value_order,
        "matrix_payload": order.matrix_payload,
        "loss_spec_order": list(order.loss_spec_order),
        "loss_response_axis": order.loss_response_axis,
        "loss_kind_order": list(order.loss_kind_order),
        "loss_value_order": order.loss_value_order,
        "research_layout": order.research_layout,
        "recovery_layout": order.recovery_layout,
        "recovery_relation": order.recovery_relation,
        "research_field_count": order.research_field_count,
        "recovery_field_count": order.recovery_field_count,
    }
    if observed != _ORDER_MANIFEST_VALUE:
        raise ValueError("sealed A027 paper-cache order contract drift")


def _require_asset_index(value: object, *, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must use exact Python int")
    if value < 0 or value >= _ASSET_COUNT:
        raise ValueError(f"{name} is outside the sealed asset-index range")
    return value


def _require_vector_index(value: object, *, field_count: int, variant: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{variant} paper-cache index must use exact Python int")
    if value < 0 or value >= field_count:
        raise ValueError(f"{variant} paper-cache index is outside the sealed range")
    return value


def _matrix_coordinates(field: PaperCacheMatrixField) -> tuple[int, int, int]:
    if type(field.matrix_name) is not str:
        raise TypeError("matrix field name must use exact str")
    try:
        matrix_index = PAPER_CACHE_MATRIX_ORDER.index(field.matrix_name)
    except ValueError as error:
        raise ValueError("matrix field name is outside the sealed order") from error
    response_index = _require_asset_index(
        field.response_or_output_index,
        name="matrix response/output index",
    )
    flow_index = _require_asset_index(
        field.flow_or_input_index,
        name="matrix flow/input index",
    )
    return matrix_index, response_index, flow_index


def _loss_coordinates(field: PaperCacheLossField) -> tuple[int, int, int]:
    if type(field.specification_name) is not str or type(field.loss_kind) is not str:
        raise TypeError("loss field names must use exact str")
    try:
        specification_index = PAPER_CACHE_LOSS_SPEC_ORDER.index(field.specification_name)
    except ValueError as error:
        raise ValueError("loss specification is outside the sealed order") from error
    response_index = _require_asset_index(field.response_index, name="loss response index")
    try:
        loss_kind_index = PAPER_CACHE_LOSS_KIND_ORDER.index(field.loss_kind)
    except ValueError as error:
        raise ValueError("loss kind is outside the sealed order") from error
    return specification_index, response_index, loss_kind_index


def research_paper_cache_index(field: object, *, contract: ResourceConfig) -> int:
    """Return the sealed research-vector column for one semantic cache field."""

    _validate_contract(contract)
    if isinstance(field, PaperCacheMatrixField) and type(field) is PaperCacheMatrixField:
        matrix_index, response_index, flow_index = _matrix_coordinates(field)
        return matrix_index * _MATRIX_FIELD_COUNT + response_index * _ASSET_COUNT + flow_index
    if isinstance(field, PaperCacheLossField) and type(field) is PaperCacheLossField:
        specification_index, response_index, loss_kind_index = _loss_coordinates(field)
        return (
            _RESEARCH_MATRIX_FIELD_COUNT
            + specification_index * _LOSS_SPEC_FIELD_COUNT
            + response_index * len(PAPER_CACHE_LOSS_KIND_ORDER)
            + loss_kind_index
        )
    raise TypeError("field must use an exact paper-cache field type")


def research_paper_cache_field(index: object, *, contract: ResourceConfig) -> PaperCacheField:
    """Invert one sealed research-vector column to its semantic cache field."""

    _validate_contract(contract)
    checked = _require_vector_index(
        index,
        field_count=PAPER_CACHE_RESEARCH_FIELD_COUNT,
        variant="research",
    )
    if checked < _RESEARCH_MATRIX_FIELD_COUNT:
        matrix_index, matrix_remainder = divmod(checked, _MATRIX_FIELD_COUNT)
        response_index, flow_index = divmod(matrix_remainder, _ASSET_COUNT)
        return PaperCacheMatrixField(
            PAPER_CACHE_MATRIX_ORDER[matrix_index],
            response_index,
            flow_index,
        )

    loss_offset = checked - _RESEARCH_MATRIX_FIELD_COUNT
    specification_index, specification_remainder = divmod(
        loss_offset,
        _LOSS_SPEC_FIELD_COUNT,
    )
    response_index, loss_kind_index = divmod(
        specification_remainder,
        len(PAPER_CACHE_LOSS_KIND_ORDER),
    )
    return PaperCacheLossField(
        PAPER_CACHE_LOSS_SPEC_ORDER[specification_index],
        response_index,
        PAPER_CACHE_LOSS_KIND_ORDER[loss_kind_index],
    )


def recovery_paper_cache_index(field: object, *, contract: ResourceConfig) -> int:
    """Return the compact recovery-vector column for one CI_I semantic field."""

    _validate_contract(contract)
    if isinstance(field, PaperCacheMatrixField) and type(field) is PaperCacheMatrixField:
        _, response_index, flow_index = _matrix_coordinates(field)
        if field.matrix_name != _RECOVERY_MATRIX_NAME:
            raise ValueError("recovery paper-cache matrix field must be CI_I_direct")
        return response_index * _ASSET_COUNT + flow_index
    if isinstance(field, PaperCacheLossField) and type(field) is PaperCacheLossField:
        _, response_index, loss_kind_index = _loss_coordinates(field)
        if field.specification_name != _RECOVERY_LOSS_SPECIFICATION:
            raise ValueError("recovery paper-cache loss field must be CI_I")
        return (
            _MATRIX_FIELD_COUNT
            + response_index * len(PAPER_CACHE_LOSS_KIND_ORDER)
            + loss_kind_index
        )
    raise TypeError("field must use an exact paper-cache field type")


def recovery_paper_cache_field(index: object, *, contract: ResourceConfig) -> PaperCacheField:
    """Invert one compact recovery-vector column to its CI_I semantic field."""

    _validate_contract(contract)
    checked = _require_vector_index(
        index,
        field_count=PAPER_CACHE_RECOVERY_FIELD_COUNT,
        variant="recovery",
    )
    if checked < _MATRIX_FIELD_COUNT:
        response_index, flow_index = divmod(checked, _ASSET_COUNT)
        return PaperCacheMatrixField(
            _RECOVERY_MATRIX_NAME,
            response_index,
            flow_index,
        )

    response_index, loss_kind_index = divmod(
        checked - _MATRIX_FIELD_COUNT,
        len(PAPER_CACHE_LOSS_KIND_ORDER),
    )
    return PaperCacheLossField(
        _RECOVERY_LOSS_SPECIFICATION,
        response_index,
        PAPER_CACHE_LOSS_KIND_ORDER[loss_kind_index],
    )


def _require_float64_array(
    value: object,
    *,
    name: str,
    shape: tuple[int, ...],
) -> NDArray[np.float64]:
    if type(value) is not np.ndarray:
        raise TypeError(f"{name} must be an exact numpy.ndarray")
    array = value
    if array.dtype != np.dtype(np.float64):
        raise TypeError(f"{name} must use exact float64 representation")
    if array.shape != shape:
        raise ValueError(f"{name} shape must be exactly {shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def _research_matrices(
    payload: PaperResearchDateCache,
) -> tuple[NDArray[np.float64], ...]:
    return (
        payload.pi_1_direct,
        payload.pi_i_direct,
        payload.ci_1_direct,
        payload.ci_i_direct,
        payload.pi_cc_purged,
        payload.ci_cc_purged,
        payload.pi_cc_full_response,
        payload.ci_cc_full_response,
        payload.cc_mean_projection_p_perp,
    )


def _readonly_vector(field_count: int) -> NDArray[np.float64]:
    return np.empty(field_count, dtype=np.float64, order="C")


def _readonly_array_from_flat(
    flat: NDArray[np.float64],
    *,
    shape: tuple[int, ...],
) -> NDArray[np.float64]:
    output = np.empty(shape, dtype=np.float64, order="C")
    output[...] = flat.reshape(shape, order="C")
    output.setflags(write=False)
    return output


def pack_research_paper_cache(
    payload: object,
    *,
    contract: ResourceConfig,
) -> NDArray[np.float64]:
    """Pack one research-date semantic payload into the sealed 8,460-vector."""

    _validate_contract(contract)
    if (
        not isinstance(payload, PaperResearchDateCache)
        or type(payload) is not PaperResearchDateCache
    ):
        raise TypeError("payload must use exact PaperResearchDateCache")

    matrices = tuple(
        _require_float64_array(
            matrix,
            name=PAPER_CACHE_MATRIX_ORDER[matrix_index],
            shape=(_ASSET_COUNT, _ASSET_COUNT),
        )
        for matrix_index, matrix in enumerate(_research_matrices(payload))
    )
    losses = _require_float64_array(
        payload.losses,
        name="research losses",
        shape=(len(PAPER_CACHE_LOSS_SPEC_ORDER), _ASSET_COUNT, len(PAPER_CACHE_LOSS_KIND_ORDER)),
    )

    packed = _readonly_vector(PAPER_CACHE_RESEARCH_FIELD_COUNT)
    for matrix_index, matrix in enumerate(matrices):
        start = matrix_index * _MATRIX_FIELD_COUNT
        packed[start : start + _MATRIX_FIELD_COUNT] = matrix.reshape(-1, order="C")
    packed[_RESEARCH_MATRIX_FIELD_COUNT:] = losses.reshape(-1, order="C")
    packed.setflags(write=False)
    return packed


def pack_recovery_paper_cache(
    payload: object,
    *,
    contract: ResourceConfig,
) -> NDArray[np.float64]:
    """Pack one compact CI_I recovery payload into the sealed 960-vector."""

    _validate_contract(contract)
    if (
        not isinstance(payload, PaperRecoveryDateCache)
        or type(payload) is not PaperRecoveryDateCache
    ):
        raise TypeError("payload must use exact PaperRecoveryDateCache")

    matrix = _require_float64_array(
        payload.ci_i_direct,
        name=_RECOVERY_MATRIX_NAME,
        shape=(_ASSET_COUNT, _ASSET_COUNT),
    )
    losses = _require_float64_array(
        payload.losses,
        name="recovery CI_I losses",
        shape=(_ASSET_COUNT, len(PAPER_CACHE_LOSS_KIND_ORDER)),
    )

    packed = _readonly_vector(PAPER_CACHE_RECOVERY_FIELD_COUNT)
    packed[:_MATRIX_FIELD_COUNT] = matrix.reshape(-1, order="C")
    packed[_MATRIX_FIELD_COUNT:] = losses.reshape(-1, order="C")
    packed.setflags(write=False)
    return packed


def unpack_research_paper_cache(
    vector: object,
    *,
    contract: ResourceConfig,
) -> PaperResearchDateCache:
    """Unpack a sealed-order research vector into independent read-only arrays."""

    _validate_contract(contract)
    packed = _require_float64_array(
        vector,
        name="research paper-cache vector",
        shape=(PAPER_CACHE_RESEARCH_FIELD_COUNT,),
    )
    matrices = tuple(
        _readonly_array_from_flat(
            packed[matrix_index * _MATRIX_FIELD_COUNT : (matrix_index + 1) * _MATRIX_FIELD_COUNT],
            shape=(_ASSET_COUNT, _ASSET_COUNT),
        )
        for matrix_index in range(len(PAPER_CACHE_MATRIX_ORDER))
    )
    losses = _readonly_array_from_flat(
        packed[_RESEARCH_MATRIX_FIELD_COUNT:],
        shape=(len(PAPER_CACHE_LOSS_SPEC_ORDER), _ASSET_COUNT, len(PAPER_CACHE_LOSS_KIND_ORDER)),
    )
    return PaperResearchDateCache(
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


def unpack_recovery_paper_cache(
    vector: object,
    *,
    contract: ResourceConfig,
) -> PaperRecoveryDateCache:
    """Unpack a compact recovery vector into independent read-only CI_I arrays."""

    _validate_contract(contract)
    packed = _require_float64_array(
        vector,
        name="recovery paper-cache vector",
        shape=(PAPER_CACHE_RECOVERY_FIELD_COUNT,),
    )
    matrix = _readonly_array_from_flat(
        packed[:_MATRIX_FIELD_COUNT],
        shape=(_ASSET_COUNT, _ASSET_COUNT),
    )
    losses = _readonly_array_from_flat(
        packed[_MATRIX_FIELD_COUNT:],
        shape=(_ASSET_COUNT, len(PAPER_CACHE_LOSS_KIND_ORDER)),
    )
    return PaperRecoveryDateCache(matrix, losses)


def paper_cache_order_manifest_bytes(*, contract: ResourceConfig) -> bytes:
    """Return the LF-terminated canonical A027 order manifest bytes."""

    _validate_contract(contract)
    return _ORDER_MANIFEST_BYTES
