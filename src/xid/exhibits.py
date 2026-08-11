"""Deterministic generator for every quantitative exhibit in the preprint.

Running ``python -m xid.exhibits --out DIR`` writes ``exhibits.json`` plus the
TikZ coordinate fragments the manuscript inputs. The output is byte-identical
on repeat, so no number in the paper is typed by hand.

Randomness is limited to test seed ``1729`` and its companion ``9191``, used
only to draw deterministic algebraic fixtures. This module opens no registered
stream, reads no market data, and makes no claim about any real market.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from xid.models.identification import (
    confounding_gap,
    gap_rank_bound,
    numerical_rank,
    one_spike_eigenvalues,
    one_spike_gap_per_entry,
    sharp_offdiag_interval,
)
from xid.models.rank_diagnostic import psi_k

Matrix = NDArray[np.float64]

N_ASSETS = 30
N_FACTORS = 3
FIXTURE_SEED = 1729
PERTURBATION_SEED = 9191

# Registered source-matched calibration, docs/G2_SOURCE_AUDIT.md.
FLOW_SHARE = 0.2827
RETURN_SHARE = 0.32
DIAGONAL_SENSITIVITY = 0.29
STRUCTURAL_ENDPOINTS = (0.0029, 0.0046)
FACTOR_LOADING = 0.7

PERTURBATION_GRID = (0.0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3)
FACTOR_COUNT_GRID = (1, 2, 3, 4, 6, 10)
FLOW_SHARE_GRID = tuple(round(0.10 + 0.0125 * i, 4) for i in range(29))
FEEDBACK_ARMS = (0, 1, 2, 30)

SCOPE = (
    "conditional analytic exhibit at published summary statistics; "
    "not an estimate of any market's impact matrix"
)


def _round(value: float) -> float:
    """Round to ten significant digits so the JSON is platform-stable."""
    return float(format(float(value), ".10g"))


def _fixture(rank_b: int) -> tuple[Matrix, ...]:
    """Rebuild the A028 frozen fixture in its registered draw order."""
    rng = np.random.default_rng(FIXTURE_SEED)

    def psd(n: int) -> Matrix:
        a = rng.normal(size=(n, n))
        return np.asarray(a @ a.T / n + np.eye(n) * 0.5, dtype=np.float64)

    lam = rng.normal(scale=0.1, size=(N_ASSETS, N_ASSETS))
    gam = rng.normal(size=(N_ASSETS, N_FACTORS))
    df = rng.normal(size=(N_ASSETS, N_FACTORS))
    if rank_b == 0:
        b = np.zeros((N_ASSETS, N_ASSETS))
    elif rank_b >= N_ASSETS:
        b = rng.normal(scale=0.02, size=(N_ASSETS, N_ASSETS))
    else:
        b = rng.normal(size=(N_ASSETS, rank_b)) @ rng.normal(size=(rank_b, N_ASSETS)) * 0.05
    return lam, b, gam, df, psd(N_FACTORS), psd(N_ASSETS), psd(N_ASSETS)


def _gap_ranks() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for rank_b in FEEDBACK_ARMS:
        lam, b, gam, df, sf, su, sv = _fixture(rank_b)
        gap = confounding_gap(lam, b, gam, df, sf, su, sv)
        rows.append(
            {
                "rank_b": rank_b,
                "observed_rank": numerical_rank(gap),
                "bound": gap_rank_bound(N_FACTORS, b),
            }
        )
    return rows


def _diagonal_truth_headline() -> dict[str, float]:
    """Spurious off-diagonal magnitude when the structural truth is diagonal."""
    rng = np.random.default_rng(FIXTURE_SEED)
    _, _, gam, df, sf, su, sv = _fixture(0)
    diagonal = rng.uniform(0.2, 0.4, N_ASSETS)
    truth = np.diag(diagonal)
    gap = confounding_gap(truth, np.zeros((N_ASSETS, N_ASSETS)), gam, df, sf, su, sv)
    off_diagonal = gap - np.diag(np.diag(gap))
    return {
        "spurious_offdiag_max": _round(float(np.abs(off_diagonal).max())),
        "own_impact_min": _round(float(diagonal.min())),
        "own_impact_max": _round(float(diagonal.max())),
        "gap_rank_under_diagonal_truth": numerical_rank(gap),
    }


def _observed_one_spike(o: float, s_q: float) -> tuple[float, float]:
    q1, _ = one_spike_eigenvalues(N_ASSETS, s_q)
    _, q0 = one_spike_eigenvalues(N_ASSETS, s_q)
    h_q = float(np.sqrt(q1 - q0))
    gap = one_spike_gap_per_entry(FACTOR_LOADING, h_q, N_ASSETS, q1)
    return DIAGONAL_SENSITIVITY + gap, o + gap


def _sharp_intervals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for o in STRUCTURAL_ENDPOINTS:
        a_diag, a_off = _observed_one_spike(o, FLOW_SHARE)
        lower, upper = sharp_offdiag_interval(N_ASSETS, FLOW_SHARE, RETURN_SHARE, a_diag, a_off)
        halfwidth = (upper - lower) / 2.0
        rows.append(
            {
                "truth": o,
                "observed_offdiagonal": _round(a_off),
                "lower": _round(lower),
                "upper": _round(upper),
                "halfwidth": _round(halfwidth),
                "halfwidth_over_observed": _round(halfwidth / a_off),
                "contains_zero": bool(lower < 0.0 < upper),
            }
        )
    return rows


def _psi_exhibits() -> dict[str, Any]:
    rng = np.random.default_rng(FIXTURE_SEED)
    base = np.diag(rng.uniform(0.2, 0.4, N_ASSETS)) + (
        rng.normal(size=(N_ASSETS, N_FACTORS)) @ rng.normal(size=(N_FACTORS, N_ASSETS)) * 0.05
    )
    pert_rng = np.random.default_rng(PERTURBATION_SEED)
    pert = pert_rng.normal(size=(N_ASSETS, N_ASSETS))
    pert -= np.diag(np.diag(pert))
    pert /= np.linalg.norm(pert)
    curve = [
        {"epsilon": eps, "psi": _round(psi_k(base + eps * pert, N_FACTORS))}
        for eps in PERTURBATION_GRID
    ]
    reference = base + 0.1 * pert
    by_k = [{"k": k, "psi": _round(psi_k(reference, k))} for k in FACTOR_COUNT_GRID]
    return {
        "psi_null": _round(psi_k(base, N_FACTORS)),
        "psi_curve": curve,
        "psi_by_factor_count": by_k,
    }


def _bounds_curve() -> list[dict[str, float]]:
    """Identified interval across a grid of leading flow-commonality shares."""
    rows: list[dict[str, float]] = []
    for s_q in FLOW_SHARE_GRID:
        a_diag, a_off = _observed_one_spike(STRUCTURAL_ENDPOINTS[-1], s_q)
        try:
            lower, upper = sharp_offdiag_interval(N_ASSETS, s_q, RETURN_SHARE, a_diag, a_off)
        except ValueError:
            continue
        rows.append(
            {
                "flow_share": s_q,
                "observed": _round(a_off),
                "lower": _round(lower),
                "upper": _round(upper),
            }
        )
    return rows


def build_exhibits() -> dict[str, Any]:
    """Assemble the complete exhibit payload."""
    payload: dict[str, Any] = {
        "scope": SCOPE,
        "assets": N_ASSETS,
        "factors": N_FACTORS,
        "flow_share": FLOW_SHARE,
        "return_share": RETURN_SHARE,
        "diagonal_sensitivity": DIAGONAL_SENSITIVITY,
        "gap_ranks": _gap_ranks(),
        "sharp_intervals": _sharp_intervals(),
        "bounds_curve": _bounds_curve(),
        "published_pairwise_correlation": _round(
            (
                one_spike_eigenvalues(N_ASSETS, FLOW_SHARE)[0]
                - one_spike_eigenvalues(N_ASSETS, FLOW_SHARE)[1]
            )
            / N_ASSETS
        ),
    }
    payload.update(_diagonal_truth_headline())
    payload.update(_psi_exhibits())
    return payload


def _coordinates(pairs: list[tuple[float, float]]) -> str:
    return " ".join(f"({format(x, '.10g')},{format(y, '.10g')})" for x, y in pairs)


def _render_bounds(payload: dict[str, Any]) -> str:
    curve = payload["bounds_curve"]
    upper = [(row["flow_share"], row["upper"]) for row in curve]
    lower = [(row["flow_share"], row["lower"]) for row in curve]
    observed = [(row["flow_share"], row["observed"]) for row in curve]
    return (
        "% Generated by python -m xid.exhibits. Do not edit by hand.\n"
        f"\\newcommand{{\\FigBoundsUpper}}{{{_coordinates(upper)}}}\n"
        f"\\newcommand{{\\FigBoundsLower}}{{{_coordinates(lower)}}}\n"
        f"\\newcommand{{\\FigBoundsObserved}}{{{_coordinates(observed)}}}\n"
    )


def _render_diagnostic(payload: dict[str, Any]) -> str:
    curve = [(row["epsilon"], row["psi"]) for row in payload["psi_curve"]]
    by_k = [(float(row["k"]), row["psi"]) for row in payload["psi_by_factor_count"]]
    return (
        "% Generated by python -m xid.exhibits. Do not edit by hand.\n"
        f"\\newcommand{{\\FigPsiCurve}}{{{_coordinates(curve)}}}\n"
        f"\\newcommand{{\\FigPsiByFactorCount}}{{{_coordinates(by_k)}}}\n"
    )


def write_exhibits(out_dir: Path) -> dict[str, Any]:
    """Write every artifact into ``out_dir`` and return the payload."""
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = build_exhibits()
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    (out_dir / "exhibits.json").write_text(text, encoding="utf-8")
    (out_dir / "fig_bounds.tex").write_text(_render_bounds(payload), encoding="utf-8")
    (out_dir / "fig_diagnostic.tex").write_text(_render_diagnostic(payload), encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    write_exhibits(args.out)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
