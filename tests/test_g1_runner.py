from __future__ import annotations

import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

import xid.sim.g1 as g1

_TEST_SEED = 1729


def _config_path() -> Path:
    return Path(__file__).parents[1] / "configs/g1.toml"


def test_target_hash_mismatch_stops_before_any_rng_draw(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base = g1.load_g1_config(_config_path())
    config = replace(
        base,
        master_seed=_TEST_SEED,
        n_samples=256,
        shard_size=256,
        checkpoint_directory=tmp_path / "checkpoints",
        output_directory=tmp_path / "results",
        ols_target_sha256="0" * 64,
    )

    def forbidden_draw(*args: object, **kwargs: object) -> g1.GeneratedBatch:
        raise AssertionError("RNG was reached before target preflight")

    monkeypatch.setattr(g1, "generate_batch", forbidden_draw)

    with pytest.raises(ValueError, match="analytic target hash mismatch"):
        g1.run_preregistered(
            config,
            config_sha256="a" * 64,
            code_sha="test-code-sha",
        )


def _git(repo: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def test_implementation_identity_requires_clean_tracked_inputs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "src/xid").mkdir(parents=True)
    (repo / "configs").mkdir()
    (repo / "src/xid/core.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "configs/g1.toml").write_text("schema = 1\n", encoding="utf-8")
    (repo / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")
    (repo / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    (repo / ".python-version").write_text("3.13.5\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "G1 Test")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "fixture")
    head = _git(repo, "rev-parse", "HEAD")

    assert g1.implementation_git_sha(repo) == head
    with pytest.raises(RuntimeError, match="Git repository top level"):
        g1.implementation_git_sha(repo / "src")

    (repo / "src/xid/core.py").write_text("VALUE = 2\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="implementation inputs are dirty"):
        g1.implementation_git_sha(repo)


def test_source_identity_ignores_documentation_only_commits(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "src/xid").mkdir(parents=True)
    (repo / "configs").mkdir()
    (repo / "src/xid/core.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "configs/g1.toml").write_text("schema = 1\n", encoding="utf-8")
    (repo / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")
    (repo / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    (repo / ".python-version").write_text("3.13.5\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "G1 Test")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "fixture")

    first = g1.implementation_source_sha256(repo)
    (repo / "README.md").write_text("documentation only\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-q", "-m", "docs")
    assert g1.implementation_source_sha256(repo) == first

    (repo / "src/xid/core.py").write_text("VALUE = 2\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="implementation inputs are dirty"):
        g1.implementation_source_sha256(repo)
    _git(repo, "add", "src/xid/core.py")
    _git(repo, "commit", "-q", "-m", "source")
    assert g1.implementation_source_sha256(repo) != first

    (repo / "src/xid/core.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "src/xid/untracked.py").write_text("VALUE = 3\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="implementation inputs are dirty"):
        g1.implementation_git_sha(repo)
