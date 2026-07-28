from __future__ import annotations

import gc
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import weakref
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest

import xid.models.g2_checkpoint as checkpoint_codec
import xid.models.g2_smooth as smooth_model
import xid.sim.g2 as g2_module
from xid.models.g2_checkpoint import (
    G2CheckpointTelemetry,
    G2PanelCheckpointExpectation,
)
from xid.models.g2_smooth import (
    G2FlowView,
    SmoothBasePanelMoments,
    SmoothCellPanelMoments,
    aggregate_contract_smooth_moments,
    build_contract_cell_date_moments,
    build_contract_smooth_date_design,
    fit_condition_ridge,
    fit_homogeneous_ols,
    load_contract_base_panel_checkpoint,
    load_contract_cell_panel_checkpoint,
    stack_contract_base_moments,
    stack_contract_cell_moments,
    write_contract_base_panel_checkpoint,
    write_contract_cell_panel_checkpoint,
)
from xid.sim.g2 import (
    G2Contract,
    G2ResponseMapIdentity,
    G2Stream,
    TestRngNamespace,
    build_cell,
    load_g2_contract,
    transform_date,
)


def _root() -> Path:
    return Path(__file__).parents[1]


@dataclass(frozen=True)
class _IssuedFixture:
    contract: G2Contract
    namespace: TestRngNamespace
    base: SmoothBasePanelMoments
    cell: SmoothCellPanelMoments
    base_expected: G2PanelCheckpointExpectation
    cell_expected: G2PanelCheckpointExpectation


@pytest.fixture(scope="module")
def issued_fixture() -> _IssuedFixture:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, 1729)
    design_cell = build_cell(contract, target_index=16)
    response_cell = build_cell(contract, target_index=0)
    base_moments = []
    cell_moments = []
    for date_index in range(48):
        raw = namespace.draw_base_normals(
            stream=G2Stream.VALIDATION_DATE_FRONTIER,
            n_dates=48,
            panel_index=0,
            date_index=date_index,
        )
        design_date = transform_date(
            raw,
            design_cell,
            contract=contract,
            phi=contract.confirmatory_ar1,
            reliability=contract.confirmatory_reliability,
        )
        response_date = transform_date(
            raw,
            response_cell,
            contract=contract,
            phi=contract.confirmatory_ar1,
            reliability=contract.confirmatory_reliability,
        )
        design = build_contract_smooth_date_design(design_date, contract=contract)
        cell_moment = build_contract_cell_date_moments(
            design,
            response_date,
            contract=contract,
        )
        base_moments.append(design.base_moments)
        cell_moments.append(cell_moment)
    base = stack_contract_base_moments(base_moments)
    cell = stack_contract_cell_moments(cell_moments)
    response_receipt = cell.response_receipts[0]
    assert response_receipt is not None
    return _IssuedFixture(
        contract=contract,
        namespace=namespace,
        base=base,
        cell=cell,
        base_expected=G2PanelCheckpointExpectation(
            master_seed=1729,
            stream=G2Stream.VALIDATION_DATE_FRONTIER,
            n_dates=48,
            panel_index=0,
            response_map=None,
        ),
        cell_expected=G2PanelCheckpointExpectation(
            master_seed=1729,
            stream=G2Stream.VALIDATION_DATE_FRONTIER,
            n_dates=48,
            panel_index=0,
            response_map=response_receipt.response_map,
        ),
    )


def _telemetry() -> G2CheckpointTelemetry:
    return G2CheckpointTelemetry(
        task_elapsed_seconds=1.25,
        cumulative_elapsed_seconds=9.5,
        peak_rss_bytes=123_456_789,
    )


def _canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
        + b"\n"
    )


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _numeric_bytes(values: np.ndarray) -> bytes:
    return values.astype("<f8", copy=False).tobytes(order="C")


def _coefficient_hash(values: np.ndarray) -> str:
    return _sha256(_numeric_bytes(values))


def _fit_hashes(
    base: SmoothBasePanelMoments,
    cell: SmoothCellPanelMoments,
    *,
    contract: G2Contract,
    response_map: G2ResponseMapIdentity,
) -> dict[str, str]:
    aggregate = aggregate_contract_smooth_moments(
        base,
        cell,
        np.ones(len(base.date_indices), dtype=np.float64),
    )
    return {
        "homogeneous": _coefficient_hash(
            fit_homogeneous_ols(
                aggregate,
                reliability=contract.confirmatory_reliability,
                expected_response_map=response_map,
                contract=contract,
            ).slopes
        ),
        "observable": _coefficient_hash(
            fit_condition_ridge(
                aggregate,
                flow_view=G2FlowView.OBSERVABLE,
                reliability=contract.confirmatory_reliability,
                expected_response_map=response_map,
                contract=contract,
            ).coefficients
        ),
        "oracle": _coefficient_hash(
            fit_condition_ridge(
                aggregate,
                flow_view=G2FlowView.ORACLE,
                reliability=contract.confirmatory_reliability,
                expected_response_map=response_map,
                contract=contract,
            ).coefficients
        ),
    }


def _publish_base(
    root: Path,
    fixture: _IssuedFixture,
) -> Any:
    root.mkdir(parents=True, exist_ok=True)
    return write_contract_base_panel_checkpoint(
        root,
        fixture.base,
        expected=fixture.base_expected,
        authority=fixture.namespace,
        contract=fixture.contract,
        repository_root=_root(),
        telemetry=_telemetry(),
    )


def _publish_pair(
    root: Path,
    fixture: _IssuedFixture,
) -> tuple[Any, Any]:
    base_evidence = _publish_base(root, fixture)
    cell_evidence = write_contract_cell_panel_checkpoint(
        root,
        fixture.base,
        fixture.cell,
        base_checkpoint=base_evidence,
        expected=fixture.cell_expected,
        authority=fixture.namespace,
        contract=fixture.contract,
        repository_root=_root(),
        telemetry=_telemetry(),
    )
    return base_evidence, cell_evidence


def _read_manifest(artifact: Path) -> dict[str, Any]:
    value = json.loads((artifact / "manifest.json").read_bytes())
    assert isinstance(value, dict)
    return value


def _artifact_sha256(
    kind: str,
    manifest_sha256: str,
    payload_pairs: list[list[str]],
) -> str:
    return _sha256(
        _canonical_bytes(
            [
                "xid-g2-panel-artifact-v1",
                kind,
                manifest_sha256,
                payload_pairs,
            ]
        )
    )


