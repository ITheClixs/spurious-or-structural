"""Deterministic smooth-estimator kernels for the sealed S0004 G2 design.

The module contains no RNG constructor and no registered execution authority.
It maps already transformed dates to streaming moments and solves the three
smooth opponents under the numerical path frozen by preregistration amendment
A007.
"""

from __future__ import annotations

import hashlib
import json
import math
import weakref
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from itertools import pairwise
from typing import cast

import numpy as np
from numpy.typing import NDArray

from xid.sim.g2 import (
    BaseProvenance,
    G2Contract,
    G2Date,
    G2DateReceipt,
    G2ResponseMapIdentity,
    G2Stream,
    validate_g2_contract,
    validate_g2_date,
)


class G2FlowView(StrEnum):
    """The two flow blocks available to the smooth ridge solver."""

    ORACLE = "oracle_q"
    OBSERVABLE = "integrated_ofi"


@dataclass(frozen=True, slots=True)
class IntegratedOfiPca:
    """Within-date PCA scores and the diagnostics that license them."""

    scores: NDArray[np.float64]
    loadings: NDArray[np.float64]
    covariance_traces: NDArray[np.float64]
    leading_eigenvalues: NDArray[np.float64]
    eigengaps: NDArray[np.float64]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class SmoothBaseDateMoments:
    """Shared raw polynomial Gram for one date."""

    date_index: int
    n_rows: int
    n_assets: int
    n_levels: int
    x0_width: int
    source_receipt: G2DateReceipt | None
    design_sha256: str
    x0tx0_upper: NDArray[np.float64]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class SmoothDateDesign:
    """Ephemeral date design plus its checkpoint-sized shared moments."""

    date_index: int
    n_rows: int
    n_assets: int
    n_levels: int
    source_receipt: G2DateReceipt | None
    design_sha256: str
    x0: NDArray[np.float64]
    pca: IntegratedOfiPca
    base_moments: SmoothBaseDateMoments


@dataclass(frozen=True, slots=True, weakref_slot=True)
class SmoothCellDateMoments:
    """Cell-specific response moments for one date."""

    date_index: int
    n_rows: int
    n_assets: int
    x0_width: int
    design_receipt: G2DateReceipt | None
    response_receipt: G2DateReceipt | None
    design_sha256: str
    x0ty: NDArray[np.float64]
    yty_upper: NDArray[np.float64]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class SmoothBasePanelMoments:
    """Date-major shared moments ready for one-call weighted aggregation."""

    date_indices: tuple[int, ...]
    n_rows: int
    n_assets: int
    n_levels: int
    x0_width: int
    source_receipts: tuple[G2DateReceipt | None, ...]
    design_sha256s: tuple[str, ...]
    x0tx0_upper: NDArray[np.float64]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class SmoothCellPanelMoments:
    """Date-major cell moments ready for one-call weighted aggregation."""

    date_indices: tuple[int, ...]
    n_rows: int
    n_assets: int
    x0_width: int
    design_receipts: tuple[G2DateReceipt | None, ...]
    response_receipts: tuple[G2DateReceipt | None, ...]
    design_sha256s: tuple[str, ...]
    x0ty: NDArray[np.float64]
    yty_upper: NDArray[np.float64]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class SmoothAggregateMoments:
    """One globally weighted raw-moment aggregate."""

    row_mass: float
    n_rows: int
    n_assets: int
    n_levels: int
    x0_width: int
    source_receipts: tuple[G2DateReceipt | None, ...]
    response_receipts: tuple[G2DateReceipt | None, ...]
    design_sha256s: tuple[str, ...]
    x0tx0: NDArray[np.float64]
    x0ty: NDArray[np.float64]
    yty: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class ConditionRidgeResult:
    """Coefficient matrix and all gate-binding ridge diagnostics."""

    coefficients: NDArray[np.float64]
    smallest_eigenvalue: float
    largest_eigenvalue: float
    penalty_condition: float
    penalty_floor: float
    penalty: float
    post_condition_number: float


@dataclass(frozen=True, slots=True)
class HomogeneousResult:
    """Pooled homogeneous slope vector and numerical diagnostics."""

    intercept: float
    slopes: NDArray[np.float64]
    singular_values: NDArray[np.float64]
    condition_number: float

    @property
    def offdiagonal(self) -> float:
        """Return the cross-sum slope, equal to each homogeneous off-diagonal."""
        return float(self.slopes[1])


@dataclass(frozen=True, slots=True)
class ConditionRidgeMoments:
    """Pure centered and proxy-partialled moments for a ridge solve."""

    flow_covariance: NDArray[np.float64]
    response_flow_covariance: NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class HomogeneousMoments:
    """Pure centered pooled moments before the three-slope solve."""

    slope_covariance: NDArray[np.float64]
    slope_response_covariance: NDArray[np.float64]
    predictor_means: NDArray[np.float64]
    response_mean: float


_IssuedRegistry = dict[int, tuple[weakref.ReferenceType[object], str]]
_CONTRACT_DESIGN_REGISTRY: _IssuedRegistry = {}
_CONTRACT_BASE_DATE_REGISTRY: _IssuedRegistry = {}
_CONTRACT_CELL_DATE_REGISTRY: _IssuedRegistry = {}
_CONTRACT_BASE_PANEL_REGISTRY: _IssuedRegistry = {}
_CONTRACT_CELL_PANEL_REGISTRY: _IssuedRegistry = {}
_CONTRACT_AGGREGATE_REGISTRY: _IssuedRegistry = {}
_ANALYTIC_DESIGN_SOURCE_IDENTITY = "xid-g2-smooth-analytic-v1"


def _validate_response_map_identity(
    response: G2ResponseMapIdentity,
    *,
    name: str,
) -> None:
    if type(response) is not G2ResponseMapIdentity:
        raise TypeError(f"{name} must use exact G2ResponseMapIdentity")
    if type(response.target_index) is not int:
        raise TypeError(f"{name} target_index must be an exact Python int")
    if type(response.paper_recovery) is not bool:
        raise TypeError(f"{name} paper_recovery must be an exact Python bool")
    if type(response.phi) is not float or not math.isfinite(response.phi):
        raise TypeError(f"{name} phi must be an exact finite Python float")
    if type(response.reliability) is not float or not math.isfinite(response.reliability):
        raise TypeError(f"{name} reliability must be an exact finite Python float")


def _validate_provenance(provenance: BaseProvenance, *, name: str) -> None:
    if type(provenance) is not BaseProvenance:
        raise TypeError(f"{name} must use exact BaseProvenance")
    if type(provenance.stream) is not G2Stream:
        raise TypeError(f"{name} stream must use exact G2Stream")
    for field_name, value in (
        ("master_seed", provenance.master_seed),
        ("phase_id", provenance.phase_id),
        ("scenario_id", provenance.scenario_id),
        ("n_dates", provenance.n_dates),
        ("panel_index", provenance.panel_index),
        ("date_index", provenance.date_index),
    ):
        if type(value) is not int:
            raise TypeError(f"{name} {field_name} must be an exact Python int")


def _receipt_payload(receipt: G2DateReceipt | None) -> object:
    if receipt is None:
        return None
    if type(receipt) is not G2DateReceipt:
        raise TypeError("issued receipt must use exact G2DateReceipt")
    provenance = receipt.provenance
    response = receipt.response_map
    _validate_provenance(provenance, name="issued receipt provenance")
    _validate_response_map_identity(response, name="issued receipt response map")
    if type(receipt.base_identity) is not str:
        raise TypeError("issued receipt base_identity must be an exact Python str")
    if type(receipt.date_content_sha256) is not str:
        raise TypeError("issued receipt content digest must be an exact Python str")
    return [
        provenance.master_seed,
        provenance.stream.value,
        provenance.phase_id,
        provenance.scenario_id,
        provenance.n_dates,
        provenance.panel_index,
        provenance.date_index,
        receipt.base_identity,
        response.target_index,
        response.paper_recovery,
        response.phi.hex(),
        response.reliability.hex(),
        receipt.date_content_sha256,
    ]


