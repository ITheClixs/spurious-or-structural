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
import math
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from xid.models.execution import (
    confounding_null_space,
    cost_error,
    factor_exposure,
    impact_cost,
    minimax_cost_schedule,
    worst_case_cost,
)
from xid.models.identification import (
    confounding_gap,
    gap_rank_bound,
    numerical_rank,
    one_spike_eigenvalues,
    one_spike_gap_per_entry,
    sharp_offdiag_interval,
)
from xid.models.identification import sharp_offdiag_interval as _sharp
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

# Quantities that are analytically zero still return floating-point noise of
# order 1e-15, and that noise is not portable across LAPACK builds. Reporting
# ten significant digits of it would be reporting the platform, not the result.
NUMERICAL_ZERO = 1e-12

SCOPE = (
    "conditional analytic exhibit at published summary statistics; "
    "not an estimate of any market's impact matrix"
)

# Capponi and Cont (2020), pp. 10-11 and 17-19, as recorded in
# docs/G2_SOURCE_AUDIT.md. Reported to two decimal places.
CC_CROSS_MEAN_BEFORE = 0.032
CC_CROSS_MEAN_AFTER = -0.039
CC_CROSS_SD_BEFORE = 0.06
CC_CROSS_SD_AFTER = 0.06
CC_OWN_MEAN_BEFORE = 2.64
CC_OWN_MEAN_AFTER = 2.57
CC_OWN_SD_BEFORE = 0.78
CC_OWN_SD_AFTER = 0.77
CC_NEGATIVE_FRACTION_BEFORE = 0.2309
CC_NEGATIVE_FRACTION_AFTER = 0.8446
CC_REPORTING_PRECISION = 0.01
SHAPE_AGREEMENT_TOLERANCE = 0.05


def _round(value: float) -> float:
    """Round to ten significant digits, collapsing analytic zeros to exactly zero.

    Ten digits is far above the drift of every stable quantity here, but a
    value whose true magnitude is zero carries no stable digits at all, so it
    is clamped rather than serialised as noise.
    """
    scalar = float(value)
    if abs(scalar) < NUMERICAL_ZERO:
        return 0.0
    return float(format(scalar, ".10g"))


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
        "numerical_zero_floor": NUMERICAL_ZERO,
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
    payload["published_control_shift"] = _published_control_shift()
    payload["execution"] = _execution_exhibits()
    payload.update(_diagonal_truth_headline())
    payload.update(_psi_exhibits())
    return payload


def _standard_normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _published_control_shift() -> dict[str, Any]:
    """Check the rank-one constant-shift signature against published summaries.

    Eq. (11) makes a single factor control shift every cross-coefficient by one
    common constant. The mean must therefore move while the cross-sectional
    dispersion and the distribution shape stay fixed. Both implications are
    checked separately because they can disagree, and a disagreement is
    informative rather than something to suppress.
    """
    mean_shift = CC_CROSS_MEAN_AFTER - CC_CROSS_MEAN_BEFORE
    sd_change = CC_CROSS_SD_AFTER - CC_CROSS_SD_BEFORE
    own_sd_change = CC_OWN_SD_AFTER - CC_OWN_SD_BEFORE

    # Under an exactly constant shift the shape is preserved, so the post-control
    # negative fraction equals the pre-control mass below the shift magnitude.
    predicted_negative_after = _standard_normal_cdf(
        (-mean_shift - CC_CROSS_MEAN_BEFORE) / CC_CROSS_SD_BEFORE
    )
    shape_gap = abs(predicted_negative_after - CC_NEGATIVE_FRACTION_AFTER)

    return {
        "source": "Capponi and Cont (2020), pp. 10-11 and 17-19",
        "cross_mean_before": CC_CROSS_MEAN_BEFORE,
        "cross_mean_after": CC_CROSS_MEAN_AFTER,
        "cross_mean_shift": _round(mean_shift),
        "cross_sd_before": CC_CROSS_SD_BEFORE,
        "cross_sd_after": CC_CROSS_SD_AFTER,
        "cross_sd_change": _round(sd_change),
        "own_mean_before": CC_OWN_MEAN_BEFORE,
        "own_mean_after": CC_OWN_MEAN_AFTER,
        "own_sd_before": CC_OWN_SD_BEFORE,
        "own_sd_after": CC_OWN_SD_AFTER,
        "own_sd_change": _round(own_sd_change),
        "reporting_precision": CC_REPORTING_PRECISION,
        "predicted_sd_change": 0.0,
        "sd_invariance_consistent": bool(abs(sd_change) <= CC_REPORTING_PRECISION),
        "negative_fraction_before_reported": CC_NEGATIVE_FRACTION_BEFORE,
        "negative_fraction_after_reported": CC_NEGATIVE_FRACTION_AFTER,
        "negative_fraction_after_predicted_normal": _round(predicted_negative_after),
        "negative_fraction_shape_gap": _round(shape_gap),
        "shape_agreement_tolerance": SHAPE_AGREEMENT_TOLERANCE,
        "negative_fraction_shape_consistent": bool(shape_gap <= SHAPE_AGREEMENT_TOLERANCE),
        "shape_check_caveat": (
            "the shape implication is evaluated under a Gaussian approximation to "
            "an empirically skewed cross-sectional distribution, so a gap indicates "
            "loading heterogeneity beyond one common factor rather than a failure "
            "of the rank bound itself"
        ),
        "scope": SCOPE,
    }


