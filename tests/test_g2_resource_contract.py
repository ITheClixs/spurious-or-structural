from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path
from typing import Any

import pytest

from xid.models import g2_resource
from xid.models.g2_resource import (
    FROZEN_RESOURCE_CONFIG_SHA256,
    FROZEN_RESOURCE_CONFIG_TYPE_TREE_SHA256,
    ResourceConfig,
    load_resource_config,
    parse_resource_config_bytes,
)


ROOT = Path(__file__).parents[1]
CONFIG_PATH = ROOT / "configs/g2_resource.toml"
EXPECTED_CONFIG_BYTES = 9_799
EXPECTED_CONFIG_SHA256 = (
    "3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29"
)
EXPECTED_TYPE_ROW_COUNT = 194
EXPECTED_TYPE_TREE_SHA256 = (
    "e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3"
)
EXPECTED_CJSON_BYTES = 9_473


def _raw_config() -> bytes:
    return CONFIG_PATH.read_bytes()


def _parsed_config_object() -> dict[str, Any]:
    return tomllib.loads(_raw_config().decode("ascii"))


def test_resource_config_file_is_the_a026_byte_exact_contract() -> None:
    raw = _raw_config()

    assert len(raw) == EXPECTED_CONFIG_BYTES
    assert raw.isascii()
    assert raw[:3] != b"\xef\xbb\xbf"
    assert b"\r" not in raw
    assert raw.endswith(b"\n")
    assert not raw.endswith(b"\n\n")
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_CONFIG_SHA256

    contract = load_resource_config(ROOT)
    assert isinstance(contract, ResourceConfig)
    assert contract.raw_sha256 == EXPECTED_CONFIG_SHA256
    assert contract.raw_byte_count == EXPECTED_CONFIG_BYTES
    assert contract.type_tree_sha256 == EXPECTED_TYPE_TREE_SHA256
    assert len(contract.type_rows) == EXPECTED_TYPE_ROW_COUNT
    assert contract.cjson_bytes.endswith(b"\n")
    assert len(contract.cjson_bytes) == EXPECTED_CJSON_BYTES
    assert FROZEN_RESOURCE_CONFIG_SHA256 == EXPECTED_CONFIG_SHA256
    assert FROZEN_RESOURCE_CONFIG_TYPE_TREE_SHA256 == EXPECTED_TYPE_TREE_SHA256


def test_resource_config_parser_exposes_the_typed_contract_literals() -> None:
    contract = parse_resource_config_bytes(_raw_config())

    assert contract.schema_version == 2
    assert contract.design_id == "S0004"
    assert contract.gate == "G2"
    assert contract.authority == "A022+A023+A024+A025+A026"
    assert contract.unknown_keys == "reject"
    assert contract.entry_module == "xid.g2_resource_benchmark"
    assert contract.base_config == "configs/g2.toml"
    assert contract.base_config_sha256 == (
        "f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc"
    )
    assert contract.population_targets == "configs/g2_population_targets.json"
    assert contract.population_targets_sha256 == (
        "f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59"
    )
    assert contract.roots.registered.result == "results/g2_resource_benchmark"
    assert contract.roots.rehearsal.result == "results/g2_resource_rehearsal"
    assert contract.addresses.rehearsal.seed == 1729
    assert contract.addresses.rehearsal.panel_indices == (10000, 10001, 10002)
    assert contract.addresses.registered.seed == 2026071529
    assert contract.addresses.registered.smooth_stream == "resource_smooth"
    assert contract.addresses.registered.paper_stream == "resource_paper"
    assert contract.addresses.call_schedule.cold_equal == (
        1260,
        0,
        25,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        5,
        5,
        25,
        0,
        0,
    )
    assert contract.schedule.rate_trace_interruption_rule == (
        "inside-any-rate-bearing-trace-select-terminal-failure-exclude-all-trace-rate-evidence-v1"
    )
    assert contract.terminal.nonpass_publication_rule == (
        "immutable-terminal-entry-selection-successor-rebuildable-forensic-close-v1"
    )
    assert contract.process.launch_quiescence_kind == (
        "darwin-fileglob-flock-exclusive-lease-v1"
    )
    assert contract.process.launch_quiescence_filename == "quiescence.lock"
    assert contract.process.launch_quiescence_mode == 0o600
    assert contract.hard_stops.maximum_terminal_nonpass_intent_bytes == 131072


@pytest.mark.parametrize(
    "bad_raw",
    [
        _raw_config() + b"\n",
        _raw_config().replace(b'schema_version = 2\n', b'schema_version = 3\n', 1),
        b"\xef\xbb\xbf" + _raw_config(),
        _raw_config().replace(b"\n", b"\r\n", 1),
    ],
)
def test_sealed_resource_config_rejects_byte_or_hash_drift(
    bad_raw: bytes,
) -> None:
    with pytest.raises(ValueError, match="resource config"):
        parse_resource_config_bytes(bad_raw)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda obj: obj.__setitem__("unexpected", "reject-me"),
        lambda obj: obj.__delitem__("authority"),
        lambda obj: obj.__setitem__("schema_version", True),
        lambda obj: obj["addresses"]["rehearsal"].__setitem__("panel_indices", [10000, 10002, 10001]),
        lambda obj: obj["process"].__setitem__("launch_quiescence_mode", "0600"),
        lambda obj: obj["schedule"].__setitem__("thermal_minimum_ns", 600000000000.0),
        lambda obj: obj["runtime"].__setitem__("single_thread", 1),
    ],
)
def test_resource_config_object_validation_rejects_schema_drift(
    mutation: Any,
) -> None:
    parsed = _parsed_config_object()
    mutation(parsed)

    with pytest.raises(ValueError, match="resource config"):
        g2_resource._resource_config_from_object(parsed)


def test_resource_config_type_tree_uses_the_corrected_a026_digest() -> None:
    contract = parse_resource_config_bytes(_raw_config())
    cjson_payload = json.dumps(
        ["xid-g2-resource-config-type-tree-v1", contract.type_rows],
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("ascii") + b"\n"

    assert len(contract.type_rows) == EXPECTED_TYPE_ROW_COUNT
    assert hashlib.sha256(cjson_payload).hexdigest() == EXPECTED_TYPE_TREE_SHA256
    assert contract.type_tree_sha256 == EXPECTED_TYPE_TREE_SHA256
