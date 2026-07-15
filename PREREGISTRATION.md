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

### A001 — G2 source-constrained calibration and no-strawman opponent

- **Date:** 2026-07-15.
- **Reason:** The original freeze preregistered the G2 threshold and the rule
  that calibration must come from opened primary sources, but intentionally did
  not invent the unavailable structural tuple or conflate two different
  published opponent specifications. Primary-source inspection established
  what can and cannot be calibrated.
- **Amendment:** Freeze `configs/g2.toml`,
  `docs/G2_SOURCE_AUDIT.md`,
  `docs/derivations/GATE_G2_PREMISE.md`, and
  `docs/predictions/GATE_G2.md` as the detailed G2 contract. The confirmatory
  source box is the Cartesian product of two flow-factor strengths, two leading
  factor alignments, and two standardized own-feedback values. The focal pair
  is `(0, 1)`. Whole dates are the bootstrap unit. Paper-exact variants are
  reported separately from a strengthened integrated-OFI factor-control hybrid;
  oracle-`q` failure is required so measurement error alone cannot pass the
  gate.
- **Inference effect:** This narrows researcher degrees of freedom before code
  and makes the positive claim harder: all eight cells, an oracle-`q` opponent,
  adequate size/power, and the original 50%/three-SE event are required. The
  amendment does not change any G1 result or any empirical/holdout rule.
- **Access statement:** No external market tape, schema sample, evaluation
  observation, or holdout observation had been accessed. No G2 implementation,
  benchmark, validation panel, power panel, or research random draw had run.
  Only the primary papers listed in the source audit were opened.

### A002 — Replace the rejected G2 source box before any random draw

- **Date:** 2026-07-15.
- **Reason:** Three independent pre-run reviews reproduced A001's population
  arithmetic but rejected its scientific and operational contract. The power
  alternative was centered on a strict decision boundary; the confirmatory
  factor-response mapping was exactly uncontrolled OLS; the structural tuple
  mixed incompatible variables/frequencies; PC2/PC3 geometry made the focal
  pair depend on unsourced asset ordering; and the paper-block/CV/bootstrap
  workload was not executable from the promised checkpoints.
- **Amendment:** A001 is retained as a failed design record and superseded for
  execution by schema-version-2 `configs/g2.toml`, canonical
  `configs/g2_population_targets.json`,
  `docs/derivations/GATE_G2_PREMISE.md`, and
  `docs/predictions/GATE_G2.md`. The confirmatory observable point is the
  permutation-invariant one-factor covariance matching Capponi--Cont's
  one-minute leading flow/return shares and score alignment. `B = 0`; the
  structural off-diagonal varies continuously from `0.0029` to `0.0046`; the
  opponent receives oracle `q`, the correct factor direction, and an
  independent 95%-reliable proxy whose error variance is not disclosed to the
  estimator. Passage requires both a full condition-ridge projection and a
  pooled homogeneous three-slope projection to clear a strengthened
  50%/three-SE rule at all seventeen frozen structural grid points, after a
  candidate-specific boundary family-size union test and an
  actual-alternative joint-power intersection test.
- **Estimand effect:** Direct proxy-control flow coefficients are compared with
  `Lambda`. CCZ factor-residual reconstructions are secondary and compared with
  `Lambda P_perp`; their response-equivalent maps cannot replace that fair
  projected target. Hasbrouck--Seppi, Benzaquen, and Takahashi quantities not
  sharing the confirmatory variable/frequency are explicitly labeled
  comparators or structural sensitivities.
- **Null effect:** Passing supports a conditional-existence claim only. Failure
  at 95% reliability is unadjudicated, not a market null, unless a separately
  preregistered sharp upper bound over all source-compatible latent
  decompositions and reliabilities also lies below 50% with adequate power.
- **Execution authority:** A001/S0002 never became a committed executable
  boundary and grants no authority to access any G2 random stream. Only design
  `S0003`, config schema version 2, target schema version 2, raw target digest
  `c2122bbdbcf50181e028a689c502b5734673ed4a9e89765869f26108975f6122`,
  and 12-decimal semantic digest
  `b645468cd53357c968c272adff489a43e43e402b522fbfdbf2175e5f71dee00c`
  are executable. Implementations must hard-fail on a schema-version-1 G2
  config, rejected digest
  `a8475753e1cd70781c028680d7d782cbee73cb19b7265b93e8335eaa7f506fbf`,
  Fourier PC2/PC3 geometry, positive confirmatory `B`, or a
  response-equivalent confirmatory estimand.
