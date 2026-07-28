"""One-shot supervised recovery evidence for the sealed G2 checkpoint codec.

The public entry point has no address overrides.  Internal ``_worker`` and
``_fresh`` commands are implementation details used by the parent supervisor;
ordinary tests exercise only the disjoint seed-1729 software path.
"""

from __future__ import annotations

import gc
import hashlib
import json
import math
import os
import resource
import signal
import stat
import subprocess
import sys
import time
from contextlib import suppress
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Literal, NoReturn, cast

import numpy as np
from numpy.typing import NDArray

import xid.models.g2_checkpoint as checkpoint_codec
from xid.models.g2_checkpoint import (
    G2CheckpointEnvironmentIdentity,
    G2CheckpointEvidence,
    G2CheckpointTelemetry,
    G2PanelCheckpointExpectation,
    inspect_g2_checkpoint_environment,
)
from xid.models.g2_smooth import (
    G2FlowView,
    SmoothBasePanelMoments,
    SmoothCellPanelMoments,
    aggregate_contract_smooth_moments,
    build_contract_cell_date_moments,
    build_contract_smooth_date_design,
    fit_condition_ridge,
    fit_homogeneous_ols,
    load_contract_base_panel_checkpoint,
    load_contract_cell_panel_checkpoint,
    stack_contract_base_moments,
    stack_contract_cell_moments,
    write_contract_base_panel_checkpoint,
    write_contract_cell_panel_checkpoint,
)
from xid.sim.g2 import (
    G2Contract,
    G2DateReceipt,
    G2ResponseMapIdentity,
    G2RuntimeFingerprint,
    G2Stream,
    TestRngNamespace,
    build_cell,
    current_g2_runtime_fingerprint,
    load_g2_contract,
    transform_date,
)

_THREAD_ENV_NAMES = (
    "BLIS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
)
_TIMEOUT_METHOD = "monotonic-process-group-kill"
_RSS_NORMALIZATION_METHOD = "ps-kib-process-tree-x1024"
_MAX_STDIO_BYTES = 1024 * 1024
_MAX_JSON_BYTES = 1024 * 1024
_MAX_CHILD_CAPABILITY_BYTES = 4096
_PUBLIC_SEED = 9191
_TEST_SEED = 1729
_PUBLIC_RESULT_LABEL = "results/g2_checkpoint_recovery"
_PUBLIC_CHECKPOINT_LABEL = "data/g2_checkpoint_recovery/checkpoints"
_PUBLIC_SCRATCH_LABEL = "data/g2_checkpoint_recovery/scratch"
_PUBLIC_SUPERVISOR_CACHE_LABEL = "data/g2_checkpoint_recovery/scratch/bootstrap-pycache"
_TEST_CHECKPOINT_LABEL = "test/checkpoints"
_TEST_SCRATCH_LABEL = "test/scratch"
_MAKE_LAUNCH_ENV = "XID_G2_RECOVERY_MAKE_TARGET"
_MAKE_LAUNCH_VALUE = "g2-checkpoint-recovery-v1"
_CHILD_CAPABILITY_ENV = "XID_G2_RECOVERY_CHILD_FD"
_CONCRETE_PATH_TYPE = type(Path())

_ATTEMPT_KEYS = frozenset(
    (
        "schema_version",
        "status",
        "seed",
        "stream",
        "phase_id",
        "scenario_id",
        "n_dates",
        "panel_index",
        "design_target_index",
        "response_target_index",
        "paper_recovery",
        "phi",
        "reliability",
        "source_snapshot_sha256",
        "runtime_sha256",
        "checkpoint_root",
        "scratch_root",
        "hard_stops",
        "supervision",
    )
)
_WORKER_RESULT_KEYS = frozenset(
    (
        "schema_version",
        "status",
        "attempt_sha256",
        "seed",
        "stream",
        "phase_id",
        "scenario_id",
        "n_dates",
        "panel_index",
        "source_snapshot_sha256",
        "runtime_sha256",
        "base_artifact_sha256",
        "cell_artifact_sha256",
        "array_sha256_before",
        "array_sha256_after",
        "receipt_sha256_before",
        "receipt_sha256_after",
        "design_digest_sha256_before",
        "design_digest_sha256_after",
        "coefficient_sha256_before",
        "coefficient_sha256_after",
        "coefficient_shapes",
        "coefficient_finite",
        "fresh_process_coefficient_sha256",
        "fresh_process_rng_draw_count",
        "artifact_logical_bytes",
        "artifact_allocated_bytes",
    )
)
_RESULT_KEYS = frozenset(
    (
        "schema_version",
        "status",
        "seed",
        "stream",
        "phase_id",
        "scenario_id",
        "n_dates",
        "panel_index",
        "source_snapshot_sha256",
        "runtime_sha256",
        "base_artifact_sha256",
        "cell_artifact_sha256",
        "array_sha256_before",
        "array_sha256_after",
        "receipt_sha256_before",
        "receipt_sha256_after",
        "design_digest_sha256_before",
        "design_digest_sha256_after",
        "coefficient_sha256_before",
        "coefficient_sha256_after",
        "coefficient_shapes",
        "coefficient_finite",
        "fresh_process_coefficient_sha256",
        "fresh_process_rng_draw_count",
        "artifact_logical_bytes",
        "artifact_allocated_bytes",
        "elapsed_seconds",
        "timeout_method",
        "peak_rss_bytes",
        "rss_normalization_method",
        "hard_stops",
    )
)
_FAILURE_KEYS = frozenset(
    (
        "schema_version",
        "status",
        "attempt_sha256",
        "failure_stage",
        "failure_type",
        "message",
        "worker_returncode",
        "elapsed_seconds",
        "peak_rss_bytes",
        "timeout_method",
        "rss_normalization_method",
        "hard_stops",
        "stdout_sha256",
        "stderr_sha256",
    )
)
_HASH_OBJECT_KEYS = {
    "array": frozenset(("base_x0tx0_upper", "cell_x0ty", "cell_yty_upper")),
    "receipt": frozenset(
        ("base_source_receipts", "cell_design_receipts", "cell_response_receipts")
    ),
    "design": frozenset(("base_design_sha256s", "cell_design_sha256s")),
    "coefficient": frozenset(("homogeneous", "observable", "oracle")),
    "bytes": frozenset(("base", "cell", "combined")),
}


class RecoveryRunFailed(RuntimeError):
    """The immutable recovery attempt was consumed and did not pass."""


class _PublicationStateUncertain(RuntimeError):
    """A final evidence link could not be durably committed or rolled back."""


@dataclass(frozen=True, slots=True)
class RecoveryRunSpec:
    """Exact parent-supervisor coordinates and hard stops."""

    mode: Literal["test", "public"]
    repository_root: Path
    result_root: Path
    checkpoint_root: Path
    scratch_root: Path
    seed: int
    stream: G2Stream
    n_dates: int
    panel_index: int
    design_target_index: int
    response_target_index: int
    expected_wall_seconds: float
    hard_wall_seconds: float
    expected_peak_rss_bytes: int
    hard_peak_rss_bytes: int
    hard_artifact_bytes: int
    poll_seconds: float
    require_clean_source: bool
    checkpoint_label: str
    scratch_label: str


@dataclass(frozen=True, slots=True)
class _SupervisionEvidence:
    elapsed_seconds: float
    peak_rss_bytes: int
    worker_returncode: int | None
    failure_stage: str | None
    failure_message: str | None


@dataclass(frozen=True, slots=True)
class _BytecodePolicy:
    supervisor_prefix: Path
    worker_prefix: Path
    fresh_prefix: Path


@dataclass(frozen=True, slots=True)
class _ChildCapability:
    role: Literal["worker", "fresh"]
    parent_pid: int
    attempt_sha256: str
    spec_sha256: str


def _canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
        + b"\n"
    )


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


def _json_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON object contains a duplicate key")
        result[key] = value
    return result


def _parse_canonical_object(
    path: Path,
    *,
    exact_keys: frozenset[str] | None = None,
    maximum: int = _MAX_JSON_BYTES,
) -> dict[str, object]:
    payload = _read_stable_regular_file(path, maximum=maximum)
    return _parse_canonical_payload(
        payload,
        name=path.name,
        exact_keys=exact_keys,
    )


def _parse_canonical_payload(
    payload: bytes,
    *,
    name: str,
    exact_keys: frozenset[str] | None = None,
) -> dict[str, object]:
    try:
        value = json.loads(
            payload.decode("ascii"),
            object_pairs_hook=_json_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ValueError(f"invalid JSON constant {token}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{name} is not canonical JSON") from error
    if type(value) is not dict or _canonical_json_bytes(value) != payload:
        raise ValueError(f"{name} is not an exact canonical JSON object")
    result = cast(dict[str, object], value)
    if exact_keys is not None and frozenset(result) != exact_keys:
        raise ValueError(f"{name} has an unexpected schema")
    return result


def _read_stable_regular_file(path: Path, *, maximum: int) -> bytes:
    if type(path) is not _CONCRETE_PATH_TYPE:
        raise TypeError("evidence path must use the exact concrete pathlib path type")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"{path.name} must be a regular file")
        if before.st_size > maximum:
            raise ValueError(f"{path.name} exceeds its size cap")
        chunks: list[bytes] = []
        remaining = maximum + 1
        while remaining:
            chunk = os.read(descriptor, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    if len(payload) > maximum:
        raise ValueError(f"{path.name} exceeds its size cap")
    identity_before = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
        before.st_ctime_ns,
    )
    identity_after = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    )
    current = os.lstat(path)
    if (
        identity_before != identity_after
        or len(payload) != before.st_size
        or stat.S_ISLNK(current.st_mode)
        or current.st_dev != before.st_dev
        or current.st_ino != before.st_ino
    ):
        raise ValueError(f"{path.name} changed while it was being read")
    return payload


