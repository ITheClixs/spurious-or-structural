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

### A008 — Bind transformed dates and smooth moments to their provenance

- **Date:** 2026-07-16.
- **Reason:** The first hostile C0003 review found that exact dataclass type,
  shape, and `date_index` checks did not prove origin. A manually constructed
  `G2Date` could reach the contract builder, and a base Gram from one design
  could be combined with cell cross-moments from another design sharing the
  same dimensions. Both paths could silently change an estimate without
  violating a numerical threshold.
- **Amendment:** `transform_date` mints a module-owned weak receipt binding the
  exact read-only transformed object, its full provenance snapshot, component
  identities, validated filtered-base identity, and a versioned content hash.
  Contract-bound estimator builders validate that receipt before constructing
  moments. Every smooth design, base moment, cell moment, and date-major panel
  carries a versioned SHA256 design digest plus its source-base identity;
  aggregation requires exact aligned equality before weighted multiplication.
  A contract-bound cell builder accepts a different structural response cell
  only when it has the same validated base identity and date index as the
  design. Full token construction and failure rules are derived in
  `docs/derivations/GATE_G2_SMOOTH_PROVENANCE.md`.
- **Inference effect:** None. This amendment rejects invalid compositions of
  already frozen moments. It changes no DGP, estimator, target, threshold,
  seed, draw, interval, family, or trial count.
- **Test prediction:** Red tests must first accept a forged transformed date
  and mixed base/cell panels under the old boundary. After repair, those cases,
  a different-base response, and any mutated receipt must fail before a solve;
  a deterministic `W=2Q` fixture must separately recover the pre-written oracle
  and observable ridge scalings.
- **Access statement:** No registered or empirical stream informed A008. The
  only prior stochastic smoke used authorized test seed `1729` and asserted
  shape/finiteness only; the failure was diagnosed from deterministic hostile
  constructions and code inspection.

### A009 — Separate complete contract panels from analytic algebra

- **Date:** 2026-07-16.
- **Reason:** A second hostile C0003 lane showed that any ascending subsequence
  could be treated as the whole panel and that dimension-generic `N=2/3`
  aggregates could call the same high-level fit functions as the sealed N=30
  design. The first path can drop a failed date; the second makes the generic
  test helper a production authority bypass.
- **Amendment:** Contract date records retain full minted stream, phase,
  scenario, declared date count, panel index, date index, source-base identity,
  and design digest. Contract stacking requires exactly the complete
  `0..n_dates-1` tuple under one prefix; a declared 48/96 frontier is distinct
  from a truncated 252-date panel. High-level ridge and pooled fits require a
  complete contract-origin aggregate with exact sealed `N=30`, `T=330`, and
  `L=10`. Dimension-generic analytic aggregation remains available only through
  pure moment-extraction and solver kernels that do not license a G2 estimate.
  Exact rules are derived in
  `docs/derivations/GATE_G2_SMOOTH_AUTHORITY.md`.
- **Inference effect:** None. The amendment rejects incomplete or unauthorized
  inputs before evaluating the already frozen estimator.
- **Test prediction:** Missing middle/tail dates, a truncated 252-date panel,
  mismatched panel prefixes, analytic high-level fits, and wrong sealed
  dimensions fail; pure analytic extraction plus solving retains the existing
  deterministic results.
- **Access statement:** No RNG informed A009. The failure was found by
  read-only code/protocol review after C0003 attempt 1.

### A010 — Bind response maps and require an issued aggregate

- **Date:** 2026-07-16.
- **Reason:** A pre-implementation critique of A008/A009 found that the shared
  base identity intentionally cannot distinguish structural cells, gamma-zero
  recovery, or transform metadata. It also found that copied provenance and
  design-digest fields remain self-attestation once the originating `X0` is no
  longer present in an aggregate.
- **Amendment:** Each transformed-date receipt and every cell moment/panel
  retains the exact `(target_index, paper_recovery, phi, reliability)` response
  map identity in addition to base identity and content hashes. Contract
  authority is minted through module-owned weak receipts at each in-memory
  stage: transformed date, contract date moment, complete contract panel, and
  contract aggregate. High-level G2 fits accept only the exact live aggregate
  object issued by that chain. Generic analytic objects never mint receipts.
  A future checkpoint loader must independently verify its complete manifest
  and content before minting a replacement receipt; no such loader is
  authorized in this slice. Full rules are in
  `docs/derivations/GATE_G2_SMOOTH_ISSUANCE.md`.
- **Inference effect:** None. The change preserves the same-base common-random-
  number design while preventing a response map or aggregate from being
  relabeled.
- **Access statement:** No RNG informed A010. It was written from a hostile
  architecture critique before the provenance repair was run.

### A011 — Issue the design wrapper and bind the expected response label

- **Date:** 2026-07-16.
- **Reason:** After C0004--C0006 was locally green, a fresh hostile construction
  found that an issued base Gram could be wrapped in a replaced
  `SmoothDateDesign` carrying an altered `X0`. The contract cell builder would
  then compute `X_bad'Y` while retaining the legitimate `X'X`, source receipt,
  and copied design digest. Separately, retaining response-map metadata in an
  aggregate did not require a high-level fit caller to assert that exact label.
- **Amendment:** Contract construction mints a weak module-owned receipt for
  the exact `SmoothDateDesign` wrapper as well as its base moment. The receipt
  binds the source receipt, design digest, `X0`, PCA diagnostics, and issued
  base-moment payload. Contract cell moments validate that design receipt
  before reading `X0`. Issued smooth tokens bind float64 dtype, shape,
  C-contiguity, read-only state, and bytes. High-level ridge and pooled fits
  require an exact expected `(target_index, paper_recovery, phi, reliability)`
  identity equal to the issued aggregate's common response identity, and the
  fit reliability must equal that identity's reliability. Details are in
  `docs/derivations/GATE_G2_SMOOTH_DESIGN_AUTHORITY.md`.
- **Inference effect:** None. The amendment closes wrapper and labeling
  authority without changing a DGP, moment, coefficient, target, threshold,
  seed, interval, family, or trial count.
- **Test prediction:** The old boundary accepts a replaced design with altered
  `X0` and a legitimate issued base moment. The repaired boundary rejects it
  before forming `X0'Y`; writable-state mutation and any expected response-map
  mismatch also fail before a solve.
- **Access statement:** No registered or empirical stream informed A011. The
  diagnosis used code inspection and the already authorized test-seed software
  surface only.

### A012 — Preserve reliability-neutral reuse and forbid callable minting

- **Date:** 2026-07-16.
- **Reason:** Hostile review of A011 found two conflicts before implementation.
  Exact equality between fit reliability and the transformed-date anchor would
  duplicate moments even though `X0` stores `f` and `e` separately and the
  sealed config requires deterministic reliability transforms to reuse the
  same moments. It also found that a callable generic registrar, or a private
  kernel that registers authority from a caller-supplied public receipt, would
  repeat the D0054 self-attestation failure.
- **Amendment:** Smooth contract moments are minted only from the canonical
  `contract.confirmatory_reliability = 0.95` date anchor. Their full date
  response map remains recorded. High-level fits require an expected response
  identity whose `(target_index, paper_recovery, phi)` equals the aggregate's
  common structural response law, while the fit reliability must equal the
  expected identity's reliability and may differ from the 0.95 anchor. Every
  issuance write is inline in the exact public contract wrapper immediately
  after live upstream validation. Generic/private numeric kernels never mint,
  and no callable generic registrar exists.
- **Inference effect:** None. The same polynomial moments and reliability
  transform were already frozen. This amendment preserves their intended reuse
  and closes a software capability route without changing a target, threshold,
  seed, draw, interval, family, or trial count.
- **Test prediction:** A copied receipt passed to a private numeric kernel
  cannot enter a contract stack. A non-anchor transformed date cannot mint a
  smooth design. The response-law validator accepts an exact structural label
  at a different registered fit reliability, and rejects any changed target,
  recovery flag, `phi`, or mismatch between expected and supplied reliability.
- **Access statement:** No new stochastic result informed A012. It follows from
  the sealed config's reliability-reuse clause, deterministic moment algebra,
  D0054, and read-only hostile review.

### A013 — Reject array subclasses at every smooth issuance boundary

- **Date:** 2026-07-16.
- **Reason:** Post-repair review found that issued tokens bound dtype, shape,
  layout, writable state, and bytes but not exact ndarray runtime type. A frozen
  issued wrapper can still be changed with `object.__setattr__`; an ndarray
  subclass with identical bytes can override transpose or matrix operations
  while reproducing the old token.
- **Amendment:** Every array hashed under a smooth issuance token must be an
  exact `numpy.ndarray`, exact float64, C-contiguous, read-only, finite value.
  Equality-compatible subclasses fail before hashing or downstream numeric
  dispatch. Analytic-only helpers retain their existing exact input checks.
- **Inference effect:** None. This rejects polymorphic software inputs and
  changes no stored valid array, estimator, target, threshold, seed, interval,
  family, or trial count.
- **Test prediction:** Under the pre-repair token, a read-only float64 C-order
  subclass view with identical bytes and an overridden transpose reaches cell
  moment construction. After repair it fails at design-receipt validation.
- **Access statement:** The diagnosis is deterministic code review. No new RNG,
  registered stream, empirical data, evaluation data, or holdout was accessed.

### A014 — Require exact retained receipt and provenance types

- **Date:** 2026-07-16.
- **Reason:** The same hostile review found that aggregate tokens and fit-label
  validation duck-typed retained receipts. A stateful equality-compatible
  object could reproduce the original payload during issued-token validation
  and expose a different response map during the following label check.
- **Amendment:** Any non-null retained receipt must be an exact `G2DateReceipt`
  containing exact `BaseProvenance`, `G2ResponseMapIdentity`, and `G2Stream`
  values plus exact Python scalar representations for every field. Receipt
  validation occurs in the common payload projection used by all issued smooth
  stages and again supplies the actual map used by fit-label validation.
- **Inference effect:** None. Valid receipts are unchanged; duck-typed software
  substitutes are rejected before numeric extraction or solving.
- **Test prediction:** Replacing an issued aggregate's response-receipt tuple on
  the same wrapper with duck-typed objects carrying equality-compatible fields
  currently passes the token and label checks. The repair rejects it before a
  high-level fit.
- **Access statement:** Deterministic code review only; no new RNG or data.

### A015 — Validate the full issued-wrapper schema before hashing

- **Date:** 2026-07-16.
- **Reason:** Issued tokens still projected wrapper scalars and containers
  through JSON without exact runtime-type checks. JSON collapses tuples and
  lists, while a value-equal `float` subclass can preserve `.hex()` but override
  reflected division used by covariance extraction.
- **Amendment:** Each issued smooth token first validates the exact wrapper and
  nested dataclass type, exact Python scalar types, exact tuple containers and
  member types, exact receipt types, and exact arrays. Only that validated
  schema is projected into the content token.
- **Inference effect:** None. All builder-produced objects already use these
  representations; only equality-compatible substitutions are rejected.
- **Test prediction:** Replacing an issued aggregate's `row_mass` on the same
  wrapper with a value-equal float subclass currently preserves its token. The
  repaired aggregate-token validation rejects it before fit arithmetic.
- **Access statement:** Deterministic code review only; no RNG or data.

### A016 — Snapshot caller sequences before smooth-panel validation

- **Date:** 2026-07-16.
- **Reason:** Final read-only contract review found that the contract cell
  stacker traversed a caller-supplied `Sequence` more than once. A stateful
  sequence could return legitimate issued moments during type, issuance, and
  provenance checks, then return changed unissued moments while arrays were
  stacked, allowing an issued panel and aggregate to contain numeric content
  that had never passed validation. The base stacker had the same multi-read
  shape even though its initial extraction list happened to close the observed
  route.
- **Amendment:** Contract and analytic smooth stackers materialize the supplied
  sequence exactly once into a local exact tuple, then perform every emptiness,
  type, issuance, provenance, dimension, metadata, and numeric read exclusively
  from that snapshot. No caller container is reread after materialization.
- **Inference effect:** None. Builder-produced lists and tuples preserve the
  same order and values. This closes a time-of-read software authority route
  without changing an estimator, target, threshold, seed, draw, interval,
  family, or trial count.
- **Test prediction:** Before repair, a state-changing complete 48-date
  sequence can pass cell-moment issuance validation and then substitute
  zeroed, unissued cross-moments into an issued aggregate. After repair, either
  the first snapshot is legitimate and those exact moments are stacked, or the
  snapshot contains a substitute and fails issuance before a panel is minted.
  The same one-read rule is regression-tested for both base and cell stackers.
