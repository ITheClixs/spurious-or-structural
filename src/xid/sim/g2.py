"""Sealed G2 contract, test-only RNG namespace, and pure DGP transforms.

This module deliberately exposes no production authority.  The three registered
G2 seeds cannot pass :class:`TestRngNamespace`; resource, validation, and
research entry points are added only after their capability chain is tested.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import math
import platform
import sys
import tomllib
import weakref
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import ClassVar, cast

import numpy as np
from numpy.typing import NDArray


def _module_source_sha256() -> str:
    digest = hashlib.sha256()
    with Path(__file__).open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


_XID_LOADED_SOURCE_SHA256 = _module_source_sha256()


@dataclass(frozen=True, slots=True)
class G2Seals:
    """The four independent A005 immutability seals."""

    config_sha256: str
    target_raw_sha256: str
    target_semantic_sha256: str
    lasso_ratio_sha256: str


FROZEN_G2_SEALS = G2Seals(
    config_sha256="f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc",
    target_raw_sha256="f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59",
    target_semantic_sha256="f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a",
    lasso_ratio_sha256="1da884c55b3f6e7bf79012973bddf092a92efb1ea098cd2717a804645a62c9a0",
)

_FROZEN_CONFIG_RELATIVE = Path("configs/g2.toml")
_FROZEN_TARGET_RELATIVE = Path("configs/g2_population_targets.json")
_FROZEN_CONFIG_SCHEMA = 3
_FROZEN_TARGET_SCHEMA = 3
_FROZEN_RNG_SCHEMA = 2
_FROZEN_DESIGN = "S0004"
_REGISTERED_SEEDS = (2026071529, 2026071521, 2026071522)
_BOOTSTRAP_REPLICATES = 499
_FROZEN_POPULATION_TARGET_BINARY64_SHA256 = (
    "2ff803d9cf5e14f916266293d0c52e2712da2db7d5d0b6f5a410c4eaefff39c7"
)


class G2Stream(StrEnum):
    """Names whose phase/scenario pairs are frozen in the schema-3 config."""

    RESOURCE_SMOOTH = "resource_smooth"
    RESOURCE_PAPER = "resource_paper"
    VALIDATION_SIZE = "validation_size"
    VALIDATION_POWER = "validation_power"
    VALIDATION_DATE_FRONTIER = "validation_date_frontier"
    VALIDATION_RELIABILITY_FRONTIER_METADATA_ONLY = "validation_reliability_frontier_metadata_only"
    VALIDATION_RECOVERY = "validation_recovery"
    VALIDATION_IID = "validation_iid"
    VALIDATION_PAPER_RECOVERY = "validation_paper_recovery"
    RESEARCH = "research"


class G2Component(IntEnum):
    """Addressed stochastic components; bootstrap weights are component six."""

    FACTOR = 1
    FLOW_INNOVATION = 2
    RETURN_INNOVATION = 3
    LEVEL_NOISE = 4
    PROXY_NOISE = 5
    BOOTSTRAP_WEIGHTS = 6


@dataclass(frozen=True, slots=True)
class G2RuntimeFingerprint:
    """Numerical runtime fields that A006 binds before registered access."""

    python_implementation: str
    python_version: str
    numpy_version: str
    system: str
    machine: str
    byteorder: str
    rng_runtime_sha256: str


AUTHORIZED_G2_RUNTIME = G2RuntimeFingerprint(
    python_implementation="cpython",
    python_version="3.13.5",
    numpy_version="2.5.1",
    system="Darwin",
    machine="arm64",
    byteorder="little",
    rng_runtime_sha256="42e68bc3e6a54914539bbaf2cda979f6863e54a7442c654a098a6755d71052f9",
)

_RUNTIME_PREFLIGHT_TEST_SEED = 1729
_AUTHORIZED_STANDARD_NORMAL_HASHES = (
    (G2Component.FACTOR, "30a773aa28fb77cc545ad16862447c641f018e5293d2a3bac6c4d2407c641747"),
    (
        G2Component.FLOW_INNOVATION,
        "30f87c3b6ccf31deed2c0bb52bd60199fd4cc2427f3f3ab9771064b3091abde9",
    ),
    (
        G2Component.RETURN_INNOVATION,
        "e709ae59d68183c82c83699a340f2b60646af1492306668e27087538a293520b",
    ),
    (
        G2Component.LEVEL_NOISE,
        "593fe9b8e8f102bce0e58303a49b26cd713121c38e2219c9005ebaaf1c074091",
    ),
    (
        G2Component.PROXY_NOISE,
        "28d3f3b5b9e3fe24734d84456e3bbc1304394012fde1dca707c1f6ecbaac8243",
    ),
)
_AUTHORIZED_LEVEL_NOISE_RAW_HASH = (
    "4b513e5dee9968d985cca87af4640a9e466238afedcf6bece87784ab56ccfdf4"
)


def current_g2_runtime_fingerprint() -> G2RuntimeFingerprint:
    """Return the numerical-runtime and compiled-Generator identity used by A006."""
    generator_binary = Path(inspect.getfile(np.random.Generator))
    runtime_payload = {
        "mac_ver": platform.mac_ver(),
        "numpy_build": np.__config__.CONFIG,
        "numpy_generator_binary_sha256": hashlib.sha256(generator_binary.read_bytes()).hexdigest(),
        "python_build": platform.python_build(),
        "python_compiler": platform.python_compiler(),
        "system_release": platform.release(),
        "system_version": platform.version(),
    }
    runtime_payload_sha256 = hashlib.sha256(
        json.dumps(
            runtime_payload,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    return G2RuntimeFingerprint(
        python_implementation=sys.implementation.name,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        numpy_version=np.__version__,
        system=platform.system(),
        machine=platform.machine(),
        byteorder=sys.byteorder,
        rng_runtime_sha256=runtime_payload_sha256,
    )


@dataclass(frozen=True, slots=True)
class PopulationTarget:
    """Target fields needed to regenerate the structural DGP cell."""

    lambda_offdiag: float
    gamma: float
    market_return_shock_variance: float
    orthogonal_return_shock_variance: float


@dataclass(frozen=True, slots=True)
class PaperSpecificationContract:
    """One row from the frozen six-specification paper reconstruction table."""

    name: str
    feature_map: str
    estimator: str
    unpenalized: tuple[str, ...]
    penalized: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PaperReconstructionContract:
    """Executable thresholds and table rows for the sealed CCZ reconstruction."""

    names: tuple[str, ...]
    label: str
    fit_window_bins: int
    test_window_bins: int
    eligible_fit_blocks_per_date: int
    cv_validation_ranges: tuple[tuple[int, int], ...]
    best_level_index: int
    lambda_grid_size: int
    lambda_min_ratio: float
    selected_ratio_tolerance: float
    post_fwl_zero_norm_multiplier: float
    coordinate_descent_tolerance: float
    kkt_tolerance: float
    maximum_iterations: int
    pca_top_eigengap_min_trace_ratio: float
    bootstrap_replicates: int
    specifications: tuple[PaperSpecificationContract, ...]


@dataclass(frozen=True, slots=True)
class G2Contract:
    """Narrow typed projection of the already byte-sealed G2 contract."""

    seals: G2Seals
    config_schema_version: int
    target_schema_version: int
    target_config_schema_version: int
    rng_key_schema_version: int
    design_id: str
    target_design_id: str
    n_assets: int
    n_levels: int
    n_dates: int
    bins_per_date: int
    flow_pc1_share: float
    return_pc1_share: float
    factor_alignment: float
    lambda_diagonal: float
    confirmatory_ar1: float
    iid_ar1: float
    confirmatory_reliability: float
    level_average_error_variance: float
    ridge_condition_cap: float
    ridge_floor_trace_ratio: float
    ridge_negative_eigen_roundoff_multiplier: float
    ridge_post_condition_slack_multiplier: float
    pca_top_eigengap_min_trace_ratio: float
    pooled_rank_multiplier: float
    pooled_condition_number_max: float
    registered_seeds: tuple[int, int, int]
    phase_scenarios: tuple[tuple[G2Stream, int, int], ...]
    component_ids: tuple[tuple[G2Component, int], ...]
    draw_shapes: tuple[tuple[G2Component, tuple[int, ...]], ...]
    lasso_ratio_grid: tuple[float, ...]
    population_targets: tuple[PopulationTarget, ...]
    paper_reconstruction: PaperReconstructionContract

    def phase_scenario(self, stream: G2Stream) -> tuple[int, int]:
        """Return the unique frozen phase/scenario pair for ``stream``."""
        for candidate, phase, scenario in self.phase_scenarios:
            if candidate is stream:
                return phase, scenario
        raise ValueError(f"stream {stream!s} is absent from the sealed G2 contract")

    def draw_shape(self, component: G2Component) -> tuple[int, ...]:
        """Return the configured one-call standard-normal shape."""
        for candidate, shape in self.draw_shapes:
            if candidate is component:
                return shape
        raise ValueError(f"component {component!s} has no configured Gaussian shape")


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _semantic_value(value: object, *, digits: int) -> object:
    if value is None or isinstance(value, str | bool | int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("semantic target contains a nonfinite float")
        return round(value, digits)
    if isinstance(value, list):
        return [_semantic_value(item, digits=digits) for item in value]
    if isinstance(value, dict):
        converted: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("semantic target object keys must be strings")
            converted[key] = _semantic_value(item, digits=digits)
        return converted
    raise TypeError(f"unsupported semantic target value: {type(value).__name__}")


def semantic_target_bytes(value: object, *, digits: int) -> bytes:
    """Apply the frozen recursive rounding and compact JSON serialization."""
    if type(digits) is not int or digits < 0:
        raise ValueError("semantic rounding digits must be a nonnegative Python integer")
    canonical = _semantic_value(value, digits=digits)
    serialized = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return serialized.encode("utf-8") + b"\n"


def float64_le_sha256(values: tuple[float, ...] | list[float]) -> str:
    """Hash literal values in the frozen little-endian float64 C-order form."""
    packed = np.asarray(values, dtype="<f8")
    if packed.ndim != 1 or not packed.flags.c_contiguous:
        raise ValueError("LASSO ratio vector must be one-dimensional and C-contiguous")
    return _sha256(packed.tobytes(order="C"))


def _population_target_binary64_sha256(targets: tuple[PopulationTarget, ...]) -> str:
    packed = np.asarray(
        [
            (
                target.lambda_offdiag,
                target.gamma,
                target.market_return_shock_variance,
                target.orthogonal_return_shock_variance,
            )
            for target in targets
        ],
        dtype="<f8",
        order="C",
    )
    if packed.shape != (len(targets), 4) or not packed.flags.c_contiguous:
        raise ValueError("population targets must form a four-column C-order matrix")
    return _sha256(packed.tobytes(order="C"))


def validate_g2_seals(observed: G2Seals) -> None:
    """Fail with the exact corrupted seal role before any RNG can be reached."""
    if type(observed) is not G2Seals:
        raise ValueError("G2 seals must use the exact frozen G2Seals representation")
    for field in (
        "config_sha256",
        "target_raw_sha256",
        "target_semantic_sha256",
        "lasso_ratio_sha256",
    ):
        value = getattr(observed, field)
        if type(value) is not str or value != getattr(FROZEN_G2_SEALS, field):
            raise ValueError(f"G2 {field} does not match the A005 seal")


def _mapping(value: object, *, name: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be a string-keyed table")
    return cast(dict[str, object], value)


def _list(value: object, *, name: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be an array")
    return cast(list[object], value)


def _integer(value: object, *, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be a Python integer")
    return value


def _number(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _text(value: object, *, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be text")
    return value


def _field(table: dict[str, object], key: str, *, table_name: str) -> object:
    try:
        return table[key]
    except KeyError as error:
        raise ValueError(f"{table_name}.{key} is required") from error


def _table(table: dict[str, object], key: str, *, table_name: str) -> dict[str, object]:
    return _mapping(_field(table, key, table_name=table_name), name=f"{table_name}.{key}")


def _target_rows(target: dict[str, object]) -> tuple[PopulationTarget, ...]:
    rows = _list(_field(target, "targets", table_name="target"), name="target.targets")
    parsed: list[PopulationTarget] = []
    for index, raw_row in enumerate(rows):
        row = _mapping(raw_row, name=f"target.targets[{index}]")
        parsed.append(
            PopulationTarget(
                lambda_offdiag=_number(
                    _field(row, "lambda_offdiag", table_name=f"target.targets[{index}]"),
                    name=f"target.targets[{index}].lambda_offdiag",
                ),
                gamma=_number(
                    _field(row, "gamma", table_name=f"target.targets[{index}]"),
                    name=f"target.targets[{index}].gamma",
                ),
                market_return_shock_variance=_number(
                    _field(
                        row,
                        "market_return_shock_variance",
                        table_name=f"target.targets[{index}]",
                    ),
                    name=f"target.targets[{index}].market_return_shock_variance",
                ),
                orthogonal_return_shock_variance=_number(
                    _field(
                        row,
                        "orthogonal_return_shock_variance",
                        table_name=f"target.targets[{index}]",
                    ),
                    name=f"target.targets[{index}].orthogonal_return_shock_variance",
                ),
            )
        )
    return tuple(parsed)


_EXPECTED_PAPER_NAMES = ("PI_1", "PI_I", "CI_1", "CI_I", "PI_CC", "CI_CC")
_EXPECTED_PAPER_CV_RANGES = ((0, 6), (6, 12), (12, 18), (18, 24), (24, 30))
_EXPECTED_SELECTED_RATIO_RULE = (
    "compute_minimum_over_40_finite_pooled_mse_values_then_select_lowest_index_largest_ratio_"
    "satisfying_mse_k_less_than_or_equal_to_minimum_plus_float64_1e_minus_12_inclusive"
)
_EXPECTED_POST_FWL_ZERO_NORM_RULE = (
    "if_finite_scaled_residual_column_sum_squares_over_n_at_or_below_100_times_machine_"
    "epsilon_drop_and_fix_zero_if_nonfinite_fail_cell"
)
_EXPECTED_PAPER_SPECIFICATIONS = (
    PaperSpecificationContract(
        name="PI_1",
        feature_map="own_best_level_ofi",
        estimator="ols",
        unpenalized=("intercept", "own_best_level_ofi"),
        penalized=(),
    ),
    PaperSpecificationContract(
        name="PI_I",
        feature_map="own_integrated_top10_ofi",
        estimator="ols",
        unpenalized=("intercept", "own_integrated_top10_ofi"),
        penalized=(),
    ),
    PaperSpecificationContract(
        name="CI_1",
        feature_map="all_assets_best_level_ofi",
        estimator="lasso_per_response",
        unpenalized=("intercept",),
        penalized=("all_30_best_level_flows",),
    ),
    PaperSpecificationContract(
        name="CI_I",
        feature_map="all_assets_integrated_top10_ofi",
        estimator="lasso_per_response",
        unpenalized=("intercept",),
        penalized=("all_30_integrated_flows",),
    ),
    PaperSpecificationContract(
        name="PI_CC",
        feature_map="best_level_cross_section_pc1_plus_own_orthogonal_residual",
        estimator="ols",
        unpenalized=("intercept", "cross_section_pc1", "own_residual_flow"),
        penalized=(),
    ),
    PaperSpecificationContract(
        name="CI_CC",
        feature_map="best_level_cross_section_pc1_plus_all_orthogonal_residuals",
        estimator="lasso_per_response",
        unpenalized=("intercept", "cross_section_pc1"),
        penalized=("all_30_residual_flows",),
    ),
)


def _text_tuple(value: object, *, name: str) -> tuple[str, ...]:
    return tuple(
        _text(item, name=f"{name}[{index}]") for index, item in enumerate(_list(value, name=name))
    )


def _cv_ranges(value: object, *, name: str) -> tuple[tuple[int, int], ...]:
    parsed: list[tuple[int, int]] = []
    for index, item in enumerate(_list(value, name=name)):
        raw = _text(item, name=f"{name}[{index}]")
        parts = raw.split(":")
        if len(parts) != 2:
            raise ValueError(f"{name}[{index}] must be a zero-based half-open range")
        start, stop = (int(part) for part in parts)
        parsed.append((start, stop))
    return tuple(parsed)


def _paper_reconstruction_contract(
    paper: dict[str, object],
) -> PaperReconstructionContract:
    table_name = "config.opponent.paper_reconstruction"
    names = _text_tuple(_field(paper, "names", table_name=table_name), name=f"{table_name}.names")
    cv_ranges = _cv_ranges(
        _field(paper, "cv_validation_index_ranges_zero_based_half_open", table_name=table_name),
        name=f"{table_name}.cv_validation_index_ranges_zero_based_half_open",
    )

    selected_ratio_rule = _text(
        _field(paper, "selected_ratio_rule", table_name=table_name),
        name=f"{table_name}.selected_ratio_rule",
    )
    if selected_ratio_rule != _EXPECTED_SELECTED_RATIO_RULE:
        raise ValueError("config-declared paper selected-ratio rule changed")
    post_fwl_zero_norm_rule = _text(
        _field(paper, "post_fwl_zero_norm_rule", table_name=table_name),
        name=f"{table_name}.post_fwl_zero_norm_rule",
    )
    if post_fwl_zero_norm_rule != _EXPECTED_POST_FWL_ZERO_NORM_RULE:
        raise ValueError("config-declared paper post-FWL zero-norm rule changed")

    specification_rows = _list(
        _field(paper, "specifications", table_name=table_name),
        name=f"{table_name}.specifications",
    )
    specifications: list[PaperSpecificationContract] = []
    for index, raw_row in enumerate(specification_rows):
        row_name = f"{table_name}.specifications[{index}]"
        row = _mapping(raw_row, name=row_name)
        specifications.append(
            PaperSpecificationContract(
                name=_text(_field(row, "id", table_name=row_name), name=f"{row_name}.id"),
                feature_map=_text(
                    _field(row, "feature_map", table_name=row_name),
                    name=f"{row_name}.feature_map",
                ),
                estimator=_text(
                    _field(row, "estimator", table_name=row_name),
                    name=f"{row_name}.estimator",
                ),
                unpenalized=_text_tuple(
                    _field(row, "unpenalized", table_name=row_name),
                    name=f"{row_name}.unpenalized",
                ),
                penalized=_text_tuple(
                    _field(row, "penalized", table_name=row_name),
                    name=f"{row_name}.penalized",
                ),
            )
        )

    contract = PaperReconstructionContract(
        names=names,
        label=_text(_field(paper, "label", table_name=table_name), name=f"{table_name}.label"),
        fit_window_bins=_integer(
            _field(paper, "fit_window_bins", table_name=table_name),
            name=f"{table_name}.fit_window_bins",
        ),
        test_window_bins=_integer(
            _field(paper, "test_window_bins", table_name=table_name),
            name=f"{table_name}.test_window_bins",
        ),
        eligible_fit_blocks_per_date=_integer(
            _field(paper, "eligible_fit_blocks_per_date", table_name=table_name),
            name=f"{table_name}.eligible_fit_blocks_per_date",
        ),
        cv_validation_ranges=cv_ranges,
        best_level_index=_integer(
            _field(paper, "best_level_zero_based_index", table_name=table_name),
            name=f"{table_name}.best_level_zero_based_index",
        ),
        lambda_grid_size=_integer(
            _field(paper, "lambda_grid_size", table_name=table_name),
            name=f"{table_name}.lambda_grid_size",
        ),
        lambda_min_ratio=_number(
            _field(paper, "lambda_min_ratio", table_name=table_name),
            name=f"{table_name}.lambda_min_ratio",
        ),
        selected_ratio_tolerance=1e-12,
        post_fwl_zero_norm_multiplier=100.0,
        coordinate_descent_tolerance=_number(
            _field(paper, "coordinate_descent_tolerance", table_name=table_name),
            name=f"{table_name}.coordinate_descent_tolerance",
        ),
        kkt_tolerance=_number(
            _field(paper, "kkt_tolerance", table_name=table_name),
            name=f"{table_name}.kkt_tolerance",
        ),
        maximum_iterations=_integer(
            _field(paper, "maximum_iterations", table_name=table_name),
            name=f"{table_name}.maximum_iterations",
        ),
        pca_top_eigengap_min_trace_ratio=_number(
            _field(paper, "pca_top_eigengap_min_trace_ratio", table_name=table_name),
            name=f"{table_name}.pca_top_eigengap_min_trace_ratio",
        ),
        bootstrap_replicates=_integer(
            _field(paper, "bootstrap_replicates", table_name=table_name),
            name=f"{table_name}.bootstrap_replicates",
        ),
        specifications=tuple(specifications),
    )
    if (
        contract.names != _EXPECTED_PAPER_NAMES
        or contract.cv_validation_ranges != _EXPECTED_PAPER_CV_RANGES
    ):
        raise ValueError("config-declared paper reconstruction ranges or names changed")
    if contract.specifications != _EXPECTED_PAPER_SPECIFICATIONS:
        raise ValueError("config-declared paper specification table changed")
    return contract


_STREAMS_IN_CONFIG_ORDER = tuple(G2Stream)
_COMPONENT_CONFIG_NAMES = (
    (G2Component.FACTOR, "factor"),
    (G2Component.FLOW_INNOVATION, "flow_innovation"),
    (G2Component.RETURN_INNOVATION, "return_innovation"),
    (G2Component.LEVEL_NOISE, "level_noise"),
    (G2Component.PROXY_NOISE, "proxy_noise"),
    (G2Component.BOOTSTRAP_WEIGHTS, "bootstrap_weights"),
)
_DRAW_SHAPE_CONFIG_NAMES = (
    (G2Component.FACTOR, "factor"),
    (G2Component.FLOW_INNOVATION, "flow_innovation"),
    (G2Component.RETURN_INNOVATION, "return_innovation"),
    (G2Component.LEVEL_NOISE, "level_noise"),
    (G2Component.PROXY_NOISE, "proxy_noise"),
)


def load_g2_contract(root: Path) -> G2Contract:
    """Load only the rooted A005 config, validating all four seals in order."""
    rooted = root.resolve()
    config_path = (rooted / _FROZEN_CONFIG_RELATIVE).resolve()
    if config_path != rooted / _FROZEN_CONFIG_RELATIVE:
        raise ValueError("the frozen G2 config path must stay directly below root/configs")
    config_raw = config_path.read_bytes()
    config_sha = _sha256(config_raw)
    if config_sha != FROZEN_G2_SEALS.config_sha256:
        raise ValueError("G2 config_sha256 does not match the A005 seal")

    config_value = cast(object, tomllib.loads(config_raw.decode("utf-8")))
    config = _mapping(config_value, name="config")
    embedded_target_raw_sha = _text(
        _field(config, "population_targets_sha256", table_name="config"),
        name="config.population_targets_sha256",
    )
    embedded_target_semantic_sha = _text(
        _field(config, "population_targets_semantic_sha256", table_name="config"),
        name="config.population_targets_semantic_sha256",
    )
    if embedded_target_raw_sha != FROZEN_G2_SEALS.target_raw_sha256:
        raise ValueError("config-declared target raw SHA does not match the A005 seal")
    if embedded_target_semantic_sha != FROZEN_G2_SEALS.target_semantic_sha256:
        raise ValueError("config-declared target semantic SHA does not match the A005 seal")
    if (
        _text(
            _field(config, "population_targets_semantic_rounding", table_name="config"),
            name="config.population_targets_semantic_rounding",
        )
        != "python_round_half_even_decimal_places"
    ):
        raise ValueError("config-declared semantic rounding rule changed")
    if (
        _text(
            _field(config, "population_targets_semantic_serialization", table_name="config"),
            name="config.population_targets_semantic_serialization",
        )
        != "sorted_keys_compact_utf8_allow_nan_false_one_lf"
    ):
        raise ValueError("config-declared semantic serialization rule changed")
    target_relative = Path(
        _text(
            _field(config, "population_targets_file", table_name="config"),
            name="config.population_targets_file",
        )
    )
    target_path = (rooted / target_relative).resolve()
    if (
        target_relative != _FROZEN_TARGET_RELATIVE
        or target_path != rooted / _FROZEN_TARGET_RELATIVE
    ):
        raise ValueError("the sealed G2 population target path is not executable")
    target_raw = target_path.read_bytes()
    target_raw_sha = _sha256(target_raw)
    if target_raw_sha != FROZEN_G2_SEALS.target_raw_sha256:
        raise ValueError("G2 target_raw_sha256 does not match the A005 seal")

    target_value = cast(object, json.loads(target_raw))
    semantic_digits = _integer(
        _field(config, "population_targets_semantic_round_digits", table_name="config"),
        name="config.population_targets_semantic_round_digits",
    )
    target_semantic_sha = _sha256(semantic_target_bytes(target_value, digits=semantic_digits))
    if target_semantic_sha != FROZEN_G2_SEALS.target_semantic_sha256:
        raise ValueError("G2 target_semantic_sha256 does not match the A005 seal")

    opponents = _table(config, "opponent", table_name="config")
    paper = _table(
        opponents,
        "paper_reconstruction",
        table_name="config.opponent",
    )
    ratio_values = tuple(
        _number(item, name=f"lambda_ratio_grid_values[{index}]")
        for index, item in enumerate(
            _list(
                _field(
                    paper,
                    "lambda_ratio_grid_values",
                    table_name="config.opponent.paper_reconstruction",
                ),
                name="config.opponent.paper_reconstruction.lambda_ratio_grid_values",
            )
        )
    )
    ratio_sha = float64_le_sha256(list(ratio_values))
    if ratio_sha != FROZEN_G2_SEALS.lasso_ratio_sha256:
        raise ValueError("G2 lasso_ratio_sha256 does not match the A005 seal")
    if (
        _text(
            _field(
                paper,
                "lambda_ratio_grid_binary64_encoding",
                table_name="config.opponent.paper_reconstruction",
            ),
            name="config.opponent.paper_reconstruction.lambda_ratio_grid_binary64_encoding",
        )
        != "little_endian_float64_c_order"
    ):
        raise ValueError("config-declared LASSO ratio encoding changed")
    if (
        _text(
            _field(
                paper,
                "lambda_ratio_grid_binary64_sha256",
                table_name="config.opponent.paper_reconstruction",
            ),
            name="config.opponent.paper_reconstruction.lambda_ratio_grid_binary64_sha256",
        )
        != ratio_sha
    ):
        raise ValueError("config-declared LASSO ratio SHA does not match its literals")

    target = _mapping(target_value, name="target")
    dimensions = _table(config, "dimensions", table_name="config")
    dependence = _table(config, "dependence", table_name="config")
    numerics = _table(config, "numerics", table_name="config")
    confirmatory = _table(opponents, "confirmatory", table_name="config.opponent")
    observable_confirmatory = _table(
        opponents,
        "observable_confirmatory",
        table_name="config.opponent",
    )
    streams = _table(config, "streams", table_name="config")
    assignments = _table(streams, "phase_scenario_assignments", table_name="config.streams")
    component_ids_table = _table(streams, "component_ids", table_name="config.streams")
    draw_shapes_table = _table(streams, "draw_shapes", table_name="config.streams")
    calibration = _table(config, "calibration", table_name="config")
    observable = _table(calibration, "observable", table_name="config.calibration")
    impact = _table(calibration, "impact_sensitivity", table_name="config.calibration")
    proxy = _table(calibration, "proxy", table_name="config.calibration")
    measurement = _table(calibration, "measurement", table_name="config.calibration")

    encoded_numeric_rules = (
        (
            "ridge_negative_eigenvalue_roundoff_tolerance",
            "after_eigvalsh_fail_if_largest_eigenvalue_nonfinite_or_at_or_below_zero_"
            "tolerance_100_times_machine_epsilon_times_max_1_abs_largest_eigenvalue_"
            "values_in_closed_minus_tolerance_to_zero_are_accepted_as_roundoff_but_raw_"
            "values_are_retained_in_condition_penalty_formula_and_regularized_solve_more_"
            "negative_values_fail_once_symmetrized_schur_matrix_is_never_projected",
        ),
        (
            "ridge_post_regularization_condition_check",
            "fail_cell_if_smin_plus_penalty_nonfinite_or_at_or_below_zero_or_if_smax_plus_"
            "penalty_over_smin_plus_penalty_exceeds_condition_cap_times_one_plus_1000_times_"
            "machine_epsilon",
        ),
        (
            "pooled_rank_tolerance",
            "machine_epsilon_times_three_times_largest_singular_value",
        ),
    )
    for field, expected in encoded_numeric_rules:
        observed = _text(
            _field(numerics, field, table_name="config.numerics"),
            name=f"config.numerics.{field}",
        )
        if observed != expected:
            raise ValueError(f"config.numerics.{field} changed its sealed numerical rule")

    target_identity = (
        _integer(_field(target, "n_assets", table_name="target"), name="target.n_assets"),
        _number(
            _field(target, "flow_pc1_share", table_name="target"),
            name="target.flow_pc1_share",
        ),
        _number(
            _field(target, "return_pc1_share", table_name="target"),
            name="target.return_pc1_share",
        ),
        _number(
            _field(target, "factor_alignment", table_name="target"),
            name="target.factor_alignment",
        ),
        _number(
            _field(target, "proxy_reliability", table_name="target"),
            name="target.proxy_reliability",
        ),
        _number(
            _field(target, "level_pc1_share", table_name="target"),
            name="target.level_pc1_share",
        ),
    )
    config_identity = (
        _integer(
            _field(dimensions, "n_assets", table_name="config.dimensions"),
            name="config.dimensions.n_assets",
        ),
        _number(
            _field(observable, "flow_pc1_share", table_name="config.calibration.observable"),
            name="config.calibration.observable.flow_pc1_share",
        ),
        _number(
            _field(observable, "return_pc1_share", table_name="config.calibration.observable"),
            name="config.calibration.observable.return_pc1_share",
        ),
        _number(
            _field(observable, "factor_alignment", table_name="config.calibration.observable"),
            name="config.calibration.observable.factor_alignment",
        ),
        _number(
            _field(proxy, "confirmatory_reliability", table_name="config.calibration.proxy"),
            name="config.calibration.proxy.confirmatory_reliability",
        ),
        _number(
            _field(measurement, "level_pc1_share", table_name="config.calibration.measurement"),
            name="config.calibration.measurement.level_pc1_share",
        ),
    )
    if target_identity != config_identity:
        raise ValueError("target metadata and config calibration identity disagree")

    phase_scenarios: list[tuple[G2Stream, int, int]] = []
    for stream in _STREAMS_IN_CONFIG_ORDER:
        pair = _list(
            _field(
                assignments,
                stream.value,
                table_name="config.streams.phase_scenario_assignments",
            ),
            name=f"config.streams.phase_scenario_assignments.{stream.value}",
        )
        if len(pair) != 2:
            raise ValueError(f"stream {stream.value} must have one phase/scenario pair")
        phase_scenarios.append(
            (
                stream,
                _integer(pair[0], name=f"{stream.value}.phase"),
                _integer(pair[1], name=f"{stream.value}.scenario"),
            )
        )

    component_ids = tuple(
        (
            component,
            _integer(
                _field(component_ids_table, name, table_name="config.streams.component_ids"),
                name=f"config.streams.component_ids.{name}",
            ),
        )
        for component, name in _COMPONENT_CONFIG_NAMES
    )
    draw_shapes: list[tuple[G2Component, tuple[int, ...]]] = []
    for component, name in _DRAW_SHAPE_CONFIG_NAMES:
        raw_shape = _list(
            _field(draw_shapes_table, name, table_name="config.streams.draw_shapes"),
            name=f"config.streams.draw_shapes.{name}",
        )
        draw_shapes.append(
            (
                component,
                tuple(
                    _integer(item, name=f"config.streams.draw_shapes.{name}[{index}]")
                    for index, item in enumerate(raw_shape)
                ),
            )
        )

    contract = G2Contract(
        seals=G2Seals(config_sha, target_raw_sha, target_semantic_sha, ratio_sha),
        config_schema_version=_integer(
            _field(config, "schema_version", table_name="config"), name="config.schema_version"
        ),
        target_schema_version=_integer(
            _field(target, "target_schema_version", table_name="target"),
            name="target.target_schema_version",
        ),
        target_config_schema_version=_integer(
            _field(target, "config_schema_version", table_name="target"),
            name="target.config_schema_version",
        ),
        rng_key_schema_version=_integer(
            _field(streams, "rng_key_schema_version", table_name="config.streams"),
            name="config.streams.rng_key_schema_version",
        ),
        design_id=_text(_field(config, "design_id", table_name="config"), name="config.design_id"),
        target_design_id=_text(
            _field(target, "design_id", table_name="target"), name="target.design_id"
        ),
        n_assets=_integer(
            _field(dimensions, "n_assets", table_name="config.dimensions"),
            name="config.dimensions.n_assets",
        ),
        n_levels=_integer(
            _field(dimensions, "n_levels", table_name="config.dimensions"),
            name="config.dimensions.n_levels",
        ),
        n_dates=_integer(
            _field(dimensions, "n_dates", table_name="config.dimensions"),
            name="config.dimensions.n_dates",
        ),
        bins_per_date=_integer(
            _field(dimensions, "bins_per_date", table_name="config.dimensions"),
            name="config.dimensions.bins_per_date",
        ),
        flow_pc1_share=_number(
            _field(observable, "flow_pc1_share", table_name="config.calibration.observable"),
            name="config.calibration.observable.flow_pc1_share",
        ),
        return_pc1_share=_number(
            _field(observable, "return_pc1_share", table_name="config.calibration.observable"),
            name="config.calibration.observable.return_pc1_share",
        ),
        factor_alignment=_number(
            _field(observable, "factor_alignment", table_name="config.calibration.observable"),
            name="config.calibration.observable.factor_alignment",
        ),
        lambda_diagonal=_number(
            _field(impact, "lambda_diagonal", table_name="config.calibration.impact_sensitivity"),
            name="config.calibration.impact_sensitivity.lambda_diagonal",
        ),
        confirmatory_ar1=_number(
            _field(dependence, "confirmatory_ar1", table_name="config.dependence"),
            name="config.dependence.confirmatory_ar1",
        ),
        iid_ar1=_number(
            _field(dependence, "iid_diagnostic_ar1", table_name="config.dependence"),
            name="config.dependence.iid_diagnostic_ar1",
        ),
        confirmatory_reliability=_number(
            _field(proxy, "confirmatory_reliability", table_name="config.calibration.proxy"),
            name="config.calibration.proxy.confirmatory_reliability",
        ),
        level_average_error_variance=_number(
            _field(target, "level_average_error_variance", table_name="target"),
            name="target.level_average_error_variance",
        ),
        ridge_condition_cap=_number(
            _field(
                confirmatory,
                "condition_number_cap",
                table_name="config.opponent.confirmatory",
            ),
            name="config.opponent.confirmatory.condition_number_cap",
        ),
        ridge_floor_trace_ratio=_number(
            _field(
                confirmatory,
                "ridge_floor_trace_ratio",
                table_name="config.opponent.confirmatory",
            ),
            name="config.opponent.confirmatory.ridge_floor_trace_ratio",
        ),
        ridge_negative_eigen_roundoff_multiplier=100.0,
        ridge_post_condition_slack_multiplier=1000.0,
        pca_top_eigengap_min_trace_ratio=_number(
            _field(
                observable_confirmatory,
                "pca_top_eigengap_min_trace_ratio",
                table_name="config.opponent.observable_confirmatory",
            ),
            name="config.opponent.observable_confirmatory.pca_top_eigengap_min_trace_ratio",
        ),
        pooled_rank_multiplier=3.0,
        pooled_condition_number_max=_number(
            _field(
                numerics,
                "pooled_condition_number_max",
                table_name="config.numerics",
            ),
            name="config.numerics.pooled_condition_number_max",
        ),
        registered_seeds=(
            _integer(
                _field(streams, "resource_benchmark_seed", table_name="config.streams"),
                name="config.streams.resource_benchmark_seed",
            ),
            _integer(
                _field(streams, "validation_seed", table_name="config.streams"),
                name="config.streams.validation_seed",
            ),
            _integer(
                _field(streams, "research_seed", table_name="config.streams"),
                name="config.streams.research_seed",
            ),
        ),
        phase_scenarios=tuple(phase_scenarios),
        component_ids=component_ids,
        draw_shapes=tuple(draw_shapes),
        lasso_ratio_grid=ratio_values,
        population_targets=_target_rows(target),
        paper_reconstruction=_paper_reconstruction_contract(paper),
    )
    validate_g2_contract(contract)
    return contract


_EXPECTED_PHASE_SCENARIOS = (
    (G2Stream.RESOURCE_SMOOTH, 10, 0),
    (G2Stream.RESOURCE_PAPER, 10, 1),
    (G2Stream.VALIDATION_SIZE, 20, 0),
    (G2Stream.VALIDATION_POWER, 21, 0),
    (G2Stream.VALIDATION_DATE_FRONTIER, 22, 2),
    (G2Stream.VALIDATION_RELIABILITY_FRONTIER_METADATA_ONLY, 22, 3),
    (G2Stream.VALIDATION_RECOVERY, 23, 0),
    (G2Stream.VALIDATION_IID, 24, 0),
    (G2Stream.VALIDATION_PAPER_RECOVERY, 25, 4),
    (G2Stream.RESEARCH, 30, 0),
)
_EXPECTED_COMPONENT_IDS = tuple((component, int(component)) for component in G2Component)


def _validate_paper_reconstruction_runtime_types(paper: PaperReconstructionContract) -> None:
    if type(paper) is not PaperReconstructionContract:
        raise ValueError("sealed G2 contract paper reconstruction changed representation")
    integer_fields = (
        paper.fit_window_bins,
        paper.test_window_bins,
        paper.eligible_fit_blocks_per_date,
        paper.best_level_index,
        paper.lambda_grid_size,
        paper.maximum_iterations,
        paper.bootstrap_replicates,
    )
    if any(type(value) is not int for value in integer_fields):
        raise ValueError("sealed G2 contract paper integer fields changed representation")
    scalar_fields = (
        paper.lambda_min_ratio,
        paper.selected_ratio_tolerance,
        paper.post_fwl_zero_norm_multiplier,
        paper.coordinate_descent_tolerance,
        paper.kkt_tolerance,
        paper.pca_top_eigengap_min_trace_ratio,
    )
    if any(type(value) is not float for value in scalar_fields):
        raise ValueError("sealed G2 contract paper scalar fields changed representation")
    if type(paper.names) is not tuple or any(type(value) is not str for value in paper.names):
        raise ValueError("sealed G2 contract paper names changed representation")
    if type(paper.label) is not str:
        raise ValueError("sealed G2 contract paper label changed representation")
    if type(paper.cv_validation_ranges) is not tuple or any(
        type(row) is not tuple
        or len(row) != 2
        or type(row[0]) is not int
        or type(row[1]) is not int
        for row in paper.cv_validation_ranges
    ):
        raise ValueError("sealed G2 contract paper CV ranges changed representation")
    if type(paper.specifications) is not tuple:
        raise ValueError("sealed G2 contract paper specification table changed representation")
    for specification in paper.specifications:
        if (
            type(specification) is not PaperSpecificationContract
            or type(specification.name) is not str
            or type(specification.feature_map) is not str
            or type(specification.estimator) is not str
            or type(specification.unpenalized) is not tuple
            or any(type(value) is not str for value in specification.unpenalized)
            or type(specification.penalized) is not tuple
            or any(type(value) is not str for value in specification.penalized)
        ):
            raise ValueError("sealed G2 contract paper specification row changed representation")


def _validate_paper_reconstruction_contract(paper: PaperReconstructionContract) -> None:
    _validate_paper_reconstruction_runtime_types(paper)
    scalar_identity = (
        paper.lambda_min_ratio,
        paper.selected_ratio_tolerance,
        paper.post_fwl_zero_norm_multiplier,
        paper.coordinate_descent_tolerance,
        paper.kkt_tolerance,
        paper.pca_top_eigengap_min_trace_ratio,
    )
    expected_scalar_identity = (0.0001, 1e-12, 100.0, 1e-10, 1e-9, 1e-10)
    expected_identity = PaperReconstructionContract(
        names=_EXPECTED_PAPER_NAMES,
        label="paper_protocol_reconstruction",
        fit_window_bins=30,
        test_window_bins=30,
        eligible_fit_blocks_per_date=10,
        cv_validation_ranges=_EXPECTED_PAPER_CV_RANGES,
        best_level_index=0,
        lambda_grid_size=40,
        lambda_min_ratio=0.0001,
        selected_ratio_tolerance=1e-12,
        post_fwl_zero_norm_multiplier=100.0,
        coordinate_descent_tolerance=1e-10,
        kkt_tolerance=1e-9,
        maximum_iterations=10_000,
        pca_top_eigengap_min_trace_ratio=1e-10,
        bootstrap_replicates=_BOOTSTRAP_REPLICATES,
        specifications=_EXPECTED_PAPER_SPECIFICATIONS,
    )
    if tuple(value.hex() for value in scalar_identity) != tuple(
        value.hex() for value in expected_scalar_identity
    ):
        raise ValueError("sealed G2 contract paper numeric thresholds changed")
    if paper != expected_identity:
        raise ValueError("sealed G2 contract paper reconstruction table changed")


def _cell_scalars(contract: G2Contract, offdiagonal: float) -> tuple[float, ...]:
    n = float(contract.n_assets)
    q1 = n * contract.flow_pc1_share
    q0 = (n - q1) / (n - 1.0)
    r1 = n * contract.return_pc1_share
    r0 = (n - r1) / (n - 1.0)
    hq = math.sqrt(q1 - q0)
    lambda1 = contract.lambda_diagonal + (n - 1.0) * offdiagonal
    lambda0 = contract.lambda_diagonal - offdiagonal
    c1 = contract.factor_alignment * math.sqrt(r1 * q1)
    hr = (c1 - lambda1 * q0) / hq
    gamma = (c1 - lambda1 * q1) / hq
    market_variance = r1 - hr * hr - lambda1 * lambda1 * q0
    orthogonal_variance = r0 - lambda0 * lambda0 * q0
    return q1, q0, r1, r0, hq, gamma, market_variance, orthogonal_variance


def _validate_g2_contract_runtime_types(contract: G2Contract) -> None:
    """Reject equality-compatible but operationally different representations."""
    if type(contract) is not G2Contract:
        raise ValueError("sealed G2 contract must use the exact G2Contract representation")
    integer_fields = (
        contract.config_schema_version,
        contract.target_schema_version,
        contract.target_config_schema_version,
        contract.rng_key_schema_version,
        contract.n_assets,
        contract.n_levels,
        contract.n_dates,
        contract.bins_per_date,
    )
    if any(type(value) is not int for value in integer_fields):
        raise ValueError("sealed G2 contract integer fields changed representation")
    if type(contract.design_id) is not str or type(contract.target_design_id) is not str:
        raise ValueError("sealed G2 contract design fields changed representation")
    scalar_fields = (
        contract.flow_pc1_share,
        contract.return_pc1_share,
        contract.factor_alignment,
        contract.lambda_diagonal,
        contract.confirmatory_ar1,
        contract.iid_ar1,
        contract.confirmatory_reliability,
        contract.level_average_error_variance,
        contract.ridge_condition_cap,
        contract.ridge_floor_trace_ratio,
        contract.ridge_negative_eigen_roundoff_multiplier,
        contract.ridge_post_condition_slack_multiplier,
        contract.pca_top_eigengap_min_trace_ratio,
        contract.pooled_rank_multiplier,
        contract.pooled_condition_number_max,
    )
    if any(type(value) is not float for value in scalar_fields):
        raise ValueError("sealed G2 contract scalar fields changed representation")
    if type(contract.registered_seeds) is not tuple or any(
        type(value) is not int for value in contract.registered_seeds
    ):
        raise ValueError("sealed G2 contract registered seeds changed representation")
    if type(contract.phase_scenarios) is not tuple or any(
        type(row) is not tuple
        or len(row) != 3
        or type(row[0]) is not G2Stream
        or type(row[1]) is not int
        or type(row[2]) is not int
        for row in contract.phase_scenarios
    ):
        raise ValueError("sealed G2 contract phase/scenario table changed representation")
    if type(contract.component_ids) is not tuple or any(
        type(row) is not tuple
        or len(row) != 2
        or type(row[0]) is not G2Component
        or type(row[1]) is not int
        for row in contract.component_ids
    ):
        raise ValueError("sealed G2 contract component table changed representation")
    if type(contract.draw_shapes) is not tuple or any(
        type(row) is not tuple
        or len(row) != 2
        or type(row[0]) is not G2Component
        or type(row[1]) is not tuple
        or any(type(value) is not int for value in row[1])
        for row in contract.draw_shapes
    ):
        raise ValueError("sealed G2 contract draw shapes changed representation")
    if type(contract.lasso_ratio_grid) is not tuple or any(
        type(value) is not float for value in contract.lasso_ratio_grid
    ):
        raise ValueError("sealed G2 contract LASSO ratios changed representation")
    if type(contract.population_targets) is not tuple or any(
        type(target) is not PopulationTarget
        or type(target.lambda_offdiag) is not float
        or type(target.gamma) is not float
        or type(target.market_return_shock_variance) is not float
        or type(target.orthogonal_return_shock_variance) is not float
        for target in contract.population_targets
    ):
        raise ValueError("sealed G2 contract population targets changed representation")
    _validate_paper_reconstruction_runtime_types(contract.paper_reconstruction)


def validate_g2_contract(contract: G2Contract) -> None:
    """Revalidate the typed capability before every RNG-producing operation."""
    _validate_g2_contract_runtime_types(contract)
    validate_g2_seals(contract.seals)
    schema_identity = (
        contract.config_schema_version,
        contract.target_schema_version,
        contract.target_config_schema_version,
        contract.rng_key_schema_version,
        contract.design_id,
        contract.target_design_id,
    )
    if schema_identity != (3, 3, 3, 2, "S0004", "S0004"):
        raise ValueError("sealed G2 contract schema/design identity is not executable")
    if (contract.n_assets, contract.n_levels, contract.n_dates, contract.bins_per_date) != (
        30,
        10,
        252,
        330,
    ):
        raise ValueError("sealed G2 contract dimensions are not executable")
    if contract.registered_seeds != _REGISTERED_SEEDS:
        raise ValueError("sealed G2 contract registered seeds changed")
    scalar_identity = (
        contract.flow_pc1_share,
        contract.return_pc1_share,
        contract.factor_alignment,
        contract.lambda_diagonal,
        contract.confirmatory_ar1,
        contract.iid_ar1,
        contract.confirmatory_reliability,
        contract.level_average_error_variance,
        contract.ridge_condition_cap,
        contract.ridge_floor_trace_ratio,
        contract.ridge_negative_eigen_roundoff_multiplier,
        contract.ridge_post_condition_slack_multiplier,
        contract.pca_top_eigengap_min_trace_ratio,
        contract.pooled_rank_multiplier,
        contract.pooled_condition_number_max,
    )
    expected_scalar_identity = (
        0.2827,
        0.32,
        0.8726,
        0.29,
        0.60,
        0.0,
        0.95,
        547.0 / 39530.0,
        10_000.0,
        1e-6,
        100.0,
        1_000.0,
        1e-10,
        3.0,
        1e12,
    )
    if tuple(value.hex() for value in scalar_identity) != tuple(
        value.hex() for value in expected_scalar_identity
    ):
        raise ValueError("sealed G2 contract estimator numerics or calibration scalars changed")
    if contract.phase_scenarios != _EXPECTED_PHASE_SCENARIOS:
        raise ValueError("sealed G2 contract phase/scenario table changed")
    if contract.component_ids != _EXPECTED_COMPONENT_IDS:
        raise ValueError("sealed G2 contract component identifiers changed")
    expected_shapes = (
        (G2Component.FACTOR, (330,)),
        (G2Component.FLOW_INNOVATION, (330, 30)),
        (G2Component.RETURN_INNOVATION, (330, 30)),
        (G2Component.LEVEL_NOISE, (330, 30, 10)),
        (G2Component.PROXY_NOISE, (330,)),
    )
    if contract.draw_shapes != expected_shapes:
        raise ValueError("sealed G2 contract draw shapes changed")
    if len(contract.lasso_ratio_grid) != 40:
        raise ValueError("sealed G2 contract LASSO ratio count changed")
    ratios = np.asarray(contract.lasso_ratio_grid, dtype=np.float64)
    if (
        not np.all(np.isfinite(ratios))
        or ratios[0] != 1.0
        or ratios[-1] != 0.0001
        or not np.all(np.diff(ratios) < 0.0)
        or float64_le_sha256(list(contract.lasso_ratio_grid)) != FROZEN_G2_SEALS.lasso_ratio_sha256
    ):
        raise ValueError("sealed G2 contract LASSO ratio vector changed")
    if len(contract.population_targets) != 17:
        raise ValueError("sealed G2 contract population target count changed")
    if (
        _population_target_binary64_sha256(contract.population_targets)
        != _FROZEN_POPULATION_TARGET_BINARY64_SHA256
    ):
        raise ValueError("sealed G2 contract population target binary64 rows changed")
    offdiagonals = np.asarray(
        [target.lambda_offdiag for target in contract.population_targets], dtype=np.float64
    )
    if not np.array_equal(
        offdiagonals,
        np.linspace(0.0029, 0.0046, 17, dtype=np.float64),
    ):
        raise ValueError("sealed G2 contract off-diagonal grid changed")
    for index, target in enumerate(contract.population_targets):
        _, _, _, _, _, gamma, market_variance, orthogonal_variance = _cell_scalars(
            contract, target.lambda_offdiag
        )
        observed = np.asarray(
            [
                target.gamma,
                target.market_return_shock_variance,
                target.orthogonal_return_shock_variance,
            ]
        )
        regenerated = np.asarray([gamma, market_variance, orthogonal_variance])
        if not np.allclose(observed, regenerated, rtol=0.0, atol=5e-13):
            raise ValueError(f"sealed G2 contract population target {index} failed regeneration")
        if market_variance <= 0.0 or orthogonal_variance <= 0.0:
            raise ValueError(f"sealed G2 contract population target {index} is infeasible")
    if contract.level_average_error_variance != 547.0 / 39530.0:
        raise ValueError("sealed G2 contract level-average error variance changed")
    _validate_paper_reconstruction_contract(contract.paper_reconstruction)


@dataclass(frozen=True, slots=True)
class RNGAddress:
    """Exact thirteen-field RNG entropy address."""

    master_seed: int
    config_schema_version: int
    rng_key_schema_version: int
    phase_id: int
    scenario_id: int
    parent_phase_id: int
    parent_scenario_id: int
    n_dates: int
    panel_index: int
    cell_key: int
    date_index: int
    component_id: int
    replicate_index: int

    def __post_init__(self) -> None:
        self.validate_fields()

    def validate_fields(self) -> None:
        """Recheck exact integer types and signs after any object deserialization."""
        if type(self) is not RNGAddress:
            raise TypeError("RNG validation requires the exact RNGAddress type")
        for name, value in zip(
            (
                "master_seed",
                "config_schema_version",
                "rng_key_schema_version",
                "phase_id",
                "scenario_id",
                "parent_phase_id",
                "parent_scenario_id",
                "n_dates",
                "panel_index",
                "cell_key",
                "date_index",
                "component_id",
                "replicate_index",
            ),
            RNGAddress.entropy(self),
            strict=True,
        ):
            if type(value) is not int:
                raise TypeError(f"RNG address {name} must be a Python integer")
            if value < 0:
                raise ValueError(f"RNG address {name} must be nonnegative")
            if value >= 2**32:
                raise ValueError(f"RNG address {name} must be smaller than 2**32")

    def entropy(self) -> tuple[int, ...]:
        """Return fields in the exact schema-2 SeedSequence order."""
        return (
            self.master_seed,
            self.config_schema_version,
            self.rng_key_schema_version,
            self.phase_id,
            self.scenario_id,
            self.parent_phase_id,
            self.parent_scenario_id,
            self.n_dates,
            self.panel_index,
            self.cell_key,
            self.date_index,
            self.component_id,
            self.replicate_index,
        )


_METADATA_ONLY_STREAM = G2Stream.VALIDATION_RELIABILITY_FRONTIER_METADATA_ONLY
_BOOTSTRAP_PARENT_STREAMS = frozenset(
    (
        G2Stream.RESOURCE_SMOOTH,
        G2Stream.RESOURCE_PAPER,
        G2Stream.VALIDATION_SIZE,
        G2Stream.VALIDATION_POWER,
        G2Stream.VALIDATION_DATE_FRONTIER,
        G2Stream.VALIDATION_PAPER_RECOVERY,
        G2Stream.RESEARCH,
    )
)


def _stream_from_pair(contract: G2Contract, phase: int, scenario: int) -> G2Stream:
    matches = tuple(
        stream
        for stream, expected_phase, expected_scenario in contract.phase_scenarios
        if (phase, scenario) == (expected_phase, expected_scenario)
    )
    if len(matches) != 1 or matches[0] is _METADATA_ONLY_STREAM:
        raise ValueError("phase/scenario pair is not a generator-bearing G2 stream")
    return matches[0]


def _validate_stream_coordinates(
    stream: G2Stream,
    *,
    n_dates: int,
    panel_index: int,
    date_index: int,
) -> None:
    if type(stream) is not G2Stream:
        raise TypeError("stream must use the exact G2Stream enum type")
    for name, value in (
        ("n_dates", n_dates),
        ("panel_index", panel_index),
        ("date_index", date_index),
    ):
        if type(value) is not int or not 0 <= value < 2**32:
            raise ValueError(f"{name} must be a uint32-range Python integer")
    if stream is _METADATA_ONLY_STREAM:
        raise ValueError("the reliability-frontier stream is metadata-only and has no generator")
    allowed_dates = (
        frozenset((48, 96)) if stream is G2Stream.VALIDATION_DATE_FRONTIER else frozenset((252,))
    )
    if n_dates not in allowed_dates:
        raise ValueError(f"n_dates={n_dates} is not licensed for {stream.value}")
    if date_index >= n_dates:
        raise ValueError("date_index must be smaller than n_dates")
    if (
        stream
        in (
            G2Stream.VALIDATION_SIZE,
            G2Stream.VALIDATION_POWER,
            G2Stream.VALIDATION_DATE_FRONTIER,
            G2Stream.VALIDATION_RECOVERY,
            G2Stream.VALIDATION_IID,
        )
        and panel_index >= 100
    ):
        raise ValueError(f"panel_index must be 0 through 99 for {stream.value}")
    if stream in (G2Stream.VALIDATION_PAPER_RECOVERY, G2Stream.RESEARCH) and panel_index != 0:
        raise ValueError(f"panel_index must be zero for {stream.value}")


@dataclass(frozen=True, slots=True)
class TestRngNamespace:
    """A capability that is mechanically disjoint from registered G2 seeds."""

    __test__: ClassVar[bool] = False

    contract: G2Contract
    master_seed: int

    def _validate_authority(self) -> None:
        if type(self) is not TestRngNamespace:
            raise TypeError("RNG operations require the exact TestRngNamespace type")
        validate_g2_contract(self.contract)
        if type(self.master_seed) is not int or not 0 <= self.master_seed < 2**32:
            raise ValueError("test master seed must be a uint32-range Python integer")
        if self.master_seed in self.contract.registered_seeds:
            raise ValueError("TestRngNamespace refuses every registered G2 seed")

    def __post_init__(self) -> None:
        TestRngNamespace._validate_authority(self)

    @classmethod
    def from_contract(cls, contract: G2Contract, master_seed: int) -> TestRngNamespace:
        if cls is not TestRngNamespace:
            raise TypeError("RNG construction requires the exact TestRngNamespace type")
        return TestRngNamespace(contract=contract, master_seed=master_seed)

    def dgp_address(
        self,
        *,
        stream: G2Stream,
        n_dates: int,
        panel_index: int,
        date_index: int,
        component: G2Component,
    ) -> RNGAddress:
        TestRngNamespace._validate_authority(self)
        if type(stream) is not G2Stream or type(component) is not G2Component:
            raise TypeError("DGP addressing requires exact G2Stream and G2Component enums")
        if component is G2Component.BOOTSTRAP_WEIGHTS:
            raise ValueError("bootstrap weights do not use a DGP address")
        _validate_stream_coordinates(
            stream,
            n_dates=n_dates,
            panel_index=panel_index,
            date_index=date_index,
        )
        phase, scenario = self.contract.phase_scenario(stream)
        address = RNGAddress(
            master_seed=self.master_seed,
            config_schema_version=self.contract.config_schema_version,
            rng_key_schema_version=self.contract.rng_key_schema_version,
            phase_id=phase,
            scenario_id=scenario,
            parent_phase_id=0,
            parent_scenario_id=0,
            n_dates=n_dates,
            panel_index=panel_index,
            cell_key=0,
            date_index=date_index,
            component_id=int(component),
            replicate_index=0,
        )
        TestRngNamespace.validate_dgp_address(self, address)
        return address

    def validate_dgp_address(self, address: RNGAddress) -> tuple[int, ...]:
        TestRngNamespace._validate_authority(self)
        if type(address) is not RNGAddress:
            raise TypeError("DGP validation requires the exact RNGAddress type")
        RNGAddress.validate_fields(address)
        entropy = RNGAddress.entropy(address)
        stream = _stream_from_pair(self.contract, entropy[3], entropy[4])
        _validate_stream_coordinates(
            stream,
            n_dates=entropy[7],
            panel_index=entropy[8],
            date_index=entropy[10],
        )
        if (
            entropy[0] != self.master_seed
            or entropy[1] != self.contract.config_schema_version
            or entropy[2] != self.contract.rng_key_schema_version
            or entropy[5] != 0
            or entropy[6] != 0
            or entropy[9] != 0
            or entropy[11] not in range(1, 6)
            or entropy[12] != 0
        ):
            raise ValueError("invalid sealed G2 DGP address")
        return entropy

    def bootstrap_address(
        self,
        *,
        parent_stream: G2Stream,
        n_dates: int,
        panel_index: int,
        replicate_index: int,
    ) -> RNGAddress:
        TestRngNamespace._validate_authority(self)
        if type(parent_stream) is not G2Stream:
            raise TypeError("bootstrap addressing requires the exact G2Stream enum type")
        if parent_stream not in _BOOTSTRAP_PARENT_STREAMS:
            raise ValueError(f"{parent_stream.value} has no licensed date bootstrap")
        _validate_stream_coordinates(
            parent_stream,
            n_dates=n_dates,
            panel_index=panel_index,
            date_index=0,
        )
        if type(replicate_index) is not int or not 0 <= replicate_index < _BOOTSTRAP_REPLICATES:
            raise ValueError("bootstrap replicate_index must be 0 through 498")
        parent_phase, parent_scenario = self.contract.phase_scenario(parent_stream)
        address = RNGAddress(
            master_seed=self.master_seed,
            config_schema_version=self.contract.config_schema_version,
            rng_key_schema_version=self.contract.rng_key_schema_version,
            phase_id=40,
            scenario_id=0,
            parent_phase_id=parent_phase,
            parent_scenario_id=parent_scenario,
            n_dates=n_dates,
            panel_index=panel_index,
            cell_key=0,
            date_index=0,
            component_id=int(G2Component.BOOTSTRAP_WEIGHTS),
            replicate_index=replicate_index,
        )
        TestRngNamespace.validate_bootstrap_address(self, address)
        return address

    def validate_bootstrap_address(self, address: RNGAddress) -> tuple[int, ...]:
        TestRngNamespace._validate_authority(self)
        if type(address) is not RNGAddress:
            raise TypeError("bootstrap validation requires the exact RNGAddress type")
        RNGAddress.validate_fields(address)
        entropy = RNGAddress.entropy(address)
        parent_stream = _stream_from_pair(
            self.contract,
            entropy[5],
            entropy[6],
        )
        if parent_stream not in _BOOTSTRAP_PARENT_STREAMS:
            raise ValueError(f"{parent_stream.value} has no licensed date bootstrap")
        _validate_stream_coordinates(
            parent_stream,
            n_dates=entropy[7],
            panel_index=entropy[8],
            date_index=0,
        )
        if (
            entropy[0] != self.master_seed
            or entropy[1] != self.contract.config_schema_version
            or entropy[2] != self.contract.rng_key_schema_version
            or entropy[3] != 40
            or entropy[4] != 0
            or entropy[9] != 0
            or entropy[10] != 0
            or entropy[11] != int(G2Component.BOOTSTRAP_WEIGHTS)
            or not 0 <= entropy[12] < _BOOTSTRAP_REPLICATES
        ):
            raise ValueError("invalid sealed G2 bootstrap address")
        return entropy

    def draw_standard_normal(self, address: RNGAddress) -> NDArray[np.float64]:
        """Make the one exact configured Gaussian call for a test-only address."""
        entropy = TestRngNamespace.validate_dgp_address(self, address)
        component = G2Component(entropy[11])
        shape = self.contract.draw_shape(component)
        seed_sequence = np.random.SeedSequence(entropy)
        generator = np.random.Generator(np.random.PCG64DXSM(seed_sequence))
        values = generator.standard_normal(size=shape, dtype=np.float64)
        if values.dtype != np.float64 or values.shape != shape or not values.flags.c_contiguous:
            raise RuntimeError("configured standard-normal draw violated dtype/shape/C-order")
        return values

    def draw_bootstrap_weights(self, address: RNGAddress) -> NDArray[np.float64]:
        """Draw one exact multinomial date-weight vector and cast to float64."""
        entropy = TestRngNamespace.validate_bootstrap_address(self, address)
        n_dates = entropy[7]
        pvals = np.full(
            n_dates,
            1.0 / float(n_dates),
            dtype=np.float64,
        )
        seed_sequence = np.random.SeedSequence(entropy)
        generator = np.random.Generator(np.random.PCG64DXSM(seed_sequence))
        counts = generator.multinomial(n=n_dates, pvals=pvals, size=None)
        weights = np.asarray(counts, dtype=np.float64, order="C")
        if weights.shape != (n_dates,) or not weights.flags.c_contiguous:
            raise RuntimeError("configured bootstrap draw violated shape/C-order")
        return weights

    def draw_base_normals(
        self,
        *,
        stream: G2Stream,
        n_dates: int,
        panel_index: int,
        date_index: int,
    ) -> RawBaseNormals:
        """Draw the five independently addressed raw arrays for one test date."""
        TestRngNamespace._validate_authority(self)
        if type(stream) is not G2Stream:
            raise TypeError("base-normal addressing requires the exact G2Stream enum type")

        def draw(component: G2Component) -> NDArray[np.float64]:
            return self.draw_standard_normal(
                self.dgp_address(
                    stream=stream,
                    n_dates=n_dates,
                    panel_index=panel_index,
                    date_index=date_index,
                    component=component,
                )
            )

        phase, scenario = self.contract.phase_scenario(stream)
        provenance = BaseProvenance(
            master_seed=self.master_seed,
            stream=stream,
            phase_id=phase,
            scenario_id=scenario,
            n_dates=n_dates,
            panel_index=panel_index,
            date_index=date_index,
        )
        base = _make_raw_base_normals(
            provenance=provenance,
            factor=draw(G2Component.FACTOR),
            flow_innovation=draw(G2Component.FLOW_INNOVATION),
            return_innovation=draw(G2Component.RETURN_INNOVATION),
            level_noise=draw(G2Component.LEVEL_NOISE),
            proxy_noise=draw(G2Component.PROXY_NOISE),
        )
        key = id(base)
        issuance = _RawBaseIssuance(
            provenance_snapshot=(
                provenance.master_seed,
                provenance.stream,
                provenance.phase_id,
                provenance.scenario_id,
                provenance.n_dates,
                provenance.panel_index,
                provenance.date_index,
            ),
            component_identities=(
                id(base.factor),
                id(base.flow_innovation),
                id(base.return_innovation),
                id(base.level_noise),
                id(base.proxy_noise),
            ),
            content_token=base.provenance_token,
        )

        def discard(reference: weakref.ReferenceType[RawBaseNormals]) -> None:
            current = _RAW_BASE_REGISTRY.get(key)
            if current is not None and current[0] is reference:
                _RAW_BASE_REGISTRY.pop(key, None)

        reference = weakref.ref(base, discard)
        _RAW_BASE_REGISTRY[key] = (reference, issuance)
        return base


def _array_sha256(values: NDArray[np.generic], *, dtype: str) -> str:
    packed = values.astype(dtype, copy=False)
    return _sha256(packed.tobytes(order="C"))


def validate_registered_g2_runtime(contract: G2Contract) -> G2RuntimeFingerprint:
    """Fail closed unless the A006 target runtime reproduces all test KATs.

    This preflight consumes only test seed 1729. Future registered capability
    constructors must call it before they can construct a registered address.
    """
    validate_g2_contract(contract)
    fingerprint = current_g2_runtime_fingerprint()
    if fingerprint != AUTHORIZED_G2_RUNTIME:
        raise RuntimeError(
            f"runtime {fingerprint!r} is not authorized for registered G2 draws; "
            f"expected {AUTHORIZED_G2_RUNTIME!r}"
        )
    namespace = TestRngNamespace.from_contract(contract, _RUNTIME_PREFLIGHT_TEST_SEED)
    for component, expected_hash in _AUTHORIZED_STANDARD_NORMAL_HASHES:
        address = namespace.dgp_address(
            stream=G2Stream.VALIDATION_SIZE,
            n_dates=252,
            panel_index=7,
            date_index=11,
            component=component,
        )
        values = namespace.draw_standard_normal(address)
        if _array_sha256(values, dtype="<f8") != expected_hash:
            raise RuntimeError(
                f"authorized runtime failed the {component.name} Gaussian known answer"
            )
    level_address = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=7,
        date_index=11,
        component=G2Component.LEVEL_NOISE,
    )
    raw = np.random.PCG64DXSM(np.random.SeedSequence(level_address.entropy())).random_raw(150_000)
    if _array_sha256(raw, dtype="<u8") != _AUTHORIZED_LEVEL_NOISE_RAW_HASH:
        raise RuntimeError("authorized runtime failed the level-noise PCG64DXSM known answer")
    return fingerprint


@dataclass(frozen=True, slots=True)
class BaseProvenance:
    """Address prefix shared by all five component arrays in one base date."""

    master_seed: int
    stream: G2Stream
    phase_id: int
    scenario_id: int
    n_dates: int
    panel_index: int
    date_index: int


@dataclass(frozen=True, slots=True)
class _RawBaseIssuance:
    """Module-owned record binding one issued wrapper to its original contents."""

    provenance_snapshot: tuple[int, G2Stream, int, int, int, int, int]
    component_identities: tuple[int, int, int, int, int]
    content_token: str


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RawBaseNormals:
    """Five address-bound, unfiltered, read-only component arrays for one date."""

    provenance: BaseProvenance
    provenance_token: str
    factor: NDArray[np.float64]
    flow_innovation: NDArray[np.float64]
    return_innovation: NDArray[np.float64]
    level_noise: NDArray[np.float64]
    proxy_noise: NDArray[np.float64]


_RAW_BASE_REGISTRY: dict[
    int,
    tuple[weakref.ReferenceType[RawBaseNormals], _RawBaseIssuance],
] = {}


@dataclass(frozen=True, slots=True)
class FilteredBaseNormals:
    """Five read-only component arrays after the one licensed AR filter."""

    provenance: BaseProvenance
    provenance_token: str
    factor: NDArray[np.float64]
    flow_innovation: NDArray[np.float64]
    return_innovation: NDArray[np.float64]
    level_noise: NDArray[np.float64]
    proxy_noise: NDArray[np.float64]


def _base_provenance_token(
    provenance: BaseProvenance,
    *,
    stage: str,
    factor: NDArray[np.float64],
    flow_innovation: NDArray[np.float64],
    return_innovation: NDArray[np.float64],
    level_noise: NDArray[np.float64],
    proxy_noise: NDArray[np.float64],
) -> str:
    header = json.dumps(
        [
            provenance.master_seed,
            provenance.stream.value,
            provenance.phase_id,
            provenance.scenario_id,
            provenance.n_dates,
            provenance.panel_index,
            provenance.date_index,
            stage,
        ],
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    digest = hashlib.sha256(header)
    for name, values in (
        ("factor", factor),
        ("flow_innovation", flow_innovation),
        ("return_innovation", return_innovation),
        ("level_noise", level_noise),
        ("proxy_noise", proxy_noise),
    ):
        digest.update(name.encode("ascii"))
        digest.update(json.dumps(values.shape, separators=(",", ":")).encode("ascii"))
        digest.update(values.dtype.str.encode("ascii"))
        digest.update(values.tobytes(order="C"))
    return digest.hexdigest()


def _readonly(values: NDArray[np.float64]) -> NDArray[np.float64]:
    result = np.ascontiguousarray(values, dtype=np.float64)
    result.setflags(write=False)
    return result


def _make_raw_base_normals(
    *,
    provenance: BaseProvenance,
    factor: NDArray[np.float64],
    flow_innovation: NDArray[np.float64],
    return_innovation: NDArray[np.float64],
    level_noise: NDArray[np.float64],
    proxy_noise: NDArray[np.float64],
) -> RawBaseNormals:
    readonly_factor = _readonly(factor)
    readonly_flow = _readonly(flow_innovation)
    readonly_return = _readonly(return_innovation)
    readonly_level = _readonly(level_noise)
    readonly_proxy = _readonly(proxy_noise)
    token = _base_provenance_token(
        provenance,
        stage="raw",
        factor=readonly_factor,
        flow_innovation=readonly_flow,
        return_innovation=readonly_return,
        level_noise=readonly_level,
        proxy_noise=readonly_proxy,
    )
    return RawBaseNormals(
        provenance=provenance,
        provenance_token=token,
        factor=readonly_factor,
        flow_innovation=readonly_flow,
        return_innovation=readonly_return,
        level_noise=readonly_level,
        proxy_noise=readonly_proxy,
    )


def _make_filtered_base_normals(
    *,
    provenance: BaseProvenance,
    factor: NDArray[np.float64],
    flow_innovation: NDArray[np.float64],
    return_innovation: NDArray[np.float64],
    level_noise: NDArray[np.float64],
    proxy_noise: NDArray[np.float64],
) -> FilteredBaseNormals:
    readonly_factor = _readonly(factor)
    readonly_flow = _readonly(flow_innovation)
    readonly_return = _readonly(return_innovation)
    readonly_level = _readonly(level_noise)
    readonly_proxy = _readonly(proxy_noise)
    return FilteredBaseNormals(
        provenance=provenance,
        provenance_token=_base_provenance_token(
            provenance,
            stage="filtered",
            factor=readonly_factor,
            flow_innovation=readonly_flow,
            return_innovation=readonly_return,
            level_noise=readonly_level,
            proxy_noise=readonly_proxy,
        ),
        factor=readonly_factor,
        flow_innovation=readonly_flow,
        return_innovation=readonly_return,
        level_noise=readonly_level,
        proxy_noise=readonly_proxy,
    )


@dataclass(frozen=True, slots=True)
class G2Cell:
    """One sealed structural cell and its feasible modal parameters."""

    target_index: int
    n_assets: int
    n_levels: int
    bins_per_date: int
    diagonal: float
    offdiagonal: float
    q1: float
    q0: float
    r1: float
    r0: float
    hq: float
    gamma: float
    market_return_shock_variance: float
    orthogonal_return_shock_variance: float
    market_vector: NDArray[np.float64]
    lambda_matrix: NDArray[np.float64]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class G2Date:
    """One transformed date under a sealed cell and deterministic view."""

    response_map: G2ResponseMapIdentity
    filtered: FilteredBaseNormals
    v: NDArray[np.float64]
    q: NDArray[np.float64]
    u: NDArray[np.float64]
    r: NDArray[np.float64]
    z: NDArray[np.float64]
    x: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class G2ResponseMapIdentity:
    """Deterministic response-map coordinates distinct from base provenance."""

    target_index: int
    paper_recovery: bool
    phi: float
    reliability: float


@dataclass(frozen=True, slots=True)
class G2DateReceipt:
    """Validated transformed-date receipt carried into contract-bound models."""

    provenance: BaseProvenance
    base_identity: str
    response_map: G2ResponseMapIdentity
    date_content_sha256: str


def validate_g2_date_receipt_metadata(
    receipt: G2DateReceipt,
    contract: G2Contract,
    *,
    require_canonical_reliability: bool = False,
) -> None:
    """Validate serialized receipt fields without granting DGP issuance authority.

    This pure validator is intentionally weaker than :func:`validate_g2_date`:
    it checks the exact sealed metadata representation but cannot establish that
    a receipt originated from live transformed arrays. Checkpoint loaders may
    use it only inside their separately documented trusted filesystem boundary.
    """
    validate_g2_contract(contract)
    if type(receipt) is not G2DateReceipt:
        raise TypeError("receipt metadata must use the exact G2DateReceipt type")
    if type(require_canonical_reliability) is not bool:
        raise TypeError("canonical-reliability flag must be an exact Python bool")
    provenance = receipt.provenance
    if type(provenance) is not BaseProvenance:
        raise TypeError("receipt provenance must use the exact BaseProvenance type")
    if type(provenance.stream) is not G2Stream:
        raise TypeError("receipt stream must use the exact G2Stream type")
    for name, value in (
        ("master_seed", provenance.master_seed),
        ("phase_id", provenance.phase_id),
        ("scenario_id", provenance.scenario_id),
        ("n_dates", provenance.n_dates),
        ("panel_index", provenance.panel_index),
        ("date_index", provenance.date_index),
    ):
        if type(value) is not int or not 0 <= value < 2**32:
            raise ValueError(f"receipt {name} must be a uint32-range Python integer")
    _validate_stream_coordinates(
        provenance.stream,
        n_dates=provenance.n_dates,
        panel_index=provenance.panel_index,
        date_index=provenance.date_index,
    )
    if (provenance.phase_id, provenance.scenario_id) != contract.phase_scenario(provenance.stream):
        raise ValueError("receipt phase/scenario is not licensed by its stream")
    response_map = receipt.response_map
    if type(response_map) is not G2ResponseMapIdentity:
        raise TypeError("receipt response map must use the exact G2ResponseMapIdentity type")
    if type(response_map.target_index) is not int or not (
        0 <= response_map.target_index < len(contract.population_targets)
    ):
        raise ValueError("receipt target index is outside the sealed target grid")
    if type(response_map.paper_recovery) is not bool:
        raise TypeError("receipt paper_recovery must be an exact Python bool")
    if type(response_map.phi) is not float or not math.isfinite(response_map.phi):
        raise TypeError("receipt phi must be an exact finite Python float")
    expected_phi = (
        contract.iid_ar1
        if provenance.stream is G2Stream.VALIDATION_IID
        else contract.confirmatory_ar1
    )
    if response_map.phi != expected_phi:
        raise ValueError("receipt phi is not licensed by its stream")
    if type(response_map.reliability) is not float or not math.isfinite(response_map.reliability):
        raise TypeError("receipt reliability must be an exact finite Python float")
    if not 0.95 <= response_map.reliability <= 1.0:
        raise ValueError("receipt reliability lies outside the sealed range")
    if (
        require_canonical_reliability
        and response_map.reliability != contract.confirmatory_reliability
    ):
        raise ValueError("smooth checkpoint receipt is not at the canonical reliability")
    recovery_streams = frozenset((G2Stream.RESOURCE_PAPER, G2Stream.VALIDATION_PAPER_RECOVERY))
    if response_map.paper_recovery and (
        response_map.target_index != len(contract.population_targets) - 1
        or provenance.stream not in recovery_streams
    ):
        raise ValueError("receipt paper-recovery map is not licensed")
    if provenance.stream is G2Stream.VALIDATION_PAPER_RECOVERY and not response_map.paper_recovery:
        raise ValueError("paper-recovery stream requires the gamma-zero response map")
    for name, digest in (
        ("base identity", receipt.base_identity),
        ("date content", receipt.date_content_sha256),
    ):
        if (
            type(digest) is not str
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise ValueError(f"receipt {name} must be a lowercase SHA256 digest")


@dataclass(frozen=True, slots=True)
class _G2DateIssuance:
    """Module-owned binding between one transformed wrapper and its contents."""

    provenance_snapshot: tuple[int, G2Stream, int, int, int, int, int]
    component_identities: tuple[int, int, int, int, int, int, int]
    base_identity: str
    response_map: G2ResponseMapIdentity
    date_content_sha256: str


_G2_DATE_REGISTRY: dict[
    int,
    tuple[weakref.ReferenceType[G2Date], _G2DateIssuance],
] = {}


def homogeneous_lambda(
    n_assets: int,
    diagonal: float,
    offdiagonal: float,
) -> NDArray[np.float64]:
    """Construct ``(d-o)I + N o m m'`` in the licensed orientation."""
    if type(n_assets) is not int or n_assets < 2:
        raise ValueError("n_assets must be a Python integer of at least two")
    if not math.isfinite(diagonal) or not math.isfinite(offdiagonal):
        raise ValueError("impact entries must be finite")
    market = np.ones(n_assets, dtype=np.float64) / math.sqrt(float(n_assets))
    matrix = (diagonal - offdiagonal) * np.eye(n_assets, dtype=np.float64)
    matrix += float(n_assets) * offdiagonal * np.outer(market, market)
    return np.ascontiguousarray(matrix, dtype=np.float64)