def _exclusive_write(path: Path, payload: bytes) -> None:
    stage = path.with_name(f".{path.name}.stage-{os.getpid()}")
    descriptor = os.open(
        stage,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
    )
    linked = False
    publication_error: BaseException | None = None
    try:
        try:
            view = memoryview(payload)
            written = 0
            while written < len(view):
                count = os.write(descriptor, view[written:])
                if count <= 0:
                    raise OSError("exclusive evidence write made no progress")
                written += count
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.link(stage, path, follow_symlinks=False)
        linked = True
        try:
            _fsync_directory(path.parent)
        except BaseException as first_error:
            try:
                _fsync_directory(path.parent)
            except BaseException:
                try:
                    os.unlink(path)
                    linked = False
                    _fsync_directory(path.parent)
                except BaseException as rollback_error:
                    raise _PublicationStateUncertain(
                        f"{path.name} publication could not be durably rolled back"
                    ) from rollback_error
                raise first_error from None
    except BaseException as error:
        publication_error = error
    preserve_uncertainty = isinstance(publication_error, _PublicationStateUncertain)
    try:
        os.unlink(stage)
    except FileNotFoundError:
        pass
    except OSError:
        pass
    except BaseException:
        if not preserve_uncertainty:
            raise
    try:
        _fsync_directory(path.parent)
    except OSError:
        pass
    except BaseException:
        if not preserve_uncertainty:
            raise
    if publication_error is not None:
        raise publication_error
    if not linked:
        raise OSError("exclusive evidence publication did not create its destination")


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _canonical_path_identity(path: Path, *, strict: bool, name: str) -> Path:
    if not path.is_absolute():
        raise ValueError(f"{name} must be an absolute canonical path")
    try:
        resolved = path.resolve(strict=strict)
    except OSError as error:
        raise ValueError(f"{name} cannot be resolved canonically") from error
    if resolved != path:
        raise ValueError(f"{name} must not contain aliases or symlinked ancestors")
    return resolved


def _ensure_directory(path: Path, *, empty: bool, name: str) -> Path:
    if not isinstance(path, Path):
        raise TypeError(f"{name} must use pathlib.Path")
    _canonical_path_identity(path, strict=False, name=name)
    try:
        path.mkdir(parents=True, mode=0o700, exist_ok=True)
        metadata = os.lstat(path)
    except OSError as error:
        raise ValueError(f"{name} cannot be created") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f"{name} must be a non-symlink directory")
    resolved = _canonical_path_identity(path, strict=True, name=name)
    if empty and any(path.iterdir()):
        raise ValueError(f"{name} must be empty before the attempt")
    return resolved


def _safe_relative_label(value: str, *, name: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(f"{name} must be a nonempty relative POSIX path")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        raise ValueError(f"{name} must be a safe relative POSIX path")
    if "\\" in value or pure.as_posix() != value:
        raise ValueError(f"{name} must be normalized POSIX text")
    return value


def _validate_spec(spec: RecoveryRunSpec) -> None:
    if type(spec) is not RecoveryRunSpec:
        raise TypeError("recovery run requires exact RecoveryRunSpec")
    if spec.mode not in ("test", "public"):
        raise ValueError("recovery mode must be test or public")
    for path_name, path_value in (
        ("repository_root", spec.repository_root),
        ("result_root", spec.result_root),
        ("checkpoint_root", spec.checkpoint_root),
        ("scratch_root", spec.scratch_root),
    ):
        if type(path_value) is not _CONCRETE_PATH_TYPE:
            raise TypeError(f"{path_name} must use the exact concrete pathlib path type")
        _canonical_path_identity(path_value, strict=False, name=path_name)
    if type(spec.stream) is not G2Stream:
        raise TypeError("recovery stream must use exact G2Stream")
    for integer_name, integer_value in (
        ("seed", spec.seed),
        ("n_dates", spec.n_dates),
        ("panel_index", spec.panel_index),
        ("design_target_index", spec.design_target_index),
        ("response_target_index", spec.response_target_index),
        ("expected_peak_rss_bytes", spec.expected_peak_rss_bytes),
        ("hard_peak_rss_bytes", spec.hard_peak_rss_bytes),
        ("hard_artifact_bytes", spec.hard_artifact_bytes),
    ):
        if type(integer_value) is not int or integer_value < 0:
            raise ValueError(f"{integer_name} must be a nonnegative exact Python int")
    for float_name, float_value in (
        ("expected_wall_seconds", spec.expected_wall_seconds),
        ("hard_wall_seconds", spec.hard_wall_seconds),
        ("poll_seconds", spec.poll_seconds),
    ):
        if type(float_value) is not float or not math.isfinite(float_value) or float_value <= 0.0:
            raise ValueError(f"{float_name} must be a positive exact finite Python float")
    if type(spec.require_clean_source) is not bool:
        raise TypeError("require_clean_source must be an exact Python bool")
    _safe_relative_label(spec.checkpoint_label, name="checkpoint_label")
    _safe_relative_label(spec.scratch_label, name="scratch_label")
    expected_stream = (
        G2Stream.VALIDATION_DATE_FRONTIER if spec.mode == "test" else G2Stream.VALIDATION_RECOVERY
    )
    common = (
        spec.stream is expected_stream
        and spec.panel_index == 0
        and spec.design_target_index == 16
        and spec.response_target_index == 0
        and spec.expected_wall_seconds == 30.0
        and spec.hard_wall_seconds == 120.0
        and spec.expected_peak_rss_bytes == 1024**3
        and spec.hard_peak_rss_bytes == 1536 * 1024**2
        and spec.hard_artifact_bytes == 12 * 1024**2
        and spec.poll_seconds == 0.05
    )
    if not common:
        raise ValueError("recovery specification differs from its frozen software contract")
    if spec.mode == "test":
        if (
            spec.seed != _TEST_SEED
            or spec.n_dates != 48
            or spec.require_clean_source
            or spec.checkpoint_label != _TEST_CHECKPOINT_LABEL
            or spec.scratch_label != _TEST_SCRATCH_LABEL
        ):
            raise ValueError(
                "test recovery accepts only the frozen seed-1729 smoke and canonical labels"
            )
    else:
        repository_root = Path(__file__).resolve().parents[2]
        expected_roots = (
            repository_root,
            repository_root / _PUBLIC_RESULT_LABEL,
            repository_root / _PUBLIC_CHECKPOINT_LABEL,
            repository_root / _PUBLIC_SCRATCH_LABEL,
        )
        if (
            spec.seed != _PUBLIC_SEED
            or spec.n_dates != 252
            or not spec.require_clean_source
            or spec.checkpoint_label != _PUBLIC_CHECKPOINT_LABEL
            or spec.scratch_label != _PUBLIC_SCRATCH_LABEL
            or (
                spec.repository_root,
                spec.result_root,
                spec.checkpoint_root,
                spec.scratch_root,
            )
            != expected_roots
        ):
            raise ValueError(
                "public recovery accepts only the exact canonical A019 address and paths"
            )


def _require_thread_environment() -> None:
    invalid = {
        name: os.environ.get(name) for name in _THREAD_ENV_NAMES if os.environ.get(name) != "1"
    }
    if invalid:
        raise ValueError(f"all numerical thread variables must equal '1': {invalid!r}")


def _response_map(spec: RecoveryRunSpec, contract: G2Contract) -> G2ResponseMapIdentity:
    return G2ResponseMapIdentity(
        target_index=spec.response_target_index,
        paper_recovery=False,
        phi=contract.confirmatory_ar1,
        reliability=contract.confirmatory_reliability,
    )


def _expectations(
    spec: RecoveryRunSpec,
    contract: G2Contract,
) -> tuple[G2PanelCheckpointExpectation, G2PanelCheckpointExpectation]:
    return (
        G2PanelCheckpointExpectation(
            master_seed=spec.seed,
            stream=spec.stream,
            n_dates=spec.n_dates,
            panel_index=spec.panel_index,
            response_map=None,
        ),
        G2PanelCheckpointExpectation(
            master_seed=spec.seed,
            stream=spec.stream,
            n_dates=spec.n_dates,
            panel_index=spec.panel_index,
            response_map=_response_map(spec, contract),
        ),
    )


def _attempt_object(
    spec: RecoveryRunSpec,
    *,
    source_snapshot_sha256: str,
    runtime_sha256: str,
    contract: G2Contract,
) -> dict[str, object]:
    phase_id, scenario_id = contract.phase_scenario(spec.stream)
    value: dict[str, object] = {
        "schema_version": 1,
        "status": "started",
        "seed": spec.seed,
        "stream": spec.stream.value,
        "phase_id": phase_id,
        "scenario_id": scenario_id,
        "n_dates": spec.n_dates,
        "panel_index": spec.panel_index,
        "design_target_index": spec.design_target_index,
        "response_target_index": spec.response_target_index,
        "paper_recovery": False,
        "phi": contract.confirmatory_ar1.hex(),
        "reliability": contract.confirmatory_reliability.hex(),
        "source_snapshot_sha256": source_snapshot_sha256,
        "runtime_sha256": runtime_sha256,
        "checkpoint_root": spec.checkpoint_label,
        "scratch_root": spec.scratch_label,
        "hard_stops": {
            "artifact_bytes": spec.hard_artifact_bytes,
            "wall_seconds": spec.hard_wall_seconds.hex(),
            "peak_rss_bytes": spec.hard_peak_rss_bytes,
        },
        "supervision": {
            "poll_seconds": spec.poll_seconds.hex(),
            "timeout_method": _TIMEOUT_METHOD,
            "rss_normalization_method": _RSS_NORMALIZATION_METHOD,
        },
    }
    if frozenset(value) != _ATTEMPT_KEYS:
        raise AssertionError("internal attempt schema changed")
    return value


def _internal_spec_object(spec: RecoveryRunSpec, *, attempt_sha256: str) -> dict[str, object]:
    result = asdict(spec)
    result["repository_root"] = str(spec.repository_root.resolve(strict=True))
    result["result_root"] = str(spec.result_root.resolve(strict=True))
    result["checkpoint_root"] = str(spec.checkpoint_root.resolve(strict=True))
    result["scratch_root"] = str(spec.scratch_root.resolve(strict=True))
    result["stream"] = spec.stream.value
    result["attempt_sha256"] = attempt_sha256
    result["schema_version"] = 1
    return cast(dict[str, object], result)


def _spec_from_internal(value: dict[str, object]) -> tuple[RecoveryRunSpec, str]:
    expected = frozenset(
        (*RecoveryRunSpec.__dataclass_fields__, "attempt_sha256", "schema_version")
    )
    if frozenset(value) != expected or type(value["schema_version"]) is not int:
        raise ValueError("internal worker specification has an unexpected schema")
    if value["schema_version"] != 1:
        raise ValueError("internal worker specification schema is unsupported")
    attempt_sha256 = _require_sha256(value["attempt_sha256"], name="attempt digest")
    try:
        spec = RecoveryRunSpec(
            mode=cast(Literal["test", "public"], value["mode"]),
            repository_root=Path(cast(str, value["repository_root"])),
            result_root=Path(cast(str, value["result_root"])),
            checkpoint_root=Path(cast(str, value["checkpoint_root"])),
            scratch_root=Path(cast(str, value["scratch_root"])),
            seed=cast(int, value["seed"]),
            stream=G2Stream(cast(str, value["stream"])),
            n_dates=cast(int, value["n_dates"]),
            panel_index=cast(int, value["panel_index"]),
            design_target_index=cast(int, value["design_target_index"]),
            response_target_index=cast(int, value["response_target_index"]),
            expected_wall_seconds=cast(float, value["expected_wall_seconds"]),
            hard_wall_seconds=cast(float, value["hard_wall_seconds"]),
            expected_peak_rss_bytes=cast(int, value["expected_peak_rss_bytes"]),
            hard_peak_rss_bytes=cast(int, value["hard_peak_rss_bytes"]),
            hard_artifact_bytes=cast(int, value["hard_artifact_bytes"]),
            poll_seconds=cast(float, value["poll_seconds"]),
            require_clean_source=cast(bool, value["require_clean_source"]),
            checkpoint_label=cast(str, value["checkpoint_label"]),
            scratch_label=cast(str, value["scratch_label"]),
        )
    except (TypeError, ValueError) as error:
        raise ValueError("internal worker specification cannot be decoded") from error
    _validate_spec(spec)
    return spec, attempt_sha256


def _validate_attempt(
    attempt: dict[str, object],
    *,
    spec: RecoveryRunSpec,
    contract: G2Contract,
) -> None:
    expected = _attempt_object(
        spec,
        source_snapshot_sha256=_require_sha256(
            attempt.get("source_snapshot_sha256"),
            name="attempt source snapshot",
        ),
        runtime_sha256=_require_sha256(
            attempt.get("runtime_sha256"),
            name="attempt runtime",
        ),
        contract=contract,
    )
    if attempt != expected:
        raise ValueError("attempt receipt differs from the exact worker specification")


def _subprocess_environment(
    repository_root: Path,
    *,
    pycache_prefix: Path,
    child_capability_fd: int | None = None,
) -> dict[str, str]:
    environment = dict(os.environ)
    source_root = str(repository_root / "src")
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        source_root if not existing else f"{source_root}{os.pathsep}{existing}"
    )
    environment["PYTHONPYCACHEPREFIX"] = str(pycache_prefix)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.pop(_MAKE_LAUNCH_ENV, None)
    if child_capability_fd is None:
        environment.pop(_CHILD_CAPABILITY_ENV, None)
    else:
        environment[_CHILD_CAPABILITY_ENV] = str(child_capability_fd)
    return environment