- **Access statement:** The diagnosis and failing construction use only
  authorized test seed `1729`; no resource, validation, research, empirical, or
  holdout stream was accessed.

### A017 — Keep the design digest response-independent

- **Date:** 2026-07-16.
- **Reason:** Final code review compared two contract designs built from the
  same addressed base realization and identical `X0` bytes but different
  structural response cells. The implementation hashed the full transformed-
  date receipt into `design_sha256`, including target, recovery, reliability,
  and response-content fields, so the two otherwise identical designs received
  different digests. This contradicted A008 and the pre-code derivation, which
  define the design digest from the filtered-base identity plus `X0`.
- **Amendment:** `design_sha256` binds only the versioned design namespace,
  exact dimensions/date index, response-independent source identity, and exact
  `X0` array contract/bytes. The contract source identity is the validated
  filtered-base token. The analytic source identity is the literal
  `xid-g2-smooth-analytic-v1` namespace. Full transformed-date receipts remain
  in issuance tokens, where response identity belongs, but do not enter the
  reusable design digest.
- **Inference effect:** None. The valid `X0`, Gram, PCA, cell moments,
  estimators, targets, thresholds, seeds, draws, intervals, families, and trial
  counts are unchanged. This corrects checkpoint/cache identity and permits
  identical shared designs across structural cells to hash identically.
- **Test prediction:** Before repair, target 0 and target 16 transformed dates
  on the same issued base have identical base identity and byte-identical `X0`
  but different design SHA256 values. After repair, the design digests are
  equal while the design issuance tokens and response receipts remain distinct;
  cross-cell construction on the common base still succeeds only through the
  contract response builder.
- **Access statement:** The diagnosis uses only authorized test seed `1729` and
  deterministic digest comparison. No registered, empirical, evaluation, or
  holdout stream was accessed.

### A018 — Define checkpoint integrity without claiming impossible origin authentication

- **Date:** 2026-07-16.
- **Reason:** A010 deferred a future loader but did not define its trust root,
  manifest variants, completion ranges, atomic state machine, or authority
  restoration rule. Unkeyed hashes can detect corruption but cannot prove
  licensed origin against an actor who may rewrite a payload and recompute all
  hashes. Leaving that distinction implicit would make the checkpoint claim
  indefensible.
- **Amendment:** Persist separate complete date-major base-panel and cell-panel
  sufficient-statistic artifacts; never persist raw rows, `X0`, PCA matrices,
  aggregates, or weak receipts. Each success-last immutable artifact binds the
  four seals, exact contract/source/runtime identity, canonical full DGP address
  domain, complete date range, exact design and response receipts, separate
  design/response digests, exact NPY payload contracts, cumulative telemetry,
  and all content hashes. Stage-specific loaders snapshot and validate every
  file, reconstruct exact immutable panels, and mint only their own weak
  registry entry inline. No generic registrar exists. This slice accepts only
  test seeds `1729` and `9191`; registered seeds remain blocked pending a later
  runtime-preflight and resource-authority capability. The trusted-origin
  boundary is the local writer process plus checkpoint directory; coordinated
  same-user recomputation of all bytes and hashes is explicitly out of scope.
  The complete contract is derived in
  `docs/derivations/GATE_G2_CHECKPOINT_AUTHORITY.md`.
- **Inference effect:** None. The amendment serializes already frozen
  sufficient statistics and changes no DGP, estimator, target, threshold,
  interval, scientific family, or trial count.
- **Test prediction:** The current code fails because no loader exists. The
  repaired code must round-trip base/cell bytes exactly, regain authority in a
  fresh process without any RNG draw or upstream replay, reject the enumerated
  malformed, mixed, stale, substituted, and publication-fault classes before
  issuance, preserve cumulative resource accounting, refuse overwrite, and
  reject registered or otherwise unlicensed seeds before filesystem access.
- **Access statement:** Deterministic derivation and code review only. No RNG,
  registered stream, empirical data, evaluation data, or holdout was accessed.

### A019 — License one exact 252-date test-seed checkpoint recovery

- **Date:** 2026-07-16.
- **Reason:** The estimator derivation deferred a full-size recovery until its
  sample, tolerance, and prediction were written before the stochastic call.
- **Amendment:** After the deterministic checkpoint suite passes, run exactly
  one dedicated, non-pytest one-shot `master_seed=9191`,
  `VALIDATION_RECOVERY`, `n_dates=252`,
  `panel_index=0`, target-16, non-paper-recovery, `phi=0.60`,
  reliability-0.95 panel. Compare uninterrupted and post-GC reloaded base/cell
  arrays, receipts, digests, and all three smooth point coefficients by exact
  byte/SHA equality, with no positive tolerance. A fresh subprocess must
  reproduce the three coefficient hashes from checkpoints with every RNG draw
  path instrumented to fail. Combined artifacts must be below 12 MiB;
  expected/hard wall time is 30/120 seconds and expected/hard peak RSS is
  1/1.5 GiB. The runner records actual elapsed/RSS/hash/source/runtime evidence
  once and refuses overwrite. Exact procedure and stop rules are in
  `docs/predictions/GATE_G2_CHECKPOINT.md`.
- **Inference effect:** This is software recovery only. It makes no comparison
  with structural truth, no premise claim, and has no statistical interval or
  multiple-testing count.
- **Access statement:** A019 was recorded before seed `9191` was used for this
  run. No registered seed or empirical data was accessed.

### A020 — Bind the Make-only recovery launcher into execution-source identity

- **Date:** 2026-07-28.
- **Reason:** Hostile closeout made the Make target part of the one-shot
  authority boundary by freezing its path/thread constants and pre-import
  symlink checks. The existing six-path source snapshot covered the Python
  implementation and frozen configs but omitted `Makefile`; a modified
  launcher could therefore remain outside the attempt hash and the public
  clean-source predicate.
- **Amendment:** Add the repository-root `Makefile` as the seventh declared
  execution-source path for checkpoint/recovery identity. Its exact mode,
  bytes, size, and SHA256 enter the same canonical tracked-plus-untracked
  snapshot as `src/xid`, the two G2 configs, `pyproject.toml`, `uv.lock`, and
  `.python-version`. Public A019 preflight requires this expanded declared
  snapshot to be clean and stable before `attempt.json`; checkpoint roots
  remain disjoint from every declared path.
- **Inference effect:** None. This strengthens launcher provenance and changes
  no DGP, estimator, address, target, threshold, interval, trial count, or
  stochastic realization.
- **Test prediction:** Before implementation, source enumeration does not
  observe `Makefile`. After implementation, a behavioral spy over the stable
  source-file identity function observes `Makefile`, its bytes change the
  snapshot hash, and ordinary source/runtime bracketing remains green.
- **Access statement:** Amendment and deterministic test design only. Seed
  `9191`, every registered G2 stream, empirical data, evaluation data, and the
  holdout remain untouched.

### A021 — Report the test-smoke RNG address without recovery relabeling

- **Date:** 2026-07-28.
- **Reason:** The seed-1729/48-date supervisor smoke intentionally draws the
  already licensed `VALIDATION_DATE_FRONTIER` test address so pytest cannot
  instantiate the exact A019 recovery address. Its in-memory spec and public
  test receipt nevertheless said `VALIDATION_RECOVERY` and phase/scenario
  `23/0`, while checkpoint construction actually used date-frontier
  phase/scenario `22/2`. A software-procedure label cannot override the
  stochastic address in evidence.
- **Amendment:** The test-only `RecoveryRunSpec`, `attempt.json`, worker
  contract, and result receipt must name the actual
  `VALIDATION_DATE_FRONTIER` stream and contract-derived `22/2` phase/scenario.
  Remove the stream-substitution helper. The phrase “seed-1729 recovery
  supervisor” describes checkpoint/write/drop/reload/fresh-process procedure
  only; it is not an RNG-stream claim. Public A019 remains exactly seed 9191,
  `VALIDATION_RECOVERY`, 252 dates, phase/scenario `23/0`, and cannot appear in
  pytest.
- **Inference effect:** None. No stochastic input changes; this corrects
  receipts to the stream already drawn and changes no estimator, target,
  threshold, interval, trial count, or public A019 address.
- **Test prediction:** Before repair, the seed-1729 result asserts recovery
  although its checkpoint receipts are date-frontier. After repair, spec,
  attempt, checkpoint receipts, and result agree on
  `VALIDATION_DATE_FRONTIER`/`22/2`, exact fresh-process hashes remain equal,
  and public A019 tests still fail before construction.
- **Access statement:** Governance correction from existing seed-1729
  software-smoke evidence only. Seed 9191, every registered G2 stream,
  empirical data, evaluation data, and the holdout remain untouched.

### A022 — Replace the non-executable resource bundle with an operand-complete admission experiment

- **Date:** 2026-07-28.
- **Reason:** The frozen resource plan named fourteen production kernels but
  timed one nominal unit of each and admitted from the last three warm
  equal-context bundles. That bundle cannot construct an honest 252-date
  base/cell panel from one date, cannot construct a paper cache from one paper
  date, leaves cheap kernels vulnerable to clock resolution, and does not test
  transfer from an equal mixture to the radically different validation and
  research mixtures. Artifact, capability, resume, RSS, and disk authority
  were also not executable. These failures were diagnosed before method
  selection and before any registered resource access.
- **Narrow supersession:** Preserve unchanged the fourteen kernels, the full
  validation/research work matrix `W`, DGP, estimators, targets, thresholds,
  interval family, phase/scenario map, registered seeds, one-/12-/three-/
  16-hour expected budgets, two-/24-/six-hour hard stops, 480-second task cap,
  3.5-GB RSS cap, decimal 2,000,000,000-byte checkpoint cap, and all scientific
  trial counts in `configs/g2.toml`. Supersede only (a) the one-unit
  `benchmark_bundle`, (b) the last-three equal-context warm rate as the sole
  admission statistic, (c) the undefined larger publication payload, and
  (d) ambiguity over combined I/O work. The sealed `configs/g2.toml` remains
  byte-unchanged; `configs/g2_resource.toml` must bind it and this amendment.
- **Fixed operand block:** One cold or equal-context block has exact kernel
  units
  `252,252,25,225,225,225,4096,1,1,1,1,1,6048000/53298000,1`
  for `k1..k14`, where the two `k13` values are separately timed recovery and
  research variants. The 4,096 `k7` calls reuse one exact 499-value fixture
  and must be byte-identical; frozen phase/task work remains `k7=1`. The
  recovery paper cache is one little-endian float64 `(252,960)` fixture; the
  research cache is four `(63,8460)` shards. Rows repeat one actually issued
  paper-date summary and are benchmark-only: every scientific loader rejects
  them. The larger publication is exactly 50 little-endian float64
  `(595000,)` shards, 238,000,000 numeric bytes total, with construction,
  hashing, fsync, success-last publication, reload, validation, and cleanup
  timed.
- **No adaptive timing choice:** Before registered authority, exactly three
  test-seed-1729 measurability rehearsals use panel indices
  `10000,10001,10002`. Fixed subblocks
  `k3=25,k4=225,k5=225,k6=225,k7=4096` must each last at least 100,000,000 ns
  in every rehearsal. In all three rehearsals the complete one-unit k14
  envelope-plus-terminal-close-probe must also satisfy
  `ceil_div(25*D_plus,12) <= 480,000,000,000` ns; this licenses only the fixed
  k14 task projection. Every rehearsal has `r=0`, so this persisted
  `D_plus` is exactly equal to `Aplus`; the legacy field name is a zero-replay
  alias, not permission to use `Rplus` in a registered absolute projection.
  It supplies no terminal-close latency bound.
  As corrected before implementation by A024, the same rehearsal publishes
  one worker-ready plus fourteen work boundaries and four cleanup intents per
  panel: all 57 work/publication/marker intervals must be at most 480/60/540
  seconds without adapting a count. Bootstrap from the
  first supervisor instruction through durable `attempt.json` must also be at
  most 480 seconds.
  Counts and addresses are frozen in
  `configs/g2_resource.toml` before rehearsal; measured evidence publishes
  success-last under `results/g2_resource_rehearsal/` and is bound by the
  later quantitative prediction seal, never written back into the config.
  Execute exact command `make g2-resource-rehearsal` once with no timing retry
  after its disjoint result/checkpoint/scratch roots are absent. Separately
  named test-stage codecs require exact `TestRngNamespace` and are rejected by
  every registered loader; both stages share only private production
  serialization/validation functions.
  Failure requires an append-only amendment; it cannot select a larger count,
  retry a rehearsal, tune a private kernel, or inspect a registered
  realization.