def _write_success_for_manifest_bytes(
    artifact: Path,
    *,
    manifest_bytes: bytes,
    kind: str,
    payload_pairs: list[list[str]],
) -> None:
    manifest_sha256 = _sha256(manifest_bytes)
    success = {
        "artifact_kind": kind,
        "artifact_sha256": _artifact_sha256(kind, manifest_sha256, payload_pairs),
        "complete": True,
        "manifest_sha256": manifest_sha256,
        "payload_sha256s": {name: digest for name, digest in payload_pairs},
        "schema_version": 1,
    }
    (artifact / "_SUCCESS").write_bytes(_canonical_bytes(success))


def _resign_manifest(artifact: Path, manifest: dict[str, Any]) -> None:
    manifest_bytes = _canonical_bytes(manifest)
    (artifact / "manifest.json").write_bytes(manifest_bytes)
    payload_pairs = [[payload["name"], payload["sha256"]] for payload in manifest["payloads"]]
    _write_success_for_manifest_bytes(
        artifact,
        manifest_bytes=manifest_bytes,
        kind=manifest["artifact_kind"],
        payload_pairs=payload_pairs,
    )


def _npy_bytes(values: np.ndarray) -> bytes:
    output = io.BytesIO()
    np.lib.format.write_array(
        output,
        values,
        version=(1, 0),
        allow_pickle=False,
    )
    return output.getvalue()


def _replace_payload(
    artifact: Path,
    *,
    name: str,
    payload_bytes: bytes,
    dtype: str,
    shape: tuple[int, ...],
    data_bytes: int,
    npy_format: str = "1.0",
) -> None:
    (artifact / name).write_bytes(payload_bytes)
    manifest = _read_manifest(artifact)
    descriptor = next(item for item in manifest["payloads"] if item["name"] == name)
    descriptor["dtype"] = dtype
    descriptor["npy_format"] = npy_format
    descriptor["shape"] = list(shape)
    descriptor["data_bytes"] = data_bytes
    descriptor["file_bytes"] = len(payload_bytes)
    descriptor["sha256"] = _sha256(payload_bytes)
    _resign_manifest(artifact, manifest)


def _oversized_header_npy(valid: bytes) -> bytes:
    if valid[:8] != b"\x93NUMPY\x01\x00":
        raise AssertionError("test helper requires NPY v1.0")
    old_length = int.from_bytes(valid[8:10], byteorder="little")
    old_header = valid[10 : 10 + old_length].rstrip(b" \n")
    new_length = 4097
    header = old_header + b" " * (new_length - len(old_header) - 1) + b"\n"
    return (
        valid[:8] + new_length.to_bytes(2, byteorder="little") + header + valid[10 + old_length :]
    )


def _load_base(root: Path, fixture: _IssuedFixture) -> Any:
    return load_contract_base_panel_checkpoint(
        root,
        expected=fixture.base_expected,
        authority=fixture.namespace,
        contract=fixture.contract,
        repository_root=_root(),
    )