def _child_capability_payload(
    *,
    role: Literal["worker", "fresh"],
    parent_pid: int,
    attempt_sha256: str,
    spec_sha256: str,
) -> bytes:
    if type(parent_pid) is not int or parent_pid <= 0:
        raise ValueError("child capability parent PID must be a positive exact integer")
    return _canonical_json_bytes(
        {
            "schema_version": 1,
            "role": role,
            "parent_pid": parent_pid,
            "attempt_sha256": _require_sha256(
                attempt_sha256,
                name="child capability attempt digest",
            ),
            "spec_sha256": _require_sha256(
                spec_sha256,
                name="child capability specification digest",
            ),
        }
    )


def _open_child_capability(
    *,
    role: Literal["worker", "fresh"],
    attempt_sha256: str,
    spec_bytes: bytes,
) -> int:
    read_descriptor, write_descriptor = os.pipe()
    try:
        payload = _child_capability_payload(
            role=role,
            parent_pid=os.getpid(),
            attempt_sha256=attempt_sha256,
            spec_sha256=_sha256(spec_bytes),
        )
        view = memoryview(payload)
        written = 0
        while written < len(view):
            count = os.write(write_descriptor, view[written:])
            if count <= 0:
                raise OSError("child capability write made no progress")
            written += count
    except BaseException:
        os.close(read_descriptor)
        raise
    finally:
        os.close(write_descriptor)
    return read_descriptor


def _require_anonymous_pipe_descriptor(
    descriptor: int,
    metadata: os.stat_result,
) -> tuple[int, int, int, int]:
    if not stat.S_ISFIFO(metadata.st_mode):
        raise ValueError("child capability descriptor must be an anonymous one-shot pipe")
    if sys.platform == "darwin":
        if metadata.st_dev != 0 or metadata.st_nlink != 0:
            raise ValueError("child capability pipe must be anonymous and non-reopenable")
    elif sys.platform.startswith("linux"):
        try:
            target = os.readlink(f"/proc/self/fd/{descriptor}")
        except OSError as error:
            raise ValueError("child capability pipe identity cannot be attested") from error
        pipe_inode = target[len("pipe:[") : -1]
        if (
            not target.startswith("pipe:[")
            or not target.endswith("]")
            or not pipe_inode.isdecimal()
        ):
            raise ValueError("child capability pipe must be anonymous and non-reopenable")
    else:
        raise ValueError("anonymous child capability pipes are unsupported on this platform")
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
    )


def _consume_child_capability(
    *,
    role: Literal["worker", "fresh"],
) -> _ChildCapability:
    descriptor_text = os.environ.pop(_CHILD_CAPABILITY_ENV, None)
    if (
        descriptor_text is None
        or not descriptor_text.isascii()
        or not descriptor_text.isdecimal()
        or str(int(descriptor_text)) != descriptor_text
    ):
        raise ValueError("private child role requires a supervisor-issued child capability")
    descriptor = int(descriptor_text)
    if descriptor < 3:
        raise ValueError("private child role received an invalid child capability descriptor")
    try:
        metadata = os.fstat(descriptor)
        identity_before = _require_anonymous_pipe_descriptor(descriptor, metadata)
        chunks: list[bytes] = []
        remaining = _MAX_CHILD_CAPABILITY_BYTES + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 4096))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        after = os.fstat(descriptor)
        identity_after = (
            after.st_dev,
            after.st_ino,
            after.st_mode,
            after.st_nlink,
        )
        if identity_after != identity_before:
            raise ValueError("child capability pipe identity changed while being consumed")
    finally:
        os.close(descriptor)
    if len(payload) > _MAX_CHILD_CAPABILITY_BYTES:
        raise ValueError("child capability exceeded its bounded size")
    value = _parse_canonical_payload(payload, name="child capability")
    expected_keys = frozenset(
        (
            "schema_version",
            "role",
            "parent_pid",
            "attempt_sha256",
            "spec_sha256",
        )
    )
    if frozenset(value) != expected_keys:
        raise ValueError("child capability has an unexpected schema")
    parent_pid = value["parent_pid"]
    if (
        value["schema_version"] != 1
        or value["role"] != role
        or type(parent_pid) is not int
        or parent_pid != os.getppid()
    ):
        raise ValueError("child capability is not bound to this role and immediate parent")
    return _ChildCapability(
        role=role,
        parent_pid=parent_pid,
        attempt_sha256=_require_sha256(
            value["attempt_sha256"],
            name="child capability attempt digest",
        ),
        spec_sha256=_require_sha256(
            value["spec_sha256"],
            name="child capability specification digest",
        ),
    )


def _worker_command(spec: RecoveryRunSpec, worker_spec_path: Path) -> list[str]:
    del spec
    return [
        sys.executable,
        "-B",
        "-m",
        "xid.g2_checkpoint_recovery",
        "_worker",
        str(worker_spec_path),
    ]


def _fresh_command(fresh_spec_path: Path) -> list[str]:
    return [
        sys.executable,
        "-B",
        "-m",
        "xid.g2_checkpoint_recovery",
        "_fresh",
        str(fresh_spec_path),
    ]


def _bytecode_policy(spec: RecoveryRunSpec, *, attempt_sha256: str) -> _BytecodePolicy:
    token = attempt_sha256[:24]
    supervisor_prefix = (
        spec.repository_root / _PUBLIC_SUPERVISOR_CACHE_LABEL
        if spec.mode == "public"
        else spec.scratch_root / f".pycache-supervisor-{token}"
    )
    return _BytecodePolicy(
        supervisor_prefix=supervisor_prefix,
        worker_prefix=spec.scratch_root / f".pycache-worker-{token}",
        fresh_prefix=spec.scratch_root / f".pycache-fresh-{token}",
    )


def _create_empty_cache_prefix(path: Path) -> None:
    try:
        os.mkdir(path, mode=0o700)
        metadata = os.lstat(path)
    except OSError as error:
        raise ValueError("bytecode cache prefix cannot be created exclusively") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("bytecode cache prefix must be a non-symlink directory")
    if any(path.iterdir()):
        raise ValueError("bytecode cache prefix must start empty")
    _fsync_directory(path.parent)


def _policy_record(
    spec: RecoveryRunSpec,
    *,
    attempt_sha256: str,
) -> dict[str, object]:
    policy = _bytecode_policy(spec, attempt_sha256=attempt_sha256)
    return {
        "schema_version": 1,
        "method": "unique-empty-pycache-prefix-plus-dont-write-bytecode",
        "supervisor_prefix": f"{spec.scratch_label}/{policy.supervisor_prefix.name}",
        "worker_prefix": f"{spec.scratch_label}/{policy.worker_prefix.name}",
        "fresh_prefix": f"{spec.scratch_label}/{policy.fresh_prefix.name}",
    }


