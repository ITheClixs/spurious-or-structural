from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest

import xid.g2_checkpoint_recovery as recovery
from xid.g2_checkpoint_recovery import RecoveryRunFailed, RecoveryRunSpec
from xid.models.g2_checkpoint import G2CheckpointEnvironmentIdentity
from xid.sim.g2 import G2Stream, TestRngNamespace


def _root() -> Path:
    return Path(__file__).parents[1]


def _thread_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "BLIS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        monkeypatch.setenv(name, "1")


def _test_spec(tmp_path: Path) -> RecoveryRunSpec:
    return RecoveryRunSpec(
        mode="test",
        repository_root=_root(),
        result_root=tmp_path / "result",
        checkpoint_root=tmp_path / "checkpoints",
        scratch_root=tmp_path / "scratch",
        seed=1729,
        stream=G2Stream.VALIDATION_DATE_FRONTIER,
        n_dates=48,
        panel_index=0,
        design_target_index=16,
        response_target_index=0,
        expected_wall_seconds=30.0,
        hard_wall_seconds=120.0,
        expected_peak_rss_bytes=1024**3,
        hard_peak_rss_bytes=1536 * 1024**2,
        hard_artifact_bytes=12 * 1024**2,
        poll_seconds=0.05,
        require_clean_source=False,
        checkpoint_label="test/checkpoints",
        scratch_label="test/scratch",
    )


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def test_process_tree_rss_parser_sums_only_descendants() -> None:
    snapshot = """\
10 1 100
11 10 200
12 11 300
13 10 400
14 99 500
"""
    assert recovery._process_tree_rss_bytes_from_ps(snapshot, root_pid=10) == 1000 * 1024


