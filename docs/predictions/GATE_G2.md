# G2 pre-run prediction

Written before G2 implementation, resource benchmarking, validation, or the
single frozen research draw. The first hostile review rejected an earlier
three-factor design and then rejected the oracle-only S0003 boundary before any
RNG access; S0004 is the only design
eligible for execution.

## Claim that may die

Conditional on diagonal sensitivity `d = 0.29` and the registered
off-diagonal sensitivity interval, a permutation-invariant one-factor model
matching the registered Capponi--Cont one-minute commonality will exhibit more
than 50% confounding error in a homogeneous off-diagonal impact coefficient
for an observable integrated-top-ten-OFI proxy-control ridge, two stronger
oracle-flow projections, and the binding published `CI_I` protocol check.

This is a conditional-existence claim. It is not an estimate of the real
market's structural tuple and does not claim that confounding explains the
published disagreement.

## Deterministic population prediction

The structural off-diagonal varies continuously from `0.0029` to `0.0046`
with diagonal `0.29`. Seventeen closed-grid points license the finite-sample
runner; the analytic formula in
`docs/derivations/GATE_G2_PREMISE.md` covers the continuous interval.

At proxy reliability `0.95`, the population predictions are:

| True off-diagonal | Homogeneous | Oracle ridge | Observable ridge | Observable error | Critical reliability: homogeneous / oracle / observable |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0029000 | 0.0098396929 | 0.0098396897 | 0.0097798675 | 237.24% | 99.260385% / 99.260383% / 99.226218% |
| 0.0046000 | 0.0109224510 | 0.0109224470 | 0.0108491633 | 135.85% | 98.634210% / 98.634207% / 98.573188% |

The upper structural endpoint is least favorable to the positive claim. Its
population observable-ridge error exceeds the 50% threshold by
`0.0039491633` in coefficient units before sampling uncertainty. Exact values
for all seventeen points are committed as canonical JSON in
`configs/g2_population_targets.json`; the raw-file SHA256 is
`f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59`.
Because full-precision floating evaluation can vary by a few ULPs, the
independently reproducible 12-decimal semantic SHA256 is
`f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`.
Every registered command must validate both roles before obtaining an RNG:
the raw digest protects the committed bytes, while the semantic digest checks
an independent derivation under the frozen canonicalization rule.

The directional prediction at reliability 0.95 is a positive overestimate. At
reliability one, homogeneous OLS recovers `Lambda`, oracle ridge retains only
the floor shrinkage `10^-6 / (1 + 10^-6)`, and observable ridge targets
`0.9816922278202821 o` because OFI measurement error remains. All three
negative-control targets are sealed analytically.

The historical Hasbrouck--Seppi comparator is nonconfirmatory. A prior
continuous calculation combining its dimensionless factor summaries with the
one-minute point gives a least favorable 77.15% population error at 95%
reliability. This is robustness evidence only, not a joint calibration.

## Strongest-opponent prediction

All three smooth confirmatory candidates must pass at all seventeen structural
grid points:

1. `ORACLE_Q_PROXY95_CONDITION_RIDGE` receives all 30 true flows and the proxy,
   partials out the proxy, and uses a positive condition-capped ridge inverse;
2. `ORACLE_Q_PROXY95_HOMOGENEOUS_OLS` is additionally told the true homogeneous
   symmetry and pools every asset row on own flow, the sum of other flows, and
   the proxy while preserving whole-date clusters. Its cross-sum coefficient
   is one off-diagonal; and
3. `INTEGRATED_OFI_PROXY95_CONDITION_RIDGE` observes only date-estimated,
   L1-normalized top-ten PC scores plus the proxy. This is the gate-binding
   observable factor-control opponent.

The second model is a no-strawman veto: it removes the high-dimensional
covariance inversion and estimates only three slopes. No truth-assisted model
selection occurs after the draw.

The `CI_I` CCZ protocol reconstruction is also binding at the primary
observable calibration and upper structural endpoint because it is the only
published CCZ equation with integrated top-ten OFI and explicit off-diagonal
coefficients. Its predeclared `(0,1)` coefficient must pass the same rule under
the shared 499 date weights. The other five CCZ reconstructions are mandatory
fidelity diagnostics reported separately.
Factor-residual operators are compared with their fair projected target
`Lambda P_perp`; their full response-equivalent maps are not silently
substituted for that estimand. No diagnostic can rescue a failed smooth
candidate or failed `CI_I` veto.

## Interval, size, and power prediction

The confirmatory standard error is the sample standard deviation of 499
whole-date multinomial-weight bootstrap estimates. Each replicate preserves
date order and all within-date bins/assets, and refits the complete smooth
candidate from date sufficient statistics. The reported 95% intervals are a
bootstrap-SE normal interval with `ddof=1` and critical value
`1.959963984540054`, and a basic date-cluster interval using Hyndman--Fan type
7 quantiles at 0.025 and 0.975.

The gate uses a stricter form of the brief's rule:

```text
abs(estimate - truth) - 0.50 abs(truth) > 3 bootstrap_se.
```

