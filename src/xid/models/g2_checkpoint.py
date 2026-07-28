"""Integrity-checked local checkpoints for sealed G2 smooth panel moments.

The codec persists only date-major sufficient statistics.  It deliberately
does not expose a generic authority-restoration hook: the stage-specific
wrappers in :mod:`xid.models.g2_smooth` reconstruct their exact panel types and
mint their weak-registry entries only after these decoders have validated the
complete local artifact.
"""

from __future__ import annotations

import fcntl
import hashlib
import importlib
import io
import json
import math
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import CodeType
from typing import cast

import numpy as np
from numpy.typing import NDArray

import xid.sim.g2 as g2_module
from xid.sim.g2 import (
    BaseProvenance,
    G2Component,
    G2Contract,
    G2DateReceipt,
    G2ResponseMapIdentity,
    G2RuntimeFingerprint,
    G2Stream,
    TestRngNamespace,
    current_g2_runtime_fingerprint,
    load_g2_contract,
    validate_g2_contract,
    validate_g2_date_receipt_metadata,
)


def _module_source_sha256() -> str:
    digest = hashlib.sha256()
    with Path(__file__).open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


_XID_LOADED_SOURCE_SHA256 = _module_source_sha256()

_SCHEMA_VERSION = 1
_SNAPSHOT_SCHEMA = "xid-g2-source-snapshot-v1"
_ARTIFACT_NAMESPACE = "xid-g2-panel-artifact-v1"
_LOCK_NAME = ".xid-g2-checkpoint.lock"
_MAX_TREE_BYTES = 2 * 1024**3
_MAX_MANIFEST_BYTES = 1024**2
_MAX_SUCCESS_BYTES = 16 * 1024
_MAX_PAYLOAD_BYTES = 5 * 1024**2
_MAX_NPY_HEADER_BYTES = 4096
_LICENSED_TEST_SEEDS = frozenset((1729, 9191))
_CONCRETE_PATH_TYPE = type(Path())
_THREAD_ENV_NAMES = (
    "BLIS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
)
_DECLARED_SOURCE_PATHS = (
    "src/xid",
    "configs/g2.toml",
    "configs/g2_population_targets.json",
    "pyproject.toml",
    "uv.lock",
    ".python-version",
    "Makefile",
)
_BASE_PAYLOAD_NAMES = ("x0tx0_upper.npy",)
_CELL_PAYLOAD_NAMES = ("x0ty.npy", "yty_upper.npy")
_MANIFEST_KEYS = frozenset(
    (
        "schema_version",
        "artifact_kind",
        "contract",
        "execution_source",
        "runtime",
        "address",
        "dimensions",
        "design_response_map",
        "response_map",
        "date_indices",
        "source_receipts",
        "design_receipts",
        "response_receipts",
        "design_sha256s",
        "parent",
        "payloads",
        "panel_token",
        "telemetry",
        "completion",
    )
)


@dataclass(frozen=True, slots=True)
class G2CheckpointTelemetry:
    """Resource counters that must survive deterministic recovery."""

    task_elapsed_seconds: float
    cumulative_elapsed_seconds: float
    peak_rss_bytes: int


@dataclass(frozen=True, slots=True)
class G2PanelCheckpointExpectation:
    """Caller-known coordinates for one complete base or response panel."""

    master_seed: int
    stream: G2Stream
    n_dates: int
    panel_index: int
    response_map: G2ResponseMapIdentity | None


@dataclass(frozen=True, slots=True)
class G2CheckpointEvidence:
    """Immutable evidence returned for one successfully decoded artifact."""

    artifact_path: Path
    artifact_sha256: str
    panel_token: str
    checkpoint_bytes: int
    telemetry: G2CheckpointTelemetry
    source_snapshot_sha256: str
    runtime_sha256: str


@dataclass(frozen=True, slots=True)
class G2CheckpointEnvironmentIdentity:
    """Validated execution identity for a checkpoint address without I/O."""

    source_snapshot_sha256: str
    runtime_sha256: str
    declared_paths_clean: bool


@dataclass(frozen=True, slots=True)
class _BasePanelWriteSnapshot:
    date_indices: tuple[int, ...]
    n_rows: int
    n_assets: int
    n_levels: int
    x0_width: int
    source_receipts: tuple[G2DateReceipt, ...]
    design_sha256s: tuple[str, ...]
    x0tx0_upper: NDArray[np.float64]
    panel_token: str


@dataclass(frozen=True, slots=True)
class _CellPanelWriteSnapshot:
    date_indices: tuple[int, ...]
    n_rows: int
    n_assets: int
    x0_width: int
    design_receipts: tuple[G2DateReceipt, ...]
    response_receipts: tuple[G2DateReceipt, ...]
    design_sha256s: tuple[str, ...]
    x0ty: NDArray[np.float64]
    yty_upper: NDArray[np.float64]
    base_panel_token: str
    cell_panel_token: str


@dataclass(frozen=True, slots=True)
class _DecodedBaseArtifact:
    evidence: G2CheckpointEvidence
    date_indices: tuple[int, ...]
    n_rows: int
    n_assets: int
    n_levels: int
    x0_width: int
    source_receipts: tuple[G2DateReceipt, ...]
    design_sha256s: tuple[str, ...]
    x0tx0_upper: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class _DecodedCellArtifact:
    evidence: G2CheckpointEvidence
    date_indices: tuple[int, ...]
    n_rows: int
    n_assets: int
    x0_width: int
    design_receipts: tuple[G2DateReceipt, ...]
    response_receipts: tuple[G2DateReceipt, ...]
    design_sha256s: tuple[str, ...]
    x0ty: NDArray[np.float64]
    yty_upper: NDArray[np.float64]
    parent_base_artifact_sha256: str
    parent_base_panel_token: str


@dataclass(frozen=True, slots=True)
class _SourceIdentity:
    snapshot_sha256: str
    git_commit: str
    declared_paths_clean: bool


@dataclass(frozen=True, slots=True)
class _RuntimeIdentity:
    payload: dict[str, object]
    runtime_sha256: str


@dataclass(frozen=True, slots=True)
class _CheckpointContext:
    expected: G2PanelCheckpointExpectation
    contract: G2Contract
    repository_root: Path
    source: _SourceIdentity
    runtime: _RuntimeIdentity
    design_response_map: G2ResponseMapIdentity


@dataclass(frozen=True, slots=True)
class _PayloadRecord:
    name: str
    payload: bytes
    descriptor: dict[str, object]


def _canonical_json_bytes(value: object) -> bytes:
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    except (TypeError, ValueError) as error:
        raise ValueError("checkpoint value is not canonical-JSON serializable") from error
    return encoded + b"\n"


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _require_sha256(value: object, *, name: str) -> str:
    if not _is_sha256(value):
        raise ValueError(f"{name} must be a lowercase SHA256 digest")
    return cast(str, value)


def _require_exact_keys(
    value: dict[str, object],
    expected: frozenset[str],
    *,
    name: str,
) -> None:
    if frozenset(value) != expected:
        raise ValueError(f"checkpoint {name} has an invalid key set")


def _json_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"checkpoint JSON contains duplicate key {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"checkpoint JSON contains invalid constant {value}")


def _parse_canonical_object(payload: bytes, *, name: str, maximum: int) -> dict[str, object]:
    if len(payload) > maximum:
        raise ValueError(f"checkpoint {name} exceeds its byte cap")
    try:
        text = payload.decode("ascii")
        value = json.loads(
            text,
            object_pairs_hook=_json_pairs,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"checkpoint {name} is invalid JSON") from error
    if type(value) is not dict:
        raise ValueError(f"checkpoint {name} must be a JSON object")
    result = cast(dict[str, object], value)
    if _canonical_json_bytes(result) != payload:
        raise ValueError(f"checkpoint {name} is not canonical JSON")
    return result


def _require_int(
    value: object,
    *,
    name: str,
    minimum: int = 0,
    maximum: int | None = None,
) -> int:
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{name} must be an exact Python integer in range")
    return value