- **Registered address schedule:** Registered resource panels are claimed
  durably and contiguously as `b=0,1,2,...`; gaps, duplicates, caller-selected
  indices, or reassignment to a different trace are terminal. A lost current
  position may be deterministically re-executed under the same reservation
  only with the replay evidence and penalty below. Panel zero is the cold
  `EQUAL` trace.
  Thermalization consumes one panel per role in exact repeated order
  `V,R,R,V` until a complete four-role cycle ends after at least 600 seconds
  of successful completed work.
  Each of exactly three warm blocks consumes one `EQUAL` panel, then repeats
  `V,R,R,V` for at least two cycles and until a complete cycle ends after at
  least 200 seconds of successful completed work. Replay penalties cannot
  shorten either stop. No fourth warm block may be added. Every reservation
  precedes its first draw and enters immutable evidence.
- **Timing and falsification:** Use integer `perf_counter_ns`, clock resolution
  `h`, raw `D_plus=D+2h`, replay count `r`,
  `D_admission_plus=D+480000000000*r+2h`, and
  `ceil_div(a,b)=(a+b-1)//b`. Cold projection is
  `ceil_div(5*W*D_admission_plus,3*U)`. Sequential total and phase-specific pair
  throughput must satisfy
  `20*N_j*D_(j-1) >= 19*N_(j-1)*D_j` for warm blocks 2 and 3. For held-out
  block `j`, phase `p`, kernel `k`, and other blocks `a,b`, define
  `H[j,p,k]=max(ceil_div(U[j,p,k]*Aplus[a,p,k],U[a,p,k]),`
  `ceil_div(U[j,p,k]*Aplus[b,p,k],U[b,p,k]))`, where `Aplus` sums
  replay-penalized conservative durations, and
  `H[j,p]=sum_k H[j,p,k]`. Require
  `Oplus[j,p] <= ceil_div(5*H[j,p],4)` for both phases and all three held-out
  blocks. Final phase projections take the slowest of cold, all three equal,
  and all three applicable phase contexts per kernel, add exact startup, then
  multiply by 1.25. The complete phase/task vectors and integer formulas are
  frozen in `docs/derivations/GATE_G2_RESOURCE_ADMISSION.md`.
- **Capability and artifact authority:** Add a separate
  `ResourceRngNamespace`; never widen `TestRngNamespace`. Its only factory
  consumes a supervisor-minted one-use anonymous-pipe capability bound to the
  attempt, worker PID/start identity, source/runtime/config hashes, and nonce.
  The child blocks before authority: the supervisor derives the payload,
  publishes and validates the complete worker claim/marker containing its
  hash, and only then writes the pipe; the child validates that pair before
  its factory can construct the namespace.
  It can issue only seed `2026071529` at `RESOURCE_SMOOTH` and
  `RESOURCE_PAPER` addresses and cannot construct validation or research
  coordinates. Preserve existing exact `base-panel` and `cell-panel` byte
  schemas, kinds, paths, hashes, and weak-issuance semantics, while leaving
  their C0015 test-only entry points unchanged. Separately derived
  resource-stage entry points accept only exact resource authority. Panel
  manifests retain the original seven-path source snapshot. Test rehearsal and
  registered execution share one exact eight-path executable snapshot, adding
  `configs/g2_resource.toml`; outer A022 receipts additionally bind the
  expanded 13-path authority snapshot plus exact panel hashes and tokens.
  Every new reservation, null, paper, cache, bootstrap,
  publication, trace, measurement, attempt, result, and failure artifact must
  match the pre-code byte authority in
  `docs/derivations/GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md`; success/failure is
  published last and the 5-MiB per-payload ceiling remains binding.
- **Source, process, and storage authority:** Bind the exact tracked-plus-
  untracked, clean, stable A020 snapshot algorithm separately over the
  seven-path panel, eight-path executable, and 13-path authority tuples frozen
  in the admission derivation. No config contains its own digest. The
  registered executable digest must equal the fixed rehearsal digest. Before
  the first worker, run exactly one twelve-child full Git check and persist its
  complete source/control/output/wait/rusage rows in `attempt.json`.
  Subprocess-free stable-byte source/control seals reconstructed against that
  bootstrap check run before and after sealed contract/resource-config loading,
  immediately before and after every nonterminal resource-root mutation, before
  every worker capability, and after every measurement block. After every
  issued worker identity is closed, no worker is alive, and every currently
  waitable direct child has been reaped, run exactly one second twelve-child
  full check, persist it in the selected terminal JSON, and permit no other
  preterminal Git subprocess. Require the three canonical resource roots absent
  before a new
  attempt. Sample the
  process tree every 50 ms by PID plus kernel start identity; reconcile every
  child through `wait4`/Darwin byte-normalized `ru_maxrss`. A sampler gap,
  unaccounted descendant, or process-identity mismatch is terminal. Route all
  temporary/cache writes into the three roots and scan logical plus allocated
  bytes at every mutation. The resource supervisor holds exclusive ownership
  and pre-reserves each complete panel mutation against the stricter decimal
  checkpoint cap before the shared serializer; the generic codec ceiling
  cannot widen it. Require resource transient at most 6 GB, baseline plus
  transient at most 30 GB, baseline plus terminal at most 25 GB, and 25%
  headroom inside both RSS and checkpoint caps. Invalid/partial panel finals
  are terminal and never regenerated in place.
- **One attempt and resume:** The public command is exactly
  `make g2-resource-benchmark`, with one logical seed-`2026071529` attempt and
  no seed retry. Durable boundaries publish after worker readiness, every
  kernel position including zero-unit positions, every trace receipt, and
  every measurement receipt. Work from the predecessor marker through the
  next cutoff is capped at 480 seconds; atomic boundary publication has a
  separate 60-second upper, so every durable-marker interval is at most 540
  seconds. Pre-attempt bootstrap through durable `attempt.json` has its own
  480-second watchdog. A work timeout is terminal. A supervisor-recorded
  termination signal, changed boot with the old PID/start absent, or exact
  same-boot dead-worker proof may resume from the latest complete boundary. A
  partial trace continues only its exact next position under the same
  reservation; a partial measurement block retains every completed
  measurement-role trace.
  A lost execution adds a fixed 480-second replay penalty and its full
  licensed RNG-call upper to all admission formulas, so loss cannot improve a
  result. Atomic nonterminal receipt directories expose no torn pair; one
  uniquely implied hidden stage is inventoried, bound, and idempotently
  deleted, while an exact valid final is reused byte-for-byte. Completed
  receipts, prefixes, measurement blocks, and stationarity/transfer/cap/
  failure verdicts are irrevocable; claimed panels are never reassigned.
  Each complete boundary carries
  nondecreasing conservative RSS and created-root uppers that enclose its own
  publication; resume keeps those uppers separate from actual observed
  telemetry and never reapplies the 25% margin to a carried RSS upper. After
  completing any suspended trace, a resumed process starts a new thermal
  epoch and accumulates 600 seconds of successful thermalization before any
  later warm trace; an active block then continues its next measurement-role
  pair. Cumulative timing starts at the first
  resource-supervisor bootstrap instruction before project import, preflight,
  baseline measurement, or root mutation; external Make/shell/uv/interpreter
  launch latency is explicitly outside that measured scope. The terminal
  result measures cumulative active elapsed only through the exact
  pre-encoding accounting cutoff. As superseded by A025 before implementation,
  acceptance adds a separately reported fixed 60-second terminal accounting
  charge that is independent of kernel-14 timing; it is a projection
  convention and never claims to measure its own later fsync. No powered-off
  interval is subtracted because no trustworthy
  prior-shutdown timestamp exists; `excluded_poweroff_ns=0`.
- **Execution gate and prediction:** The current repository is predicted to
  fail closed before RNG because the production kernels, typed compute parser,
  resource capability/config/runner, and exact new artifact codecs do not yet
  exist. Implementation begins under test seeds only. Before any registered
  resource authority, all fourteen production paths must recover known truth
  where applicable, deterministic hostile tests must pass, the exact
  test-seed timing/RSS/disk evidence and quantitative registered prediction
  must be append-sealed in `docs/predictions/GATE_G2_RESOURCE.md`, two hostile
  reviews and hosted CI must pass on the exact clean SHA, all roots must be
  absent, and the human must explicitly authorize the irreversible Make
  command. No derivation or test alone licenses it.
- **Inference effect:** None. A022 is an engineering admission design. It
  cannot report coefficients, truth comparisons, bias, power, premise
  outcomes, or scientific intervals. Deterministic failure classes and
  resource timings add zero scientific trials.
- **Access statement:** This amendment, its derivations, prediction, and
  hostile design reviews were written before resource-run implementation.
  Registered resource seed `2026071529`, validation seed `2026071521`,
  research seed `2026071522`, empirical data, evaluation data, and the holdout
  remain untouched.

### A023 — Narrow A022 to conditional projection and close byte-authority gaps

- **Date:** 2026-07-29, before resource-run implementation or any A022
  rehearsal.
- **Reason:** Fresh hostile review found that A022's fixed phase traces are not
  proportional to the frozen work matrix `W`. No nontrivial exact proportional
  trace exists: if `alpha=a/b` is reduced, integrality at kernel 14 where
  `W[p,14]=1` forces `b=1`; removing kernel 14 still leaves greatest common
  divisor one in both phases. The existing same-phase held-out formula tests
  temporal stability only, not transfer to a realized full-workload mixture.
  A separate systems review also found underdetermined registry, rehearsal
  identity, NPY-header, stage/debris, retained-inventory, and disk-accounting
  bytes.
- **Narrow supersession:** Preserve every A022 RNG address, panel schedule,
  cold/equal/validation/research trace vector, kernel atom, artifact payload,
  cap, stop, frozen `W` count, and no-adaptation rule. Supersede only A022's
  full-mixture transfer interpretation and the incomplete byte encodings named
  here. The corrected claim is: on the frozen runtime and resource address
  law, all production kernels are timed in operand-complete cold/equal
  contexts and two fixed, non-`W`-proportional phase-labelled stress contexts.
  Admission is conditional on per-kernel linear extrapolation from the
  slowest admissible context to `W`. The blocked checks establish temporal
  stability and cross-context robustness of shared kernels; they do not
  establish exact transfer to the full validation or research mixture.
- **Temporal and cross-context falsifiers:** Retain A022's same-phase
  leave-one-warm-block-out `H[j,p,k]` formula and aggregate 1.25 check as
  `temporal_checks`. For held-out block `j`, phase `p`, other phase `q`, and
  other blocks `a,b`, freeze
  `C={1,2,3,4,5,6,7,8,9,10,14}` and define
  `X[j,p,k]=max(ceil_div(U[j,p,k]*Aplus[a,q,k],U[a,q,k]),`
  `ceil_div(U[j,p,k]*Aplus[b,q,k],U[b,q,k]))`.
  Require both
  `Aplus[j,p,k] <= ceil_div(5*X[j,p,k],4)` for every `k in C` and
  `sum_C Aplus[j,p,k] <= ceil_div(5*sum_C X[j,p,k],4)`.
  The exact six temporal and 72 cross-context receipt rows are frozen in the
  A022 derivations. Kernels 11, 12, and both kernel-13 variants stay outside
  the cross-phase set and use cold/equal/own-phase slowest rates.
- **Byte-authority correction:** Before A024's two private resume-wrapper
  classes, count the four A022 issuable new wrapper classes
  in one ninth weak `_RESOURCE_ARTIFACT_REGISTRY`; all live-count vectors have
  nine entries. Rehearsal attempt/trace/result/failure receipts bind panel,
  executable, and historical authority snapshots; only the executable digest
  must equal registered execution because the later prediction seal changes
  governance bytes. Freeze the literal NumPy-1.0 118-byte header grammar,
  deterministic artifact/receipt/file stage names, complete debris rows and
  final-leaf digests, full rehearsal artifact-inventory rows, six-digit octal
  no-follow disk rows, repository-relative outside-baseline coverage, and
  positive `f_frsize`-else-`f_bsize` allocation units. The exact encodings in
  `docs/derivations/GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md` control.
- **Inference effect:** None. This correction weakens an engineering
  interpretation and strengthens falsification/provenance. It changes no
  scientific hypothesis, estimator, interval, threshold, or trial count.
- **Access statement:** A023 was written from document review and deterministic
  local checks only. No A022 rehearsal, registered resource, validation,
  research, empirical-data, evaluation-data, or holdout access occurred.