- **Access statement:** No G2 implementation, resource benchmark, validation
  panel, research draw, external market tape, schema sample, evaluation
  observation, or holdout observation had been accessed. Only deterministic
  algebra and the already opened primary papers informed this correction.

### A003 — Make the observable and published opponents gate binding

- **Date:** 2026-07-15.
- **Reason:** A fresh three-lane hostile audit rejected S0003 before code or
  RNG. Its oracle-flow projections could fail even if measurement attenuation,
  regularization, or factor purging moved the observable published algorithm
  toward truth. The audit also found an ambiguous pooled intercept, colliding
  bootstrap keys, a non-reproducible cold/warm benchmark, an under-specified
  fold-local LASSO path, and a cache that discarded block-varying factor
  loadings. More oracle information is not an error-dominance theorem.
- **Amendment:** A002 remains a failed pre-run design record and is superseded
  for execution by design `S0004`, config schema version 3, and target schema
  version 3. The observable integrated-top-ten-OFI plus 95%-reliable
  proxy-control condition ridge is now gate binding at all 17 structural grid
  points. The oracle condition ridge and globally centered pooled homogeneous
  OLS are binding no-strawman checks. The registered CCZ `CI_I` protocol
  reconstruction is a separate binding published-model veto at the primary
  observable point and `o = 0.0046`; the other five reconstructions remain
  mandatory estimand-specific diagnostics.
- **Inference effect:** Positive G2 is the intersection of all 51 smooth
  candidate/grid events and the one frozen `CI_I` event. One hundred smooth
  validation superpanels use a nine-node proxy-noise-amplitude null grid from
  exact-factor recovery to each candidate/cell's sealed 50%-materiality root,
  and a 51-event joint power indicator at reliability 0.95. This licenses a
  finite null grid, not continuum-uniform size. `CI_I` must first recover a
  homogeneous diagonal `0.29` and focal cross coefficient `0.0046` in one
  full-`N`, full-`T` no-confounding panel and then clears the same named
  499-date-bootstrap rule in the sole research draw. Recovery additionally
  requires every one of the 31 point errors to be strictly below 50% and the
  focal material-bias declaration to be false; it is not called a size/power
  license.
- **Execution effect:** Bootstrap entropy now includes parent phase, parent
  scenario, and date count. The LASSO selects a common fold-relative penalty
  ratio and maps it to the outer-training `lambda_max`. The paper cache retains
  block-formed direct, purged, full-response, and projection operators. A
  fixed cold/warm benchmark must project every enumerated workload inside the
  one-/12-/three-/16-hour expected caps before validation. The
  two-/24-/six-/32-hour hard limits remain runtime stops, not admission slack.
- **Execution authority:** Only `S0004`, config schema version 3, target schema
  version 3, raw target SHA256
  `f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59`,
  and 12-decimal semantic SHA256
  `f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`
  may authorize G2 execution. Implementations must additionally hard-fail on
  S0003/schema-2 and its raw digest
  `c2122bbdbcf50181e028a689c502b5734673ed4a9e89765869f26108975f6122`,
  as well as every A002 rejection condition.
- **Null effect:** A single S0004 miss is failure of the sole preregistered
  finite-sample demonstration, not logical falsification of its known
  population law and not a premise-killing market null. The latter still
  requires a separately preregistered, adequately powered sharp upper bound
  over the source-compatible class.
- **Access statement:** No G2 implementation, benchmark, validation panel,
  research draw, external market tape, schema sample, evaluation observation,
  or holdout observation had been accessed. Only deterministic algebra,
  opened primary papers, and read-only hostile audits informed A003.

### A004 — Separate the strengthened hybrid from published reconstructions

- **Date:** 2026-07-15.
- **Reason:** The original H1 shorthand says “strongest published
  own-flow-plus-observed-factor baseline,” but source inspection established
  that CCZ publishes integrated top-ten OFI and cross-sectional-factor models
  separately. Calling their combination published would be a novelty and
  fidelity error.
- **Amendment:** For S0004, H1 is operationalized by two non-substitutable
  surfaces. The primary, fully licensed observable opponent is a deliberately
  strengthened integrated-top-ten-OFI plus correctly loaded noisy-proxy ridge;
  it is **not** attributed to CCZ. All six CCZ equations are separately labeled
  protocol reconstructions because the paper omits numerical choices, and
  `CI_I` is the binding published-equation veto because it alone combines
  integrated OFI with explicit cross coefficients. No result may call the
  hybrid paper-exact or claim that CCZ estimated it.
