"""Sealed A027 resource configuration contract.

This module is deliberately side-effect light: it reads only the frozen
resource TOML when asked to load the contract, rejects drift before any caller
can create roots or RNG state, and exposes immutable Python values for the
runner stages that are still gated.
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, NoReturn, cast

FROZEN_RESOURCE_CONFIG_BYTE_COUNT = 10_863
FROZEN_RESOURCE_CONFIG_SHA256 = "1a14fd68012819d5f901a97ddd9e9a58dd35886bdcc5d47728467f6417fc3cd3"
FROZEN_RESOURCE_CONFIG_TYPE_ROW_COUNT = 209
FROZEN_RESOURCE_CONFIG_TYPE_TREE_SHA256 = (
    "81eed87be58bf04a897fdcf3dd39cf142944647824a9f97938d46f341803a2ff"
)
_CONFIG_RELATIVE_PATH = Path("configs/g2_resource.toml")
_TYPE_TREE_NAMESPACE = "xid-g2-resource-config-type-tree-v1"
_FROZEN_RESOURCE_CONFIG_JSON = (
    '{"addresses":{"bootstrap_component_id":6,"bootstrap_replicate_range":[0,25],"call_schedu'
    'le":{"bootstrap_order":"replicate-ascending-v1","cold_equal":[1260,0,25,0,0,0,0,0,0,0,5,'
    '5,25,0,0],"dgp_order":"date-major-component-ascending-v1","paper_weight_rule":"draw-at-f'
    'irst-positive-k13-persist-through-last-positive-k13-v1","research":[1260,0,25,0,0,0,0,0,'
    '0,0,5,0,0,25,0],"validation":[1260,0,25,0,0,0,0,0,0,0,0,5,25,0,0]},"cell_key":0,"config_'
    'schema_version":3,"dgp_component_ids":[1,2,3,4,5],"n_dates":252,"registered":{"bootstrap'
    '_phase_scenario":[40,0],"first_panel_index":0,"panel_rule":"contiguous-no-gap-no-reassig'
    'nment","paper_phase_scenario":[10,1],"paper_stream":"resource_paper","seed":2026071529,"'
    'smooth_phase_scenario":[10,0],"smooth_stream":"resource_smooth"},"rehearsal":{"panel_ind'
    'ices":[10000,10001,10002],"seed":1729},"rng_key_schema_version":2},"artifacts":{"dtype":'
    '"<f8","fortran_order":false,"manifest_cap_bytes":1048576,"marker_cap_bytes":16384,"npy_f'
    'ormat":"1.0","npy_prefix_bytes":128,"paper_cache_order":{"loss_kind_order":["sse","sst"]'
    ',"loss_response_axis":"response_asset_index_ascending_zero_through_29","loss_spec_order":['
    '"PI_1","PI_I","CI_1","CI_I","PI_CC","CI_CC"],"loss_value_order":"spec_then_response_then'
    '_kind","matrix_column_axis":"flow_or_input_asset_index_ascending_zero_through_29","matrix_'
    'order":["PI_1_direct","PI_I_direct","CI_1_direct","CI_I_direct","PI_CC_purged","CI_CC_pur'
    'ged","PI_CC_full_response","CI_CC_full_response","cc_mean_projection_p_perp"],"matrix_pay'
    'load":"original_unit_slope_operator_only_no_intercept_or_factor_coefficient_except_p_perp_'
    'is_the_asset_space_operator","matrix_row_axis":"response_or_output_asset_index_ascending_z'
    'ero_through_29","matrix_value_order":"matrix_then_row_then_column","namespace":"xid-g2-pap'
    'er-cache-order-v1","recovery_field_count":960,"recovery_layout":"ci_i_direct_matrix_then_c'
    'i_i_loss_pairs","recovery_relation":"distinct_compact_semantic_projection_not_research_pr'
    'efix","research_field_count":8460,"research_layout":"nine_matrices_then_all_loss_pairs"},"p'
    'ublication_envelope_elements_per_shard":595000,"pu'
    'blication_envelope_numeric_bytes":238000000,"publication_envelope_shards":50,"rehearsal_'
    'artifact_kind_count":13,"rehearsal_artifact_row_count":51,"resume_lifecycle":{"cleanup_i'
    'ntent_record_positions":[9,12,13,14],"create_after_record_positions":[0,1,2,3,4,5],"pape'
    'r_weight_cleanup_positions":[13,12,13],"paper_weight_last_consumer_positions":[13,12,13]'
    ',"paper_weight_last_consumer_rule":"last-positive-k13-position-v1","paper_weight_produce'
    'r_positions":[12,12,13],"paper_weight_producer_rule":"first-positive-k13-position-v1","p'
    'aper_weight_role_order":["cold_equal","validation","research"],"smooth_last_use_record_p'
    'osition":9},"root_receipt_cap_bytes":1048576,"shapes":{"null_batch":[25,3,9],"paper_boot'
    'strap_recovery":[25,960],"paper_bootstrap_research":[25,8460],"paper_cache_recovery":[25'
    '2,960],"paper_cache_research_shard":[63,8460],"paper_full_date":[8460],"paper_recovery_d'
    'ate":[960],"publication_envelope_shard":[595000],"resume_base_panel":[252,2016],"resume_'
    'bootstrap_weights":[25,252],"resume_candidate_focal_equal_validation":[25,9],"resume_can'
    'didate_focal_research":[25,1],"resume_cell_x0ty":[252,63,30],"resume_cell_yty_upper":[25'
    '2,465],"resume_paper_bootstrap_weights":[25,252]}},"authority":"A022+A023+A024+A025+A026+A027'
    '","base_config":"configs/g2.toml","base_config_sha256":"f6291894462db2215ec9d94b2b936f5b'
    '969e47b61cdbbe50de7ae0782a83defc","design_id":"S0004","entry_module":"xid.g2_resource_be'
    'nchmark","gate":"G2","hard_stops":{"absolute_transient_bytes":30000000000,"attempt_boots'
    'trap_ns":480000000000,"boundary_publication_ns":60000000000,"checkpoint_margin_tree_byte'
    's":1600000000,"checkpoint_tree_bytes":2000000000,"checkpoint_work_ns":480000000000,"comb'
    'ined_expected_ns":57600000000000,"combined_hard_ns":115200000000000,"created_transient_b'
    'ytes":6000000000,"durable_marker_interval_ns":540000000000,"maximum_canonical_path_bytes'
    '":240,"maximum_cleanup_row_bytes":1024,"maximum_failure_intent_envelope_bytes":753664,"m'
    'aximum_failure_intent_nonrow_bytes":131072,"maximum_failure_resume_count":641,"maximum_i'
    'nterruption_count":63,"maximum_process_death_row_bytes":512,"maximum_process_death_rows"'
    ':128,"maximum_sampler_gap_ns":1000000000,"maximum_terminal_cleanup_rows":512,"maximum_te'
    'rminal_nonpass_intent_bytes":131072,"maximum_trace_count":4096,"maximum_worker_count":64'
    ',"maximum_worker_wait_row_bytes":512,"payload_bytes":5242880,"peak_rss_bytes":3500000000'
    ',"research_expected_ns":10800000000000,"research_hard_ns":21600000000000,"resource_expec'
    'ted_ns":3600000000000,"resource_hard_ns":7200000000000,"sampler_period_ns":50000000,"ste'
    'ady_total_bytes":25000000000,"task_ns":480000000000,"unknown_loss_absolute_workspace_upp'
    'er_bytes":30000000001,"unknown_loss_checkpoint_tree_upper_bytes":2000000001,"unknown_los'
    's_created_roots_upper_bytes":6000000001,"unknown_loss_rss_upper_bytes":3500000001,"valid'
    'ation_expected_ns":43200000000000,"validation_hard_ns":86400000000000},"kernels":{"artif'
    'act_io_kernel_ids":[1,2,3,4,5,6,8,9,10,11,12,13,14],"canonical_boundaries_per_trace":15,'
    '"canonical_boundary_next_positions":[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"clock_resolut'
    'ion_enclosure_multiplier":2,"cold_rate_denominator":3,"cold_rate_numerator":5,"first_epo'
    'ch_internal_cutoff":"post-k1-pre-k2-nondurable-cumulative-v1","first_epoch_positions":[0'
    ',1],"first_epoch_registry_rule":"baseline-before-k1-retained-after-k1-baseline-after-k2-'
    'v1","measurability_kernel_ids":[3,4,5,6,7],"measurability_minimum_ns":100000000,"project'
    'ion_margin_denominator":4,"projection_margin_numerator":5,"record_order":["k1-default","'
    'k2-default","k3-default","k4-default","k5-default","k6-default","k7-default","k9-default'
    '","k10-default","k8-default","k11-default","k12-default","k13-recovery","k13-research","'
    'k14-default"],"rehearsal_boundary_count":45,"rehearsal_cleanup_intent_count":12,"rehears'
    'al_resource_accounting_row_count":58,"rehearsal_terminal_accounting_row_count":1,"rehear'
    'sal_trace_count":3,"units":{"cold_equal":[252,252,25,225,225,225,4096,1,1,1,1,1,6048000,'
    '53298000,1],"research":[252,252,25,25,25,25,1,1,1,1,1,0,0,53298000,1],"validation":[252,'
    '252,25,225,225,225,1,1,1,1,0,1,6048000,0,1]}},"population_targets":"configs/g2_populatio'
    'n_targets.json","population_targets_sha256":"f13adcff4259773485ca5952d23ae923d3c501c84d4'
    'edb102c1886460ada4a59","process":{"death_methods":["wait4-reaped","double-process-identi'
    'ty-absence","boot-identity-changed"],"initial_supervisor_identity":"pid-start-boot-v1","'
    'launch_quiescence_filename":"quiescence.lock","launch_quiescence_kind":"darwin-fileglob-'
    'flock-exclusive-lease-v1","launch_quiescence_mode":384,"launch_quiescence_rule":"atomic-'
    'intent-directory-stable-inode-no-unlock-no-dup-no-pass-no-descendant-last-close-v1","lau'
    'nch_quiescence_successor_rule":"fresh-open-nofollow-fstat-same-inode-flock-ex-nb-plus-su'
    'pervisor-death-v1"},"registered_make_target":"g2-resource-benchmark","registries":{"name'
    's":["_RAW_BASE_REGISTRY","_G2_DATE_REGISTRY","_CONTRACT_DESIGN_REGISTRY","_CONTRACT_BASE'
    '_DATE_REGISTRY","_CONTRACT_CELL_DATE_REGISTRY","_CONTRACT_BASE_PANEL_REGISTRY","_CONTRAC'
    'T_CELL_PANEL_REGISTRY","_CONTRACT_AGGREGATE_REGISTRY","_RESOURCE_ARTIFACT_REGISTRY"]},"r'
    'ehearsal_make_target":"g2-resource-rehearsal","replay":{"first_epoch_rule":"one-epoch-or'
    'dinal-full-penalty-per-record-v1","maximum_lost_work_ns":480000000000,"maximum_marker_in'
    'terval_ns":540000000000,"penalty_ns":480000000000,"powered_off_exclusion_ns":0},"roots":'
    '{"registered":{"checkpoint":"data/g2_resource_benchmark/checkpoints","result":"results/g'
    '2_resource_benchmark","scratch":"data/g2_resource_benchmark/scratch"},"rehearsal":{"chec'
    'kpoint":"data/g2_resource_rehearsal/checkpoints","result":"results/g2_resource_rehearsal'
    '","scratch":"data/g2_resource_rehearsal/scratch"}},"runtime":{"byteorder":"little","mach'
    'ine":"arm64","numpy_version":"2.5.1","python_implementation":"cpython","python_version":'
    '"3.13.5","single_thread":true,"system":"Darwin","thread_env":{"BLIS_NUM_THREADS":"1","MK'
    'L_NUM_THREADS":"1","NUMEXPR_NUM_THREADS":"1","OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS'
    '":"1","VECLIB_MAXIMUM_THREADS":"1"}},"schedule":{"boundary_rule":"canonical-worker-ready'
    "-post-k1-k2-post-remaining-record-trace-measurement-plus-resume-worker-ready-copy-prefix"
    '-v1","cold_trace_count":1,"measurement_pair_order":[["validation","research"],["research'
    '","validation"]],"rate_trace_interruption_rule":"inside-any-rate-bearing-trace-select-te'
    'rminal-failure-exclude-all-trace-rate-evidence-v1","recovery_thermal_rule":"between-rate'
    '-traces-reset-600s-before-next-warm-trace-recovery-cycle-restarts-v2","rehearsal_success'
    '_rule":"retain-evidence-roots-no-post-result-cleanup-v1","reservation_resume_rule":"immu'
    'table-original-claim-contiguous-predecessor-ancestry-v1","telemetry_continuity_rule":"cl'
    'osed-segments-only-unknown-loss-limit-plus-one-v1","thermal_minimum_ns":600000000000,"th'
    'ermal_phase_order":["validation","research","research","validation"],"warm_block_count":'
    '3,"warm_block_minimum_ns":200000000000,"warm_block_minimum_pairs":4},"schema_version":2,'
    '"source":{"authority_namespace":"xid-g2-resource-authority-source-snapshot-v1","authorit'
    'y_paths":["src/xid","configs/g2.toml","configs/g2_population_targets.json","configs/g2_r'
    'esource.toml","PREREGISTRATION.md","docs/G2_COMPUTE_PLAN.md","docs/derivations/GATE_G2_R'
    'ESOURCE_ADMISSION.md","docs/derivations/GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md","docs/pr'
    'edictions/GATE_G2_RESOURCE.md","pyproject.toml","uv.lock",".python-version","Makefile"],'
    '"executable_namespace":"xid-g2-resource-executable-source-snapshot-v1","executable_paths'
    '":["src/xid","configs/g2.toml","configs/g2_population_targets.json","configs/g2_resource'
    '.toml","pyproject.toml","uv.lock",".python-version","Makefile"],"namespace_suffix_rule":'
    '"append-one-lf-before-sha256-v1","panel_namespace":"xid-g2-source-snapshot-v1","panel_pa'
    'ths":["src/xid","configs/g2.toml","configs/g2_population_targets.json","pyproject.toml",'
    '"uv.lock",".python-version","Makefile"]},"terminal":{"accounting_charge_ns":60000000000,'
    '"accounting_method":"fixed-terminal-accounting-charge-v1","failure_path":"terminal/failu'
    're","failure_stage":"terminal/.failure.xid-g2-terminal-stage-v1","nonpass_path":"termina'
    'l/nonpass","nonpass_publication_rule":"immutable-terminal-entry-selection-successor-rebu'
    'ildable-forensic-close-v1","nonpass_stage":"terminal/.nonpass.xid-g2-terminal-stage-v1",'
    '"publication_rule":"write-fsync-children-stage-no-overwrite-directory-rename-parent-fsyn'
    'c-v1","success_path":"terminal/success","success_stage":"terminal/.success.xid-g2-termin'
    'al-stage-v1"},"unknown_keys":"reject"}'
)


@dataclass(frozen=True, slots=True)
class FrozenResourceSection:
    """Immutable attribute view over a nested resource-config table."""

    _values: Mapping[str, Any]

    def __getattr__(self, name: str) -> Any:
        try:
            return self._values[name]
        except KeyError as error:
            raise AttributeError(name) from error


@dataclass(frozen=True, slots=True)
class ResourceConfig:
    """Typed, immutable view of the byte-sealed resource TOML."""

    raw_sha256: str
    raw_byte_count: int
    type_rows: tuple[tuple[str, str], ...]
    type_tree_sha256: str
    cjson_bytes: bytes
    schema_version: int
    design_id: str
    gate: str
    authority: str
    entry_module: str
    registered_make_target: str
    rehearsal_make_target: str
    base_config: str
    base_config_sha256: str
    population_targets: str
    population_targets_sha256: str
    unknown_keys: str
    roots: FrozenResourceSection
    source: FrozenResourceSection
    runtime: FrozenResourceSection
    addresses: FrozenResourceSection
    kernels: FrozenResourceSection
    schedule: FrozenResourceSection
    terminal: FrozenResourceSection
    process: FrozenResourceSection
    hard_stops: FrozenResourceSection
    artifacts: FrozenResourceSection
    replay: FrozenResourceSection
    registries: FrozenResourceSection


def _fail(message: str) -> NoReturn:
    raise ValueError(f"sealed resource config: {message}")


def _config_path(root: Path) -> Path:
    return root / _CONFIG_RELATIVE_PATH


def _canonical_json_bytes(value: object) -> bytes:
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("ascii")
    except (TypeError, ValueError) as error:
        _fail(f"non-canonical JSON value: {error}")
    return encoded + b"\n"


def _type_descriptor(value: object) -> str:
    if type(value) is bool:
        return "boolean"
    if type(value) is int:
        return "integer"
    if type(value) is str:
        return "string"
    if type(value) is list:
        element_types = tuple(_type_descriptor(element) for element in value)
        if not element_types:
            _fail("empty arrays are not part of the resource config")
        if len(set(element_types)) != 1:
            _fail("heterogeneous arrays are not part of the resource config")
        return f"array[{element_types[0]};{len(value)}]"
    _fail(f"unsupported type {type(value).__name__}")


def _type_rows(value: Mapping[str, object]) -> tuple[tuple[str, str], ...]:
    rows: list[tuple[str, str]] = []

    def visit(prefix: str, node: object) -> None:
        if type(node) is dict:
            for key, child in node.items():
                if type(key) is not str:
                    _fail("non-string table key")
                visit(f"{prefix}.{key}" if prefix else key, child)
            return
        rows.append((prefix, _type_descriptor(node)))

    visit("", value)
    return tuple(sorted(rows, key=lambda row: row[0].encode("utf-8")))


def _type_tree_bytes(rows: tuple[tuple[str, str], ...]) -> bytes:
    json_rows = [[path, descriptor] for path, descriptor in rows]
    return _canonical_json_bytes([_TYPE_TREE_NAMESPACE, json_rows])


def _freeze(value: object) -> Any:
    if type(value) is dict:
        return FrozenResourceSection(
            MappingProxyType({key: _freeze(child) for key, child in value.items()})
        )
    if type(value) is list:
        return tuple(_freeze(child) for child in value)
    return value


def _check_exact_object(actual: object, expected: object, path: str) -> None:
    if type(expected) is dict:
        if type(actual) is not dict:
            _fail(f"{path} expected table")
        actual_keys = set(actual)
        expected_keys = set(expected)
        if actual_keys != expected_keys:
            missing = sorted(expected_keys - actual_keys)
            extra = sorted(actual_keys - expected_keys)
            _fail(f"{path} key drift missing={missing} extra={extra}")
        for key in expected:
            _check_exact_object(actual[key], expected[key], f"{path}.{key}" if path else key)
        return
    if type(expected) is list:
        if type(actual) is not list:
            _fail(f"{path} expected array")
        if len(actual) != len(expected):
            _fail(f"{path} array length drift")
        for index, (actual_child, expected_child) in enumerate(zip(actual, expected, strict=True)):
            _check_exact_object(actual_child, expected_child, f"{path}[{index}]")
        return
    if type(actual) is not type(expected):
        _fail(f"{path} type drift")
    if actual != expected:
        _fail(f"{path} value drift")


def _frozen_config_object() -> dict[str, Any]:
    value = json.loads(_FROZEN_RESOURCE_CONFIG_JSON)
    if type(value) is not dict:
        _fail("compiled resource literal is not a table")
    return cast(dict[str, Any], value)


def _resource_config_from_object(value: Mapping[str, Any]) -> ResourceConfig:
    if type(value) is not dict:
        _fail("top-level object must be a built-in dict")
    expected = _frozen_config_object()
    _check_exact_object(value, expected, "")

    rows = _type_rows(cast(Mapping[str, object], value))
    if len(rows) != FROZEN_RESOURCE_CONFIG_TYPE_ROW_COUNT:
        _fail("type-row count drift")
    cjson_bytes = _type_tree_bytes(rows)
    type_tree_sha256 = hashlib.sha256(cjson_bytes).hexdigest()
    if type_tree_sha256 != FROZEN_RESOURCE_CONFIG_TYPE_TREE_SHA256:
        _fail("type-tree SHA256 drift")

    frozen = cast(FrozenResourceSection, _freeze(value))
    return ResourceConfig(
        raw_sha256=FROZEN_RESOURCE_CONFIG_SHA256,
        raw_byte_count=FROZEN_RESOURCE_CONFIG_BYTE_COUNT,
        type_rows=rows,
        type_tree_sha256=type_tree_sha256,
        cjson_bytes=cjson_bytes,
        schema_version=cast(int, frozen.schema_version),
        design_id=cast(str, frozen.design_id),
        gate=cast(str, frozen.gate),
        authority=cast(str, frozen.authority),
        entry_module=cast(str, frozen.entry_module),
        registered_make_target=cast(str, frozen.registered_make_target),
        rehearsal_make_target=cast(str, frozen.rehearsal_make_target),
        base_config=cast(str, frozen.base_config),
        base_config_sha256=cast(str, frozen.base_config_sha256),
        population_targets=cast(str, frozen.population_targets),
        population_targets_sha256=cast(str, frozen.population_targets_sha256),
        unknown_keys=cast(str, frozen.unknown_keys),
        roots=cast(FrozenResourceSection, frozen.roots),
        source=cast(FrozenResourceSection, frozen.source),
        runtime=cast(FrozenResourceSection, frozen.runtime),
        addresses=cast(FrozenResourceSection, frozen.addresses),
        kernels=cast(FrozenResourceSection, frozen.kernels),
        schedule=cast(FrozenResourceSection, frozen.schedule),
        terminal=cast(FrozenResourceSection, frozen.terminal),
        process=cast(FrozenResourceSection, frozen.process),
        hard_stops=cast(FrozenResourceSection, frozen.hard_stops),
        artifacts=cast(FrozenResourceSection, frozen.artifacts),
        replay=cast(FrozenResourceSection, frozen.replay),
        registries=cast(FrozenResourceSection, frozen.registries),
    )


def parse_resource_config_bytes(raw: bytes) -> ResourceConfig:
    """Validate exact resource-config bytes and return the frozen typed object."""

    if len(raw) != FROZEN_RESOURCE_CONFIG_BYTE_COUNT:
        _fail("byte count drift")
    if raw.startswith(b"\xef\xbb\xbf"):
        _fail("BOM is forbidden")
    if not raw.isascii():
        _fail("non-ASCII bytes are forbidden")
    if b"\r" in raw:
        _fail("carriage returns are forbidden")
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        _fail("file must end in exactly one LF")
    if hashlib.sha256(raw).hexdigest() != FROZEN_RESOURCE_CONFIG_SHA256:
        _fail("SHA256 drift")
    try:
        parsed = tomllib.loads(raw.decode("ascii"))
    except tomllib.TOMLDecodeError as error:
        _fail(f"TOML parse failed: {error}")
    return _resource_config_from_object(parsed)


def load_resource_config(root: Path) -> ResourceConfig:
    """Load the sealed resource config from ``root/configs/g2_resource.toml``."""

    return parse_resource_config_bytes(_config_path(root).read_bytes())