def _prepare_bytecode_policy(
    spec: RecoveryRunSpec,
    *,
    attempt_sha256: str,
) -> _BytecodePolicy:
    policy = _bytecode_policy(spec, attempt_sha256=attempt_sha256)
    prefixes = [policy.worker_prefix, policy.fresh_prefix]
    if spec.mode == "test":
        prefixes.insert(0, policy.supervisor_prefix)
    else:
        _validate_supervisor_bootstrap(policy.supervisor_prefix)
    for prefix in prefixes:
        _create_empty_cache_prefix(prefix)
    _exclusive_write(
        spec.scratch_root / "bytecode-policy.json",
        _canonical_json_bytes(_policy_record(spec, attempt_sha256=attempt_sha256)),
    )
    sys.pycache_prefix = str(policy.supervisor_prefix)
    sys.dont_write_bytecode = True
    os.environ["PYTHONPYCACHEPREFIX"] = str(policy.supervisor_prefix)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    return policy


def _validate_policy_record(
    spec: RecoveryRunSpec,
    *,
    attempt_sha256: str,
) -> _BytecodePolicy:
    observed = _parse_canonical_object(spec.scratch_root / "bytecode-policy.json")
    expected = _policy_record(spec, attempt_sha256=attempt_sha256)
    if observed != expected:
        raise ValueError("bytecode policy record differs from the attempt-derived policy")
    return _bytecode_policy(spec, attempt_sha256=attempt_sha256)


def _validate_child_bytecode_prefix(path: Path) -> None:
    configured = os.environ.get("PYTHONPYCACHEPREFIX")
    if configured is None or Path(configured).resolve(strict=True) != path.resolve(strict=True):
        raise ValueError("child process bytecode cache prefix differs from the frozen policy")
    if sys.pycache_prefix is None or Path(sys.pycache_prefix).resolve(strict=True) != path.resolve(
        strict=True
    ):
        raise ValueError("interpreter bytecode cache prefix differs from its environment")
    if not sys.dont_write_bytecode or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise ValueError("child process must disable bytecode-cache writes")
    if any(path.iterdir()):
        raise ValueError("child process bytecode cache prefix was not empty at startup")


def _validate_supervisor_bootstrap(path: Path) -> None:
    if type(path) is not _CONCRETE_PATH_TYPE:
        raise TypeError("supervisor bytecode prefix must use the exact concrete path type")
    try:
        metadata = os.lstat(path)
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise ValueError("supervisor bytecode cache prefix does not exist") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("supervisor bytecode cache prefix must be a non-symlink directory")
    configured = os.environ.get("PYTHONPYCACHEPREFIX")
    if configured is None or Path(configured).resolve(strict=True) != resolved:
        raise ValueError("supervisor bytecode cache prefix differs from its launcher")
    if sys.pycache_prefix is None or Path(sys.pycache_prefix).resolve(strict=True) != resolved:
        raise ValueError("interpreter bytecode cache prefix differs from its launcher")
    if not sys.dont_write_bytecode or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise ValueError("supervisor launcher must disable bytecode-cache writes")
    if any(path.iterdir()):
        raise ValueError("supervisor bytecode cache prefix must remain empty")


def _require_cache_prefix_still_empty(path: Path) -> None:
    if any(path.iterdir()):
        raise ValueError("bytecode cache prefix was populated despite the no-write policy")


def _process_tree_rss_bytes_from_ps(snapshot: str, *, root_pid: int) -> int:
    """Sum RSS KiB over one PID and its complete descendant closure."""
    if type(snapshot) is not str or type(root_pid) is not int or root_pid <= 0:
        raise ValueError("process-tree RSS inputs have invalid exact types")
    rows: dict[int, tuple[int, int]] = {}
    for line in snapshot.splitlines():
        fields = line.split()
        if not fields:
            continue
        if len(fields) != 3:
            raise ValueError("ps RSS snapshot has an unexpected row")
        try:
            pid, parent_pid, rss_kib = (int(field) for field in fields)
        except ValueError as error:
            raise ValueError("ps RSS snapshot contains a non-integer") from error
        if pid <= 0 or parent_pid < 0 or rss_kib < 0 or pid in rows:
            raise ValueError("ps RSS snapshot contains invalid process coordinates")
        rows[pid] = (parent_pid, rss_kib)
    descendants = {root_pid}
    changed = True
    while changed:
        changed = False
        for pid, (parent_pid, _rss_kib) in rows.items():
            if pid not in descendants and parent_pid in descendants:
                descendants.add(pid)
                changed = True
    return sum(rows[pid][1] for pid in descendants if pid in rows) * 1024


def _sample_process_tree_rss(root_pid: int) -> int:
    completed = subprocess.run(
        ["ps", "-axo", "pid=,ppid=,rss="],
        check=True,
        capture_output=True,
        encoding="ascii",
        timeout=5.0,
    )
    return _process_tree_rss_bytes_from_ps(completed.stdout, root_pid=root_pid)


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    if not _process_group_exists(process.pid):
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    if process.poll() is None:
        with suppress(subprocess.TimeoutExpired):
            process.wait(timeout=2.0)
    if _wait_for_process_group_exit(process.pid, timeout=2.0):
        return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    if process.poll() is None:
        with suppress(subprocess.TimeoutExpired):
            process.wait(timeout=5.0)
    if not _wait_for_process_group_exit(process.pid, timeout=5.0):
        raise RecoveryRunFailed("worker process group survived SIGKILL")


