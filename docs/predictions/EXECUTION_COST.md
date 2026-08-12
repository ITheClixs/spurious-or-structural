# Execution-cost pre-run prediction

Registered on 2026-08-12 after the symbolic derivation in
`docs/derivations/EXECUTION_COST_UNDER_CONFOUNDING.md` and before any execution
module, robust scheduler, exhibit, figure, or manuscript section existed. Every
quantity below is a deterministic evaluation of derived algebra. None is a
fitted, simulated, or stochastic result.

## Scope

This prediction covers amendment A029 only. It opens, modifies, and licenses no
part of the G2 premise test, which remains open and executable-red. Registered
resource seed `2026071529`, validation seed `2026071521`, and research seed
`2026071522` are not accessed, and no external market data, evaluation data, or
holdout is touched. The only randomness permitted is test seed `1729`, used to
draw deterministic algebraic fixtures.

## Frozen fixture

Predictions 1 to 3 use the A028 fixture at `N = 30`, `K = 3`, `B = 0`, with a
strictly diagonal structural matrix whose entries are drawn
`uniform(0.2, 0.4, 30)`, constructed in the registered draw order recorded in
`docs/predictions/THEORY_EXTENSION.md`.

Predictions 4 and 5 use the registered source-matched one-spike calibration:
`N = 30`, `s_q = 0.2827`, `s_r = 0.32`, `d = 0.29`, `o = 0.0046`, and factor
loading `gamma = 0.7`, giving `T/N = 0.0904196`.

Three frozen trades are used throughout: the equal-weight index trade
`m = 1/sqrt(N)`, a unit-norm random trade drawn at seed `1729`, and a
confound-neutral trade obtained by projecting a seed-`1729` normal draw onto
the orthogonal complement of the row space of `G`.

Three frozen target vectors are used for scheduling: the index-like target
`c = 1`, a neutral target `c = (1, -1, 0, ..., 0)`, and a general target drawn
`normal(size=30)` at seed `1729`.

## Quantitative predictions fixed before implementation

**Prediction 1 — the immune subspace exists and has the predicted dimension.**
The relative cost error of the confound-neutral trade is below `1e-12`, and the
numerically determined null space of `G` at relative tolerance `1e-10` has
dimension exactly `N - K = 27`.

**Prediction 2 — the headline cost errors.** Relative cost errors are:

| Trade | Predicted relative cost error |
| :--- | ---: |
| Equal-weight index | `-8.4174%` |
| Frozen random unit | `-0.6454%` |
| Confound-neutral | `-0.0000%` |

each to four decimal places.

**Prediction 3 — the exposure law.** In the one-spike geometry the ratio
`x'Gx / (m'x)^2` is constant across the frozen trades to below `1e-12` and
equals `N g` with `g = gamma h_q / (N q_1)`.

**Prediction 4 — the identified cost interval.** The interval of Eq. (7) has
half-width `(T/N)(1'x)^2` with `T/N = 0.0904196`, and is exactly zero for every
dollar-neutral trade.

**Prediction 5 — the robust schedule.** The closed form of Eq. (9) matches a
dense grid search over feasible schedules to below `1e-10`. Its worst-case cost
improvement over the naive schedule is:

| Target | Predicted improvement | Predicted factor exposure `1'x` |
| :--- | ---: | :--- |
| Index-like, `c = 1` | `0.000%` | `+1.0000` unchanged |
| Neutral, `1'c = 0` | `0.000%` | `0` unchanged |
| General random `c` | `3.109%` | `-0.0663` to `-0.0130` |

and `abs(1'x)` is weakly decreasing in the robustness penalty in every case.

## Intervals and reporting

Every quantity is a deterministic algebraic identity or an exact evaluation of
one, so the named interval method is **not applicable** rather than omitted.
The multiple-testing count for this slice is **zero**: no stochastic draw and
no coefficient-to-truth comparison is performed.

## Failure interpretation fixed before implementation

- A nonzero cost error on the confound-neutral trade above `1e-12` falsifies
  Theorem 6 and stops the execution results entirely.
- A null-space dimension other than `N - K` at `B = 0` indicates a degenerate
  fixture rather than a false theorem; the fixture is diagnosed and the
  discrepancy logged before anything is changed.
- A closed-form versus grid-search disagreement above `1e-10` means the
  Proposition 8 algebra is wrong. The derivation is corrected and re-reviewed;
  the tolerance is not relaxed to accommodate the implementation.
- A strictly positive improvement on either degenerate target would falsify
  Corollary 8.1 and require the corollary to be withdrawn, not softened.
- If the general-target improvement differs materially from `3.109%`, the
  observed value is reported and the discrepancy diagnosed. The fixture,
  targets, and calibration are not re-drawn to recover the predicted number.