### A024 — Make A022 restartable without persisting raw statistical state

- **Date:** 2026-07-29, before resource-run implementation, any A022
  rehearsal, or any registered G2 access.
- **Reason:** Fresh hostile recovery review found that A022's boundary after
  kernel 1 is not executable. Kernel 2 requires the exact live issued raw base
  and `SmoothDateDesign`, including `X0` and PCA state; the durable boundary
  stores only timing metadata. Later boundaries likewise omit the bootstrap
  weights and candidate focal values required by subsequent kernels. A worker
  or boot loss therefore could not continue the claimed next position without
  either redrawing RNG, silently replaying completed stochastic work, or
  inventing unregistered operand bytes. The same review found that kernel 8's
  null-batch manifest names kernel-9/10 panel artifact hashes before those
  artifacts exist in the A022 order.
- **Narrow supersession:** Preserve all seeds, address domains, panel counts,
  fourteen kernel definitions, unit counts, numerical procedures, artifact
  payloads, phase vectors, frozen work matrix `W`, rates, falsifiers, budgets,
  and scientific interpretations. Supersede only A022's record order,
  per-position boundary claim, and missing resume-state lifecycle. The exact
  15-record order is now
  `(k1,k2,k3,k4,k5,k6,k7,k9,k10,k8,k11,k12,k13-recovery,`
  `k13-research,k14)`. Moving only the three smooth I/O records makes the
  base artifact precede the cell artifact and both precede the null artifact
  that binds their hashes; the numerical dependency `k7 -> k8` remains
  intact. Because k8, k9, and k10 each have one unit in every trace role, the
  three exact numerical unit vectors remain byte-for-byte unchanged.
- **First operand epoch:** Kernels 1 and 2 remain individually timed in their
  canonical order but form one indivisible operand epoch. There is no durable
  boundary between them. The first kernel boundary is published only after
  both records and their resume-only panel state are durable. A literal
  `480,000,000,000`-ns watchdog covers the combined work from the worker-ready
  marker through the pre-boundary cutoff, and the boundary publisher retains
  its separate `60,000,000,000`-ns cap. Any rehearsal in which this fixed
  epoch does not fit fails; no count, date, shape, or timing denominator may
  adapt. One non-durable cumulative monotonic cutoff is sampled after all k1
  work and before any k2 work. It is the exact k1 accounting end and k2
  accounting start, so the two record durations partition the epoch exactly
  without overlap. Registry conformance is epoch-level: all nine registries
  equal the pre-k1 baseline before k1; k1's raw/design authority may remain
  live only through the internal cutoff and its retained/high-water vector is
  recorded; after k2 state issuance, release, and collection, all nine counts
  must again equal baseline before the durable boundary.
- **Minimal resume state:** The first boundary binds separate immutable
  resume-only base and cell sufficient-statistic artifacts containing exactly
  the existing panel payload arrays: base `x0tx0_upper (252,2016)` and cell
  `x0ty (252,63,30)` plus `yty_upper (252,465)`, totaling exactly
  `8,811,936` numeric bytes. They are distinct from the later timed k9/k10
  production artifacts. After k3, one immutable artifact stores the exact
  `(25,252)` float64 bootstrap-weight matrix, its licensed address inventory,
  and the ordered digest of the 25 aggregate outputs. After each of k4, k5,
  and k6, one immutable candidate artifact stores the exact focal array:
  `(25,9)` in rehearsal/equal/validation roles or `(25,1)` in a research
  role, plus the complete fit-output inventory digest. Resume loaders are
  private, stage-specific, attempt-bound, and benchmark-only; they reissue
  only the existing immutable panel types or private weight/focal wrappers.
  Scientific, validation, research, coefficient-to-truth, and generic
  registrars reject every resume kind. Raw normals, `X0`, PCA matrices,
  aggregate objects, and fit objects remain unpersisted. Before each of k4,
  k5, and k6, both ordinary continuation and resume load the saved panels and
  weights, deterministically recompute all 25 aggregates, verify the frozen
  aggregate digest, and charge that reconstruction to that record's prelude.
  They release and collect those objects before the boundary and never redraw
  RNG. Ordinary and resumed execution therefore have one operand path.
- **Boundary and replay correction:** Each trace now has one worker-ready
  boundary plus 14 work boundaries: after the indivisible k1+k2 epoch and
  after each remaining record. Their exact next-position sequence is
  `[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15]`. The three fixed rehearsals
  therefore publish exactly 45 boundary leaves, not 48. Every boundary carries
  a sorted, path-complete resume-state inventory and the exact completed record
  prefix. A loss before the next boundary replays only the current indivisible
  epoch or record under the same reservation and address schedule, with the
  fixed replay penalty and full licensed RNG upper; no prior durable prefix is
  rerun. An uncommitted valid final is bound and removed before replay rather
  than reused as if its missing timing record existed. A lost k1+k2 epoch has
  one epoch replay ordinal `r`, but both eventual records carry
  `replay_count=r`, `replay_penalty_ns=480000000000*r`, and only their own
  complete licensed RNG-call sequence repeated `r` times in their upper
  inventories. This deliberately conservative double admission charge keeps
  neither per-kernel rate eligible to improve through interruption selection;
  lifecycle and cumulative elapsed count the physical epoch only once.
  Boundaries store an exact two-position pending-epoch object rather than
  pretending that either record was independently durable.
- **Cleanup journal:** Before any timed last-use deletion, publish one
  immutable cleanup-intent receipt binding the predecessor boundary, completed
  successful-work fields, complete artifact/resume-state rows, and exact
  descending-path deletion order. Cleanup then continues idempotently across
  worker or boot loss, and the following boundary closes the originating
  record's full prelude/kernel/epilogue and five-substage duration. A cleanup
  intent cannot authorize new numerical work, RNG, a different deletion
  order, or a different terminal outcome. Resume-only smooth state remains
  available through k8, whose intent removes the null artifact, production
  base/cell artifacts, and all smooth resume operands; recovery/full paper
  parents remain available through their exact k13 consumers. The byte
  schemas, receipt inventories, failure
  limits, and no-marker forensic-incomplete branch are frozen in
  `docs/derivations/GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md`.
  Each equal/test trace has exactly four cleanup intents, so the three
  rehearsals have 45 boundary leaves, 12 cleanup-intent leaves, and 57
  checkpoint intervals whose work/publication/marker caps all must pass.
- **Interruption and terminal-selection correction:** A worker capability is
  released only after its claim, reservation, and worker-ready marker all
  validate. Loss before the first worker-ready boundary is terminal before
  `SeedSequence`, not an invented resume point. A registered interruption may
  chain through further supervisor loss before a new worker-ready boundary;
  the chained receipt carries the same boundary, complete trace-progress
  object, next position, pending replay, debris, and recovery action without
  adding another replay ordinal. A clean boundary signal likewise preserves
  any already-pending replay count. A resumed worker-ready copies every
  trace-start/reservation/progress field and advances nothing. An exact marked
  trace or measurement receipt may complete only its uniquely derived missing
  following boundary. Ordinary and supervisor-only cleanup suffixes retain the
  480/60/540-second watchdogs.

  Terminal failure is selected before destructive cleanup by one immutable
  failure-intent receipt that binds the failure identity, durable
  receipt/artifact/RNG/log evidence, and the complete checkpoint/scratch
  deletion order. Once marked, it forbids all ordinary work, RNG, success, or a
  different failure. Cleanup may continue only through contiguous
  failure-resume receipts and an exact missing-prefix/remaining-suffix state;
  the final failure JSON reproduces the intent and publishes `_FAILURE`
  success-last. A crash during terminal cleanup can therefore delay evidence
  closure but cannot change the selected outcome.
- **Configuration and review gate:** `configs/g2_resource.toml` is a
  preregistered source artifact, not a measured result. Its exact LF-terminated
  bytes, digest, key/type schema, source tuples, reordered record list,
  boundary count, roots, addresses, caps, shapes, schedule, and registry names
  must be frozen in the artifact authority before implementation. The
  corrected package requires two fresh independent hostile passes, the locked
  local suite, and hosted CI before any test-seed rehearsal.
- **Inference effect:** None. A024 repairs persistence and dependency order for
  an engineering benchmark. It does not inspect or change a coefficient,
  truth comparison, interval, threshold, trial count, or scientific gate.
- **Access statement:** A024 was derived from source and document inspection
  only. No A022 rehearsal, registered resource seed `2026071529`, validation
  seed `2026071521`, research seed `2026071522`, empirical data, evaluation
  data, or holdout was accessed.

### A025 — Close the A024 hostile state-machine audit before implementation

- **Date:** 2026-07-29, before resource-run implementation, any A022
  rehearsal, or any registered G2 access. Amendment A025 is independent of
  assumption A025 in `ASSUMPTIONS.md`.
- **Reason:** Three fresh hostile reviews of the A024-corrected package still
  failed it. They found receipt-publication crash states with no transition,
  whole-leaf cleanup rows that could not represent a crash after one child
  unlink, an uncheckpointed terminal-cleanup suffix, underdefined failure
  clocks and process-death bytes, a reservation/current-worker identity
  contradiction, an ambiguous post-interruption thermal rule, telemetry that
  a lost supervisor could erase, no finite terminal-JSON liveness bound, a
  missing paper-bootstrap-weight lifecycle, and an unbounded terminal-success
  tail. A subsequent exact methods review also found that replay-penalizing
  both a held/current duration and its predictor/reference duration can make a
  failed stationarity or transfer check pass after an interruption. These are
  pre-code specification failures; no result was observed. The same freeze's
  systems re-review additionally found that spawn preceded durable child
  identity, Darwin absence evidence lacked an executable syscall truth table,
  a dead final-success boundary could fall through generic adoption, worker
  deadlines were not precommitted by the authorizing receipt, and the
  failure-intent size proof did not cover every terminal file shape.
- **Narrow supersession:** Preserve A022--A024's seeds, address domains,
  record order, numerical kernels, unit vectors, work matrix, estimators,
  thresholds, budgets, and conditional interpretation. Supersede only the
  failed receipt, cleanup, interruption, evidence-carry, RNG-lifecycle, and
  terminal-close clauses and the replay-timing comparator operand roles with
  the exact A025 authority below, including durable launch/birth receipts,
  factorized Darwin absence evidence, watchdog-arm provenance, non-adoptable
  terminal entry, and all-terminal size preflight. In particular, earlier
  A022--A024 uses of a
  replay-penalized duration on the predictor/reference side are historical and
  superseded. If an earlier A022--A024 sentence conflicts with A025, A025
  controls and the validator must reject the historical branch.
- **Exact successful RNG sequences:** Let `D(s,d,c)` denote the existing
  13-word DGP address for stream `s`, date `d`, and component `c`, and let
  `B(s,r)` denote the existing 13-word bootstrap address for stream `s` and
  replicate `r`, always with the current reserved panel. In record-position
  order, the complete successful call sequences are:

  ```text
  position 0:  [D(resource_smooth,d,c)
                for d in 0..251, then c in 1..5]
  position 2:  [B(resource_smooth,r) for r in 0..24]
  position 10: [D(resource_paper,0,c) for c in 1..5] if units > 0, else []
  position 11: [D(resource_paper,1,c) for c in 1..5] if units > 0, else []
  position 12: [B(resource_paper,r) for r in 0..24]
               for equal/validation roles, else []
  position 13: [B(resource_paper,r) for r in 0..24]
               for research roles, else []
  every other position: []
  ```

  The resulting 15-position count vectors are exactly
  `[1260,0,25,0,0,0,0,0,0,0,5,5,25,0,0]` for equal/rehearsal,
  `[1260,0,25,0,0,0,0,0,0,0,0,5,25,0,0]` for validation, and
  `[1260,0,25,0,0,0,0,0,0,0,5,0,0,25,0]` for research. Call order,
  successful inventories, and every replay copy use those sequences without
  sorting or deduplication.
- **Shared paper-weight lifecycle:** The first positive kernel-13 position in
  a trace draws the 25 paper bootstrap vectors and publishes one immutable
  `resource-resume-paper-bootstrap-weights-v1` `(25,252)` artifact. The last
  positive kernel-13 position is its sole last consumer and deletes it through
  that position's cleanup intent. Thus producer/last-consumer positions are
  `12/13` for equal/rehearsal, `12/12` for validation, and `13/13` for
  research. Both positive equal-context variants load the same bytes. A
  zero-unit kernel-13 variant draws nothing. This adds no scientific payload
  and uses the existing private resource-wrapper registry. A successful
  rehearsal now retains 13 artifact-kind counts and 51 artifact rows.
