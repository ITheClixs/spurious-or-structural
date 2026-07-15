# Specification log

Every statistical or pipeline specification is appended in execution order.
The trial count used for later multiple-testing correction includes failed and
abandoned research specifications. Software-only TDD red/green cycles are not
empirical model trials, but gate-level pipeline variants are recorded.

## Trial counts

- Empirical specifications: **0**
- Simulation estimator specifications: **1 run and passed; 2 G2 designs rejected pre-run; 1 G2 design registered and pending**
- Software-only pipeline specifications: **1 completed**
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
  at the pre-implementation contract boundary, unimplemented, and unrun.
  Documentation commit `a5c7f1c02e941a0d6fdef3d645dfea63884cdfd7`
  passed hosted CI run `29448917107`; test-first implementation with test-only
  seeds is open. Registered resource, validation, and research streams remain
  blocked. S0002 and S0003 remain non-executable.
- **Multiple-testing count:** one new specification. No stochastic run exists
  until a registered stream is consumed.
