"""Deterministic G0 smoke pipeline.

This module intentionally contains no estimator. Statistical work remains
locked behind the derivation and simulation gates.
"""

import argparse
import fcntl
import hashlib
import json
import tempfile
import tomllib
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

_UINT64_MASK = (1 << 64) - 1


@dataclass(frozen=True)
class DemoConfig:
    """Configuration for the dependency-light G0 smoke path."""

    schema_version: int
    seed: int
    bins_per_asset: int
    assets: tuple[str, ...]
    output_directory: Path


def _require_table(value: object, *, name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a table")
    return cast(dict[str, object], value)


def _require_exact_keys(table: dict[str, object], expected: set[str], *, name: str) -> None:
    if set(table) != expected:
        raise ValueError(f"{name} keys must be exactly {sorted(expected)}")


def _require_integer(value: object, *, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    return value


def _require_string(value: object, *, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def _output_is_unsafe(path: Path) -> bool:
    return path.is_absolute() or not path.parts or ".." in path.parts


def _validate_demo_config(config: DemoConfig) -> None:
    schema_version = _require_integer(config.schema_version, name="schema_version")
    if schema_version != 1:
        raise ValueError("unsupported demo schema_version")
    seed = _require_integer(config.seed, name="seed")
    if not 0 <= seed <= _UINT64_MASK:
        raise ValueError("seed must be an unsigned 64-bit integer")
    bins_per_asset = _require_integer(config.bins_per_asset, name="bins_per_asset")
    if bins_per_asset <= 0:
        raise ValueError("bins_per_asset must be positive")
    if not isinstance(config.assets, tuple) or not config.assets:
        raise ValueError("assets must be a non-empty tuple of strings")
    if any(not isinstance(asset, str) or not asset.strip() for asset in config.assets):
        raise ValueError("assets must be a non-empty tuple of strings")
    if len(set(config.assets)) != len(config.assets):
        raise ValueError("assets must be unique")
    if not isinstance(config.output_directory, Path) or _output_is_unsafe(config.output_directory):
        raise ValueError("output directory must stay below root")


def load_demo_config(path: Path) -> DemoConfig:
    """Load the versioned demo configuration."""
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    _require_exact_keys(raw, {"demo", "output"}, name="top-level config")
    demo = _require_table(raw["demo"], name="demo")
    output = _require_table(raw["output"], name="output")
    _require_exact_keys(
        demo,
        {"assets", "bins_per_asset", "schema_version", "seed"},
        name="demo",
    )
    _require_exact_keys(output, {"directory"}, name="output")

    schema_version = _require_integer(demo["schema_version"], name="schema_version")
    if schema_version != 1:
        raise ValueError("unsupported demo schema_version")
    seed = _require_integer(demo["seed"], name="seed")
    if not 0 <= seed <= _UINT64_MASK:
        raise ValueError("seed must be an unsigned 64-bit integer")
    bins_per_asset = _require_integer(demo["bins_per_asset"], name="bins_per_asset")
    if bins_per_asset <= 0:
        raise ValueError("bins_per_asset must be positive")

    raw_assets = demo["assets"]
    if not isinstance(raw_assets, list) or not raw_assets:
        raise ValueError("assets must be a non-empty list of strings")
    if any(not isinstance(asset, str) or not asset.strip() for asset in raw_assets):
        raise ValueError("assets must be a non-empty list of strings")
    assets = tuple(raw_assets)
    if len(set(assets)) != len(assets):
        raise ValueError("assets must be unique")

    output_directory = Path(_require_string(output["directory"], name="output directory"))
    if _output_is_unsafe(output_directory):
        raise ValueError("output directory must stay below root")

    config = DemoConfig(
        schema_version=schema_version,
        seed=seed,
        bins_per_asset=bins_per_asset,
        assets=assets,
        output_directory=output_directory,
    )
    _validate_demo_config(config)
    return config


def _stable_uint64(seed: int, asset_index: int, bin_index: int) -> int:
    """Return a platform-independent pseudo-random integer for smoke data."""
    value = (
        seed ^ ((asset_index + 1) * 0x9E3779B97F4A7C15) ^ ((bin_index + 1) * 0xD1B54A32D192ED03)
    ) & _UINT64_MASK
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & _UINT64_MASK
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & _UINT64_MASK
    return value ^ (value >> 31)


def _synthetic_records(config: DemoConfig) -> Iterator[dict[str, int | str]]:
    for bin_index in range(config.bins_per_asset):
        for asset_index, asset in enumerate(config.assets):
            value = _stable_uint64(config.seed, asset_index, bin_index)
            yield {
                "asset": asset,
                "bin_index": bin_index,
                "synthetic_signed_count": int(value % 2001) - 1000,
            }


def run_demo(config: DemoConfig, *, root: Path) -> dict[str, object]:
    """Run the deterministic, inference-free G0 smoke path."""
    _validate_demo_config(config)
    output_directory = root / config.output_directory
    output_directory.parent.mkdir(parents=True, exist_ok=True)
    data_path = output_directory / "synthetic_bins.jsonl"
    summary_path = output_directory / "summary.json"
    success_path = output_directory / "_SUCCESS"
    lock_path = output_directory.parent / f".{output_directory.name}.lock"

    with tempfile.TemporaryDirectory(prefix=".xid-demo-", dir=output_directory.parent) as stage:
        stage_directory = Path(stage)
        staged_data_path = stage_directory / data_path.name
        digest = hashlib.sha256()
        row_count = 0
        with staged_data_path.open("wb") as stream:
            for record in _synthetic_records(config):
                encoded = (
                    json.dumps(record, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
                    + "\n"
                ).encode("utf-8")
                stream.write(encoded)
                digest.update(encoded)
                row_count += 1

        summary: dict[str, object] = {
            "assets": list(config.assets),
            "bins_per_asset": config.bins_per_asset,
            "data_sha256": digest.hexdigest(),
            "evidence_scope": "software-smoke-only",
            "gate": "G0",
            "interval_status": "not-applicable-no-statistical-claim",
            "research_claim": "none",
            "row_count": row_count,
            "schema_version": config.schema_version,
            "seed": config.seed,
        }
        summary_bytes = (
            json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        staged_summary_path = stage_directory / summary_path.name
        staged_summary_path.write_bytes(summary_bytes)
        success = {
            "data_sha256": digest.hexdigest(),
            "summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
        }
        staged_success_path = stage_directory / success_path.name
        staged_success_path.write_text(
            json.dumps(success, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        output_directory.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a", encoding="utf-8") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            success_path.unlink(missing_ok=True)
            staged_data_path.replace(data_path)
            staged_summary_path.replace(summary_path)
            staged_success_path.replace(success_path)
            fcntl.flock(lock, fcntl.LOCK_UN)
        return summary


def main(argv: Sequence[str] | None = None) -> int:
    """Run the G0 demo command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    arguments = parser.parse_args(argv)
    summary = run_demo(load_demo_config(arguments.config), root=arguments.root)
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