def test_base_and_cross_cell_checkpoint_round_trip_regains_exact_authority(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    base_evidence, cell_evidence = _publish_pair(tmp_path, fixture)

    loaded_base = _load_base(tmp_path, fixture)
    loaded_cell = load_contract_cell_panel_checkpoint(
        tmp_path,
        base_checkpoint=loaded_base,
        expected=fixture.cell_expected,
        authority=fixture.namespace,
        contract=fixture.contract,
        repository_root=_root(),
    )

    assert loaded_base.evidence == base_evidence
    assert loaded_cell.evidence == cell_evidence
    assert loaded_base.evidence.telemetry == _telemetry()
    assert loaded_cell.evidence.telemetry == _telemetry()
    assert loaded_base.panel.source_receipts[0] is not None
    assert loaded_cell.panel.response_receipts[0] is not None
    assert loaded_base.panel.source_receipts[0].response_map.target_index == 16
    assert loaded_cell.panel.response_receipts[0].response_map.target_index == 0
    assert loaded_base.panel.source_receipts == fixture.base.source_receipts
    assert loaded_cell.panel.design_receipts == fixture.cell.design_receipts
    assert loaded_cell.panel.response_receipts == fixture.cell.response_receipts
    assert loaded_base.panel.design_sha256s == fixture.base.design_sha256s
    assert loaded_cell.panel.design_sha256s == fixture.cell.design_sha256s
    for recovered, original in (
        (loaded_base.panel.x0tx0_upper, fixture.base.x0tx0_upper),
        (loaded_cell.panel.x0ty, fixture.cell.x0ty),
        (loaded_cell.panel.yty_upper, fixture.cell.yty_upper),
    ):
        assert _numeric_bytes(recovered) == _numeric_bytes(original)
        assert _sha256(_numeric_bytes(recovered)) == _sha256(_numeric_bytes(original))
        assert type(recovered) is np.ndarray
        assert not recovered.flags.writeable
    response_map = fixture.cell_expected.response_map
    assert response_map is not None
    assert _fit_hashes(
        loaded_base.panel,
        loaded_cell.panel,
        contract=fixture.contract,
        response_map=response_map,
    ) == _fit_hashes(
        fixture.base,
        fixture.cell,
        contract=fixture.contract,
        response_map=response_map,
    )
    forged_loaded_base = replace(loaded_base.panel)
    with pytest.raises(ValueError, match="issued|builder"):
        aggregate_contract_smooth_moments(
            forged_loaded_base,
            loaded_cell.panel,
            np.ones(48, dtype=np.float64),
        )


def test_fresh_process_loads_and_fits_with_all_rng_draws_blocked(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    _publish_pair(tmp_path, fixture)
    response_map = fixture.cell_expected.response_map
    assert response_map is not None
    expected_hashes = _fit_hashes(
        fixture.base,
        fixture.cell,
        contract=fixture.contract,
        response_map=response_map,
    )
    script = """
import hashlib
import json
from pathlib import Path
import numpy as np

from xid.models.g2_checkpoint import G2PanelCheckpointExpectation
from xid.models.g2_smooth import (
    G2FlowView,
    aggregate_contract_smooth_moments,
    fit_condition_ridge,
    fit_homogeneous_ols,
    load_contract_base_panel_checkpoint,
    load_contract_cell_panel_checkpoint,
)
from xid.sim.g2 import G2ResponseMapIdentity, G2Stream, TestRngNamespace, load_g2_contract
import xid.models.g2_checkpoint as checkpoint_codec
from xid.sim.g2 import current_g2_runtime_fingerprint

repo = Path(__import__("sys").argv[1])
checkpoint_root = Path(__import__("sys").argv[2])
contract = load_g2_contract(repo)
authority = TestRngNamespace.from_contract(contract, 1729)
fingerprint = current_g2_runtime_fingerprint()
def forbidden(*args, **kwargs):
    raise AssertionError("checkpoint recovery attempted an RNG draw")
TestRngNamespace.draw_standard_normal = forbidden
TestRngNamespace.draw_bootstrap_weights = forbidden
TestRngNamespace.draw_base_normals = forbidden
checkpoint_codec.current_g2_runtime_fingerprint = lambda: fingerprint
np.random.default_rng = forbidden
np.random.SeedSequence = forbidden
np.random.PCG64DXSM = forbidden
np.random.Generator = forbidden
response = G2ResponseMapIdentity(0, False, contract.confirmatory_ar1, 0.95)
base_expected = G2PanelCheckpointExpectation(
    1729, G2Stream.VALIDATION_DATE_FRONTIER, 48, 0, None
)
cell_expected = G2PanelCheckpointExpectation(
    1729, G2Stream.VALIDATION_DATE_FRONTIER, 48, 0, response
)
base = load_contract_base_panel_checkpoint(
    checkpoint_root,
    expected=base_expected,
    authority=authority,
    contract=contract,
    repository_root=repo,
)
cell = load_contract_cell_panel_checkpoint(
    checkpoint_root,
    base_checkpoint=base,
    expected=cell_expected,
    authority=authority,
    contract=contract,
    repository_root=repo,
)
aggregate = aggregate_contract_smooth_moments(
    base.panel, cell.panel, np.ones(48, dtype=np.float64)
)
def digest(values):
    return hashlib.sha256(values.astype("<f8", copy=False).tobytes(order="C")).hexdigest()
out = {
    "oracle": digest(fit_condition_ridge(
        aggregate,
        flow_view=G2FlowView.ORACLE,
        reliability=0.95,
        expected_response_map=response,
        contract=contract,
    ).coefficients),
    "observable": digest(fit_condition_ridge(
        aggregate,
        flow_view=G2FlowView.OBSERVABLE,
        reliability=0.95,
        expected_response_map=response,
        contract=contract,
    ).coefficients),
    "homogeneous": digest(fit_homogeneous_ols(
        aggregate,
        reliability=0.95,
        expected_response_map=response,
        contract=contract,
    ).slopes),
}
print(json.dumps(out, sort_keys=True))
"""
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(_root() / "src")
    completed = subprocess.run(
        [sys.executable, "-c", script, str(_root()), str(tmp_path)],
        cwd=_root(),
        env=environment,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert json.loads(completed.stdout) == expected_hashes


def test_writers_refuse_copied_or_hand_built_panels(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    forged_base = replace(fixture.base)
    with pytest.raises(ValueError, match="issued|builder"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            forged_base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )
    base_evidence = _publish_base(tmp_path, fixture)
    forged_evidence = replace(base_evidence, artifact_sha256="0" * 64)
    with pytest.raises(ValueError, match="base|artifact|evidence|SHA256"):
        write_contract_cell_panel_checkpoint(
            tmp_path,
            fixture.base,
            fixture.cell,
            base_checkpoint=forged_evidence,
            expected=fixture.cell_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )
    forged_cell = replace(fixture.cell)
    with pytest.raises(ValueError, match="issued|builder"):
        write_contract_cell_panel_checkpoint(
            tmp_path,
            fixture.base,
            forged_cell,
            base_checkpoint=base_evidence,
            expected=fixture.cell_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )


def test_direct_codec_writer_cannot_mint_authority_from_a_copied_panel(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    forged = replace(fixture.base)

    with pytest.raises(ValueError, match="issued|builder|panel|authority"):
        checkpoint_codec._write_base_artifact(
            tmp_path,
            expected=fixture.base_expected,
            contract=fixture.contract,
            authority=fixture.namespace,
            repository_root=_root(),
            telemetry=_telemetry(),
            panel=forged,
        )


@pytest.mark.parametrize(
    "case",
    [
        "missing_manifest",
        "missing_success",
        "missing_payload",
        "extra_file",
        "payload_symlink",
        "payload_hardlink",
        "raw_manifest_tamper",
        "raw_payload_tamper",
        "raw_success_tamper",
        "noncanonical_manifest",
        "duplicate_manifest_key",
        "extra_manifest_key",
        "oversized_manifest",
    ],
)
def test_loader_rejects_filesystem_and_json_faults(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    case: str,
) -> None:
    fixture = issued_fixture
    evidence = _publish_base(tmp_path, fixture)
    artifact = evidence.artifact_path
    payload = artifact / "x0tx0_upper.npy"
    if case == "missing_manifest":
        (artifact / "manifest.json").unlink()
    elif case == "missing_success":
        (artifact / "_SUCCESS").unlink()
    elif case == "missing_payload":
        payload.unlink()
    elif case == "extra_file":
        (artifact / "unexpected.txt").write_text("unexpected", encoding="utf-8")
    elif case == "payload_symlink":
        external = tmp_path / "external.npy"
        external.write_bytes(payload.read_bytes())
        payload.unlink()
        payload.symlink_to(external)
    elif case == "payload_hardlink":
        external = tmp_path / "external.npy"
        payload.rename(external)
        os.link(external, payload)
    elif case == "raw_manifest_tamper":
        manifest_path = artifact / "manifest.json"
        manifest_path.write_bytes(manifest_path.read_bytes() + b"tamper")
    elif case == "raw_payload_tamper":
        payload_bytes = bytearray(payload.read_bytes())
        payload_bytes[-1] ^= 1
        payload.write_bytes(payload_bytes)
    elif case == "raw_success_tamper":
        success_path = artifact / "_SUCCESS"
        success_path.write_bytes(success_path.read_bytes() + b"tamper")
    elif case == "noncanonical_manifest":
        manifest = _read_manifest(artifact)
        noncanonical = json.dumps(manifest, indent=2, sort_keys=False).encode() + b"\n"
        (artifact / "manifest.json").write_bytes(noncanonical)
        payload_pairs = [[item["name"], item["sha256"]] for item in manifest["payloads"]]
        _write_success_for_manifest_bytes(
            artifact,
            manifest_bytes=noncanonical,
            kind=manifest["artifact_kind"],
            payload_pairs=payload_pairs,
        )
    elif case == "duplicate_manifest_key":
        manifest = _read_manifest(artifact)
        canonical = _canonical_bytes(manifest)
        duplicate = b'{"schema_version":1,' + canonical[1:]
        (artifact / "manifest.json").write_bytes(duplicate)
        payload_pairs = [[item["name"], item["sha256"]] for item in manifest["payloads"]]
        _write_success_for_manifest_bytes(
            artifact,
            manifest_bytes=duplicate,
            kind=manifest["artifact_kind"],
            payload_pairs=payload_pairs,
        )
    elif case == "extra_manifest_key":
        manifest = _read_manifest(artifact)
        manifest["unexpected"] = True
        _resign_manifest(artifact, manifest)
    elif case == "oversized_manifest":
        manifest = _read_manifest(artifact)
        manifest["padding"] = "x" * (1024 * 1024)
        oversized = _canonical_bytes(manifest)
        (artifact / "manifest.json").write_bytes(oversized)
        payload_pairs = [[item["name"], item["sha256"]] for item in manifest["payloads"]]
        _write_success_for_manifest_bytes(
            artifact,
            manifest_bytes=oversized,
            kind=manifest["artifact_kind"],
            payload_pairs=payload_pairs,
        )
    else:
        raise AssertionError(f"unhandled test case {case}")
    with pytest.raises(
        (OSError, ValueError),
        match="checkpoint|payload|file|JSON|link|success|manifest|canonical|size|hash",
    ):
        _load_base(tmp_path, fixture)


@pytest.mark.parametrize(
    "case",
    [
        "big_endian",
        "float32",
        "fortran_order",
        "wrong_shape",
        "nonfinite",
        "trailing_bytes",
        "oversized_header",
        "version_2",
    ],
)
def test_loader_rejects_npy_contract_faults(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    case: str,
) -> None:
    fixture = issued_fixture
    evidence = _publish_base(tmp_path, fixture)
    artifact = evidence.artifact_path
    original = fixture.base.x0tx0_upper
    name = "x0tx0_upper.npy"
    if case == "big_endian":
        values = original.astype(">f8")
        payload = _npy_bytes(values)
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=payload,
            dtype=">f8",
            shape=values.shape,
            data_bytes=values.nbytes,
        )
    elif case == "float32":
        values = original.astype("<f4")
        payload = _npy_bytes(values)
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=payload,
            dtype="<f4",
            shape=values.shape,
            data_bytes=values.nbytes,
        )
    elif case == "fortran_order":
        values = np.asfortranarray(original)
        payload = _npy_bytes(values)
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=payload,
            dtype="<f8",
            shape=values.shape,
            data_bytes=values.nbytes,
        )
    elif case == "wrong_shape":
        values = original[:-1]
        payload = _npy_bytes(values)
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=payload,
            dtype="<f8",
            shape=values.shape,
            data_bytes=values.nbytes,
        )
    elif case == "nonfinite":
        values = original.copy()
        values[0, 0] = np.nan
        payload = _npy_bytes(values)
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=payload,
            dtype="<f8",
            shape=values.shape,
            data_bytes=values.nbytes,
        )
    elif case == "trailing_bytes":
        valid = (artifact / name).read_bytes()
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=valid + b"trailing",
            dtype="<f8",
            shape=original.shape,
            data_bytes=original.nbytes,
        )
    elif case == "oversized_header":
        valid = (artifact / name).read_bytes()
        oversized = _oversized_header_npy(valid)
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=oversized,
            dtype="<f8",
            shape=original.shape,
            data_bytes=original.nbytes,
        )
    elif case == "version_2":
        output = io.BytesIO()
        np.lib.format.write_array(
            output,
            original,
            version=(2, 0),
            allow_pickle=False,
        )
        payload = output.getvalue()
        _replace_payload(
            artifact,
            name=name,
            payload_bytes=payload,
            dtype="<f8",
            shape=original.shape,
            data_bytes=original.nbytes,
            npy_format="2.0",
        )
    else:
        raise AssertionError(f"unhandled test case {case}")
    with pytest.raises(ValueError, match="NPY|dtype|endian|order|shape|finite|header|trailing"):
        _load_base(tmp_path, fixture)


