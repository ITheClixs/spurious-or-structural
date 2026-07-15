from __future__ import annotations

import hashlib
import json
import os
import subprocess
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

import xid.g1 as g1_cli
from xid.sim.g1 import PreregisteredRun, load_g1_config, run_preregistered

_TEST_SEED = 314159


def _config_path() -> Path:
    return Path(__file__).parents[1] / "configs/g1.toml"


def _small_complete_run(
    tmp_path: Path,
) -> tuple[g1_cli.RootedG1Config, PreregisteredRun]:
    base = load_g1_config(_config_path())
    config = replace(
        base,
        master_seed=_TEST_SEED,
        n_samples=512,
        shard_size=256,
        checkpoint_directory=tmp_path / "checkpoints",
        output_directory=tmp_path / "results/g1",
    )
    rooted = g1_cli.RootedG1Config(
        config=config,
        config_sha256="a" * 64,
        implementation_source_sha256="b" * 64,
        implementation_commit_sha="c" * 40,
    )
    run = run_preregistered(
        config,
        config_sha256=rooted.config_sha256,
        code_sha=rooted.implementation_source_sha256,
    )
    return rooted, run


def test_rooted_config_resolves_only_the_frozen_repository_config(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "configs").mkdir(parents=True)
    (root / "src/xid").mkdir(parents=True)
    config_bytes = _config_path().read_bytes()
    (root / "configs/g1.toml").write_bytes(config_bytes)
    (root / "src/xid/__init__.py").write_text("\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")
    (root / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    (root / ".python-version").write_text("3.13.5\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "G1 Test"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=root, check=True)

    rooted = g1_cli.load_rooted_g1_config(root=root, config_path=Path("configs/g1.toml"))

    assert rooted.config.checkpoint_directory == root / "data/checkpoints/g1"
    assert rooted.config.output_directory == root / "results/g1"
    assert rooted.config_sha256 == hashlib.sha256(config_bytes).hexdigest()
    assert len(rooted.implementation_source_sha256) == 64
    assert len(rooted.implementation_commit_sha) == 40

    with pytest.raises(ValueError, match="frozen configs/g1.toml"):
        g1_cli.load_rooted_g1_config(root=root, config_path=Path("configs/alternate.toml"))


def test_benchmark_config_uses_only_the_distinct_benchmark_seed(tmp_path: Path) -> None:
    rooted, _ = _small_complete_run(tmp_path)

    benchmark = g1_cli.benchmark_config(rooted.config)

    assert benchmark.master_seed == rooted.config.benchmark_seed
    assert benchmark.master_seed != rooted.config.master_seed
    assert benchmark.n_samples == rooted.config.shard_size
    assert benchmark.checkpoint_directory != rooted.config.checkpoint_directory
    assert benchmark.output_directory == rooted.config.output_directory


def test_production_runtime_requires_explicit_single_thread_controls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in g1_cli.THREAD_ENVIRONMENT:
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(RuntimeError, match="single-thread numerical runtime"):
        g1_cli.require_single_thread_runtime()

    for name in g1_cli.THREAD_ENVIRONMENT:
        monkeypatch.setenv(name, "1")
    assert g1_cli.require_single_thread_runtime() == {
        name: "1" for name in g1_cli.THREAD_ENVIRONMENT
    }


def test_publish_is_byte_stable_and_carries_every_coefficient_interval(tmp_path: Path) -> None:
    rooted, run = _small_complete_run(tmp_path)

    summary = g1_cli.publish_preregistered_run(rooted, run)
    output = rooted.config.output_directory
    original_summary = (output / "summary.json").read_bytes()
    original_estimates = (output / "estimates.json").read_bytes()
    marker = json.loads((output / "_SUCCESS").read_text(encoding="utf-8"))

    assert summary["gate"] == "G1"
    assert summary["evidence_scope"] == "simulation-known-ground-truth"
    assert summary["interval_method"] == "classical-homoskedastic-student-t-bonferroni"
    assert marker == {
        "estimates_sha256": hashlib.sha256(original_estimates).hexdigest(),
        "summary_sha256": hashlib.sha256(original_summary).hexdigest(),
    }
    estimates = json.loads(original_estimates)
    for regression in ("ols", "controlled"):
        report = estimates[regression]
        for field in ("coefficient", "target", "standard_error", "lower", "upper"):
            assert np.asarray(report[field]).shape == (30, 30)
        coefficient = np.asarray(report["coefficient"])
        lower = np.asarray(report["lower"])
        upper = np.asarray(report["upper"])
        assert np.all(lower < coefficient)
        assert np.all(coefficient < upper)

    rerun = replace(
        run,
        shards=replace(
            run.shards,
            new_shards=0,
            reused_shards=2,
            elapsed_seconds=999.0,
            peak_rss_bytes=123,
        ),
    )
    assert g1_cli.publish_preregistered_run(rooted, rerun) == summary
    assert (output / "summary.json").read_bytes() == original_summary
    assert (output / "estimates.json").read_bytes() == original_estimates


def test_publish_refuses_to_replace_valid_evidence_with_different_estimates(
    tmp_path: Path,
) -> None:
    rooted, run = _small_complete_run(tmp_path)
    g1_cli.publish_preregistered_run(rooted, run)
    assert run.estimates is not None
    changed_coefficient = run.estimates.ols.coefficient.copy()
    changed_coefficient[0, 0] += 0.01
    changed_ols = replace(run.estimates.ols, coefficient=changed_coefficient)
    changed_run = replace(run, estimates=replace(run.estimates, ols=changed_ols))

    with pytest.raises(RuntimeError, match="run estimates do not match checkpoint moments"):
        g1_cli.publish_preregistered_run(rooted, changed_run)


def test_interrupted_result_publish_has_no_success_marker_and_recovers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rooted, run = _small_complete_run(tmp_path)
    original_replace = Path.replace

    def fail_estimate_publish(source: Path, target: str | os.PathLike[str]) -> Path:
        if source.name == "estimates.json" and source.parent.name.startswith(".g1.tmp-"):
            raise OSError("injected G1 publication failure")
        return original_replace(source, target)

    monkeypatch.setattr(Path, "replace", fail_estimate_publish)
    with pytest.raises(OSError, match="injected G1 publication failure"):
        g1_cli.publish_preregistered_run(rooted, run)
    assert not (rooted.config.output_directory / "_SUCCESS").exists()

    monkeypatch.undo()
    g1_cli.publish_preregistered_run(rooted, run)
    assert (rooted.config.output_directory / "_SUCCESS").is_file()