- **Receipt-stage normalization:** An ordinary atomic receipt stage is not
  debris. Before deriving a transition, the recovery supervisor admits only:
  absent stage/final; one valid canonical receipt file from which the exact
  marker is derived; one valid complete staged receipt/marker pair; or one
  valid visible final pair. A valid receipt-only stage is completed, and a
  valid complete stage is renamed and parent-fsynced without changing its
  bytes. A successor may perform that idempotent adoption only after proving
  the encoded publisher dead; the next durable receipt binds that death.
  Marker-only, partial/corrupt, extra-entry, mismatched, or conflicting
  states are forensically incomplete. An absent work-boundary stage means the
  current record was not committed and is replayed; an absent trace or
  measurement receipt is reconstructed only from its complete durable prefix
  and followed by its uniquely derived boundary. The measurement literal is
  exactly `"resource-measurement-block-v1"`. Every adoptable claim/receipt
  encodes and revalidates its unique publisher PID/start identity. The
  temporary kernel-14 probe and hidden terminal outcomes are not
  successor-adoptable checkpoints. Neither are worker-birth stages, the
  registered `terminal_entry=true` final block-3 boundary, the final
  rehearsal boundary, or a cleanup-complete final failure-resume stage after
  publisher death. Their same live publisher may finish exact staged bytes;
  a dead publisher authorizes no adoption, next receipt, terminal Git check,
  outcome creation, or opposite outcome.
- **Entry-level ordinary cleanup and debris:** A cleanup intent first freezes
  logical targets and then a complete child-before-parent filesystem-entry
  sequence. Regular-file rows bind exact mode, logical/allocated bytes, and
  content SHA256; directory rows bind exact type/mode and use null byte/hash
  fields so deleting a child cannot invalidate a surviving parent row. A
  filesystem is legal only when an exact row prefix is absent and the suffix
  validates, with no extra path. Debris uses the same entry rows plus a
  monotone completed-prefix count and remaining-suffix digest. Chained
  interruptions copy the immutable target/row bytes but advance those two
  progress fields from the actual filesystem; they do not falsely copy stale
  progress byte-for-byte. Artifact finals bind the exact artifact SHA256;
  receipt finals bind the receipt-final domain digest. Kernel 14's close probe
  uses the ordinary atomic receipt-directory publisher, eliminating an
  unrepresentable partial root-file probe state. Every entry is assigned to
  the unique deepest matching target; terminal root targets own all remaining
  ancestors/ordinary entries; target slices are positive, contiguous, and
  exhaustive; and tree/root evidence hashes the exact target slice. Before
  every checkpoint/scratch mutation, the exact prospective terminal plan must
  remain within the row/path/byte caps.
- **Terminal-failure checkpointing:** Failure selection remains immutable
  before deletion. Cleanup inventories use the same entry-level row grammar.
  Between one and 641 contiguous failure-resume receipts are mandatory,
  including an exact final receipt published only after every cleanup row is
  absent and every required parent fsync is complete. Resume zero has predecessor kind
  `"failure-intent"` and its digest; later resumes have predecessor kind
  `"failure-resume"` and the immediately prior resume digest. Each resume
  stores prior durable wall/perf/cumulative anchors, current resume and cutoff
  wall/perf samples, a same-boot monotonic or cross-boot wall charged gap,
  current active work, and the exact cumulative sum. After predecessor
  publication/adoption, each segment takes its resume samples before its first
  deletion or parent fsync and its cutoff samples after every prefix advance
  and fsync charged to that segment. Resume zero therefore encodes completed
  prefix zero and is cleanup-complete iff the intent has zero entries. Active
  cleanup work is at most 480 seconds; each failure-intent/resume row receives
  a fixed 60-second publication accounting charge; and the accounted sum is at
  most 540 seconds. The charge is not an observed or enforced receipt-close
  latency bound. After the final full-prefix receipt,
  deterministic
  `failure.json` plus `_FAILURE` close receives the same fixed terminal
  accounting charge and cannot reopen work. The terminal
  outcome is one atomic directory
  `terminal/failure/{failure.json,_FAILURE}`: both children are written and
  fsynced in the unique hidden stage. `_FAILURE` binds the exact JSON and
  carries the same post-JSON Git/process/publication-RSS certificate as
  `_SUCCESS`; after marker/stage fsync the same final in-process seal gates the
  no-overwrite directory rename and terminal-parent fsync. No visible
  JSON-without-marker state exists. Resume zero is the
  pre-deletion anchor; every later nonfinal receipt strictly advances the
  cleanup prefix or binds a newly dead publisher. A nonfinal staged resume may
  be adopted and bound by the next receipt only when a later slot/death row is
  available, but a last-slot or dead-publisher
  cleanup-complete stage is forensically incomplete rather than duplicated.
  The final-resume publisher is encoded in `failure.json` and must remain
  continuously alive through outcome-directory rename and therefore
  visibility. Its earlier death permits no successor creation or rename; an
  exact visible final may only be revalidated and followed by an idempotent
  terminal-parent fsync.
- **Durable worker birth and watchdog provenance:** Before every worker spawn,
  the supervisor publishes a launch intent containing the capability-nonce
  commitment, parent identity, and an arithmetically derived watchdog arm:
  480 seconds of work followed by a distinct 60-second reap grace. The
  bootstrap-only child inherits parent-liveness and capability descriptors,
  exits on pre-capability parent loss, and publishes its PID/start/boot birth
  record as its first durable action. Only a complete validated launch/birth
  pair may be referenced by the worker claim, reservation, worker-ready
  boundary, and capability release. A complete birth must later join an exact
  wait/death proof even if no claim followed. Every boundary, cleanup intent,
  or interruption that can precede worker work persists the next arm before
  that work; wait/death rows bind its exact receipt digest, work deadline, and
  reap deadline. No deadline may first appear in a wait row, be recomputed
  from a later clock, or be extended because earlier setup consumed time.
- **Process identities and death proofs:** Both registered and rehearsal
  attempts bind the initial supervisor PID, kernel start identity, and boot
  digest. Every claimed-worker `wait4` appends one hash-bound cumulative row carrying
  worker claim/identity, raw status, byte-normalized `ru_maxrss`, post-wait
  sample, and deadline. Process-death rows additionally bind the old boot
  digest and use only three exact methods: `wait4-reaped`, with that same
  status/`ru_maxrss`/sample/deadline evidence;
  `double-process-identity-absence`, with two same-boot zeroed-buffer
  `proc_pidinfo(PROC_PIDTBSDINFO)` checks 50 ms to 1 second apart and null
  wait/rusage/deadline fields; or `boot-identity-changed`, with all
  perf/wait/rusage/deadline fields null and unequal boot digests. Double
  absence passes only two zero/`ESRCH` observations or two complete reads
  naming the same stable replacement PID/start identity. Target presence,
  mixed absence classes, changing replacement identity, permission failure,
  ambiguous zero/zero, short/oversize return, malformed struct, PID mismatch,
  ABI failure, or boot change between observations fails. The shared
  verdict/replacement identity is factorized once with two raw
  `[perf_counter_ns,return_bytes,errno]` samples, preserving exact evidence
  while keeping the maximum process-death row within 512 canonical bytes.
  Per-method nullability and ordering are byte-authoritative. Interruption,
  failure-intent, and failure-resume chains prove every superseded identity
  exactly once, with at most 128 distinct death rows across the whole attempt.
  Kernel 14's receipt probe is not a child role. Git subprocesses are legal only
  in three twelve-child sets: bootstrap before the first worker;
  terminal-pre-JSON after every issued worker identity is closed, no worker is
  alive, and every currently waitable direct child has been reaped; and
  post-JSON inside the terminal marker certificate. The first two sets' 24
  complete rows remain
  reconstructible from `attempt.json` plus terminal JSON; the third set remains
  in the marker. Intermediate seals launch no subprocess, no Git child overlaps
  a worker, and Git children are wait-only: missing Git wait/rusage evidence is
  forensically incomplete, not replaceable by a worker death proof.
- **Reservation ancestry:** A reservation permanently retains its original
  worker-claim digest. An initial capability requires direct equality among
  payload, worker claim, reservation, and worker-ready boundary. A resumed
  capability requires payload/current-claim/worker-ready equality and walks
  the finite, gap-free, repetition-free predecessor chain backward from the
  current claim to the unique immutable creator digest. Every link in that
  suffix has one authorizing contiguous interruption; older claims may occur
  only beyond the creator, and an interruption retaining the same worker
  creates no claim link. It never rewrites the reservation or equates an old
  claimant with the current child.
- **Thermal reset after interruption:** Every admitted interruption, whether
  inside a trace or exactly at a trace/measurement boundary, resets thermal
  qualification. A suspended trace first completes but contributes nothing to
  the new recovery epoch. Before the next warm measurement trace, consume new
  contiguous panels in a reset
  `validation,research,research,validation` cycle until complete successful
  recovery-thermal traces total at least 600 seconds. These traces do not
  count toward measurement pairs or their 200-second minima. A second
  interruption discards only recovery-thermal qualification since the prior
  interruption; completed scientific/timing receipt prefixes remain. No
  thermal work is required when no later warm trace exists.
- **Replay-monotone timing roles and falsifier:** For record `i`, freeze
  `Rplus_i=duration_plus_ns_i=D_i+2*h_i` and
  `Aplus_i=admission_duration_plus_ns_i=Rplus_i+480000000000*r_i`.
  Aggregates sum those exact record fields:
  `Rplus[j,p,k]=sum_i Rplus_i`, `Aplus[j,p,k]=sum_i Aplus_i`,
  `Rplus[j,p]=sum_k Rplus[j,p,k]`, and
  `Aplus[j,p]=sum_k Aplus[j,p,k]`. `Rplus` is used only for
  predictor/reference operands. `Aplus` is used only for held/current
  operands and for every cold, conservative/projected task, block, phase,
  combined, and final absolute projection or budget. Raw `D` remains
  diagnostic timing and the successful-work stop clock.
  For measurement block `j`, `N_j` is its complete balanced-pair count. For
  `s in {overall,validation,research}`, `Rplus[j,s]` and `Aplus[j,s]` sum the
  corresponding record fields over the named phase traces, excluding the
  `EQUAL` trace; `overall` combines validation and research. Stationarity is
  exactly
  `20*N_j*Rplus[j-1,s] >= 19*N_(j-1)*Aplus[j,s]`. For held-out warm block
  `j`, phase `p`, kernel `k`, and the other blocks `a,b`, temporal reference is
  `H[j,p,k]=max(ceil_div(U[j,p,k]*Rplus[a,p,k],U[a,p,k]),`
  `ceil_div(U[j,p,k]*Rplus[b,p,k],U[b,p,k]))`; set
  `H[j,p]=sum_{k:U[j,p,k]>0} H[j,p,k]` and require
  `Aplus[j,p] <= ceil_div(5*H[j,p],4)`. For other phase `q` and
  `C={1,2,3,4,5,6,7,8,9,10,14}`, cross-context reference is
  `X[j,p,k]=max(ceil_div(U[j,p,k]*Rplus[a,q,k],U[a,q,k]),`
  `ceil_div(U[j,p,k]*Rplus[b,q,k],U[b,q,k]))`; require both
  `Aplus[j,p,k] <= ceil_div(5*X[j,p,k],4)` for every `k in C` and
  `sum_C Aplus[j,p,k] <= ceil_div(5*sum_C X[j,p,k],4)`.
  The pre-code falsifier fixes raw `D`, units `U`, and resolution `h`, then
  increments each record's replay count separately. Every reference-side
  `Rplus`, `H`, and `X` must remain unchanged; every affected held/current
  `Aplus` and dependent absolute projection must weakly increase; the raw
  successful-work stop clocks must remain unchanged; and no stationarity,
  temporal, cross-context, task, phase, total, or overall acceptance Boolean
  may change from false to true. Two mandatory fixtures reject the superseded
  symmetric-`Aplus` rules: equal-count stationarity with raw block totals
  `600 s,640 s`, where replaying the prior block must not turn
  `20*600 < 19*640` into a pass; and unit-one temporal blocks with raw totals
  `[1000 s,1000 s,1300 s]` and replay counts `[1,0,0]`, where the third block
  must still fail the `1.25*1000 s` upper. This correction changes only which
  already-bound duration enters each comparator; no threshold, seed, unit,
  work vector, window, budget, or scientific inference changes.