Thus the margin beyond 50%, rather than error merely relative to zero, must
clear three standard errors.

Before the research seed is available, 100 independent panels must license the
exact final procedure:

- a null-grid superpanel runs nine proxy-noise-amplitude nodes from `R = 1` to
  each candidate/cell's semantic-hash-sealed 50%-materiality boundary, for 459
  strict events; the one-sided 95% Clopper--Pearson upper bound on the family
  indicator that **any** event passes is at most 5%; and
- a power superpanel runs all 51 smooth components at proxy reliability 0.95; the
  one-sided 95% Wilson lower bound on the gate indicator that **every**
  component passes is at least 80%.

With 100 superpanels, the first rule permits at most one family-union success
and the second requires at least 87 gate-intersection successes. Reliability
one also supplies a 51-component analytic-target recovery diagnostic. This is
a frozen null-grid calibration, not a continuum-uniform size proof. Marginal
component rates receive unadjusted, descriptive, non-gating one-sided 95%
Clopper--Pearson upper intervals for null components and Wilson lower intervals
for power components.

All 51 actual alternatives supply the joint power license; no impossible
exactly-50% alternative is planted. The upper endpoint alone supplies the
reduced 48-/96-date and reliability frontiers. Their six candidate-by-date and
twelve candidate-by-extra-reliability passage rates each receive an unadjusted,
descriptive, non-gating one-sided 95% Wilson lower interval over 100
superpanels. A failed validation seed is not retried. The heavier published
`CI_I` branch separately must recover homogeneous
diagonal `0.29` and focal cross-impact `0.0046` at actual `N=30` and 252 dates
before its binding research run.
That recovery retains the confirmatory equicorrelated flow law but removes price
confounding (`Gamma = 0`), so it cannot pass by replacing the hard collinear
design with independent flows, exact measured flows, isotropic return noise, or
a zero cross coefficient. It preserves every research upper-endpoint
distribution parameter and deterministic map except `Gamma`, but uses its own
disjoint phase-25/scenario-4 addressed normals so validation cannot inspect the
phase-30 research realization.
All 31 truth values must lie inside their Bonferroni date-bootstrap-normal
intervals, every point error must be strictly below 50%, and the focal
material-bias declaration must be false. This does not upgrade one recovery
panel into a Monte Carlo size/power license.

The finite null grid has a frozen maximum proxy-noise-amplitude gap of
`0.015038828627620739` and maximum adjacent reliability gap of
`0.003307437435413063`. These gaps ship with the outcome. Any nonfinite result,
declared required-full-rank/conditioning failure, weak PCA, named cell failure,
or solver nonconvergence fails validation outright; it is not treated as
evidence of size control.

## Dependence and resource prediction

All latent components use stationary Gaussian AR(1) paths with coefficient
`0.60`, independent stationary initialization by date, and no cross-date
innovations. This unsourced value is an explicitly hostile dependence stress,
not empirical calibration. An IID path is diagnostic.

Validation uses reliability-polynomial date moments. A shared base plus one
252-date structural cell is `8,811,936` bytes; all retained numeric validation
output is below 238 MB and a 2x allocation remains below 500 MB. The paper path
streams one raw date and retains a roughly 17.1 MB research summary.

The benchmark times fourteen distinct kernels, including base/cell
construction, each of the three fits, weighted aggregation, interval
finalization, every checkpoint boundary, a complete six-spec paper date, and a
`CI_I`-recovery date. It runs until at least four total complete bundles and at
least 600 post-cold seconds have elapsed; the last three complete bundles
determine warm throughput. Each phase
uses 1.25 times planned work divided by the smaller of warm throughput and 60%
of cold throughput. Any one-/12-/three-/16-hour expected-cap projection breach,
480-second task/batch, 3.5 GB RSS, or 2 GB checkpoint breach stops before
validation. The two-/24-/six-/32-hour hard limits are runtime kill thresholds,
not admission slack.

## Interpretation of every outcome

- **All three smooth candidates and `CI_I` pass their frozen scopes after the
  smooth null-grid/power license and published recovery check:** G2
  supports material confounding in the registered source-matched model class.
- **A nonbinding CCZ diagnostic differs:** report the estimand-specific
  discrepancy; it cannot rescue a failed binding event.
- **Any smooth confirmatory candidate or the `CI_I` veto fails:** no-strawman veto; G2 does
  not pass.
- **Population bound crosses 50%:** deterministic design failure; no RNG is
  permitted.
- **Size, power, or compute license fails:** unadjudicated design failure; the
  research seed remains sealed.
- **The sole research draw misses a registered event after adequate smooth
  power:** the preregistered finite-sample demonstration fails. With an 80%
  power floor this does not logically falsify the analytically known population
  fixture, and it is not a premise-killing market null.
- **Premise-killing null:** permitted only after a separately preregistered
  sharp source-compatible bias upper bound lies below 50% with adequate power.

The research seed is consumed once, after a clean implementation boundary and
hosted CI. It is never retried under another seed or silent specification.
