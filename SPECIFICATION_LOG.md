# Specification log

Every statistical or pipeline specification is appended in execution order.
The trial count used for later multiple-testing correction includes failed and
abandoned research specifications. Software-only TDD red/green cycles are not
empirical model trials, but gate-level pipeline variants are recorded.

## Trial counts

- Empirical specifications: **0**
- Simulation estimator specifications: **0**
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
- **Multiple-testing count:** excluded from empirical/model trial counts because
  no effect, model, or hypothesis is evaluated.