def _execution_exhibits() -> dict[str, Any]:
    """A029: which trade directions a confounded matrix misprices."""
    _, _, gam, df, sf, su, sv = _fixture(0)
    truth_rng = np.random.default_rng(FIXTURE_SEED)
    truth = np.diag(truth_rng.uniform(0.2, 0.4, N_ASSETS))
    gap = confounding_gap(truth, np.zeros((N_ASSETS, N_ASSETS)), gam, df, sf, su, sv)

    trade_rng = np.random.default_rng(PERTURBATION_SEED)
    index = np.full(N_ASSETS, 1.0 / np.sqrt(N_ASSETS))
    random_trade = trade_rng.normal(size=N_ASSETS)
    random_trade /= np.linalg.norm(random_trade)
    basis = confounding_null_space(gap)
    neutral = basis @ (basis.T @ trade_rng.normal(size=N_ASSETS))
    neutral /= np.linalg.norm(neutral)

    general = [
        {
            "trade": name,
            "true_cost": _round(impact_cost(x, truth)),
            "cost_error": _round(cost_error(x, gap)),
            "relative_percent": _round(100.0 * cost_error(x, gap) / impact_cost(x, truth)),
        }
        for name, x in (
            ("index", index),
            ("random", random_trade),
            ("confound_neutral", neutral),
        )
    ]

    q1, q0 = one_spike_eigenvalues(N_ASSETS, FLOW_SHARE)
    h_q = float(np.sqrt(q1 - q0))
    g = one_spike_gap_per_entry(FACTOR_LOADING, h_q, N_ASSETS, q1)
    o = STRUCTURAL_ENDPOINTS[-1]
    m = np.full(N_ASSETS, 1.0 / np.sqrt(N_ASSETS))
    spike_truth = (DIAGONAL_SENSITIVITY - o) * np.eye(N_ASSETS) + N_ASSETS * o * np.outer(m, m)
    spike_gap = g * np.ones((N_ASSETS, N_ASSETS))
    pair = np.zeros(N_ASSETS)
    pair[0], pair[1] = 1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)
    spike_rng = np.random.default_rng(PERTURBATION_SEED)
    spike_random = spike_rng.normal(size=N_ASSETS)
    spike_random /= np.linalg.norm(spike_random)
    one_spike = [
        {
            "trade": name,
            "true_cost": _round(impact_cost(x, spike_truth)),
            "cost_error": _round(cost_error(x, spike_gap)),
            "relative_percent": _round(
                100.0 * cost_error(x, spike_gap) / impact_cost(x, spike_truth)
            ),
            "factor_exposure": _round(factor_exposure(x)),
        }
        for name, x in (
            ("index", m),
            ("random", spike_random),
            ("dollar_neutral_pair", pair),
        )
    ]

    a_diag, a_off = DIAGONAL_SENSITIVITY + g, o + g
    lower, upper = _sharp(N_ASSETS, FLOW_SHARE, RETURN_SHARE, a_diag, a_off)
    penalty = (upper - lower) / 2.0
    a = (a_diag - a_off) * np.eye(N_ASSETS) + a_off * np.ones((N_ASSETS, N_ASSETS))
    a_sym = np.asarray((a + a.T) / 2.0, dtype=np.float64)
    target_rng = np.random.default_rng(FIXTURE_SEED)
    neutral_target = np.zeros(N_ASSETS)
    neutral_target[0], neutral_target[1] = 1.0, -1.0
    targets = {
        "index_like": np.ones(N_ASSETS),
        "neutral": neutral_target,
        "general": target_rng.normal(size=N_ASSETS),
    }
    schedules = []
    for name, c in targets.items():
        naive = minimax_cost_schedule(a_sym, c, 1.0, 0.0)
        robust = minimax_cost_schedule(a_sym, c, 1.0, penalty)
        naive_wc = worst_case_cost(naive, a_sym, penalty)
        robust_wc = worst_case_cost(robust, a_sym, penalty)
        schedules.append(
            {
                "target": name,
                "naive_worst_case": _round(naive_wc),
                "robust_worst_case": _round(robust_wc),
                "improvement_percent": _round(100.0 * (naive_wc - robust_wc) / naive_wc),
                "naive_exposure": _round(factor_exposure(naive)),
                "robust_exposure": _round(factor_exposure(robust)),
            }
        )

    return {
        "immune_subspace_dimension": int(basis.shape[1]),
        "cost_error_general_fixture": general,
        "cost_error_one_spike": one_spike,
        "exposure_law_constant": _round(N_ASSETS * g),
        "robust_schedule_penalty": _round(penalty),
        "robust_schedules": schedules,
    }


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


def _render_psi_study(out_dir: Path) -> str:
    """Read the committed confirmatory study and emit its figure coordinates.

    The study itself is slow and lives in ``xid.psi_study``. This generator only
    reprojects its committed output, so the figure can never disagree with the
    numbers the test suite checks.
    """
    study_path = out_dir / "psi_study.json"
    if not study_path.is_file():
        return (
            "% psi_study.json absent; run python -m xid.psi_study first.\n"
            "\\newcommand{\\FigPsiSize}{}\n"
            "\\newcommand{\\FigPsiPower}{}\n"
        )
    study = json.loads(study_path.read_text())
    size = [(float(row["sample_size"]), float(row["plug_in_size"])) for row in study["size"]]
    power = [(float(row["epsilon"]), float(row["power"])) for row in study["power"]]
    return (
        "% Generated by python -m xid.exhibits from the committed psi study.\n"
        f"\\newcommand{{\\FigPsiSize}}{{{_coordinates(size)}}}\n"
        f"\\newcommand{{\\FigPsiPower}}{{{_coordinates(power)}}}\n"
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
    (out_dir / "fig_psi_study.tex").write_text(_render_psi_study(out_dir), encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    write_exhibits(args.out)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
