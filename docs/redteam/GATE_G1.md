# Red-team memo — G1 probability-limit derivation

Review date: 2026-07-15

## Verdict

**G1 passed.** This memo and the immutable result artifacts were committed at
`44965d0370810f756ad1c5cc7938a289cb943906`; hosted CI run `29426776688`
completed successfully. G2 is open, without weakening any criticism below.

The claim under attack is narrow: under the explicitly stated simultaneous
linear Gaussian system, the streamed regressions converge to the two derived
pseudo-true coefficient matrices. This is not evidence that structural
cross-impact is identified, that a factor proxy cures endogeneity, or that the
fixture resembles market data.

## Evidence

- The sole master seed `2026071501` generated 100 immutable shards, exactly
  10,000,000 observations, contiguous indices 0 through 99, and 100 unique
  payload hashes. No alternate master attempt exists.
- Uncontrolled OLS has maximum elementwise no-floor relative discrepancy
  `5.639467093140219e-4`; proxy-controlled OLS has
  `5.123714186295689e-4`. Their maximum is strictly below `10^-3`.
- All 1,800 targets lie inside the named 95% family-wise classical
  homoskedastic Student-t Bonferroni intervals. Maximum absolute standardized
  errors are 3.428433462 and 3.122083665, below critical values near 4.191.
- Separate primitive-bias and full reduced-form covariance calculations agree;
  mutation tests reject omitted simultaneity, omitted confounding, a missing
  transpose, and scalar proxy attenuation.
- Independent reviewers reconstructed the result from raw checkpoint moments,
  checked both matrix orientations and the FWL proxy residual, and matched the
  published coefficients, intervals, and strict discrepancy statistic.
- `_SUCCESS` binds summary SHA256
  `b590b8ba079c70917e3e768ff1079051f2b8a6c8007336367aa2d299ec3c5d54`
  and estimates SHA256
  `f5129b0fc7695e7db13074dad64ac6123263992ccca920f579d85205bba8f06f`.
  Deterministic resume left both files and the marker byte-identical.

## Attacks

### 1. The fixture ducks the economically hard coefficients

Every target is large and positive, spanning approximately 0.772 to 0.920.
The no-floor relative metric is therefore numerically well behaved and never
tests a near-zero coefficient, a sign boundary, or a sparse cross-impact
matrix. Those are precisely the cases that matter to the empirical dispute.

**Assessment:** serious and unanswered, but not a G1 blocker. G1 validates the
stated matrix algebra. G2 must calibrate sign-sensitive off-diagonals and may
not cite this pass as evidence that their finite-sample problem is easy.

### 2. Generator and target code could share the same mistake

The reduced-form generator and analytic target paths necessarily share the
fixture and some structural conventions. A common timing or orientation error
could make simulation and target agree.

**Assessment:** materially mitigated, not eliminated. The derivation is written
from primitives; a second full block-covariance path, structural-equation
residual checks, mutation tests, raw-checkpoint refits, and independent algebra
audits all agree. A shared misunderstanding of the economic timing convention
remains possible and belongs in the empirical design.

### 3. IID Gaussian shocks make inference unusually forgiving

Joint Gaussianity makes the population linear-projection residual independent
of its regressors, so classical homoskedastic Student-t intervals are appropriate
for this fixture. Real order flow is serially dependent, heavy-tailed,
heteroskedastic, and timestamp-sensitive.

**Assessment:** not transported. The interval result validates only the frozen
simulation. Empirical inference must use dependence-robust methods derived and
tested later; reusing these intervals would be a design violation.

### 4. One seed does not establish interval calibration

All 1,800 targets happened to lie inside their simultaneous intervals, but one
realisation cannot estimate the repeated-sampling coverage of a nominal 95%
procedure.

**Assessment:** true and nonblocking. Interval inclusion was preregistered as a
secondary integrity check, not the gate statistic. The gate is the strict
finite-sample discrepancy, and no seed retry was allowed or used.

### 5. Ten million observations can conceal weak finite-sample behavior

The sample is intentionally large enough to validate a probability limit.
Passing says little about the smaller effective sample sizes, conditioning,
weak identification, or non-convex optimization that later gates must face.

**Assessment:** not a defect in this gate. G4 must publish the identification
and finite-sample failure frontier; G5 must demonstrate the naive estimator's
failures rather than infer scalability from G1.

### 6. Zero shock cross-covariances are substantive

The primitive-only formulas require zero contemporaneous cross-covariances
among factor, return shock, flow shock, and proxy noise. That assumption is
unlikely to be innocuous in market data.

**Assessment:** correctly exposed as A012 and in the derivation. If empirical
diagnostics reject it, additional covariance terms enter and these formulas do
not describe the tape. The G1 conditional result remains mathematically valid.

### 7. Fast execution is not scientific corroboration

The full generator used 8.239197838 cumulative shard seconds and less than
438 MB checkpoint RSS. This proves the laptop design is adequate; it says
nothing about economic validity.

**Assessment:** resource pass only. The result must not be made more credible
because it was easy to reproduce.

## Strongest unresolved objection

This experiment validates a conditional algebraic identity on a dense positive
Gaussian fixture, not the near-zero, sign-sensitive object at the centre of the
cross-impact debate. A perfectly correct G1 can coexist with a dead G2 premise,
unidentified G4 system, or rejected empirical model. The next gate must be able
to kill the project rather than inherit confidence from this software result.

## What would have falsified G1

- A gate discrepancy at or above `10^-3` under the sole frozen seed.
- Any target-hash, structural-equation, checkpoint, source, runtime, or
  publication-marker mismatch.
- An independent raw-moment refit or algebra path that disagreed with the
  serialized targets, coefficients, or orientation.
- Evidence of a seed retry, changed threshold, omitted coefficient, denominator
  floor, or post-outcome fixture adjustment.

None occurred.

## Gate decision

- Symbolic derivation: **passed**.
- Frozen 10-million-row recovery: **passed**.
- Named simultaneous intervals and complete coefficient reporting: **passed**.
- Independent hostile review: **passed**.
- Durable closeout and hosted parity: **passed**, run `29426776688`.
- G1 overall: **passed; G2 open**.