def build_cell(contract: G2Contract, *, target_index: int) -> G2Cell:
    """Regenerate and verify one target cell before any stochastic transform."""
    validate_g2_contract(contract)
    if type(target_index) is not int or not 0 <= target_index < len(contract.population_targets):
        raise ValueError("target_index is outside the sealed 17-point grid")
    target = contract.population_targets[target_index]
    q1, q0, r1, r0, hq, gamma, market_variance, orthogonal_variance = _cell_scalars(
        contract, target.lambda_offdiag
    )
    if not np.allclose(
        [gamma, market_variance, orthogonal_variance],
        [
            target.gamma,
            target.market_return_shock_variance,
            target.orthogonal_return_shock_variance,
        ],
        rtol=0.0,
        atol=5e-13,
    ):
        raise ValueError("sealed population target does not match the regenerated DGP cell")
    if market_variance <= 0.0 or orthogonal_variance <= 0.0:
        raise ValueError("return-shock modal variances must be strictly positive")
    market = np.ones(contract.n_assets, dtype=np.float64) / math.sqrt(float(contract.n_assets))
    market.setflags(write=False)
    lambda_matrix = homogeneous_lambda(
        contract.n_assets, contract.lambda_diagonal, target.lambda_offdiag
    )
    lambda_matrix.setflags(write=False)
    return G2Cell(
        target_index=target_index,
        n_assets=contract.n_assets,
        n_levels=contract.n_levels,
        bins_per_date=contract.bins_per_date,
        diagonal=contract.lambda_diagonal,
        offdiagonal=target.lambda_offdiag,
        q1=q1,
        q0=q0,
        r1=r1,
        r0=r0,
        hq=hq,
        gamma=gamma,
        market_return_shock_variance=market_variance,
        orthogonal_return_shock_variance=orthogonal_variance,
        market_vector=market,
        lambda_matrix=lambda_matrix,
    )


