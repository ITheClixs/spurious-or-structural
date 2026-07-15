"""G1 probability-limit derivation and streamed simulation verifier."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import cast

import numpy as np
from numpy.typing import NDArray
from scipy.stats import t as student_t  # type: ignore[import-untyped]

FloatArray = NDArray[np.float64]

_UINT64_MAX = (1 << 64) - 1
_COMPONENT_IDS = {"f": 0, "u": 1, "v": 2, "epsilon": 3}
_INTERVAL_METHOD = "classical-homoskedastic-student-t-bonferroni"
NUMERICAL_THREAD_ENVIRONMENT = (
    "BLIS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
)
_IMPLEMENTATION_PATHS = (
    "src/xid",
    "configs/g1.toml",
    "pyproject.toml",
    "uv.lock",
    ".python-version",
)


@dataclass(frozen=True)
class SquareFormulaSpec:
    """Formula for a dense square matrix with a diagonal shift."""

    base: float
    row_scale: float
    column_scale: float
    diagonal_shift: float
    index_denominator: float


@dataclass(frozen=True)
class GammaFormulaSpec:
    """Formula for factor loadings in the return equation."""

    base: float
    sine_amplitude: float
    factor_scale: float
    sine_denominator: float


@dataclass(frozen=True)
class DeltaFormulaSpec:
    """Formula for factor loadings in the flow equation."""

    base: float
    cosine_amplitude: float
    factor_scale: float
    cosine_denominator: float
    factor_index_offset: float


@dataclass(frozen=True)
class ToeplitzCovarianceSpec:
    """Stationary exponential Toeplitz covariance specification."""

    variance: float
    distance_decay: float


@dataclass(frozen=True)
class G1Config:
    """Strict, versioned configuration for the preregistered G1 run."""

    schema_version: int
    master_seed: int
    benchmark_seed: int
    n_assets: int
    n_factors: int
    n_samples: int
    shard_size: int
    expected_wall_seconds: int
    hard_stop_wall_seconds: int
    phase_rss_abort_bytes: int
    absolute_rss_abort_bytes: int
    checkpoint_directory: Path
    output_directory: Path
    lambda_spec: SquareFormulaSpec
    feedback_spec: SquareFormulaSpec
    gamma_spec: GammaFormulaSpec
    delta_f_spec: DeltaFormulaSpec
    sigma_f_values: tuple[tuple[float, ...], ...]
    sigma_epsilon_values: tuple[tuple[float, ...], ...]
    sigma_u_spec: ToeplitzCovarianceSpec
    sigma_v_spec: ToeplitzCovarianceSpec
    relative_tolerance: float
    familywise_confidence: float
    coefficient_count: int
    analytic_round_digits: int
    ols_target_sha256: str
    proxy_target_sha256: str
    combined_target_sha256: str


@dataclass(frozen=True)
class G1Fixture:
    """Materialized structural matrices for one G1 data-generating process."""

    lambda_matrix: FloatArray
    feedback: FloatArray
    gamma: FloatArray
    delta_f: FloatArray
    sigma_f: FloatArray
    sigma_epsilon: FloatArray
    sigma_u: FloatArray
    sigma_v: FloatArray

    @property
    def n_assets(self) -> int:
        return int(self.lambda_matrix.shape[0])

    @property
    def n_factors(self) -> int:
        return int(self.gamma.shape[1])


@dataclass(frozen=True)
class AnalyticTargets:
    """Population coefficients and their separately derived bias components."""

    ols: FloatArray
    controlled: FloatArray
    ols_confounding_bias: FloatArray
    ols_simultaneity_bias: FloatArray
    controlled_confounding_bias: FloatArray
    controlled_simultaneity_bias: FloatArray
    sigma_qq: FloatArray
    sigma_q_partial: FloatArray
    sigma_x_proxy: FloatArray


@dataclass(frozen=True)
class TargetHashes:
    """Canonical hashes anchoring the preregistered analytic matrices."""

    ols: str
    controlled: str
    combined: str


@dataclass(frozen=True)
class GeneratedBatch:
    """One independently keyed batch from the simultaneous reduced form."""

    q: FloatArray
    r: FloatArray
    fhat: FloatArray
    f: FloatArray
    u: FloatArray
    v: FloatArray
    epsilon: FloatArray

    def combined(self) -> FloatArray:
        """Return rows ordered exactly as `[q, r, fhat]`."""
        return np.concatenate((self.q, self.r, self.fhat), axis=1)


@dataclass(frozen=True)
class CenteredMoments:
    """Mergeable row count, mean, and centered scatter matrix."""

    count: int
    mean: FloatArray
    scatter: FloatArray

    @classmethod
    def from_rows(cls, rows: FloatArray) -> CenteredMoments:
        """Compute centered sufficient statistics from a nonempty 2-D array."""
        values = np.asarray(rows, dtype=np.float64)
        if values.ndim != 2 or values.shape[0] == 0 or values.shape[1] == 0:
            raise ValueError("rows must be a nonempty two-dimensional array")
        if not np.all(np.isfinite(values)):
            raise ValueError("rows must be finite")
        mean = np.mean(values, axis=0, dtype=np.float64)
        centered = values - mean
        scatter = centered.T @ centered
        return cls(count=int(values.shape[0]), mean=mean, scatter=scatter)

    def merge(self, other: CenteredMoments) -> CenteredMoments:
        """Merge two partitions with the Chan--Golub--LeVeque identity."""
        if self.mean.shape != other.mean.shape or self.scatter.shape != other.scatter.shape:
            raise ValueError("moment dimensions do not match")
        if self.count <= 0 or other.count <= 0:
            raise ValueError("moment counts must be positive")
        total = self.count + other.count
        delta = other.mean - self.mean
        mean = self.mean + delta * (other.count / total)
        correction = np.outer(delta, delta) * (self.count * other.count / total)
        scatter = self.scatter + other.scatter + correction
        return CenteredMoments(count=total, mean=mean, scatter=scatter)


@dataclass(frozen=True)
class ShardIdentity:
    """Inputs that make one checkpoint safe to reuse."""

    config_sha256: str
    code_sha: str
    numpy_version: str
    runtime_sha256: str
    master_seed: int
    shard_index: int
    rows: int


@dataclass(frozen=True)
class ShardRunResult:
    """Aggregated sufficient statistics and resume accounting."""

    moments: CenteredMoments
    new_shards: int
    reused_shards: int
    elapsed_seconds: float
    generation_seconds: float
    peak_rss_bytes: int


@dataclass(frozen=True)
class ShardCheckpoint:
    """Validated moments and resource telemetry from one immutable shard."""

    moments: CenteredMoments
    elapsed_seconds: float
    peak_rss_bytes: int


@dataclass(frozen=True)
class CoefficientEstimate:
    """One coefficient matrix with simultaneous intervals and diagnostics."""

    coefficient: FloatArray
    standard_error: FloatArray
    lower: FloatArray
    upper: FloatArray
    signed_relative_error: FloatArray
    signed_relative_lower: FloatArray
    signed_relative_upper: FloatArray
    critical_value: float
    degrees_freedom: int
    max_relative_discrepancy: float
    target_in_all_intervals: bool


@dataclass(frozen=True)
class G1Estimates:
    """Both G1 regressions and the preregistered maximum discrepancy."""

    ols: CoefficientEstimate
    controlled: CoefficientEstimate
    gate_discrepancy: float
    interval_method: str = _INTERVAL_METHOD


@dataclass(frozen=True)
class PreregisteredRun:
    """Preflight evidence, streamed moments, and estimates for one G1 run."""

    target_hashes: TargetHashes
    shards: ShardRunResult
    estimates: G1Estimates | None


def _require_table(value: object, *, name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a table")
    return cast(dict[str, object], value)


def _require_exact_keys(table: dict[str, object], expected: set[str], *, name: str) -> None:
    if set(table) != expected:
        raise ValueError(f"{name} keys must be exactly {sorted(expected)}")


def _require_int(value: object, *, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    return value


def _require_float(value: object, *, name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"{name} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _require_string(value: object, *, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def _require_matrix(value: object, *, name: str) -> tuple[tuple[float, ...], ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a nonempty matrix")
    rows: list[tuple[float, ...]] = []
    for row_index, row in enumerate(value):
        if not isinstance(row, list) or not row:
            raise ValueError(f"{name}[{row_index}] must be a nonempty row")
        rows.append(
            tuple(
                _require_float(element, name=f"{name}[{row_index}][{column_index}]")
                for column_index, element in enumerate(row)
            )
        )
    if len({len(row) for row in rows}) != 1:
        raise ValueError(f"{name} rows must have equal length")
    return tuple(rows)


def _safe_relative_path(value: object, *, name: str) -> Path:
    path = Path(_require_string(value, name=name))
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"{name} must stay below the run root")
    return path


def _square_spec(table: dict[str, object], *, name: str) -> SquareFormulaSpec:
    keys = {"base", "row_scale", "column_scale", "diagonal_shift", "index_denominator"}
    _require_exact_keys(table, keys, name=name)
    return SquareFormulaSpec(
        base=_require_float(table["base"], name=f"{name}.base"),
        row_scale=_require_float(table["row_scale"], name=f"{name}.row_scale"),
        column_scale=_require_float(table["column_scale"], name=f"{name}.column_scale"),
        diagonal_shift=_require_float(table["diagonal_shift"], name=f"{name}.diagonal_shift"),
        index_denominator=_require_float(
            table["index_denominator"], name=f"{name}.index_denominator"
        ),
    )


def load_g1_config(path: Path) -> G1Config:
    """Load and strictly validate the frozen G1 configuration."""
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    top_level = {
        "experiment",
        "paths",
        "lambda",
        "feedback",
        "gamma",
        "delta_f",
        "sigma_f",
        "sigma_epsilon",
        "sigma_u",
        "sigma_v",
        "validation",
    }
    _require_exact_keys(raw, top_level, name="top-level G1 config")
    experiment = _require_table(raw["experiment"], name="experiment")
    _require_exact_keys(
        experiment,
        {
            "schema_version",
            "master_seed",
            "benchmark_seed",
            "n_assets",
            "n_factors",
            "n_samples",
            "shard_size",
            "expected_wall_seconds",
            "hard_stop_wall_seconds",
            "phase_rss_abort_bytes",
            "absolute_rss_abort_bytes",
        },
        name="experiment",
    )
    paths = _require_table(raw["paths"], name="paths")
    _require_exact_keys(paths, {"checkpoint_directory", "output_directory"}, name="paths")
    gamma = _require_table(raw["gamma"], name="gamma")
    _require_exact_keys(
        gamma,
        {"base", "sine_amplitude", "factor_scale", "sine_denominator"},
        name="gamma",
    )
    delta_f = _require_table(raw["delta_f"], name="delta_f")
    _require_exact_keys(
        delta_f,
        {
            "base",
            "cosine_amplitude",
            "factor_scale",
            "cosine_denominator",
            "factor_index_offset",
        },
        name="delta_f",
    )
    sigma_f = _require_table(raw["sigma_f"], name="sigma_f")
    sigma_epsilon = _require_table(raw["sigma_epsilon"], name="sigma_epsilon")
    _require_exact_keys(sigma_f, {"matrix"}, name="sigma_f")
    _require_exact_keys(sigma_epsilon, {"matrix"}, name="sigma_epsilon")
    sigma_u = _require_table(raw["sigma_u"], name="sigma_u")
    sigma_v = _require_table(raw["sigma_v"], name="sigma_v")
    _require_exact_keys(sigma_u, {"variance", "distance_decay"}, name="sigma_u")
    _require_exact_keys(sigma_v, {"variance", "distance_decay"}, name="sigma_v")
    validation = _require_table(raw["validation"], name="validation")
    _require_exact_keys(
        validation,
        {
            "relative_tolerance",
            "familywise_confidence",
            "coefficient_count",
            "analytic_round_digits",
            "ols_target_sha256",
            "proxy_target_sha256",
            "combined_target_sha256",
        },
        name="validation",
    )

    config = G1Config(
        schema_version=_require_int(experiment["schema_version"], name="schema_version"),
        master_seed=_require_int(experiment["master_seed"], name="master_seed"),
        benchmark_seed=_require_int(experiment["benchmark_seed"], name="benchmark_seed"),
        n_assets=_require_int(experiment["n_assets"], name="n_assets"),
        n_factors=_require_int(experiment["n_factors"], name="n_factors"),
        n_samples=_require_int(experiment["n_samples"], name="n_samples"),
        shard_size=_require_int(experiment["shard_size"], name="shard_size"),
        expected_wall_seconds=_require_int(
            experiment["expected_wall_seconds"], name="expected_wall_seconds"
        ),
        hard_stop_wall_seconds=_require_int(
            experiment["hard_stop_wall_seconds"], name="hard_stop_wall_seconds"
        ),
        phase_rss_abort_bytes=_require_int(
            experiment["phase_rss_abort_bytes"], name="phase_rss_abort_bytes"
        ),
        absolute_rss_abort_bytes=_require_int(
            experiment["absolute_rss_abort_bytes"], name="absolute_rss_abort_bytes"
        ),
        checkpoint_directory=_safe_relative_path(
            paths["checkpoint_directory"], name="checkpoint_directory"
        ),
        output_directory=_safe_relative_path(paths["output_directory"], name="output_directory"),
        lambda_spec=_square_spec(_require_table(raw["lambda"], name="lambda"), name="lambda"),
        feedback_spec=_square_spec(
            _require_table(raw["feedback"], name="feedback"), name="feedback"
        ),
        gamma_spec=GammaFormulaSpec(
            base=_require_float(gamma["base"], name="gamma.base"),
            sine_amplitude=_require_float(gamma["sine_amplitude"], name="gamma.sine_amplitude"),
            factor_scale=_require_float(gamma["factor_scale"], name="gamma.factor_scale"),
            sine_denominator=_require_float(
                gamma["sine_denominator"], name="gamma.sine_denominator"
            ),
        ),
        delta_f_spec=DeltaFormulaSpec(
            base=_require_float(delta_f["base"], name="delta_f.base"),
            cosine_amplitude=_require_float(
                delta_f["cosine_amplitude"], name="delta_f.cosine_amplitude"
            ),
            factor_scale=_require_float(delta_f["factor_scale"], name="delta_f.factor_scale"),
            cosine_denominator=_require_float(
                delta_f["cosine_denominator"], name="delta_f.cosine_denominator"
            ),
            factor_index_offset=_require_float(
                delta_f["factor_index_offset"], name="delta_f.factor_index_offset"
            ),
        ),
        sigma_f_values=_require_matrix(sigma_f["matrix"], name="sigma_f.matrix"),
        sigma_epsilon_values=_require_matrix(sigma_epsilon["matrix"], name="sigma_epsilon.matrix"),
        sigma_u_spec=ToeplitzCovarianceSpec(
            variance=_require_float(sigma_u["variance"], name="sigma_u.variance"),
            distance_decay=_require_float(sigma_u["distance_decay"], name="sigma_u.distance_decay"),
        ),
        sigma_v_spec=ToeplitzCovarianceSpec(
            variance=_require_float(sigma_v["variance"], name="sigma_v.variance"),
            distance_decay=_require_float(sigma_v["distance_decay"], name="sigma_v.distance_decay"),
        ),
        relative_tolerance=_require_float(
            validation["relative_tolerance"], name="relative_tolerance"
        ),
        familywise_confidence=_require_float(
            validation["familywise_confidence"], name="familywise_confidence"
        ),
        coefficient_count=_require_int(validation["coefficient_count"], name="coefficient_count"),
        analytic_round_digits=_require_int(
            validation["analytic_round_digits"], name="analytic_round_digits"
        ),
        ols_target_sha256=_require_string(
            validation["ols_target_sha256"], name="ols_target_sha256"
        ),
        proxy_target_sha256=_require_string(
            validation["proxy_target_sha256"], name="proxy_target_sha256"
        ),
        combined_target_sha256=_require_string(
            validation["combined_target_sha256"], name="combined_target_sha256"
        ),
    )
    _validate_loaded_config(config)
    return config


def _validate_loaded_config(config: G1Config) -> None:
    if config.schema_version != 1:
        raise ValueError("unsupported G1 schema_version")
    for name, seed in (
        ("master_seed", config.master_seed),
        ("benchmark_seed", config.benchmark_seed),
    ):
        if not 0 <= seed <= _UINT64_MAX:
            raise ValueError(f"{name} must be an unsigned 64-bit integer")
    if config.n_assets <= 0 or config.n_factors <= 0:
        raise ValueError("n_assets and n_factors must be positive")
    if config.n_samples <= 0 or config.shard_size <= 0:
        raise ValueError("n_samples and shard_size must be positive")
    if config.n_samples % config.shard_size != 0:
        raise ValueError("n_samples must be divisible by shard_size")
    if config.expected_wall_seconds <= 0 or config.hard_stop_wall_seconds <= 0:
        raise ValueError("wall-clock budgets must be positive")
    if config.expected_wall_seconds >= config.hard_stop_wall_seconds:
        raise ValueError("expected wall budget must be below the hard stop")
    if config.phase_rss_abort_bytes <= 0:
        raise ValueError("phase RSS abort must be positive")
    if config.phase_rss_abort_bytes >= config.absolute_rss_abort_bytes:
        raise ValueError("phase RSS abort must be below the absolute guard")
    if not 0.0 < config.relative_tolerance < 1.0:
        raise ValueError("relative_tolerance must lie in (0, 1)")
    if not 0.0 < config.familywise_confidence < 1.0:
        raise ValueError("familywise_confidence must lie in (0, 1)")
    if config.coefficient_count != 2 * config.n_assets * config.n_assets:
        raise ValueError("coefficient_count must cover both square coefficient matrices")
    if config.analytic_round_digits < 1:
        raise ValueError("analytic_round_digits must be positive")
    for name, digest in (
        ("ols_target_sha256", config.ols_target_sha256),
        ("proxy_target_sha256", config.proxy_target_sha256),
        ("combined_target_sha256", config.combined_target_sha256),
    ):
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ValueError(f"{name} must be a lowercase SHA256 digest")
    if len(config.sigma_f_values) != config.n_factors or any(
        len(row) != config.n_factors for row in config.sigma_f_values
    ):
        raise ValueError("sigma_f must be n_factors by n_factors")
    if len(config.sigma_epsilon_values) != config.n_factors or any(
        len(row) != config.n_factors for row in config.sigma_epsilon_values
    ):
        raise ValueError("sigma_epsilon must be n_factors by n_factors")


def _square_matrix(spec: SquareFormulaSpec, dimension: int) -> FloatArray:
    if spec.index_denominator <= 0.0:
        raise ValueError("index denominator must be positive")
    row_index = np.arange(1, dimension + 1, dtype=np.float64)[:, None]
    column_index = np.arange(1, dimension + 1, dtype=np.float64)[None, :]
    return (
        spec.base
        + spec.row_scale * row_index / spec.index_denominator
        + spec.column_scale * column_index / spec.index_denominator
        + spec.diagonal_shift * np.eye(dimension, dtype=np.float64)
    )


def _toeplitz_covariance(spec: ToeplitzCovarianceSpec, dimension: int) -> FloatArray:
    if spec.variance <= 0.0 or not 0.0 <= spec.distance_decay < 1.0:
        raise ValueError("Toeplitz variance must be positive and decay must lie in [0, 1)")
    indices = np.arange(dimension)
    distances = np.abs(indices[:, None] - indices[None, :])
    return spec.variance * np.power(spec.distance_decay, distances)


def build_fixture(config: G1Config) -> G1Fixture:
    """Materialize the frozen structural and covariance matrices."""
    asset_index = np.arange(1, config.n_assets + 1, dtype=np.float64)[:, None]
    factor_index = np.arange(1, config.n_factors + 1, dtype=np.float64)[None, :]
    gamma_spec = config.gamma_spec
    delta_spec = config.delta_f_spec
    if gamma_spec.sine_denominator <= 0.0 or delta_spec.cosine_denominator <= 0.0:
        raise ValueError("trigonometric denominators must be positive")
    gamma = (
        gamma_spec.base
        + gamma_spec.sine_amplitude
        * np.sin(asset_index * factor_index / gamma_spec.sine_denominator)
        + gamma_spec.factor_scale * factor_index
    )
    delta_f = (
        delta_spec.base
        + delta_spec.cosine_amplitude
        * np.cos(
            asset_index
            * (factor_index + delta_spec.factor_index_offset)
            / delta_spec.cosine_denominator
        )
        + delta_spec.factor_scale * factor_index
    )
    fixture = G1Fixture(
        lambda_matrix=_square_matrix(config.lambda_spec, config.n_assets),
        feedback=_square_matrix(config.feedback_spec, config.n_assets),
        gamma=gamma,
        delta_f=delta_f,
        sigma_f=np.asarray(config.sigma_f_values, dtype=np.float64),
        sigma_epsilon=np.asarray(config.sigma_epsilon_values, dtype=np.float64),
        sigma_u=_toeplitz_covariance(config.sigma_u_spec, config.n_assets),
        sigma_v=_toeplitz_covariance(config.sigma_v_spec, config.n_assets),
    )
    _validate_fixture(fixture)
    return fixture


def _validate_fixture(fixture: G1Fixture) -> None:
    n_assets = fixture.n_assets
    n_factors = fixture.n_factors
    expected_shapes = {
        "lambda": (fixture.lambda_matrix, (n_assets, n_assets)),
        "feedback": (fixture.feedback, (n_assets, n_assets)),
        "gamma": (fixture.gamma, (n_assets, n_factors)),
        "delta_f": (fixture.delta_f, (n_assets, n_factors)),
        "sigma_f": (fixture.sigma_f, (n_factors, n_factors)),
        "sigma_epsilon": (fixture.sigma_epsilon, (n_factors, n_factors)),
        "sigma_u": (fixture.sigma_u, (n_assets, n_assets)),
        "sigma_v": (fixture.sigma_v, (n_assets, n_assets)),
    }
    for name, (matrix, shape) in expected_shapes.items():
        if matrix.shape != shape or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} has invalid shape or nonfinite values")
    for name, covariance in (
        ("sigma_f", fixture.sigma_f),
        ("sigma_epsilon", fixture.sigma_epsilon),
        ("sigma_u", fixture.sigma_u),
        ("sigma_v", fixture.sigma_v),
    ):
        if not np.allclose(covariance, covariance.T, rtol=0.0, atol=1e-13):
            raise ValueError(f"{name} must be symmetric")
        if float(np.min(np.linalg.eigvalsh(covariance))) < -1e-12:
            raise ValueError(f"{name} must be positive semidefinite")
    loop_matrix = np.eye(n_assets) - fixture.feedback @ fixture.lambda_matrix
    if np.linalg.matrix_rank(loop_matrix) != n_assets:
        raise ValueError("I - B Lambda must be nonsingular")


def _right_solve(numerator: FloatArray, denominator: FloatArray) -> FloatArray:
    """Return `numerator @ inv(denominator)` without forming an inverse."""
    return np.linalg.solve(denominator.T, numerator.T).T


def _reduced_flow_parts(
    fixture: G1Fixture,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    identity = np.eye(fixture.n_assets, dtype=np.float64)
    h_matrix = np.linalg.solve(
        identity - fixture.feedback @ fixture.lambda_matrix,
        identity,
    )
    direct_factor = fixture.feedback @ fixture.gamma + fixture.delta_f
    return (
        h_matrix,
        h_matrix @ direct_factor,
        h_matrix @ fixture.feedback,
        h_matrix,
    )


def analytic_targets(fixture: G1Fixture) -> AnalyticTargets:
    """Evaluate the two primitive-only probability-limit formulas."""
    _, factor_flow, innovation_flow, flow_noise = _reduced_flow_parts(fixture)
    sigma_qq = (
        factor_flow @ fixture.sigma_f @ factor_flow.T
        + innovation_flow @ fixture.sigma_u @ innovation_flow.T
        + flow_noise @ fixture.sigma_v @ flow_noise.T
    )
    ols_confounding = _right_solve(
        fixture.gamma @ fixture.sigma_f @ factor_flow.T,
        sigma_qq,
    )
    ols_simultaneity = _right_solve(fixture.sigma_u @ innovation_flow.T, sigma_qq)
    proxy_covariance = fixture.sigma_f + fixture.sigma_epsilon
    residual_factor = fixture.sigma_f - fixture.sigma_f @ np.linalg.solve(
        proxy_covariance, fixture.sigma_f
    )
    sigma_q_partial = (
        factor_flow @ residual_factor @ factor_flow.T
        + innovation_flow @ fixture.sigma_u @ innovation_flow.T
        + flow_noise @ fixture.sigma_v @ flow_noise.T
    )
    controlled_confounding = _right_solve(
        fixture.gamma @ residual_factor @ factor_flow.T,
        sigma_q_partial,
    )
    controlled_simultaneity = _right_solve(
        fixture.sigma_u @ innovation_flow.T,
        sigma_q_partial,
    )
    sigma_qh = factor_flow @ fixture.sigma_f
    sigma_x_proxy = np.block([[sigma_qq, sigma_qh], [sigma_qh.T, proxy_covariance]]).astype(
        np.float64
    )
    return AnalyticTargets(
        ols=fixture.lambda_matrix + ols_confounding + ols_simultaneity,
        controlled=fixture.lambda_matrix + controlled_confounding + controlled_simultaneity,
        ols_confounding_bias=ols_confounding,
        ols_simultaneity_bias=ols_simultaneity,
        controlled_confounding_bias=controlled_confounding,
        controlled_simultaneity_bias=controlled_simultaneity,
        sigma_qq=sigma_qq,
        sigma_q_partial=sigma_q_partial,
        sigma_x_proxy=sigma_x_proxy,
    )


def analytic_targets_via_reduced_form(fixture: G1Fixture) -> AnalyticTargets:
    """Independently evaluate the targets from full reduced-form covariances."""
    baseline = analytic_targets(fixture)
    _, factor_flow, innovation_flow, flow_noise = _reduced_flow_parts(fixture)
    identity = np.eye(fixture.n_assets, dtype=np.float64)
    return_factor = fixture.lambda_matrix @ factor_flow + fixture.gamma
    return_innovation = fixture.lambda_matrix @ innovation_flow + identity
    return_flow_noise = fixture.lambda_matrix @ flow_noise
    sigma_qq = baseline.sigma_qq
    sigma_rq = (
        return_factor @ fixture.sigma_f @ factor_flow.T
        + return_innovation @ fixture.sigma_u @ innovation_flow.T
        + return_flow_noise @ fixture.sigma_v @ flow_noise.T
    )
    ols = _right_solve(sigma_rq, sigma_qq)
    sigma_qh = factor_flow @ fixture.sigma_f
    sigma_rh = return_factor @ fixture.sigma_f
    sigma_x = np.block(
        [
            [sigma_qq, sigma_qh],
            [sigma_qh.T, fixture.sigma_f + fixture.sigma_epsilon],
        ]
    ).astype(np.float64)
    sigma_rx = np.concatenate((sigma_rq, sigma_rh), axis=1)
    all_coefficients = _right_solve(sigma_rx, sigma_x)
    return replace(
        baseline,
        ols=ols,
        controlled=all_coefficients[:, : fixture.n_assets],
        sigma_x_proxy=sigma_x,
    )


def _canonical_matrix(matrix: FloatArray, digits: int) -> list[list[float]]:
    return [[round(float(value), digits) for value in row] for row in matrix]


def _canonical_json_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def canonical_target_hashes(targets: AnalyticTargets, *, digits: int) -> TargetHashes:
    """Hash the rounded matrices under the preregistered JSON convention."""
    if digits < 1:
        raise ValueError("digits must be positive")
    ols = _canonical_matrix(targets.ols, digits)
    controlled = _canonical_matrix(targets.controlled, digits)
    return TargetHashes(
        ols=_canonical_json_sha256(ols),
        controlled=_canonical_json_sha256(controlled),
        combined=_canonical_json_sha256({"controlled": controlled, "ols": ols}),
    )


def runtime_sha256() -> str:
    """Fingerprint the numerical runtime that can change generated moments."""
    return _canonical_json_sha256(
        {
            "machine": platform.machine(),
            "numpy_build": np.__config__.CONFIG,
            "numpy_version": np.__version__,
            "python_version": platform.python_version(),
            "system": platform.system(),
            "system_release": platform.release(),
            "thread_environment": {
                name: os.environ.get(name) for name in NUMERICAL_THREAD_ENVIRONMENT
            },
        }
    )


def validate_preregistered_targets(
    config: G1Config,
    targets: AnalyticTargets,
) -> TargetHashes:
    """Reject any analytic target that differs from the sealed preregistration."""
    observed = canonical_target_hashes(targets, digits=config.analytic_round_digits)
    expected = TargetHashes(
        ols=config.ols_target_sha256,
        controlled=config.proxy_target_sha256,
        combined=config.combined_target_sha256,
    )
    if observed != expected:
        raise ValueError(
            f"analytic target hash mismatch: expected={expected!r}, observed={observed!r}"
        )
    return observed


def _git_output(repository: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _validated_repository(root: Path) -> Path:
    repository = root.resolve()
    top_level = Path(_git_output(repository, "rev-parse", "--show-toplevel")).resolve()
    if repository != top_level:
        raise RuntimeError("G1 root must be the Git repository top level")
    return repository


def _require_clean_implementation(repository: Path) -> None:
    status = _git_output(
        repository,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        *_IMPLEMENTATION_PATHS,
    )
    if status:
        raise RuntimeError(f"implementation inputs are dirty:\n{status}")


def implementation_git_sha(root: Path) -> str:
    """Return the clean implementation commit from the repository top level."""
    repository = _validated_repository(root)
    _require_clean_implementation(repository)
    head = _git_output(repository, "rev-parse", "--verify", "HEAD^{commit}")
    if len(head) not in {40, 64} or any(character not in "0123456789abcdef" for character in head):
        raise RuntimeError("git returned an invalid implementation SHA")
    return head


def implementation_source_sha256(root: Path) -> str:
    """Hash the tracked implementation inputs independently of unrelated commits."""
    repository = _validated_repository(root)
    _require_clean_implementation(repository)
    listing = _git_output(repository, "ls-files", "--stage", "--", *_IMPLEMENTATION_PATHS)
    if not listing:
        raise RuntimeError("no tracked G1 implementation inputs found")
    tracked_paths = {
        line.split("\t", maxsplit=1)[1] for line in listing.splitlines() if "\t" in line
    }
    required = {".python-version", "configs/g1.toml", "pyproject.toml", "uv.lock"}
    if not required.issubset(tracked_paths) or not any(
        path.startswith("src/xid/") for path in tracked_paths
    ):
        raise RuntimeError("tracked G1 implementation inputs are incomplete")
    canonical = (listing + "\n").encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def max_relative_discrepancy(estimate: FloatArray, target: FloatArray) -> float:
    """Return the preregistered no-floor maximum elementwise relative error."""
    estimate_values = np.asarray(estimate, dtype=np.float64)
    target_values = np.asarray(target, dtype=np.float64)
    if estimate_values.shape != target_values.shape:
        raise ValueError("estimate and target shapes must match")
    if np.any(target_values == 0.0):
        raise ValueError("target contains zero; no denominator floor is permitted")
    return float(np.max(np.abs(estimate_values - target_values) / np.abs(target_values)))


def _normal_draws(
    covariance: FloatArray,
    *,
    rows: int,
    master_seed: int,
    shard_index: int,
    component_id: int,
) -> FloatArray:
    seed = np.random.SeedSequence([master_seed, shard_index, component_id])
    generator = np.random.Generator(np.random.PCG64DXSM(seed))
    standard = generator.standard_normal((rows, covariance.shape[0]), dtype=np.float64)
    if np.all(covariance == 0.0):
        return np.zeros_like(standard)
    cholesky = np.linalg.cholesky(covariance)
    return standard @ cholesky.T


def generate_batch(
    fixture: G1Fixture,
    *,
    rows: int,
    master_seed: int,
    shard_index: int,
) -> GeneratedBatch:
    """Generate one deterministic, independently keyed simultaneous-system batch."""
    if rows <= 0 or shard_index < 0:
        raise ValueError("rows must be positive and shard_index nonnegative")
    f = _normal_draws(
        fixture.sigma_f,
        rows=rows,
        master_seed=master_seed,
        shard_index=shard_index,
        component_id=_COMPONENT_IDS["f"],
    )
    u = _normal_draws(
        fixture.sigma_u,
        rows=rows,
        master_seed=master_seed,
        shard_index=shard_index,
        component_id=_COMPONENT_IDS["u"],
    )
    v = _normal_draws(
        fixture.sigma_v,
        rows=rows,
        master_seed=master_seed,
        shard_index=shard_index,
        component_id=_COMPONENT_IDS["v"],
    )
    epsilon = _normal_draws(
        fixture.sigma_epsilon,
        rows=rows,
        master_seed=master_seed,
        shard_index=shard_index,
        component_id=_COMPONENT_IDS["epsilon"],
    )
    _, factor_flow, innovation_flow, flow_noise = _reduced_flow_parts(fixture)
    q = f @ factor_flow.T + u @ innovation_flow.T + v @ flow_noise.T
    r = q @ fixture.lambda_matrix.T + f @ fixture.gamma.T + u
    return GeneratedBatch(q=q, r=r, fhat=f + epsilon, f=f, u=u, v=v, epsilon=epsilon)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: object) -> None:
    data = (
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    with path.open("wb") as stream:
        stream.write(data)
        stream.flush()


def _identity_payload(identity: ShardIdentity) -> dict[str, object]:
    return cast(dict[str, object], asdict(identity))


def _rng_keys(identity: ShardIdentity) -> dict[str, list[int]]:
    return {
        name: [identity.master_seed, identity.shard_index, component_id]
        for name, component_id in sorted(_COMPONENT_IDS.items())
    }


def write_shard_checkpoint(
    path: Path,
    *,
    moments: CenteredMoments,
    identity: ShardIdentity,
    elapsed_seconds: float,
    peak_rss_bytes: int,
) -> None:
    """Atomically publish one immutable, hash-validated shard directory."""
    if path.exists():
        raise FileExistsError(f"checkpoint already exists: {path}")
    if moments.count != identity.rows:
        raise ValueError("moment count does not match shard identity")
    if not math.isfinite(elapsed_seconds) or elapsed_seconds < 0.0:
        raise ValueError("checkpoint elapsed_seconds must be finite and nonnegative")
    if (
        not isinstance(peak_rss_bytes, int)
        or isinstance(peak_rss_bytes, bool)
        or peak_rss_bytes < 0
    ):
        raise ValueError("checkpoint peak_rss_bytes must be a nonnegative integer")
    path.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{path.name}.tmp-", dir=path.parent))
    try:
        payload_path = stage / "moments.npz"
        with payload_path.open("wb") as stream:
            np.savez(
                stream,
                count=np.array([moments.count], dtype=np.int64),
                mean=moments.mean,
                scatter=moments.scatter,
            )
            stream.flush()
        payload_sha256 = _sha256_file(payload_path)
        metadata = {
            "schema_version": 1,
            "identity": _identity_payload(identity),
            "rng_keys": _rng_keys(identity),
            "elapsed_seconds": elapsed_seconds,
            "peak_rss_bytes": peak_rss_bytes,
            "dimension": int(moments.mean.shape[0]),
            "payload_sha256": payload_sha256,
        }
        metadata_path = stage / "metadata.json"
        _write_json(metadata_path, metadata)
        _write_json(
            stage / "_SUCCESS",
            {
                "metadata_sha256": _sha256_file(metadata_path),
                "payload_sha256": payload_sha256,
            },
        )
        stage.replace(path)
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def _load_shard_record(path: Path, *, expected: ShardIdentity) -> ShardCheckpoint:
    """Load one shard's moments and telemetry after validating all hashes."""
    success_path = path / "_SUCCESS"
    metadata_path = path / "metadata.json"
    payload_path = path / "moments.npz"
    if not success_path.is_file() or not metadata_path.is_file() or not payload_path.is_file():
        raise ValueError("checkpoint is incomplete")
    success = json.loads(success_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(success, dict) or not isinstance(metadata, dict):
        raise ValueError("checkpoint metadata must be JSON objects")
    if success.get("metadata_sha256") != _sha256_file(metadata_path):
        raise ValueError("metadata SHA256 mismatch")
    payload_sha256 = _sha256_file(payload_path)
    if success.get("payload_sha256") != payload_sha256:
        raise ValueError("payload SHA256 mismatch")
    if metadata.get("payload_sha256") != payload_sha256:
        raise ValueError("payload SHA256 mismatch")
    if metadata.get("identity") != _identity_payload(expected):
        raise ValueError("checkpoint identity mismatch")
    if metadata.get("rng_keys") != _rng_keys(expected):
        raise ValueError("checkpoint RNG key mismatch")
    if metadata.get("schema_version") != 1:
        raise ValueError("checkpoint schema version mismatch")
    elapsed_value = metadata.get("elapsed_seconds")
    if (
        not isinstance(elapsed_value, int | float)
        or isinstance(elapsed_value, bool)
        or not math.isfinite(float(elapsed_value))
        or float(elapsed_value) < 0.0
    ):
        raise ValueError("checkpoint elapsed_seconds is invalid")
    peak_rss_value = metadata.get("peak_rss_bytes")
    if (
        not isinstance(peak_rss_value, int)
        or isinstance(peak_rss_value, bool)
        or peak_rss_value < 0
    ):
        raise ValueError("checkpoint peak_rss_bytes is invalid")
    with np.load(payload_path, allow_pickle=False) as archive:
        count_values = np.asarray(archive["count"], dtype=np.int64)
        mean = np.asarray(archive["mean"], dtype=np.float64)
        scatter = np.asarray(archive["scatter"], dtype=np.float64)
    if count_values.shape != (1,):
        raise ValueError("checkpoint count has invalid shape")
    count = int(count_values[0])
    if count != expected.rows or mean.ndim != 1 or scatter.shape != (mean.size, mean.size):
        raise ValueError("checkpoint moments have invalid dimensions")
    if not np.all(np.isfinite(mean)) or not np.all(np.isfinite(scatter)):
        raise ValueError("checkpoint moments must be finite")
    if metadata.get("dimension") != int(mean.size):
        raise ValueError("checkpoint metadata dimension mismatch")
    return ShardCheckpoint(
        moments=CenteredMoments(count=count, mean=mean, scatter=scatter),
        elapsed_seconds=float(elapsed_value),
        peak_rss_bytes=peak_rss_value,
    )


def load_shard_checkpoint(path: Path, *, expected: ShardIdentity) -> CenteredMoments:
    """Load one shard's moments only after identity, telemetry, and hashes validate."""
    return _load_shard_record(path, expected=expected).moments


def _max_rss_bytes() -> int:
    maximum = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return maximum if sys.platform == "darwin" else maximum * 1024


def _structural_residual(batch: GeneratedBatch, fixture: G1Fixture) -> float:
    return_error = batch.r - (
        batch.q @ fixture.lambda_matrix.T + batch.f @ fixture.gamma.T + batch.u
    )
    flow_error = batch.q - (batch.r @ fixture.feedback.T + batch.f @ fixture.delta_f.T + batch.v)
    return float(max(np.max(np.abs(return_error)), np.max(np.abs(flow_error))))


def run_shards(
    config: G1Config,
    fixture: G1Fixture,
    *,
    config_sha256: str,
    code_sha: str,
    max_new_shards: int | None = None,
) -> ShardRunResult:
    """Generate or reuse shards, then merge all available shards in fixed order."""
    if config.n_samples <= 0 or config.shard_size <= 0:
        raise ValueError("sample and shard sizes must be positive")
    if config.n_samples % config.shard_size != 0:
        raise ValueError("n_samples must be divisible by shard_size")
    if max_new_shards is not None and max_new_shards < 0:
        raise ValueError("max_new_shards must be nonnegative")
    total_shards = config.n_samples // config.shard_size
    start = time.perf_counter()
    aggregate: CenteredMoments | None = None
    new_shards = 0
    reused_shards = 0
    generation_seconds = 0.0
    shard_elapsed: list[float] = []
    runtime_identity = runtime_sha256()
    for shard_index in range(total_shards):
        identity = ShardIdentity(
            config_sha256=config_sha256,
            code_sha=code_sha,
            numpy_version=np.__version__,
            runtime_sha256=runtime_identity,
            master_seed=config.master_seed,
            shard_index=shard_index,
            rows=config.shard_size,
        )
        checkpoint = config.checkpoint_directory / f"shard-{shard_index:05d}"
        if checkpoint.exists():
            record = _load_shard_record(checkpoint, expected=identity)
            moments = record.moments
            elapsed = record.elapsed_seconds
            peak_rss = record.peak_rss_bytes
            reused_shards += 1
        else:
            if max_new_shards is not None and new_shards >= max_new_shards:
                break
            shard_start = time.perf_counter()
            batch = generate_batch(
                fixture,
                rows=config.shard_size,
                master_seed=config.master_seed,
                shard_index=shard_index,
            )
            residual = _structural_residual(batch, fixture)
            scale = max(1.0, float(np.max(np.abs(batch.q))), float(np.max(np.abs(batch.r))))
            if residual > 1e-12 * scale:
                raise RuntimeError(f"structural equation residual too large: {residual}")
            moments = CenteredMoments.from_rows(batch.combined())
            peak_rss = _max_rss_bytes()
            if peak_rss >= config.absolute_rss_abort_bytes:
                raise MemoryError("absolute RSS guard breached")
            if peak_rss >= config.phase_rss_abort_bytes:
                raise MemoryError("G1 phase RSS guard breached")
            elapsed = time.perf_counter() - shard_start
            if elapsed >= 480.0:
                raise RuntimeError("one G1 shard reached the eight-minute design stop")
            write_shard_checkpoint(
                checkpoint,
                moments=moments,
                identity=identity,
                elapsed_seconds=elapsed,
                peak_rss_bytes=peak_rss,
            )
            new_shards += 1
        if elapsed >= 480.0:
            raise RuntimeError("one G1 shard reached the eight-minute design stop")
        if peak_rss >= config.absolute_rss_abort_bytes:
            raise MemoryError("stored shard breached the absolute RSS guard")
        if peak_rss >= config.phase_rss_abort_bytes:
            raise MemoryError("stored shard breached the G1 phase RSS guard")
        generation_seconds += elapsed
        shard_elapsed.append(elapsed)
        aggregate = moments if aggregate is None else aggregate.merge(moments)
        total_elapsed = time.perf_counter() - start
        if total_elapsed >= config.hard_stop_wall_seconds:
            raise RuntimeError("G1 hard wall-clock stop reached after checkpointing")
        if generation_seconds >= config.hard_stop_wall_seconds:
            raise RuntimeError("cumulative G1 shard time reached the hard wall-clock stop")
        if generation_seconds >= 0.8 * config.hard_stop_wall_seconds:
            remaining = total_shards - (shard_index + 1)
            forecast = generation_seconds + float(np.mean(shard_elapsed)) * remaining
            if forecast >= config.hard_stop_wall_seconds:
                raise RuntimeError("G1 completion forecast exceeds the hard wall-clock stop")
    if aggregate is None:
        raise RuntimeError("no G1 shards are available")
    return ShardRunResult(
        moments=aggregate,
        new_shards=new_shards,
        reused_shards=reused_shards,
        elapsed_seconds=time.perf_counter() - start,
        generation_seconds=generation_seconds,
        peak_rss_bytes=_max_rss_bytes(),
    )


def _fit_coefficient_matrix(
    *,
    scatter: FloatArray,
    x_indices: NDArray[np.int64],
    y_indices: NDArray[np.int64],
    q_columns: int,
    count: int,
    target: FloatArray,
    familywise_confidence: float,
    coefficient_count: int,
) -> CoefficientEstimate:
    x_scatter = scatter[np.ix_(x_indices, x_indices)]
    xy_scatter = scatter[np.ix_(x_indices, y_indices)]
    y_scatter = scatter[np.ix_(y_indices, y_indices)]
    beta = np.linalg.solve(x_scatter, xy_scatter)
    residual_scatter = y_scatter - xy_scatter.T @ beta
    degrees_freedom = count - int(x_indices.size) - 1
    if degrees_freedom <= 0:
        raise ValueError("insufficient rows for regression inference")
    residual_variance = np.diag(residual_scatter) / degrees_freedom
    if np.any(residual_variance <= 0.0):
        raise ValueError("residual variances must be positive")
    inverse_design = np.linalg.solve(x_scatter, np.eye(x_indices.size, dtype=np.float64))
    coefficient = beta[:q_columns, :].T
    standard_error = np.sqrt(
        residual_variance[:, None] * np.diag(inverse_design)[:q_columns][None, :]
    )
    alpha = 1.0 - familywise_confidence
    tail_probability = alpha / (2.0 * coefficient_count)
    critical_value = float(student_t.ppf(1.0 - tail_probability, degrees_freedom))
    lower = coefficient - critical_value * standard_error
    upper = coefficient + critical_value * standard_error
    signed_relative_error = (coefficient - target) / target
    relative_endpoint_a = (lower - target) / target
    relative_endpoint_b = (upper - target) / target
    signed_relative_lower = np.minimum(relative_endpoint_a, relative_endpoint_b)
    signed_relative_upper = np.maximum(relative_endpoint_a, relative_endpoint_b)
    return CoefficientEstimate(
        coefficient=coefficient,
        standard_error=standard_error,
        lower=lower,
        upper=upper,
        signed_relative_error=signed_relative_error,
        signed_relative_lower=signed_relative_lower,
        signed_relative_upper=signed_relative_upper,
        critical_value=critical_value,
        degrees_freedom=degrees_freedom,
        max_relative_discrepancy=max_relative_discrepancy(coefficient, target),
        target_in_all_intervals=bool(np.all((lower <= target) & (target <= upper))),
    )


def estimate_from_moments(
    moments: CenteredMoments,
    *,
    fixture: G1Fixture,
    targets: AnalyticTargets,
    familywise_confidence: float,
    coefficient_count: int,
) -> G1Estimates:
    """Estimate both regressions and their Bonferroni Student-t intervals."""
    n_assets = fixture.n_assets
    n_factors = fixture.n_factors
    expected_dimension = 2 * n_assets + n_factors
    if moments.mean.shape != (expected_dimension,) or moments.scatter.shape != (
        expected_dimension,
        expected_dimension,
    ):
        raise ValueError("moment dimension does not match fixture")
    q_indices = np.arange(0, n_assets, dtype=np.int64)
    r_indices = np.arange(n_assets, 2 * n_assets, dtype=np.int64)
    factor_indices = np.arange(2 * n_assets, expected_dimension, dtype=np.int64)
    controlled_indices = np.concatenate((q_indices, factor_indices))
    ols = _fit_coefficient_matrix(
        scatter=moments.scatter,
        x_indices=q_indices,
        y_indices=r_indices,
        q_columns=n_assets,
        count=moments.count,
        target=targets.ols,
        familywise_confidence=familywise_confidence,
        coefficient_count=coefficient_count,
    )
    controlled = _fit_coefficient_matrix(
        scatter=moments.scatter,
        x_indices=controlled_indices,
        y_indices=r_indices,
        q_columns=n_assets,
        count=moments.count,
        target=targets.controlled,
        familywise_confidence=familywise_confidence,
        coefficient_count=coefficient_count,
    )
    return G1Estimates(
        ols=ols,
        controlled=controlled,
        gate_discrepancy=max(
            ols.max_relative_discrepancy,
            controlled.max_relative_discrepancy,
        ),
    )


def run_preregistered(
    config: G1Config,
    *,
    config_sha256: str,
    code_sha: str,
    max_new_shards: int | None = None,
) -> PreregisteredRun:
    """Validate sealed targets before drawing, then stream the G1 experiment."""
    _validate_loaded_config(config)
    fixture = build_fixture(config)
    targets = analytic_targets(fixture)
    hashes = validate_preregistered_targets(config, targets)
    alternative = analytic_targets_via_reduced_form(fixture)
    if not np.allclose(targets.ols, alternative.ols, rtol=0.0, atol=5e-13):
        raise RuntimeError("independent OLS analytic paths disagree")
    if not np.allclose(
        targets.controlled,
        alternative.controlled,
        rtol=0.0,
        atol=5e-13,
    ):
        raise RuntimeError("independent controlled analytic paths disagree")
    shards = run_shards(
        config,
        fixture,
        config_sha256=config_sha256,
        code_sha=code_sha,
        max_new_shards=max_new_shards,
    )
    estimates = None
    if shards.moments.count == config.n_samples:
        estimates = estimate_from_moments(
            shards.moments,
            fixture=fixture,
            targets=targets,
            familywise_confidence=config.familywise_confidence,
            coefficient_count=config.coefficient_count,
        )
    return PreregisteredRun(
        target_hashes=hashes,
        shards=shards,
        estimates=estimates,
    )
