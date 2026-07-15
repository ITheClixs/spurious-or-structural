# Preregistration

Version 0.1, frozen for its first research commit on 2026-07-15, before any
external market data access. The commit containing this exact text is the freeze
boundary; an earlier runtime-only commit contains no preregistration or research
artifact.

## Integrity rule

This record is append-only after its first commit. Corrections and design
changes go in the `AMENDMENTS` section with a date, reason, effect on inference,
and an explicit statement of whether any affected data had already been seen.
The original text is never rewritten.

Current access statement: no external market archive, schema sample, evaluation
observation, or holdout observation has been requested or opened. The only G0
sample is generated synthetic smoke data and is not a market model.

## Questions and falsifiable hypotheses

The structural object is the cross-impact matrix `Lambda` in a simultaneous
return/order-flow system with latent price-relevant, flow-driving factors.

- **H1, material confounding:** at empirically defensible factor strength and
  flow collinearity, the strongest published own-flow-plus-observed-factor
  baseline has an off-diagonal sign error or more than 50% relative error, and
  the error exceeds three bootstrap standard errors.
- **H2, noisy controls:** increasing a factor proxy's reliability reduces but
  does not generically remove off-diagonal bias. G1 will derive and verify the
  exact probability limit before any empirical use.
- **H3, identification:** a method chosen only after diagnosing the system's
  moment geometry recovers `Lambda` at the planned operating point with
  `sigma_min(J) / sigma_max(J) > 10^-8` and truth inside a named bootstrap
  interval.
- **H4, independent theoretical corroboration:** an identified estimate is
  closer than OLS to a no-manipulation admissible set derived from opened
  primary sources. The bootstrap interval for the distance difference must
  exclude zero in the favorable direction. A result in the opposite direction
  falsifies the identification approach.
- **H5, economic relevance:** using the identified estimate changes scheduled
  multi-asset liquidation decisions enough to reduce out-of-model regret. This
  is evaluated both under known-truth Monte Carlo and once on sealed, genuinely
  observed forced-liquidation events.

Null outcomes are first-class results: immaterial calibrated bias, weak
identification, structural-model rejection, worse theoretical admissibility,
or no incremental execution value each triggers the corresponding null framing
in the operating brief. Every null requires a power calculation.

## Primary quantities and gate thresholds

- G1 maximum elementwise relative probability-limit discrepancy: `< 10^-3`
  with approximately `10^7` streamed observations.
- G2 premise threshold: off-diagonal sign flip or `> 50%` error, larger than
  three named bootstrap standard errors. Failure kills the positive premise.
- G4/G5 Jacobian threshold: `sigma_min(J) / sigma_max(J) > 10^-8`, recovery
  inside a named bootstrap interval, and a published failure frontier over
  `N`, `T`, differential regime contrast, and factor strength.
- G5 diagnosis: at least two distinct naive-estimator failure modes must be
  demonstrated numerically before a replacement is selected.
- G7 primary falsification: bootstrap the difference in distance to the
  admissible set; report maximum implied round-trip manipulation profit with an
  interval.

No estimator for H3 is preregistered here. Selecting one before deriving the
moments and diagnosing the naive failure would violate the research design. The
selection rule is preregistered: candidates may be considered only after the
failure is written in `DECISIONS.md`, and the chosen method must address that
specific failure.

## Data-source and universe rules

Only free, public, reproducibly downloadable data are eligible. A venue is
eligible only if byte-level G3 inspection finds sufficient historical trades,
multi-level book information, timestamps, contract metadata, and liquidation
records without paid access. Venue choice uses coverage, timestamp integrity,
and budget fit—not observed impact estimates.

The target universe is 30 linear perpetual-futures contracts. The formation
rule ranks all active and delisted contracts by trailing median daily notional
activity over a pre-training formation interval, applies documented continuity
and minimum-coverage rules, and retains the top 30. Delisted instruments remain
eligible; symbol redenominations and multiplier changes are mapped rather than
dropped. Exact formation dates and continuity thresholds will be appended after
G3 establishes what fields exist, before any training or holdout URL is fetched.

## Permitted G3 discovery access

Before bulk acquisition, G3 may fetch headers/metadata and at most one
symbol-day for each candidate file type. The preferred inspection date is
2024-06-17; if it is unavailable, use the earliest subsequent date common to
the candidate streams and record the substitution before opening the file.
Discovery files are design-only and permanently excluded from calibration,
training, identification, and holdout evaluation. The cumulative discovery cap
is 8 GB.

## Provisional sampling envelope

The capacity plan reserves four mutually disjoint externally defined regimes,
four full-day schema/calibration pilot dates, 48 six-hour training dates (12 per
regime), and 16 sealed six-hour holdout dates (four per regime), for 30 symbols.
These counts are an upper envelope, not permission to download. An amendment
must freeze the exact event source, event timestamps, matching rule, random
seed, dates, URLs, and inclusion probabilities before the first bulk request.

Regimes must be externally timestamped or predetermined. They may not be
defined using contemporaneous returns, order flow, estimated `Lambda`, or the
outcome under test. Matched controls are drawn from the complement using a
frozen seed and calendar-block strata. Every sampled unit records inclusion
probability `pi_i`; estimation uses inverse-probability weight `1 / pi_i` and
cluster-aware resampling.

The preregistered headline bin-width sweep is `100 ms, 250 ms, 500 ms, 1 s,
2 s, 5 s`. A monotone change in apparent cross-impact with bin width is treated
as evidence for asynchronicity/Epps contamination, not structural impact.

## Calibration boundary for G2 before G3

G2 precedes the data-inventory gate but requires defensible real-data
calibration. Its initial calibration must therefore use numerical summaries
from primary papers or public aggregate sources that have been opened and
verified, not locally downloaded market tape. If those sources cannot bound
factor strength and flow collinearity tightly enough, G2 does not pass; the
project records the gap rather than silently consuming G3 data early.

## Inference and specification control

- Time dependence is handled with a named HAC or block-bootstrap method whose
  block rule is fixed before the corresponding run. Cross-sectional and event
  clustering are preserved.
- Confidence level is 95% unless a gate explicitly defines another level.
- Each inferential artifact stores estimate, lower bound, upper bound, level,
  and method.
- `SPECIFICATION_LOG.md` supplies the complete trial count. Any return/P&L-like
  claim uses the preregistered Deflated Sharpe treatment; model comparisons use
  the relevant Model Confidence Set or loss-differential procedure.
- No neural model is eligible unless it beats the locked linear baseline under
  a Model Confidence Set.

## Holdout policy

Holdout files and manifests remain physically separate and gate-locked. G6 code
must reject holdout partitions. G7 records a single open event in
`SPECIFICATION_LOG.md`; after that event, parameter tuning, universe changes,
regime changes, and specification changes are prohibited. Forced-liquidation
events used for economics are disjoint from identification and must have known
size, side, and timestamp from a source not inferred from the same return/flow
outcomes.

## AMENDMENTS

None.