def _validated_cell(contract: G2Contract, cell: G2Cell) -> G2Cell:
    expected = build_cell(contract, target_index=cell.target_index)
    scalar_fields = (
        "target_index",
        "n_assets",
        "n_levels",
        "bins_per_date",
        "diagonal",
        "offdiagonal",
        "q1",
        "q0",
        "r1",
        "r0",
        "hq",
        "gamma",
        "market_return_shock_variance",
        "orthogonal_return_shock_variance",
    )
    if any(getattr(cell, field) != getattr(expected, field) for field in scalar_fields):
        raise ValueError("G2 cell scalars do not match the sealed target index")
    for name, observed, regenerated in (
        ("market_vector", cell.market_vector, expected.market_vector),
        ("lambda_matrix", cell.lambda_matrix, expected.lambda_matrix),
    ):
        if (
            observed.dtype != np.float64
            or not observed.flags.c_contiguous
            or observed.flags.writeable
            or not np.array_equal(observed, regenerated)
        ):
            raise ValueError(f"G2 cell {name} is not the read-only sealed construction")
    return expected


def filter_ar1_date(raw: NDArray[np.float64], *, phi: float) -> NDArray[np.float64]:
    """Filter one date along axis zero with a stationary first draw and reset."""
    if raw.dtype != np.float64 or raw.ndim < 1 or raw.shape[0] < 1:
        raise ValueError("AR input must be a nonempty float64 array")
    if not np.all(np.isfinite(raw)):
        raise ValueError("AR input must be finite")
    if not math.isfinite(phi) or not 0.0 <= phi < 1.0:
        raise ValueError("AR coefficient must be finite in [0, 1)")
    if phi == 0.0:
        return np.array(raw, dtype=np.float64, copy=True, order="C")
    filtered = np.empty(raw.shape, dtype=np.float64, order="C")
    filtered[0] = raw[0]
    innovation_scale = math.sqrt(1.0 - phi * phi)
    for index in range(1, raw.shape[0]):
        filtered[index] = phi * filtered[index - 1] + innovation_scale * raw[index]
    return filtered


