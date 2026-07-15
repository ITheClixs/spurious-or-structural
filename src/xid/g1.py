"""Provenance-locked command and deterministic result publisher for gate G1."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import platform
import tempfile
from collections.abc import Sequence
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
import scipy  # type: ignore[import-untyped]

from xid.sim.g1 import (
    NUMERICAL_THREAD_ENVIRONMENT,
    CoefficientEstimate,
    G1Config,
    PreregisteredRun,
    TargetHashes,
    analytic_targets,
    build_fixture,
    estimate_from_moments,
    implementation_git_sha,
    implementation_source_sha256,
    load_g1_config,
    run_preregistered,
    runtime_sha256,
    validate_preregistered_targets,
)

_FROZEN_CONFIG_PATH = Path("configs/g1.toml")
THREAD_ENVIRONMENT = NUMERICAL_THREAD_ENVIRONMENT


@dataclass(frozen=True)
class RootedG1Config:
    """Frozen config bytes plus clean implementation provenance."""

    config: G1Config
    config_sha256: str
    implementation_source_sha256: str
    implementation_commit_sha: str


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_sha256(value: str, *, name: str) -> None:
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{name} must be a lowercase SHA256 digest")


def load_rooted_g1_config(*, root: Path, config_path: Path) -> RootedG1Config:
    """Load the one frozen config and derive provenance without override seams."""
    repository = root.resolve()
    requested = config_path if config_path.is_absolute() else repository / config_path
    requested = requested.resolve()
    expected = (repository / _FROZEN_CONFIG_PATH).resolve()
    if requested != expected:
        raise ValueError("G1 production runs require the frozen configs/g1.toml")
    config = load_g1_config(requested)
    rooted = replace(
        config,
        checkpoint_directory=repository / config.checkpoint_directory,
        output_directory=repository / config.output_directory,
    )
    return RootedG1Config(
        config=rooted,
        config_sha256=_file_sha256(requested),
        implementation_source_sha256=implementation_source_sha256(repository),
        implementation_commit_sha=implementation_git_sha(repository),
    )


def benchmark_config(config: G1Config) -> G1Config:
    """Use one shard under the distinct preregistered benchmark stream."""
    return replace(
        config,
        master_seed=config.benchmark_seed,
        n_samples=config.shard_size,
        checkpoint_directory=config.checkpoint_directory.with_name(
            f"{config.checkpoint_directory.name}-benchmark"
        ),
    )


def require_single_thread_runtime() -> dict[str, str]:
    """Refuse production numerics unless every supported BLAS control is one."""
    observed = {name: os.environ.get(name) for name in THREAD_ENVIRONMENT}
    if any(value != "1" for value in observed.values()):
        raise RuntimeError(
            "G1 requires an explicit single-thread numerical runtime: "
            + ", ".join(f"{name}=1" for name in THREAD_ENVIRONMENT)
        )
    return {name: "1" for name in THREAD_ENVIRONMENT}


def _matrix(matrix: np.ndarray[tuple[int, ...], np.dtype[np.float64]]) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix]


def _coefficient_payload(
    report: CoefficientEstimate,
    *,
    target: np.ndarray[tuple[int, ...], np.dtype[np.float64]],
) -> dict[str, object]:
    return {
        "coefficient": _matrix(report.coefficient),
        "lower": _matrix(report.lower),
        "signed_relative_error": _matrix(report.signed_relative_error),
        "signed_relative_lower": _matrix(report.signed_relative_lower),
        "signed_relative_upper": _matrix(report.signed_relative_upper),
        "standard_error": _matrix(report.standard_error),
        "target": _matrix(target),
        "upper": _matrix(report.upper),
    }


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _target_hash_payload(hashes: TargetHashes) -> dict[str, str]:
    return {key: str(value) for key, value in asdict(hashes).items()}


def _result_payloads(
    rooted: RootedG1Config,
    run: PreregisteredRun,
) -> tuple[dict[str, object], dict[str, object]]:
    config = rooted.config
    _require_sha256(rooted.config_sha256, name="config_sha256")
    _require_sha256(
        rooted.implementation_source_sha256,
        name="implementation_source_sha256",
    )
    if run.shards.moments.count != config.n_samples or run.estimates is None:
        raise ValueError("G1 results require the exact complete preregistered sample")
    fixture = build_fixture(config)
    targets = analytic_targets(fixture)
    target_hashes = validate_preregistered_targets(config, targets)
    if run.target_hashes != target_hashes:
        raise ValueError("run target hashes do not match the frozen config")
    recomputed = estimate_from_moments(
        run.shards.moments,
        fixture=fixture,
        targets=targets,
        familywise_confidence=config.familywise_confidence,
        coefficient_count=config.coefficient_count,
    )
    supplied_payload = {
        "controlled": _coefficient_payload(run.estimates.controlled, target=targets.controlled),
        "ols": _coefficient_payload(run.estimates.ols, target=targets.ols),
    }
    recomputed_payload = {
        "controlled": _coefficient_payload(recomputed.controlled, target=targets.controlled),
        "ols": _coefficient_payload(recomputed.ols, target=targets.ols),
    }
    if supplied_payload != recomputed_payload:
        raise RuntimeError("run estimates do not match checkpoint moments")

    passed = recomputed.gate_discrepancy < config.relative_tolerance
    summary: dict[str, object] = {
        "coefficient_count": config.coefficient_count,
        "config_sha256": rooted.config_sha256,
        "controlled": {
            "critical_value": recomputed.controlled.critical_value,
            "degrees_freedom": recomputed.controlled.degrees_freedom,
            "max_relative_discrepancy": recomputed.controlled.max_relative_discrepancy,
            "target_in_all_intervals": recomputed.controlled.target_in_all_intervals,
        },
        "evidence_scope": "simulation-known-ground-truth",
        "familywise_confidence": config.familywise_confidence,
        "gate": "G1",
        "gate_criterion": {
            "comparison": "strictly-less-than",
            "metric": "max-elementwise-relative-discrepancy-no-denominator-floor",
            "threshold": config.relative_tolerance,
        },
        "gate_discrepancy": recomputed.gate_discrepancy,
        "implementation_source_sha256": rooted.implementation_source_sha256,
        "interval_method": recomputed.interval_method,
        "n_assets": config.n_assets,
        "n_factors": config.n_factors,
        "n_samples": config.n_samples,
        "numpy_version": np.__version__,
        "ols": {
            "critical_value": recomputed.ols.critical_value,
            "degrees_freedom": recomputed.ols.degrees_freedom,
            "max_relative_discrepancy": recomputed.ols.max_relative_discrepancy,
            "target_in_all_intervals": recomputed.ols.target_in_all_intervals,
        },
        "passed": passed,
        "python_version": platform.python_version(),
        "runtime_sha256": runtime_sha256(),
        "schema_version": 1,
        "scipy_version": scipy.__version__,
        "seed": config.master_seed,
        "shard_size": config.shard_size,
        "target_hashes": _target_hash_payload(target_hashes),
    }
    estimates: dict[str, object] = {
        "controlled": supplied_payload["controlled"],
        "gate": "G1",
        "interval_method": recomputed.interval_method,
        "ols": supplied_payload["ols"],
        "schema_version": 1,
    }
    return summary, estimates


def _validate_existing_evidence(
    output: Path,
    *,
    summary_bytes: bytes,
    estimates_bytes: bytes,
) -> None:
    marker_path = output / "_SUCCESS"
    existing_summary = (output / "summary.json").read_bytes()
    existing_estimates = (output / "estimates.json").read_bytes()
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    expected_marker = {
        "estimates_sha256": hashlib.sha256(existing_estimates).hexdigest(),
        "summary_sha256": hashlib.sha256(existing_summary).hexdigest(),
    }
    if marker != expected_marker:
        raise RuntimeError("published G1 evidence fails its success-marker hashes")
    if existing_summary != summary_bytes or existing_estimates != estimates_bytes:
        raise RuntimeError("published G1 evidence differs from the requested run")


def publish_preregistered_run(
    rooted: RootedG1Config,
    run: PreregisteredRun,
) -> dict[str, object]:
    """Publish deterministic evidence with an immutable, success-last contract."""
    summary, estimates = _result_payloads(rooted, run)
    summary_bytes = _json_bytes(summary)
    estimates_bytes = _json_bytes(estimates)
    success_bytes = _json_bytes(
        {
            "estimates_sha256": hashlib.sha256(estimates_bytes).hexdigest(),
            "summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
        }
    )
    output = rooted.config.output_directory
    if not output.is_absolute():
        raise ValueError("rooted G1 output directory must be absolute")
    output.parent.mkdir(parents=True, exist_ok=True)
    lock_path = output.parent / f".{output.name}.lock"
    with tempfile.TemporaryDirectory(prefix=f".{output.name}.tmp-", dir=output.parent) as stage:
        stage_path = Path(stage)
        (stage_path / "summary.json").write_bytes(summary_bytes)
        (stage_path / "estimates.json").write_bytes(estimates_bytes)
        (stage_path / "_SUCCESS").write_bytes(success_bytes)
        with lock_path.open("a", encoding="utf-8") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if (output / "_SUCCESS").is_file():
                _validate_existing_evidence(
                    output,
                    summary_bytes=summary_bytes,
                    estimates_bytes=estimates_bytes,
                )
            else:
                output.mkdir(parents=True, exist_ok=True)
                (output / "_SUCCESS").unlink(missing_ok=True)
                (stage_path / "summary.json").replace(output / "summary.json")
                (stage_path / "estimates.json").replace(output / "estimates.json")
                (stage_path / "_SUCCESS").replace(output / "_SUCCESS")
            fcntl.flock(lock, fcntl.LOCK_UN)
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    """Run the distinct-seed benchmark or the sealed G1 experiment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("benchmark", "run"))
    parser.add_argument("--config", default=_FROZEN_CONFIG_PATH, type=Path)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    arguments = parser.parse_args(argv)
    require_single_thread_runtime()
    rooted = load_rooted_g1_config(root=arguments.root, config_path=arguments.config)
    config = benchmark_config(rooted.config) if arguments.mode == "benchmark" else rooted.config
    run = run_preregistered(
        config,
        config_sha256=rooted.config_sha256,
        code_sha=rooted.implementation_source_sha256,
    )
    if arguments.mode == "benchmark":
        print(
            json.dumps(
                {
                    "elapsed_seconds": run.shards.elapsed_seconds,
                    "generation_seconds": run.shards.generation_seconds,
                    "implementation_commit_sha": rooted.implementation_commit_sha,
                    "implementation_source_sha256": rooted.implementation_source_sha256,
                    "mode": "benchmark",
                    "peak_rss_bytes": run.shards.peak_rss_bytes,
                    "rows": run.shards.moments.count,
                    "seed": config.master_seed,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        return 0
    summary = publish_preregistered_run(rooted, run)
    print(
        json.dumps(
            {
                "implementation_commit_sha": rooted.implementation_commit_sha,
                "mode": "run",
                "summary": summary,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )
    return 0 if bool(summary["passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