def _wait_for_process_group_exit(process_group_id: int, *, timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while _process_group_exists(process_group_id):
        now = time.monotonic()
        if now >= deadline:
            return False
        time.sleep(min(0.05, deadline - now))
    return True


def _process_group_exists(process_group_id: int) -> bool:
    try:
        os.killpg(process_group_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _supervise_worker(
    spec: RecoveryRunSpec,
    *,
    command: list[str],
    stdout_path: Path,
    stderr_path: Path,
    worker_pycache_prefix: Path,
    child_capability_fd: int,
) -> _SupervisionEvidence:
    started = time.monotonic()
    peak_rss = 0
    failure_stage: str | None = None
    failure_message: str | None = None
    returncode: int | None = None
    process: subprocess.Popen[bytes] | None = None
    try:
        with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
            process = subprocess.Popen(
                command,
                cwd=spec.repository_root,
                env=_subprocess_environment(
                    spec.repository_root,
                    pycache_prefix=worker_pycache_prefix,
                    child_capability_fd=child_capability_fd,
                ),
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                start_new_session=True,
                pass_fds=(child_capability_fd,),
            )
            while True:
                elapsed = time.monotonic() - started
                returncode = process.poll()
                if returncode is not None:
                    break
                if elapsed > spec.hard_wall_seconds:
                    failure_stage = "wall_timeout"
                    failure_message = "worker exceeded the hard wall-clock stop"
                    _terminate_process_group(process)
                    break
                try:
                    observed_rss = _sample_process_tree_rss(process.pid)
                except (OSError, ValueError, subprocess.SubprocessError) as error:
                    if spec.mode == "test" and isinstance(error, PermissionError):
                        # The Codex filesystem/process sandbox denies ``ps`` even
                        # though the same command is available on the target Mac
                        # and hosted CI.  The public one-shot remains fail-closed.
                        observed_rss = 0
                    else:
                        failure_stage = "rss_poll"
                        failure_message = f"worker RSS polling failed: {type(error).__name__}"
                        _terminate_process_group(process)
                        break
                peak_rss = max(peak_rss, observed_rss)
                if observed_rss > spec.hard_peak_rss_bytes:
                    failure_stage = "rss_stop"
                    failure_message = "worker exceeded the first observed RSS hard stop"
                    _terminate_process_group(process)
                    break
                if stdout_path.stat().st_size > _MAX_STDIO_BYTES or (
                    stderr_path.stat().st_size > _MAX_STDIO_BYTES
                ):
                    failure_stage = "stdio_stop"
                    failure_message = "worker stdout or stderr exceeded its bounded cap"
                    _terminate_process_group(process)
                    break
                time.sleep(spec.poll_seconds)
            returncode = process.wait(timeout=5.0)
            if stdout_path.stat().st_size > _MAX_STDIO_BYTES or (
                stderr_path.stat().st_size > _MAX_STDIO_BYTES
            ):
                failure_stage = failure_stage or "stdio_stop"
                failure_message = failure_message or (
                    "worker stdout or stderr exceeded its bounded cap"
                )
            if _process_group_exists(process.pid):
                failure_stage = failure_stage or "process_group_leak"
                failure_message = failure_message or (
                    "worker exited while descendants remained in its process group"
                )
                _terminate_process_group(process)
    finally:
        if process is not None and _process_group_exists(process.pid):
            _terminate_process_group(process)
    return _SupervisionEvidence(
        elapsed_seconds=time.monotonic() - started,
        peak_rss_bytes=peak_rss,
        worker_returncode=returncode,
        failure_stage=failure_stage,
        failure_message=failure_message,
    )


def _file_sha256_or_empty(path: Path) -> str:
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except FileNotFoundError:
        return _sha256(b"")
    digest = hashlib.sha256()
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"{path.name} must be a regular file")
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    if (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
        before.st_ctime_ns,
    ) != (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    ):
        raise ValueError(f"{path.name} changed while it was being hashed")
    return digest.hexdigest()


def _entry_exists(path: Path) -> bool:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return False
    return True


def _hard_stop_object(
    spec: RecoveryRunSpec,
    *,
    artifact_bytes: int | None,
    elapsed_seconds: float,
    peak_rss_bytes: int,
) -> dict[str, object]:
    artifact_observed = artifact_bytes if artifact_bytes is not None else 0
    return {
        "artifact_bytes": {
            "limit": spec.hard_artifact_bytes,
            "observed": artifact_observed,
            "passed": artifact_bytes is not None and artifact_observed < spec.hard_artifact_bytes,
        },
        "wall_seconds": {
            "limit": spec.hard_wall_seconds.hex(),
            "observed": elapsed_seconds.hex(),
            "passed": elapsed_seconds <= spec.hard_wall_seconds,
        },
        "peak_rss_bytes": {
            "limit": spec.hard_peak_rss_bytes,
            "observed": peak_rss_bytes,
            "passed": peak_rss_bytes <= spec.hard_peak_rss_bytes,
        },
    }


def _publish_failure(
    spec: RecoveryRunSpec,
    *,
    attempt_sha256: str,
    supervision: _SupervisionEvidence,
    stdout_path: Path,
    stderr_path: Path,
    failure_stage: str,
    failure: BaseException,
    artifact_bytes: int | None = None,
) -> None:
    failure_path = spec.result_root / "failure.json"
    marker_path = spec.result_root / "_FAILURE"
    success_marker_path = spec.result_root / "_SUCCESS"
    if (
        _entry_exists(success_marker_path)
        or _entry_exists(failure_path)
        or _entry_exists(marker_path)
    ):
        return
    message = str(failure).replace("\x00", "")[:1000]
    value: dict[str, object] = {
        "schema_version": 1,
        "status": "failed",
        "attempt_sha256": attempt_sha256,
        "failure_stage": failure_stage,
        "failure_type": type(failure).__name__,
        "message": message,
        "worker_returncode": supervision.worker_returncode,
        "elapsed_seconds": supervision.elapsed_seconds.hex(),
        "peak_rss_bytes": supervision.peak_rss_bytes,
        "timeout_method": _TIMEOUT_METHOD,
        "rss_normalization_method": _RSS_NORMALIZATION_METHOD,
        "hard_stops": _hard_stop_object(
            spec,
            artifact_bytes=artifact_bytes,
            elapsed_seconds=supervision.elapsed_seconds,
            peak_rss_bytes=supervision.peak_rss_bytes,
        ),
        "stdout_sha256": _file_sha256_or_empty(stdout_path),
        "stderr_sha256": _file_sha256_or_empty(stderr_path),
    }
    if frozenset(value) != _FAILURE_KEYS:
        raise AssertionError("internal failure schema changed")
    failure_bytes = _canonical_json_bytes(value)
    _exclusive_write(failure_path, failure_bytes)
    if _entry_exists(success_marker_path):
        return
    _exclusive_write(
        marker_path,
        _canonical_json_bytes(
            {
                "schema_version": 1,
                "status": "failed",
                "failure_sha256": _sha256(failure_bytes),
                "complete": True,
            }
        ),
    )


def _validate_exact_hash_object(
    value: object,
    *,
    keys: frozenset[str],
    name: str,
) -> dict[str, str]:
    if type(value) is not dict or frozenset(value) != keys:
        raise ValueError(f"{name} has an unexpected schema")
    result = cast(dict[str, object], value)
    return {key: _require_sha256(result[key], name=f"{name}.{key}") for key in keys}


def _validate_byte_object(value: object, *, name: str) -> dict[str, int]:
    keys = _HASH_OBJECT_KEYS["bytes"]
    if type(value) is not dict or frozenset(value) != keys:
        raise ValueError(f"{name} has an unexpected schema")
    result: dict[str, int] = {}
    table = cast(dict[str, object], value)
    for key in keys:
        item = table[key]
        if type(item) is not int or item < 0:
            raise ValueError(f"{name}.{key} must be a nonnegative exact integer")
        result[key] = item
    if result["combined"] != result["base"] + result["cell"]:
        raise ValueError(f"{name} combined count is inconsistent")
    return result


def _validate_worker_result(
    value: dict[str, object],
    *,
    spec: RecoveryRunSpec,
    attempt_sha256: str,
    contract: G2Contract,
    source_snapshot_sha256: str,
    runtime_sha256: str,
) -> dict[str, object]:
    if frozenset(value) != _WORKER_RESULT_KEYS:
        raise ValueError("worker result has an unexpected schema")
    phase_id, scenario_id = contract.phase_scenario(spec.stream)
    exact_scalars = {
        "schema_version": 1,
        "status": "passed",
        "attempt_sha256": attempt_sha256,
        "seed": spec.seed,
        "stream": spec.stream.value,
        "phase_id": phase_id,
        "scenario_id": scenario_id,
        "n_dates": spec.n_dates,
        "panel_index": spec.panel_index,
        "source_snapshot_sha256": source_snapshot_sha256,
        "runtime_sha256": runtime_sha256,
        "fresh_process_rng_draw_count": 0,
    }
    for key, expected in exact_scalars.items():
        current = value[key]
        if type(current) is not type(expected) or current != expected:
            raise ValueError(f"worker result {key} differs from the attempt")
    for key in ("base_artifact_sha256", "cell_artifact_sha256"):
        _require_sha256(value[key], name=f"worker result {key}")
    array_before = _validate_exact_hash_object(
        value["array_sha256_before"],
        keys=_HASH_OBJECT_KEYS["array"],
        name="array_sha256_before",
    )
    array_after = _validate_exact_hash_object(
        value["array_sha256_after"],
        keys=_HASH_OBJECT_KEYS["array"],
        name="array_sha256_after",
    )
    receipt_before = _validate_exact_hash_object(
        value["receipt_sha256_before"],
        keys=_HASH_OBJECT_KEYS["receipt"],
        name="receipt_sha256_before",
    )
    receipt_after = _validate_exact_hash_object(
        value["receipt_sha256_after"],
        keys=_HASH_OBJECT_KEYS["receipt"],
        name="receipt_sha256_after",
    )
    design_before = _validate_exact_hash_object(
        value["design_digest_sha256_before"],
        keys=_HASH_OBJECT_KEYS["design"],
        name="design_digest_sha256_before",
    )
    design_after = _validate_exact_hash_object(
        value["design_digest_sha256_after"],
        keys=_HASH_OBJECT_KEYS["design"],
        name="design_digest_sha256_after",
    )
    coefficients_before = _validate_exact_hash_object(
        value["coefficient_sha256_before"],
        keys=_HASH_OBJECT_KEYS["coefficient"],
        name="coefficient_sha256_before",
    )
    coefficients_after = _validate_exact_hash_object(
        value["coefficient_sha256_after"],
        keys=_HASH_OBJECT_KEYS["coefficient"],
        name="coefficient_sha256_after",
    )
    fresh = _validate_exact_hash_object(
        value["fresh_process_coefficient_sha256"],
        keys=_HASH_OBJECT_KEYS["coefficient"],
        name="fresh_process_coefficient_sha256",
    )
    if array_before != array_after:
        raise ValueError("worker array hashes changed across recovery")
    if receipt_before != receipt_after:
        raise ValueError("worker receipt hashes changed across recovery")
    if design_before != design_after:
        raise ValueError("worker design digests changed across recovery")
    if coefficients_before != coefficients_after or coefficients_after != fresh:
        raise ValueError("worker coefficient hashes changed across recovery")
    expected_shapes = {
        "homogeneous": [3],
        "observable": [contract.n_assets, contract.n_assets],
        "oracle": [contract.n_assets, contract.n_assets],
    }
    expected_finite = {key: True for key in _HASH_OBJECT_KEYS["coefficient"]}
    if value["coefficient_shapes"] != expected_shapes:
        raise ValueError("worker coefficient shapes differ from the sealed contract")
    if value["coefficient_finite"] != expected_finite:
        raise ValueError("worker reported a nonfinite coefficient")
    logical = _validate_byte_object(value["artifact_logical_bytes"], name="logical bytes")
    allocated = _validate_byte_object(
        value["artifact_allocated_bytes"],
        name="allocated bytes",
    )
    if max(logical["combined"], allocated["combined"]) >= spec.hard_artifact_bytes:
        raise ValueError("worker artifacts reached the strict byte hard stop")
    return value


def _result_from_worker(
    worker: dict[str, object],
    *,
    spec: RecoveryRunSpec,
    supervision: _SupervisionEvidence,
) -> dict[str, object]:
    result = {key: value for key, value in worker.items() if key in _RESULT_KEYS}
    logical = cast(dict[str, int], worker["artifact_logical_bytes"])
    allocated = cast(dict[str, int], worker["artifact_allocated_bytes"])
    artifact_observed = max(logical["combined"], allocated["combined"])
    result.update(
        {
            "elapsed_seconds": supervision.elapsed_seconds.hex(),
            "timeout_method": _TIMEOUT_METHOD,
            "peak_rss_bytes": supervision.peak_rss_bytes,
            "rss_normalization_method": _RSS_NORMALIZATION_METHOD,
            "hard_stops": _hard_stop_object(
                spec,
                artifact_bytes=artifact_observed,
                elapsed_seconds=supervision.elapsed_seconds,
                peak_rss_bytes=supervision.peak_rss_bytes,
            ),
        }
    )
    if frozenset(result) != _RESULT_KEYS:
        raise AssertionError("internal result schema changed")
    hard_stops = cast(dict[str, dict[str, object]], result["hard_stops"])
    if not all(item["passed"] is True for item in hard_stops.values()):
        raise ValueError("supervisor hard-stop evidence did not pass")
    return result


def _prepare_scratch_root(spec: RecoveryRunSpec) -> Path:
    if spec.mode == "test":
        return _ensure_directory(spec.scratch_root, empty=True, name="scratch root")
    try:
        metadata = os.lstat(spec.scratch_root)
    except OSError as error:
        raise ValueError("public scratch root must be prepared by the Make launcher") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("public scratch root must be a non-symlink directory")
    bootstrap = spec.repository_root / _PUBLIC_SUPERVISOR_CACHE_LABEL
    entries = tuple(spec.scratch_root.iterdir())
    if entries != (bootstrap,):
        raise ValueError("public scratch root must contain only its exact empty bootstrap prefix")
    _validate_supervisor_bootstrap(bootstrap)
    return _canonical_path_identity(spec.scratch_root, strict=True, name="scratch root")


def _preflight(spec: RecoveryRunSpec) -> tuple[G2Contract, str, str]:
    _validate_spec(spec)
    _require_thread_environment()
    result_root = _ensure_directory(spec.result_root, empty=False, name="result root")
    for name in ("attempt.json", "result.json", "_SUCCESS", "failure.json", "_FAILURE"):
        if (result_root / name).exists():
            raise FileExistsError("recovery attempt is consumed and immutable")
    if any(result_root.iterdir()):
        raise ValueError("result root contains an unexpected pre-attempt entry")
    _ensure_directory(spec.checkpoint_root, empty=True, name="checkpoint root")
    _prepare_scratch_root(spec)
    contract = load_g2_contract(spec.repository_root)
    authority = TestRngNamespace.from_contract(contract, spec.seed)
    base_expected, _cell_expected = _expectations(spec, contract)
    environment = inspect_g2_checkpoint_environment(
        expected=base_expected,
        contract=contract,
        authority=authority,
        repository_root=spec.repository_root,
    )
    if spec.require_clean_source and not environment.declared_paths_clean:
        raise ValueError("public A019 requires a clean declared execution-source snapshot")
    return (
        contract,
        environment.source_snapshot_sha256,
        environment.runtime_sha256,
    )


def _require_worker_execution_identity(
    spec: RecoveryRunSpec,
    *,
    attempt: dict[str, object],
    contract: G2Contract,
) -> tuple[
    TestRngNamespace,
    G2PanelCheckpointExpectation,
    G2PanelCheckpointExpectation,
    G2CheckpointEnvironmentIdentity,
]:
    authority = TestRngNamespace.from_contract(contract, spec.seed)
    base_expected, cell_expected = _expectations(spec, contract)
    environment = inspect_g2_checkpoint_environment(
        expected=base_expected,
        contract=contract,
        authority=authority,
        repository_root=spec.repository_root,
    )
    attempted_source = _require_sha256(
        attempt.get("source_snapshot_sha256"),
        name="attempt source snapshot",
    )
    attempted_runtime = _require_sha256(
        attempt.get("runtime_sha256"),
        name="attempt runtime",
    )
    if environment.source_snapshot_sha256 != attempted_source:
        raise ValueError("current source identity differs from the immutable attempt")
    if environment.runtime_sha256 != attempted_runtime:
        raise ValueError("current runtime identity differs from the immutable attempt")
    if spec.require_clean_source and not environment.declared_paths_clean:
        raise ValueError("public A019 source became dirty after supervisor preflight")
    return authority, base_expected, cell_expected, environment


def _run_supervisor(spec: RecoveryRunSpec) -> dict[str, object]:
    """Consume one immutable attempt and supervise its process tree."""
    _validate_spec(spec)
    if spec.mode == "public":
        _validate_supervisor_bootstrap(spec.repository_root / _PUBLIC_SUPERVISOR_CACHE_LABEL)
    attempt_path = spec.result_root / "attempt.json"
    if attempt_path.exists():
        raise FileExistsError("recovery attempt is consumed and immutable")
    contract, source_snapshot_sha256, runtime_sha256 = _preflight(spec)
    attempt = _attempt_object(
        spec,
        source_snapshot_sha256=source_snapshot_sha256,
        runtime_sha256=runtime_sha256,
        contract=contract,
    )
    attempt_bytes = _canonical_json_bytes(attempt)
    _exclusive_write(attempt_path, attempt_bytes)
    attempt_sha256 = _sha256(attempt_bytes)
    worker_spec_path = spec.scratch_root / "_worker-spec.json"
    worker_result_path = spec.scratch_root / "_worker-result.json"
    stdout_path = spec.scratch_root / "worker.stdout"
    stderr_path = spec.scratch_root / "worker.stderr"
    supervision = _SupervisionEvidence(0.0, 0, None, None, None)
    try:
        bytecode_policy = _prepare_bytecode_policy(
            spec,
            attempt_sha256=attempt_sha256,
        )
        worker_spec_bytes = _canonical_json_bytes(
            _internal_spec_object(spec, attempt_sha256=attempt_sha256)
        )
        _exclusive_write(worker_spec_path, worker_spec_bytes)
        capability_fd = _open_child_capability(
            role="worker",
            attempt_sha256=attempt_sha256,
            spec_bytes=worker_spec_bytes,
        )
        try:
            supervision = _supervise_worker(
                spec,
                command=_worker_command(spec, worker_spec_path),
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                worker_pycache_prefix=bytecode_policy.worker_prefix,
                child_capability_fd=capability_fd,
            )
        finally:
            os.close(capability_fd)
        _require_cache_prefix_still_empty(bytecode_policy.supervisor_prefix)
        _require_cache_prefix_still_empty(bytecode_policy.worker_prefix)
        if supervision.failure_stage is not None:
            raise RecoveryRunFailed(supervision.failure_message or "worker supervision failed")
        if supervision.worker_returncode != 0:
            raise RecoveryRunFailed(
                f"worker returned nonzero status {supervision.worker_returncode}"
            )
        worker = _parse_canonical_object(
            worker_result_path,
            exact_keys=_WORKER_RESULT_KEYS,
        )
        validated = _validate_worker_result(
            worker,
            spec=spec,
            attempt_sha256=attempt_sha256,
            contract=contract,
            source_snapshot_sha256=source_snapshot_sha256,
            runtime_sha256=runtime_sha256,
        )
        result = _result_from_worker(validated, spec=spec, supervision=supervision)
        result_bytes = _canonical_json_bytes(result)
        _exclusive_write(spec.result_root / "result.json", result_bytes)
        _exclusive_write(
            spec.result_root / "_SUCCESS",
            _canonical_json_bytes(
                {
                    "schema_version": 1,
                    "status": "passed",
                    "result_sha256": _sha256(result_bytes),
                    "complete": True,
                }
            ),
        )
        return result
    except BaseException as error:
        stage = supervision.failure_stage or (
            "worker_return" if supervision.worker_returncode not in (None, 0) else "supervisor"
        )
        if not isinstance(error, _PublicationStateUncertain):
            with suppress(BaseException):
                _publish_failure(
                    spec,
                    attempt_sha256=attempt_sha256,
                    supervision=supervision,
                    stdout_path=stdout_path,
                    stderr_path=stderr_path,
                    failure_stage=stage,
                    failure=error,
                )
        if isinstance(error, RecoveryRunFailed):
            raise
        raise RecoveryRunFailed(f"{stage} failed: {error}") from error


def _numeric_sha256(values: NDArray[np.float64]) -> str:
    packed = values.astype("<f8", copy=False)
    return _sha256(packed.tobytes(order="C"))


def _receipt_payload(receipt: G2DateReceipt) -> list[object]:
    provenance = receipt.provenance
    response = receipt.response_map
    return [
        provenance.master_seed,
        provenance.stream.value,
        provenance.phase_id,
        provenance.scenario_id,
        provenance.n_dates,
        provenance.panel_index,
        provenance.date_index,
        receipt.base_identity,
        response.target_index,
        response.paper_recovery,
        response.phi.hex(),
        response.reliability.hex(),
        receipt.date_content_sha256,
    ]


def _tuple_sha256(values: object) -> str:
    return _sha256(_canonical_json_bytes(values))


def _panel_hashes(
    base: SmoothBasePanelMoments,
    cell: SmoothCellPanelMoments,
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    arrays = {
        "base_x0tx0_upper": _numeric_sha256(base.x0tx0_upper),
        "cell_x0ty": _numeric_sha256(cell.x0ty),
        "cell_yty_upper": _numeric_sha256(cell.yty_upper),
    }
    receipts = {
        "base_source_receipts": _tuple_sha256(
            [_receipt_payload(cast(G2DateReceipt, item)) for item in base.source_receipts]
        ),
        "cell_design_receipts": _tuple_sha256(
            [_receipt_payload(cast(G2DateReceipt, item)) for item in cell.design_receipts]
        ),
        "cell_response_receipts": _tuple_sha256(
            [_receipt_payload(cast(G2DateReceipt, item)) for item in cell.response_receipts]
        ),
    }
    designs = {
        "base_design_sha256s": _tuple_sha256(list(base.design_sha256s)),
        "cell_design_sha256s": _tuple_sha256(list(cell.design_sha256s)),
    }
    return arrays, receipts, designs


def _fit_outputs(
    base: SmoothBasePanelMoments,
    cell: SmoothCellPanelMoments,
    *,
    contract: G2Contract,
    response_map: G2ResponseMapIdentity,
) -> tuple[dict[str, str], dict[str, list[int]], dict[str, bool]]:
    aggregate = aggregate_contract_smooth_moments(
        base,
        cell,
        np.ones(len(base.date_indices), dtype=np.float64),
    )
    coefficient_values: dict[str, NDArray[np.float64]] = {
        "homogeneous": fit_homogeneous_ols(
            aggregate,
            reliability=contract.confirmatory_reliability,
            expected_response_map=response_map,
            contract=contract,
        ).slopes,
        "observable": fit_condition_ridge(
            aggregate,
            flow_view=G2FlowView.OBSERVABLE,
            reliability=contract.confirmatory_reliability,
            expected_response_map=response_map,
            contract=contract,
        ).coefficients,
        "oracle": fit_condition_ridge(
            aggregate,
            flow_view=G2FlowView.ORACLE,
            reliability=contract.confirmatory_reliability,
            expected_response_map=response_map,
            contract=contract,
        ).coefficients,
    }
    hashes = {key: _numeric_sha256(value) for key, value in coefficient_values.items()}
    shapes = {key: list(value.shape) for key, value in coefficient_values.items()}
    finite = {key: bool(np.all(np.isfinite(value))) for key, value in coefficient_values.items()}
    return hashes, shapes, finite


def _self_peak_rss_bytes() -> int:
    observed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    multiplier = 1 if sys.platform == "darwin" else 1024
    return int(observed) * multiplier


def _path_usage(path: Path) -> tuple[int, int]:
    logical = 0
    allocated = 0
    pending = [path]
    while pending:
        current = pending.pop()
        metadata = os.lstat(current)
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError("artifact tree contains a symlink")
        logical += metadata.st_size
        allocated += metadata.st_blocks * 512
        if stat.S_ISDIR(metadata.st_mode):
            with os.scandir(current) as entries:
                pending.extend(Path(entry.path) for entry in entries)
        elif not stat.S_ISREG(metadata.st_mode):
            raise ValueError("artifact tree contains a non-regular entry")
    return logical, allocated


def _artifact_byte_objects(
    base: G2CheckpointEvidence,
    cell: G2CheckpointEvidence,
) -> tuple[dict[str, int], dict[str, int]]:
    base_logical, base_allocated = _path_usage(base.artifact_path)
    cell_logical, cell_allocated = _path_usage(cell.artifact_path)
    return (
        {
            "base": base_logical,
            "cell": cell_logical,
            "combined": base_logical + cell_logical,
        },
        {
            "base": base_allocated,
            "cell": cell_allocated,
            "combined": base_allocated + cell_allocated,
        },
    )


def _patch_rng_draws_to_fail(
    fingerprint: G2RuntimeFingerprint,
) -> list[int]:
    draw_count = [0]

    def forbidden(*_args: object, **_kwargs: object) -> NoReturn:
        draw_count[0] += 1
        raise AssertionError("checkpoint recovery attempted an RNG draw or constructor")

    setattr(  # noqa: B010
        checkpoint_codec,
        "current_g2_runtime_fingerprint",
        lambda: fingerprint,
    )
    setattr(TestRngNamespace, "draw_standard_normal", forbidden)  # noqa: B010
    setattr(TestRngNamespace, "draw_bootstrap_weights", forbidden)  # noqa: B010
    setattr(TestRngNamespace, "draw_base_normals", forbidden)  # noqa: B010
    setattr(np.random, "default_rng", forbidden)  # noqa: B010
    setattr(np.random, "SeedSequence", forbidden)  # noqa: B010
    setattr(np.random, "PCG64DXSM", forbidden)  # noqa: B010
    setattr(np.random, "Generator", forbidden)  # noqa: B010
    return draw_count


def _load_and_fit_without_draws(
    spec: RecoveryRunSpec,
    *,
    contract: G2Contract,
    authority: TestRngNamespace,
    base_expected: G2PanelCheckpointExpectation,
    cell_expected: G2PanelCheckpointExpectation,
) -> tuple[
    SmoothBasePanelMoments,
    SmoothCellPanelMoments,
    G2CheckpointEvidence,
    G2CheckpointEvidence,
    dict[str, str],
    dict[str, list[int]],
    dict[str, bool],
]:
    loaded_base = load_contract_base_panel_checkpoint(
        spec.checkpoint_root,
        expected=base_expected,
        authority=authority,
        contract=contract,
        repository_root=spec.repository_root,
    )
    loaded_cell = load_contract_cell_panel_checkpoint(
        spec.checkpoint_root,
        base_checkpoint=loaded_base,
        expected=cell_expected,
        authority=authority,
        contract=contract,
        repository_root=spec.repository_root,
    )
    response_map = cell_expected.response_map
    if response_map is None:
        raise AssertionError("cell expectation lost its response map")
    coefficients, shapes, finite = _fit_outputs(
        loaded_base.panel,
        loaded_cell.panel,
        contract=contract,
        response_map=response_map,
    )
    return (
        loaded_base.panel,
        loaded_cell.panel,
        loaded_base.evidence,
        loaded_cell.evidence,
        coefficients,
        shapes,
        finite,
    )


def _fresh_spec_object(
    spec: RecoveryRunSpec,
    *,
    attempt_sha256: str,
) -> dict[str, object]:
    return _internal_spec_object(spec, attempt_sha256=attempt_sha256)


def _run_fresh_process(
    spec: RecoveryRunSpec,
    *,
    attempt_sha256: str,
) -> tuple[dict[str, str], int]:
    bytecode_policy = _validate_policy_record(
        spec,
        attempt_sha256=attempt_sha256,
    )
    fresh_spec_path = spec.scratch_root / "_fresh-spec.json"
    fresh_spec_bytes = _canonical_json_bytes(
        _fresh_spec_object(spec, attempt_sha256=attempt_sha256)
    )
    _exclusive_write(fresh_spec_path, fresh_spec_bytes)
    capability_fd = _open_child_capability(
        role="fresh",
        attempt_sha256=attempt_sha256,
        spec_bytes=fresh_spec_bytes,
    )
    try:
        completed = subprocess.run(
            _fresh_command(fresh_spec_path),
            cwd=spec.repository_root,
            env=_subprocess_environment(
                spec.repository_root,
                pycache_prefix=bytecode_policy.fresh_prefix,
                child_capability_fd=capability_fd,
            ),
            check=True,
            capture_output=True,
            timeout=min(60.0, spec.hard_wall_seconds),
            pass_fds=(capability_fd,),
        )
    finally:
        os.close(capability_fd)
    _require_cache_prefix_still_empty(bytecode_policy.fresh_prefix)
    if len(completed.stdout) > _MAX_STDIO_BYTES or len(completed.stderr) > _MAX_STDIO_BYTES:
        raise ValueError("fresh-process output exceeded its bounded cap")
    try:
        value = json.loads(completed.stdout.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("fresh process returned invalid JSON") from error
    if type(value) is not dict or _canonical_json_bytes(value) != completed.stdout:
        raise ValueError("fresh process returned noncanonical JSON")
    result = cast(dict[str, object], value)
    if frozenset(result) != frozenset(("coefficient_sha256", "rng_draw_count")):
        raise ValueError("fresh process returned an unexpected schema")
    hashes = _validate_exact_hash_object(
        result["coefficient_sha256"],
        keys=_HASH_OBJECT_KEYS["coefficient"],
        name="fresh coefficient hashes",
    )
    draw_count = result["rng_draw_count"]
    if type(draw_count) is not int or draw_count != 0:
        raise ValueError("fresh process attempted an RNG draw")
    return hashes, draw_count


def _run_primary_worker(spec: RecoveryRunSpec, *, attempt_sha256: str) -> dict[str, object]:
    bytecode_policy = _validate_policy_record(
        spec,
        attempt_sha256=attempt_sha256,
    )
    _validate_child_bytecode_prefix(bytecode_policy.worker_prefix)
    attempt_path = spec.result_root / "attempt.json"
    attempt_bytes = _read_stable_regular_file(attempt_path, maximum=_MAX_JSON_BYTES)
    attempt = _parse_canonical_payload(
        attempt_bytes,
        name=attempt_path.name,
        exact_keys=_ATTEMPT_KEYS,
    )
    if _sha256(attempt_bytes) != attempt_sha256:
        raise ValueError("worker attempt digest differs from its supervisor specification")
    contract = load_g2_contract(spec.repository_root)
    _validate_attempt(attempt, spec=spec, contract=contract)
    authority, base_expected, cell_expected, _environment = _require_worker_execution_identity(
        spec,
        attempt=attempt,
        contract=contract,
    )
    claim_path = spec.scratch_root / "worker-claim.json"
    _exclusive_write(
        claim_path,
        _canonical_json_bytes(
            {
                "schema_version": 1,
                "status": "claimed",
                "attempt_sha256": attempt_sha256,
                "pid": os.getpid(),
                "pycache_prefix": (f"{spec.scratch_label}/{bytecode_policy.worker_prefix.name}"),
            }
        ),
    )
    design_cell = build_cell(contract, target_index=spec.design_target_index)
    response_cell = build_cell(contract, target_index=spec.response_target_index)
    base_moments = []
    cell_moments = []
    worker_started = time.monotonic()
    for date_index in range(spec.n_dates):
        raw = authority.draw_base_normals(
            stream=spec.stream,
            n_dates=spec.n_dates,
            panel_index=spec.panel_index,
            date_index=date_index,
        )
        design_date = transform_date(
            raw,
            design_cell,
            contract=contract,
            phi=contract.confirmatory_ar1,
            reliability=contract.confirmatory_reliability,
        )
        response_date = transform_date(
            raw,
            response_cell,
            contract=contract,
            phi=contract.confirmatory_ar1,
            reliability=contract.confirmatory_reliability,
        )
        design = build_contract_smooth_date_design(design_date, contract=contract)
        cell_moment = build_contract_cell_date_moments(
            design,
            response_date,
            contract=contract,
        )
        base_moments.append(design.base_moments)
        cell_moments.append(cell_moment)
        del raw, design_date, response_date, design, cell_moment
    base_panel = stack_contract_base_moments(base_moments)
    cell_panel = stack_contract_cell_moments(cell_moments)
    del base_moments, cell_moments, design_cell, response_cell
    gc.collect()
    before_arrays, before_receipts, before_designs = _panel_hashes(
        base_panel,
        cell_panel,
    )
    response_map = cell_expected.response_map
    if response_map is None:
        raise AssertionError("worker cell expectation lost its response map")
    before_coefficients, coefficient_shapes, coefficient_finite = _fit_outputs(
        base_panel,
        cell_panel,
        contract=contract,
        response_map=response_map,
    )
    if not all(coefficient_finite.values()):
        raise ValueError("pre-checkpoint coefficient contains a nonfinite value")
    base_telemetry = G2CheckpointTelemetry(
        task_elapsed_seconds=time.monotonic() - worker_started,
        cumulative_elapsed_seconds=time.monotonic() - worker_started,
        peak_rss_bytes=_self_peak_rss_bytes(),
    )
    base_evidence = write_contract_base_panel_checkpoint(
        spec.checkpoint_root,
        base_panel,
        expected=base_expected,
        authority=authority,
        contract=contract,
        repository_root=spec.repository_root,
        telemetry=base_telemetry,
    )
    cell_started = time.monotonic()
    cell_telemetry = G2CheckpointTelemetry(
        task_elapsed_seconds=time.monotonic() - cell_started,
        cumulative_elapsed_seconds=time.monotonic() - worker_started,
        peak_rss_bytes=_self_peak_rss_bytes(),
    )
    cell_evidence = write_contract_cell_panel_checkpoint(
        spec.checkpoint_root,
        base_panel,
        cell_panel,
        base_checkpoint=base_evidence,
        expected=cell_expected,
        authority=authority,
        contract=contract,
        repository_root=spec.repository_root,
        telemetry=cell_telemetry,
    )
    artifact_logical_bytes, artifact_allocated_bytes = _artifact_byte_objects(
        base_evidence,
        cell_evidence,
    )
    if (
        max(
            artifact_logical_bytes["combined"],
            artifact_allocated_bytes["combined"],
        )
        >= spec.hard_artifact_bytes
    ):
        raise ValueError("combined checkpoint artifacts reached the strict byte hard stop")
    base_artifact_sha256 = base_evidence.artifact_sha256
    cell_artifact_sha256 = cell_evidence.artifact_sha256
    source_snapshot_sha256 = base_evidence.source_snapshot_sha256
    runtime_sha256 = base_evidence.runtime_sha256
    if (
        cell_evidence.source_snapshot_sha256 != source_snapshot_sha256
        or cell_evidence.runtime_sha256 != runtime_sha256
    ):
        raise ValueError("base and cell checkpoint execution identities differ")
    del base_panel, cell_panel, base_telemetry, cell_telemetry
    gc.collect()
    frozen_fingerprint = current_g2_runtime_fingerprint()
    draw_count = _patch_rng_draws_to_fail(frozen_fingerprint)
    (
        loaded_base,
        loaded_cell,
        loaded_base_evidence,
        loaded_cell_evidence,
        after_coefficients,
        after_shapes,
        after_finite,
    ) = _load_and_fit_without_draws(
        spec,
        contract=contract,
        authority=authority,
        base_expected=base_expected,
        cell_expected=cell_expected,
    )
    if draw_count[0] != 0:
        raise ValueError("same-process checkpoint recovery attempted an RNG draw")
    if (
        loaded_base_evidence.artifact_sha256 != base_artifact_sha256
        or loaded_cell_evidence.artifact_sha256 != cell_artifact_sha256
    ):
        raise ValueError("loaded artifact identity differs from the published checkpoint")
    after_arrays, after_receipts, after_designs = _panel_hashes(
        loaded_base,
        loaded_cell,
    )
    if coefficient_shapes != after_shapes or coefficient_finite != after_finite:
        raise ValueError("coefficient shape or finiteness changed across recovery")
    if before_arrays != after_arrays:
        raise ValueError("panel numeric bytes changed across recovery")
    if before_receipts != after_receipts:
        raise ValueError("panel receipts changed across recovery")
    if before_designs != after_designs:
        raise ValueError("panel design digests changed across recovery")
    if before_coefficients != after_coefficients:
        raise ValueError("coefficient bytes changed across recovery")
    fresh_coefficients, fresh_draw_count = _run_fresh_process(
        spec,
        attempt_sha256=attempt_sha256,
    )
    if fresh_coefficients != after_coefficients or fresh_draw_count != 0:
        raise ValueError("fresh-process checkpoint recovery differs or drew RNG")
    phase_id, scenario_id = contract.phase_scenario(spec.stream)
    result: dict[str, object] = {
        "schema_version": 1,
        "status": "passed",
        "attempt_sha256": attempt_sha256,
        "seed": spec.seed,
        "stream": spec.stream.value,
        "phase_id": phase_id,
        "scenario_id": scenario_id,
        "n_dates": spec.n_dates,
        "panel_index": spec.panel_index,
        "source_snapshot_sha256": source_snapshot_sha256,
        "runtime_sha256": runtime_sha256,
        "base_artifact_sha256": base_artifact_sha256,
        "cell_artifact_sha256": cell_artifact_sha256,
        "array_sha256_before": before_arrays,
        "array_sha256_after": after_arrays,
        "receipt_sha256_before": before_receipts,
        "receipt_sha256_after": after_receipts,
        "design_digest_sha256_before": before_designs,
        "design_digest_sha256_after": after_designs,
        "coefficient_sha256_before": before_coefficients,
        "coefficient_sha256_after": after_coefficients,
        "coefficient_shapes": coefficient_shapes,
        "coefficient_finite": coefficient_finite,
        "fresh_process_coefficient_sha256": fresh_coefficients,
        "fresh_process_rng_draw_count": fresh_draw_count,
        "artifact_logical_bytes": artifact_logical_bytes,
        "artifact_allocated_bytes": artifact_allocated_bytes,
    }
    if frozenset(result) != _WORKER_RESULT_KEYS:
        raise AssertionError("primary worker result schema changed")
    return result


def _run_fresh_worker(spec: RecoveryRunSpec, *, attempt_sha256: str) -> dict[str, object]:
    bytecode_policy = _validate_policy_record(
        spec,
        attempt_sha256=attempt_sha256,
    )
    _validate_child_bytecode_prefix(bytecode_policy.fresh_prefix)
    attempt_path = spec.result_root / "attempt.json"
    attempt_bytes = _read_stable_regular_file(attempt_path, maximum=_MAX_JSON_BYTES)
    attempt = _parse_canonical_payload(
        attempt_bytes,
        name=attempt_path.name,
        exact_keys=_ATTEMPT_KEYS,
    )
    if _sha256(attempt_bytes) != attempt_sha256:
        raise ValueError("fresh worker attempt digest differs from its specification")
    contract = load_g2_contract(spec.repository_root)
    _validate_attempt(attempt, spec=spec, contract=contract)
    authority, base_expected, cell_expected, _environment = _require_worker_execution_identity(
        spec,
        attempt=attempt,
        contract=contract,
    )
    frozen_fingerprint = current_g2_runtime_fingerprint()
    draw_count = _patch_rng_draws_to_fail(frozen_fingerprint)
    (
        _loaded_base,
        _loaded_cell,
        _base_evidence,
        _cell_evidence,
        coefficients,
        _shapes,
        _finite,
    ) = _load_and_fit_without_draws(
        spec,
        contract=contract,
        authority=authority,
        base_expected=base_expected,
        cell_expected=cell_expected,
    )
    return {
        "coefficient_sha256": coefficients,
        "rng_draw_count": draw_count[0],
    }


def _public_spec(repository_root: Path) -> RecoveryRunSpec:
    return RecoveryRunSpec(
        mode="public",
        repository_root=repository_root,
        result_root=repository_root / _PUBLIC_RESULT_LABEL,
        checkpoint_root=repository_root / _PUBLIC_CHECKPOINT_LABEL,
        scratch_root=repository_root / _PUBLIC_SCRATCH_LABEL,
        seed=_PUBLIC_SEED,
        stream=G2Stream.VALIDATION_RECOVERY,
        n_dates=252,
        panel_index=0,
        design_target_index=16,
        response_target_index=0,
        expected_wall_seconds=30.0,
        hard_wall_seconds=120.0,
        expected_peak_rss_bytes=1024**3,
        hard_peak_rss_bytes=1536 * 1024**2,
        hard_artifact_bytes=12 * 1024**2,
        poll_seconds=0.05,
        require_clean_source=True,
        checkpoint_label=_PUBLIC_CHECKPOINT_LABEL,
        scratch_label=_PUBLIC_SCRATCH_LABEL,
    )


def _load_internal_spec(
    path: Path,
    *,
    role: Literal["worker", "fresh"],
    capability: _ChildCapability,
) -> tuple[RecoveryRunSpec, str]:
    payload = _read_stable_regular_file(path, maximum=_MAX_JSON_BYTES)
    if _sha256(payload) != capability.spec_sha256:
        raise ValueError("child specification differs from its parent-issued capability")
    spec, attempt_sha256 = _spec_from_internal(_parse_canonical_payload(payload, name=path.name))
    expected_name = "_worker-spec.json" if role == "worker" else "_fresh-spec.json"
    if (
        capability.role != role
        or capability.attempt_sha256 != attempt_sha256
        or path != spec.scratch_root / expected_name
    ):
        raise ValueError(
            "child capability, attempt, role, or canonical scratch path is inconsistent"
        )
    return spec, attempt_sha256


def _require_make_launcher() -> None:
    make_level = os.environ.get("MAKELEVEL")
    if (
        os.environ.get(_MAKE_LAUNCH_ENV) != _MAKE_LAUNCH_VALUE
        or make_level is None
        or not make_level.isascii()
        or not make_level.isdecimal()
        or int(make_level) < 1
    ):
        raise SystemExit("public recovery is Make-only; run `make g2-checkpoint-recovery`")


def main(argv: list[str] | None = None) -> int:
    """Run the fixed public A019 supervisor or one private child role."""
    arguments = sys.argv[1:] if argv is None else argv
    if not arguments:
        raise SystemExit("public recovery is Make-only; run `make g2-checkpoint-recovery`")
    if arguments == ["_supervisor"]:
        _require_make_launcher()
        repository_root = Path(__file__).resolve().parents[2]
        result = _run_supervisor(_public_spec(repository_root))
        sys.stdout.buffer.write(_canonical_json_bytes(result))
        return 0
    if len(arguments) == 2 and arguments[0] == "_worker":
        capability = _consume_child_capability(role="worker")
        spec, attempt_sha256 = _load_internal_spec(
            Path(arguments[1]),
            role="worker",
            capability=capability,
        )
        result = _run_primary_worker(spec, attempt_sha256=attempt_sha256)
        _exclusive_write(
            spec.scratch_root / "_worker-result.json",
            _canonical_json_bytes(result),
        )
        return 0
    if len(arguments) == 2 and arguments[0] == "_fresh":
        capability = _consume_child_capability(role="fresh")
        spec, attempt_sha256 = _load_internal_spec(
            Path(arguments[1]),
            role="fresh",
            capability=capability,
        )
        result = _run_fresh_worker(spec, attempt_sha256=attempt_sha256)
        sys.stdout.buffer.write(_canonical_json_bytes(result))
        return 0
    raise SystemExit("public recovery accepts no address overrides")


if __name__ == "__main__":
    raise SystemExit(main())