- **Closed-segment telemetry continuity:** Observed samples remain labeled
  observed, and only a durably closed process segment can preserve pass
  authority. A live supervisor closes a worker-loss segment only after
  continuous sampling, cumulative hash-bound `wait4`/rusage rows, and a final
  disk scan; a
  cross-boot successor may carry that segment only through its already
  durable clean-exit interruption receipt. Abrupt supervisor loss or direct
  boot loss has predecessor-close method `"unknown-loss"` and assigns
  admission uppers strictly above their limits: RSS `3,500,000,001` bytes,
  checkpoint tree `2,000,000,001` bytes, created roots `6,000,000,001` bytes,
  and absolute workspace `30,000,000,001` bytes. It therefore selects
  terminal failure `"select-terminal-failure-telemetry-gap"` before a new
  worker, capability, RNG call, or thermal trace. Complete segments use the
  maximum of their prior durable upper and current observed margin, never
  relabel a bound as a sample, and never apply the 25% margin twice. The
  cumulative rusage envelope adds the supervisor high water to the larger of
  the maximum cumulative worker-wait `ru_maxrss` and the maximum Git-child
  `ru_maxrss` across every complete preterminal check available at that cutoff.
  The bootstrap maximum is present at every durable cutoff; the terminal
  pre-JSON maximum joins it only at the terminal cutoff. The post-JSON set
  remains in the separate publication envelope. The
  separate 1.6-GB pre-mutation checkpoint ceiling remains the largest
  admitted observed tree compatible with the 2-GB post-margin cap.
- **Finite evidence liveness:** Registered execution admits at most 64 worker
  launch intents, 64 worker births, 64 worker claims, 63 interruptions, 4,096
  traces, and 641 failure resumes. A terminal
  cleanup inventory has at most 512 rows; the attempt-wide process-death union
  has at most 128 rows; the cumulative worker-wait inventory has at most 64
  rows; and every canonical path has at most 240 ASCII bytes. Each cleanup row
  must encode in at most 1,024 canonical bytes and each death or worker-wait
  row in at most 512. The 131,072-byte non-row term is the exact failure-intent
  encoding with all three row arrays replaced by empty arrays, including all
  delimiters/enclosures.
  Therefore
  the intent envelope is below
  `512*1024 + 128*512 + 64*512 + 131072 = 753,664` bytes, strictly below the
  1,048,576-byte root-receipt cap. Before failure selection, a count/path/
  encoding bound selects terminal failure before the one-past object is
  created. After selection, resume/death/encoding-cap exhaustion stops the
  consumed failure as forensically incomplete before mutation; it cannot
  become an unmarked cleanup dead end.
  The intent equation is not accepted as proof for other files. A frozen
  fixture-schema digest separately constructs maximum canonical failure
  intent, index-zero/progress/death/cleanup-complete failure resumes,
  rehearsal and registered success/failure JSON, and `_SUCCESS`/`_FAILURE`.
  Each applicable fixture uses all 64 waits, 128 deaths, 512 cleanup rows, 641
  resumes, 240-byte paths, maximum scalar/string widths, all source/control
  rows, 24 preterminal Git rows, 12 post-JSON Git rows, and 1,201
  publication-RSS samples. Every exact file including terminal LF must remain
  at or below 1,048,576 bytes and every one-past mutation fails before file or
  stage creation.
- **Terminal-outcome accounting row:** The complete rehearsal and registered
  schedules add one root terminal accounting row, not a new work boundary.
  Success and any fully closed marked failure use the same certificate and
  final-seal protocol. From the
  final durable boundary through waits, scans, aggregation, the exact
  terminal-pre-JSON full Git check, child reaping/rusage, and the pre-JSON
  cutoff, active work is at most 480 seconds. `attempt.json` already contains
  the exact bootstrap check. Terminal JSON contains its digest, the exact
  second check, their two-check inventory/hash, and cumulative RSS whose
  preterminal Git high-water reconstructs from the 24 child rows jointly bound
  by `attempt.json` plus terminal JSON.
  Before non-resumable terminal entry, the final registered-success boundary
  persists passing size uppers for `result.json/_SUCCESS`; the final rehearsal
  boundary does the same for its success schema; and the cleanup-complete
  failure resume persists passing uppers for `failure.json/_FAILURE`. Every
  preflight binds the frozen fixture-schema digest and 1,048,576-byte cap. A
  missing/failing success preflight selects ordinary failure before terminal
  entry. After failure selection, a missing/failing final preflight stops
  before final-resume publication or any terminal-stage mutation and remains
  forensically incomplete.
  The selected atomic directory is
  `terminal/success/{result.json,_SUCCESS}` or
  `terminal/failure/{failure.json,_FAILURE}`: the hidden stage is created and
  the terminal parent fsynced, and the exact JSON written/fsynced. A final
  twelve-child Git check then runs under the live sampler. `_SUCCESS` binds the
  result and `_FAILURE` binds the failure; both carry the same post-JSON
  certificate: complete Git child output/wait/rusage, source and Git-control
  rows, runtime/module/boot/publisher identities, publication-local sampler
  state, and the recomputed 25%-margin RSS upper. After marker/stage fsync, a
  no-subprocess final seal recomputes those identities, proves no descendants,
  stops/joins the sampler, requires the publisher to be the only live thread,
  and takes the final self-resident/RUSAGE_SELF sample. Every final gap is at
  most one second, the observed envelope is at most 2.8 GB, and its 25%-margin
  admission upper is at most 3.5 GB; only then does it license the no-overwrite
  rename plus terminal-parent fsync. The measured pre-JSON work is at most 480
  seconds; the later complete publication sequence receives a fixed 60-second
  accounting charge, giving an accounted sum at most 540 seconds. The charge is
  not an observed or enforced end-to-end latency upper. No visible
  JSON-without-marker branch exists. Forward cutover occurs only after exclusive
  hidden-stage creation and successful terminal-parent fsync. A stage absent
  after a crash in the intervening window is pre-cutover; an exact surviving
  stage conservatively locks its kind. The same live publisher may finish it
  and an exact visible final is reusable after a current-live terminal-parent
  fsync, but a dead-publisher hidden outcome is forensically incomplete and
  never permits the opposite outcome. Terminal JSON and marker certificate
  both bind the publisher; success matches the
  final-boundary publisher and failure matches the final-resume publisher.
  Publication of that final boundary or final resume is non-resumable terminal
  entry: its publisher must remain continuously alive through visibility.
  Publisher death or a failed/incomplete terminal-pre-JSON check is
  forensically incomplete, cannot select the opposite outcome, and never
  authorizes a retry or third preterminal check.
  Publication RSS is a 50-ms sampled empirical envelope plus child `wait4`
  high-water evidence and 25% policy headroom, not a continuous mathematical
  bound; a sub-sample parent-process spike remains an explicit limitation.
  The 60 seconds are a conservative accounting charge, not a false
  observation of the marker/rename/parent-fsync suffix; visible-directory
  existence attests the final seal, and an external post-seal source race
  remains outside the trusted local-process boundary.
  Kernel 14 remains a benchmark probe but
  supplies no terminal-close bound. Rehearsal `TC` and `TS` remain immutable
  evidence roots on success; there is no post-result cleanup suffix. The
  rehearsal therefore has 45 canonical boundaries, 12 cleanup intents, 57
  capped ordinary checkpoint intervals, one terminal accounting row, and 58
  resource-accounting rows in total.
- **Failure-prefix and byte-order closure:** Marked failure admits only
  category-contiguous receipt prefixes with at most one active incomplete
  trace and with every cross-category count derived by the canonical
  scheduler. Generic parent arrays are UTF-8 role-sorted; the null-batch order
  is `base-panel`, `cell-panel`, `resume-homogeneous-focals`,
  `resume-observable-focals`, `resume-oracle-focals`. Cleanup object-kind
  literals, target order, and entry order are frozen in the artifact
  authority. The exhaustive receipt-kind list includes terminal failure
  intent and resume.
- **Configuration and review gate:** The amended
  `configs/g2_resource.toml` freezes these counts, call-count vectors, caps,
  paper-weight shape/lifecycle, terminal accounting row, thermal reset,
  immutable reservation-creator ancestry, closed-segment telemetry continuity,
  the one-sided `Rplus`/`Aplus` comparator roles, and the deterministic
  replay-monotonicity falsifier. The artifact authority additionally freezes
  launch/birth receipt schemas, watchdog-arm arithmetic, Darwin absence
  factorization, terminal-entry nonadoption, and the terminal-size fixture
  digest; these use existing numeric caps and therefore do not alter the
  sealed TOML bytes.
  Implementation remains forbidden until the exact config byte/hash/type
  seal is recomputed, all cross-document stale values are removed or
  explicitly historical, and fresh independent methods, systems, and schema
  reviews pass. The locked local suite and hosted CI follow those reviews
  before test-seed implementation.
- **Inference effect:** None. A025 removes implementation discretion and
  strengthens interruption-selection falsification in an engineering
  benchmark. It changes no statistical estimator, target, interval,
  threshold, scientific trial, or registered validation/research address.
- **Access statement:** A025 was derived from source and document inspection
  plus deterministic byte/count calculations only. No A022 rehearsal,
  registered resource seed `2026071529`, validation seed `2026071521`,
  research seed `2026071522`, empirical data, evaluation data, or holdout was
  accessed.

### A026 — Close interruption selection and consumed terminal crash states

- **Date:** 2026-08-06, before resource-run implementation, any A022
  rehearsal, or any registered G2 access. Amendment A026 is independent of
  assumption A026 in `ASSUMPTIONS.md`.
- **Reason:** Fresh review of amendment A025 passed the byte/schema audit but
  failed methods and systems review. First, a worker interruption inside a
  rate-bearing trace could cool the machine and still let the resumed suffix
  enter the admitted timing sample before rethermalization. Second, same-boot
  supervisor death after a visible launch intent but before a visible worker
  birth consumed the attempt while authorizing neither work nor marked
  failure. Third, death after the non-resumable terminal-entry receipt could
  consume the selected outcome without any terminal directory. These are
  deterministic specification failures; no timing result, random draw, or
  data value was observed.
- **Narrow supersession:** Preserve amendments A022--A025's seeds, address
  domains, RNG sequences, record order, numerical kernels, work matrix,
  estimators, thresholds, budgets, artifact shapes, successful-rehearsal
  counts, and conditional per-kernel interpretation. Supersede only their
  conflicting interruption-admission, launch-only recovery, and
  terminal-entry dead-publisher clauses. In every conflict, amendment A026
  controls.
- **Rate-bearing interruption rule:** A rate-bearing trace is any cold,
  equal-context, validation-context, or research-context trace whose elapsed
  kernel durations could enter `N`, `U`, `Rplus`, `Aplus`, `H`, `X`, a warm
  minimum, a stationarity statistic, a temporal comparison, a cross-context
  comparison, or a phase projection. From the trace's worker-ready boundary
  through its trace boundary, any interruption selects ordinary terminal
  failure. The unfinished trace contributes no rate or comparison operand,
  cannot be completed or replaced, and no later measurement trace is legal.
  Its durable prefix remains available only for failure evidence and bounded
  cleanup. Every record admitted from a successful rate-bearing trace therefore
  has `replay_count=0` and byte-equal `Rplus=Aplus`; any nonzero replay count in
  an admission-bearing record is terminal failure. The replay-monotonicity
  fixtures remain mandatory negative tests but cannot license replayed rate
  evidence. An interruption strictly between two completed rate-bearing traces
  preserves the earlier completed evidence but requires a fresh uninterrupted
  600-second recovery-thermal cycle before the next warm trace. An
  interruption inside that recovery cycle discards the partial cycle and
  restarts the full cycle after recovery; recovery-cycle time never enters a
  rate operand. Thus no post-interruption suffix can improve an admitted rate,
  and no failure-selected trace can be replaced by a more favorable trace.
- **Launch-quiescence lease:** Every worker launch intent is one atomic
  receipt directory that contains its exact JSON/marker pair and one regular
  file named `quiescence.lock`, mode decimal `384`. Before the directory
  becomes visible, the supervisor opens that file once, verifies its stable
  inode/type/mode/link identity, acquires a nonblocking whole-file exclusive
  Darwin `flock`, and keeps the sole intended open-file object live. Spawn is
  forbidden before the complete intent directory is visible. The bootstrap
  child inherits exactly one duplicate reference to that same open-file
  object; neither process may call `LOCK_UN`, reopen the file, duplicate or
  pass the descriptor, leak it to another process, unlink or replace the
  path, or spawn a descendant while launch-only. The descriptor is not
  close-on-exec and remains held through visible birth and claim; afterward
  the ordinary exact PID/start/boot process authority controls. A hidden
  launch-intent stage is normalized under the ordinary receipt rule while its
  original publisher is live, or after publisher death only by a successor
  that validates the same lease inode and acquires the lock as below.
