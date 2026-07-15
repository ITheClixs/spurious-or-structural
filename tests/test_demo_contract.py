from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import xid.demo as demo


def test_xid_package_is_importable() -> None:
    assert importlib.util.find_spec("xid") is not None


def test_demo_module_is_importable() -> None:
    assert importlib.util.find_spec("xid.demo") is not None


def test_demo_exposes_a_runner() -> None:
    assert callable(getattr(demo, "run_demo", None))


def test_demo_exposes_a_config_loader() -> None:
    assert callable(getattr(demo, "load_demo_config", None))


def test_load_demo_config_reads_the_versioned_contract(tmp_path: Path) -> None:
    config_path = tmp_path / "demo.toml"
    config_path.write_text(
        """
[demo]
schema_version = 1
seed = 1729
bins_per_asset = 8
assets = ["BTC-PERP", "ETH-PERP"]

[output]
directory = "results/demo"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = demo.load_demo_config(config_path)

    assert config.schema_version == 1
    assert config.seed == 1729
    assert config.bins_per_asset == 8
    assert config.assets == ("BTC-PERP", "ETH-PERP")
    assert config.output_directory == Path("results/demo")


def test_load_demo_config_rejects_nonpositive_bins(tmp_path: Path) -> None:
    config_path = tmp_path / "demo.toml"
    config_path.write_text(
        """
[demo]
schema_version = 1
seed = 1729
bins_per_asset = 0
assets = ["BTC-PERP"]

[output]
directory = "results/demo"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="bins_per_asset must be positive"):
        demo.load_demo_config(config_path)


@pytest.mark.parametrize(
    ("demo_block", "output_directory", "message"),
    [
        (
            'schema_version = 2\nseed = 1729\nbins_per_asset = 8\nassets = ["BTC-PERP"]',
            "results/demo",
            "unsupported demo schema_version",
        ),
        (
            "schema_version = 1\nseed = 1729\nbins_per_asset = 8\n"
            'assets = ["BTC-PERP", "BTC-PERP"]',
            "results/demo",
            "assets must be unique",
        ),
        (
            'schema_version = 1\nseed = 1729\nbins_per_asset = 8\nassets = ["BTC-PERP"]',
            "../escape",
            "output directory must stay below root",
        ),
    ],
)
def test_load_demo_config_rejects_ambiguous_or_unsafe_values(
    tmp_path: Path,
    demo_block: str,
    output_directory: str,
    message: str,
) -> None:
    config_path = tmp_path / "demo.toml"
    config_path.write_text(
        f'[demo]\n{demo_block}\n\n[output]\ndirectory = "{output_directory}"\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=message):
        demo.load_demo_config(config_path)


def test_run_demo_revalidates_direct_config_objects(tmp_path: Path) -> None:
    unsafe = demo.DemoConfig(
        schema_version=1,
        seed=1729,
        bins_per_asset=8,
        assets=("BTC-PERP",),
        output_directory=Path("../escape"),
    )

    with pytest.raises(ValueError, match="output directory must stay below root"):
        demo.run_demo(unsafe, root=tmp_path)


def test_run_demo_writes_byte_reproducible_smoke_artifacts(tmp_path: Path) -> None:
    config_path = tmp_path / "demo.toml"
    config_path.write_text(
        """
[demo]
schema_version = 1
seed = 1729
bins_per_asset = 8
assets = ["BTC-PERP", "ETH-PERP"]

[output]
directory = "results/demo"
""".strip()
        + "\n",
        encoding="utf-8",
    )
    config = demo.load_demo_config(config_path)
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"

    first_summary = demo.run_demo(config, root=first_root)
    second_summary = demo.run_demo(config, root=second_root)

    assert first_summary == second_summary
    assert first_summary["gate"] == "G0"
    assert first_summary["evidence_scope"] == "software-smoke-only"
    assert first_summary["row_count"] == 16
    assert first_summary["interval_status"] == "not-applicable-no-statistical-claim"
    first_output = first_root / config.output_directory
    second_output = second_root / config.output_directory
    assert (first_output / "synthetic_bins.jsonl").read_bytes() == (
        second_output / "synthetic_bins.jsonl"
    ).read_bytes()
    assert (first_output / "summary.json").read_bytes() == (
        second_output / "summary.json"
    ).read_bytes()
    data_bytes = (first_output / "synthetic_bins.jsonl").read_bytes()
    assert hashlib.sha256(data_bytes).hexdigest() == first_summary["data_sha256"]
    first_marker = json.loads((first_output / "_SUCCESS").read_text(encoding="utf-8"))
    summary_bytes = (first_output / "summary.json").read_bytes()
    assert first_marker == {
        "data_sha256": first_summary["data_sha256"],
        "summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
    }


def test_interrupted_publish_is_invalid_and_next_run_recovers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first_config_path = tmp_path / "first.toml"
    first_config_path.write_text(
        """
[demo]
schema_version = 1
seed = 1729
bins_per_asset = 8
assets = ["BTC-PERP", "ETH-PERP"]

[output]
directory = "results/demo"
""".strip()
        + "\n",
        encoding="utf-8",
    )
    second_config_path = tmp_path / "second.toml"
    second_config_path.write_text(
        first_config_path.read_text(encoding="utf-8").replace("seed = 1729", "seed = 1730"),
        encoding="utf-8",
    )
    root = tmp_path / "run"
    demo.run_demo(demo.load_demo_config(first_config_path), root=root)
    output = root / "results/demo"

    original_replace = Path.replace

    def fail_summary_publish(source: Path, target: str | os.PathLike[str]) -> Path:
        if source.name == "summary.json" and source.parent.name.startswith(".xid-demo-"):
            raise OSError("injected summary publish failure")
        return original_replace(source, target)

    monkeypatch.setattr(Path, "replace", fail_summary_publish)
    with pytest.raises(OSError, match="injected summary publish failure"):
        demo.run_demo(demo.load_demo_config(second_config_path), root=root)

    assert not (output / "_SUCCESS").exists()
    monkeypatch.undo()

    recovered = demo.run_demo(demo.load_demo_config(second_config_path), root=root)
    data_bytes = (output / "synthetic_bins.jsonl").read_bytes()
    summary_bytes = (output / "summary.json").read_bytes()
    marker = json.loads((output / "_SUCCESS").read_text(encoding="utf-8"))
    assert hashlib.sha256(data_bytes).hexdigest() == recovered["data_sha256"]
    assert marker == {
        "data_sha256": recovered["data_sha256"],
        "summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
    }


def test_module_cli_runs_the_demo_from_a_config(tmp_path: Path) -> None:
    config_path = tmp_path / "demo.toml"
    config_path.write_text(
        """
[demo]
schema_version = 1
seed = 1729
bins_per_asset = 4
assets = ["BTC-PERP", "ETH-PERP"]

[output]
directory = "artifacts"
""".strip()
        + "\n",
        encoding="utf-8",
    )
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(Path(__file__).parents[1] / "src")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "xid.demo",
            "--config",
            str(config_path),
            "--root",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        env=environment,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (tmp_path / "artifacts" / "summary.json").is_file()
    assert '"evidence_scope": "software-smoke-only"' in completed.stdout
