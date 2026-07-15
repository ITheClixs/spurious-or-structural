from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import t as student_t  # type: ignore[import-untyped]

from xid.sim.g1 import (
    CenteredMoments,
    ShardIdentity,
    analytic_targets,
    build_fixture,
    estimate_from_moments,
    generate_batch,
    load_g1_config,
    load_shard_checkpoint,
    run_shards,
    runtime_sha256,
    write_shard_checkpoint,
)

_TEST_SEED = 1729


def _config_path() -> Path:
    return Path(__file__).parents[1] / "configs/g1.toml"


def test_generated_batch_satisfies_both_structural_equations() -> None:
    config = load_g1_config(_config_path())
    fixture = build_fixture(config)

    batch = generate_batch(fixture, rows=512, master_seed=_TEST_SEED, shard_index=0)

    return_residual = batch.r - (
        batch.q @ fixture.lambda_matrix.T + batch.f @ fixture.gamma.T + batch.u
    )
    flow_residual = batch.q - (batch.r @ fixture.feedback.T + batch.f @ fixture.delta_f.T + batch.v)
    scale = max(1.0, float(np.max(np.abs(batch.q))), float(np.max(np.abs(batch.r))))
    np.testing.assert_allclose(return_residual, 0.0, rtol=0.0, atol=1e-12 * scale)
    np.testing.assert_allclose(flow_residual, 0.0, rtol=0.0, atol=1e-12 * scale)
    np.testing.assert_array_equal(batch.fhat, batch.f + batch.epsilon)


def test_rng_keys_are_reproducible_and_shard_specific() -> None:
    config = load_g1_config(_config_path())
    fixture = build_fixture(config)

    first = generate_batch(fixture, rows=32, master_seed=_TEST_SEED, shard_index=7)
    repeated = generate_batch(fixture, rows=32, master_seed=_TEST_SEED, shard_index=7)
    different = generate_batch(fixture, rows=32, master_seed=_TEST_SEED, shard_index=8)

    np.testing.assert_array_equal(first.combined(), repeated.combined())
    assert not np.array_equal(first.combined(), different.combined())


def test_centered_moment_merge_matches_direct_and_is_partition_invariant() -> None:
    rng = np.random.Generator(np.random.PCG64DXSM(1729))
    rows = rng.standard_normal((41, 7))

    direct = CenteredMoments.from_rows(rows)
    first_partition = CenteredMoments.from_rows(rows[:9])
    second_partition = CenteredMoments.from_rows(rows[9:])
    left = first_partition.merge(second_partition)
    partitioned = (
        CenteredMoments.from_rows(rows[:5])
        .merge(CenteredMoments.from_rows(rows[5:17]))
        .merge(CenteredMoments.from_rows(rows[17:]))
    )

    assert left.count == direct.count == partitioned.count
    np.testing.assert_allclose(left.mean, direct.mean, rtol=0.0, atol=2e-15)
    np.testing.assert_allclose(partitioned.mean, direct.mean, rtol=0.0, atol=2e-15)
    np.testing.assert_allclose(left.scatter, direct.scatter, rtol=2e-15, atol=5e-14)
    np.testing.assert_allclose(partitioned.scatter, direct.scatter, rtol=2e-15, atol=5e-14)
    naive_within_partition_sum = first_partition.scatter + second_partition.scatter
    assert float(np.max(np.abs(naive_within_partition_sum - direct.scatter))) > 0.1