def symmetric_modal_map(
    filtered: NDArray[np.float64],
    *,
    market_variance: float,
    orthogonal_variance: float,
    market_vector: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Apply the symmetric market/orthogonal covariance square root."""
    if filtered.dtype != np.float64 or filtered.ndim != 2:
        raise ValueError("modal input must be a two-dimensional float64 array")
    if not np.all(np.isfinite(filtered)):
        raise ValueError("modal input must be finite")
    if market_vector.dtype != np.float64 or market_vector.shape != (filtered.shape[1],):
        raise ValueError("market vector does not match the modal input")
    if (
        not math.isfinite(market_variance)
        or not math.isfinite(orthogonal_variance)
        or market_variance <= 0.0
        or orthogonal_variance <= 0.0
    ):
        raise ValueError("modal variances must be finite and strictly positive")
    market_norm = float(market_vector @ market_vector)
    if not math.isclose(market_norm, 1.0, rel_tol=0.0, abs_tol=5e-15):
        raise ValueError("market vector must have unit Euclidean norm")
    orthogonal_scale = math.sqrt(orthogonal_variance)
    market_adjustment = math.sqrt(market_variance) - orthogonal_scale
    market_scores = filtered @ market_vector
    mapped = orthogonal_scale * filtered + market_adjustment * np.outer(
        market_scores, market_vector
    )
    return np.ascontiguousarray(mapped, dtype=np.float64)


def _validate_raw_base(
    base: RawBaseNormals,
    cell: G2Cell,
    contract: G2Contract,
) -> None:
    if type(base) is not RawBaseNormals:
        raise TypeError("transform_date requires unfiltered RawBaseNormals")
    if type(base.provenance) is not BaseProvenance:
        raise TypeError("raw base provenance must use the exact BaseProvenance type")
    registry_entry = _RAW_BASE_REGISTRY.get(id(base))
    if registry_entry is None or registry_entry[0]() is not base:
        raise ValueError(
            "raw base provenance issuance was not minted by TestRngNamespace.draw_base_normals"
        )
    issuance = registry_entry[1]
    if issuance.provenance_snapshot != (
        base.provenance.master_seed,
        base.provenance.stream,
        base.provenance.phase_id,
        base.provenance.scenario_id,
        base.provenance.n_dates,
        base.provenance.panel_index,
        base.provenance.date_index,
    ) or issuance.component_identities != (
        id(base.factor),
        id(base.flow_innovation),
        id(base.return_innovation),
        id(base.level_noise),
        id(base.proxy_noise),
    ):
        raise ValueError("raw base provenance/components were not issued for these exact objects")
    expected_pair = contract.phase_scenario(base.provenance.stream)
    _validate_stream_coordinates(
        base.provenance.stream,
        n_dates=base.provenance.n_dates,
        panel_index=base.provenance.panel_index,
        date_index=base.provenance.date_index,
    )
    if (
        (base.provenance.phase_id, base.provenance.scenario_id) != expected_pair
        or type(base.provenance.master_seed) is not int
        or not 0 <= base.provenance.master_seed < 2**32
        or type(base.provenance.phase_id) is not int
        or type(base.provenance.scenario_id) is not int
        or type(base.provenance_token) is not str
    ):
        raise ValueError("base-normal provenance is not a licensed G2 DGP namespace")
    expected = (
        ("factor", base.factor, (cell.bins_per_date,)),
        ("flow_innovation", base.flow_innovation, (cell.bins_per_date, cell.n_assets)),
        ("return_innovation", base.return_innovation, (cell.bins_per_date, cell.n_assets)),
        (
            "level_noise",
            base.level_noise,
            (cell.bins_per_date, cell.n_assets, cell.n_levels),
        ),
        ("proxy_noise", base.proxy_noise, (cell.bins_per_date,)),
    )
    for name, values, shape in expected:
        if (
            values.dtype != np.float64
            or values.shape != shape
            or not values.flags.c_contiguous
            or values.flags.writeable
        ):
            raise ValueError(f"{name} does not have the sealed float64 C-order shape {shape}")
        if not np.all(np.isfinite(values)):
            raise ValueError(f"{name} contains a nonfinite value")
    expected_token = _base_provenance_token(
        base.provenance,
        stage="raw",
        factor=base.factor,
        flow_innovation=base.flow_innovation,
        return_innovation=base.return_innovation,
        level_noise=base.level_noise,
        proxy_noise=base.proxy_noise,
    )
    if base.provenance_token != expected_token:
        raise ValueError("raw base token does not bind the supplied component bytes")
    if issuance.content_token != expected_token:
        raise ValueError("raw base issuance does not bind the supplied component bytes")


def _g2_date_content_token(date: G2Date) -> str:
    provenance = date.filtered.provenance
    header = json.dumps(
        [
            "xid-g2-date-v1",
            provenance.master_seed,
            provenance.stream.value,
            provenance.phase_id,
            provenance.scenario_id,
            provenance.n_dates,
            provenance.panel_index,
            provenance.date_index,
            date.filtered.provenance_token,
            date.response_map.target_index,
            date.response_map.paper_recovery,
            date.response_map.phi.hex(),
            date.response_map.reliability.hex(),
        ],
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    digest = hashlib.sha256(header)
    for name, values in (
        ("v", date.v),
        ("q", date.q),
        ("u", date.u),
        ("r", date.r),
        ("z", date.z),
        ("x", date.x),
    ):
        digest.update(name.encode("ascii"))
        digest.update(json.dumps(values.shape, separators=(",", ":")).encode("ascii"))
        digest.update(values.dtype.str.encode("ascii"))
        digest.update(values.tobytes(order="C"))
    return digest.hexdigest()


def validate_g2_date(date: G2Date, contract: G2Contract) -> G2DateReceipt:
    """Validate that one transformed date was minted by ``transform_date``."""
    validate_g2_contract(contract)
    if type(date) is not G2Date:
        raise TypeError("transformed date must use the exact G2Date type")
    registry_entry = _G2_DATE_REGISTRY.get(id(date))
    if registry_entry is None or registry_entry[0]() is not date:
        raise ValueError("transformed date receipt was not issued by transform_date")
    issuance = registry_entry[1]
    if type(date.filtered) is not FilteredBaseNormals:
        raise TypeError("transformed date must contain exact FilteredBaseNormals")
    if type(date.response_map) is not G2ResponseMapIdentity:
        raise TypeError("transformed date must contain exact response-map identity")
    provenance = date.filtered.provenance
    if type(provenance) is not BaseProvenance:
        raise TypeError("transformed date provenance must use exact BaseProvenance")
    snapshot = (
        provenance.master_seed,
        provenance.stream,
        provenance.phase_id,
        provenance.scenario_id,
        provenance.n_dates,
        provenance.panel_index,
        provenance.date_index,
    )
    identities = (
        id(date.filtered),
        id(date.v),
        id(date.q),
        id(date.u),
        id(date.r),
        id(date.z),
        id(date.x),
    )
    if (
        snapshot != issuance.provenance_snapshot
        or identities != issuance.component_identities
        or date.response_map != issuance.response_map
    ):
        raise ValueError("transformed date receipt no longer binds its provenance or components")
    expected_pair = contract.phase_scenario(provenance.stream)
    _validate_stream_coordinates(
        provenance.stream,
        n_dates=provenance.n_dates,
        panel_index=provenance.panel_index,
        date_index=provenance.date_index,
    )
    if (
        (provenance.phase_id, provenance.scenario_id) != expected_pair
        or type(provenance.master_seed) is not int
        or not 0 <= provenance.master_seed < 2**32
        or type(date.filtered.provenance_token) is not str
    ):
        raise ValueError("transformed date provenance is not licensed by the G2 contract")
    response_map = date.response_map
    expected_phi = (
        contract.iid_ar1
        if provenance.stream is G2Stream.VALIDATION_IID
        else contract.confirmatory_ar1
    )
    recovery_streams = frozenset((G2Stream.RESOURCE_PAPER, G2Stream.VALIDATION_PAPER_RECOVERY))
    if (
        type(response_map.target_index) is not int
        or not 0 <= response_map.target_index < len(contract.population_targets)
        or type(response_map.paper_recovery) is not bool
        or type(response_map.phi) is not float
        or response_map.phi != expected_phi
        or type(response_map.reliability) is not float
        or not 0.95 <= response_map.reliability <= 1.0
        or (
            response_map.paper_recovery
            and (
                response_map.target_index != len(contract.population_targets) - 1
                or provenance.stream not in recovery_streams
            )
        )
        or (
            provenance.stream is G2Stream.VALIDATION_PAPER_RECOVERY
            and not response_map.paper_recovery
        )
    ):
        raise ValueError("transformed date response-map identity is not licensed")
    filtered_expected = (
        ("factor", date.filtered.factor, (contract.bins_per_date,)),
        (
            "flow_innovation",
            date.filtered.flow_innovation,
            (contract.bins_per_date, contract.n_assets),
        ),
        (
            "return_innovation",
            date.filtered.return_innovation,
            (contract.bins_per_date, contract.n_assets),
        ),
        (
            "level_noise",
            date.filtered.level_noise,
            (contract.bins_per_date, contract.n_assets, contract.n_levels),
        ),
        ("proxy_noise", date.filtered.proxy_noise, (contract.bins_per_date,)),
    )
    output_expected = (
        ("v", date.v, (contract.bins_per_date, contract.n_assets)),
        ("q", date.q, (contract.bins_per_date, contract.n_assets)),
        ("u", date.u, (contract.bins_per_date, contract.n_assets)),
        ("r", date.r, (contract.bins_per_date, contract.n_assets)),
        ("z", date.z, (contract.bins_per_date,)),
        (
            "x",
            date.x,
            (contract.bins_per_date, contract.n_assets, contract.n_levels),
        ),
    )
    for name, values, shape in (*filtered_expected, *output_expected):
        if (
            type(values) is not np.ndarray
            or values.dtype != np.dtype(np.float64)
            or values.shape != shape
            or not values.flags.c_contiguous
            or values.flags.writeable
            or not np.all(np.isfinite(values))
        ):
            raise ValueError(f"transformed date {name} violates its sealed array contract")
    expected_base_identity = _base_provenance_token(
        provenance,
        stage="filtered",
        factor=date.filtered.factor,
        flow_innovation=date.filtered.flow_innovation,
        return_innovation=date.filtered.return_innovation,
        level_noise=date.filtered.level_noise,
        proxy_noise=date.filtered.proxy_noise,
    )
    if (
        date.filtered.provenance_token != expected_base_identity
        or issuance.base_identity != expected_base_identity
    ):
        raise ValueError("transformed date filtered-base identity is invalid")
    content_token = _g2_date_content_token(date)
    if content_token != issuance.date_content_sha256:
        raise ValueError("transformed date content no longer matches its issued receipt")
    receipt = G2DateReceipt(
        provenance=provenance,
        base_identity=expected_base_identity,
        response_map=date.response_map,
        date_content_sha256=content_token,
    )
    validate_g2_date_receipt_metadata(receipt, contract)
    return receipt


def transform_date(
    base: RawBaseNormals,
    cell: G2Cell,
    *,
    contract: G2Contract,
    phi: float,
    reliability: float,
    paper_recovery: bool = False,
) -> G2Date:
    """Filter first, then apply only the frozen deterministic G2 maps."""
    sealed_cell = _validated_cell(contract, cell)
    _validate_raw_base(base, sealed_cell, contract)
    if not math.isfinite(reliability) or not 0.95 <= reliability <= 1.0:
        raise ValueError("proxy reliability must lie in the sealed [0.95, 1] range")
    expected_phi = (
        contract.iid_ar1
        if base.provenance.stream is G2Stream.VALIDATION_IID
        else contract.confirmatory_ar1
    )
    if phi != expected_phi:
        raise ValueError(
            f"phi={phi} is not licensed for {base.provenance.stream.value}; expected {expected_phi}"
        )
    if paper_recovery and sealed_cell.target_index != 16:
        raise ValueError("paper recovery is licensed only at the upper structural endpoint")
    recovery_streams = frozenset((G2Stream.RESOURCE_PAPER, G2Stream.VALIDATION_PAPER_RECOVERY))
    if paper_recovery and base.provenance.stream not in recovery_streams:
        raise ValueError("paper recovery requires the disjoint paper-recovery RNG namespace")
    if base.provenance.stream is G2Stream.VALIDATION_PAPER_RECOVERY and not paper_recovery:
        raise ValueError("phase-25/scenario-4 base normals require the gamma-zero recovery map")
    filtered = _make_filtered_base_normals(
        provenance=base.provenance,
        factor=filter_ar1_date(base.factor, phi=phi),
        flow_innovation=filter_ar1_date(base.flow_innovation, phi=phi),
        return_innovation=filter_ar1_date(base.return_innovation, phi=phi),
        level_noise=filter_ar1_date(base.level_noise, phi=phi),
        proxy_noise=filter_ar1_date(base.proxy_noise, phi=phi),
    )
    market = sealed_cell.market_vector
    v = np.sqrt(sealed_cell.q0) * filtered.flow_innovation
    q = sealed_cell.hq * filtered.factor[:, None] * market[None, :] + v
    u = symmetric_modal_map(
        filtered.return_innovation,
        market_variance=sealed_cell.market_return_shock_variance,
        orthogonal_variance=sealed_cell.orthogonal_return_shock_variance,
        market_vector=market,
    )
    gamma = 0.0 if paper_recovery else sealed_cell.gamma
    r = q @ sealed_cell.lambda_matrix.T + gamma * filtered.factor[:, None] * market[None, :] + u
    z = filtered.factor + math.sqrt(1.0 / reliability - 1.0) * filtered.proxy_noise
    x = q[:, :, None] + math.sqrt(547.0 / 3953.0) * filtered.level_noise
    outputs = tuple(_readonly(value) for value in (v, q, u, r, z, x))
    if any(not np.all(np.isfinite(value)) for value in outputs):
        raise ValueError("a transformed G2 date contains a nonfinite value")
    response_map = G2ResponseMapIdentity(
        target_index=sealed_cell.target_index,
        paper_recovery=paper_recovery,
        phi=float(phi),
        reliability=float(reliability),
    )
    date = G2Date(
        response_map=response_map,
        filtered=filtered,
        v=outputs[0],
        q=outputs[1],
        u=outputs[2],
        r=outputs[3],
        z=outputs[4],
        x=outputs[5],
    )
    key = id(date)
    content_token = _g2_date_content_token(date)
    issuance = _G2DateIssuance(
        provenance_snapshot=(
            base.provenance.master_seed,
            base.provenance.stream,
            base.provenance.phase_id,
            base.provenance.scenario_id,
            base.provenance.n_dates,
            base.provenance.panel_index,
            base.provenance.date_index,
        ),
        component_identities=(
            id(date.filtered),
            id(date.v),
            id(date.q),
            id(date.u),
            id(date.r),
            id(date.z),
            id(date.x),
        ),
        base_identity=filtered.provenance_token,
        response_map=response_map,
        date_content_sha256=content_token,
    )

    def discard(reference: weakref.ReferenceType[G2Date]) -> None:
        current = _G2_DATE_REGISTRY.get(key)
        if current is not None and current[0] is reference:
            _G2_DATE_REGISTRY.pop(key, None)

    reference = weakref.ref(date, discard)
    _G2_DATE_REGISTRY[key] = (reference, issuance)
    return date
