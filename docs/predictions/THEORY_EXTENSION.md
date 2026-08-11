# Theory-extension pre-run prediction

Registered on 2026-08-12 after the symbolic derivation in
`docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md` and before any
identification module, rank diagnostic, exhibit generator, or manuscript
revision existed. Every quantity below is a deterministic evaluation of derived
algebra. None is a fitted, simulated, or stochastic result.

## Scope

This prediction covers amendment A028 only. It does not open, modify, or
license any part of the G2 premise test. G2 remains open and executable-red.
The registered resource seed `2026071529`, validation seed `2026071521`, and
research seed `2026071522` are not accessed. No external market data,
evaluation data, or holdout is touched. The only randomness permitted is test
seed `1729`, used to draw fixture matrices for deterministic algebraic checks.

## Frozen fixture

Predictions 1 through 3 and 5 use the following fixture, constructed with
`numpy.random.default_rng(1729)` in exactly this call order so that the draw is
reproducible:

- `N = 30` assets and `K = 3` factors.
- `lam` drawn as `normal(scale=0.1, size=(30, 30))`.
- `gam` drawn as `normal(size=(30, 3))`.
- `df` drawn as `normal(size=(30, 3))`.
- `B` constructed per arm: the zero matrix for `rank(B) = 0`; an outer product
  of two `normal(size=30)` draws scaled by `0.05` for `rank(B) = 1`;
  `normal(size=(30, 2)) @ normal(size=(2, 30))` scaled by `0.05` for
  `rank(B) = 2`; and `normal(scale=0.02, size=(30, 30))` for the full-rank arm.
- Each covariance is built as `A @ A.T / n + 0.5 * I` from a fresh
  `normal(size=(n, n))` draw, giving `sf` at `n = 3` and `su`, `sv` at
  `n = 30`.

Predictions 4 and 6 use the registered source-matched one-spike calibration:
`N = 30`, `s_q = 0.2827`, `s_r = 0.32`, `d = 0.29`, and
`o` in `{0.0029, 0.0046}`, taken from `docs/G2_SOURCE_AUDIT.md`.

## Quantitative predictions fixed before implementation

**Prediction 1 — the rank bound binds and is tight.** With the fixture above,
the numerical rank of `G = plim OLS − Λ` at relative tolerance `1e-10` is:

| `rank(B)` | Predicted `rank(G)` | Bound `K + rank(B)` |
| ---: | ---: | ---: |
| 0 | 3 | 3 |
| 1 | 4 | 4 |
| 2 | 5 | 5 |
| 30 | 30 | 33 |

Every observed rank must be at most its bound. The first three arms must attain
the bound exactly; the fourth is capped by the matrix dimension `N = 30`.

**Prediction 2 — diagonal truth gives an exactly rank-`K` gap.** With `Λ`
diagonal, entries drawn `uniform(0.2, 0.4, 30)`, and `B = 0`:

- `rank(G) = 3` exactly at relative tolerance `1e-10`;
- the induced off-diagonal entries are not all zero, so the spurious
  cross-impact matrix is dense rather than approximately diagonal; and
- `psi_3(Λ + G) < 1e-8`.

**Prediction 3 — the diagnostic is strictly monotone in structural
perturbation.** Adding a Frobenius-normalized dense off-diagonal perturbation
of size `ε` to a diagonal-plus-rank-3 matrix, `psi_3` is strictly increasing
over the frozen grid

```
ε ∈ {0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3}.
```

Strictness is required at every consecutive pair. A non-strict outcome
indicates the alternating projection stalled and is a failure of the
implementation, not a licence to weaken the assertion.

**Prediction 4 — the closed-form identified interval is exact.** In the
one-spike model the closed form

```
T² = (r_1 − q_1 a_1²)(q_1 − q_0) / (q_1 q_0)
```

agrees with a bisection search over the exact positive-semidefiniteness
boundary to relative error below `1e-10`. At the registered calibration the
predicted values are:

| `o` | `A_off` | `T` | Identified interval for `Λ_off` |
| ---: | ---: | ---: | :--- |
| 0.0029 | 0.0105537 | 2.8291865 | `[−0.083753, +0.104860]` |
| 0.0046 | 0.0122537 | 2.7125872 | `[−0.078166, +0.102673]` |

Both intervals contain zero. At the upper endpoint the half-width
`T/N = 0.0904196` is `7.38` times the observed off-diagonal coefficient.

**Prediction 5 — the diagnostic is permutation invariant.** Simultaneously
permuting rows and columns of a matrix changes `psi_3` by less than `1e-12`.

**Prediction 6 — the one-spike gap is entrywise constant.** In the one-spike
model every entry of `G` equals `γ h_q / (N q_1)` to within `1e-12`, across all
`900` entries.

## Published-summary consistency check

Capponi and Cont report, at one-minute frequency, a mean cross-coefficient of
`0.032` with cross-sectional standard deviation `0.06` before a principal
component control, and `−0.039` with standard deviation `0.06` after it; the
mean own coefficient moves from `2.64` (SD `0.78`) to `2.57` (SD `0.77`)
(`docs/G2_SOURCE_AUDIT.md`, pp. 10–11 and 17–19 of the source).

Prediction 6 implies that in the permutation-invariant geometry a single factor
control shifts **every** cross-coefficient by a common constant. The
cross-sectional standard deviation of the cross-coefficients is therefore
predicted to be unchanged, while the mean moves by the shift. The reported
figures give a mean shift of `−0.071` against a standard-deviation change of
`0.00`, which is the predicted signature.

This check is unit-free and requires no variable standard deviations, which the
sources do not report. It is a **conditional analytic exhibit at published
summary statistics; not an estimate of any market's impact matrix.** The
reported standard deviations are given to two decimal places, so the check is a
consistency observation and not a precise test. The published dispersion
figures are not confidence intervals and are not promoted to any.

## Intervals and reporting

Every quantity in this document is a deterministic algebraic identity or an
exact evaluation of one. No sampling distribution is involved, so the named
interval method is **not applicable** rather than omitted. The
multiple-testing count for this slice is **zero**: no stochastic draw and no
coefficient-to-truth comparison is performed.

## Failure interpretation fixed before implementation

- A rank observation exceeding `K + rank(B)` falsifies Theorem 2 and stops the
  theory extension entirely; the manuscript revision does not proceed.
- A rank observation strictly below the bound in the first three arms indicates
  a degenerate fixture rather than a false theorem; the fixture is diagnosed
  and the discrepancy is logged before anything is changed.
- A closed-form/bisection disagreement above `1e-10` means the Proposition 4
  algebra is wrong. The derivation is corrected and re-reviewed; the test is
  not relaxed to accommodate the implementation.
- A non-monotone `psi` curve means the alternating projection stalled. The
  iteration count is raised and the change is logged; the strictness assertion
  is not weakened.
- If the published-summary consistency check disagrees with the reported
  figures, the disagreement is reported in the manuscript as a limitation of
  the one-spike convention. The convention is **not** retuned to improve the
  match, and the main results of Sections 1 through 4 of the derivation do not
  depend on that check.