def test_exclusive_evidence_write_never_exposes_a_partial_destination(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "attempt.json"
    real_write = os.write
    write_calls = 0

    def interrupted_write(descriptor: int, payload: bytes | memoryview) -> int:
        nonlocal write_calls
        write_calls += 1
        if write_calls == 1:
            return real_write(descriptor, bytes(payload[:1]))
        raise OSError("injected write interruption")

    monkeypatch.setattr(os, "write", interrupted_write)

    with pytest.raises(OSError, match="injected"):
        recovery._exclusive_write(destination, b"complete-evidence\n")

    assert not destination.exists()
    assert tuple(tmp_path.iterdir()) == ()


def test_stage_cleanup_interrupt_propagates_without_active_uncertainty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "attempt.json"
    payload = b"complete-evidence\n"
    real_unlink = os.unlink

    def interrupt_stage_cleanup(path: Path) -> None:
        if path.name.startswith(".attempt.json.stage-"):
            raise KeyboardInterrupt("injected ordinary cleanup interrupt")
        real_unlink(path)

    monkeypatch.setattr(os, "unlink", interrupt_stage_cleanup)

    with pytest.raises(KeyboardInterrupt, match="ordinary cleanup interrupt"):
        recovery._exclusive_write(destination, payload)

    assert destination.read_bytes() == payload


def test_supervisor_rejects_a_symlinked_root_ancestor_before_consuming_attempt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _thread_env(monkeypatch)
    outside = tmp_path / "outside"
    outside.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(outside, target_is_directory=True)
    spec = replace(
        _test_spec(tmp_path),
        result_root=alias / "result",
        checkpoint_root=alias / "checkpoints",
        scratch_root=alias / "scratch",
    )
    monkeypatch.setattr(
        recovery,
        "load_g2_contract",
        lambda *_args, **_kwargs: pytest.fail(
            "symlinked path reached contract loading after filesystem mutation"
        ),
    )

    with pytest.raises(ValueError, match="canonical|symlink"):
        recovery._run_supervisor(spec)

    assert not (outside / "result" / "attempt.json").exists()
    assert tuple(outside.iterdir()) == ()


def test_process_group_cleanup_reaches_descendants_after_the_leader_exits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ExitedLeader:
        pid = 424242

        @staticmethod
        def poll() -> int:
            return 0

        @staticmethod
        def wait(*, timeout: float) -> int:
            del timeout
            return 0

    signals: list[int] = []

    def killpg(_pid: int, sent_signal: int) -> None:
        signals.append(sent_signal)
        if sent_signal != 0:
            raise ProcessLookupError

    monkeypatch.setattr(os, "killpg", killpg)

    recovery._terminate_process_group(cast(subprocess.Popen[bytes], ExitedLeader()))

    assert signals == [0, signal.SIGTERM]


def test_process_group_cleanup_fails_if_descendants_survive_sigkill(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ExitedLeader:
        pid = 424243

        @staticmethod
        def poll() -> int:
            return 0

        @staticmethod
        def wait(*, timeout: float) -> int:
            del timeout
            return 0

    signals: list[int] = []
    clock = 0.0

    def monotonic() -> float:
        nonlocal clock
        clock += 3.0
        return clock

    monkeypatch.setattr(recovery, "_process_group_exists", lambda _pid: True)
    monkeypatch.setattr(os, "killpg", lambda _pid, sent_signal: signals.append(sent_signal))
    monkeypatch.setattr(time, "monotonic", monotonic)
    monkeypatch.setattr(time, "sleep", lambda _seconds: None)

    with pytest.raises(RecoveryRunFailed, match="process group|SIGKILL|survived"):
        recovery._terminate_process_group(cast(subprocess.Popen[bytes], ExitedLeader()))

    assert signals == [signal.SIGTERM, signal.SIGKILL]


def test_supervisor_bootstrap_requires_an_exact_empty_bytecode_prefix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prefix = tmp_path / "bootstrap-pycache"
    prefix.mkdir()
    monkeypatch.setenv("PYTHONPYCACHEPREFIX", str(prefix))
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setattr(sys, "pycache_prefix", str(prefix))
    monkeypatch.setattr(sys, "dont_write_bytecode", True)

    recovery._validate_supervisor_bootstrap(prefix)

    (prefix / "stale.pyc").write_bytes(b"stale")
    with pytest.raises(ValueError, match="empty|bytecode|cache"):
        recovery._validate_supervisor_bootstrap(prefix)


@pytest.mark.parametrize("role", ("_worker", "_fresh"))
def test_direct_child_roles_fail_before_loading_an_arbitrary_specification(
    role: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arbitrary = tmp_path / "attacker-controlled.json"
    arbitrary.write_text("{}\n", encoding="ascii")
    monkeypatch.delenv("XID_G2_RECOVERY_CHILD_FD", raising=False)
    monkeypatch.setattr(
        recovery,
        "_load_internal_spec",
        lambda *_args, **_kwargs: pytest.fail("direct child reached disk specification"),
    )

    with pytest.raises(ValueError, match="child capability"):
        recovery.main([role, str(arbitrary)])


def test_child_capability_is_one_shot_and_bound_to_the_immediate_parent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attempt_sha256 = "a" * 64
    spec_bytes = b'{"schema_version":1}\n'
    descriptor = recovery._open_child_capability(
        role="worker",
        attempt_sha256=attempt_sha256,
        spec_bytes=spec_bytes,
    )
    monkeypatch.setenv("XID_G2_RECOVERY_CHILD_FD", str(descriptor))
    monkeypatch.setattr(os, "getppid", os.getpid)

    capability = recovery._consume_child_capability(role="worker")

    assert capability.role == "worker"
    assert capability.parent_pid == os.getpid()
    assert capability.attempt_sha256 == attempt_sha256
    assert capability.spec_sha256 == recovery._sha256(spec_bytes)
    with pytest.raises(ValueError, match="child capability"):
        recovery._consume_child_capability(role="worker")


def test_child_capability_rejects_a_reopenable_named_fifo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fifo = tmp_path / "replayable-capability"
    os.mkfifo(fifo, 0o600)
    payload = recovery._child_capability_payload(
        role="worker",
        parent_pid=os.getpid(),
        attempt_sha256="a" * 64,
        spec_sha256="b" * 64,
    )
    monkeypatch.setattr(os, "getppid", os.getpid)

    for _replay in range(2):
        read_descriptor = os.open(fifo, os.O_RDONLY | os.O_NONBLOCK)
        write_descriptor = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
        try:
            assert os.write(write_descriptor, payload) == len(payload)
        finally:
            os.close(write_descriptor)
        monkeypatch.setenv("XID_G2_RECOVERY_CHILD_FD", str(read_descriptor))

        with pytest.raises(ValueError, match="anonymous|one-shot|reopenable"):
            recovery._consume_child_capability(role="worker")


def test_child_specification_is_bound_to_its_exact_scratch_path(
    tmp_path: Path,
) -> None:
    spec = _test_spec(tmp_path)
    for path in (spec.result_root, spec.checkpoint_root, spec.scratch_root):
        path.mkdir()
    attempt_sha256 = "b" * 64
    spec_bytes = recovery._canonical_json_bytes(
        recovery._internal_spec_object(spec, attempt_sha256=attempt_sha256)
    )
    capability = recovery._ChildCapability(
        role="worker",
        parent_pid=os.getpid(),
        attempt_sha256=attempt_sha256,
        spec_sha256=recovery._sha256(spec_bytes),
    )
    canonical = spec.scratch_root / "_worker-spec.json"
    canonical.write_bytes(spec_bytes)
    loaded, loaded_attempt = recovery._load_internal_spec(
        canonical,
        role="worker",
        capability=capability,
    )
    assert loaded == spec
    assert loaded_attempt == attempt_sha256

    alias = tmp_path / "_worker-spec.json"
    alias.write_bytes(spec_bytes)
    with pytest.raises(ValueError, match="canonical scratch path"):
        recovery._load_internal_spec(
            alias,
            role="worker",
            capability=capability,
        )


def test_recovery_spec_rejects_noncanonical_labels_and_public_path_aliases(
    tmp_path: Path,
) -> None:
    spec = _test_spec(tmp_path)
    with pytest.raises(ValueError, match="label|canonical|frozen"):
        recovery._validate_spec(replace(spec, scratch_label="arbitrary/scratch"))
    with pytest.raises(ValueError, match="label|canonical|frozen"):
        recovery._validate_spec(replace(spec, checkpoint_label="arbitrary/checkpoints"))


def test_public_cli_is_make_only_before_constructing_the_a019_specification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        recovery,
        "_public_spec",
        lambda *_args, **_kwargs: pytest.fail("direct CLI constructed the A019 address"),
    )

    with pytest.raises(SystemExit, match="make g2-checkpoint-recovery"):
        recovery.main([])
    with pytest.raises(SystemExit, match="make g2-checkpoint-recovery"):
        recovery.main(["_supervisor"])


def test_make_recovery_surface_cannot_override_its_bootstrap_or_thread_contract(
    tmp_path: Path,
) -> None:
    redirected = tmp_path / "redirected-cache"
    completed = subprocess.run(
        [
            "make",
            "-n",
            f"G2_RECOVERY_BOOTSTRAP_CACHE={redirected}",
            "G1_THREAD_ENV=INJECTED_RECOVERY_ENV=1",
            "g2-checkpoint-recovery",
        ],
        cwd=_root(),
        check=True,
        capture_output=True,
        encoding="utf-8",
    )

    assert str(redirected) not in completed.stdout
    assert "INJECTED_RECOVERY_ENV=1" not in completed.stdout
    assert "mkdir -p data/g2_checkpoint_recovery/scratch/bootstrap-pycache" in completed.stdout


def test_make_recovery_rejects_a_symlinked_data_ancestor_before_mutation(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / "data").symlink_to(outside, target_is_directory=True)
    (tmp_path / "Makefile").write_bytes((_root() / "Makefile").read_bytes())

    completed = subprocess.run(
        ["make", "UV=false", "g2-checkpoint-recovery"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        encoding="utf-8",
    )

    assert completed.returncode != 0
    assert tuple(outside.iterdir()) == ()


def test_every_attempt_bytecode_prefix_is_below_the_exact_scratch_root(
    tmp_path: Path,
) -> None:
    spec = _test_spec(tmp_path)
    policy = recovery._bytecode_policy(spec, attempt_sha256="c" * 64)

    assert policy.supervisor_prefix.is_relative_to(spec.scratch_root)
    assert policy.worker_prefix.is_relative_to(spec.scratch_root)
    assert policy.fresh_prefix.is_relative_to(spec.scratch_root)


def test_failed_supervisor_attempt_is_immutable_and_nonrerunnable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _thread_env(monkeypatch)
    spec = _test_spec(tmp_path)
    monkeypatch.setattr(
        recovery,
        "_worker_command",
        lambda *_args, **_kwargs: [sys.executable, "-c", "raise SystemExit(7)"],
    )

    with pytest.raises(RecoveryRunFailed, match="worker|return"):
        recovery._run_supervisor(spec)

    assert (spec.result_root / "attempt.json").is_file()
    assert (spec.result_root / "failure.json").is_file()
    assert (spec.result_root / "_FAILURE").is_file()
    assert not (spec.result_root / "result.json").exists()
    assert not (spec.result_root / "_SUCCESS").exists()
    failure = _read_json(spec.result_root / "failure.json")
    assert failure["status"] == "failed"
    assert failure["worker_returncode"] == 7

    monkeypatch.setattr(
        recovery,
        "_worker_command",
        lambda *_args, **_kwargs: pytest.fail("rerun reached worker construction"),
    )
    with pytest.raises(FileExistsError, match="attempt|consumed|immutable"):
        recovery._run_supervisor(spec)


def test_worker_supervision_always_tears_down_after_an_unexpected_exception(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class RunningWorker:
        pid = 424244

        @staticmethod
        def poll() -> None:
            return None

    worker = cast(subprocess.Popen[bytes], RunningWorker())
    termination_calls: list[int] = []
    monkeypatch.setattr(subprocess, "Popen", lambda *_args, **_kwargs: worker)
    monkeypatch.setattr(
        recovery,
        "_sample_process_tree_rss",
        lambda _pid: (_ for _ in ()).throw(RuntimeError("injected sampler defect")),
    )
    monkeypatch.setattr(recovery, "_process_group_exists", lambda _pid: True)
    monkeypatch.setattr(
        recovery,
        "_terminate_process_group",
        lambda process: termination_calls.append(process.pid),
    )

    with pytest.raises(RuntimeError, match="injected sampler defect"):
        recovery._supervise_worker(
            _test_spec(tmp_path),
            command=[sys.executable, "-c", "pass"],
            stdout_path=tmp_path / "worker.stdout",
            stderr_path=tmp_path / "worker.stderr",
            worker_pycache_prefix=tmp_path / "worker-pycache",
            child_capability_fd=99,
        )

    assert termination_calls == [424244]


@pytest.mark.parametrize("changed_identity", ("source", "runtime"))
def test_primary_worker_rechecks_attempt_identity_before_claim_or_draw(
    changed_identity: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _thread_env(monkeypatch)
    spec = _test_spec(tmp_path)
    contract, source_sha256, runtime_sha256 = recovery._preflight(spec)
    attempt = recovery._attempt_object(
        spec,
        source_snapshot_sha256=source_sha256,
        runtime_sha256=runtime_sha256,
        contract=contract,
    )
    attempt_bytes = recovery._canonical_json_bytes(attempt)
    recovery._exclusive_write(spec.result_root / "attempt.json", attempt_bytes)
    attempt_sha256 = recovery._sha256(attempt_bytes)
    policy = recovery._prepare_bytecode_policy(spec, attempt_sha256=attempt_sha256)
    monkeypatch.setenv("PYTHONPYCACHEPREFIX", str(policy.worker_prefix))
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setattr(sys, "pycache_prefix", str(policy.worker_prefix))
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    observed = G2CheckpointEnvironmentIdentity(
        source_snapshot_sha256=("0" * 64 if changed_identity == "source" else source_sha256),
        runtime_sha256=("1" * 64 if changed_identity == "runtime" else runtime_sha256),
        declared_paths_clean=True,
    )
    monkeypatch.setattr(recovery, "inspect_g2_checkpoint_environment", lambda **_kwargs: observed)
    monkeypatch.setattr(
        TestRngNamespace,
        "draw_base_normals",
        lambda *_args, **_kwargs: pytest.fail("identity mismatch reached a simulation draw"),
    )

    mismatch = f"{changed_identity}.*attempt|attempt.*{changed_identity}"
    with pytest.raises(ValueError, match=mismatch):
        recovery._run_primary_worker(spec, attempt_sha256=attempt_sha256)

    assert not (spec.scratch_root / "worker-claim.json").exists()


def test_seed_1729_supervisor_round_trips_and_fresh_process_draws_zero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _thread_env(monkeypatch)
    spec = _test_spec(tmp_path)

    result = recovery._run_supervisor(spec)

    assert result["status"] == "passed"
    assert result["seed"] == 1729
    assert result["stream"] == G2Stream.VALIDATION_DATE_FRONTIER.value
    assert result["phase_id"] == 22
    assert result["scenario_id"] == 2
    assert result["n_dates"] == 48
    assert result["array_sha256_before"] == result["array_sha256_after"]
    assert result["receipt_sha256_before"] == result["receipt_sha256_after"]
    assert result["design_digest_sha256_before"] == result["design_digest_sha256_after"]
    assert result["coefficient_sha256_before"] == result["coefficient_sha256_after"]
    assert result["fresh_process_coefficient_sha256"] == result["coefficient_sha256_after"]
    assert result["fresh_process_rng_draw_count"] == 0
    assert result["coefficient_shapes"] == {
        "homogeneous": [3],
        "observable": [30, 30],
        "oracle": [30, 30],
    }
    assert result["coefficient_finite"] == {
        "homogeneous": True,
        "observable": True,
        "oracle": True,
    }
    hard_stops = result["hard_stops"]
    assert isinstance(hard_stops, dict)
    assert all(item["passed"] is True for item in hard_stops.values())
    assert (spec.result_root / "attempt.json").is_file()
    assert (spec.result_root / "result.json").is_file()
    assert (spec.result_root / "_SUCCESS").is_file()
    assert not (spec.result_root / "failure.json").exists()
    assert not (spec.result_root / "_FAILURE").exists()

    with pytest.raises(FileExistsError, match="attempt|consumed|immutable"):
        recovery._run_supervisor(spec)


def test_success_marker_fsync_fault_never_publishes_both_terminal_outcomes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _thread_env(monkeypatch)
    spec = _test_spec(tmp_path)
    real_fsync_directory = recovery._fsync_directory
    injected = False

    def fail_once_after_success_link(path: Path) -> None:
        nonlocal injected
        if not injected and path == spec.result_root and (spec.result_root / "_SUCCESS").exists():
            injected = True
            raise OSError("injected post-link directory fsync fault")
        real_fsync_directory(path)

    monkeypatch.setattr(recovery, "_fsync_directory", fail_once_after_success_link)

    try:
        result = recovery._run_supervisor(spec)
    except RecoveryRunFailed:
        result = None

    assert injected
    terminal_markers = {
        marker for marker in ("_SUCCESS", "_FAILURE") if (spec.result_root / marker).exists()
    }
    assert len(terminal_markers) == 1
    if result is not None:
        assert result["status"] == "passed"
        assert terminal_markers == {"_SUCCESS"}
    else:
        assert terminal_markers == {"_FAILURE"}


def test_uncertain_success_rollback_does_not_publish_failure_marker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _thread_env(monkeypatch)
    spec = _test_spec(tmp_path)
    real_fsync_directory = recovery._fsync_directory
    armed = False
    injected_faults = 0

    def fail_commit_retry_and_rollback(path: Path) -> None:
        nonlocal armed, injected_faults
        if path == spec.result_root and (armed or (spec.result_root / "_SUCCESS").exists()):
            armed = True
            if injected_faults < 3:
                injected_faults += 1
                raise OSError(f"injected terminal durability fault {injected_faults}")
        real_fsync_directory(path)

    monkeypatch.setattr(
        recovery,
        "_fsync_directory",
        fail_commit_retry_and_rollback,
    )

    with pytest.raises(RecoveryRunFailed, match="durably rolled back|publication"):
        recovery._run_supervisor(spec)

    assert injected_faults == 3
    assert (spec.result_root / "attempt.json").is_file()
    assert not (spec.result_root / "_SUCCESS").exists()
    assert not (spec.result_root / "failure.json").exists()
    assert not (spec.result_root / "_FAILURE").exists()


@pytest.mark.parametrize(
    "cleanup_fault",
    (
        OSError("injected success-stage cleanup fault"),
        KeyboardInterrupt("injected success-stage cleanup interrupt"),
    ),
    ids=("oserror", "keyboard-interrupt"),
)
def test_uncertain_success_survives_stage_cleanup_fault_without_failure_marker(
    cleanup_fault: BaseException,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _thread_env(monkeypatch)
    spec = _test_spec(tmp_path)
    real_fsync_directory = recovery._fsync_directory
    real_unlink = os.unlink
    armed = False
    injected_fsync_faults = 0
    injected_cleanup_fault = False

    def fail_commit_retry_and_rollback(path: Path) -> None:
        nonlocal armed, injected_fsync_faults
        if path == spec.result_root and (armed or (spec.result_root / "_SUCCESS").exists()):
            armed = True
            if injected_fsync_faults < 3:
                injected_fsync_faults += 1
                raise OSError(f"injected terminal durability fault {injected_fsync_faults}")
        real_fsync_directory(path)

    def fail_success_stage_cleanup(path: Path) -> None:
        nonlocal injected_cleanup_fault
        if not injected_cleanup_fault and path.name.startswith("._SUCCESS.stage-"):
            injected_cleanup_fault = True
            raise cleanup_fault
        real_unlink(path)

    monkeypatch.setattr(
        recovery,
        "_fsync_directory",
        fail_commit_retry_and_rollback,
    )
    monkeypatch.setattr(os, "unlink", fail_success_stage_cleanup)

    with pytest.raises(RecoveryRunFailed, match="durably rolled back|publication"):
        recovery._run_supervisor(spec)

    assert injected_fsync_faults == 3
    assert injected_cleanup_fault
    assert (spec.result_root / "attempt.json").is_file()
    assert not (spec.result_root / "_SUCCESS").exists()
    assert not (spec.result_root / "failure.json").exists()
    assert not (spec.result_root / "_FAILURE").exists()