- **Inference effect:** Positive G2 still requires every one of the 51 smooth
  events and the `CI_I` veto. The separation prevents either an invented hybrid
  attribution or a nonbinding published diagnostic from carrying the claim.
- **Access statement:** No implementation, benchmark, validation panel,
  research draw, market tape, evaluation observation, or holdout observation
  had been accessed. The correction follows only from the already opened
  primary paper and hostile source audit.

### A005 — Seal one S0004 execution authority after hostile review

- **Date:** 2026-07-15.
- **Reason:** Three fresh read-only audit lanes accepted the final S0004
  population mathematics, inference map, opponent fidelity, RNG namespace,
  workload arithmetic, and compute admission only after twenty pre-run defects
  were diagnosed and repaired. The last repairs froze observable PCA and ridge
  numerics, every phase/scenario pair and distribution call, the literal
  binary64 LASSO ratio path and inclusive CV tie map, all mandatory frontier
  intervals, and the post-cold benchmark clock. No implementation or registered
  G2 random stream existed during those reviews.
- **Amendment:** A001--A004 remain immutable historical records. A001/S0002,
  A002/S0003, and every pre-D0031 candidate, estimator, veto, validation,
  workload, budget, key, or execution clause grant no current authority. The
  only S0004 contract is design/schema 3 in the exact sealed config and target
  artifacts below, interpreted by A003--A005 and D0031--D0049. Any conflict,
  stale digest, unlisted stream pair, or rejected-schema input is a hard failure,
  not an alternative implementation.
- **Seals:** Raw `configs/g2.toml` SHA256
  `f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc`;
  raw `configs/g2_population_targets.json` SHA256
  `f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59`;
  its 12-decimal semantic SHA256
  `f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`;
  and the little-endian float64 C-order LASSO-ratio-vector SHA256
  `1da884c55b3f6e7bf79012973bddf092a92efb1ea098cd2717a804645a62c9a0`.
  Changing any executable config byte requires a new logged specification,
  amendment, hostile audit, and clean hosted boundary before use.
- **Execution effect:** This amendment does not expose the resource,
  validation, or research streams. After an independent sealed-surface pass, a
  clean documentation commit, push, and hosted-green CI boundary, S0004 may be
  implemented test-first using test-only seeds. The resource seed becomes
  eligible only after implementation parity and hostile code review. Validation
  remains sealed until the distinct benchmark passes every expected admission;
  research remains sealed until every registered validation license passes.
- **Null effect:** The fixture's 95% proxy reliability and latent decomposition
  remain source-compatible modeling choices, not identified market facts. A
  positive result is conditional existence evidence. A miss is an unadjudicated
  S0004 failure and cannot activate the premise-dead branch without the separate
  sharp source-compatible bound already required by A003.
- **Access statement:** At this seal, no G2 implementation, resource benchmark,
  validation panel, research draw, external market tape, schema sample,
  evaluation observation, or holdout observation had been accessed. Only
  deterministic algebra, opened primary papers, local parser/hash checks, and
  read-only hostile audits informed A005.

### A006 — Bind registered Gaussian bytes to the declared target runtime

