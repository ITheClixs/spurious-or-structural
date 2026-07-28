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
  A019 attempt and cannot be rerun.
- **Intervals:** not applicable; software integrity/recovery only.
- **Multiple-testing count:** zero. No coefficient is compared with truth.
