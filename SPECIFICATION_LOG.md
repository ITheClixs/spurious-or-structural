# Specification log

Every statistical or pipeline specification is appended in execution order.
The trial count used for later multiple-testing correction includes failed and
abandoned research specifications. Software-only TDD red/green cycles are not
empirical model trials, but gate-level pipeline variants are recorded.

## Trial counts

- Empirical specifications: **0**
- Simulation estimator specifications: **1 run and passed; 2 G2 designs rejected pre-run; 1 G2 design registered and pending**
- Software-only pipeline specifications: **4 completed; source revisions hosted-green**
- Holdout opens: **0**

## P0001 — G0 deterministic record-and-hash smoke path

- **Registered:** 2026-07-15, before first configured run.
- **Scope:** software-only; generated records; no market model, estimator, or
  inferential claim.
- **Configuration:** `configs/demo.toml`; two labels, 32 bins per label, fixed
  seed 20260715; standard-library streaming JSON Lines; SHA256 and row count;
  staged publication under a file lock with `_SUCCESS` written last.
- **Prediction:** see `docs/predictions/GATE_G0.md`.
- **Outcome:** passed locally. An initial sandboxed invocation stopped before
  project execution because uv could not access its external cache; the same
  locked command in the permitted environment completed. The original
  two-file publisher then failed hostile review because interruption could leave
  a mixed artifact pair. Without changing the configured data or expected
  values, publication was redesigned to stage uniquely, serialize with a file
  lock, invalidate before publish, and write a hash-bearing `_SUCCESS` marker
  last. A fault-injection regression proves interrupted output is invalid and
  the next run recovers.
- **Local evidence:** post-fix clean demos each completed in 0.04 seconds at
  28,180,480 and 28,229,632 bytes maximum RSS. Both produced 64 rows and
  identical hashes: JSONL
  `0c2792e71d5807b447bf9b0140eeecccd4f7b06590a9d825ab12eeaa4f03c964`,
  summary `05efff3914a98781783877cfdf5c8ce6b938bbd2851bd503a4e80fa99465c090`,
  marker `e3157945cdcaa04738f5e0d5f572d246aa4b2dd156e88966b328f3844f9ffc7a`.
- **Hosted evidence:** CI run `29416847411` completed with conclusion `success`
  for exact candidate SHA `3abbad1dc3bfa6114434ce2bb5d2de0140b0dafa`.
- **Multiple-testing count:** excluded from empirical/model trial counts because
  no effect, model, or hypothesis is evaluated.

## S0001 — G1 simultaneous-system probability-limit recovery

- **Registered:** 2026-07-15, after the derivation and before implementation or
  any random draw.
- **Scope:** simulation validation of the two derived population regression
  coefficients; no empirical data and no structural estimator.
- **Configuration:** `configs/g1.toml`; `N=30`, `K=3`, `T=10,000,000`; one
  frozen master seed; 100 independently keyed 100,000-row Gaussian shards;
  float64 count/mean/centered-scatter checkpoints; uncontrolled OLS and OLS
  controlling for `fhat=f+epsilon`.
- **Prediction:** `docs/predictions/GATE_G1.md`; combined analytic target hash
  `80e6026821d67708587eb3abe606c05a7f58c5e4499430e6db72ae6d36faee1d`;
  pass iff the maximum elementwise relative discrepancy across both matrices is
  strictly below `10^-3`.
- **Interval:** classical homoskedastic Student-t coefficient intervals with a
  95% Bonferroni family-wise correction across all 1,800 coefficients.
- **Status:** passed on the sole frozen master draw. The test-first
  implementation passes 25 G1 software tests and the full 38-test locked suite.
  Stochastic software tests use only nonregistered test seeds and do not
  evaluate the gate threshold. Resource seed `2026071599` was consumed once;
  master seed `2026071501` was consumed once, without retry or specification
  change.
- **Implementation contract:** sealed target hashes are checked before RNG;
  PCG64DXSM component streams are keyed by seed/shard/component; immutable
  checkpoints contain mergeable centered moments; production runs require
  clean tracked execution inputs at the Git top level; shard reuse additionally
  requires an exact single-thread numerical-runtime fingerprint and reloads
  resource telemetry so shard/phase stops survive resumption; completed results
  report all coefficient intervals and are published success-last.
- **Pre-draw implementation boundary:** commit
  `fe9e69123469496135cdffe516778a1f58206b3f`, execution-input SHA256
  `8a25de8d3cd268284157df20ef3190d5519b714574e90a17c79729462e086a2b`,
  config SHA256
  `2a71f58d1eec7eb39e68e7333ce5cb385a3fcdc85466ee234d334299c8886efd`.
- **Hosted software check:** run `29422105528` stopped before stochastic work on
  a `2.24931185e-13` Linux-versus-Mac algebra-path rounding difference. The
  cross-platform software assertion was aligned from `2e-13` to the existing
  production preflight bound `5e-13`. S0001 remains registered and unrun.
- **Hosted acceptance:** repair commit
  `1adc73921da9f112f4eed56789b7a92a74b67f47` passed CI run `29422306505`
  with 38 tests and full local-parity checks. Neither registered seed was used;
  S0001 remains registered and unrun.
- **Benchmark boundary:** acceptance-ledger commit
  `3c56fa96f3dbc730503cb2f8bbcc586dbd9c57ad` passed hosted run
  `29422623200`. The preregistered seed `2026071599` then produced exactly one
  100,000-row resource shard: 0.086404708 seconds generation, 0.087642709
  seconds in-process total, and 381,517,824 bytes peak RSS. The derated 100-shard
  projection is 18.2589 seconds; A013 passes. Benchmark mode published no
  coefficient estimates, so S0001 remains unrun.
- **Frozen outcome:** exact pre-draw head
  `cc3b01faa469150e15668644d023618cb28c0ab8` passed hosted CI run
  `29423237074` before the first master checkpoint. The 100 shards contain
  10,000,000 rows under seed `2026071501`. Uncontrolled maximum relative
  discrepancy is `5.639467093140219e-4`; controlled maximum relative
  discrepancy is `5.123714186295689e-4`; the strict gate statistic is therefore
  `5.639467093140219e-4 < 10^-3`. All 1,800 targets are inside 95% family-wise
  classical homoskedastic Student-t Bonferroni intervals, with critical values
  `4.190961010324029` and `4.190961010324613`. S0001 passed.
- **Runtime outcome:** cumulative shard generation was 8.239197838 seconds;
  maximum shard duration was 0.099412500 seconds; maximum checkpoint RSS was
  437,829,632 bytes. All 100 checkpoint payload hashes are unique and bind the
  frozen config, execution source, runtime, seed, row count, and shard index.
- **Publication and replay:** result SHA256 values are summary
  `b590b8ba079c70917e3e768ff1079051f2b8a6c8007336367aa2d299ec3c5d54`,
  estimates `f5129b0fc7695e7db13074dad64ac6123263992ccca920f579d85205bba8f06f`,
  and marker `6d2d75323f0a30705b852be85354ec2143fa9876dab92ead60a495bf81bd52cf`.
  An immediate resume reused the validated checkpoints and left all three bytes
  and hashes unchanged; this is the same registered attempt.
- **Hosted closeout:** evidence commit
  `44965d0370810f756ad1c5cc7938a289cb943906` passed CI run `29426776688`.
  G1 is closed; no additional S0001 draw is permitted.
- **Multiple-testing count:** included as one simulation specification. Crash
  recovery with identical validated shards remains the same attempt; changing
  the seed, sample size, fixture, target, accumulator, or metric creates a new
  attempt.

## S0002 — Rejected three-factor G2 source-box design

- **Registered:** 2026-07-15, after primary-source extraction and before G2
  implementation or RNG access.
- **Scope:** deterministic population design only; eight Fourier-modal cells,
  positive own feedback, a response-equivalent integrated-OFI/factor hybrid,
  and a proposed date bootstrap/LASSO validation.
- **Prediction:** the direct population calculation predicted 105.82%--613.48%
  focal relative error across eight cells. The canonical digest was proposed as
  `a8475753e1cd70781c028680d7d782cbee73cb19b7265b93e8335eaa7f506fbf` but
  no exact payload had yet been committed.
- **Outcome:** rejected before implementation, benchmarking, validation, or a
  research draw. Three hostile audits independently reproduced all eight
  values and verified positive structural variances, then found the power
  alternative mathematically impossible, the confirmatory response map equal
  to uncontrolled OLS, the calibration cross-frequency/incompatible, the
  focal pair dependent on arbitrary eigenvectors, and the compute/CV/bootstrap
  contract underdefined. The failure and repairs are recorded in
  `docs/redteam/GATE_G2_PRERUN.md` and amendment A002.
- **Multiple-testing count:** counted as a rejected simulation design because
  its population outcomes were inspected, even though no random stream was
  consumed. It cannot be revived without a new logged specification.

## S0003 — Label-invariant noisy-control G2 premise test

- **Registered:** 2026-07-15, after S0002's diagnosis and before implementation
  or any registered G2 stream.
- **Scope:** conditional confounding-only simulation at `N=30`, `B=0`, the
  one-minute Capponi--Cont leading observable moments, diagonal sensitivity
  `0.29`, homogeneous off-diagonal sensitivity `0.0029`--`0.0046`, oracle
  flow, a correctly loaded independent 95%-reliable proxy, and a stationary
  within-date AR(1) stress of 0.60.