- **Date:** 2026-07-15.
- **Reason:** The first hosted test of S0004 implementation commit `682a381`
  found that NumPy 2.5.1 `Generator.standard_normal` is not byte-identical on
  the declared M4/arm64 runtime and hosted Linux/x86_64. Test-seed diagnostics
  established that the exact 150,000-word PCG64DXSM stream matches, 98 of 99
  Gaussian blocks match, and the only differing value is index 60,328:
  `0x1.f987e87be94a3p+1` on M4 versus `0x1.f987e87be94a2p+1`
  on Linux. This one-ULP 3.95-sigma value lies above NumPy's
  `3.6541528853610088` Ziggurat cutoff; the version-2.5.1 source computes that
  tail with platform `log1p`. NumPy's documented
  [stream guarantee](https://numpy.org/doc/stable/reference/random/compatibility.html)
  is conditional on the same build, environment, and machine, while
  [PCG64DXSM](https://numpy.org/doc/2.2/reference/random/bit_generators/pcg64dxsm.html)
  separately guarantees the integer stream for a fixed seed. The
  [version-2.5.1 source](https://github.com/numpy/numpy/blob/v2.5.1/numpy/random/src/distributions/distributions.c#L137-L177)
  is the primary implementation evidence for the tail-path diagnosis.
- **Amendment:** D0048's exact one-call distribution contract, every address,
  shape, seed, config byte, population target, validation threshold, and
  inferential rule remain unchanged. Registered resource, validation, and
  research authority is restricted to CPython 3.13.5, NumPy 2.5.1, little-endian
  Darwin/arm64 and additionally requires all five test-seed-1729 Gaussian
  known answers plus the level-noise raw-PCG known answer before any registered
  seed can be constructed. The fingerprint additionally hashes the Python
  build/compiler, NumPy build metadata, installed `_generator` binary, and OS
  release/build. An unknown runtime or failed preflight is a hard stop.
  Checkpoints and result manifests must record this numerical-runtime
  fingerprint and reject cross-fingerprint resume.
- **Hosted-CI effect:** Linux/x86_64 remains a software verification surface,
  not registered execution authority. It must reproduce the universal raw-PCG
  known answer, the exact NumPy call trace, and its predeclared test-seed
  Gaussian known answers; it must also prove that registered-runtime preflight
  rejects Linux before `SeedSequence`. Platform-specific test hashes may not be
  used as alternative research realizations or selected after seeing a
  registered result.
- **Inference effect:** None. This is a pre-data software-portability correction,
  not a new statistical specification, seed retry, or multiple test. The one
  realized G2 sample remains fixed by A005 plus the single authorized target
  runtime. Cross-platform byte-identical Gaussian replay is not claimed; a
  future demand for it requires a new design and portable transform before any
  affected registered access.
- **Access statement:** Only test seed `1729` was used to diagnose this failure.
  No resource, validation, research, empirical, evaluation, or holdout stream
  was accessed. The amendment precedes all registered G2 authority.

### A007 — Fix the smooth-estimator binary64 path before implementation

- **Date:** 2026-07-16.
- **Reason:** A pre-implementation contract map found four algebraically
  equivalent but not byte-equivalent choices left implicit by A005: centered
  scatter versus covariance units, packed-triangle layout, weighted-date
  accumulation, and the exact pooled singular-value routine. The sealed target
  file resolves the first choice because its oracle and observable penalties,
  `7.549327586206895e-7` and `7.687703503231941e-7`, are covariance-unit trace
  floors. The remaining choices affect storage or rounding, not the estimand.
- **Amendment:** Aggregate raw per-date cross-products under date weights,
  partial the one global intercept, and divide the resulting centered moments
  by the weighted row mass before proxy partialling or solving. Pack symmetric
  date moments with row-major `numpy.triu_indices`. Store checkpoint panels
  date-major in ascending `date_index` order and aggregate each flattened
  C-contiguous field panel with one `numpy.matmul` call. Point weights are
  float64 ones; bootstrap weights are the frozen float64 multinomial counts and
  must be finite nonnegative integers summing exactly to the date count. The
  pooled rank check uses `numpy.linalg.svd(..., compute_uv=False)`. Observable
  PCA uses the default-lower-triangle `numpy.linalg.eigh` result on
  `X_centered.T @ X_centered / 330` without an extra symmetrization.
- **Inference effect:** None. Covariance and scatter scaling give the same
  ridge and OLS coefficients in exact arithmetic because every registered
  penalty is degree-one homogeneous in the flow covariance. This amendment
  selects one replayable binary64 path and reproduces the already sealed
  penalty diagnostics; it does not change a target, threshold, seed, draw,
  confidence method, family rule, or trial count.
- **Implementation effect:** The typed sealed contract must project all
  estimator thresholds already present in `configs/g2.toml`; estimator code may
  not carry an unvalidated alternative set of magic constants. Low-level math
  helpers may be dimension-generic for analytic tests, while contract-bound
  builders enforce `N=30`, `T=330`, `L=10` and provenance. Full details and
  equations are in `docs/derivations/GATE_G2_SMOOTH_ESTIMATORS.md`.
- **Access statement:** No new stochastic call informed A007. The amendment was
  written from sealed artifacts, deterministic algebra, and three read-only
  implementation audits. Resource, validation, research, empirical,
  evaluation, and holdout data remain unaccessed; only the previously declared
  test-seed diagnostics exist.