def _payload_sha256(
    label: str,
    metadata: object,
    arrays: Sequence[tuple[str, NDArray[np.float64]]],
    *,
    bind_array_contract: bool = False,
) -> str:
    digest = hashlib.sha256(
        json.dumps(
            [label, metadata],
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    )
    for name, values in arrays:
        if bind_array_contract and (
            type(values) is not np.ndarray
            or values.dtype != np.dtype(np.float64)
            or not values.flags.c_contiguous
            or values.flags.writeable
            or not np.all(np.isfinite(values))
        ):
            raise ValueError(
                f"issued array {name} must be exact finite read-only C-contiguous float64"
            )
        digest.update(name.encode("ascii"))
        digest.update(json.dumps(values.shape, separators=(",", ":")).encode("ascii"))
        digest.update(values.dtype.str.encode("ascii"))
        if bind_array_contract:
            digest.update(b"C1" if values.flags.c_contiguous else b"C0")
            digest.update(b"W1" if values.flags.writeable else b"W0")
        digest.update(values.tobytes(order="C"))
    return digest.hexdigest()


def _validate_issued(
    obj: object,
    registry: _IssuedRegistry,
    token: str,
    *,
    name: str,
) -> None:
    entry = registry.get(id(obj))
    if entry is None or entry[0]() is not obj or entry[1] != token:
        raise ValueError(f"{name} was not issued by the contract-bound builder")


def _design_sha256(
    *,
    date_index: int,
    n_rows: int,
    n_assets: int,
    n_levels: int,
    source_identity: str,
    x0: NDArray[np.float64],
) -> str:
    if type(source_identity) is not str:
        raise TypeError("design source identity must be an exact Python str")
    return _payload_sha256(
        "xid-g2-smooth-design-v1",
        [
            date_index,
            n_rows,
            n_assets,
            n_levels,
            source_identity,
        ],
        (("x0", x0),),
    )


def _base_date_token(moment: SmoothBaseDateMoments) -> str:
    if type(moment) is not SmoothBaseDateMoments:
        raise TypeError("base date token requires exact SmoothBaseDateMoments")
    for name, value in (
        ("date_index", moment.date_index),
        ("n_rows", moment.n_rows),
        ("n_assets", moment.n_assets),
        ("n_levels", moment.n_levels),
        ("x0_width", moment.x0_width),
    ):
        if type(value) is not int:
            raise TypeError(f"base date {name} must be an exact Python int")
    if type(moment.design_sha256) is not str:
        raise TypeError("base date design digest must be an exact Python str")
    return _payload_sha256(
        "xid-g2-smooth-base-date-v1",
        [
            moment.date_index,
            moment.n_rows,
            moment.n_assets,
            moment.n_levels,
            moment.x0_width,
            _receipt_payload(moment.source_receipt),
            moment.design_sha256,
        ],
        (("x0tx0_upper", moment.x0tx0_upper),),
        bind_array_contract=True,
    )


def _design_token(design: SmoothDateDesign) -> str:
    if type(design) is not SmoothDateDesign:
        raise TypeError("design token requires exact SmoothDateDesign")
    for name, value in (
        ("date_index", design.date_index),
        ("n_rows", design.n_rows),
        ("n_assets", design.n_assets),
        ("n_levels", design.n_levels),
    ):
        if type(value) is not int:
            raise TypeError(f"design {name} must be an exact Python int")
    if type(design.design_sha256) is not str:
        raise TypeError("design digest must be an exact Python str")
    if type(design.pca) is not IntegratedOfiPca:
        raise TypeError("design PCA diagnostics must use exact IntegratedOfiPca")
    if type(design.base_moments) is not SmoothBaseDateMoments:
        raise TypeError("design base moments must use exact SmoothBaseDateMoments")
    return _payload_sha256(
        "xid-g2-smooth-design-issuance-v1",
        [
            design.date_index,
            design.n_rows,
            design.n_assets,
            design.n_levels,
            _receipt_payload(design.source_receipt),
            design.design_sha256,
            _base_date_token(design.base_moments),
        ],
        (
            ("x0", design.x0),
            ("pca_scores", design.pca.scores),
            ("pca_loadings", design.pca.loadings),
            ("pca_covariance_traces", design.pca.covariance_traces),
            ("pca_leading_eigenvalues", design.pca.leading_eigenvalues),
            ("pca_eigengaps", design.pca.eigengaps),
        ),
        bind_array_contract=True,
    )


def _cell_date_token(moment: SmoothCellDateMoments) -> str:
    if type(moment) is not SmoothCellDateMoments:
        raise TypeError("cell date token requires exact SmoothCellDateMoments")
    for name, value in (
        ("date_index", moment.date_index),
        ("n_rows", moment.n_rows),
        ("n_assets", moment.n_assets),
        ("x0_width", moment.x0_width),
    ):
        if type(value) is not int:
            raise TypeError(f"cell date {name} must be an exact Python int")
    if type(moment.design_sha256) is not str:
        raise TypeError("cell date design digest must be an exact Python str")
    return _payload_sha256(
        "xid-g2-smooth-cell-date-v1",
        [
            moment.date_index,
            moment.n_rows,
            moment.n_assets,
            moment.x0_width,
            _receipt_payload(moment.design_receipt),
            _receipt_payload(moment.response_receipt),
            moment.design_sha256,
        ],
        (("x0ty", moment.x0ty), ("yty_upper", moment.yty_upper)),
        bind_array_contract=True,
    )


def _base_panel_token(panel: SmoothBasePanelMoments) -> str:
    if type(panel) is not SmoothBasePanelMoments:
        raise TypeError("base panel token requires exact SmoothBasePanelMoments")
    for name, value in (
        ("n_rows", panel.n_rows),
        ("n_assets", panel.n_assets),
        ("n_levels", panel.n_levels),
        ("x0_width", panel.x0_width),
    ):
        if type(value) is not int:
            raise TypeError(f"base panel {name} must be an exact Python int")
    if type(panel.date_indices) is not tuple or any(
        type(value) is not int for value in panel.date_indices
    ):
        raise TypeError("base panel date_indices must be an exact tuple of Python ints")
    if type(panel.source_receipts) is not tuple:
        raise TypeError("base panel source_receipts must be an exact tuple")
    if type(panel.design_sha256s) is not tuple or any(
        type(value) is not str for value in panel.design_sha256s
    ):
        raise TypeError("base panel design digests must be an exact tuple of strings")
    return _payload_sha256(
        "xid-g2-smooth-base-panel-v1",
        [
            panel.date_indices,
            panel.n_rows,
            panel.n_assets,
            panel.n_levels,
            panel.x0_width,
            [_receipt_payload(item) for item in panel.source_receipts],
            panel.design_sha256s,
        ],
        (("x0tx0_upper", panel.x0tx0_upper),),
        bind_array_contract=True,
    )


def _cell_panel_token(panel: SmoothCellPanelMoments) -> str:
    if type(panel) is not SmoothCellPanelMoments:
        raise TypeError("cell panel token requires exact SmoothCellPanelMoments")
    for name, value in (
        ("n_rows", panel.n_rows),
        ("n_assets", panel.n_assets),
        ("x0_width", panel.x0_width),
    ):
        if type(value) is not int:
            raise TypeError(f"cell panel {name} must be an exact Python int")
    if type(panel.date_indices) is not tuple or any(
        type(value) is not int for value in panel.date_indices
    ):
        raise TypeError("cell panel date_indices must be an exact tuple of Python ints")
    if type(panel.design_receipts) is not tuple or type(panel.response_receipts) is not tuple:
        raise TypeError("cell panel receipt collections must be exact tuples")
    if type(panel.design_sha256s) is not tuple or any(
        type(value) is not str for value in panel.design_sha256s
    ):
        raise TypeError("cell panel design digests must be an exact tuple of strings")
    return _payload_sha256(
        "xid-g2-smooth-cell-panel-v1",
        [
            panel.date_indices,
            panel.n_rows,
            panel.n_assets,
            panel.x0_width,
            [_receipt_payload(item) for item in panel.design_receipts],
            [_receipt_payload(item) for item in panel.response_receipts],
            panel.design_sha256s,
        ],
        (("x0ty", panel.x0ty), ("yty_upper", panel.yty_upper)),
        bind_array_contract=True,
    )


def _aggregate_token(aggregate: SmoothAggregateMoments) -> str:
    if type(aggregate) is not SmoothAggregateMoments:
        raise TypeError("aggregate token requires exact SmoothAggregateMoments")
    if type(aggregate.row_mass) is not float or not math.isfinite(aggregate.row_mass):
        raise TypeError("aggregate row_mass must be an exact finite Python float")
    for name, value in (
        ("n_rows", aggregate.n_rows),
        ("n_assets", aggregate.n_assets),
        ("n_levels", aggregate.n_levels),
        ("x0_width", aggregate.x0_width),
    ):
        if type(value) is not int:
            raise TypeError(f"aggregate {name} must be an exact Python int")
    if (
        type(aggregate.source_receipts) is not tuple
        or type(aggregate.response_receipts) is not tuple
    ):
        raise TypeError("aggregate receipt collections must be exact tuples")
    if type(aggregate.design_sha256s) is not tuple or any(
        type(value) is not str for value in aggregate.design_sha256s
    ):
        raise TypeError("aggregate design digests must be an exact tuple of strings")
    return _payload_sha256(
        "xid-g2-smooth-aggregate-v1",
        [
            aggregate.row_mass.hex(),
            aggregate.n_rows,
            aggregate.n_assets,
            aggregate.n_levels,
            aggregate.x0_width,
            [_receipt_payload(item) for item in aggregate.source_receipts],
            [_receipt_payload(item) for item in aggregate.response_receipts],
            aggregate.design_sha256s,
        ],
        (
            ("x0tx0", aggregate.x0tx0),
            ("x0ty", aggregate.x0ty),
            ("yty", aggregate.yty),
        ),
        bind_array_contract=True,
    )


def _readonly_float64(values: NDArray[np.float64]) -> NDArray[np.float64]:
    result = np.array(values, dtype=np.float64, order="C", copy=True)
    result.setflags(write=False)
    return result


def _finite_float64_array(
    values: NDArray[np.float64],
    *,
    name: str,
    ndim: int,
) -> NDArray[np.float64]:
    if type(values) is not np.ndarray or values.dtype != np.dtype(np.float64):
        raise TypeError(f"{name} must be an exact float64 ndarray")
    if values.ndim != ndim:
        raise ValueError(f"{name} must have {ndim} dimensions")
    if not np.all(np.isfinite(values)):
        raise ValueError(f"{name} contains a nonfinite value")
    return values


def pack_symmetric_upper(matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    """Pack a finite symmetric matrix using row-major ``numpy.triu_indices``."""
    checked = _finite_float64_array(matrix, name="matrix", ndim=2)
    if checked.shape[0] != checked.shape[1]:
        raise ValueError("matrix must be square and symmetric")
    if not np.array_equal(checked, checked.T):
        raise ValueError("matrix must be exactly symmetric before packing")
    indices = np.triu_indices(checked.shape[0])
    return _readonly_float64(checked[indices])


def unpack_symmetric_upper(
    packed: NDArray[np.float64],
    *,
    size: int,
) -> NDArray[np.float64]:
    """Unpack the exact row-major upper-triangle representation."""
    checked = _finite_float64_array(packed, name="packed", ndim=1)
    if type(size) is not int or size < 1:
        raise ValueError("packed matrix size must be a positive Python integer")
    expected = size * (size + 1) // 2
    if checked.shape != (expected,):
        raise ValueError(f"packed vector must contain exactly {expected} values")
    result = np.empty((size, size), dtype=np.float64)
    rows, columns = np.triu_indices(size)
    result[rows, columns] = checked
    result[columns, rows] = checked
    return _readonly_float64(result)


def integrate_ofi_pc1(
    level_flows: NDArray[np.float64],
    *,
    eigengap_ratio: float,
) -> IntegratedOfiPca:
    """Compute the frozen within-date, within-asset integrated-OFI score."""
    levels = _finite_float64_array(level_flows, name="level_flows", ndim=3)
    if not math.isfinite(eigengap_ratio) or eigengap_ratio <= 0.0:
        raise ValueError("eigengap_ratio must be finite and positive")
    n_rows, n_assets, n_levels = levels.shape
    if n_rows < 2 or n_assets < 1 or n_levels < 2:
        raise ValueError("level_flows need at least two rows, one asset, and two levels")

    scores = np.empty((n_rows, n_assets), dtype=np.float64)
    loadings = np.empty((n_assets, n_levels), dtype=np.float64)
    traces = np.empty(n_assets, dtype=np.float64)
    leading = np.empty(n_assets, dtype=np.float64)
    gaps = np.empty(n_assets, dtype=np.float64)
    divisor = float(n_rows)

    for asset in range(n_assets):
        asset_levels = levels[:, asset, :]
        means = np.mean(asset_levels, axis=0, dtype=np.float64)
        centered = asset_levels - means
        covariance = (centered.T @ centered) / divisor
        trace = float(np.trace(covariance))
        if not math.isfinite(trace) or trace <= 0.0:
            raise ValueError(f"asset {asset} PCA covariance trace is nonfinite or nonpositive")
        try:
            eigenvalues, eigenvectors = np.linalg.eigh(covariance)
        except np.linalg.LinAlgError as error:
            raise ValueError(f"asset {asset} PCA eigendecomposition failed") from error
        top_two = eigenvalues[-2:]
        loading = eigenvectors[:, -1]
        if not np.all(np.isfinite(top_two)) or not np.all(np.isfinite(loading)):
            raise ValueError(f"asset {asset} PCA leading eigenpair is nonfinite")
        gap = float(top_two[1] - top_two[0])
        if not math.isfinite(gap) or gap <= eigengap_ratio * trace:
            raise ValueError(f"asset {asset} PCA eigengap is too weak")
        sign_index = int(np.argmax(np.abs(loading)))
        if loading[sign_index] < 0.0:
            loading = -loading
        l1_norm = float(np.sum(np.abs(loading), dtype=np.float64))
        if not math.isfinite(l1_norm) or l1_norm <= 0.0:
            raise ValueError(f"asset {asset} PCA loading L1 norm is invalid")
        score = (centered @ loading) / l1_norm
        if not np.all(np.isfinite(score)):
            raise ValueError(f"asset {asset} PCA score is nonfinite")
        scores[:, asset] = score
        loadings[asset] = loading
        traces[asset] = trace
        leading[asset] = float(top_two[1])
        gaps[asset] = gap

    return IntegratedOfiPca(
        scores=_readonly_float64(scores),
        loadings=_readonly_float64(loadings),
        covariance_traces=_readonly_float64(traces),
        leading_eigenvalues=_readonly_float64(leading),
        eigengaps=_readonly_float64(gaps),
    )


def build_smooth_date_design(
    *,
    date_index: int,
    factor: NDArray[np.float64],
    proxy_noise: NDArray[np.float64],
    oracle_flow: NDArray[np.float64],
    level_flows: NDArray[np.float64],
    eigengap_ratio: float,
) -> SmoothDateDesign:
    """Build an analytic-only date design with no contract authority."""
    return _build_smooth_date_design(
        date_index=date_index,
        factor=factor,
        proxy_noise=proxy_noise,
        oracle_flow=oracle_flow,
        level_flows=level_flows,
        eigengap_ratio=eigengap_ratio,
        source_receipt=None,
    )


def _build_smooth_date_design(
    *,
    date_index: int,
    factor: NDArray[np.float64],
    proxy_noise: NDArray[np.float64],
    oracle_flow: NDArray[np.float64],
    level_flows: NDArray[np.float64],
    eigengap_ratio: float,
    source_receipt: G2DateReceipt | None,
) -> SmoothDateDesign:
    """Build one raw polynomial design and its shared packed Gram."""
    if type(date_index) is not int or date_index < 0:
        raise ValueError("date_index must be a nonnegative Python integer")
    checked_factor = _finite_float64_array(factor, name="factor", ndim=1)
    checked_proxy = _finite_float64_array(proxy_noise, name="proxy_noise", ndim=1)
    checked_flow = _finite_float64_array(oracle_flow, name="oracle_flow", ndim=2)
    checked_levels = _finite_float64_array(level_flows, name="level_flows", ndim=3)
    n_rows, n_assets = checked_flow.shape
    if checked_factor.shape != (n_rows,) or checked_proxy.shape != (n_rows,):
        raise ValueError("factor, proxy_noise, and oracle_flow row counts must match")
    if checked_levels.shape[:2] != (n_rows, n_assets):
        raise ValueError("level_flows rows/assets must match oracle_flow")
    pca = integrate_ofi_pc1(checked_levels, eigengap_ratio=eigengap_ratio)
    x0 = np.column_stack(
        (
            np.ones(n_rows, dtype=np.float64),
            checked_factor,
            checked_proxy,
            checked_flow,
            pca.scores,
        )
    )
    x0 = np.ascontiguousarray(x0, dtype=np.float64)
    gram = x0.T @ x0
    if not np.all(np.isfinite(gram)):
        raise ValueError("shared date Gram contains a nonfinite value")
    if source_receipt is None:
        source_identity = _ANALYTIC_DESIGN_SOURCE_IDENTITY
    else:
        if type(source_receipt) is not G2DateReceipt:
            raise TypeError("design source receipt must use exact G2DateReceipt")
        if type(source_receipt.base_identity) is not str:
            raise TypeError("design source base identity must be an exact Python str")
        source_identity = source_receipt.base_identity
    design_sha256 = _design_sha256(
        date_index=date_index,
        n_rows=n_rows,
        n_assets=n_assets,
        n_levels=checked_levels.shape[2],
        source_identity=source_identity,
        x0=x0,
    )
    base = SmoothBaseDateMoments(
        date_index=date_index,
        n_rows=n_rows,
        n_assets=n_assets,
        n_levels=checked_levels.shape[2],
        x0_width=x0.shape[1],
        source_receipt=source_receipt,
        design_sha256=design_sha256,
        x0tx0_upper=pack_symmetric_upper(gram),
    )
    design = SmoothDateDesign(
        date_index=date_index,
        n_rows=n_rows,
        n_assets=n_assets,
        n_levels=checked_levels.shape[2],
        source_receipt=source_receipt,
        design_sha256=design_sha256,
        x0=_readonly_float64(x0),
        pca=pca,
        base_moments=base,
    )
    return design


def build_contract_smooth_date_design(
    date: G2Date,
    *,
    contract: G2Contract,
) -> SmoothDateDesign:
    """Apply the generic date kernel only to the sealed G2 dimensions."""
    validate_g2_contract(contract)
    if type(date) is not G2Date:
        raise TypeError("contract date design requires the exact G2Date type")
    receipt = validate_g2_date(date, contract)
    if receipt.response_map.reliability != contract.confirmatory_reliability:
        raise ValueError("smooth contract designs require the canonical reliability anchor")
    expected = (contract.bins_per_date, contract.n_assets)
    if date.q.shape != expected or date.x.shape != (*expected, contract.n_levels):
        raise ValueError("G2Date does not match the sealed smooth-estimator dimensions")
    if date.filtered.factor.shape != (
        contract.bins_per_date,
    ) or date.filtered.proxy_noise.shape != (contract.bins_per_date,):
        raise ValueError("G2Date factor/proxy shapes changed")
    design = _build_smooth_date_design(
        date_index=date.filtered.provenance.date_index,
        factor=date.filtered.factor,
        proxy_noise=date.filtered.proxy_noise,
        oracle_flow=date.q,
        level_flows=date.x,
        eigengap_ratio=contract.pca_top_eigengap_min_trace_ratio,
        source_receipt=receipt,
    )
    if (design.n_rows, design.n_assets, design.n_levels, design.base_moments.x0_width) != (
        contract.bins_per_date,
        contract.n_assets,
        contract.n_levels,
        3 + 2 * contract.n_assets,
    ):
        raise ValueError("contract date design did not preserve the sealed dimensions")
    base_key = id(design.base_moments)

    def discard_base(reference: weakref.ReferenceType[SmoothBaseDateMoments]) -> None:
        current = _CONTRACT_BASE_DATE_REGISTRY.get(base_key)
        if current is not None and current[0] is reference:
            _CONTRACT_BASE_DATE_REGISTRY.pop(base_key, None)

    base_reference = cast(
        weakref.ReferenceType[object],
        weakref.ref(design.base_moments, discard_base),
    )
    _CONTRACT_BASE_DATE_REGISTRY[base_key] = (
        base_reference,
        _base_date_token(design.base_moments),
    )
    design_key = id(design)

    def discard_design(reference: weakref.ReferenceType[SmoothDateDesign]) -> None:
        current = _CONTRACT_DESIGN_REGISTRY.get(design_key)
        if current is not None and current[0] is reference:
            _CONTRACT_DESIGN_REGISTRY.pop(design_key, None)

    design_reference = cast(
        weakref.ReferenceType[object],
        weakref.ref(design, discard_design),
    )
    _CONTRACT_DESIGN_REGISTRY[design_key] = (design_reference, _design_token(design))
    return design


def build_cell_date_moments(
    design: SmoothDateDesign,
    responses: NDArray[np.float64],
) -> SmoothCellDateMoments:
    """Build the response moments for one structural cell/date."""
    if type(design) is not SmoothDateDesign:
        raise TypeError("cell moments require the exact SmoothDateDesign type")
    if design.source_receipt is not None:
        raise ValueError("contract designs require build_contract_cell_date_moments")
    return _build_cell_date_moments(
        design,
        responses,
        response_receipt=None,
    )


def _build_cell_date_moments(
    design: SmoothDateDesign,
    responses: NDArray[np.float64],
    *,
    response_receipt: G2DateReceipt | None,
) -> SmoothCellDateMoments:
    checked = _finite_float64_array(responses, name="responses", ndim=2)
    if checked.shape != (design.n_rows, design.n_assets):
        raise ValueError("responses must match the date design rows and assets")
    cross = design.x0.T @ checked
    yty = checked.T @ checked
    if not np.all(np.isfinite(cross)) or not np.all(np.isfinite(yty)):
        raise ValueError("cell date moments contain a nonfinite value")
    moment = SmoothCellDateMoments(
        date_index=design.date_index,
        n_rows=design.n_rows,
        n_assets=design.n_assets,
        x0_width=design.base_moments.x0_width,
        design_receipt=design.source_receipt,
        response_receipt=response_receipt,
        design_sha256=design.design_sha256,
        x0ty=_readonly_float64(cross),
        yty_upper=pack_symmetric_upper(yty),
    )
    return moment


def build_contract_cell_date_moments(
    design: SmoothDateDesign,
    date: G2Date,
    *,
    contract: G2Contract,
) -> SmoothCellDateMoments:
    """Build issued response moments from a date on the design's exact base."""
    validate_g2_contract(contract)
    if type(design) is not SmoothDateDesign or design.source_receipt is None:
        raise TypeError("contract cell moments require an issued contract design")
    _validate_issued(
        design,
        _CONTRACT_DESIGN_REGISTRY,
        _design_token(design),
        name="contract date design",
    )
    _validate_issued(
        design.base_moments,
        _CONTRACT_BASE_DATE_REGISTRY,
        _base_date_token(design.base_moments),
        name="contract base date moment",
    )
    response_receipt = validate_g2_date(date, contract)
    if response_receipt.response_map.reliability != contract.confirmatory_reliability:
        raise ValueError("smooth contract responses require the canonical reliability anchor")
    design_provenance = design.source_receipt.provenance
    response_provenance = response_receipt.provenance
    if (
        response_receipt.base_identity != design.source_receipt.base_identity
        or response_provenance != design_provenance
        or response_provenance.date_index != design.date_index
    ):
        raise ValueError("contract response date does not share the design base provenance")
    moment = _build_cell_date_moments(
        design,
        date.r,
        response_receipt=response_receipt,
    )
    moment_key = id(moment)

    def discard_moment(reference: weakref.ReferenceType[SmoothCellDateMoments]) -> None:
        current = _CONTRACT_CELL_DATE_REGISTRY.get(moment_key)
        if current is not None and current[0] is reference:
            _CONTRACT_CELL_DATE_REGISTRY.pop(moment_key, None)

    moment_reference = cast(
        weakref.ReferenceType[object],
        weakref.ref(moment, discard_moment),
    )
    _CONTRACT_CELL_DATE_REGISTRY[moment_key] = (
        moment_reference,
        _cell_date_token(moment),
    )
    return moment


def _strictly_ascending(indices: tuple[int, ...]) -> bool:
    return all(left < right for left, right in pairwise(indices))


def _validate_complete_contract_receipts(
    receipts: Sequence[G2DateReceipt],
    *,
    require_common_response_map: bool,
) -> None:
    if not receipts:
        raise ValueError("a contract panel requires at least one issued receipt")
    first = receipts[0]
    provenance = first.provenance
    prefix = (
        provenance.master_seed,
        provenance.stream,
        provenance.phase_id,
        provenance.scenario_id,
        provenance.n_dates,
        provenance.panel_index,
    )
    if len(receipts) != provenance.n_dates:
        raise ValueError("contract panel omitted one or more declared dates")
    for expected_index, receipt in enumerate(receipts):
        current = receipt.provenance
        current_prefix = (
            current.master_seed,
            current.stream,
            current.phase_id,
            current.scenario_id,
            current.n_dates,
            current.panel_index,
        )
        if current_prefix != prefix or current.date_index != expected_index:
            raise ValueError("contract panel provenance is not one complete ordered panel")
        if require_common_response_map and receipt.response_map != first.response_map:
            raise ValueError("contract cell panel mixes response-map identities")


def stack_base_moments(
    dates: Sequence[SmoothDateDesign | SmoothBaseDateMoments],
) -> SmoothBasePanelMoments:
    """Stack shared moments in their already ascending date order."""
    snapshot = tuple(dates)
    if not snapshot:
        raise ValueError("at least one base date is required")
    extracted: list[SmoothBaseDateMoments] = []
    for date in snapshot:
        if type(date) is SmoothDateDesign:
            extracted.append(date.base_moments)
        elif type(date) is SmoothBaseDateMoments:
            extracted.append(date)
        else:
            raise TypeError("base panel entries must be exact smooth date moment types")
    first = extracted[0]
    if any(item.source_receipt is not None for item in extracted):
        raise ValueError("contract base moments require stack_contract_base_moments")
    indices = tuple(item.date_index for item in extracted)
    if not _strictly_ascending(indices):
        raise ValueError("base date indices must be strictly ascending")
    identity = (first.n_rows, first.n_assets, first.n_levels, first.x0_width)
    if any(
        (item.n_rows, item.n_assets, item.n_levels, item.x0_width) != identity for item in extracted
    ):
        raise ValueError("base date moments have inconsistent dimensions")
    stacked = np.stack([item.x0tx0_upper for item in extracted], axis=0)
    return SmoothBasePanelMoments(
        date_indices=indices,
        n_rows=first.n_rows,
        n_assets=first.n_assets,
        n_levels=first.n_levels,
        x0_width=first.x0_width,
        source_receipts=tuple(item.source_receipt for item in extracted),
        design_sha256s=tuple(item.design_sha256 for item in extracted),
        x0tx0_upper=_readonly_float64(stacked),
    )


def stack_contract_base_moments(
    dates: Sequence[SmoothDateDesign | SmoothBaseDateMoments],
) -> SmoothBasePanelMoments:
    """Stack one complete issued contract panel and mint its panel receipt."""
    snapshot = tuple(dates)
    if not snapshot:
        raise ValueError("at least one contract base date is required")
    extracted: list[SmoothBaseDateMoments] = []
    for date in snapshot:
        if type(date) is SmoothDateDesign:
            extracted.append(date.base_moments)
        elif type(date) is SmoothBaseDateMoments:
            extracted.append(date)
        else:
            raise TypeError("contract base panel entries use exact smooth moment types")
    receipts: list[G2DateReceipt] = []
    for item in extracted:
        if item.source_receipt is None:
            raise ValueError("analytic base moments cannot enter a contract panel")
        _validate_issued(
            item,
            _CONTRACT_BASE_DATE_REGISTRY,
            _base_date_token(item),
            name="contract base date moment",
        )
        receipts.append(item.source_receipt)
    _validate_complete_contract_receipts(receipts, require_common_response_map=False)
    first = extracted[0]
    identity = (first.n_rows, first.n_assets, first.n_levels, first.x0_width)
    if any(
        (item.n_rows, item.n_assets, item.n_levels, item.x0_width) != identity for item in extracted
    ):
        raise ValueError("contract base date moments have inconsistent dimensions")
    indices = tuple(item.date_index for item in extracted)
    stacked = np.stack([item.x0tx0_upper for item in extracted], axis=0)
    panel = SmoothBasePanelMoments(
        date_indices=indices,
        n_rows=first.n_rows,
        n_assets=first.n_assets,
        n_levels=first.n_levels,
        x0_width=first.x0_width,
        source_receipts=tuple(receipts),
        design_sha256s=tuple(item.design_sha256 for item in extracted),
        x0tx0_upper=_readonly_float64(stacked),
    )
    panel_key = id(panel)

    def discard_panel(reference: weakref.ReferenceType[SmoothBasePanelMoments]) -> None:
        current = _CONTRACT_BASE_PANEL_REGISTRY.get(panel_key)
        if current is not None and current[0] is reference:
            _CONTRACT_BASE_PANEL_REGISTRY.pop(panel_key, None)

    panel_reference = cast(
        weakref.ReferenceType[object],
        weakref.ref(panel, discard_panel),
    )
    _CONTRACT_BASE_PANEL_REGISTRY[panel_key] = (panel_reference, _base_panel_token(panel))
    return panel


def stack_cell_moments(dates: Sequence[SmoothCellDateMoments]) -> SmoothCellPanelMoments:
    """Stack cell moments in their already ascending date order."""
    snapshot = tuple(dates)
    if not snapshot:
        raise ValueError("at least one cell date is required")
    if any(type(item) is not SmoothCellDateMoments for item in snapshot):
        raise TypeError("cell panel entries must be exact SmoothCellDateMoments values")
    first = snapshot[0]
    if any(
        item.design_receipt is not None or item.response_receipt is not None for item in snapshot
    ):
        raise ValueError("contract cell moments require stack_contract_cell_moments")
    indices = tuple(item.date_index for item in snapshot)
    if not _strictly_ascending(indices):
        raise ValueError("cell date indices must be strictly ascending")
    identity = (first.n_rows, first.n_assets, first.x0_width)
    if any((item.n_rows, item.n_assets, item.x0_width) != identity for item in snapshot):
        raise ValueError("cell date moments have inconsistent dimensions")
    x0ty = np.stack([item.x0ty for item in snapshot], axis=0)
    yty = np.stack([item.yty_upper for item in snapshot], axis=0)
    return SmoothCellPanelMoments(
        date_indices=indices,
        n_rows=first.n_rows,
        n_assets=first.n_assets,
        x0_width=first.x0_width,
        design_receipts=tuple(item.design_receipt for item in snapshot),
        response_receipts=tuple(item.response_receipt for item in snapshot),
        design_sha256s=tuple(item.design_sha256 for item in snapshot),
        x0ty=_readonly_float64(x0ty),
        yty_upper=_readonly_float64(yty),
    )


def stack_contract_cell_moments(
    dates: Sequence[SmoothCellDateMoments],
) -> SmoothCellPanelMoments:
    """Stack one complete issued contract response panel and mint its receipt."""
    snapshot = tuple(dates)
    if not snapshot:
        raise ValueError("at least one contract cell date is required")
    if any(type(item) is not SmoothCellDateMoments for item in snapshot):
        raise TypeError("contract cell panel entries use exact SmoothCellDateMoments")
    design_receipts: list[G2DateReceipt] = []
    response_receipts: list[G2DateReceipt] = []
    for item in snapshot:
        if item.design_receipt is None or item.response_receipt is None:
            raise ValueError("analytic cell moments cannot enter a contract panel")
        _validate_issued(
            item,
            _CONTRACT_CELL_DATE_REGISTRY,
            _cell_date_token(item),
            name="contract cell date moment",
        )
        design_receipts.append(item.design_receipt)
        response_receipts.append(item.response_receipt)
    _validate_complete_contract_receipts(
        design_receipts,
        require_common_response_map=False,
    )
    _validate_complete_contract_receipts(
        response_receipts,
        require_common_response_map=True,
    )
    for design_receipt, response_receipt in zip(
        design_receipts,
        response_receipts,
        strict=True,
    ):
        if (
            design_receipt.provenance != response_receipt.provenance
            or design_receipt.base_identity != response_receipt.base_identity
        ):
            raise ValueError("contract cell panel response does not match its design base")
    first = snapshot[0]
    identity = (first.n_rows, first.n_assets, first.x0_width)
    if any((item.n_rows, item.n_assets, item.x0_width) != identity for item in snapshot):
        raise ValueError("contract cell date moments have inconsistent dimensions")
    indices = tuple(item.date_index for item in snapshot)
    x0ty = np.stack([item.x0ty for item in snapshot], axis=0)
    yty = np.stack([item.yty_upper for item in snapshot], axis=0)
    panel = SmoothCellPanelMoments(
        date_indices=indices,
        n_rows=first.n_rows,
        n_assets=first.n_assets,
        x0_width=first.x0_width,
        design_receipts=tuple(design_receipts),
        response_receipts=tuple(response_receipts),
        design_sha256s=tuple(item.design_sha256 for item in snapshot),
        x0ty=_readonly_float64(x0ty),
        yty_upper=_readonly_float64(yty),
    )
    panel_key = id(panel)

    def discard_panel(reference: weakref.ReferenceType[SmoothCellPanelMoments]) -> None:
        current = _CONTRACT_CELL_PANEL_REGISTRY.get(panel_key)
        if current is not None and current[0] is reference:
            _CONTRACT_CELL_PANEL_REGISTRY.pop(panel_key, None)

    panel_reference = cast(
        weakref.ReferenceType[object],
        weakref.ref(panel, discard_panel),
    )
    _CONTRACT_CELL_PANEL_REGISTRY[panel_key] = (panel_reference, _cell_panel_token(panel))
    return panel


def _validate_date_weights(weights: NDArray[np.float64], *, n_dates: int) -> None:
    if type(weights) is not np.ndarray or weights.dtype != np.dtype(np.float64):
        raise TypeError("date weights must be an exact float64 ndarray")
    if weights.shape != (n_dates,) or not weights.flags.c_contiguous:
        raise ValueError("date weights must be a C-contiguous vector matching the panel")
    if not np.all(np.isfinite(weights)):
        raise ValueError("date weights contain a nonfinite value")
    if np.any(weights < 0.0) or np.any(np.signbit(weights) & (weights == 0.0)):
        raise ValueError("date weights must be nonnegative without signed zero")
    if not np.array_equal(weights, np.floor(weights)):
        raise ValueError("date weights must be exact integer counts")
    if float(np.sum(weights, dtype=np.float64)) != float(n_dates):
        raise ValueError("date weights must sum exactly to the number of dates")


def aggregate_smooth_moments(
    base: SmoothBasePanelMoments,
    cell: SmoothCellPanelMoments,
    weights: NDArray[np.float64],
) -> SmoothAggregateMoments:
    """Aggregate analytic-only panels without minting contract authority."""
    if any(item is not None for item in base.source_receipts) or any(
        item is not None for item in cell.response_receipts
    ):
        raise ValueError("contract panels require aggregate_contract_smooth_moments")
    return _aggregate_smooth_moments(base, cell, weights)


def aggregate_contract_smooth_moments(
    base: SmoothBasePanelMoments,
    cell: SmoothCellPanelMoments,
    weights: NDArray[np.float64],
) -> SmoothAggregateMoments:
    """Aggregate issued complete contract panels and mint aggregate authority."""
    _validate_issued(
        base,
        _CONTRACT_BASE_PANEL_REGISTRY,
        _base_panel_token(base),
        name="contract base panel",
    )
    _validate_issued(
        cell,
        _CONTRACT_CELL_PANEL_REGISTRY,
        _cell_panel_token(cell),
        name="contract cell panel",
    )
    aggregate = _aggregate_smooth_moments(base, cell, weights)
    aggregate_key = id(aggregate)

    def discard_aggregate(reference: weakref.ReferenceType[SmoothAggregateMoments]) -> None:
        current = _CONTRACT_AGGREGATE_REGISTRY.get(aggregate_key)
        if current is not None and current[0] is reference:
            _CONTRACT_AGGREGATE_REGISTRY.pop(aggregate_key, None)

    aggregate_reference = cast(
        weakref.ReferenceType[object],
        weakref.ref(aggregate, discard_aggregate),
    )
    _CONTRACT_AGGREGATE_REGISTRY[aggregate_key] = (
        aggregate_reference,
        _aggregate_token(aggregate),
    )
    return aggregate


def _aggregate_smooth_moments(
    base: SmoothBasePanelMoments,
    cell: SmoothCellPanelMoments,
    weights: NDArray[np.float64],
) -> SmoothAggregateMoments:
    """Aggregate all three moment fields with one matrix multiplication each."""
    if type(base) is not SmoothBasePanelMoments or type(cell) is not SmoothCellPanelMoments:
        raise TypeError("aggregation requires exact smooth panel moment types")
    if base.date_indices != cell.date_indices:
        raise ValueError("base and cell panel date provenance differs")
    if base.design_sha256s != cell.design_sha256s:
        raise ValueError("base and cell panels contain different design digests")
    if base.source_receipts != cell.design_receipts:
        raise ValueError("base and cell panels contain different design provenance")
    if (base.n_rows, base.n_assets, base.x0_width) != (
        cell.n_rows,
        cell.n_assets,
        cell.x0_width,
    ):
        raise ValueError("base and cell panel dimensions differ")
    n_dates = len(base.date_indices)
    _validate_date_weights(weights, n_dates=n_dates)
    packed_gram = np.matmul(weights, base.x0tx0_upper)
    cross_flat = np.matmul(weights, cell.x0ty.reshape(n_dates, -1))
    packed_yty = np.matmul(weights, cell.yty_upper)
    gram = unpack_symmetric_upper(
        np.ascontiguousarray(packed_gram, dtype=np.float64),
        size=base.x0_width,
    )
    yty = unpack_symmetric_upper(
        np.ascontiguousarray(packed_yty, dtype=np.float64),
        size=base.n_assets,
    )
    cross = np.ascontiguousarray(
        cross_flat.reshape(base.x0_width, base.n_assets),
        dtype=np.float64,
    )
    row_mass = float(gram[0, 0])
    expected_mass = float(n_dates * base.n_rows)
    if not math.isfinite(row_mass) or row_mass <= 0.0 or row_mass != expected_mass:
        raise ValueError("aggregated global row mass is invalid")
    if not np.all(np.isfinite(cross)):
        raise ValueError("aggregated response cross-moments are nonfinite")
    return SmoothAggregateMoments(
        row_mass=row_mass,
        n_rows=base.n_rows,
        n_assets=base.n_assets,
        n_levels=base.n_levels,
        x0_width=base.x0_width,
        source_receipts=base.source_receipts,
        response_receipts=cell.response_receipts,
        design_sha256s=base.design_sha256s,
        x0tx0=gram,
        x0ty=_readonly_float64(cross),
        yty=yty,
    )


def solve_condition_ridge(
    flow_covariance: NDArray[np.float64],
    response_flow_covariance: NDArray[np.float64],
    *,
    contract: G2Contract,
) -> ConditionRidgeResult:
    """Apply the frozen once-symmetrized condition-capped ridge solve."""
    validate_g2_contract(contract)
    flow = _finite_float64_array(flow_covariance, name="flow_covariance", ndim=2)
    cross = _finite_float64_array(
        response_flow_covariance,
        name="response_flow_covariance",
        ndim=2,
    )
    if flow.shape[0] != flow.shape[1] or cross.shape[1] != flow.shape[0]:
        raise ValueError("ridge covariance dimensions are incompatible")
    symmetric = 0.5 * (flow + flow.T)
    try:
        eigenvalues = np.linalg.eigvalsh(symmetric)
    except np.linalg.LinAlgError as error:
        raise ValueError("ridge eigensolver failed") from error
    if not np.all(np.isfinite(eigenvalues)):
        raise ValueError("ridge eigenvalues are nonfinite")
    smallest = float(eigenvalues[0])
    largest = float(eigenvalues[-1])
    if not math.isfinite(largest) or largest <= 0.0:
        raise ValueError("ridge largest eigenvalue must be finite and positive")
    epsilon = np.finfo(np.float64).eps
    negative_tolerance = (
        contract.ridge_negative_eigen_roundoff_multiplier * epsilon * max(1.0, abs(largest))
    )
    if smallest < -negative_tolerance:
        raise ValueError("ridge smallest eigenvalue is more negative than roundoff tolerance")
    condition_penalty = max(
        0.0,
        (largest - contract.ridge_condition_cap * smallest) / (contract.ridge_condition_cap - 1.0),
    )
    floor_penalty = (
        contract.ridge_floor_trace_ratio * float(np.trace(symmetric)) / float(flow.shape[0])
    )
    penalty = max(condition_penalty, floor_penalty)
    regularized_minimum = smallest + penalty
    if not math.isfinite(penalty) or not math.isfinite(regularized_minimum):
        raise ValueError("ridge penalty is nonfinite")
    if regularized_minimum <= 0.0:
        raise ValueError("ridge regularized minimum eigenvalue is nonpositive")
    post_condition = (largest + penalty) / regularized_minimum
    allowed = contract.ridge_condition_cap * (
        1.0 + contract.ridge_post_condition_slack_multiplier * epsilon
    )
    if not math.isfinite(post_condition) or post_condition > allowed:
        raise ValueError("ridge post-regularization condition cap failed")
    regularized = symmetric + penalty * np.eye(flow.shape[0], dtype=np.float64)
    try:
        coefficients = np.linalg.solve(regularized.T, cross.T).T
    except np.linalg.LinAlgError as error:
        raise ValueError("ridge linear solve failed") from error
    if not np.all(np.isfinite(coefficients)):
        raise ValueError("ridge coefficients are nonfinite")
    return ConditionRidgeResult(
        coefficients=_readonly_float64(coefficients),
        smallest_eigenvalue=smallest,
        largest_eigenvalue=largest,
        penalty_condition=float(condition_penalty),
        penalty_floor=float(floor_penalty),
        penalty=float(penalty),
        post_condition_number=float(post_condition),
    )


def _reliability_tau(reliability: float) -> float:
    if not math.isfinite(reliability) or not 0.95 <= reliability <= 1.0:
        raise ValueError("smooth estimator reliability must lie in [0.95, 1]")
    return math.sqrt(1.0 / reliability - 1.0)


def _validate_contract_aggregate(
    aggregate: SmoothAggregateMoments,
    contract: G2Contract,
) -> None:
    validate_g2_contract(contract)
    if type(aggregate) is not SmoothAggregateMoments:
        raise TypeError("G2 fit requires exact SmoothAggregateMoments")
    _validate_issued(
        aggregate,
        _CONTRACT_AGGREGATE_REGISTRY,
        _aggregate_token(aggregate),
        name="contract aggregate",
    )
    if (
        aggregate.n_rows != contract.bins_per_date
        or aggregate.n_assets != contract.n_assets
        or aggregate.n_levels != contract.n_levels
        or aggregate.x0_width != 3 + 2 * contract.n_assets
    ):
        raise ValueError("contract aggregate dimensions differ from the sealed G2 design")
    if any(item is None for item in aggregate.source_receipts) or any(
        item is None for item in aggregate.response_receipts
    ):
        raise ValueError("contract aggregate lost issued date provenance")
    n_dates = len(aggregate.source_receipts)
    if aggregate.row_mass != float(n_dates * contract.bins_per_date):
        raise ValueError("contract aggregate row mass differs from its complete panel")


def validate_aggregate_response_map(
    aggregate: SmoothAggregateMoments,
    *,
    expected: G2ResponseMapIdentity,
    reliability: float,
) -> G2ResponseMapIdentity:
    """Bind a fit label to one aggregate while preserving reliability reuse."""
    if type(aggregate) is not SmoothAggregateMoments:
        raise TypeError("response-map validation requires exact SmoothAggregateMoments")
    _validate_response_map_identity(expected, name="expected response map")
    if type(reliability) is not float or reliability != expected.reliability:
        raise ValueError("fit reliability differs from the expected response-map identity")
    if not aggregate.response_receipts or any(
        receipt is None for receipt in aggregate.response_receipts
    ):
        raise ValueError("aggregate does not retain a complete response-map identity")
    receipts = tuple(receipt for receipt in aggregate.response_receipts if receipt is not None)
    for receipt in receipts:
        _receipt_payload(receipt)
    actual = receipts[0].response_map
    if any(receipt.response_map != actual for receipt in receipts):
        raise ValueError("aggregate mixes response-map identities")
    actual_structural = (actual.target_index, actual.paper_recovery, actual.phi)
    expected_structural = (
        expected.target_index,
        expected.paper_recovery,
        expected.phi,
    )
    if actual_structural != expected_structural:
        raise ValueError("aggregate structural response map differs from the expected identity")
    return actual


def extract_condition_ridge_moments(
    aggregate: SmoothAggregateMoments,
    *,
    flow_view: G2FlowView,
    reliability: float,
) -> ConditionRidgeMoments:
    """Extract pure global covariance blocks for one ridge view."""
    if type(aggregate) is not SmoothAggregateMoments:
        raise TypeError("ridge extraction requires exact SmoothAggregateMoments")
    if type(flow_view) is not G2FlowView:
        raise TypeError("flow_view must use the exact G2FlowView enum")
    n_assets = aggregate.n_assets
    if aggregate.x0_width != 3 + 2 * n_assets:
        raise ValueError("aggregate polynomial width is inconsistent with its asset count")
    tau = _reliability_tau(reliability)
    gram = aggregate.x0tx0
    cross = aggregate.x0ty
    mass = aggregate.row_mass
    start = 3 if flow_view is G2FlowView.ORACLE else 3 + n_assets
    indices = slice(start, start + n_assets)
    sum_z = float(gram[0, 1] + tau * gram[0, 2])
    sum_flow = gram[indices, 0]
    sum_response = cross[0, :]
    raw_zz = float(gram[1, 1] + 2.0 * tau * gram[1, 2] + tau * tau * gram[2, 2])
    raw_flow_z = gram[indices, 1] + tau * gram[indices, 2]
    raw_flow_flow = gram[indices, indices]
    raw_z_response = cross[1, :] + tau * cross[2, :]
    raw_flow_response = cross[indices, :]

    proxy_variance = (raw_zz - sum_z * sum_z / mass) / mass
    flow_proxy = (raw_flow_z - sum_flow * sum_z / mass) / mass
    flow_covariance = (raw_flow_flow - np.outer(sum_flow, sum_flow) / mass) / mass
    response_proxy = (raw_z_response - sum_response * sum_z / mass) / mass
    response_flow = (raw_flow_response.T - np.outer(sum_response, sum_flow) / mass) / mass
    if not math.isfinite(proxy_variance) or proxy_variance <= 0.0:
        raise ValueError("centered proxy variance must be finite and positive")
    schur_flow = flow_covariance - np.outer(flow_proxy, flow_proxy) / proxy_variance
    schur_response = response_flow - np.outer(response_proxy, flow_proxy) / proxy_variance
    if not np.all(np.isfinite(schur_flow)) or not np.all(np.isfinite(schur_response)):
        raise ValueError("ridge Schur covariance is nonfinite")
    return ConditionRidgeMoments(
        flow_covariance=_readonly_float64(np.ascontiguousarray(schur_flow, dtype=np.float64)),
        response_flow_covariance=_readonly_float64(
            np.ascontiguousarray(schur_response, dtype=np.float64)
        ),
    )


def fit_condition_ridge(
    aggregate: SmoothAggregateMoments,
    *,
    flow_view: G2FlowView,
    reliability: float,
    expected_response_map: G2ResponseMapIdentity,
    contract: G2Contract,
) -> ConditionRidgeResult:
    """Fit one licensed G2 ridge view from an issued complete aggregate."""
    _validate_contract_aggregate(aggregate, contract)
    validate_aggregate_response_map(
        aggregate,
        expected=expected_response_map,
        reliability=reliability,
    )
    moments = extract_condition_ridge_moments(
        aggregate,
        flow_view=flow_view,
        reliability=reliability,
    )
    return solve_condition_ridge(
        moments.flow_covariance,
        moments.response_flow_covariance,
        contract=contract,
    )


def solve_pooled_homogeneous(
    slope_covariance: NDArray[np.float64],
    slope_response_covariance: NDArray[np.float64],
    *,
    predictor_means: NDArray[np.float64],
    response_mean: float,
    contract: G2Contract,
) -> HomogeneousResult:
    """Solve the frozen full-rank three-slope pooled system."""
    validate_g2_contract(contract)
    slopes_cov = _finite_float64_array(slope_covariance, name="slope_covariance", ndim=2)
    response_cov = _finite_float64_array(
        slope_response_covariance,
        name="slope_response_covariance",
        ndim=1,
    )
    means = _finite_float64_array(predictor_means, name="predictor_means", ndim=1)
    if slopes_cov.shape != (3, 3) or response_cov.shape != (3,) or means.shape != (3,):
        raise ValueError("pooled homogeneous solve requires one three-slope system")
    if not math.isfinite(response_mean):
        raise ValueError("pooled response mean is nonfinite")
    symmetric = 0.5 * (slopes_cov + slopes_cov.T)
    try:
        singular_values = np.linalg.svd(symmetric, compute_uv=False)
    except np.linalg.LinAlgError as error:
        raise ValueError("pooled singular-value calculation failed") from error
    if not np.all(np.isfinite(singular_values)):
        raise ValueError("pooled singular values are nonfinite")
    largest = float(singular_values[0])
    smallest = float(singular_values[-1])
    rank_tolerance = contract.pooled_rank_multiplier * np.finfo(np.float64).eps * largest
    if smallest <= rank_tolerance:
        raise ValueError("pooled slope matrix failed the full-rank tolerance")
    condition = largest / smallest
    if not math.isfinite(condition) or condition > contract.pooled_condition_number_max:
        raise ValueError("pooled slope matrix exceeds the condition cap")
    try:
        slopes = np.linalg.solve(symmetric, response_cov)
    except np.linalg.LinAlgError as error:
        raise ValueError("pooled linear solve failed") from error
    if not np.all(np.isfinite(slopes)):
        raise ValueError("pooled slopes are nonfinite")
    intercept = float(response_mean - means @ slopes)
    if not math.isfinite(intercept):
        raise ValueError("pooled intercept is nonfinite")
    return HomogeneousResult(
        intercept=intercept,
        slopes=_readonly_float64(slopes),
        singular_values=_readonly_float64(singular_values),
        condition_number=float(condition),
    )


def extract_homogeneous_moments(
    aggregate: SmoothAggregateMoments,
    *,
    reliability: float,
) -> HomogeneousMoments:
    """Derive pure pooled moments algebraically without fit authority."""
    if type(aggregate) is not SmoothAggregateMoments:
        raise TypeError("homogeneous extraction requires exact SmoothAggregateMoments")
    n_assets = aggregate.n_assets
    if n_assets < 2 or aggregate.x0_width != 3 + 2 * n_assets:
        raise ValueError("aggregate dimensions cannot define homogeneous moments")
    tau = _reliability_tau(reliability)
    gram = aggregate.x0tx0
    cross = aggregate.x0ty
    mass = aggregate.row_mass
    q_indices = slice(3, 3 + n_assets)
    q_cross = gram[q_indices, q_indices]
    q_response = cross[q_indices, :]
    q_sum = gram[q_indices, 0]
    ones = np.ones(n_assets, dtype=np.float64)
    sum_q = float(ones @ q_sum)
    sum_z = float(gram[0, 1] + tau * gram[0, 2])
    raw_zz = float(gram[1, 1] + 2.0 * tau * gram[1, 2] + tau * tau * gram[2, 2])
    q_z = gram[q_indices, 1] + tau * gram[q_indices, 2]
    response_sum_vector = cross[0, :]
    response_sum = float(ones @ response_sum_vector)
    z_response = cross[1, :] + tau * cross[2, :]

    trace_q = float(np.trace(q_cross))
    total_q_cross = float(ones @ q_cross @ ones)
    total_qz = float(ones @ q_z)
    predictor_sums = np.asarray(
        [sum_q, (n_assets - 1.0) * sum_q, n_assets * sum_z],
        dtype=np.float64,
    )
    raw_slope = np.asarray(
        [
            [trace_q, total_q_cross - trace_q, total_qz],
            [
                total_q_cross - trace_q,
                (n_assets - 2.0) * total_q_cross + trace_q,
                (n_assets - 1.0) * total_qz,
            ],
            [total_qz, (n_assets - 1.0) * total_qz, n_assets * raw_zz],
        ],
        dtype=np.float64,
    )
    trace_q_response = float(np.trace(q_response))
    total_q_response = float(ones @ q_response @ ones)
    raw_response = np.asarray(
        [
            trace_q_response,
            total_q_response - trace_q_response,
            float(z_response @ ones),
        ],
        dtype=np.float64,
    )
    pooled_mass = float(n_assets) * mass
    if not math.isfinite(pooled_mass) or pooled_mass <= 0.0:
        raise ValueError("pooled global weight mass must be finite and positive")
    slope_covariance = (
        raw_slope - np.outer(predictor_sums, predictor_sums) / pooled_mass
    ) / pooled_mass
    slope_response = (raw_response - predictor_sums * response_sum / pooled_mass) / pooled_mass
    return HomogeneousMoments(
        slope_covariance=_readonly_float64(
            np.ascontiguousarray(slope_covariance, dtype=np.float64)
        ),
        slope_response_covariance=_readonly_float64(
            np.ascontiguousarray(slope_response, dtype=np.float64)
        ),
        predictor_means=_readonly_float64(
            np.ascontiguousarray(predictor_sums / pooled_mass, dtype=np.float64)
        ),
        response_mean=response_sum / pooled_mass,
    )


def fit_homogeneous_ols(
    aggregate: SmoothAggregateMoments,
    *,
    reliability: float,
    expected_response_map: G2ResponseMapIdentity,
    contract: G2Contract,
) -> HomogeneousResult:
    """Fit licensed G2 pooled OLS from an issued complete aggregate."""
    _validate_contract_aggregate(aggregate, contract)
    validate_aggregate_response_map(
        aggregate,
        expected=expected_response_map,
        reliability=reliability,
    )
    moments = extract_homogeneous_moments(aggregate, reliability=reliability)
    return solve_pooled_homogeneous(
        moments.slope_covariance,
        moments.slope_response_covariance,
        predictor_means=moments.predictor_means,
        response_mean=moments.response_mean,
        contract=contract,
    )