- **Confirmatory candidates:** full-flow condition-capped ridge and a
  pooled homogeneous three-slope OLS given the true symmetry. Both must pass
  all 17 frozen off-diagonal grid points. All six CCZ protocol reconstructions
  are mandatory fidelity diagnostics; they and measured top-ten OFI are
  secondary and use fair projected estimands.
- **Prediction:** `docs/predictions/GATE_G2.md`; the least favorable population
  condition-ridge relative error is `1.3744450002738078`. The exact canonical
  raw target file SHA256 is
  `c2122bbdbcf50181e028a689c502b5734673ed4a9e89765869f26108975f6122`;
  its independently reproducible 12-decimal semantic SHA256 is
  `b645468cd53357c968c272adff489a43e43e402b522fbfdbf2175e5f71dee00c`.
- **Interval and decision:** 499 whole-date multinomial-weight bootstrap draws;
  bootstrap-SE normal and basic 95% intervals; pass only if
  `abs(error) - 0.5 * abs(truth) > 3 * bootstrap_se` for both candidates at
  every point.
- **Licensing:** before the one research draw, 100 exact-procedure size
  superpanels must put the one-sided 95% Clopper--Pearson upper bound for the
  family union of any candidate/grid boundary passage at or below 5%.
  One hundred power superpanels must put the one-sided 95% Wilson lower bound
  for the intersection of all candidate/grid passages at or above 80% under
  reliability 0.95. Reliability one is a recovery diagnostic. A distinct
  benchmark must license the measured compute projection. Neither registered
  seed may be retried.
- **Status:** rejected before implementation or RNG. After second-audit repairs,
  the fresh math audit passed but inference and professor audits found that the
  observable and published opponents were nonbinding, the boundary-only size
  claim was unjustified, and several RNG/CV/cache/benchmark contracts remained
  ambiguous. A003/S0004 supersedes it.
- **Multiple-testing count:** enters the simulation-design count now that its
  analytic predictions are inspected. It becomes a run only when a registered
  stochastic stream is consumed.

## S0004 — Observable and published-opponent G2 premise test

- **Registered:** 2026-07-15, after the fresh S0003 hostile audit and before
  implementation, benchmarking, validation, or any registered G2 stream.
- **Why S0003 died:** its oracle-flow projections were binding while the
  measured top-ten opponent and every published CCZ fit were nonbinding. More
  information does not imply coefficient-error dominance. The same audit found
  a boundary-only size overclaim, bootstrap-key collisions, an omitted pooled
  intercept contract, ambiguous fold-local LASSO penalties, an insufficient CC
  cache, and a non-reproducible benchmark formula.
- **Scope:** the same conditional `N=30`, `B=0`, one-factor observable law and
  structural interval, now with three binding smooth candidates: observable
  integrated-top-ten-OFI proxy-control ridge, oracle-flow condition ridge, and
  globally centered pooled homogeneous OLS. `CI_I` is a binding published
  protocol veto at the primary observable point and `o=0.0046`.
- **Population prediction:** observable ridge ranges from
  `0.009779867515744457` to `0.010849163255110856`; relative error falls from
  `2.3723681088773994` to `1.3585137511110557`. At reliability one its sealed
  target is `0.9816922278202821 o` because multi-level measurement error
  remains.
- **Seals:** raw target SHA256
  `f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59`;
  12-decimal semantic SHA256
  `f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`;
  raw config SHA256
  `f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc`;
  literal LASSO-ratio binary64 SHA256
  `1da884c55b3f6e7bf79012973bddf092a92efb1ea098cd2717a804645a62c9a0`.
- **Smooth validation:** 100 superpanels, 459-event nine-node
  proxy-noise-amplitude null-grid union with one-sided 95% Clopper--Pearson
  upper bound at most 5%, and 51-event reliability-0.95 power intersection with
  one-sided 95% Wilson lower bound at least 80%. Integer thresholds remain one
  or fewer null-union successes and 87 or more power-intersection successes.
  This is not a continuum-uniform size claim.
- **Published validation:** one full-`N`, full-`T` no-confounding `CI_I`
  recovery panel must recover diagonal `0.29` and focal cross coefficient
  `0.0046` inside Bonferroni intervals, with all 31 point errors strictly below
  50% and no focal material-bias declaration, before the single binding
  research reconstruction. This is not a Monte Carlo size/power claim.
- **Interval and decision:** unchanged strict
  `abs(error)-0.5*abs(truth)>3*bootstrap_se`, 499 whole-date weights, named
  normal/basic intervals. Positive G2 is the intersection of all 51 smooth
  events and the `CI_I` veto.
- **Workload:** 26,405,400 smooth validation fits, 15,195,600 `CI_I` recovery
  LASSO solutions, and 45,586,800 six-spec research LASSO solutions. Fourteen
  separately timed kernels must project inside the one-/12-/three-/16-hour
  expected caps. The two-/24-/six-/32-hour hard limits are runtime stops, not
  preflight slack.
- **Status:** registered, content-audited, hash-sealed, independently admitted
  at the pre-implementation contract boundary, and unrun. The contract,
  test-only RNG namespace, pure DGP, and in-memory smooth estimator core are
  implemented and hostile-reviewed; checkpointing, resource authority,
  validation, and research authority remain absent at this historical entry.
  The estimator-core commit later passed hosted CI run `29492765654`; see the
  C0014 closeout evidence below.
  Documentation commit `a5c7f1c02e941a0d6fdef3d645dfea63884cdfd7`
  passed hosted CI run `29448917107`; test-first implementation with test-only
  seeds is open. Registered resource, validation, and research streams remain
  blocked. S0002 and S0003 remain non-executable.
- **Multiple-testing count:** one new specification. No registered scientific
  stochastic run or attempt exists until a registered stream is consumed;
  test-seed software smokes do not count as scientific attempts.

## C0001 — S0004 contract, test-RNG, and DGP software check

- **Recorded:** 2026-07-15, after test-first implementation and before any G2
  resource, validation, or research stream access.
- **Scope:** software-only checks of the four A005 seals, exact typed contract,
  13-field test entropy namespace, exact NumPy call contract, stream schedules,
  AR-filter-first DGP, all 17 population cells, gamma-zero recovery separation,
  and raw-component issuance. Test seeds are `1729` and `9191` only.
- **Prediction before implementation:** altered seals/schemas/addresses must fail
  before `SeedSequence`; each component makes one configured standard-normal
  call; all 17 cells match the frozen covariance and observable moments; raw
  components filter once and phase-25 recovery cannot reuse phase-21 or phase-30
  arrays.
- **Outcome:** initial red tests failed because the module was absent. Successive
  hostile reviews then reproduced sub-tolerance target forgery, equality/type
  substitutions, entropy subclass and TOCTOU routes, unused bootstrap keys,
  double filtering, cross-date/component mixing, and forgeable provenance
  receipts. Each was repaired without changing the S0004 config or consuming a
  registered stream. The stabilized suite passes 79 targeted tests; independent
  DGP recomputation reports maximum all-cell algebra discrepancy `0.0`.
- **Intervals:** not applicable; this entry makes no statistical estimate or
  research claim. Its named evidence is deterministic equality, known-answer
  hashes, failure-before-RNG probes, and test pass/fail status.
- **Multiple-testing count:** zero. This is a software validation record inside
  already registered S0004, not a new parameter specification or stochastic
  attempt.

## C0002 — Cross-platform level-noise RNG diagnostic

- **Recorded:** 2026-07-15, after hosted run `29453577345` and before any fix or
  registered G2 stream access.
- **Scope:** deterministic test-seed diagnosis of one Linux/macOS known-answer
  mismatch at the raw-BitGenerator versus Gaussian-transform boundary. Seed
  `1729` only; no resource, validation, research, or bootstrap realization.
- **Prediction before hosted run:** the exact 150,000-word PCG64DXSM raw digest
  matches across platforms, while at least one later 1,000-value Gaussian block
  differs. A raw mismatch would falsify the transform-only diagnosis.
- **Outcome:** Stage-one hosted run `29453989738` matched the frozen raw PCG
  digest and 98 of 99 Gaussian 1,000-value blocks. The sole mismatch is block
  60 (indices 60,000--60,999); every later block returns to exact equality, so
  generator-state consumption did not diverge. Stage two will compare the
  exact binary64 values inside that block; prediction recorded in D0055.
- **Final diagnosis:** Hosted run `29454185569` differs at one value only,
  global index 60,328, by one ULP. The value is in NumPy's `log1p` Ziggurat-tail
  branch. C0002 therefore supports A006's runtime-conditional byte contract and
  rejects accepting Linux as an alternative registered realization.
- **Acceptance:** Repair commit `ff3a343e9c4cfbf672d7cae5614081733c4b695e`
  passed hosted CI run `29455143418`; Linux matched its frozen runtime-class
  test KAT and rejected registered preflight before `SeedSequence`. C0002 is
  closed without a registered draw.
- **Intervals:** not applicable; exact byte equality and the first divergent
  block are the named methods.
- **Multiple-testing count:** zero. This diagnoses software portability and
  does not test a scientific parameter or select a stochastic specification.

## C0003 — Smooth sufficient-statistic and estimator software check

- **Registered:** 2026-07-16, before estimator implementation and before any
  new stochastic call.