- **Launch-only recovery:** A same-boot launch intent without complete visible
  birth is recovery-pending, not forensically terminal. A successor first
  proves the encoded supervisor dead with the existing factorized
  PID/start/boot evidence. It then independently opens the visible or valid
  staged `quiescence.lock` with no-follow semantics, revalidates the bound
  inode/type/mode/link identity, and attempts `LOCK_EX|LOCK_NB`. `EWOULDBLOCK`
  authorizes no mutation and leaves the state recovery-pending. Successful
  acquisition proves that no incompatible lock remains on the inherited
  Darwin open-file object; under the frozen no-unlock/no-dup/no-pass/no-
  descendant bootstrap discipline, no launch-only child can retain authority.
  The successor then selects the ordinary pre-RNG terminal-failure lane,
  without releasing a capability or constructing `SeedSequence`. A changed
  boot retains the existing pre-capability failure rule because neither
  process nor inherited descriptor survives. This lease is a quiescence proof
  combined with the named supervisor-death proof; it is not represented as a
  PID-only child-death proof.
- **Forensic terminal nonpass:** The terminal root has a third mutually
  exclusive close kind,
  `terminal/nonpass/{nonpass.json,_NONPASS}`, staged at
  `terminal/.nonpass.xid-g2-terminal-stage-v1`. It is legal only after an
  immutable `terminal_entry=true` success boundary or cleanup-complete final
  failure resume has selected success or failure and the encoded terminal
  publisher is proved dead, or after that same publisher encounters a
  post-entry Git, process, sampler, seal, or publication failure. Before any
  nonpass-stage mutation, one ordinary successor-adoptable
  `resource-terminal-nonpass-intent-v1` receipt freezes the selected kind,
  selected-entry digest, original publisher-death/failure evidence, expected
  canonical `nonpass.json` and `_NONPASS` bytes, and their digests. The close
  contains no new Git check, random draw, timing measurement, source-admission
  claim, or opposite outcome. It is a definitive consumed-attempt nonpass:
  it can never satisfy resource admission, cannot license retry under the same
  seed, and cannot coexist with visible success or failure.
- **Restartable nonpass publication:** `nonpass.json` and `_NONPASS` are pure
  functions of the visible nonpass intent and contain no successor-local time
  or identity. After proving the encoded stage publisher dead, a successor
  may remove only an exact incomplete suffix of the hidden nonpass stage,
  rebuild the same bytes, fsync the children and stage, no-overwrite rename it,
  and fsync `terminal/`. An uncertain rename is resolved by validating the
  exact visible pair and fsyncing the parent. A valid complete hidden stage is
  adoptable; invalid bytes select no other outcome and fail closed. The same
  fixed 60-second terminal accounting charge applies, but it is not an
  observed close-latency bound. This continuation is safe because it certifies
  only non-admission of an already consumed attempt.
- **Configuration and review gate:** The amended
  `configs/g2_resource.toml` is exactly 9,799 ASCII bytes with SHA256
  `3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
  194 parsed leaf-type rows, and type-tree SHA256
  `e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.
  It has no BOM or carriage return and ends in exactly one LF. The added
  maximum nonpass-intent size is 131,072 bytes. Successful-rehearsal counts
  remain seven resume-state rows per trace, 13 retained artifact kinds, 51
  retained artifact rows, 45 canonical boundaries, 12 cleanup intents, 57
  ordinary checkpoint intervals, one terminal accounting row, and 58 total
  resource-accounting rows. Implementation remains forbidden until fresh
  independent methods, systems, and schema reviews all pass this settled
  A022--A026 package, followed by the locked local suite and hosted CI.
- **Inference effect:** None. Amendment A026 removes timing-selection and
  crash-state discretion from an engineering admission benchmark. It changes
  no statistical estimator, population target, interval, scientific
  threshold, trial count, or registered validation/research address.
- **Access statement:** Amendment A026 was derived from source/document
  inspection, deterministic byte/type calculations, and primary Darwin
  process-lock documentation only. No A022 rehearsal, registered resource
  seed `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.

## A027 — Exact paper-cache field order before serialization

- **Registered:** 2026-08-06, after A026 document acceptance and before any
  paper-cache index, codec, serializer, resource fixture, rehearsal, or
  registered execution path existed.
- **Reason:** A026 fixed the nine cached matrices, six-by-thirty SSE/SST pairs,
  shapes, NPY envelope, and bootstrap operation over column `c`, but did not
  define the bijection from semantic fields to `c`. Inferring that bijection
  from tuple names or from one-dimensional C-order would allow an undetected
  transpose or permutation.
- **Research vector:** matrix order is
  `(PI_1_direct, PI_I_direct, CI_1_direct, CI_I_direct, PI_CC_purged,
  CI_CC_purged, PI_CC_full_response, CI_CC_full_response,
  cc_mean_projection_p_perp)`. With row `i` and column `j` in ascending sealed
  asset order, `c = 900*m + 30*i + j`. Rows are response/output assets;
  columns are flow/input assets. The first eight payloads are original-unit
  slope operators without intercepts or separate factor coefficients; the
  ninth is the asset-space `P_perp` operator.
- **Loss vector:** spec order is
  `(PI_1, PI_I, CI_1, CI_I, PI_CC, CI_CC)`, response index is ascending, and
  kind order is `(sse, sst)`. Its research index is
  `c = 8100 + 60*s + 2*i + ell`. Therefore
  `9*30*30 + 6*30*2 = 8460` exactly.
- **Recovery vector:** recovery is a compact `CI_I` vector, not a research
  prefix. Coefficients use `c = 30*i + j`; losses use
  `c = 900 + 2*i + ell`, giving `30*30 + 30*2 = 960`. The corresponding full
  research positions are `2700:3600` and `8280:8340`.
- **Inverse map:** quotient/remainder by 900 and 30 recovers research matrix,
  row, and column below 8100; quotient/remainder by 60 and 2 recovers loss
  spec, response, and kind above 8100. Recovery uses the analogous 900/30 and
  2 decompositions. Out-of-range indices are invalid.
- **Machine authority:** the parsed
  `artifacts.paper_cache_order` table has LF-terminated canonical-manifest
  SHA256
  `8810471ce6c0747af7cdda48299989303cd85a9c7def7c681f2a57f93348a083`.
  The active config is 10,863 ASCII bytes with SHA256
  `1a14fd68012819d5f901a97ddd9e9a58dd35886bdcc5d47728467f6417fc3cd3`,
  209 leaf-type rows, and type-tree SHA256
  `81eed87be58bf04a897fdcf3dd39cf142944647824a9f97938d46f341803a2ff`.
- **Implementation license:** only after fresh independent methods and schema
  review may a deterministic in-memory field/index and pack/unpack slice be
  written test-first. It must reject transpose, permutation, SSE/SST reversal,
  recovery/research confusion, nonfinite values, wrong dtype/shape/type, and
  source aliasing. An NPY writer, resource fixture, bootstrap artifact,
  resource capability, rehearsal, and every registered RNG path remain
  prohibited.
- **Inference effect:** none. A027 changes no scientific config byte,
  estimator, target, interval, bootstrap weight, threshold, trial count, or
  registered validation/research address.
- **Access statement:** no A022 rehearsal, registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.


## A028 — Confounding rank bound and partial identification before implementation

- **Registered:** 2026-08-12, after the symbolic derivation in
  `docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md` and before any
  identification module, rank diagnostic, exhibit generator, or manuscript
  revision existed.
- **Reason:** Theorem 1 proves that the population return-on-flow coefficient
  differs from the structural impact matrix but bounds neither the size nor the
  structure of that difference, and says nothing about recoverability. Without
  a bound, the project's motivating claim stays rhetorical: a reader cannot
  distinguish "the estimate may be contaminated" from "the estimate is
  uninformative about the structural entry." A028 registers the missing
  results before they are implemented so that neither the rank bound, the
  identified set, nor the diagnostic can be tuned after seeing output.
- **Research vector:** the confounding gap
  `G = plim OLS - Lambda` satisfies `rank(G) <= K + rank(B)`. With `B = 0` and
  diagonal `Lambda`, the population coefficient matrix lies in the
  diagonal-plus-rank-`K` set. The structural matrix is therefore
  set-identified, not point-identified, from second moments. In the registered
  permutation-invariant one-spike geometry the gap is a single constant added
  to every entry, and the structural off-diagonal has the closed-form
  identified interval `[A_off - T/N, A_off + T/N]` with
  `T^2 = (r_1 - q_1 a_1^2)(q_1 - q_0)/(q_1 q_0)`.
- **Diagnostic vector:** `psi_K(A)` is the relative Frobenius distance from the
  diagonal-plus-rank-`K` set, computed by alternating projection between exact
  diagonal extraction and rank-`K` truncated SVD. Its population value is zero
  under the pure-confounding null. A materially nonzero value is evidence for
  structural cross-impact, which is the reverse polarity of the naive
  off-diagonal-magnitude reading. Because alternating projection returns a
  stationary point, the computed statistic is an upper bound on the true
  distance and the test is conservative toward failing to reject.
- **Predictions:** the six numbered predictions of Section 5 of the derivation
  are frozen verbatim and are restated in
  `docs/predictions/THEORY_EXTENSION.md`. They are deterministic algebraic
  checks at test seed `1729`; no interval method applies and the
  multiple-testing count is zero.
- **Implementation license:** a pure-algebra identification module, a
  deterministic rank diagnostic, a deterministic exhibit generator, and
  manuscript and README revisions may be written test-first. Every new
  statistic must fail closed on wrong dtype, wrong shape, nonfinite entries,
  and out-of-range factor counts.
- **Scope withheld:** no registered resource, validation, or research stream;
  no random-number namespace beyond test seeds `1729`, `9191`, and `314159`;
  no external market data; no new G2 estimator, kernel, threshold, or
  bootstrap weight; no change to any sealed G2 digest; no change to the frozen
  G1 result; and no claim that any exhibit estimates a real market's impact
  matrix.
- **Exhibit scope:** evaluations at published summary statistics already opened
  in `docs/G2_SOURCE_AUDIT.md` are conditional analytic exhibits. Each carries
  the label "conditional analytic exhibit at published summary statistics; not
  an estimate of any market's impact matrix." Published dispersion figures are
  not promoted to confidence intervals.
- **Failure rule:** if any of the six predictions fails, the affected result
  does not enter the manuscript. A failed prediction is diagnosed and logged in
  `SPECIFICATION_LOG.md`; it is not repaired after seeing output and then
  silently accepted. The one-spike convention is not retuned to improve
  agreement with any published summary.
- **Inference effect:** none on G2. A028 changes no scientific config byte,
  estimator, target, interval, bootstrap weight, threshold, trial count, or
  registered validation/research address. G2 remains open and executable-red.
- **Access statement:** no A022 rehearsal, registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.

## A029 — Execution-cost consequences of low-rank confounding before implementation

- **Registered:** 2026-08-12, after the symbolic derivation in
  `docs/derivations/EXECUTION_COST_UNDER_CONFOUNDING.md` and before any
  execution module, robust scheduler, exhibit, figure, or manuscript section
  existed.
- **Reason:** A028 established that the structural impact matrix is
  set-identified. That is a statement about estimation and leaves the
  practically decisive question unanswered: a desk does not consume the matrix,
  it consumes the cost of a trade computed through the matrix. Without the
  present results a reader cannot tell whether the identification failure costs
  anything, and the project would be asserting a problem it had not sized.
- **Research vector:** the cost error `C(x,A) - C(x,Lambda) = x' G x` is the
  quadratic form of a matrix of rank at most `K + rank(B)`, so it vanishes on a
  trade subspace of dimension at least `N - K - rank(B)`. In the
  permutation-invariant one-spike geometry `G = g 1 1'` and the error is
  exactly `g (1'x)^2`, proportional to squared factor exposure, maximal for an
  equal-weight index basket and identically zero for every dollar-neutral
  basket. The identified set induces the sharp cost interval
  `C(x,A) +/- (T/N)(1'x)^2`, which is degenerate for dollar-neutral trades, so
  execution cost can be point-identified where the impact matrix is not.
