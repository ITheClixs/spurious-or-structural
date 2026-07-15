"""Sealed G2 contract, test-only RNG namespace, and pure DGP transforms.

This module deliberately exposes no production authority.  The three registered
G2 seeds cannot pass :class:`TestRngNamespace`; resource, validation, and
research entry points are added only after their capability chain is tested.
"""

from __future__ import annotations

import hashlib
import json
import math
import tomllib
import weakref
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import ClassVar, cast

import numpy as np
from numpy.typing import NDArray


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
class PopulationTarget:
    """Target fields needed to regenerate the structural DGP cell."""

    lambda_offdiag: float
    gamma: float
    market_return_shock_variance: float
    orthogonal_return_shock_variance: float


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
    registered_seeds: tuple[int, int, int]
    phase_scenarios: tuple[tuple[G2Stream, int, int], ...]
    component_ids: tuple[tuple[G2Component, int], ...]
    draw_shapes: tuple[tuple[G2Component, tuple[int, ...]], ...]
    lasso_ratio_grid: tuple[float, ...]
    population_targets: tuple[PopulationTarget, ...]

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

    paper = _table(
        _table(config, "opponent", table_name="config"),
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
    streams = _table(config, "streams", table_name="config")
    assignments = _table(streams, "phase_scenario_assignments", table_name="config.streams")
    component_ids_table = _table(streams, "component_ids", table_name="config.streams")
    draw_shapes_table = _table(streams, "draw_shapes", table_name="config.streams")
    calibration = _table(config, "calibration", table_name="config")
    observable = _table(calibration, "observable", table_name="config.calibration")
    impact = _table(calibration, "impact_sensitivity", table_name="config.calibration")
    proxy = _table(calibration, "proxy", table_name="config.calibration")
    measurement = _table(calibration, "measurement", table_name="config.calibration")

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
    )
    if tuple(value.hex() for value in scalar_identity) != tuple(
        value.hex() for value in expected_scalar_identity
    ):
        raise ValueError("sealed G2 contract calibration scalars changed")
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


@dataclass(frozen=True, slots=True)
class G2Date:
    """One transformed date under a sealed cell and deterministic view."""

    filtered: FilteredBaseNormals
    v: NDArray[np.float64]
    q: NDArray[np.float64]
    u: NDArray[np.float64]
    r: NDArray[np.float64]
    z: NDArray[np.float64]
    x: NDArray[np.float64]


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
    outputs = tuple(np.ascontiguousarray(value, dtype=np.float64) for value in (v, q, u, r, z, x))
    if any(not np.all(np.isfinite(value)) for value in outputs):
        raise ValueError("a transformed G2 date contains a nonfinite value")
    return G2Date(
        filtered=filtered,
        v=outputs[0],
        q=outputs[1],
        u=outputs[2],
        r=outputs[3],
        z=outputs[4],
        x=outputs[5],
    )