def test_checkpoint_round_trip_rejects_payload_tampering(tmp_path: Path) -> None:
    rows = np.arange(30, dtype=np.float64).reshape(10, 3)
    moments = CenteredMoments.from_rows(rows)
    identity = ShardIdentity(
        config_sha256="a" * 64,
        code_sha="test-code-sha",
        numpy_version=np.__version__,
        runtime_sha256=runtime_sha256(),
        master_seed=1729,
        shard_index=2,
        rows=10,
    )
    checkpoint = tmp_path / "shard-00002"
    write_shard_checkpoint(
        checkpoint,
        moments=moments,
        identity=identity,
        elapsed_seconds=0.5,
        peak_rss_bytes=12_345_678,
    )

    loaded = load_shard_checkpoint(checkpoint, expected=identity)

    assert loaded.count == moments.count
    np.testing.assert_array_equal(loaded.mean, moments.mean)
    np.testing.assert_array_equal(loaded.scatter, moments.scatter)
    metadata = json.loads((checkpoint / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["rng_keys"] == {
        "epsilon": [1729, 2, 3],
        "f": [1729, 2, 0],
        "u": [1729, 2, 1],
        "v": [1729, 2, 2],
    }
    with pytest.raises(ValueError, match="checkpoint identity mismatch"):
        load_shard_checkpoint(
            checkpoint,
            expected=replace(identity, runtime_sha256="c" * 64),
        )
    payload = checkpoint / "moments.npz"
    payload.write_bytes(payload.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="payload SHA256 mismatch"):
        load_shard_checkpoint(checkpoint, expected=identity)


def test_interrupted_shard_run_resumes_without_regeneration(tmp_path: Path) -> None:
    base = load_g1_config(_config_path())
    config = replace(
        base,
        master_seed=_TEST_SEED,
        n_samples=512,
        shard_size=256,
        checkpoint_directory=tmp_path / "checkpoints",
        output_directory=tmp_path / "results",
    )
    fixture = build_fixture(config)
    config_sha = "b" * 64
    code_sha = "test-code-sha"

    interrupted = run_shards(
        config,
        fixture,
        config_sha256=config_sha,
        code_sha=code_sha,
        max_new_shards=1,
    )
    resumed = run_shards(
        config,
        fixture,
        config_sha256=config_sha,
        code_sha=code_sha,
    )
    replayed = run_shards(
        config,
        fixture,
        config_sha256=config_sha,
        code_sha=code_sha,
    )
    fresh_config = replace(config, checkpoint_directory=tmp_path / "fresh-checkpoints")
    uninterrupted = run_shards(
        fresh_config,
        fixture,
        config_sha256=config_sha,
        code_sha=code_sha,
    )

    assert interrupted.moments.count == 256
    assert interrupted.new_shards == 1
    assert resumed.moments.count == 512
    assert resumed.new_shards == 1
    assert resumed.reused_shards == 1
    assert replayed.new_shards == 0
    assert replayed.reused_shards == 2
    np.testing.assert_array_equal(resumed.moments.mean, replayed.moments.mean)
    np.testing.assert_array_equal(resumed.moments.scatter, replayed.moments.scatter)
    np.testing.assert_array_equal(resumed.moments.mean, uninterrupted.moments.mean)
    np.testing.assert_array_equal(resumed.moments.scatter, uninterrupted.moments.scatter)

    with pytest.raises(ValueError, match="checkpoint identity mismatch"):
        run_shards(
            config,
            fixture,
            config_sha256=config_sha,
            code_sha="changed-code-sha",
        )


def test_resume_rejects_slow_shards_and_cumulative_budget_bypass(tmp_path: Path) -> None:
    base = load_g1_config(_config_path())
    config = replace(
        base,
        master_seed=_TEST_SEED,
        n_samples=512,
        shard_size=256,
        expected_wall_seconds=10,
        hard_stop_wall_seconds=15,
        checkpoint_directory=tmp_path / "checkpoints",
        output_directory=tmp_path / "results",
    )
    fixture = build_fixture(config)
    config_sha = "b" * 64
    code_sha = "test-code-sha"
    for shard_index in range(2):
        batch = generate_batch(
            fixture,
            rows=config.shard_size,
            master_seed=config.master_seed,
            shard_index=shard_index,
        )
        identity = ShardIdentity(
            config_sha256=config_sha,
            code_sha=code_sha,
            numpy_version=np.__version__,
            runtime_sha256=runtime_sha256(),
            master_seed=config.master_seed,
            shard_index=shard_index,
            rows=config.shard_size,
        )
        write_shard_checkpoint(
            config.checkpoint_directory / f"shard-{shard_index:05d}",
            moments=CenteredMoments.from_rows(batch.combined()),
            identity=identity,
            elapsed_seconds=8.0,
            peak_rss_bytes=12_345_678,
        )

    with pytest.raises(RuntimeError, match="cumulative G1 shard time reached"):
        run_shards(
            config,
            fixture,
            config_sha256=config_sha,
            code_sha=code_sha,
        )

    slow_config = replace(
        config,
        n_samples=256,
        expected_wall_seconds=500,
        hard_stop_wall_seconds=1_000,
        checkpoint_directory=tmp_path / "slow-checkpoints",
    )
    batch = generate_batch(
        fixture,
        rows=slow_config.shard_size,
        master_seed=slow_config.master_seed,
        shard_index=0,
    )
    identity = ShardIdentity(
        config_sha256=config_sha,
        code_sha=code_sha,
        numpy_version=np.__version__,
        runtime_sha256=runtime_sha256(),
        master_seed=slow_config.master_seed,
        shard_index=0,
        rows=slow_config.shard_size,
    )
    write_shard_checkpoint(
        slow_config.checkpoint_directory / "shard-00000",
        moments=CenteredMoments.from_rows(batch.combined()),
        identity=identity,
        elapsed_seconds=481.0,
        peak_rss_bytes=12_345_678,
    )
    with pytest.raises(RuntimeError, match="eight-minute design stop"):
        run_shards(
            slow_config,
            fixture,
            config_sha256=config_sha,
            code_sha=code_sha,
        )


def test_small_inference_smoke_reports_named_simultaneous_intervals() -> None:
    config = load_g1_config(_config_path())
    fixture = build_fixture(config)
    targets = analytic_targets(fixture)
    batch = generate_batch(fixture, rows=4_000, master_seed=9191, shard_index=0)
    moments = CenteredMoments.from_rows(batch.combined())

    estimates = estimate_from_moments(
        moments,
        fixture=fixture,
        targets=targets,
        familywise_confidence=config.familywise_confidence,
        coefficient_count=config.coefficient_count,
    )

    assert estimates.interval_method == "classical-homoskedastic-student-t-bonferroni"
    assert estimates.ols.coefficient.shape == (30, 30)
    assert estimates.controlled.coefficient.shape == (30, 30)
    assert estimates.ols.critical_value > 3.0
    assert estimates.controlled.critical_value > 3.0
    assert np.all(estimates.ols.lower < estimates.ols.coefficient)
    assert np.all(estimates.ols.coefficient < estimates.ols.upper)
    assert np.all(estimates.controlled.lower < estimates.controlled.coefficient)
    assert np.all(estimates.controlled.coefficient < estimates.controlled.upper)
    assert np.isfinite(estimates.gate_discrepancy)

    n_assets = fixture.n_assets
    ones = np.ones((batch.q.shape[0], 1), dtype=np.float64)
    ols_design = np.concatenate((ones, batch.q), axis=1)
    controlled_design = np.concatenate((ones, batch.q, batch.fhat), axis=1)
    for design, reported in (
        (ols_design, estimates.ols),
        (controlled_design, estimates.controlled),
    ):
        beta, _, _, _ = np.linalg.lstsq(design, batch.r, rcond=None)
        residual = batch.r - design @ beta
        degrees_freedom = batch.r.shape[0] - design.shape[1]
        residual_variance = np.sum(residual * residual, axis=0) / degrees_freedom
        inverse_design = np.linalg.solve(
            design.T @ design,
            np.eye(design.shape[1], dtype=np.float64),
        )
        direct_coefficient = beta[1 : n_assets + 1, :].T
        direct_standard_error = np.sqrt(
            residual_variance[:, None] * np.diag(inverse_design)[1 : n_assets + 1][None, :]
        )
        direct_critical = float(
            student_t.ppf(
                1.0 - (1.0 - config.familywise_confidence) / (2.0 * config.coefficient_count),
                degrees_freedom,
            )
        )
        np.testing.assert_allclose(
            reported.coefficient,
            direct_coefficient,
            rtol=3e-12,
            atol=3e-12,
        )
        np.testing.assert_allclose(
            reported.standard_error,
            direct_standard_error,
            rtol=1e-10,
            atol=1e-13,
        )
        assert reported.degrees_freedom == degrees_freedom
        assert reported.critical_value == pytest.approx(direct_critical, rel=1e-14)
        np.testing.assert_allclose(
            reported.lower,
            direct_coefficient - direct_critical * direct_standard_error,
            rtol=3e-12,
            atol=3e-12,
        )
        np.testing.assert_allclose(
            reported.upper,
            direct_coefficient + direct_critical * direct_standard_error,
            rtol=3e-12,
            atol=3e-12,
        )

    centered_q = batch.q - np.mean(batch.q, axis=0)
    centered_full = np.concatenate((batch.q, batch.fhat), axis=1)
    centered_full -= np.mean(centered_full, axis=0)
    raw_q_inverse = np.linalg.solve(
        centered_q.T @ centered_q,
        np.eye(n_assets, dtype=np.float64),
    )
    full_inverse = np.linalg.solve(
        centered_full.T @ centered_full,
        np.eye(centered_full.shape[1], dtype=np.float64),
    )
    assert float(np.max(np.abs(np.diag(raw_q_inverse) - np.diag(full_inverse)[:n_assets]))) > 1e-5