def _require_bool(value: object, *, name: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{name} must be an exact JSON boolean")
    return value


def _require_exact_json_value(
    value: object,
    expected: object,
    *,
    name: str,
) -> None:
    if type(value) is not type(expected):
        raise ValueError(f"checkpoint {name} contains an invalid JSON type")
    if type(expected) is dict:
        observed_table = cast(dict[str, object], value)
        expected_table = cast(dict[str, object], expected)
        _require_exact_keys(observed_table, frozenset(expected_table), name=name)
        for key, expected_item in expected_table.items():
            _require_exact_json_value(
                observed_table[key],
                expected_item,
                name=f"{name}.{key}",
            )
        return
    if type(expected) is list:
        observed_items = cast(list[object], value)
        expected_items = cast(list[object], expected)
        if len(observed_items) != len(expected_items):
            raise ValueError(f"checkpoint {name} has an invalid array length")
        for index, (observed_item, expected_item) in enumerate(
            zip(observed_items, expected_items, strict=True)
        ):
            _require_exact_json_value(
                observed_item,
                expected_item,
                name=f"{name}[{index}]",
            )
        return
    if value != expected:
        raise ValueError(f"checkpoint {name} identity mismatch")


def _parse_hex_float(value: object, *, name: str, nonnegative: bool = False) -> float:
    if type(value) is not str:
        raise ValueError(f"{name} must be an exact binary64 hex string")
    try:
        parsed = float.fromhex(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an exact binary64 hex string") from error
    if not math.isfinite(parsed) or parsed.hex() != value:
        raise ValueError(f"{name} must use canonical finite binary64 hex")
    if nonnegative and (parsed < 0.0 or (parsed == 0.0 and math.copysign(1.0, parsed) < 0.0)):
        raise ValueError(f"{name} must be nonnegative without signed zero")
    return parsed


def _response_map_payload(response: G2ResponseMapIdentity) -> list[object]:
    _validate_response_map_representation(response, name="response map")
    return [
        response.target_index,
        response.paper_recovery,
        response.phi.hex(),
        response.reliability.hex(),
    ]


def _response_map_object(response: G2ResponseMapIdentity) -> dict[str, object]:
    return {
        "target_index": response.target_index,
        "paper_recovery": response.paper_recovery,
        "phi": response.phi.hex(),
        "reliability": response.reliability.hex(),
    }


def _parse_response_map(value: object, *, name: str) -> G2ResponseMapIdentity:
    if type(value) is not dict:
        raise ValueError(f"checkpoint {name} must be a response-map object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(("target_index", "paper_recovery", "phi", "reliability")),
        name=name,
    )
    return G2ResponseMapIdentity(
        target_index=_require_int(table["target_index"], name=f"{name}.target_index"),
        paper_recovery=_require_bool(
            table["paper_recovery"],
            name=f"{name}.paper_recovery",
        ),
        phi=_parse_hex_float(table["phi"], name=f"{name}.phi"),
        reliability=_parse_hex_float(table["reliability"], name=f"{name}.reliability"),
    )


def _validate_response_map_representation(
    response: G2ResponseMapIdentity,
    *,
    name: str,
) -> None:
    if type(response) is not G2ResponseMapIdentity:
        raise TypeError(f"{name} must use exact G2ResponseMapIdentity")
    if type(response.target_index) is not int:
        raise TypeError(f"{name} target_index must be an exact Python int")
    if type(response.paper_recovery) is not bool:
        raise TypeError(f"{name} paper_recovery must be an exact Python bool")
    if type(response.phi) is not float or not math.isfinite(response.phi):
        raise TypeError(f"{name} phi must be an exact finite Python float")
    if type(response.reliability) is not float or not math.isfinite(response.reliability):
        raise TypeError(f"{name} reliability must be an exact finite Python float")


def _validate_response_map_for_stream(
    response: G2ResponseMapIdentity,
    *,
    stream: G2Stream,
    contract: G2Contract,
    name: str,
) -> None:
    _validate_response_map_representation(response, name=name)
    if not 0 <= response.target_index < len(contract.population_targets):
        raise ValueError(f"{name} target index is outside the sealed grid")
    expected_phi = (
        contract.iid_ar1 if stream is G2Stream.VALIDATION_IID else contract.confirmatory_ar1
    )
    if response.phi != expected_phi:
        raise ValueError(f"{name} phi is not licensed by the stream")
    if response.reliability != contract.confirmatory_reliability:
        raise ValueError(f"{name} reliability is not the canonical checkpoint value")
    if response.paper_recovery and (
        stream not in (G2Stream.RESOURCE_PAPER, G2Stream.VALIDATION_PAPER_RECOVERY)
        or response.target_index != len(contract.population_targets) - 1
    ):
        raise ValueError(f"{name} paper-recovery identity is not licensed")
    if stream is G2Stream.VALIDATION_PAPER_RECOVERY and not response.paper_recovery:
        raise ValueError(f"{name} must use the paper-recovery identity")


def _design_response_map(
    stream: G2Stream,
    *,
    contract: G2Contract,
) -> G2ResponseMapIdentity:
    return G2ResponseMapIdentity(
        target_index=16,
        paper_recovery=stream is G2Stream.VALIDATION_PAPER_RECOVERY,
        phi=contract.iid_ar1 if stream is G2Stream.VALIDATION_IID else contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )


def _map_sha256(response: G2ResponseMapIdentity) -> str:
    return _sha256(_canonical_json_bytes(_response_map_payload(response)))


def _receipt_object(receipt: G2DateReceipt) -> dict[str, object]:
    provenance = receipt.provenance
    response = receipt.response_map
    return {
        "master_seed": provenance.master_seed,
        "stream": provenance.stream.value,
        "phase_id": provenance.phase_id,
        "scenario_id": provenance.scenario_id,
        "n_dates": provenance.n_dates,
        "panel_index": provenance.panel_index,
        "date_index": provenance.date_index,
        "base_identity": receipt.base_identity,
        "target_index": response.target_index,
        "paper_recovery": response.paper_recovery,
        "phi": response.phi.hex(),
        "reliability": response.reliability.hex(),
        "date_content_sha256": receipt.date_content_sha256,
    }


def _parse_receipt(value: object, *, contract: G2Contract, name: str) -> G2DateReceipt:
    if type(value) is not dict:
        raise ValueError(f"checkpoint {name} must be a receipt object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(
            (
                "master_seed",
                "stream",
                "phase_id",
                "scenario_id",
                "n_dates",
                "panel_index",
                "date_index",
                "base_identity",
                "target_index",
                "paper_recovery",
                "phi",
                "reliability",
                "date_content_sha256",
            )
        ),
        name=name,
    )
    stream_value = table["stream"]
    if type(stream_value) is not str:
        raise ValueError(f"checkpoint {name}.stream must be text")
    try:
        stream = G2Stream(stream_value)
    except ValueError as error:
        raise ValueError(f"checkpoint {name}.stream is unknown") from error
    receipt = G2DateReceipt(
        provenance=BaseProvenance(
            master_seed=_require_int(
                table["master_seed"],
                name=f"{name}.master_seed",
                maximum=2**32 - 1,
            ),
            stream=stream,
            phase_id=_require_int(
                table["phase_id"],
                name=f"{name}.phase_id",
                maximum=2**32 - 1,
            ),
            scenario_id=_require_int(
                table["scenario_id"],
                name=f"{name}.scenario_id",
                maximum=2**32 - 1,
            ),
            n_dates=_require_int(
                table["n_dates"],
                name=f"{name}.n_dates",
                maximum=2**32 - 1,
            ),
            panel_index=_require_int(
                table["panel_index"],
                name=f"{name}.panel_index",
                maximum=2**32 - 1,
            ),
            date_index=_require_int(
                table["date_index"],
                name=f"{name}.date_index",
                maximum=2**32 - 1,
            ),
        ),
        base_identity=_require_sha256(
            table["base_identity"],
            name=f"{name}.base_identity",
        ),
        response_map=G2ResponseMapIdentity(
            target_index=_require_int(
                table["target_index"],
                name=f"{name}.target_index",
            ),
            paper_recovery=_require_bool(
                table["paper_recovery"],
                name=f"{name}.paper_recovery",
            ),
            phi=_parse_hex_float(table["phi"], name=f"{name}.phi"),
            reliability=_parse_hex_float(
                table["reliability"],
                name=f"{name}.reliability",
            ),
        ),
        date_content_sha256=_require_sha256(
            table["date_content_sha256"],
            name=f"{name}.date_content_sha256",
        ),
    )
    validate_g2_date_receipt_metadata(
        receipt,
        contract,
        require_canonical_reliability=True,
    )
    return receipt


def _validate_receipts(
    receipts: Sequence[G2DateReceipt],
    *,
    expected: G2PanelCheckpointExpectation,
    response_map: G2ResponseMapIdentity,
    contract: G2Contract,
    name: str,
) -> tuple[G2DateReceipt, ...]:
    snapshot = tuple(receipts)
    if len(snapshot) != expected.n_dates:
        raise ValueError(f"checkpoint {name} does not contain every date")
    phase, scenario = contract.phase_scenario(expected.stream)
    for date_index, receipt in enumerate(snapshot):
        validate_g2_date_receipt_metadata(
            receipt,
            contract,
            require_canonical_reliability=True,
        )
        provenance = receipt.provenance
        if (
            provenance.master_seed != expected.master_seed
            or provenance.stream is not expected.stream
            or provenance.phase_id != phase
            or provenance.scenario_id != scenario
            or provenance.n_dates != expected.n_dates
            or provenance.panel_index != expected.panel_index
            or provenance.date_index != date_index
        ):
            raise ValueError(f"checkpoint {name} receipt coordinate mismatch")
        if receipt.response_map != response_map:
            raise ValueError(f"checkpoint {name} response-map identity mismatch")
    return snapshot


def _run_git_text(repository_root: Path, arguments: Sequence[str]) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repository_root,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return completed.stdout


def _stable_source_file_identity(path: Path) -> tuple[os.stat_result, int, str]:
    try:
        path_before = os.lstat(path)
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as error:
        raise ValueError("execution-source file disappeared during snapshot") from error
    try:
        descriptor_before = os.fstat(descriptor)
        if (
            stat.S_ISLNK(path_before.st_mode)
            or not stat.S_ISREG(path_before.st_mode)
            or not stat.S_ISREG(descriptor_before.st_mode)
            or (path_before.st_dev, path_before.st_ino)
            != (descriptor_before.st_dev, descriptor_before.st_ino)
        ):
            raise ValueError("execution-source entries must be regular non-symlink files")
        digest = hashlib.sha256()
        byte_count = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            byte_count += len(chunk)
        descriptor_after = os.fstat(descriptor)
        path_after = os.lstat(path)
    except OSError as error:
        raise ValueError("execution-source file changed during snapshot") from error
    finally:
        os.close(descriptor)
    stable_fields_before = (
        descriptor_before.st_dev,
        descriptor_before.st_ino,
        descriptor_before.st_size,
        descriptor_before.st_mtime_ns,
        descriptor_before.st_ctime_ns,
        descriptor_before.st_mode,
    )
    stable_fields_after = (
        descriptor_after.st_dev,
        descriptor_after.st_ino,
        descriptor_after.st_size,
        descriptor_after.st_mtime_ns,
        descriptor_after.st_ctime_ns,
        descriptor_after.st_mode,
    )
    stable_path_after = (
        path_after.st_dev,
        path_after.st_ino,
        path_after.st_size,
        path_after.st_mtime_ns,
        path_after.st_ctime_ns,
        path_after.st_mode,
    )
    if (
        stable_fields_before != stable_fields_after
        or stable_fields_after != stable_path_after
        or byte_count != descriptor_after.st_size
    ):
        raise ValueError("execution-source file changed during snapshot")
    return descriptor_after, byte_count, digest.hexdigest()


def _stable_source_bytes(path: Path, *, maximum: int = 8 * 1024**2) -> bytes:
    flags = os.O_RDONLY | os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("execution-source file cannot be opened safely") from error
    try:
        descriptor_before = os.fstat(descriptor)
        path_before = os.lstat(path)
        if (
            stat.S_ISLNK(path_before.st_mode)
            or not stat.S_ISREG(descriptor_before.st_mode)
            or descriptor_before.st_size > maximum
        ):
            raise ValueError("execution-source file is not a bounded regular file")
        chunks: list[bytes] = []
        byte_count = 0
        while chunk := os.read(descriptor, 1024 * 1024):
            byte_count += len(chunk)
            if byte_count > maximum:
                raise ValueError("execution-source file exceeds its compile-time cap")
            chunks.append(chunk)
        descriptor_after = os.fstat(descriptor)
        path_after = os.lstat(path)
    finally:
        os.close(descriptor)
    stable_descriptor_before = (
        descriptor_before.st_dev,
        descriptor_before.st_ino,
        descriptor_before.st_size,
        descriptor_before.st_mtime_ns,
        descriptor_before.st_ctime_ns,
        descriptor_before.st_mode,
    )
    stable_descriptor_after = (
        descriptor_after.st_dev,
        descriptor_after.st_ino,
        descriptor_after.st_size,
        descriptor_after.st_mtime_ns,
        descriptor_after.st_ctime_ns,
        descriptor_after.st_mode,
    )
    stable_path_after = (
        path_after.st_dev,
        path_after.st_ino,
        path_after.st_size,
        path_after.st_mtime_ns,
        path_after.st_ctime_ns,
        path_after.st_mode,
    )
    if (
        stable_descriptor_before != stable_descriptor_after
        or stable_descriptor_after != stable_path_after
        or byte_count != descriptor_after.st_size
    ):
        raise ValueError("execution-source file changed during compilation snapshot")
    return b"".join(chunks)


def _validate_loader_code_matches_source(module: object, path: Path) -> None:
    loader = getattr(module, "__loader__", None)
    module_name = getattr(module, "__name__", None)
    get_code = getattr(loader, "get_code", None)
    source_to_code = getattr(loader, "source_to_code", None)
    if type(module_name) is not str or not callable(get_code) or not callable(source_to_code):
        raise ValueError("imported G2 module loader cannot attest executable code")
    loaded_code = get_code(module_name)
    source_bytes = _stable_source_bytes(path)
    fresh_code = source_to_code(source_bytes, str(path))
    if type(loaded_code) is not CodeType or type(fresh_code) is not CodeType:
        raise ValueError("imported G2 module loader returned no executable code")
    if loaded_code != fresh_code:
        raise ValueError("imported G2 module bytecode differs from current source")


def _exact_repository_root(repository_root: Path) -> Path:
    if type(repository_root) is not _CONCRETE_PATH_TYPE:
        raise TypeError("repository_root must use the exact concrete pathlib path type")
    try:
        supplied_stat = os.lstat(repository_root)
    except OSError as error:
        raise ValueError("repository root does not exist") from error
    if stat.S_ISLNK(supplied_stat.st_mode) or not stat.S_ISDIR(supplied_stat.st_mode):
        raise ValueError("repository root must be a non-symlink directory")
    try:
        supplied = repository_root.resolve(strict=True)
        git_top = Path(
            _run_git_text(repository_root, ("rev-parse", "--show-toplevel")).strip()
        ).resolve(strict=True)
    except (OSError, subprocess.CalledProcessError) as error:
        raise ValueError("repository root is not a valid Git worktree") from error
    if supplied != git_top:
        raise ValueError("supplied repository root does not equal the Git top level")
    return supplied


def _source_snapshot(repository_root: Path) -> _SourceIdentity:
    command = [
        "git",
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        *_DECLARED_SOURCE_PATHS,
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=repository_root,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as error:
        raise ValueError("execution-source enumeration failed") from error
    entries = completed.stdout.split(b"\0")
    if entries and entries[-1] == b"":
        entries.pop()
    normalized_paths: list[str] = []
    seen: set[str] = set()
    for raw_path in entries:
        try:
            path_text = raw_path.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("execution-source path is not valid UTF-8") from error
        if unicodedata.normalize("NFC", path_text) != path_text:
            raise ValueError("execution-source path is not NFC-normalized")
        pure_path = PurePosixPath(path_text)
        if (
            pure_path.is_absolute()
            or not pure_path.parts
            or any(part in ("", ".", "..") for part in pure_path.parts)
            or "\\" in path_text
        ):
            raise ValueError("execution-source path is not a safe relative POSIX path")
        if path_text in seen:
            raise ValueError("execution-source enumeration contains a duplicate path")
        seen.add(path_text)
        normalized_paths.append(path_text)
    required_files = frozenset(_DECLARED_SOURCE_PATHS[1:])
    if not required_files.issubset(seen) or not any(
        path == "src/xid" or path.startswith("src/xid/") for path in seen
    ):
        raise ValueError("execution-source snapshot is missing a declared path")
    digest = hashlib.sha256(b"xid-g2-source-snapshot-v1\n")
    for path_text in sorted(normalized_paths, key=lambda value: value.encode("utf-8")):
        path = repository_root.joinpath(*PurePosixPath(path_text).parts)
        file_stat, byte_count, file_sha256 = _stable_source_file_identity(path)
        mode = "100755" if file_stat.st_mode & 0o111 else "100644"
        digest.update(
            _canonical_json_bytes(
                [path_text, mode, byte_count, file_sha256],
            )
        )
    try:
        git_commit = _run_git_text(repository_root, ("rev-parse", "HEAD")).strip()
        dirty = _run_git_text(
            repository_root,
            (
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--",
                *_DECLARED_SOURCE_PATHS,
            ),
        )
    except subprocess.CalledProcessError as error:
        raise ValueError("execution-source Git identity failed") from error
    if len(git_commit) not in (40, 64) or any(
        character not in "0123456789abcdef" for character in git_commit
    ):
        raise ValueError("execution-source Git commit is not a lowercase object digest")
    return _SourceIdentity(
        snapshot_sha256=digest.hexdigest(),
        git_commit=git_commit,
        declared_paths_clean=dirty == "",
    )


def _validate_module_origins(repository_root: Path) -> None:
    smooth_module = importlib.import_module("xid.models.g2_smooth")
    expected_modules = (
        (g2_module, repository_root / "src/xid/sim/g2.py"),
        (smooth_module, repository_root / "src/xid/models/g2_smooth.py"),
        (sys.modules[__name__], repository_root / "src/xid/models/g2_checkpoint.py"),
    )
    for module, expected_path in expected_modules:
        module_file = getattr(module, "__file__", None)
        if type(module_file) is not str:
            raise ValueError("imported G2 module has no exact source file")
        path = Path(module_file)
        try:
            path_stat = os.lstat(path)
            resolved = path.resolve(strict=True)
            expected = expected_path.resolve(strict=True)
        except OSError as error:
            raise ValueError("imported G2 module does not resolve inside the repository") from error
        if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISREG(path_stat.st_mode):
            raise ValueError("imported G2 module source must be a regular non-symlink file")
        if resolved != expected:
            raise ValueError("imported G2 module is stale or from another repository")
        loaded_sha256 = getattr(module, "_XID_LOADED_SOURCE_SHA256", None)
        _file_stat, _byte_count, current_sha256 = _stable_source_file_identity(path)
        if not _is_sha256(loaded_sha256) or loaded_sha256 != current_sha256:
            raise ValueError("imported G2 module source changed after it was loaded")
        _validate_loader_code_matches_source(module, path)


def _runtime_fingerprint_payload(fingerprint: G2RuntimeFingerprint) -> dict[str, object]:
    if type(fingerprint) is not G2RuntimeFingerprint:
        raise TypeError("runtime fingerprint must use exact G2RuntimeFingerprint")
    return {
        "python_implementation": fingerprint.python_implementation,
        "python_version": fingerprint.python_version,
        "numpy_version": fingerprint.numpy_version,
        "system": fingerprint.system,
        "machine": fingerprint.machine,
        "byteorder": fingerprint.byteorder,
        "rng_runtime_sha256": fingerprint.rng_runtime_sha256,
    }


def _runtime_identity() -> _RuntimeIdentity:
    fingerprint_payload = _runtime_fingerprint_payload(current_g2_runtime_fingerprint())
    thread_env: dict[str, object] = {name: os.environ.get(name) for name in _THREAD_ENV_NAMES}
    payload = {**fingerprint_payload, "thread_env": thread_env}
    return _RuntimeIdentity(
        payload=payload,
        runtime_sha256=_sha256(
            _canonical_json_bytes(
                [fingerprint_payload, thread_env],
            )
        ),
    )


def _validate_expectation_and_authority(
    expected: G2PanelCheckpointExpectation,
    *,
    contract: G2Contract,
    authority: TestRngNamespace,
    artifact_kind: str,
) -> G2ResponseMapIdentity:
    if type(expected) is not G2PanelCheckpointExpectation:
        raise TypeError("checkpoint expected identity must use exact expectation type")
    if type(contract) is not G2Contract:
        raise TypeError("checkpoint contract must use exact G2Contract")
    if type(authority) is not TestRngNamespace:
        raise TypeError("checkpoint authority requires exact TestRngNamespace")
    TestRngNamespace._validate_authority(authority)
    validate_g2_contract(contract)
    if authority.contract is not contract:
        raise ValueError("checkpoint authority must reference the exact current contract")
    if authority.master_seed not in _LICENSED_TEST_SEEDS:
        raise ValueError("checkpoint authority accepts only a licensed test seed")
    if type(expected.master_seed) is not int or expected.master_seed != authority.master_seed:
        raise ValueError("checkpoint expected seed does not match its authority")
    if type(expected.stream) is not G2Stream:
        raise TypeError("checkpoint expected stream must use exact G2Stream")
    if type(expected.n_dates) is not int or not 1 <= expected.n_dates < 2**32:
        raise ValueError("checkpoint expected date count must be a positive uint32")
    if type(expected.panel_index) is not int or not 0 <= expected.panel_index < 2**32:
        raise ValueError("checkpoint expected panel index must be a uint32")
    if artifact_kind == "base-panel":
        if expected.response_map is not None:
            raise ValueError("base checkpoint expectation cannot carry a response map")
    elif artifact_kind == "cell-panel":
        if expected.response_map is None:
            raise ValueError("cell checkpoint expectation requires a response map")
        _validate_response_map_for_stream(
            expected.response_map,
            stream=expected.stream,
            contract=contract,
            name="expected response map",
        )
    else:
        raise ValueError("unknown checkpoint artifact kind")
    for date_index in (0, expected.n_dates - 1):
        authority.dgp_address(
            stream=expected.stream,
            n_dates=expected.n_dates,
            panel_index=expected.panel_index,
            date_index=date_index,
            component=G2Component.FACTOR,
        )
    design_response_map = _design_response_map(expected.stream, contract=contract)
    _validate_response_map_for_stream(
        design_response_map,
        stream=expected.stream,
        contract=contract,
        name="design response map",
    )
    return design_response_map


def _checkpoint_context(
    expected: G2PanelCheckpointExpectation,
    *,
    contract: G2Contract,
    authority: TestRngNamespace,
    repository_root: Path,
    artifact_kind: str,
) -> _CheckpointContext:
    design_response_map = _validate_expectation_and_authority(
        expected,
        contract=contract,
        authority=authority,
        artifact_kind=artifact_kind,
    )
    rooted_repository = _exact_repository_root(repository_root)
    source_before = _source_snapshot(rooted_repository)
    loaded_contract = load_g2_contract(rooted_repository)
    source_after = _source_snapshot(rooted_repository)
    if source_before != source_after:
        raise ValueError("execution source changed while loading the sealed contract")
    if loaded_contract != contract:
        raise ValueError("checkpoint contract differs from the rooted sealed contract")
    _validate_module_origins(rooted_repository)
    return _CheckpointContext(
        expected=expected,
        contract=contract,
        repository_root=rooted_repository,
        source=source_after,
        runtime=_runtime_identity(),
        design_response_map=design_response_map,
    )


def inspect_g2_checkpoint_environment(
    *,
    expected: G2PanelCheckpointExpectation,
    contract: G2Contract,
    authority: TestRngNamespace,
    repository_root: Path,
) -> G2CheckpointEnvironmentIdentity:
    """Validate one base-panel address and return its bound source/runtime identity."""
    context = _checkpoint_context(
        expected,
        contract=contract,
        authority=authority,
        repository_root=repository_root,
        artifact_kind="base-panel",
    )
    return G2CheckpointEnvironmentIdentity(
        source_snapshot_sha256=context.source.snapshot_sha256,
        runtime_sha256=context.runtime.runtime_sha256,
        declared_paths_clean=context.source.declared_paths_clean,
    )


def _assert_context_stable(context: _CheckpointContext) -> None:
    _validate_module_origins(context.repository_root)
    if _source_snapshot(context.repository_root).snapshot_sha256 != context.source.snapshot_sha256:
        raise ValueError("checkpoint execution source changed during operation")
    if _runtime_identity() != context.runtime:
        raise ValueError("checkpoint numerical runtime or thread environment changed")


def _validate_checkpoint_root(checkpoint_root: Path, repository_root: Path) -> Path:
    if type(checkpoint_root) is not _CONCRETE_PATH_TYPE:
        raise TypeError("checkpoint root must use the exact concrete pathlib path type")
    try:
        root_stat = os.lstat(checkpoint_root)
    except OSError as error:
        raise ValueError("checkpoint root must already exist") from error
    if stat.S_ISLNK(root_stat.st_mode):
        raise ValueError("checkpoint root cannot be a symlink")
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError("checkpoint root must be a directory")
    root = checkpoint_root.resolve(strict=True)
    for relative in _DECLARED_SOURCE_PATHS:
        source_path = (repository_root / relative).resolve(strict=True)
        if (
            root == source_path
            or root.is_relative_to(source_path)
            or source_path.is_relative_to(root)
        ):
            raise ValueError("checkpoint root must be disjoint from execution-source paths")
    return root


def _artifact_relative_path(
    expected: G2PanelCheckpointExpectation,
    *,
    design_response_map: G2ResponseMapIdentity,
    artifact_kind: str,
    base_artifact_sha256: str | None = None,
) -> Path:
    prefix = Path(
        "panel-v1",
        expected.stream.value,
        f"seed-{expected.master_seed:010d}",
        f"dates-{expected.n_dates:03d}",
        f"panel-{expected.panel_index:010d}",
    )
    if artifact_kind == "base-panel":
        return prefix / f"base-{_map_sha256(design_response_map)}"
    if artifact_kind != "cell-panel" or expected.response_map is None:
        raise ValueError("invalid checkpoint path request")
    parent_digest = _require_sha256(
        base_artifact_sha256,
        name="parent base artifact digest",
    )
    return prefix / f"cell-{_map_sha256(expected.response_map)}-parent-{parent_digest}"


def _validate_existing_directory(path: Path, *, name: str) -> None:
    path_stat = os.lstat(path)
    if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISDIR(path_stat.st_mode):
        raise ValueError(f"checkpoint {name} must be a non-symlink directory")


def _ensure_parent_directories(root: Path, relative_parent: Path) -> Path:
    current = root
    for part in relative_parent.parts:
        parent = current
        current = parent / part
        try:
            _validate_existing_directory(current, name="path component")
        except FileNotFoundError:
            os.mkdir(current, mode=0o700)
            _validate_existing_directory(current, name="path component")
            _fsync_directory(current)
            _fsync_directory(parent)
            _enforce_tree_cap(root)
    return current


def _path_usage(path: Path) -> tuple[int, int]:
    logical = 0
    allocated = 0
    stack = [path]
    while stack:
        current = stack.pop()
        current_stat = os.lstat(current)
        if stat.S_ISLNK(current_stat.st_mode):
            raise ValueError("checkpoint tree contains a symlink")
        logical += current_stat.st_size
        allocated += current_stat.st_blocks * 512
        if stat.S_ISDIR(current_stat.st_mode):
            with os.scandir(current) as entries:
                stack.extend(Path(entry.path) for entry in entries)
        elif not stat.S_ISREG(current_stat.st_mode):
            raise ValueError("checkpoint tree contains a non-regular file")
    return logical, allocated


def _enforce_tree_cap(root: Path) -> None:
    logical, allocated = _path_usage(root)
    if max(logical, allocated) > _MAX_TREE_BYTES:
        raise ValueError("checkpoint tree exceeds the sealed 2 GB allocation cap")


def _round_up(value: int, quantum: int) -> int:
    if type(value) is not int or value < 0:
        raise TypeError("checkpoint projected byte count must be a nonnegative int")
    if type(quantum) is not int or quantum <= 0:
        raise TypeError("checkpoint allocation quantum must be a positive int")
    return ((value + quantum - 1) // quantum) * quantum


def _allocation_quantum(root: Path) -> int:
    filesystem = os.statvfs(root)
    return max(
        512,
        int(filesystem.f_frsize),
        int(filesystem.f_bsize),
    )


def _reserve_tree_capacity(
    root: Path,
    payloads: tuple[bytes, ...],
    *,
    future_entry_units: int,
    operation: str,
) -> None:
    """Conservatively reserve payload and directory growth before mutation."""
    if type(payloads) is not tuple or any(type(payload) is not bytes for payload in payloads):
        raise TypeError("checkpoint capacity reservation requires an exact bytes tuple")
    if type(future_entry_units) is not int or future_entry_units < 0:
        raise TypeError("checkpoint future entry units must be a nonnegative exact int")
    if type(operation) is not str or not operation:
        raise TypeError("checkpoint capacity operation must be a nonempty exact str")
    logical, allocated = _path_usage(root)
    allocation_quantum = _allocation_quantum(root)
    entry_reservation = future_entry_units * allocation_quantum
    projected_logical = logical + sum(len(payload) for payload in payloads) + entry_reservation
    projected_allocated = (
        allocated
        + sum(_round_up(len(payload), allocation_quantum) for payload in payloads)
        + entry_reservation
    )
    if max(projected_logical, projected_allocated) > _MAX_TREE_BYTES:
        raise ValueError(f"checkpoint projected {operation} exceeds the sealed 2 GB allocation cap")


def _reserve_stage_capacity(root: Path, payloads: tuple[bytes, ...]) -> None:
    """Reject a complete staged publication before writing its first artifact."""
    _reserve_tree_capacity(
        root,
        payloads,
        future_entry_units=len(payloads),
        operation="stage",
    )


def _missing_parent_directory_count(root: Path, relative_parent: Path) -> int:
    current = root
    missing = 0
    for part in relative_parent.parts:
        current = current / part
        if missing:
            missing += 1
            continue
        try:
            _validate_existing_directory(current, name="path component")
        except FileNotFoundError:
            missing = 1
    return missing


def _write_file(path: Path, payload: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    file_descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(payload)
        written = 0
        while written < len(view):
            count = os.write(file_descriptor, view[written:])
            if count <= 0:
                raise OSError("checkpoint file write made no progress")
            written += count
        os.fsync(file_descriptor)
    finally:
        os.close(file_descriptor)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _acquire_root_lock(root: Path, *, final_relative_path: Path) -> tuple[Path, int]:
    lock_path = root / _LOCK_NAME
    payload = _canonical_json_bytes(
        {
            "schema_version": _SCHEMA_VERSION,
            "pid": os.getpid(),
            "final_relative_path": final_relative_path.as_posix(),
        }
    )
    root_descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(root_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise FileExistsError("checkpoint reader or writer lease already exists") from error
        _reserve_tree_capacity(
            root,
            (payload,),
            future_entry_units=1,
            operation="writer lock",
        )
        try:
            _write_file(lock_path, payload)
        except FileExistsError as error:
            raise FileExistsError("checkpoint writer lock already exists") from error
        _enforce_tree_cap(root)
        _fsync_directory(root)
        return lock_path, root_descriptor
    except BaseException:
        try:
            fcntl.flock(root_descriptor, fcntl.LOCK_UN)
        finally:
            os.close(root_descriptor)
        raise


def _release_root_lock(
    root: Path,
    lease: tuple[Path, int],
    *,
    remove_marker: bool,
) -> None:
    lock_path, root_descriptor = lease
    try:
        if remove_marker:
            lock_path.unlink()
            _fsync_directory(root)
    finally:
        try:
            fcntl.flock(root_descriptor, fcntl.LOCK_UN)
        finally:
            os.close(root_descriptor)


def _require_no_root_lock(root: Path) -> None:
    if os.path.lexists(root / _LOCK_NAME):
        raise FileExistsError("checkpoint writer lock blocks artifact loading")


@contextmanager
def _checkpoint_load_guard(
    checkpoint_root: Path,
    repository_root: Path,
    *,
    expected: G2PanelCheckpointExpectation,
    contract: G2Contract,
    authority: TestRngNamespace,
    artifact_kind: str,
) -> Iterator[None]:
    """Hold a shared root lease through stage-specific authority restoration."""
    _validate_expectation_and_authority(
        expected,
        contract=contract,
        authority=authority,
        artifact_kind=artifact_kind,
    )
    rooted_repository = _exact_repository_root(repository_root)
    root = _validate_checkpoint_root(checkpoint_root, rooted_repository)
    root_descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(root_descriptor, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise FileExistsError("checkpoint writer lease blocks artifact loading") from error
        _require_no_root_lock(root)
        yield
        _require_no_root_lock(root)
    finally:
        try:
            fcntl.flock(root_descriptor, fcntl.LOCK_UN)
        finally:
            os.close(root_descriptor)


def _validate_telemetry(telemetry: G2CheckpointTelemetry) -> None:
    if type(telemetry) is not G2CheckpointTelemetry:
        raise TypeError("checkpoint telemetry must use exact G2CheckpointTelemetry")
    for name, value in (
        ("task elapsed seconds", telemetry.task_elapsed_seconds),
        ("cumulative elapsed seconds", telemetry.cumulative_elapsed_seconds),
    ):
        if type(value) is not float or not math.isfinite(value):
            raise TypeError(f"checkpoint {name} must be an exact finite Python float")
        if value < 0.0 or (value == 0.0 and math.copysign(1.0, value) < 0.0):
            raise ValueError(f"checkpoint {name} must be nonnegative without signed zero")
    if telemetry.cumulative_elapsed_seconds < telemetry.task_elapsed_seconds:
        raise ValueError("checkpoint cumulative elapsed seconds cannot be below task time")
    if type(telemetry.peak_rss_bytes) is not int or telemetry.peak_rss_bytes < 0:
        raise ValueError("checkpoint peak RSS bytes must be a nonnegative integer")


def _telemetry_object(telemetry: G2CheckpointTelemetry) -> dict[str, object]:
    _validate_telemetry(telemetry)
    return {
        "task_elapsed_seconds": telemetry.task_elapsed_seconds.hex(),
        "cumulative_elapsed_seconds": telemetry.cumulative_elapsed_seconds.hex(),
        "peak_rss_bytes": telemetry.peak_rss_bytes,
    }


def _parse_telemetry(value: object) -> G2CheckpointTelemetry:
    if type(value) is not dict:
        raise ValueError("checkpoint telemetry must be an object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(
            (
                "task_elapsed_seconds",
                "cumulative_elapsed_seconds",
                "peak_rss_bytes",
            )
        ),
        name="telemetry",
    )
    telemetry = G2CheckpointTelemetry(
        task_elapsed_seconds=_parse_hex_float(
            table["task_elapsed_seconds"],
            name="checkpoint telemetry task elapsed seconds",
            nonnegative=True,
        ),
        cumulative_elapsed_seconds=_parse_hex_float(
            table["cumulative_elapsed_seconds"],
            name="checkpoint telemetry cumulative elapsed seconds",
            nonnegative=True,
        ),
        peak_rss_bytes=_require_int(
            table["peak_rss_bytes"],
            name="checkpoint telemetry peak RSS bytes",
        ),
    )
    _validate_telemetry(telemetry)
    return telemetry


def _validate_panel_dimensions(
    *,
    date_indices: tuple[int, ...],
    n_rows: int,
    n_assets: int,
    n_levels: int | None,
    x0_width: int,
    context: _CheckpointContext,
) -> None:
    expected = context.expected
    contract = context.contract
    if (
        type(date_indices) is not tuple
        or date_indices != tuple(range(expected.n_dates))
        or any(type(value) is not int for value in date_indices)
    ):
        raise ValueError("checkpoint date indices must be one complete ordered panel")
    if type(n_rows) is not int or n_rows != contract.bins_per_date:
        raise ValueError("checkpoint row dimension differs from the sealed contract")
    if type(n_assets) is not int or n_assets != contract.n_assets:
        raise ValueError("checkpoint asset dimension differs from the sealed contract")
    if n_levels is not None and (type(n_levels) is not int or n_levels != contract.n_levels):
        raise ValueError("checkpoint level dimension differs from the sealed contract")
    if type(x0_width) is not int or x0_width != 3 + 2 * contract.n_assets:
        raise ValueError("checkpoint X0 width differs from the sealed design")


def _validate_writer_array(
    values: NDArray[np.float64],
    *,
    shape: tuple[int, ...],
    name: str,
) -> None:
    if type(values) is not np.ndarray or values.dtype != np.dtype("<f8"):
        raise TypeError(f"checkpoint {name} must be an exact little-endian float64 ndarray")
    if values.shape != shape or not values.flags.c_contiguous:
        raise ValueError(f"checkpoint {name} has invalid shape or C order")
    if values.flags.writeable:
        raise ValueError(f"checkpoint {name} must be read-only before serialization")
    if not np.all(np.isfinite(values)):
        raise ValueError(f"checkpoint {name} contains a nonfinite value")


def _npy_payload(
    name: str,
    values: NDArray[np.float64],
    *,
    shape: tuple[int, ...],
) -> _PayloadRecord:
    _validate_writer_array(values, shape=shape, name=name)
    output = io.BytesIO()
    np.lib.format.write_array(
        output,
        values,
        version=(1, 0),
        allow_pickle=False,
    )
    payload = output.getvalue()
    expected_data_bytes = math.prod(shape) * 8
    if len(payload) > expected_data_bytes + _MAX_NPY_HEADER_BYTES:
        raise ValueError(f"checkpoint NPY payload {name} has an oversized header")
    return _PayloadRecord(
        name=name,
        payload=payload,
        descriptor={
            "name": name,
            "npy_format": "1.0",
            "dtype": "<f8",
            "shape": list(shape),
            "data_bytes": expected_data_bytes,
            "file_bytes": len(payload),
            "sha256": _sha256(payload),
        },
    )


def _contract_object(contract: G2Contract) -> dict[str, object]:
    seals = contract.seals
    return {
        "config_schema_version": contract.config_schema_version,
        "target_schema_version": contract.target_schema_version,
        "target_config_schema_version": contract.target_config_schema_version,
        "rng_key_schema_version": contract.rng_key_schema_version,
        "design_id": contract.design_id,
        "target_design_id": contract.target_design_id,
        "seals": {
            "config_sha256": seals.config_sha256,
            "target_raw_sha256": seals.target_raw_sha256,
            "target_semantic_sha256": seals.target_semantic_sha256,
            "lasso_ratio_sha256": seals.lasso_ratio_sha256,
        },
    }


def _source_object(source: _SourceIdentity) -> dict[str, object]:
    return {
        "snapshot_schema": _SNAPSHOT_SCHEMA,
        "snapshot_sha256": source.snapshot_sha256,
        "git_commit": source.git_commit,
        "declared_paths_clean": source.declared_paths_clean,
    }


def _runtime_object(runtime: _RuntimeIdentity) -> dict[str, object]:
    return {**runtime.payload, "runtime_sha256": runtime.runtime_sha256}


def _address_object(context: _CheckpointContext) -> dict[str, object]:
    expected = context.expected
    phase, scenario = context.contract.phase_scenario(expected.stream)
    return {
        "master_seed": expected.master_seed,
        "config_schema_version": context.contract.config_schema_version,
        "rng_key_schema_version": context.contract.rng_key_schema_version,
        "stream": expected.stream.value,
        "phase_id": phase,
        "scenario_id": scenario,
        "parent_phase_id": 0,
        "parent_scenario_id": 0,
        "n_dates": expected.n_dates,
        "panel_index": expected.panel_index,
        "cell_key": 0,
        "component_ids": [1, 2, 3, 4, 5],
        "replicate_index": 0,
        "completed_date_range": [0, expected.n_dates],
        "completed_replicate_range": None,
    }


def _completion_object(n_dates: int) -> dict[str, object]:
    return {
        "completed_date_range": [0, n_dates],
        "completed_replicate_range": None,
    }


def _base_manifest(
    *,
    context: _CheckpointContext,
    telemetry: G2CheckpointTelemetry,
    date_indices: tuple[int, ...],
    n_rows: int,
    n_assets: int,
    n_levels: int,
    x0_width: int,
    source_receipts: tuple[G2DateReceipt, ...],
    design_sha256s: tuple[str, ...],
    payload: _PayloadRecord,
    panel_token: str,
) -> dict[str, object]:
    return {
        "schema_version": _SCHEMA_VERSION,
        "artifact_kind": "base-panel",
        "contract": _contract_object(context.contract),
        "execution_source": _source_object(context.source),
        "runtime": _runtime_object(context.runtime),
        "address": _address_object(context),
        "dimensions": {
            "n_rows": n_rows,
            "n_assets": n_assets,
            "n_levels": n_levels,
            "x0_width": x0_width,
        },
        "design_response_map": _response_map_object(context.design_response_map),
        "response_map": None,
        "date_indices": list(date_indices),
        "source_receipts": [_receipt_object(receipt) for receipt in source_receipts],
        "design_receipts": None,
        "response_receipts": None,
        "design_sha256s": list(design_sha256s),
        "parent": None,
        "payloads": [payload.descriptor],
        "panel_token": panel_token,
        "telemetry": _telemetry_object(telemetry),
        "completion": _completion_object(context.expected.n_dates),
    }


def _cell_manifest(
    *,
    context: _CheckpointContext,
    base_checkpoint: G2CheckpointEvidence,
    telemetry: G2CheckpointTelemetry,
    date_indices: tuple[int, ...],
    n_rows: int,
    n_assets: int,
    x0_width: int,
    design_receipts: tuple[G2DateReceipt, ...],
    response_receipts: tuple[G2DateReceipt, ...],
    design_sha256s: tuple[str, ...],
    payloads: tuple[_PayloadRecord, _PayloadRecord],
    panel_token: str,
) -> dict[str, object]:
    response_map = context.expected.response_map
    if response_map is None:
        raise ValueError("cell checkpoint response map disappeared")
    return {
        "schema_version": _SCHEMA_VERSION,
        "artifact_kind": "cell-panel",
        "contract": _contract_object(context.contract),
        "execution_source": _source_object(context.source),
        "runtime": _runtime_object(context.runtime),
        "address": _address_object(context),
        "dimensions": {
            "n_rows": n_rows,
            "n_assets": n_assets,
            "n_levels": context.contract.n_levels,
            "x0_width": x0_width,
        },
        "design_response_map": _response_map_object(context.design_response_map),
        "response_map": _response_map_object(response_map),
        "date_indices": list(date_indices),
        "source_receipts": None,
        "design_receipts": [_receipt_object(receipt) for receipt in design_receipts],
        "response_receipts": [_receipt_object(receipt) for receipt in response_receipts],
        "design_sha256s": list(design_sha256s),
        "parent": {
            "base_artifact_sha256": base_checkpoint.artifact_sha256,
            "base_panel_token": base_checkpoint.panel_token,
        },
        "payloads": [payload.descriptor for payload in payloads],
        "panel_token": panel_token,
        "telemetry": _telemetry_object(telemetry),
        "completion": _completion_object(context.expected.n_dates),
    }


def _artifact_sha256(
    artifact_kind: str,
    manifest_sha256: str,
    payloads: Sequence[_PayloadRecord] | Sequence[tuple[str, str]],
) -> str:
    payload_pairs: list[list[str]] = []
    for payload in payloads:
        if isinstance(payload, _PayloadRecord):
            payload_pairs.append(
                [payload.name, cast(str, payload.descriptor["sha256"])],
            )
        else:
            name, digest = payload
            payload_pairs.append([name, digest])
    return _sha256(
        _canonical_json_bytes(
            [
                _ARTIFACT_NAMESPACE,
                artifact_kind,
                manifest_sha256,
                payload_pairs,
            ]
        )
    )


def _success_bytes(
    artifact_kind: str,
    *,
    manifest_bytes: bytes,
    payloads: Sequence[_PayloadRecord],
) -> tuple[bytes, str]:
    manifest_sha256 = _sha256(manifest_bytes)
    artifact_sha256 = _artifact_sha256(
        artifact_kind,
        manifest_sha256,
        payloads,
    )
    payload_sha256s = {
        payload.name: cast(str, payload.descriptor["sha256"]) for payload in payloads
    }
    return (
        _canonical_json_bytes(
            {
                "schema_version": _SCHEMA_VERSION,
                "artifact_kind": artifact_kind,
                "manifest_sha256": manifest_sha256,
                "artifact_sha256": artifact_sha256,
                "payload_sha256s": payload_sha256s,
                "complete": True,
            }
        ),
        artifact_sha256,
    )


def _publish_artifact(
    root: Path,
    *,
    relative_path: Path,
    context: _CheckpointContext,
    artifact_kind: str,
    manifest: dict[str, object],
    payloads: Sequence[_PayloadRecord],
    panel_token: str,
    telemetry: G2CheckpointTelemetry,
    validate_parent: Callable[[], None] | None = None,
) -> G2CheckpointEvidence:
    manifest_bytes = _canonical_json_bytes(manifest)
    success_bytes, artifact_sha256 = _success_bytes(
        artifact_kind,
        manifest_bytes=manifest_bytes,
        payloads=payloads,
    )
    staged_payloads = (
        *(payload.payload for payload in payloads),
        manifest_bytes,
        success_bytes,
    )
    lock_lease = _acquire_root_lock(root, final_relative_path=relative_path)
    stage: Path | None = None
    published = False
    completed = False
    final_path = root / relative_path
    try:
        _enforce_tree_cap(root)
        missing_directories = _missing_parent_directory_count(root, relative_path.parent)
        _reserve_tree_capacity(
            root,
            staged_payloads,
            future_entry_units=(2 * missing_directories + 2 + len(staged_payloads) + 1),
            operation="complete publication",
        )
        parent = _ensure_parent_directories(root, relative_path.parent)
        if os.path.lexists(final_path):
            raise FileExistsError("checkpoint destination exists and is immutable")
        if validate_parent is not None:
            validate_parent()
        stage = Path(
            tempfile.mkdtemp(
                prefix=f".{relative_path.name}.stage-",
                dir=parent,
            )
        )
        os.chmod(stage, 0o700)
        _enforce_tree_cap(root)
        _reserve_stage_capacity(root, staged_payloads)
        for payload in payloads:
            _write_file(stage / payload.name, payload.payload)
            _enforce_tree_cap(root)
        _write_file(stage / "manifest.json", manifest_bytes)
        _enforce_tree_cap(root)
        _write_file(stage / "_SUCCESS", success_bytes)
        _enforce_tree_cap(root)
        _fsync_directory(stage)
        _assert_context_stable(context)
        _enforce_tree_cap(root)
        if os.path.lexists(final_path):
            raise FileExistsError("checkpoint destination exists and is immutable")
        os.rename(stage, final_path)
        published = True
        stage = None
        _enforce_tree_cap(root)
        _fsync_directory(parent)
        logical, allocated = _path_usage(final_path)
        evidence = G2CheckpointEvidence(
            artifact_path=final_path,
            artifact_sha256=artifact_sha256,
            panel_token=panel_token,
            checkpoint_bytes=max(logical, allocated),
            telemetry=telemetry,
            source_snapshot_sha256=context.source.snapshot_sha256,
            runtime_sha256=context.runtime.runtime_sha256,
        )
        completed = True
        return evidence
    finally:
        cleanup_complete = stage is None
        try:
            if stage is not None and os.path.lexists(stage):
                shutil.rmtree(stage)
                _fsync_directory(stage.parent)
                cleanup_complete = True
        finally:
            _release_root_lock(
                root,
                lock_lease,
                remove_marker=completed or (not published and cleanup_complete),
            )


def _validate_digest_tuple(values: tuple[str, ...], *, n_dates: int, name: str) -> None:
    if (
        type(values) is not tuple
        or len(values) != n_dates
        or any(not _is_sha256(value) for value in values)
    ):
        raise ValueError(f"checkpoint {name} must be one digest per ordered date")


def _validate_evidence(
    evidence: G2CheckpointEvidence,
    *,
    expected_path: Path,
    context: _CheckpointContext,
) -> None:
    if type(evidence) is not G2CheckpointEvidence:
        raise TypeError("base checkpoint evidence must use exact G2CheckpointEvidence")
    if evidence.artifact_path != expected_path:
        raise ValueError("base checkpoint evidence path does not match its address")
    _require_sha256(evidence.artifact_sha256, name="base artifact digest")
    _require_sha256(evidence.panel_token, name="base panel token")
    if type(evidence.checkpoint_bytes) is not int or evidence.checkpoint_bytes < 0:
        raise ValueError("base checkpoint byte count is invalid")
    _validate_telemetry(evidence.telemetry)
    if evidence.source_snapshot_sha256 != context.source.snapshot_sha256:
        raise ValueError("base checkpoint evidence source identity mismatch")
    if evidence.runtime_sha256 != context.runtime.runtime_sha256:
        raise ValueError("base checkpoint evidence runtime identity mismatch")


def _write_base_artifact(
    checkpoint_root: Path,
    *,
    expected: G2PanelCheckpointExpectation,
    contract: G2Contract,
    authority: TestRngNamespace,
    repository_root: Path,
    telemetry: G2CheckpointTelemetry,
    panel: object,
) -> G2CheckpointEvidence:
    """Write one immutable complete base-panel artifact."""
    smooth_module = importlib.import_module("xid.models.g2_smooth")
    snapshot_builder = getattr(smooth_module, "_checkpoint_base_snapshot", None)
    if not callable(snapshot_builder):
        raise ValueError("checkpoint base panel authority builder is unavailable")
    snapshot = snapshot_builder(panel)
    if type(snapshot) is not _BasePanelWriteSnapshot:
        raise TypeError("checkpoint base panel authority snapshot has the wrong type")
    context = _checkpoint_context(
        expected,
        contract=contract,
        authority=authority,
        repository_root=repository_root,
        artifact_kind="base-panel",
    )
    root = _validate_checkpoint_root(checkpoint_root, context.repository_root)
    _validate_telemetry(telemetry)
    _validate_panel_dimensions(
        date_indices=snapshot.date_indices,
        n_rows=snapshot.n_rows,
        n_assets=snapshot.n_assets,
        n_levels=snapshot.n_levels,
        x0_width=snapshot.x0_width,
        context=context,
    )
    receipts = _validate_receipts(
        snapshot.source_receipts,
        expected=expected,
        response_map=context.design_response_map,
        contract=contract,
        name="source receipts",
    )
    _validate_digest_tuple(
        snapshot.design_sha256s,
        n_dates=expected.n_dates,
        name="design SHA256s",
    )
    token = _require_sha256(snapshot.panel_token, name="base panel token")
    packed_width = snapshot.x0_width * (snapshot.x0_width + 1) // 2
    payload = _npy_payload(
        "x0tx0_upper.npy",
        snapshot.x0tx0_upper,
        shape=(expected.n_dates, packed_width),
    )
    manifest = _base_manifest(
        context=context,
        telemetry=telemetry,
        date_indices=snapshot.date_indices,
        n_rows=snapshot.n_rows,
        n_assets=snapshot.n_assets,
        n_levels=snapshot.n_levels,
        x0_width=snapshot.x0_width,
        source_receipts=receipts,
        design_sha256s=snapshot.design_sha256s,
        payload=payload,
        panel_token=token,
    )
    relative_path = _artifact_relative_path(
        expected,
        design_response_map=context.design_response_map,
        artifact_kind="base-panel",
    )
    return _publish_artifact(
        root,
        relative_path=relative_path,
        context=context,
        artifact_kind="base-panel",
        manifest=manifest,
        payloads=(payload,),
        panel_token=token,
        telemetry=telemetry,
    )


def _write_cell_artifact(
    checkpoint_root: Path,
    *,
    base_checkpoint: G2CheckpointEvidence,
    expected: G2PanelCheckpointExpectation,
    contract: G2Contract,
    authority: TestRngNamespace,
    repository_root: Path,
    telemetry: G2CheckpointTelemetry,
    base_panel: object,
    cell_panel: object,
) -> G2CheckpointEvidence:
    """Write one immutable response artifact after reloading its base parent."""
    smooth_module = importlib.import_module("xid.models.g2_smooth")
    snapshot_builder = getattr(smooth_module, "_checkpoint_cell_snapshot", None)
    if not callable(snapshot_builder):
        raise ValueError("checkpoint cell panel authority builder is unavailable")
    snapshot = snapshot_builder(base_panel, cell_panel)
    if type(snapshot) is not _CellPanelWriteSnapshot:
        raise TypeError("checkpoint cell panel authority snapshot has the wrong type")
    context = _checkpoint_context(
        expected,
        contract=contract,
        authority=authority,
        repository_root=repository_root,
        artifact_kind="cell-panel",
    )
    root = _validate_checkpoint_root(checkpoint_root, context.repository_root)
    _validate_telemetry(telemetry)
    _validate_panel_dimensions(
        date_indices=snapshot.date_indices,
        n_rows=snapshot.n_rows,
        n_assets=snapshot.n_assets,
        n_levels=contract.n_levels,
        x0_width=snapshot.x0_width,
        context=context,
    )
    design_receipt_snapshot = _validate_receipts(
        snapshot.design_receipts,
        expected=expected,
        response_map=context.design_response_map,
        contract=contract,
        name="cell design receipts",
    )
    response_map = expected.response_map
    if response_map is None:
        raise ValueError("cell checkpoint response map disappeared")
    response_receipt_snapshot = _validate_receipts(
        snapshot.response_receipts,
        expected=expected,
        response_map=response_map,
        contract=contract,
        name="cell response receipts",
    )
    for design_receipt, response_receipt in zip(
        design_receipt_snapshot,
        response_receipt_snapshot,
        strict=True,
    ):
        if (
            design_receipt.provenance != response_receipt.provenance
            or design_receipt.base_identity != response_receipt.base_identity
        ):
            raise ValueError("cell response receipt does not match its design base")
    _validate_digest_tuple(
        snapshot.design_sha256s,
        n_dates=expected.n_dates,
        name="design SHA256s",
    )
    token = _require_sha256(snapshot.cell_panel_token, name="cell panel token")
    base_expected = G2PanelCheckpointExpectation(
        master_seed=expected.master_seed,
        stream=expected.stream,
        n_dates=expected.n_dates,
        panel_index=expected.panel_index,
        response_map=None,
    )
    base_relative = _artifact_relative_path(
        base_expected,
        design_response_map=context.design_response_map,
        artifact_kind="base-panel",
    )
    base_path = root / base_relative
    _validate_evidence(
        base_checkpoint,
        expected_path=base_path,
        context=context,
    )
    if base_checkpoint.panel_token != snapshot.base_panel_token:
        raise ValueError("cell panel authority does not match its base checkpoint")
    x0ty_payload = _npy_payload(
        "x0ty.npy",
        snapshot.x0ty,
        shape=(expected.n_dates, snapshot.x0_width, snapshot.n_assets),
    )
    yty_payload = _npy_payload(
        "yty_upper.npy",
        snapshot.yty_upper,
        shape=(
            expected.n_dates,
            snapshot.n_assets * (snapshot.n_assets + 1) // 2,
        ),
    )
    payloads = (x0ty_payload, yty_payload)
    manifest = _cell_manifest(
        context=context,
        base_checkpoint=base_checkpoint,
        telemetry=telemetry,
        date_indices=snapshot.date_indices,
        n_rows=snapshot.n_rows,
        n_assets=snapshot.n_assets,
        x0_width=snapshot.x0_width,
        design_receipts=design_receipt_snapshot,
        response_receipts=response_receipt_snapshot,
        design_sha256s=snapshot.design_sha256s,
        payloads=payloads,
        panel_token=token,
    )
    relative_path = _artifact_relative_path(
        expected,
        design_response_map=context.design_response_map,
        artifact_kind="cell-panel",
        base_artifact_sha256=base_checkpoint.artifact_sha256,
    )

    def validate_parent() -> None:
        decoded_base = _decode_base_artifact(
            root,
            relative_path=base_relative,
            context=context,
        )
        if decoded_base.evidence != base_checkpoint:
            raise ValueError("cell parent base checkpoint evidence does not match disk")
        if decoded_base.source_receipts != design_receipt_snapshot:
            raise ValueError("cell design receipts do not match the base artifact")
        if decoded_base.design_sha256s != snapshot.design_sha256s:
            raise ValueError("cell design digests do not match the base artifact")
        if (
            decoded_base.date_indices != snapshot.date_indices
            or decoded_base.n_rows != snapshot.n_rows
            or decoded_base.n_assets != snapshot.n_assets
            or decoded_base.x0_width != snapshot.x0_width
        ):
            raise ValueError("cell dimensions do not match the base artifact")

    return _publish_artifact(
        root,
        relative_path=relative_path,
        context=context,
        artifact_kind="cell-panel",
        manifest=manifest,
        payloads=payloads,
        panel_token=token,
        telemetry=telemetry,
        validate_parent=validate_parent,
    )


def _open_artifact_directory(root: Path, relative_path: Path) -> int:
    try:
        descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as error:
        raise ValueError("checkpoint root cannot be opened without following links") from error
    try:
        for part in relative_path.parts:
            try:
                next_descriptor = os.open(
                    part,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
            except OSError as error:
                raise ValueError(
                    "checkpoint artifact address cannot be opened without following links"
                ) from error
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _stat_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_nlink,
        value.st_mode,
    )


def _read_pinned_file(
    directory_descriptor: int,
    name: str,
    *,
    maximum: int,
) -> tuple[bytes, os.stat_result]:
    flags = os.O_RDONLY | os.O_NOFOLLOW
    try:
        descriptor = os.open(name, flags, dir_fd=directory_descriptor)
    except OSError as error:
        raise OSError(
            f"checkpoint file {name} could not be opened without following links"
        ) from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ValueError(f"checkpoint file {name} must be a single-link regular file")
        if before.st_size > maximum:
            raise ValueError(f"checkpoint file {name} exceeds its byte cap")
        with os.fdopen(os.dup(descriptor), "rb", closefd=True) as handle:
            payload = handle.read(maximum + 1)
        after = os.fstat(descriptor)
        if _stat_identity(before) != _stat_identity(after):
            raise ValueError(f"checkpoint file {name} changed while it was read")
        if len(payload) != before.st_size or len(payload) > maximum:
            raise ValueError(f"checkpoint file {name} has an invalid length")
        return payload, after
    finally:
        os.close(descriptor)


def _read_artifact_files(
    root: Path,
    *,
    relative_path: Path,
    payload_names: tuple[str, ...],
) -> tuple[dict[str, bytes], int]:
    directory_descriptor = _open_artifact_directory(root, relative_path)
    try:
        directory_stat = os.fstat(directory_descriptor)
        if not stat.S_ISDIR(directory_stat.st_mode):
            raise ValueError("checkpoint artifact is not a directory")
        expected_names = frozenset((*payload_names, "manifest.json", "_SUCCESS"))
        observed_names = frozenset(os.listdir(directory_descriptor))
        if observed_names != expected_names:
            raise ValueError("checkpoint artifact has a missing or unexpected file")
        snapshots: dict[str, bytes] = {}
        stats: list[os.stat_result] = []
        for name in (*payload_names, "manifest.json", "_SUCCESS"):
            maximum = (
                _MAX_MANIFEST_BYTES
                if name == "manifest.json"
                else _MAX_SUCCESS_BYTES
                if name == "_SUCCESS"
                else _MAX_PAYLOAD_BYTES
            )
            payload, payload_stat = _read_pinned_file(
                directory_descriptor,
                name,
                maximum=maximum,
            )
            snapshots[name] = payload
            stats.append(payload_stat)
        logical = directory_stat.st_size + sum(value.st_size for value in stats)
        allocated = directory_stat.st_blocks * 512 + sum(value.st_blocks * 512 for value in stats)
        return snapshots, max(logical, allocated)
    finally:
        os.close(directory_descriptor)


def _validate_contract_manifest(value: object, *, contract: G2Contract) -> None:
    if type(value) is not dict:
        raise ValueError("checkpoint contract identity must be an object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(
            (
                "config_schema_version",
                "target_schema_version",
                "target_config_schema_version",
                "rng_key_schema_version",
                "design_id",
                "target_design_id",
                "seals",
            )
        ),
        name="contract",
    )
    seals = table["seals"]
    if type(seals) is not dict:
        raise ValueError("checkpoint contract seals must be an object")
    _require_exact_keys(
        cast(dict[str, object], seals),
        frozenset(
            (
                "config_sha256",
                "target_raw_sha256",
                "target_semantic_sha256",
                "lasso_ratio_sha256",
            )
        ),
        name="contract seals",
    )
    _require_exact_json_value(
        table,
        _contract_object(contract),
        name="contract",
    )


def _validate_source_manifest(value: object, *, source: _SourceIdentity) -> None:
    if type(value) is not dict:
        raise ValueError("checkpoint execution source identity must be an object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(
            (
                "snapshot_schema",
                "snapshot_sha256",
                "git_commit",
                "declared_paths_clean",
            )
        ),
        name="execution source",
    )
    if table["snapshot_schema"] != _SNAPSHOT_SCHEMA:
        raise ValueError("checkpoint execution source schema mismatch")
    if table["snapshot_sha256"] != source.snapshot_sha256:
        raise ValueError("checkpoint execution source snapshot mismatch")
    git_commit = table["git_commit"]
    if (
        type(git_commit) is not str
        or len(git_commit) not in (40, 64)
        or any(character not in "0123456789abcdef" for character in git_commit)
    ):
        raise ValueError("checkpoint execution source commit is invalid")
    _require_bool(
        table["declared_paths_clean"],
        name="checkpoint execution source clean flag",
    )


def _validate_runtime_manifest(value: object, *, runtime: _RuntimeIdentity) -> None:
    if type(value) is not dict:
        raise ValueError("checkpoint runtime identity must be an object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(
            (
                "python_implementation",
                "python_version",
                "numpy_version",
                "system",
                "machine",
                "byteorder",
                "rng_runtime_sha256",
                "thread_env",
                "runtime_sha256",
            )
        ),
        name="runtime",
    )
    thread_env = table["thread_env"]
    if type(thread_env) is not dict:
        raise ValueError("checkpoint runtime thread environment must be an object")
    _require_exact_keys(
        cast(dict[str, object], thread_env),
        frozenset(_THREAD_ENV_NAMES),
        name="runtime thread environment",
    )
    _require_exact_json_value(
        table,
        _runtime_object(runtime),
        name="runtime",
    )


def _validate_address_manifest(value: object, *, context: _CheckpointContext) -> None:
    if type(value) is not dict:
        raise ValueError("checkpoint address must be an object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(
            (
                "master_seed",
                "config_schema_version",
                "rng_key_schema_version",
                "stream",
                "phase_id",
                "scenario_id",
                "parent_phase_id",
                "parent_scenario_id",
                "n_dates",
                "panel_index",
                "cell_key",
                "component_ids",
                "replicate_index",
                "completed_date_range",
                "completed_replicate_range",
            )
        ),
        name="address",
    )
    _require_exact_json_value(
        table,
        _address_object(context),
        name="address",
    )


def _validate_completion(value: object, *, n_dates: int) -> None:
    if type(value) is not dict:
        raise ValueError("checkpoint completion range must be an object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(("completed_date_range", "completed_replicate_range")),
        name="completion",
    )
    _require_exact_json_value(
        table,
        _completion_object(n_dates),
        name="completion",
    )


def _parse_dimensions(value: object, *, context: _CheckpointContext) -> tuple[int, int, int, int]:
    if type(value) is not dict:
        raise ValueError("checkpoint dimensions must be an object")
    table = cast(dict[str, object], value)
    _require_exact_keys(
        table,
        frozenset(("n_rows", "n_assets", "n_levels", "x0_width")),
        name="dimensions",
    )
    n_rows = _require_int(table["n_rows"], name="checkpoint n_rows")
    n_assets = _require_int(table["n_assets"], name="checkpoint n_assets")
    n_levels = _require_int(table["n_levels"], name="checkpoint n_levels")
    x0_width = _require_int(table["x0_width"], name="checkpoint x0_width")
    _validate_panel_dimensions(
        date_indices=tuple(range(context.expected.n_dates)),
        n_rows=n_rows,
        n_assets=n_assets,
        n_levels=n_levels,
        x0_width=x0_width,
        context=context,
    )
    return n_rows, n_assets, n_levels, x0_width


def _parse_date_indices(value: object, *, n_dates: int) -> tuple[int, ...]:
    if type(value) is not list:
        raise ValueError("checkpoint date indices must be an array")
    result = tuple(
        _require_int(item, name="checkpoint date index") for item in cast(list[object], value)
    )
    if result != tuple(range(n_dates)):
        raise ValueError("checkpoint date indices are incomplete, duplicate, or out of order")
    return result


def _parse_receipt_array(
    value: object,
    *,
    context: _CheckpointContext,
    response_map: G2ResponseMapIdentity,
    name: str,
) -> tuple[G2DateReceipt, ...]:
    if type(value) is not list:
        raise ValueError(f"checkpoint {name} must be an array")
    receipts = tuple(
        _parse_receipt(item, contract=context.contract, name=f"{name}[{index}]")
        for index, item in enumerate(cast(list[object], value))
    )
    return _validate_receipts(
        receipts,
        expected=context.expected,
        response_map=response_map,
        contract=context.contract,
        name=name,
    )


def _parse_design_sha256s(value: object, *, n_dates: int) -> tuple[str, ...]:
    if type(value) is not list:
        raise ValueError("checkpoint design SHA256s must be an array")
    result = tuple(
        _require_sha256(item, name="checkpoint design SHA256") for item in cast(list[object], value)
    )
    _validate_digest_tuple(result, n_dates=n_dates, name="design SHA256s")
    return result


def _decode_npy(
    payload: bytes,
    *,
    descriptor: object,
    expected_name: str,
    expected_shape: tuple[int, ...],
) -> NDArray[np.float64]:
    if type(descriptor) is not dict:
        raise ValueError("checkpoint payload descriptor must be an object")
    table = cast(dict[str, object], descriptor)
    _require_exact_keys(
        table,
        frozenset(
            (
                "name",
                "npy_format",
                "dtype",
                "shape",
                "data_bytes",
                "file_bytes",
                "sha256",
            )
        ),
        name="payload descriptor",
    )
    expected_data_bytes = math.prod(expected_shape) * 8
    expected_descriptor = {
        "name": expected_name,
        "npy_format": "1.0",
        "dtype": "<f8",
        "shape": list(expected_shape),
        "data_bytes": expected_data_bytes,
        "file_bytes": len(payload),
        "sha256": _sha256(payload),
    }
    _require_exact_json_value(
        table,
        expected_descriptor,
        name="NPY payload descriptor",
    )
    if len(payload) > expected_data_bytes + _MAX_NPY_HEADER_BYTES:
        raise ValueError("checkpoint NPY payload has an oversized header or trailing bytes")
    if len(payload) < 10 or payload[:8] != b"\x93NUMPY\x01\x00":
        raise ValueError("checkpoint NPY payload must use format version 1.0")
    header_length = int.from_bytes(payload[8:10], byteorder="little")
    if header_length > _MAX_NPY_HEADER_BYTES:
        raise ValueError("checkpoint NPY header exceeds 4096 bytes")
    stream = io.BytesIO(payload)
    try:
        version = np.lib.format.read_magic(stream)
        shape, fortran_order, dtype = np.lib.format.read_array_header_1_0(
            stream,
            max_header_size=_MAX_NPY_HEADER_BYTES,
        )
    except (EOFError, ValueError) as error:
        raise ValueError("checkpoint NPY header is invalid") from error
    if version != (1, 0):
        raise ValueError("checkpoint NPY format version mismatch")
    if shape != expected_shape:
        raise ValueError("checkpoint NPY shape mismatch")
    if fortran_order:
        raise ValueError("checkpoint NPY Fortran order is forbidden")
    if dtype.str != "<f8" or dtype.fields is not None or dtype.subdtype is not None:
        raise ValueError("checkpoint NPY dtype or endian is not exact <f8")
    data_offset = stream.tell()
    if data_offset + expected_data_bytes != len(payload):
        raise ValueError("checkpoint NPY payload has trailing or missing bytes")
    view = np.frombuffer(
        payload,
        dtype=np.dtype("<f8"),
        count=math.prod(expected_shape),
        offset=data_offset,
    )
    values = np.array(view.reshape(expected_shape), dtype=np.float64, order="C", copy=True)
    if not np.all(np.isfinite(values)):
        raise ValueError("checkpoint NPY payload contains a nonfinite value")
    values.setflags(write=False)
    return values


def _validate_manifest_common(
    manifest: dict[str, object],
    *,
    context: _CheckpointContext,
    artifact_kind: str,
) -> tuple[tuple[int, ...], int, int, int, int, G2CheckpointTelemetry, str]:
    _require_exact_keys(manifest, _MANIFEST_KEYS, name="manifest")
    if (
        _require_int(
            manifest["schema_version"],
            name="checkpoint manifest schema version",
            minimum=_SCHEMA_VERSION,
            maximum=_SCHEMA_VERSION,
        )
        != _SCHEMA_VERSION
    ):
        raise AssertionError("validated manifest schema version changed")
    if type(manifest["artifact_kind"]) is not str or manifest["artifact_kind"] != artifact_kind:
        raise ValueError("checkpoint artifact kind mismatch")
    _validate_contract_manifest(manifest["contract"], contract=context.contract)
    _validate_source_manifest(manifest["execution_source"], source=context.source)
    _validate_runtime_manifest(manifest["runtime"], runtime=context.runtime)
    _validate_address_manifest(manifest["address"], context=context)
    n_rows, n_assets, n_levels, x0_width = _parse_dimensions(
        manifest["dimensions"],
        context=context,
    )
    observed_design_map = _parse_response_map(
        manifest["design_response_map"],
        name="design response map",
    )
    if observed_design_map != context.design_response_map:
        raise ValueError("checkpoint design response-map identity mismatch")
    date_indices = _parse_date_indices(
        manifest["date_indices"],
        n_dates=context.expected.n_dates,
    )
    panel_token = _require_sha256(
        manifest["panel_token"],
        name="checkpoint panel token",
    )
    telemetry = _parse_telemetry(manifest["telemetry"])
    _validate_completion(
        manifest["completion"],
        n_dates=context.expected.n_dates,
    )
    return (
        date_indices,
        n_rows,
        n_assets,
        n_levels,
        x0_width,
        telemetry,
        panel_token,
    )


def _validate_success(
    success: dict[str, object],
    *,
    artifact_kind: str,
    manifest_bytes: bytes,
    payload_pairs: tuple[tuple[str, str], ...],
) -> str:
    _require_exact_keys(
        success,
        frozenset(
            (
                "schema_version",
                "artifact_kind",
                "manifest_sha256",
                "artifact_sha256",
                "payload_sha256s",
                "complete",
            )
        ),
        name="success marker",
    )
    schema_version = _require_int(
        success["schema_version"],
        name="checkpoint success schema version",
        minimum=_SCHEMA_VERSION,
        maximum=_SCHEMA_VERSION,
    )
    if (
        schema_version != _SCHEMA_VERSION
        or type(success["artifact_kind"]) is not str
        or success["artifact_kind"] != artifact_kind
        or success["complete"] is not True
    ):
        raise ValueError("checkpoint success marker identity is invalid")
    manifest_sha256 = _sha256(manifest_bytes)
    if success["manifest_sha256"] != manifest_sha256:
        raise ValueError("checkpoint success marker manifest hash mismatch")
    payload_sha256s = success["payload_sha256s"]
    if type(payload_sha256s) is not dict or payload_sha256s != dict(payload_pairs):
        raise ValueError("checkpoint success marker payload hashes mismatch")
    artifact_sha256 = _artifact_sha256(
        artifact_kind,
        manifest_sha256,
        payload_pairs,
    )
    if success["artifact_sha256"] != artifact_sha256:
        raise ValueError("checkpoint success marker artifact hash mismatch")
    return artifact_sha256


def _evidence_from_decoded(
    *,
    root: Path,
    relative_path: Path,
    context: _CheckpointContext,
    checkpoint_bytes: int,
    artifact_sha256: str,
    panel_token: str,
    telemetry: G2CheckpointTelemetry,
) -> G2CheckpointEvidence:
    return G2CheckpointEvidence(
        artifact_path=root / relative_path,
        artifact_sha256=artifact_sha256,
        panel_token=panel_token,
        checkpoint_bytes=checkpoint_bytes,
        telemetry=telemetry,
        source_snapshot_sha256=context.source.snapshot_sha256,
        runtime_sha256=context.runtime.runtime_sha256,
    )


def _decode_base_artifact(
    root: Path,
    *,
    relative_path: Path,
    context: _CheckpointContext,
) -> _DecodedBaseArtifact:
    snapshots, checkpoint_bytes = _read_artifact_files(
        root,
        relative_path=relative_path,
        payload_names=_BASE_PAYLOAD_NAMES,
    )
    manifest_bytes = snapshots["manifest.json"]
    manifest = _parse_canonical_object(
        manifest_bytes,
        name="manifest",
        maximum=_MAX_MANIFEST_BYTES,
    )
    (
        date_indices,
        n_rows,
        n_assets,
        n_levels,
        x0_width,
        telemetry,
        panel_token,
    ) = _validate_manifest_common(
        manifest,
        context=context,
        artifact_kind="base-panel",
    )
    if manifest["response_map"] is not None:
        raise ValueError("base checkpoint cannot contain a response map")
    if (
        manifest["design_receipts"] is not None
        or manifest["response_receipts"] is not None
        or manifest["parent"] is not None
    ):
        raise ValueError("base checkpoint contains cell-only metadata")
    source_receipts = _parse_receipt_array(
        manifest["source_receipts"],
        context=context,
        response_map=context.design_response_map,
        name="source receipts",
    )
    design_sha256s = _parse_design_sha256s(
        manifest["design_sha256s"],
        n_dates=context.expected.n_dates,
    )
    payload_descriptors = manifest["payloads"]
    if type(payload_descriptors) is not list or len(payload_descriptors) != 1:
        raise ValueError("base checkpoint payload descriptor count mismatch")
    packed_width = x0_width * (x0_width + 1) // 2
    payload = snapshots["x0tx0_upper.npy"]
    x0tx0_upper = _decode_npy(
        payload,
        descriptor=cast(list[object], payload_descriptors)[0],
        expected_name="x0tx0_upper.npy",
        expected_shape=(context.expected.n_dates, packed_width),
    )
    payload_pairs = (("x0tx0_upper.npy", _sha256(payload)),)
    success = _parse_canonical_object(
        snapshots["_SUCCESS"],
        name="success marker",
        maximum=_MAX_SUCCESS_BYTES,
    )
    artifact_sha256 = _validate_success(
        success,
        artifact_kind="base-panel",
        manifest_bytes=manifest_bytes,
        payload_pairs=payload_pairs,
    )
    evidence = _evidence_from_decoded(
        root=root,
        relative_path=relative_path,
        context=context,
        checkpoint_bytes=checkpoint_bytes,
        artifact_sha256=artifact_sha256,
        panel_token=panel_token,
        telemetry=telemetry,
    )
    return _DecodedBaseArtifact(
        evidence=evidence,
        date_indices=date_indices,
        n_rows=n_rows,
        n_assets=n_assets,
        n_levels=n_levels,
        x0_width=x0_width,
        source_receipts=source_receipts,
        design_sha256s=design_sha256s,
        x0tx0_upper=x0tx0_upper,
    )


def _decode_cell_artifact(
    root: Path,
    *,
    relative_path: Path,
    context: _CheckpointContext,
    base_checkpoint: G2CheckpointEvidence,
) -> _DecodedCellArtifact:
    snapshots, checkpoint_bytes = _read_artifact_files(
        root,
        relative_path=relative_path,
        payload_names=_CELL_PAYLOAD_NAMES,
    )
    manifest_bytes = snapshots["manifest.json"]
    manifest = _parse_canonical_object(
        manifest_bytes,
        name="manifest",
        maximum=_MAX_MANIFEST_BYTES,
    )
    (
        date_indices,
        n_rows,
        n_assets,
        _n_levels,
        x0_width,
        telemetry,
        panel_token,
    ) = _validate_manifest_common(
        manifest,
        context=context,
        artifact_kind="cell-panel",
    )
    if manifest["source_receipts"] is not None:
        raise ValueError("cell checkpoint cannot contain source receipts")
    response_map = context.expected.response_map
    if response_map is None:
        raise ValueError("cell checkpoint response map disappeared")
    observed_response_map = _parse_response_map(
        manifest["response_map"],
        name="response map",
    )
    if observed_response_map != response_map:
        raise ValueError("checkpoint response-map identity mismatch")
    design_receipts = _parse_receipt_array(
        manifest["design_receipts"],
        context=context,
        response_map=context.design_response_map,
        name="design receipts",
    )
    response_receipts = _parse_receipt_array(
        manifest["response_receipts"],
        context=context,
        response_map=response_map,
        name="response receipts",
    )
    for design_receipt, response_receipt in zip(
        design_receipts,
        response_receipts,
        strict=True,
    ):
        if (
            design_receipt.provenance != response_receipt.provenance
            or design_receipt.base_identity != response_receipt.base_identity
        ):
            raise ValueError("checkpoint response receipt does not match its design base")
    design_sha256s = _parse_design_sha256s(
        manifest["design_sha256s"],
        n_dates=context.expected.n_dates,
    )
    parent = manifest["parent"]
    if type(parent) is not dict:
        raise ValueError("cell checkpoint parent identity must be an object")
    parent_table = cast(dict[str, object], parent)
    _require_exact_keys(
        parent_table,
        frozenset(("base_artifact_sha256", "base_panel_token")),
        name="parent",
    )
    parent_artifact_sha256 = _require_sha256(
        parent_table["base_artifact_sha256"],
        name="checkpoint parent base artifact digest",
    )
    parent_panel_token = _require_sha256(
        parent_table["base_panel_token"],
        name="checkpoint parent base panel token",
    )
    if (
        parent_artifact_sha256 != base_checkpoint.artifact_sha256
        or parent_panel_token != base_checkpoint.panel_token
    ):
        raise ValueError("cell checkpoint parent base identity mismatch")
    payload_descriptors = manifest["payloads"]
    if type(payload_descriptors) is not list or len(payload_descriptors) != 2:
        raise ValueError("cell checkpoint payload descriptor count mismatch")
    descriptors = cast(list[object], payload_descriptors)
    x0ty_payload = snapshots["x0ty.npy"]
    yty_payload = snapshots["yty_upper.npy"]
    x0ty = _decode_npy(
        x0ty_payload,
        descriptor=descriptors[0],
        expected_name="x0ty.npy",
        expected_shape=(context.expected.n_dates, x0_width, n_assets),
    )
    yty_upper = _decode_npy(
        yty_payload,
        descriptor=descriptors[1],
        expected_name="yty_upper.npy",
        expected_shape=(context.expected.n_dates, n_assets * (n_assets + 1) // 2),
    )
    payload_pairs = (
        ("x0ty.npy", _sha256(x0ty_payload)),
        ("yty_upper.npy", _sha256(yty_payload)),
    )
    success = _parse_canonical_object(
        snapshots["_SUCCESS"],
        name="success marker",
        maximum=_MAX_SUCCESS_BYTES,
    )
    artifact_sha256 = _validate_success(
        success,
        artifact_kind="cell-panel",
        manifest_bytes=manifest_bytes,
        payload_pairs=payload_pairs,
    )
    evidence = _evidence_from_decoded(
        root=root,
        relative_path=relative_path,
        context=context,
        checkpoint_bytes=checkpoint_bytes,
        artifact_sha256=artifact_sha256,
        panel_token=panel_token,
        telemetry=telemetry,
    )
    return _DecodedCellArtifact(
        evidence=evidence,
        date_indices=date_indices,
        n_rows=n_rows,
        n_assets=n_assets,
        x0_width=x0_width,
        design_receipts=design_receipts,
        response_receipts=response_receipts,
        design_sha256s=design_sha256s,
        x0ty=x0ty,
        yty_upper=yty_upper,
        parent_base_artifact_sha256=parent_artifact_sha256,
        parent_base_panel_token=parent_panel_token,
    )


def _load_base_artifact(
    checkpoint_root: Path,
    *,
    expected: G2PanelCheckpointExpectation,
    contract: G2Contract,
    authority: TestRngNamespace,
    repository_root: Path,
) -> _DecodedBaseArtifact:
    """Decode one base artifact without restoring model-stage authority."""
    context = _checkpoint_context(
        expected,
        contract=contract,
        authority=authority,
        repository_root=repository_root,
        artifact_kind="base-panel",
    )
    root = _validate_checkpoint_root(checkpoint_root, context.repository_root)
    _require_no_root_lock(root)
    _enforce_tree_cap(root)
    relative_path = _artifact_relative_path(
        expected,
        design_response_map=context.design_response_map,
        artifact_kind="base-panel",
    )
    decoded = _decode_base_artifact(
        root,
        relative_path=relative_path,
        context=context,
    )
    _assert_context_stable(context)
    _require_no_root_lock(root)
    return decoded


def _load_cell_artifact(
    checkpoint_root: Path,
    *,
    base_checkpoint: G2CheckpointEvidence,
    expected: G2PanelCheckpointExpectation,
    contract: G2Contract,
    authority: TestRngNamespace,
    repository_root: Path,
) -> _DecodedCellArtifact:
    """Decode a cell artifact and independently reload its immutable base parent."""
    context = _checkpoint_context(
        expected,
        contract=contract,
        authority=authority,
        repository_root=repository_root,
        artifact_kind="cell-panel",
    )
    root = _validate_checkpoint_root(checkpoint_root, context.repository_root)
    _require_no_root_lock(root)
    _enforce_tree_cap(root)
    base_expected = G2PanelCheckpointExpectation(
        master_seed=expected.master_seed,
        stream=expected.stream,
        n_dates=expected.n_dates,
        panel_index=expected.panel_index,
        response_map=None,
    )
    base_relative = _artifact_relative_path(
        base_expected,
        design_response_map=context.design_response_map,
        artifact_kind="base-panel",
    )
    _validate_evidence(
        base_checkpoint,
        expected_path=root / base_relative,
        context=context,
    )
    decoded_base = _decode_base_artifact(
        root,
        relative_path=base_relative,
        context=context,
    )
    if decoded_base.evidence != base_checkpoint:
        raise ValueError("cell parent base checkpoint evidence does not match disk")
    relative_path = _artifact_relative_path(
        expected,
        design_response_map=context.design_response_map,
        artifact_kind="cell-panel",
        base_artifact_sha256=base_checkpoint.artifact_sha256,
    )
    decoded_cell = _decode_cell_artifact(
        root,
        relative_path=relative_path,
        context=context,
        base_checkpoint=base_checkpoint,
    )
    if decoded_cell.design_receipts != decoded_base.source_receipts:
        raise ValueError("cell design receipts do not match the loaded base artifact")
    if decoded_cell.design_sha256s != decoded_base.design_sha256s:
        raise ValueError("cell design digests do not match the loaded base artifact")
    if (
        decoded_cell.date_indices != decoded_base.date_indices
        or decoded_cell.n_rows != decoded_base.n_rows
        or decoded_cell.n_assets != decoded_base.n_assets
        or decoded_cell.x0_width != decoded_base.x0_width
    ):
        raise ValueError("cell dimensions do not match the loaded base artifact")
    _assert_context_stable(context)
    _require_no_root_lock(root)
    return decoded_cell