- **Scope:** software-only validation of upper-packed date moments, one-call
  weighted aggregation, global covariance centering, observable PCA,
  condition-capped ridge, and pooled homogeneous OLS. Analytic fixtures are
  deterministic; any stochastic smoke uses only test seeds `1729` or `9191`.
- **Prediction before implementation:** Moment and explicit-row routes agree;
  known nonsymmetric ridge orientation is preserved; the positive trace floor
  shrinks by exactly `1/(1+1e-6)` in the orthogonal fixture; the condition branch
  lands within its declared cap; PCA centering/sign/L1 rules match analytic
  scores; pooled algebra recovers its known off-diagonal without division; and
  every nonfinite, zero-proxy, weak-eigengap, negative-eigenvalue, rank, and
  condition failure is rejected rather than dropped.
- **Numerical path:** preregistration amendment A007 and
  `docs/derivations/GATE_G2_SMOOTH_ESTIMATORS.md` freeze covariance units,
  packing, aggregation, PCA, and SVD before red tests. No threshold or target is
  selected from a stochastic result.
- **Status:** attempt 1 failed hostile review; superseded by C0004--C0014.
- **Intervals:** not applicable; this is deterministic software validation and
  makes no effect estimate.
- **Multiple-testing count:** zero. It implements the already registered S0004
  estimators and does not add a scientific specification.

### C0003 attempt 1 outcome — failed hostile review

- **Date:** 2026-07-16.
- **Local evidence before review:** 20 focused deterministic/test-seed tests,
  the 138-test repository suite, Ruff, formatting, strict mypy, demo, and
  committed-result drift were green.
- **Mismatch:** The test set did not exercise origin binding. A hostile
  deterministic construction showed that a forged `G2Date` and mismatched
  base/cell moment panels were accepted. The primary observable ridge also had
  no analytic integration fixture capable of detecting selection of the oracle
  flow block.
- **Interpretation:** C0003 failed. Green numerical tests did not establish the
  advertised contract boundary. No effect estimate or registered result was
  produced, so the scientific specification count remains unchanged.

## C0004 — Provenance-bound smooth estimator repair check

- **Registered:** 2026-07-16, after diagnosing C0003 and before implementing
  the repair.
- **Scope:** deterministic rejection of forged transformed dates, mismatched
  base/cell designs, different-base contract responses, mutated transformed
  content, and stale weak receipts; exact propagation of aligned design
  digests; and an analytic `W=2Q` oracle-versus-observable integration fixture.
- **Prediction before implementation:** The old boundary accepts forged and
  mixed provenance. The repaired boundary rejects them before aggregation or a
  solve, preserves legitimate same-base/different-cell construction, releases
  dead receipts, and returns oracle `B/(1+1e-6)` versus observable
  `B/[2(1+1e-6)]` with trace floors `1e-6` and `4e-6`.
- **Status:** passed after the C0003 failure. Forged dates, mixed base/cell
  provenance, changed transformed content, stale receipts, and crossed designs
  are rejected. The deterministic `W=2Q` integration fixture returns the
  preregistered oracle and observable ridge values and trace floors.
- **Intervals:** not applicable; this is deterministic software validation and
  makes no effect estimate.
- **Multiple-testing count:** zero. This repairs the implementation of the
  already frozen S0004 specification.

## C0005 — Complete-panel and fit-authority repair check

- **Registered:** 2026-07-16, after the second C0003 hostile diagnosis and
  before implementation.
- **Scope:** deterministic complete-range validation for contract panels,
  distinction between declared frontiers and truncated panels, exact
  base/cell panel-prefix equality, and separation of analytic moment algebra
  from high-level sealed G2 fits.
- **Prediction before implementation:** Any missing middle/tail date, shortened
  date-252 prefix, mismatched stream/panel/design tuple, analytic-origin
  high-level fit, or wrong N/T/L contract aggregate fails before a coefficient.
  Existing analytic extraction-plus-solver results remain unchanged.
- **Status:** passed. Missing tail and middle dates, mixed panel and stream
  prefixes, mixed design digests, analytic-origin high-level fits, and mutated
  N/T/L issued aggregates all fail before a coefficient. Generic extraction
  and solver fixtures remain available without gaining contract-fit authority.
- **Intervals:** not applicable; this is deterministic software validation.
- **Multiple-testing count:** zero. It repairs an authority boundary without
  adding a scientific specification.

## C0006 — Response-map and issued-aggregate repair check

- **Registered:** 2026-07-16, after the A008/A009 pre-code critique and before
  executing the repair.
- **Scope:** exact response-map metadata, weak issuance validation for contract
  moments/panels/aggregates, copied-digest forgery rejection, and preservation
  of distinct same-base structural cells.
- **Prediction before implementation:** A hand-built object carrying copied
  contract flags/digests cannot reach a high-level fit; stale or mutated issued
  objects fail; same-base response cells retain different map identities; and
  analytic objects remain usable only through extraction plus generic solvers.
- **Status:** passed for the C0006 boundary. Exact weak issuance covers
  base/cell date moments, base/cell panels, and aggregates. Dynamic mutation is
  rejected at those stages, weak-registry cleanup is exercised for the date and
  panel stages, copied-digest aggregates cannot fit, and same-base structural
  cells retain distinct response-map identities. Design-wrapper issuance is
  the separately diagnosed C0007 repair.
- **Intervals:** not applicable; deterministic capability validation only.
- **Multiple-testing count:** zero. No scientific specification changes.

## C0007 — Design-wrapper and fit-label authority repair check

- **Registered:** 2026-07-16, after the post-C0006 wrapper diagnosis and before
  implementing its repair.
- **Scope:** deterministic rejection of a replaced contract design carrying an
  altered `X0` plus a legitimate issued base moment; binding of issued array
  dtype/layout/read-only state; and exact expected response-map validation at
  both high-level fit boundaries.
- **Prediction before implementation:** The current boundary accepts the
  replaced design and forms a changed `X0'Y`. The repaired boundary rejects it
  before multiplication. Any target, recovery flag, `phi`, reliability, or
  writable-state mismatch also fails before extraction or solving, while an
  exact response identity passes the pure validator.
- **Status:** passed. Replaced designs, writable/dtype/layout state changes,
  and target, recovery-flag, `phi`, or reliability relabels fail. The
  target/recovery/`phi` checks are exercised through both high-level fit
  wrappers; exact labels pass. Equality-compatible ndarray subclass semantics
  are the later C0010 diagnosis and repair.
- **Intervals:** not applicable; deterministic capability validation only.
- **Multiple-testing count:** zero. This changes no scientific specification.

## C0008 — Reliability-reuse and inline-issuance repair check

- **Registered:** 2026-07-16, after the A011 hostile consistency review and
  before implementing the repair.
- **Scope:** canonical 0.95 smooth-moment anchoring; reuse at other registered
  reliability transforms; rejection of non-anchor contract designs; and
  removal of every callable or private receipt-to-authority minting path.
- **Prediction before implementation:** A private design kernel supplied a
  copied `G2DateReceipt` currently mints an accepted contract base moment. The
  repair makes that object unissued. The pure response-law check accepts the
  same target/recovery/`phi` at another reliability only when the expected
  identity and supplied fit reliability agree; all structural relabels fail.
- **Status:** passed. Stored moments are issued only at the canonical 0.95
  anchor and are reused for alternative fit reliabilities. Non-anchor builders
  fail, private numeric kernels cannot mint from copied receipts, and no
  callable generic issuance registrar remains.
- **Intervals:** not applicable; deterministic capability validation only.
- **Multiple-testing count:** zero. No scientific specification changes.

## C0009 — Complete issued-path software smoke

- **Registered:** 2026-07-16, after hostile review found that only rejection
  paths reached the high-level fits and before running this smoke.
- **Scope:** one complete 48-date `VALIDATION_DATE_FRONTIER` panel at target 16,
  panel 0, canonical reliability anchor 0.95, and test seed `1729`; issued base
  and cell stacking, point-weight aggregation, oracle ridge, observable ridge,
  and pooled homogeneous OLS. No coefficient is compared with a target and no
  pass/fail claim about bias, recovery, size, or power is permitted.
- **Prediction before run:** All 48 addressed dates mint one complete ordered
  panel; both issued stacks and the aggregate validate; the three high-level
  fits return finite outputs with shapes `(30,30)`, `(30,30)`, and `(3,)`; an
  expected target/recovery/`phi` relabel fails. Expected wall-clock is under 10
  seconds, hard stop 60 seconds, and peak RSS under 1 GB.
- **Status:** passed under the 60-second hard stop. The exact command was
  `/usr/bin/time -l /usr/bin/perl -e 'alarm 60; exec @ARGV' uv run pytest
  tests/test_g2_smooth.py::test_complete_issued_frontier_path_fits_all_smooth_estimators
  -q`. The final repaired path completed in 0.65 seconds wall-clock with
  maximum RSS 63,766,528 bytes and returned the three finite outputs at the
  preregistered shapes. The
  smoke also rejects structural relabels and exercises stage mutation/cleanup.
  It compares no coefficient with truth and makes no recovery, bias, size, or
  power claim.
- **Intervals:** not applicable; deterministic/software-smoke assertions only.
- **Multiple-testing count:** zero. This consumes only an authorized test seed
  and evaluates no scientific target.

## C0010 — Exact-ndarray issuance repair check