@pytest.mark.parametrize(
    "case",
    [
        "seal",
        "source",
        "runtime",
        "address_seed",
        "completion",
        "design_map",
        "date_order",
        "receipt_order",
        "telemetry",
        "kind",
        "stream",
        "phase",
        "scenario",
        "n_dates",
        "panel_index",
        "replicate_index",
        "manifest_schema_float",
        "contract_config_schema_float",
        "contract_rng_schema_float",
        "address_seed_float",
        "address_config_schema_float",
        "address_rng_schema_float",
        "address_component_float",
        "completion_float",
        "design_digest",
        "duplicate_date",
        "incomplete_dates",
    ],
)
def test_loader_rejects_self_consistent_manifest_identity_faults(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    case: str,
) -> None:
    fixture = issued_fixture
    evidence = _publish_base(tmp_path, fixture)
    artifact = evidence.artifact_path
    manifest = _read_manifest(artifact)
    if case == "seal":
        manifest["contract"]["seals"]["config_sha256"] = "0" * 64
    elif case == "source":
        manifest["execution_source"]["snapshot_sha256"] = "0" * 64
    elif case == "runtime":
        manifest["runtime"]["runtime_sha256"] = "0" * 64
    elif case == "address_seed":
        manifest["address"]["master_seed"] = 42
    elif case == "completion":
        manifest["completion"]["completed_date_range"] = [0, 47]
    elif case == "design_map":
        manifest["design_response_map"]["target_index"] = 0
    elif case == "date_order":
        manifest["date_indices"][0], manifest["date_indices"][1] = (
            manifest["date_indices"][1],
            manifest["date_indices"][0],
        )
    elif case == "receipt_order":
        manifest["source_receipts"][1] = dict(manifest["source_receipts"][0])
    elif case == "telemetry":
        manifest["telemetry"]["peak_rss_bytes"] = -1
    elif case == "kind":
        manifest["artifact_kind"] = "cell-panel"
    elif case == "stream":
        manifest["address"]["stream"] = G2Stream.VALIDATION_RECOVERY.value
    elif case == "phase":
        manifest["address"]["phase_id"] += 1
    elif case == "scenario":
        manifest["address"]["scenario_id"] += 1
    elif case == "n_dates":
        manifest["address"]["n_dates"] = 96
    elif case == "panel_index":
        manifest["address"]["panel_index"] = 1
    elif case == "replicate_index":
        manifest["address"]["replicate_index"] = 1
    elif case == "manifest_schema_float":
        manifest["schema_version"] = 1.0
    elif case == "contract_config_schema_float":
        manifest["contract"]["config_schema_version"] = float(
            manifest["contract"]["config_schema_version"]
        )
    elif case == "contract_rng_schema_float":
        manifest["contract"]["rng_key_schema_version"] = float(
            manifest["contract"]["rng_key_schema_version"]
        )
    elif case == "address_seed_float":
        manifest["address"]["master_seed"] = float(manifest["address"]["master_seed"])
    elif case == "address_config_schema_float":
        manifest["address"]["config_schema_version"] = float(
            manifest["address"]["config_schema_version"]
        )
    elif case == "address_rng_schema_float":
        manifest["address"]["rng_key_schema_version"] = float(
            manifest["address"]["rng_key_schema_version"]
        )
    elif case == "address_component_float":
        manifest["address"]["component_ids"][0] = 1.0
    elif case == "completion_float":
        manifest["completion"]["completed_date_range"][0] = 0.0
    elif case == "design_digest":
        manifest["design_sha256s"][0] = "0" * 64
    elif case == "duplicate_date":
        manifest["date_indices"][1] = 0
    elif case == "incomplete_dates":
        manifest["date_indices"].pop()
        manifest["source_receipts"].pop()
        manifest["design_sha256s"].pop()
    else:
        raise AssertionError(f"unhandled test case {case}")
    _resign_manifest(artifact, manifest)
    with pytest.raises(
        ValueError,
        match=(
            "contract|source|runtime|seed|range|map|date|receipt|RSS|kind|stream|"
            "phase|scenario|panel|replicate|digest|complete|schema|integer|type"
        ),
    ):
        _load_base(tmp_path, fixture)