- **Scheduling vector:** minimising worst-case cost under a linear target
  constraint `c'x = q` gives `x*(pi) = (lambda/2) M(pi)^{-1} c` with
  `M(pi) = A_s + pi 1 1'` at `pi = T/N`, whose factor exposure is weakly
  smaller than the naive schedule's. Robustness is strictly worthless whenever
  the constraint pins the factor exposure, which covers a fixed total-quantity
  constraint, an index-like target, and any target whose unconstrained optimum
  is already neutral. Those degenerate cases are registered as part of the
  claim rather than omitted.
- **Predictions:** the five numbered predictions of Section 5 of the derivation
  are frozen verbatim and restated in `docs/predictions/EXECUTION_COST.md`.
  They are deterministic algebraic checks at test seed `1729`; no interval
  method applies and the multiple-testing count is zero.
- **Implementation license:** a pure-algebra execution-cost module, a
  closed-form robust scheduler validated against a dense grid search,
  deterministic exhibits, figures, and manuscript and README sections may be
  written test-first. Every statistic must fail closed on wrong dtype, wrong
  shape, nonfinite entries, and infeasible constraints.
- **Scope withheld:** no dynamic execution schedule, transient-impact or decay
  kernel, risk-aversion term, or timing-risk model; no registered resource,
  validation, or research stream; no random-number namespace beyond test seeds
  `1729`, `9191`, and `314159`; no external market data; no change to any
  sealed G2 digest; and no claim about trading profitability, transaction-cost
  savings, capacity, or deployment.
- **Failure rule:** if any of the five predictions fails, the affected result
  does not enter the manuscript. A failed prediction is diagnosed and logged in
  `SPECIFICATION_LOG.md`; it is not repaired after seeing output and then
  silently accepted. If the closed-form schedule disagrees with the grid
  search, the derivation is corrected rather than the tolerance relaxed.
- **Inference effect:** none on G2. A029 changes no scientific config byte,
  estimator, target, interval, bootstrap weight, threshold, trial count, or
  registered validation/research address. G2 remains open and executable-red.
- **Access statement:** no A022 rehearsal, registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.

## A030 — Finite-sample null distribution for the low-rank departure statistic

- **Registered:** 2026-08-12, after the derivation in
  `docs/derivations/PSI_NULL_DISTRIBUTION.md` and its exploratory pilot, and
  before any bootstrap implementation, confirmatory run, exhibit, or manuscript
  section existed.
- **Reason:** the strongest unresolved objection in
  `docs/redteam/THEORY_EXTENSION.md` is that `psi_K` had no sampling
  distribution, so "materially nonzero" was never operationalised and the
  statistic was descriptive rather than inferential. Without a null
  distribution the diagnostic cannot be applied to data by anyone, which makes
  the paper's central practical instrument unusable.
- **Pilot disclosure:** the size and power tables of Section 4 of the
  derivation are **exploratory pilot results**, run at test seeds `1729` and
  `9191` before this registration. They are disclosed as pilot evidence and are
  explicitly not confirmatory. The confirmatory run uses a fresh sampling seed
  `314159` against the predictions frozen here.
- **Research vector:** under `H0` the estimate is a noisy observation of a
  point in the diagonal-plus-rank-`K` manifold, whose dimension is
  `N + K(2N - K)`, so `psi_K` is `O_p(T^{-1/2})`. A parametric plug-in
  bootstrap that refits the null projection and redraws the estimation error
  from the ordinary-least-squares sampling law supplies the critical value, at
  `B = 199` and `alpha = 0.05`.
- **Factor-count rule fixed before use:** the eigenvalue-ratio criterion of Ahn
  and Horenstein applied to the off-diagonal part of the estimate, maximised
  over `1 <= k <= 10`. It is not re-selected after observing a rejection.
- **Disclosed negative result:** a degrees-of-freedom variance inflation of
  `sqrt(N^2 / (N^2 - dim D_K))` is registered as **not adopted**. The pilot
  shows it drives realised size to exactly zero at every sample size, removing
  all power, because the plug-in bias is in the centre of the null distribution
  rather than its scale. It is reported rather than omitted.
- **Predictions:** the five numbered predictions of Section 5 of the derivation
  are frozen verbatim and restated in `docs/predictions/PSI_NULL.md`. They
  concern realised Monte Carlo rejection rates, so the named interval method is
  the binomial Monte Carlo standard error at `M = 150`, approximately `0.018`.
- **Scope withheld:** no dependent or block bootstrap, no heteroskedastic or
  serially correlated sampling model, no registered resource, validation, or
  research stream, no market data, no change to any sealed G2 digest, and no
  claim that the test is valid at small samples.
- **Failure rule:** if the confirmatory size at `T = 5000` falls outside two
  and a half Monte Carlo standard errors of nominal, the test is reported as
  size-distorted at every sample size examined and `psi_K` reverts to a
  descriptive statistic in the manuscript. A failing prediction is diagnosed
  and logged, never repaired after the fact and then quietly accepted.
- **Usage bound:** the manuscript must state the minimum sample size at which
  the test is usable rather than implying general validity.
- **Inference effect:** none on G2, which remains open and executable-red.
- **Access statement:** no A022 rehearsal, registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.

## A031 — Semantic paper-matrix assembly before implementation

- **Registered:** 2026-08-12, after the derivation in
  `docs/derivations/GATE_G2_PAPER_ASSEMBLY.md` and before any assembly driver,
  synthetic panel fixture, or date cache existed.
- **Reason:** the paper kernels and the A027 cache codec both exist, and the
  protocol, block schedule, and fold rules are binding, but the composition
  from kernels to the nine matrices was never stated. It is the only undefined
  step between an issued date panel and a `PaperResearchDateCache`, and it is a
  step where an error is invisible: a purged operator written into a
  full-response slot, or coefficients written one response row off, yields a
  cache that is finite, correctly shaped, correctly hashed, and wrong.
- **Composition vector:** assembly iterates outer blocks `0..9` ascending, then
  the sealed specification order
  `(PI_1, PI_I, CI_1, CI_I, PI_CC, CI_CC)`, then responses `0..29` ascending.
  Each block yields an original-unit operator per specification, and the ten
  operators are averaged equally within the date per
  `GATE_G2_PREMISE.md` line 553.
- **Placement vector:** the four direct specifications write their block-mean
  operators to the four direct slots, with exact `0.0` off-diagonals for the
  two own-flow specifications. The cross-sectional specifications write the
  residual-flow operator to the purged slots and
  `C_purged P_perp + b W^T`, formed per block and averaged afterwards, to the
  full-response slots. The ninth matrix is the block-mean `P_perp`, cached as
  the projection rather than the loading because the loading is sign-ambiguous
  and averaging loadings would cancel.
- **Loss vector:** `sse` accumulates squared next-block residuals and `sst`
  accumulates squared deviations from the **outer-training** response mean,
  summed across the ten scored blocks in ascending order, in
  specification-major, response-major `(sse, sst)` order.
- **Predictions:** the eight numbered predictions of Section 6 of the
  derivation are frozen verbatim and restated in
  `docs/predictions/PAPER_ASSEMBLY.md`. They are deterministic checks on a
  synthetic panel at test seed `1729`; no interval method applies and the
  multiple-testing count is zero.
- **Implementation license:** a pure composition driver over already-issued
  panels, a synthetic panel fixture for verification, and its tests may be
  written test-first. The driver must fail the date on a nonfinite value, a
  nonconvergent solve, a weak eigengap, a rank-deficient design, an empty
  scored block, or an exactly zero `sst`. No cell may be dropped, averaged
  over, or filled.
- **Scope withheld:** no NPY serializer, resource fixture, bootstrap batch,
  resource capability, Make target, rehearsal, registered stream, registered
  seed, or market data. No estimator, kernel, threshold, or sealed digest may
  change.
- **Failure rule:** a failing prediction is diagnosed and logged in
  `SPECIFICATION_LOG.md`, not repaired after seeing output and then silently
  accepted. In particular, predictions 6 and 8 exist to show that the placement
  and averaging-order contracts are load-bearing; if a permutation or a
  reordering leaves the packed vector unchanged, the contract is vacuous and
  must be re-derived rather than declared satisfied.
- **Inference effect:** none. G2 remains open and executable-red, and no
  registered resource, validation, or research stream is licensed.
- **Access statement:** no A022 rehearsal, registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.

## A032 — Cross-block rank restrictions before implementation

- **Registered:** 2026-08-16, after the derivation in
  `docs/derivations/CROSS_BLOCK_RANK.md` and before any cross-block module,
  tetrad statistic, or manuscript section existed.
- **Reason:** the `psi_K` statistic solves a nonconvex problem whose value
  depends on its starting point and must estimate a diagonal nuisance it does
  not care about. Choosing row and column index sets that are disjoint removes
  the diagonal from the submatrix entirely, turning the restriction into an
  exact rank bound testable with one singular value decomposition.
- **Research vector:** for disjoint `I` and `J`, `A_{I,J} = G_{I,J}` and hence
  `rank(A_{I,J}) <= K` under diagonal structural impact with `B = 0` and at
  most `K` latent factors. Every `(K+1)`-minor of such a block vanishes; at
  `K = 1` this gives tetrads `A_ij A_kl - A_il A_kj = 0`.
- **Predictions:** the five numbered predictions of Section 5 of the derivation
  are frozen verbatim. They are deterministic algebraic checks at test seed
  `1729`; no interval method applies and the multiple-testing count is zero.
- **Disclosed negative result:** recovering the diagonal by alternating
  projection is registered as **not reliable**. Started from the observed
  matrix it recovers the structural diagonal to `4.2e-16`; started from twenty
  random diagonals at scale `5.0` its solutions spread by `24.66`. Direct
  local-identification testing shows the diagonal is nonetheless identified in
  every configuration tested, so the failure is algorithmic. Any estimator
  built on the completion inherits a defect the identification does not have,
  and this is recorded rather than omitted.
- **Scope withheld:** no sampling distribution for `sigma_{K+1}`, no factor-count
  selection rule, no claim of a global converse, no registered stream, no market
  data, and no change to any sealed digest or to the frozen G1 result.
- **Failure rule:** if prediction 4 fails, so that overlapping index sets
  satisfy the restriction as readily as disjoint ones, the disjointness
  hypothesis is vacuous and the theorem is re-derived rather than declared
  satisfied. A failing prediction is diagnosed and logged, never repaired after
  the fact.
- **Claim discipline:** the restriction may be described as rejecting the
  maintained pure-confounding null under a stated factor budget. It may not be
  described as proving genuine structural cross-impact.
- **Inference effect:** none on G2, which remains open and executable-red.
- **Access statement:** no A022 rehearsal, registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.

## A033 — Minimum confounding dimension before implementation

- **Registered:** 2026-08-16, after the derivation in `docs/derivations/K_MIN.md`
  and before any `K_min` module existed.
- **Reason:** committing to a factor budget before looking at the data inverts
  the natural question. Asking instead how many latent dimensions would be
  needed to rationalise the observed matrix without structural cross-impact is
  better posed, and falsification of pure confounding reduces to comparing that
  number against the factor budget the order flow supports.
- **Research vector:** `K_min(A) = min over diagonal D of rank(A - D)`.
  Proposition 10 gives the certified lower bound
  `K_min >= max over disjoint (I,J) of rank(A_{I,J})`, computable by singular
  value decomposition with no nuisance parameter and no nonconvex solve.
  Falsification needs exactly this direction, so the unreliable completion that
  would bound `K_min` from above is off the critical path.
- **Disclosed limitation, registered in advance:** the exact-rank bound
  **saturates at the block dimension under a perturbation of `1e-6`** and is
  therefore unusable on sample data as stated. The singular spectrum
  nevertheless separates structure from noise at every level tested, with the
  noise singular values scaling linearly in the perturbation, so the quantity is
  estimable in principle with a cut calibrated to the sampling distribution.
  That calibration is not attempted and no `K_min` point estimate is claimed.
- **Predictions:** the five numbered predictions of Section 4 of the derivation
  are frozen verbatim. Deterministic checks at test seed `1729`; no interval
  method applies and the multiple-testing count is zero.
- **Scope withheld:** no inference, no upper bound on `K_min`, no factor-count
  estimator, no comparison against a flow-factor count, no market data, no
  registered stream, and no change to any sealed digest.
- **Failure rule:** if prediction 1 fails, so that the bound misses the true
  rank in population, Proposition 10 is re-derived rather than the tolerance
  loosened. If prediction 3 fails, the saturation claim is withdrawn and the
  exact-rank statistic is re-examined for usability.
- **Access statement:** no A022 rehearsal, registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  empirical data, evaluation data, or holdout was accessed.