- **Registered:** 2026-07-16, after the post-C0009 dispatch diagnosis and before
  implementing its repair.
- **Scope:** deterministic rejection of equality-compatible read-only float64
  ndarray subclasses at design, moment, panel, and aggregate token validation.
- **Prediction before implementation:** A same-object issued design whose `X0`
  is replaced through `object.__setattr__` by a byte-identical subclass with an
  overridden transpose currently reaches `X0'Y`. The repaired common token
  validator rejects the subclass before downstream numeric dispatch.
- **Status:** passed after the diagnosed byte-identical ndarray-subclass attack
  failed red. Every issued token requires exact read-only C-contiguous float64
  `np.ndarray` objects before hashing or numerical dispatch.
- **Intervals:** not applicable; deterministic capability validation only.
- **Multiple-testing count:** zero. No scientific specification changes.

## C0011 — Exact retained-receipt repair check

- **Registered:** 2026-07-16, after the post-C0010 receipt-projection diagnosis
  and before implementing its repair.
- **Scope:** deterministic rejection of duck-typed or stateful substitutes for
  `G2DateReceipt`, `BaseProvenance`, `G2ResponseMapIdentity`, `G2Stream`, and
  their scalar fields at every issued smooth stage.
- **Prediction before implementation:** A same-wrapper issued aggregate with
  equality-compatible duck-typed response receipts currently passes aggregate
  token validation and the fit-label check. Exact typed projection rejects it.
- **Status:** passed after the diagnosed duck-receipt attack failed red. Exact
  receipt, provenance, response-map, stream, scalar, and nested types are
  validated before token projection and fit-label comparison.
- **Intervals:** not applicable; deterministic capability validation only.
- **Multiple-testing count:** zero. No scientific specification changes.

## C0012 — Full issued-wrapper schema repair check

- **Registered:** 2026-07-16, after the post-C0011 scalar/container diagnosis
  and before implementing its repair.
- **Scope:** exact dataclass, scalar, tuple, tuple-member, nested receipt, and
  array types for every issued smooth design, moment, panel, and aggregate.
- **Prediction before implementation:** A same-wrapper aggregate with a
  value-equal `float` subclass as `row_mass` currently reproduces the issued
  token. The repaired stage token rejects it before any covariance division.
- **Status:** passed after the diagnosed value-equal `float`-subclass attack
  failed red. Every stage-specific token checks the complete wrapper schema
  before canonical projection. Private-registry mutation remains outside the
  supported single-threaded public-API contract.
- **Intervals:** not applicable; deterministic representation validation.
- **Multiple-testing count:** zero. No scientific specification changes.

## C0013 — Single-snapshot sequence repair check

- **Registered:** 2026-07-16, after the final contract review reproduced a
  multi-traversal substitution and before repairing the stackers.
- **Scope:** deterministic/test-seed rejection of caller sequences that change
  their returned base or cell moments across traversals; exact preservation of
  one legitimate snapshot; and absence of later caller-container reads before
  panel issuance.
- **Prediction before implementation:** The pre-repair cell stacker accepts
  issued moments for its validation passes, then stacks substituted zeroed
  cross-moments and mints an issued aggregate. After repair, each stacker reads
  the caller sequence once into an exact tuple and uses only that tuple, so the
  substituted content either enters the snapshot and fails issuance or is
  never observed. Ordinary list/tuple outputs remain byte-identical.
- **Status:** passed after the preregistered red mismatch. Before repair, the
  complete 48-date state-changing sequence produced an issued cell panel whose
  90,720 cross-moment entries were all zero even though every issued input
  cross-moment was nonzero. After repair, contract and analytic snapshot
  regressions pass, the caller sequence is traversed exactly once, and the
  stacked arrays equal the validated first snapshot exactly.
- **Intervals:** not applicable; deterministic capability validation only.
- **Multiple-testing count:** zero. This changes no scientific specification.

### C0004--C0013 interim closeout evidence, reopened by C0014

- **Focused suite:** 49 deterministic/test-seed tests passed in 0.95 seconds.
- **Repository gate:** Ruff, format check, strict mypy over 18 files, 157 tests
  in 1.99 seconds, deterministic demo, and committed `results/demo`/`results/g1`
  drift checks all passed.
- **Independent review:** the final mathematical audit passed; the contract
  audit first reproduced C0013's state-changing-sequence substitution, then
  passed the one-snapshot repair with exact source and regression evidence.
- **Scientific access:** no registered resource, validation, recovery, IID,
  paper-recovery, or research stream ran. These are software-capability checks
  and do not change the empirical or scientific trial count.

## C0014 — Response-independent design-digest repair check

- **Registered:** 2026-07-16, after final code review reproduced a mismatch
  between the derived design identity and `_design_sha256`, before repair.
- **Scope:** one test-seed common-base pair at targets 0 and 16; equality of
  filtered-base identity, `X0`, packed Gram, and design digest; distinct full
  response receipts/issuance tokens; and unchanged common-base cross-cell
  response construction.
- **Prediction before implementation:** The pre-repair designs have identical
  `X0` and source-base identity but different design SHA256 values because the
  digest includes the full response receipt. The repaired digest uses only the
  response-independent source identity and exact design bytes, so the digests
  match while response authority remains distinct in issued tokens.
- **Status:** passed after the preregistered red mismatch. Same-base target 0
  and target 16 designs had byte-identical `X0` and packed Grams but different
  design digests before repair. They now share one design SHA256; their response
  maps and full issuance tokens remain distinct, common-base cross-cell
  construction still passes, and an analytic design with the same `X0` retains
  a different namespace-bound digest.
- **Intervals:** not applicable; deterministic/test-seed identity validation.
- **Multiple-testing count:** zero. No estimator or scientific specification
  changes.

### C0004--C0014 final estimator-core closeout evidence

- **Focused suite:** 49 G2 DGP/smooth/contract tests passed after C0014; the
  independent final code reviewer reproduced the post-repair result in 0.91
  seconds with targeted Ruff and strict mypy clean.
- **Repository gate:** the complete local gate passes Ruff, formatting, strict
  mypy over 18 files, 157 tests, deterministic demo, and committed
  `results/demo`/`results/g1` drift checks.
- **Issued-path smoke:** the complete 48-date test-seed-1729 path passed under a
  60-second alarm in 0.65 seconds with maximum RSS 63,766,528 bytes. It checks
  finite shapes and authority transitions only, not recovery or bias.
- **Independent review:** final mathematical and contract audits pass. Final
  code review first reopened the earlier closeout through C0014, then passed
  the response-independent design repair; its two remaining documentation
  accuracy findings were corrected before commit. Ledger and verification
  audits pass.
- **Scientific access:** no registered resource, validation, recovery, IID,
  paper-recovery, or research stream ran. These are software-capability checks
  and do not change the empirical or scientific trial count.
- **Hosted parity:** estimator-core commit
  `5500611da123bdc1dedd2124b0f2fd26e04525db` passed CI run `29492765654`;
  the parity job completed in 31 seconds. Hosted execution used only the locked
  deterministic/test-seed suite and did not open a registered G2 stream.

## C0015 — Immutable G2 panel checkpoint and test-seed recovery

- **Registered:** 2026-07-16, after deriving the persistence trust boundary and
  before checkpoint code or the seed-9191 recovery call.
- **Scope:** separate complete base-panel and cell-panel NPY artifacts; exact
  manifest/source/runtime/address/receipt/payload validation; success-last
  immutable publication; stage-specific fresh authority restoration;
  cumulative telemetry recovery; registered-seed refusal; and the single
  252-date software-recovery run frozen in preregistration amendment A019.
- **Prediction before implementation:** The current repository fails because no
  serialized loader exists. After repair, deterministic hostile cases in
  `docs/derivations/GATE_G2_CHECKPOINT_AUTHORITY.md` fail before issuance, an
  exact fresh-process round trip succeeds without any RNG draw or upstream
  replay, and the dedicated preregistration-amendment-A019 one-shot
  uninterrupted/reloaded arrays, receipts, digests, and three coefficient
  outputs match exactly. Artifact, wall-clock, and RSS hard stops are 12 MiB,
  120 seconds, and 1.5 GiB.
