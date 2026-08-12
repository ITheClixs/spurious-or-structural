from __future__ import annotations

import json
import subprocess
import sys
from itertools import pairwise
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
GENERATED = ROOT / "docs" / "pre_results" / "generated"
ARTIFACTS = (
    "exhibits.json",
    "fig_bounds.tex",
    "fig_diagnostic.tex",
    "fig_psi_study.tex",
)


def _payload() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((GENERATED / "exhibits.json").read_text())
    return loaded


def test_generated_artifacts_are_committed() -> None:
    for name in ARTIFACTS:
        assert (GENERATED / name).is_file(), name


def _generate(into: Path) -> None:
    subprocess.run(
        [sys.executable, "-m", "xid.exhibits", "--out", str(into)],
        check=True,
        cwd=ROOT,
    )


def test_exhibits_regenerate_byte_identically(tmp_path: Path) -> None:
    """The generator is deterministic: two runs agree byte for byte."""
    import shutil

    first, second = tmp_path / "a", tmp_path / "b"
    for target in (first, second):
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy(GENERATED / "psi_study.json", target / "psi_study.json")
    _generate(first)
    _generate(second)
    for name in ARTIFACTS:
        assert (first / name).read_bytes() == (second / name).read_bytes(), name


def _walk(node: Any, path: str = "") -> list[tuple[str, float]]:
    if isinstance(node, bool):
        return []
    if isinstance(node, int | float):
        return [(path, float(node))]
    if isinstance(node, dict):
        return [kv for k, v in node.items() for kv in _walk(v, f"{path}.{k}")]
    if isinstance(node, list):
        return [kv for i, v in enumerate(node) for kv in _walk(v, f"{path}[{i}]")]
    return []


def test_committed_exhibits_match_regeneration_within_tolerance(
    tmp_path: Path,
) -> None:
    """Committed values must survive a rebuild on any supported platform.

    Byte identity is not portable, because LAPACK builds differ in the last
    bits of an eigen- or singular-value decomposition. Numerical agreement is
    the property that actually protects the manuscript, so it is asserted
    separately and with a declared tolerance.
    """
    _generate(tmp_path)
    fresh = dict(_walk(json.loads((tmp_path / "exhibits.json").read_text())))
    committed = dict(_walk(json.loads((GENERATED / "exhibits.json").read_text())))
    assert fresh.keys() == committed.keys()
    for key, want in committed.items():
        got = fresh[key]
        scale = max(abs(want), 1.0)
        assert abs(got - want) / scale < 1e-8, f"{key}: {got} vs {want}"


def test_exhibit_keys_are_complete() -> None:
    payload = _payload()
    for key in (
        "gap_ranks",
        "spurious_offdiag_max",
        "own_impact_min",
        "own_impact_max",
        "sharp_intervals",
        "psi_null",
        "psi_curve",
        "psi_by_factor_count",
        "published_pairwise_correlation",
        "scope",
    ):
        assert key in payload, key


def test_gap_ranks_match_the_registered_prediction() -> None:
    rows = {row["rank_b"]: row for row in _payload()["gap_ranks"]}
    assert rows[0]["observed_rank"] == 3
    assert rows[1]["observed_rank"] == 4
    assert rows[2]["observed_rank"] == 5
    assert rows[30]["observed_rank"] == 30
    for row in rows.values():
        assert row["observed_rank"] <= row["bound"]


def test_spurious_offdiagonal_is_same_order_as_own_impact() -> None:
    """The headline claim: zero true cross-impact, realistic spurious magnitude."""
    payload = _payload()
    assert payload["spurious_offdiag_max"] > 0.5 * payload["own_impact_min"]
    assert payload["own_impact_min"] >= 0.2
    assert payload["own_impact_max"] <= 0.4


def test_sharp_intervals_contain_zero_at_both_registered_endpoints() -> None:
    intervals = _payload()["sharp_intervals"]
    assert len(intervals) == 2
    for row in intervals:
        assert row["lower"] < 0.0 < row["upper"]
        assert row["lower"] < row["truth"] < row["upper"]
        assert row["contains_zero"] is True


def test_identified_halfwidth_dwarfs_the_observed_coefficient() -> None:
    upper = next(r for r in _payload()["sharp_intervals"] if r["truth"] == 0.0046)
    assert upper["halfwidth_over_observed"] > 7.0


def test_psi_curve_is_strictly_increasing_from_a_numerical_zero() -> None:
    curve = _payload()["psi_curve"]
    assert curve[0]["epsilon"] == 0.0
    assert curve[0]["psi"] == 0.0
    values = [row["psi"] for row in curve]
    assert all(a < b for a, b in pairwise(values)), values


def test_psi_null_is_reported_as_an_exact_analytic_zero() -> None:
    """Proposition 5 makes this exactly zero; noise below the floor is clamped."""
    payload = _payload()
    assert payload["psi_null"] == 0.0
    assert payload["numerical_zero_floor"] == 1e-12


def test_psi_by_factor_count_has_an_elbow_at_the_true_factor_count() -> None:
    """Understating K inflates the statistic; the elbow locates the true count."""
    rows = {row["k"]: row["psi"] for row in _payload()["psi_by_factor_count"]}
    assert rows[1] > 10.0 * rows[3]
    assert rows[2] > 5.0 * rows[3]
    assert rows[4] < rows[3]


def test_scope_label_disclaims_any_market_estimate() -> None:
    assert "not an estimate of any market" in _payload()["scope"]


def test_figure_fragments_define_the_macros_the_manuscript_inputs() -> None:
    bounds = (GENERATED / "fig_bounds.tex").read_text()
    diagnostic = (GENERATED / "fig_diagnostic.tex").read_text()
    for macro in ("\\FigBoundsUpper", "\\FigBoundsLower", "\\FigBoundsObserved"):
        assert macro in bounds, macro
    for macro in ("\\FigPsiCurve", "\\FigPsiByFactorCount"):
        assert macro in diagnostic, macro
    study_fig = (GENERATED / "fig_psi_study.tex").read_text()
    for macro in ("\\FigPsiSize", "\\FigPsiPower"):
        assert macro in study_fig, macro


def test_published_control_shift_block_records_the_source_figures() -> None:
    block = _payload()["published_control_shift"]
    assert block["cross_mean_before"] == 0.032
    assert block["cross_mean_after"] == -0.039
    assert abs(block["cross_mean_shift"] - (-0.071)) < 1e-12
    assert block["cross_sd_before"] == 0.06
    assert block["cross_sd_after"] == 0.06


def test_rank_one_predicts_the_observed_dispersion_invariance() -> None:
    """A constant shift moves the mean and leaves the cross-sectional SD fixed."""
    block = _payload()["published_control_shift"]
    assert block["predicted_sd_change"] == 0.0
    assert abs(block["cross_sd_change"]) <= block["reporting_precision"]
    assert block["sd_invariance_consistent"] is True


def test_negative_fraction_check_is_reported_even_though_it_disagrees() -> None:
    """The weaker shape check under-predicts; the paper must say so."""
    block = _payload()["published_control_shift"]
    assert "negative_fraction_after_reported" in block
    assert "negative_fraction_after_predicted_normal" in block
    assert block["negative_fraction_shape_consistent"] is False


def test_published_block_carries_the_scope_disclaimer() -> None:
    assert "not an estimate of any market" in _payload()["published_control_shift"]["scope"]