@pytest.mark.parametrize("schema_version", [1.0, True])
def test_loader_rejects_self_consistent_success_schema_type_aliases(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    schema_version: object,
) -> None:
    fixture = issued_fixture
    evidence = _publish_base(tmp_path, fixture)
    success_path = evidence.artifact_path / "_SUCCESS"
    success = json.loads(success_path.read_bytes())
    success["schema_version"] = schema_version
    success_path.write_bytes(_canonical_bytes(success))

    with pytest.raises(ValueError, match="success|schema|integer|identity"):
        _load_base(tmp_path, fixture)


@pytest.mark.parametrize("missing_name", ["x0ty.npy", "yty_upper.npy"])
def test_cell_loader_rejects_either_missing_payload(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    missing_name: str,
) -> None:
    fixture = issued_fixture
    _base_evidence, cell_evidence = _publish_pair(tmp_path, fixture)
    (cell_evidence.artifact_path / missing_name).unlink()
    loaded_base = _load_base(tmp_path, fixture)
    with pytest.raises(ValueError, match="payload|file|checkpoint"):
        load_contract_cell_panel_checkpoint(
            tmp_path,
            base_checkpoint=loaded_base,
            expected=fixture.cell_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
        )


def test_cell_loader_rejects_parent_response_and_mixed_coordinate_faults(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    _base_evidence, cell_evidence = _publish_pair(tmp_path, fixture)
    manifest = _read_manifest(cell_evidence.artifact_path)
    manifest["parent"]["base_artifact_sha256"] = "0" * 64
    _resign_manifest(cell_evidence.artifact_path, manifest)
    loaded_base = _load_base(tmp_path, fixture)
    with pytest.raises(ValueError, match="parent|base"):
        load_contract_cell_panel_checkpoint(
            tmp_path,
            base_checkpoint=loaded_base,
            expected=fixture.cell_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
        )

    token_root = tmp_path / "parent-token"
    _token_base, token_cell = _publish_pair(token_root, fixture)
    token_manifest = _read_manifest(token_cell.artifact_path)
    token_manifest["parent"]["base_panel_token"] = "0" * 64
    _resign_manifest(token_cell.artifact_path, token_manifest)
    loaded_token_base = _load_base(token_root, fixture)
    with pytest.raises(ValueError, match="parent|base|token"):
        load_contract_cell_panel_checkpoint(
            token_root,
            base_checkpoint=loaded_token_base,
            expected=fixture.cell_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
        )

    digest_root = tmp_path / "design-digest"
    _digest_base, digest_cell = _publish_pair(digest_root, fixture)
    digest_manifest = _read_manifest(digest_cell.artifact_path)
    digest_manifest["design_sha256s"][0] = "0" * 64
    _resign_manifest(digest_cell.artifact_path, digest_manifest)
    loaded_digest_base = _load_base(digest_root, fixture)
    with pytest.raises(ValueError, match="design|digest|base"):
        load_contract_cell_panel_checkpoint(
            digest_root,
            base_checkpoint=loaded_digest_base,
            expected=fixture.cell_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
        )

    relabeled_root = tmp_path / "relabeled"
    _clean_base, clean_cell = _publish_pair(relabeled_root, fixture)
    response_map = fixture.cell_expected.response_map
    assert response_map is not None
    wrong_response = replace(
        response_map,
        target_index=1,
    )
    wrong_expected = replace(fixture.cell_expected, response_map=wrong_response)
    response_payload = [
        wrong_response.target_index,
        wrong_response.paper_recovery,
        wrong_response.phi.hex(),
        wrong_response.reliability.hex(),
    ]
    wrong_map_sha = _sha256(_canonical_bytes(response_payload))
    cell_relative = clean_cell.artifact_path.relative_to(relabeled_root)
    cell_name = cell_relative.name
    prefix, parent = cell_name.split("-parent-", maxsplit=1)
    assert prefix.startswith("cell-")
    wrong_cell = relabeled_root / cell_relative.with_name(f"cell-{wrong_map_sha}-parent-{parent}")
    wrong_cell.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(clean_cell.artifact_path, wrong_cell)
    loaded_base_copy = load_contract_base_panel_checkpoint(
        relabeled_root,
        expected=fixture.base_expected,
        authority=fixture.namespace,
        contract=fixture.contract,
        repository_root=_root(),
    )
    with pytest.raises(ValueError, match="response|map|identity"):
        load_contract_cell_panel_checkpoint(
            relabeled_root,
            base_checkpoint=loaded_base_copy,
            expected=wrong_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
        )


def test_loader_rejects_internal_identity_copied_to_wrong_coordinate(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    evidence = _publish_base(tmp_path, fixture)
    wrong_expected = replace(fixture.base_expected, panel_index=1)
    relative = evidence.artifact_path.relative_to(tmp_path)
    parts = list(relative.parts)
    panel_position = next(index for index, part in enumerate(parts) if part.startswith("panel-"))
    parts[panel_position] = "panel-0000000001"
    wrong_artifact = tmp_path.joinpath(*parts)
    wrong_artifact.parent.mkdir(parents=True)
    shutil.copytree(evidence.artifact_path, wrong_artifact)
    with pytest.raises(ValueError, match="panel|identity|address"):
        load_contract_base_panel_checkpoint(
            tmp_path,
            expected=wrong_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
        )


@pytest.mark.parametrize("master_seed", [42, 2026071529, 2026071521, 2026071522])
def test_loader_refuses_unlicensed_seed_before_filesystem_access(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    master_seed: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    expected = replace(fixture.base_expected, master_seed=master_seed)
    real_root = tmp_path / "real"
    real_root.mkdir()
    deceptive_root = tmp_path / "linked"
    deceptive_root.symlink_to(real_root, target_is_directory=True)
    if master_seed in fixture.contract.registered_seeds:
        authority = object.__new__(TestRngNamespace)
        object.__setattr__(authority, "contract", fixture.contract)
        object.__setattr__(authority, "master_seed", master_seed)
    else:
        authority = TestRngNamespace.from_contract(fixture.contract, master_seed)

    def forbidden(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise AssertionError("unlicensed checkpoint preflight reached RNG")

    monkeypatch.setattr(TestRngNamespace, "draw_standard_normal", forbidden)
    monkeypatch.setattr(TestRngNamespace, "draw_bootstrap_weights", forbidden)
    monkeypatch.setattr(TestRngNamespace, "draw_base_normals", forbidden)
    monkeypatch.setattr(np.random, "default_rng", forbidden)
    monkeypatch.setattr(np.random, "SeedSequence", forbidden)
    monkeypatch.setattr(np.random, "PCG64DXSM", forbidden)
    monkeypatch.setattr(np.random, "Generator", forbidden)
    with pytest.raises(ValueError, match="registered|licensed test seed"):
        load_contract_base_panel_checkpoint(
            deceptive_root,
            expected=expected,
            authority=authority,
            contract=fixture.contract,
            repository_root=_root(),
        )


def test_runtime_environment_change_invalidates_checkpoint(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    _publish_base(tmp_path, fixture)
    current = os.environ.get("OMP_NUM_THREADS")
    changed = "17" if current != "17" else "19"
    monkeypatch.setenv("OMP_NUM_THREADS", changed)
    with pytest.raises(ValueError, match="runtime|thread"):
        _load_base(tmp_path, fixture)


def test_publication_is_immutable_invalid_existing_is_not_repaired_and_lock_blocks(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    evidence = _publish_base(tmp_path, fixture)
    original_manifest = (evidence.artifact_path / "manifest.json").read_bytes()
    (evidence.artifact_path / "_SUCCESS").write_text("invalid", encoding="utf-8")
    with pytest.raises(FileExistsError, match="exists|immutable"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )
    assert (evidence.artifact_path / "manifest.json").read_bytes() == original_manifest

    locked_root = tmp_path / "locked"
    locked_root.mkdir()
    (locked_root / ".xid-g2-checkpoint.lock").write_text("stale", encoding="utf-8")
    with pytest.raises(FileExistsError, match="lock|writer"):
        write_contract_base_panel_checkpoint(
            locked_root,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )


def test_loader_refuses_valid_artifact_while_root_lock_exists(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    _publish_base(tmp_path, fixture)
    (tmp_path / ".xid-g2-checkpoint.lock").write_text("stale", encoding="utf-8")

    with pytest.raises(FileExistsError, match="lock|writer"):
        _load_base(tmp_path, fixture)


def test_handled_publish_failure_leaves_no_final_stage_or_lock(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture

    def fail_rename(source: object, destination: object, *args: object, **kwargs: object) -> None:
        del source, destination, args, kwargs
        raise OSError("injected rename failure")

    monkeypatch.setattr("xid.models.g2_checkpoint.os.rename", fail_rename)
    with pytest.raises(OSError, match="injected"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )
    assert not (tmp_path / ".xid-g2-checkpoint.lock").exists()
    assert not any(".stage-" in path.name for path in tmp_path.rglob("*"))
    assert not any(path.name.startswith("base-") for path in tmp_path.rglob("*"))


def test_source_change_while_loading_contract_aborts_without_lock_or_publication(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    original_source_snapshot = checkpoint_codec._source_snapshot
    original_load_contract = cast(Any, checkpoint_codec).load_g2_contract
    initial = original_source_snapshot(_root())
    contract_load_completed = False

    def changing_source_snapshot(repository_root: Path) -> Any:
        if not contract_load_completed:
            return initial
        return replace(initial, snapshot_sha256="0" * 64)

    def tracked_load_contract(repository_root: Path) -> G2Contract:
        nonlocal contract_load_completed
        result = original_load_contract(repository_root)
        contract_load_completed = True
        return cast(G2Contract, result)

    monkeypatch.setattr(
        checkpoint_codec,
        "_source_snapshot",
        changing_source_snapshot,
    )
    monkeypatch.setattr(
        checkpoint_codec,
        "load_g2_contract",
        tracked_load_contract,
    )
    with pytest.raises(ValueError, match="source changed|execution source"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )

    assert contract_load_completed
    assert not (tmp_path / ".xid-g2-checkpoint.lock").exists()
    assert not any(".stage-" in path.name for path in tmp_path.rglob("*"))
    assert not any(path.name.startswith("base-") for path in tmp_path.rglob("*"))


def test_source_snapshot_binds_the_make_only_recovery_launcher(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository_root = _root()
    observed: list[str] = []
    original_identity = checkpoint_codec._stable_source_file_identity

    def track_source(path: Path) -> Any:
        observed.append(path.relative_to(repository_root).as_posix())
        return original_identity(path)

    monkeypatch.setattr(
        checkpoint_codec,
        "_stable_source_file_identity",
        track_source,
    )

    bound = checkpoint_codec._source_snapshot(repository_root)

    assert "Makefile" in observed

    def alter_makefile_identity(path: Path) -> Any:
        metadata, byte_count, sha256 = original_identity(path)
        if path == repository_root / "Makefile":
            sha256 = "0" * 64 if sha256 != "0" * 64 else "1" * 64
        return metadata, byte_count, sha256

    monkeypatch.setattr(
        checkpoint_codec,
        "_stable_source_file_identity",
        alter_makefile_identity,
    )
    altered = checkpoint_codec._source_snapshot(repository_root)

    assert altered.snapshot_sha256 != bound.snapshot_sha256


def test_source_snapshot_streams_files_without_path_read_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbid_read_bytes(_path: Path) -> bytes:
        raise AssertionError("source snapshot attempted whole-file read_bytes")

    monkeypatch.setattr(Path, "read_bytes", forbid_read_bytes)
    identity = checkpoint_codec._source_snapshot(_root())
    assert len(identity.snapshot_sha256) == 64


def test_runtime_hash_uses_the_frozen_two_object_preimage(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    evidence = _publish_base(tmp_path, issued_fixture)
    runtime = _read_manifest(evidence.artifact_path)["runtime"]
    fingerprint = {
        name: runtime[name]
        for name in (
            "python_implementation",
            "python_version",
            "numpy_version",
            "system",
            "machine",
            "byteorder",
            "rng_runtime_sha256",
        )
    }
    expected = _sha256(_canonical_bytes([fingerprint, runtime["thread_env"]]))
    assert runtime["runtime_sha256"] == expected


def test_loader_bytecode_must_match_a_fresh_source_compilation(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    original_loader = checkpoint_codec.__loader__
    assert original_loader is not None

    class MismatchedLoader:
        def get_code(self, module_name: str) -> object:
            del module_name
            return compile(
                "EXECUTED_FROM_STALE_BYTECODE = True\n",
                str(checkpoint_codec.__file__),
                "exec",
            )

        def source_to_code(self, data: bytes, path: str) -> object:
            return cast(Any, original_loader).source_to_code(data, path)

    monkeypatch.setattr(checkpoint_codec, "__loader__", MismatchedLoader())
    with pytest.raises(ValueError, match="bytecode|executable|source"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )


@pytest.mark.parametrize(
    "module",
    [checkpoint_codec, smooth_model, g2_module],
    ids=["checkpoint", "smooth", "sim"],
)
def test_same_path_stale_import_hash_is_rejected(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
    module: object,
) -> None:
    fixture = issued_fixture
    monkeypatch.setattr(
        module,
        "_XID_LOADED_SOURCE_SHA256",
        "0" * 64,
        raising=False,
    )

    with pytest.raises(ValueError, match="stale|loaded|source|import"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )


def test_post_rename_parent_fsync_failure_retains_lock_and_blocks_loading(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    original_fsync_directory = checkpoint_codec._fsync_directory

    def fail_after_publish(path: Path) -> None:
        if path.name == "panel-0000000000" and any(
            child.name.startswith("base-") for child in path.iterdir()
        ):
            raise OSError("injected post-rename parent fsync failure")
        original_fsync_directory(path)

    monkeypatch.setattr(
        checkpoint_codec,
        "_fsync_directory",
        fail_after_publish,
    )
    with pytest.raises(OSError, match="post-rename"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )

    assert (tmp_path / ".xid-g2-checkpoint.lock").exists()
    assert any(path.name.startswith("base-") for path in tmp_path.rglob("*"))
    with pytest.raises(FileExistsError, match="lock|writer"):
        _load_base(tmp_path, fixture)


@pytest.mark.parametrize("failure_site", ["remove_stage", "fsync_stage_parent"])
def test_uncertain_pre_rename_cleanup_retains_root_lock(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
    failure_site: str,
) -> None:
    fixture = issued_fixture
    rename_failed = False

    def fail_rename(source: object, destination: object, *args: object, **kwargs: object) -> None:
        nonlocal rename_failed
        del source, destination, args, kwargs
        rename_failed = True
        raise OSError("injected rename failure")

    monkeypatch.setattr("xid.models.g2_checkpoint.os.rename", fail_rename)
    if failure_site == "remove_stage":
        monkeypatch.setattr(
            "xid.models.g2_checkpoint.shutil.rmtree",
            lambda _path: (_ for _ in ()).throw(OSError("injected stage removal failure")),
        )
    else:
        original_fsync_directory = checkpoint_codec._fsync_directory

        def fail_cleanup_fsync(path: Path) -> None:
            if rename_failed and path.name == "panel-0000000000":
                raise OSError("injected cleanup fsync failure")
            original_fsync_directory(path)

        monkeypatch.setattr(
            checkpoint_codec,
            "_fsync_directory",
            fail_cleanup_fsync,
        )

    with pytest.raises(OSError, match="stage removal|cleanup fsync"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )

    assert (tmp_path / ".xid-g2-checkpoint.lock").exists()
    with pytest.raises(FileExistsError, match="lock|writer"):
        _load_base(tmp_path, fixture)


def test_root_contract_source_disjointness_and_global_allocation_cap(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    source_root = _root() / "src" / "xid"
    with pytest.raises(ValueError, match="source|disjoint|checkpoint root"):
        load_contract_base_panel_checkpoint(
            source_root,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
        )

    oversized_root = tmp_path / "oversized"
    oversized_root.mkdir()
    with (oversized_root / "sparse.bin").open("wb") as handle:
        handle.truncate(2 * 1024**3 + 1)
    with pytest.raises(ValueError, match="2 GB|allocation|checkpoint"):
        write_contract_base_panel_checkpoint(
            oversized_root,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )


def test_near_cap_root_rejects_projected_stage_before_first_artifact_write(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    with (tmp_path / "near-cap.bin").open("wb") as handle:
        handle.truncate(2 * 1024**3 - 500_000)
    original_write_file = checkpoint_codec._write_file

    def forbid_artifact_write(path: Path, payload: bytes) -> None:
        if path.name != ".xid-g2-checkpoint.lock":
            raise AssertionError("artifact write occurred before projected-cap refusal")
        original_write_file(path, payload)

    monkeypatch.setattr(checkpoint_codec, "_write_file", forbid_artifact_write)
    with pytest.raises(ValueError, match="2 GB|allocation|capacity|cap"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )

    assert not (tmp_path / ".xid-g2-checkpoint.lock").exists()
    assert not any(".stage-" in path.name for path in tmp_path.rglob("*"))


def _set_sparse_tree_logical_usage(root: Path, target: int) -> None:
    padding = root / "logical-cap-padding.bin"
    padding.touch()
    logical, allocated = checkpoint_codec._path_usage(root)
    assert allocated < target
    assert logical <= target
    with padding.open("r+b") as handle:
        handle.truncate(target - logical)
    final_logical, final_allocated = checkpoint_codec._path_usage(root)
    assert final_logical == target
    assert final_allocated < target


def test_root_lock_is_refused_before_any_mutation_when_one_byte_below_cap(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    _set_sparse_tree_logical_usage(tmp_path, checkpoint_codec._MAX_TREE_BYTES - 1)

    def forbid_every_write(path: Path, payload: bytes) -> None:
        del path, payload
        raise AssertionError("lock write occurred before projected-cap refusal")

    monkeypatch.setattr(checkpoint_codec, "_write_file", forbid_every_write)
    with pytest.raises(ValueError, match="2 GB|allocation|capacity|cap"):
        write_contract_base_panel_checkpoint(
            tmp_path,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )

    assert checkpoint_codec._path_usage(tmp_path)[0] == checkpoint_codec._MAX_TREE_BYTES - 1
    assert not (tmp_path / ".xid-g2-checkpoint.lock").exists()
    assert not any(".stage-" in path.name for path in tmp_path.rglob("*"))


def test_stage_reservation_counts_logical_directory_entry_growth(tmp_path: Path) -> None:
    payload = b"0123456789"
    _set_sparse_tree_logical_usage(
        tmp_path,
        checkpoint_codec._MAX_TREE_BYTES - len(payload) - 1,
    )

    with pytest.raises(ValueError, match="2 GB|allocation|capacity|cap"):
        checkpoint_codec._reserve_stage_capacity(tmp_path, (payload,))


def test_late_writer_lock_prevents_loaded_authority_from_being_issued(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    _publish_pair(tmp_path, fixture)
    registry_size = len(smooth_model._CONTRACT_BASE_PANEL_REGISTRY)
    original_assert_context_stable = checkpoint_codec._assert_context_stable

    def inject_lock_after_context_check(context: object) -> None:
        original_assert_context_stable(cast(Any, context))
        (tmp_path / ".xid-g2-checkpoint.lock").write_bytes(b"injected late writer")

    monkeypatch.setattr(
        checkpoint_codec,
        "_assert_context_stable",
        inject_lock_after_context_check,
    )
    with pytest.raises(FileExistsError, match="lock|writer"):
        _load_base(tmp_path, fixture)

    assert len(smooth_model._CONTRACT_BASE_PANEL_REGISTRY) == registry_size


def test_guard_exit_marker_revokes_just_issued_loaded_authority(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    _publish_pair(tmp_path, fixture)
    registry_keys = set(smooth_model._CONTRACT_BASE_PANEL_REGISTRY)
    original_require_no_root_lock = checkpoint_codec._require_no_root_lock
    check_count = 0

    def inject_marker_at_guard_exit(root: Path) -> None:
        nonlocal check_count
        check_count += 1
        if check_count == 4:
            (root / ".xid-g2-checkpoint.lock").write_bytes(b"injected at guard exit")
        original_require_no_root_lock(root)

    monkeypatch.setattr(
        checkpoint_codec,
        "_require_no_root_lock",
        inject_marker_at_guard_exit,
    )
    with pytest.raises(FileExistsError, match="lock|writer"):
        _load_base(tmp_path, fixture)

    assert check_count == 4
    assert set(smooth_model._CONTRACT_BASE_PANEL_REGISTRY) == registry_keys


def test_shared_loader_lease_blocks_cooperative_writer_through_authority_issue(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    _publish_base(tmp_path, fixture)
    original_assert_context_stable = checkpoint_codec._assert_context_stable
    writer_was_blocked = False

    def attempt_writer_while_loader_is_live(context: object) -> None:
        nonlocal writer_was_blocked
        original_assert_context_stable(cast(Any, context))
        with pytest.raises(FileExistsError, match="reader.*lease"):
            write_contract_base_panel_checkpoint(
                tmp_path,
                fixture.base,
                expected=fixture.base_expected,
                authority=fixture.namespace,
                contract=fixture.contract,
                repository_root=_root(),
                telemetry=_telemetry(),
            )
        writer_was_blocked = True

    monkeypatch.setattr(
        checkpoint_codec,
        "_assert_context_stable",
        attempt_writer_while_loader_is_live,
    )
    loaded = _load_base(tmp_path, fixture)

    assert writer_was_blocked
    assert loaded.panel.source_receipts == fixture.base.source_receipts
    assert np.array_equal(loaded.panel.x0tx0_upper, fixture.base.x0tx0_upper)
    assert not (tmp_path / ".xid-g2-checkpoint.lock").exists()


def test_symlink_root_and_stale_import_binding_are_refused(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = issued_fixture
    real_root = tmp_path / "real"
    real_root.mkdir()
    linked_root = tmp_path / "linked"
    linked_root.symlink_to(real_root, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink|root"):
        write_contract_base_panel_checkpoint(
            linked_root,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )

    monkeypatch.setattr(checkpoint_codec, "__file__", str(tmp_path / "stale.py"))
    with pytest.raises(ValueError, match="import|module|repository"):
        write_contract_base_panel_checkpoint(
            real_root,
            fixture.base,
            expected=fixture.base_expected,
            authority=fixture.namespace,
            contract=fixture.contract,
            repository_root=_root(),
            telemetry=_telemetry(),
        )


def test_loaded_authority_survives_only_while_loaded_wrapper_is_live(
    tmp_path: Path,
    issued_fixture: _IssuedFixture,
) -> None:
    fixture = issued_fixture
    _publish_pair(tmp_path, fixture)
    loaded_base = _load_base(tmp_path, fixture)
    loaded_cell = load_contract_cell_panel_checkpoint(
        tmp_path,
        base_checkpoint=loaded_base,
        expected=fixture.cell_expected,
        authority=fixture.namespace,
        contract=fixture.contract,
        repository_root=_root(),
    )
    base_reference = weakref.ref(loaded_base.panel)
    cell_reference = weakref.ref(loaded_cell.panel)
    del loaded_cell
    del loaded_base
    gc.collect()
    assert base_reference() is None
    assert cell_reference() is None