- **Status:** passed, including the sole preregistration-amendment-A019
  one-shot. The first red collection failed because the named checkpoint
  module did not exist. Pre-code hostile review rejected an
  initial test shape that pytest-collected seed `9191` and omitted
  fresh-process/RSS/timeout and writer-authority evidence. Post-implementation
  hostile review then reproduced a direct codec authority bypass,
  timestamp-valid stale bytecode acceptance, unreserved transient cap
  breaches of 94 and 31 bytes, loader/writer TOCTOU, direct private-child path
  overrides, missing pre-draw identity reinspection, partial final evidence,
  exited-leader process-group leakage, symlinked-ancestor mutation before
  attempt rejection, missing post-`SIGKILL` proof, replayable named-FIFO child
  authority, exceptional-path worker leakage, and dual terminal markers after
  a directory-fsync fault. Closeout additionally found that execution-source
  identity omitted the sole Make launcher and that the seed-1729 test
  attempt/result mislabeled actual date-frontier draws as recovery draws.
  The repaired checkpoint suite passes 86 tests and the seed-1729 recovery
  supervisor passes 26, including exact fresh-process recovery with all draw
  paths blocked, transient/uncertain terminal-publication fault injection,
  cleanup-interrupt precedence, fixed pre-import Make authority, launcher
  source binding, and exact stream/phase/scenario receipts. The complete
  269-test local gate, Ruff, format, strict mypy, deterministic demo, and
  committed-result drift pass. A020's live-session
  prediction/red-before-repair sequence has no immutable repository-local
  proof, so its chronology pass is explicitly qualified and current mtimes are
  not treated as evidence. Commit `5aca81115400` passed hosted CI run
  `30349473867`, including the Linux anonymous-pipe path. After explicit user
  authorization, a fresh preflight proved clean source HEAD
  `a75ea69d85c5425bd5fe824361869c3a7edb55e7`, successful matching hosted run
  `30350204001`, and absent canonical roots. The exact command
  `make g2-checkpoint-recovery` then consumed A019 once, with no retry, and
  passed. The immutable result records seed `9191`,
  `VALIDATION_RECOVERY`, 252 dates, panel 0, phase/scenario `23/0`,
  18.907810209 seconds elapsed, 178,864,128 bytes peak RSS, and 9,183,232
  allocated checkpoint bytes. Pre-checkpoint, reloaded, and fresh-process
  oracle/observable/homogeneous coefficient hashes are identical; the fresh
  process records zero RNG draws. Result SHA256
  `7061e9d5a734115cadad728e262eceb177d5eddb9f1cb6391a1f81aa040e7a3c`
  is bound by `_SUCCESS`; no failure marker exists. This consumes the only
  A019 attempt and cannot be rerun. Evidence commit
  `e328a33f0792ff81c8a0a3e6d54b7ad0a7563f7e` passed hosted CI run
  `30386325383`.
- **Intervals:** not applicable; software integrity/recovery only.
- **Multiple-testing count:** zero. No coefficient is compared with truth.

## C0016 — A022--A026 conditional, restartable G2 resource admission

- **Registered:** 2026-07-28, through append-only preregistration amendment
  A022, followed on 2026-07-29 by pre-implementation amendments A023--A025
  and on 2026-08-06 by pre-implementation amendment A026, before resource-run
  code, rehearsal, or any registered resource, validation, or research RNG
  access.
- **Scope:** preserve the frozen fourteen kernels, full validation/research
  work matrix, science, seeds, and budgets while replacing only the impossible
  one-unit resource bundle and last-three-only admission statistic. Measure
  fixed operand-complete cold/equal blocks, exact non-`W`-proportional phase
  traces, thermal stationarity, blocked temporal stability, shared-kernel
  cross-context robustness, source/runtime/artifact provenance, process-tree
  RSS, three-root disk, registries, crash/resume, and success-last publication.
  Amendment A024 freezes exact record order
  `k1,k2,k3,k4,k5,k6,k7,k9,k10,k8,k11,k12,k13-recovery,k13-research,k14`,
  a composite k1+k2 epoch, minimal resume-only panels/weights/focals, one
  ordinary/resume aggregate-recomputation path, cleanup intents, chained
  interruption evidence, and immutable terminal-failure selection. Amendment
  A025 closes the receipt-stage, entry-level cleanup, failure-checkpoint,
  process-death, reservation-ancestry, thermal-reset, telemetry-continuity,
  finite-evidence, paper-weight, failure-prefix, and terminal-success schemas
  without changing the record order, numerical work, or scientific addresses.
  Amendment A026 makes any interruption inside a rate-bearing trace terminal,
  adds an inherited Darwin `flock` quiescence lease to launch intents, and adds
  successor-rebuildable forensic terminal nonpass after an uncertifiable exact
  success/failure terminal-entry state.
- **Prediction before implementation:** The repository fails closed because no
  typed compute parser, resource config/capability/supervisor, complete paper
  and interval paths, or byte-licensed new artifacts exist. After test-seed
  repair, three fixed seed-1729 rehearsals at panels `10000..10002` must show
  each of `k3=25,k4=225,k5=225,k6=225,k7=4096` lasting at least 100 ms without
  tuning. Each repaired trace must close seven resume-state rows, and the
  successful rehearsal must retain exactly 13 artifact-kind counts and 51
  artifact rows, publish 45 canonical boundaries and 12 cleanup intents, and
  expose 57 capped ordinary checkpoint intervals plus one terminal
  accounting row: 58 resource-accounting rows in total. The 60-second terminal
  value is a fixed charge, not an end-to-end close-time claim. Only then may a
  quantitative registered prediction be append-sealed
  and hostile-reviewed.
- **Status:** current deterministic red; design registered, resource-path
  implementation and rehearsal not started. The first two independent hostile design reviews failed eight
  material ambiguities. A fresh methodological review then rejected the
  repaired draft's full-mixture interpretation, and a fresh systems review
  found six byte-level blockers. A023 now makes projection conditional, retains
  six temporal rows, adds 72 cross-context rows, counts nine registries, and
  freezes three-source rehearsal identity, literal NPY bytes, deterministic
  stages/debris, retained rehearsal inventory rows, and exact disk/statvfs
  encodings. Recovery review then rejected the A023 package because k1's
  boundary was not executable on resume and k8's parents did not yet exist.
  A024 repairs dependency order and operand lifetime and adds conservative
  replay, cleanup, interruption, and terminal-failure journals. The first
  hostile A024 review failed nine further transitions. Three fresh independent
  hostile reviews of the corrected A024 package then failed receipt
  publication, entry-level cleanup, terminal checkpoint/clock, process-death,
  reservation ancestry, thermal reset, telemetry continuity, finite evidence,
  paper-weight lifecycle, failure-prefix, and terminal-success closure. A025
  incorporated those findings. Fresh A025 schema review passed, but methods
  review found interruption-tainted rate evidence and systems review found
  launch-only and terminal-entry consumed dead ends. A026 records the
  append-only repair, with active config seal 9,799 bytes/
  `3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
  194 leaf rows/type-tree
  `e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.
  Fresh A026 methods and systems reviews passed. Schema review failed first on
  an LF-omitting type-tree hash and then on one stale abbreviated prefix; after
  both clerical corrections, an independent third recomputation passed 9,799
  bytes, the config hash, 194 rows, 9,473 CJSON bytes, and the corrected
  type-tree hash with no stale residue. Document authority is accepted, but the
  executable gate remains red: the resource capability/supervisor, complete
  paper-cache path, and rehearsal do not exist. C0017 later projects sealed
  cache/aggregation semantics without creating those paths. The latest locked
  deterministic gate passed Ruff, format, strict mypy over 26 source files, all
  306 tests, deterministic demo regeneration, and committed-result drift.
- **Intervals:** eventual timings use the named
  `[max(1,D-2h),D+2h]` clock-resolution enclosure, warm-block min--max ranges,
  and exact rational upper projections; three serial warm blocks are never
  called a probabilistic confidence interval.
- **Multiple-testing count:** zero scientific trials. Deterministic failure
  classes, test-seed software rehearsals, and resource timing diagnostics do
  not inspect coefficients against truth or alter the scientific trial ledger.
- **Access:** registered resource seed `2026071529`, validation seed
  `2026071521`, research seed `2026071522`, empirical data, evaluation data,
  and holdout remain untouched.

## C0017 — Typed paper-cache and aggregation contract projection

- **Registered:** 2026-08-06 in the test-first contract slice committed as
  `634d6133d232`, after A026 document acceptance and before implementation. The
  RED test named the exact sealed fields and prohibited inference of an
  8,460-field representation order.
- **Scope:** project the existing `paper_reconstruction` semantics from
  `configs/g2.toml` into `PaperReconstructionContract`: equal-block/date
  coefficient aggregation, pooled OOS SSE/SST prediction aggregation, shared-
  weight bootstrap aggregation with no LASSO refit, the nine paper-cache matrix
  names, cached loss fields, 7,200 reported coefficient-map values, 180
  reported OOS values, and the two cache-only loss components. Enforce exact
  runtime types and sealed identity. Do not assemble a paper matrix, flatten a
  cache, create a resource fixture, or access RNG.
- **Prediction before implementation:** the focused contract test fails on the
  missing `coefficient_aggregation` attribute. After the smallest semantic
  projection, that test and the neighboring reconstruction contract test pass;
  the full deterministic repository gate remains green. Any attempt to accept
  integer `0` for `bootstrap_refit`, reorder a cache, or infer serialization
  authority fails the slice.
- **Status:** passed for typed semantic capability only. The initial focused
  test failed exactly on the absent attribute. Commit `916022bb2b76` added the
  nine fields, an exact-Boolean parser, runtime representation checks, and
  sealed-identity validation. The two focused tests and all 10 G2 contract
  tests passed. Ruff, format checking over 26 files, strict mypy over 26 source
  files, all 306 tests in 36.99 seconds, the 64-row deterministic G0 demo with
  expected hashes, and committed-result drift passed. Independent review found
  no authority widening. Paper matrix assembly, cache serialization, 8,460-
  vector order, resource fixtures, and registered execution remain absent.
  The version-0.1 pre-results manuscript and README may report this only as
  software verification, not as resource feasibility or a scientific result.
- **Intervals:** not applicable; deterministic contract and software checks
  only.
- **Multiple-testing count:** zero. No new draw or coefficient-to-truth
  comparison occurred.
- **Access:** test seed 1729 was not needed. Registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  external market data, evaluation data, and holdout remain untouched.

## C0018 — A027 paper-cache index and in-memory codec

