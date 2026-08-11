from __future__ import annotations

import json
import subprocess
import sys
from itertools import pairwise
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
GENERATED = ROOT / "docs" / "pre_results" / "generated"
ARTIFACTS = ("exhibits.json", "fig_bounds.tex", "fig_diagnostic.tex")


def _payload() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((GENERATED / "exhibits.json").read_text())
    return loaded


def test_generated_artifacts_are_committed() -> None:
    for name in ARTIFACTS:
        assert (GENERATED / name).is_file(), name


def test_exhibits_regenerate_byte_identically(tmp_path: Path) -> None:
    """Every manuscript number must come back identical from committed code."""
    for _ in range(2):
        subprocess.run(
            [sys.executable, "-m", "xid.exhibits", "--out", str(tmp_path)],
            check=True,
            cwd=ROOT,
        )
    for name in ARTIFACTS:
        assert (tmp_path / name).read_bytes() == (GENERATED / name).read_bytes(), name


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
    assert curve[0]["psi"] < 1e-12
    values = [row["psi"] for row in curve]
    assert all(a < b for a, b in pairwise(values)), values


def test_psi_null_is_numerically_zero() -> None:
    assert _payload()["psi_null"] < 1e-12


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
