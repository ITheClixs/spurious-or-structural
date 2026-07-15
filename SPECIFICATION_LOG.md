# Specification log

Every statistical or pipeline specification is appended in execution order.
The trial count used for later multiple-testing correction includes failed and
abandoned research specifications. Software-only TDD red/green cycles are not
empirical model trials, but gate-level pipeline variants are recorded.

## Trial counts

- Empirical specifications: **0**
- Simulation estimator specifications: **1 registered, 0 run**
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
- **Status:** registered, not run. The test-first implementation passes 25 G1
  software tests and the full 38-test locked suite after the resume-guard
  repair. Stochastic software tests use only nonregistered test seeds and do
  not evaluate the gate threshold; neither registered seed has been drawn.
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
- **Multiple-testing count:** included as one simulation specification. Crash
  recovery with identical validated shards remains the same attempt; changing
  the seed, sample size, fixture, target, accumulator, or metric creates a new
  attempt.