- **Registered:** 2026-08-06 after the append-only A027 representation
  derivation and independent methods/schema passes, before changing the A026
  parser seal, creating an order module, or running a focused test. The hostile
  scope review remains failed until implementation, ledgers, and red-team
  state agree.
- **Scope:** update only the typed resource-config seal/order-table projection;
  implement the exact research and recovery field/index bijections; and pack
  and unpack already-computed, finite float64 matrices/loss arrays to owned,
  C-contiguous, read-only in-memory vectors. No paper estimator, NPY writer,
  path, artifact kind, fixture, bootstrap batch, resource root, Make target,
  capability, random-number constructor, rehearsal, or registered path may be
  added.
- **Prediction before tests:** the first focused resource-contract test fails
  with the existing A026 byte-count seal when it reads the 10,863-byte A027
  config. A separate wished-for order test fails because
  `xid.models.g2_paper_cache` does not exist. After the smallest implementation,
  literal asymmetric sentinels recover exact indices `0`, `899`, `900`,
  `2699`, `2700`, `3599`, `7199`, `7200`, `8099`, `8100`, `8279`, `8280`,
  `8339`, and `8459`; quotient/remainder inverses round-trip every field;
  `(sse,sst)` cannot swap; and recovery cannot pass as a research prefix.
  Packed vectors must not share memory with sources, and unpacked arrays must
  not share memory with their vector.
- **Configuration prediction:** the resource config reproduces 10,863 ASCII
  bytes and SHA256
  `1a14fd68012819d5f901a97ddd9e9a58dd35886bdcc5d47728467f6417fc3cd3`;
  its type tree reproduces 209 rows, 10,369 bytes, and SHA256
  `81eed87be58bf04a897fdcf3dd39cf142944647824a9f97938d46f341803a2ff`;
  and its 1,057-byte order manifest reproduces SHA256
  `8810471ce6c0747af7cdda48299989303cd85a9c7def7c681f2a57f93348a083`.
- **Observed RED:** the first resource-contract run failed exactly at the stale
  A026 parser seal: four tests failed and eleven passed, with every failure
  reporting `sealed resource config: byte count drift`. After the parser was
  updated, all 15 resource-contract tests passed. The first order run then
  failed all five wished-for tests because `xid.models.g2_paper_cache` did not
  exist. After the index implementation, all five passed. The pack/unpack RED
  preserved those five passes and failed the five new tests on the absent
  payload/codec surface.
- **Observed GREEN:** the final focused slice passed all 25 resource-contract
  and cache-order tests in 0.15 seconds. Literal asymmetric sentinels matched
  every preregistered boundary, the complete 8,460- and 960-field inverses were
  bijective, recovery mapped to research positions `2700:3600` and
  `8280:8340` rather than a prefix, and packed/unpacked arrays were exact
  float64, owned, C-contiguous, read-only, finite, and non-aliasing. The
  manifest reproduced 1,057 bytes and SHA256
  `8810471ce6c0747af7cdda48299989303cd85a9c7def7c681f2a57f93348a083`.
  The repository-wide deterministic gate passed Ruff, format checking over 28
  files, strict mypy over 28 source files, all 317 tests in 37.07 seconds, the
  64-row G0 demo with expected hashes, and committed-result drift.
- **Status:** passed for A027 deterministic representation capability only.
  No serializer, artifact, fixture, bootstrap batch, resource capability,
  rehearsal, or registered execution path was implemented; C0016 resource
  admission remains executable-red.
- **Intervals:** not applicable; deterministic representation checks only.
- **Multiple-testing count:** zero. No stochastic draw or coefficient-to-truth
  comparison is part of this slice.
- **Access:** test seed 1729 is not required. Registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  external market data, evaluation data, and holdout remain untouched.

## C0019 — A028 confounding rank bound, partial identification, and diagnostic

- **Registered:** 2026-08-12 after the append-only A028 derivation in
  `docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md` and the six frozen
  predictions in `docs/predictions/THEORY_EXTENSION.md`, and before any
  identification module, rank diagnostic, exhibit generator, figure, or
  manuscript revision existed.
- **Scope:** prove and implement the rank bound on the confounding gap, the
  identified-set characterisation, the closed-form one-spike interval, and the
  diagonal-plus-rank-`K` departure statistic; generate every manuscript number
  deterministically; and revise the preprint and README. No paper estimator,
  registered stream, RNG namespace, market data, G2 kernel, threshold, or
  sealed digest change was permitted.
- **Prediction before tests:** the numerical rank of the gap equals `3`, `4`,
  `5`, `30` at `rank(B)` of `0`, `1`, `2`, `30`, each within `K + rank(B)`; a
  diagonal truth gives an exactly rank-3 gap with nonzero off-diagonals and
  `psi_3 < 1e-8`; `psi_3` increases strictly over the frozen perturbation grid;
  the closed-form identification scale agrees with a bisection over the exact
  positive-semidefiniteness frontier to below `1e-10`; `psi_3` is permutation
  invariant below `1e-12`; and the one-spike gap is entrywise constant below
  `1e-12`.
- **Observed RED:** the first identification run failed collection with
  `ModuleNotFoundError: No module named 'xid.models.identification'`. The
  one-spike extension then failed with
  `ImportError: cannot import name 'identification_scale'`. The diagnostic run
  failed with
  `ModuleNotFoundError: No module named 'xid.models.rank_diagnostic'`. The
  exhibit run failed all 11 tests on the absent generated directory, and the
  published-summary slice failed 4 tests on the absent
  `published_control_shift` block.
- **Observed GREEN:** all six predictions hold. Gap ranks are `3`, `4`, `5`,
  `30` against bounds `3`, `4`, `5`, `33`. A strictly diagonal truth yields a
  rank-3 gap whose largest off-diagonal is `0.2207424367` against realised
  own-impact spanning `0.2061484059` to `0.3952712629`. `psi_3` at exact
  structure is `1.759954843e-15` and is strictly increasing over the grid.
  The closed-form scale matches bisection to `9.8e-16` relative. The one-spike
  gap is constant across all 900 entries. Sharp intervals are
  `[-0.08375252224, 0.1048599132]` at `o = 0.0029` and
  `[-0.0781658777, 0.1026732686]` at `o = 0.0046`; both contain zero and the
  half-width is `8.94` and `7.38` times the observed off-diagonal.
- **Published-summary exhibit, split outcome:** the dispersion implication is
  consistent, with a reported mean cross-coefficient shift of `-0.071` against
  an unchanged cross-sectional standard deviation of `0.06` and an
  own-coefficient standard deviation moving only from `0.78` to `0.77`. The
  distribution-shape implication fails: the predicted post-control negative
  fraction is `0.7421538892` against a reported `0.8446`, a gap of
  `0.1024461108` exceeding the declared `0.05` tolerance. Under the registered
  failure rule the one-spike convention was not retuned; the disagreement is
  reported in the manuscript, the README, and the red-team memo.
- **Status:** passed for deterministic identification theory, representation,
  and dissemination only. No serializer, artifact, fixture, bootstrap batch,
  resource capability, rehearsal, or registered execution path was implemented;
  C0016 resource admission remains executable-red.
- **Intervals:** not applicable. Every reported quantity is a deterministic
  algebraic identity or an exact evaluation of one, and is labelled as such
  rather than given a fabricated interval. Published dispersion figures were
  not promoted to confidence intervals.
- **Multiple-testing count:** zero. No stochastic draw and no
  coefficient-to-truth comparison is part of this slice.
- **Strongest unresolved objection:** `psi_K` depends on an assumed factor
  count and has no derived finite-sample null distribution, so it is a
  population restriction with a descriptive sample analogue rather than a
  hypothesis test. Recorded in `docs/redteam/THEORY_EXTENSION.md`.
- **Access:** test seeds `1729` and `9191` only. Registered resource seed
  `2026071529`, validation seed `2026071521`, research seed `2026071522`,
  external market data, evaluation data, and holdout remain untouched. Sealed
  digests `f6291894...` for `configs/g2.toml` and `1a14fd68...` for
  `configs/g2_resource.toml` were verified unchanged.

## C0020 — A029 execution cost under low-rank confounding

- **Registered:** 2026-08-12 after the A029 derivation in
  `docs/derivations/EXECUTION_COST_UNDER_CONFOUNDING.md` and the five frozen
  predictions in `docs/predictions/EXECUTION_COST.md`, and before any execution
  module, robust scheduler, exhibit, figure, or manuscript section existed.
- **Scope:** derive and implement the rank-`K` cost error and its immune
  subspace, the one-spike exposure law, the identified cost interval, and the
  closed-form minimax-cost schedule. No dynamic schedule, decay kernel,
  risk-aversion term, registered stream, market data, or sealed-digest change
  is permitted.
- **Pre-implementation correction to Prediction 2.** The first registration of
  Prediction 2 was defective and was corrected before any implementation
  existed. Two faults: it did not pin the generator used to draw the trade
  vectors, so its percentages were not reproducible; and it placed the
  index-versus-neutral contrast in the general fixture, where `Gamma` and
  `Delta_f` are generic normal draws and the equal-weight direction has no
  privileged relationship to the confounding subspace. That contrast belongs to
  the one-spike geometry, where `m` is the confounding direction. The trade
  generator is now pinned to seed `9191` in the order random-unit then
  confound-neutral, and the corrected values are recorded separately for the
  general fixture (`-9.8113%`, `-9.7661%`, `+0.0000%`) and for the one-spike
  geometry (`+54.2302%`, `+5.4183%`, `+0.0000%`). Predictions 1, 3, 4, and 5
  were verified unaffected and stand as first registered. No result was
  retrofitted to a number already published, and no fixture, target, or
  calibration was re-drawn to recover the original percentages.
- **Observed RED:** the first execution run failed collection with
  `ModuleNotFoundError: No module named 'xid.models.execution'`.
- **Observed GREEN, local:** all 22 focused tests passed on the first
  implementation run and all five predictions held. The immune subspace has
  dimension exactly `N - K = 27`; the confound-neutral trade carries cost error
  `5.204170e-17`; general-fixture relative errors are `-9.8113%`, `-9.7661%`,
  and `+0.0000%`; one-spike relative errors are `+54.2302%`, `+5.4183%`, and
  `+0.0000%`; the exposure ratio equals `N g = 0.2296108639`; the identified
  cost half-width is `(T/N)(1'x)^2` with `T/N = 0.0904195732` and is exactly
  zero for a dollar-neutral trade; and the minimax schedule improves worst-case
  cost by `0.0000%`, `0.0000%`, and `3.1095%` while matching a 20,000-point
  grid search.
- **Observed FAILURE on hosted Linux, and its diagnosis.** Prediction 3 failed
  in hosted continuous integration. The registered tolerance demanded an
  absolute spread below `1e-12` in the exposure ratio, a quantity of magnitude
  `0.23`, which is about twenty units in the last place. Linux reproduced the
  ratio with a spread of `7.4e-11` between `0.22961086389613597` and
  `0.2296108638224396`, a relative discrepancy of `3.2e-10`, while macOS stayed
  below `1e-12`. The ratio is a reduction over 900 float64 products and its
  final digits depend on BLAS blocking, so the registered tolerance was tighter
  than float64 delivers portably. This is a defect in the tolerance, not
  evidence against the exposure law, since a genuine violation of a
  proportionality claim would appear in the leading significant digits rather
  than the tenth. The tolerance is restated as `1e-9` relative, three times the
  largest observed spread and six orders below any structural effect, and the
  amendment is recorded in `docs/predictions/EXECUTION_COST.md`. The companion
  assertion on the general-fixture neutral trade was widened from `1e-15` to
  `1e-13` for the same reason, still eleven orders below the `1e-2` structural
  errors in that fixture. No predicted value was changed and no fixture was
  re-drawn.
- **Recurrence note:** this is the second tolerance defect of the same kind in
  this project, after the A028 exhibit that serialised ten significant digits
  of an analytic zero. Both arose from fixing a tolerance against a single
  platform before the cross-platform result existed. Future numerical
  predictions state tolerances in relative terms and are set from the expected
  conditioning of the computation rather than from an observed macOS run.
- **Status:** passed for deterministic execution-cost theory only, after the
  Prediction 3 tolerance amendment. No dynamic schedule, decay kernel, or
  registered execution path was implemented; C0016 resource admission remains
  executable-red.
- **Intervals:** not applicable; deterministic algebraic evaluations only.
- **Multiple-testing count:** zero.
- **Access:** test seeds `1729`, `9191`, and `314159` only. Registered seeds,
  external market data, evaluation data, and holdout remain untouched.

## C0021 — A030 finite-sample null distribution for the departure statistic

- **Registered:** 2026-08-12 after the derivation in
  `docs/derivations/PSI_NULL_DISTRIBUTION.md`, with its exploratory pilot
  explicitly disclosed, and before any bootstrap implementation or confirmatory
  run existed.
- **Scope:** supply a sampling distribution for `psi_K` so the diagnostic
  becomes a test, fix a factor-count rule before use, and report realised size
  and power. No dependent bootstrap, heteroskedastic model, registered stream,
  or market data.
- **Pilot disclosure:** size and power tables were first produced at seeds
  `1729` and `9191` before registration and were labelled exploratory. The
  confirmatory run used the fresh sampling seed `314159` fixed in the
  registration.
- **Observed RED:** the first study run failed with
  `ModuleNotFoundError: No module named 'xid.psi_study'`; the first artifact
  check failed on the absent `psi_study.json`.
- **Observed GREEN:** all five registered predictions hold at the confirmatory
  seed. Realised size at nominal 5% is `0.267`, `0.127`, `0.100`, and `0.040`
  at `T` of 500, 1,000, 2,000, and 5,000, with Monte Carlo standard error
  `0.0178`. Power at `T = 5000` is `0.070`, `0.270`, `0.870`, and `1.000`
  against Frobenius perturbations of `0.05`, `0.10`, `0.20`, and `0.40`, with
  standard error `0.0218`. The null manifold has dimension `201` against `900`
  free parameters.
- **Registered negative result, confirmed:** the degrees-of-freedom variance
  inflation of `1.134704` produces realised size of exactly `0.000` at every
  sample size, removing all power. It remains **not adopted**. The plug-in bias
  lies in the centre of the null distribution rather than its scale, so a scale
  correction cannot reach it.
- **Usage bound:** the test is usable only above roughly `T = 5 N^2`. Below
  that it over-rejects severely, and the manuscript states the bound rather
  than implying general validity.
- **Effect on the standing objection:** objection 2 of
  `docs/redteam/THEORY_EXTENSION.md` is now partially resolved. `psi_K` is a
  test rather than a descriptive statistic, but only for large samples and only
  under a Gaussian, homoskedastic, serially independent sampling model. The
  factor count remains assumed, and the selection rule was validated on one
  fixture where the true count was known.
- **Status:** passed. C0016 resource admission remains executable-red and G2
  remains open.
- **Intervals:** rejection rates are Monte Carlo proportions reported with
  binomial standard errors at `M = 150` and `M = 100`; that is the named
  interval method. All other quantities are deterministic.
- **Multiple-testing count:** zero. No coefficient-to-truth comparison and no
  registered stochastic draw is part of this slice.
- **Access:** test seeds `1729`, `9191`, and `314159` only. Registered seeds,
  external market data, evaluation data, and holdout remain untouched.

## C0022 — A031 paper-matrix assembly, implemented and cost-blocked

- **Registered:** 2026-08-12 after the A031 derivation and predictions, before
  any assembly driver existed.
- **Observed RED:** the first run failed with
  `ModuleNotFoundError: No module named 'xid.models.g2_assembly'`, then with
  `ValueError: y_values must have 1 dimensions` from passing a two-dimensional
  fold response into the LASSO preparation kernel.
- **Observed GREEN, partial:** the driver is implemented and the fail-closed
  boundary is verified. Non-float64 panels, wrong bin counts, and nonfinite
  returns are all rejected, and the sealed specification order is asserted.
  Four tests pass.
- **NOT VERIFIED:** the eight registered A031 predictions are **not** confirmed.
  They require a complete date assembly, which costs about 4.2 hours at the
  sealed solver numerics, so they are implemented but skipped behind
  `XID_RUN_SLOW_ASSEMBLY`. **A031 must not be recorded as passed.**
- **Blocking measurement:** a warm-started 40-ratio LASSO path over realistic
  structured features takes `3.356` seconds, with per-solve median `45.2` ms
  and maximum `259.4` ms. The solver is healthy: median `413` sweeps against a
  `10,000` cap, and zero of forty solves reach the cap. Applying the median to
  the registered `60,782,400` LASSO solutions gives `763` hours, which is `48x`
  the 16-hour expected envelope and `24x` the 32-hour hard envelope. Fitting the
  expected envelope requires `948` microseconds per solve against `45,200`
  measured. Recorded in `docs/redteam/PAPER_ASSEMBLY_COST.md`.
- **Consequence:** the A022 quantitative prediction seal must not be written
  against this implementation, because the projection it would record is known
  wrong by more than an order of magnitude. G2 stays executable-red for a
  reason that is now quantitative rather than procedural.
- **Status:** implementation complete, verification blocked on throughput. Not
  a pass.
- **Intervals:** timing figures are single-machine medians over forty solves and
  carry no inferential interval; they are reported as measurements, not
  estimates.
- **Multiple-testing count:** zero.
- **Access:** test seed `1729` only. Registered seeds, market data, evaluation
  data, and holdout remain untouched.

## A035 — identified linear and quadratic functionals

- **Registered before implementation:** `docs/derivations/IDENTIFIED_FUNCTIONALS.md`
  and the A035 block of `PREREGISTRATION.md` were written and committed before
  `src/xid/models/functionals.py` existed.
- **Result:** with `W = Sigma_qq^{-1} Delta_f`, the linear functional
  `a' Lambda b` is point identified over the identified set if and only if
  `W' b = 0`, and the execution cost `x' Lambda x` if and only if `W' x = 0`.
  The condition binds the flow argument alone: orthogonalising the response
  argument leaves the spread at `7.40` against `6.65` for a free pair, while
  orthogonalising the flow argument collapses it to `3.0e-15`.
- **Reach of the published corollary:** in the one-spike geometry
  `col(W) = span(m)` to `|cos| = 1.000000000000`, so the dollar-neutral cost
  result the manuscript already reports is exactly this theorem's instance.
  It generalises to `W' x = 0`; it does not generalise to any other geometry
  by accident.
- **Width:** `width{x' Lambda x} = 2 R ||x|| ||W' x||` for admissible loadings
  in a Frobenius ball of radius `R`, attained at `Gamma* = R (x w')/||x w'||_F`.
  Verified against the maximiser to `1e-10` relative at four trade scales.
- **Disclosed error:** the width was first conjectured proportional to
  `||W' x||` alone. Ratios of `3.44, 4.28, 2.58, 5.28` falsified it before it
  reached the derivation, and a 20,000-direction random search undershot the
  supremum by roughly half. Both are recorded in the derivation as evidence
  that sampling an admissible set is not a substitute for its attaining point.
- **Status:** all five registered predictions hold. Deterministic; test seed
  `1729` only.
- **Intervals:** none apply; these are population statements about an
  identified set with no sampling variation.
- **Multiple-testing count:** zero.
- **Access:** no registered seed, market data, evaluation data, or holdout was
  touched.

## A036 — generic sharpness of the confounding-gap rank bound

- **Registered before implementation:** `docs/derivations/GENERIC_GAP_RANK.md`
  and the A036 block of `PREREGISTRATION.md` were written before
  `src/xid/models/gap_rank.py` existed.
- **Result:** the gap factors as `G = L R` with inner dimension
  `K + rank(B)`. When `K + rank(B) <= N` and the stated regularity conditions
  hold, both factors have full rank and Sylvester's rank inequality forces
  `rank(G) = K + rank(B)` exactly. The manuscript's "generically attained" is
  now a theorem rather than an assertion.
- **Observed:** `rank(G) = min(N, K + rank(B))` in all forty draws of each of
  ten configurations, with no draw disagreeing in any cell. The factorisation
  matched `confounding_gap` to `1.3e-14`.
- **Exceptional set:** every hypothesis was violated in turn and each violation
  lowered the rank by exactly the predicted amount. The economically
  interesting one is `col(Gamma) ∩ Sigma_uu col(B') = {0}`: when a priced-risk
  direction aligns with a feedback direction transported by `Sigma_uu`, the two
  confounding channels overlap and the data count them once, not twice.
- **Consequence for the theory's content:** when `K + rank(B) >= N` the gap is
  generically of full rank and carries no low-rank restriction at all. Every
  testable implication of this paper therefore requires a factor-plus-feedback
  budget strictly below the cross-section size, and that condition is now
  stated rather than assumed.
- **Limitation carried forward:** the capped case `K + rank(B) > N` rests on
  genericity plus numerical witnesses, not a closed-form proof. Labelled as
  such in the derivation and wherever the result is used.
- **Status:** all five registered predictions hold. Deterministic; seeds
  `1000..1039` and `2000..2029` only.
- **Intervals:** none apply; population ranks with no sampling variation.
- **Multiple-testing count:** zero.
- **Access:** no registered seed, market data, evaluation data, or holdout was
  touched.

## A037 — execution regret under a confounded impact matrix

- **Registered before implementation:** `docs/derivations/EXECUTION_REGRET.md`
  and the A037 block of `PREREGISTRATION.md` preceded
  `src/xid/models/regret.py`.
- **Result:** for `min x' A_s x` subject to one linear constraint, the loss
  from acting on the confounded matrix obeys the exact identity
  `Regret = delta' Lambda_s delta` with `delta = x_A - x_L`, verified to
  `1.1e-17`. Regret is therefore the true cost of the error in the *trade*,
  never negative, and never the cost of the error in the matrix.
- **The practically important consequence:** a first-order error in the impact
  matrix produces only a second-order loss in execution,
  `Regret = eps^2 (Pi G_s x_L)' Lambda_s^{-1} (Pi G_s x_L) + O(eps^3)`.
  Observed ratios `Regret/eps^2` rise monotonically to the predicted
  `0.003388738`, and successive halvings divide regret by `3.91, 3.95, 3.98`.
  At `eps = 0.4` the regret is `0.87%` of the optimal cost; at `eps = 0.05` it
  is `0.015%`.
- **Zero-regret condition:** `Pi G_s x_L = 0`. Any gap proportional to
  `Lambda_s` qualifies, since the argmin is scale invariant. This is the
  decision-side analogue of the A035 identified-functional condition.
- **Disclosed correction, pre-commit:** registered prediction 5 compared the
  rescaling gaps against a generic gap "of the same Frobenius norm". That is
  ill-posed — such a gap drives the believed matrix indefinite, smallest
  eigenvalue `-0.537`, so no trade exists to compare. The comparison was moved
  inside the admissible region at `eps = 0.05` and the correction recorded in
  both the derivation and the preregistration rather than silently applied. A
  test now pins the ill-posedness itself.
- **Status:** all five registered predictions hold as corrected.
  Deterministic; seed `1729` only.
- **Intervals:** none apply; population quantities with no sampling variation.
- **Multiple-testing count:** zero.
- **Access:** no registered seed, market data, evaluation data, or holdout was
  touched.

## A038 — converse to the cross-block rank restriction

- **Registered before implementation:** `docs/derivations/CROSS_BLOCK_CONVERSE.md`
  and the A038 block of `PREREGISTRATION.md` preceded
  `src/xid/models/cross_block_converse.py`.
- **Result (i), content boundary:** the restriction is non-vacuous if and only
  if `K(2N-K) < N^2-N`, which reduces exactly to `K < N - sqrt(N)`. This is a
  second budget constraint beside Corollary 10.1: the gap loses its low-rank
  structure at `K + rank(B) >= N`, and the test loses its power to detect
  anything at `K >= N - sqrt(N)`. At `N = 30` these bind at `K = 30` and
  `K = 25`.
- **Result (ii), global converse at `K = 1`:** with `N >= 4` and three nonzero
  anchors, vanishing disjoint tetrads force `A_ij = x_i y_j` off the diagonal,
  giving an explicit rank-one completion. Recovered from off-diagonal entries
  alone to `4.4e-16`, with `rank(A - D*) = 1` at every `N` tested. At `N = 3`
  the tetrad family is empty, so the `N >= 4` hypothesis is load-bearing.
- **Result (iii), local converse for general `K`:** the tangent space of the
  cross-block minor variety at a generic diagonal-plus-rank-`K` point has
  dimension exactly `K(2N-K)`, matching the off-diagonals of rank-`K` matrices,
  in all nine configurations across `K = 1, 2, 3`. The restriction is therefore
  a local characterisation, not merely a necessary condition.
- **Left open, and reported as open:** for `K >= 2`, whether some `A` satisfies
  every disjoint cross-block bound while admitting no rank-`K` diagonal
  completion. Tangent-space equality at generic points of the model does not
  exclude other irreducible components. Neither proved nor refuted. The
  practical consequence is narrow, since rejection uses only the forward
  implication of Theorem 9; it is non-rejection whose reading would tighten.
- **Not imported:** the Ledermann bound governs the symmetric Frisch problem,
  a different count from the asymmetric coefficient matrix here. Condition (1)
  is the count that applies and is derived rather than borrowed.
- **Status:** all five registered predictions hold. Deterministic; seeds `7`
  and `11` only. Tangent ranks are numerical, from finite differences at
  `h = 1e-6` read at relative threshold `1e-6`, and are labelled as such.
- **Intervals:** none apply; population statements with no sampling variation.
- **Multiple-testing count:** zero.
- **Access:** no registered seed, market data, evaluation data, or holdout was
  touched.

## A039 — dependence-robust inference for the cross-block restriction

- **Registered before implementation:** `docs/derivations/CROSS_BLOCK_INFERENCE.md`
  and the A039 block of `PREREGISTRATION.md` preceded
  `src/xid/models/cross_block_inference.py` and `src/xid/crossblock_study.py`.
- **Construction:** per-date sufficient statistics reduce any date weighting to
  a weighted sum of small matrices, the bootstrap is recentred on the rank-`K`
  truncation of the observed block so the resampled distribution is a null
  distribution, and whole dates are resampled so within-day dependence of
  arbitrary form is preserved without being modelled.
- **Headline finding:** the procedure implied by treating bins as independent
  observations rejects a true null in **every replication**, `1.000` at both
  the 5% and 10% levels. Any cross-impact rank test that resamples
  high-frequency observations independently manufactures rejections out of
  serial correlation alone. The date-cluster scheme holds its level at `0.040`
  and `0.080`.
- **Power, reported with its limits:** at `D = 50` the rejection rate runs
  `0.040, 0.227, 0.873, 1.000, 1.000` across `cross` in
  `{0, 0.05, 0.10, 0.20, 0.40}`; at `D = 200` it runs
  `0.053, 0.920, 1.000, 1.000, 1.000`. A non-rejection on a short panel is
  close to uninformative, so `D` must be reported beside every `p`-value.
- **Provenance:** both tables were regenerated from the shipped implementation
  and agree with the exploratory run to the last digit reported. The four
  registered predictions execute as tests behind `XID_RUN_SLOW_INFERENCE=1`.
- **Reporting rule registered:** applications must report the whole map
  `K -> p_K` over a prespecified range with `D`, `B`, index sets, and replicate
  count. No `K` is selected here.
- **Status:** all five registered predictions hold, verified against the module
  rather than the exploratory script.
- **Intervals:** rejection rates are Monte Carlo proportions over 150–200
  replications; registered acceptance bands are intervals for that reason.
- **Multiple-testing count:** zero.
- **Access:** simulated data only. No registered seed, market data, evaluation
  data, or holdout was touched.
