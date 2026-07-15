# Research state

Last updated: 2026-07-15

## Current gate

**G0 — Environment and compute plan: passed on 2026-07-15.**

**G1 — The derivation: in progress.** Both probability limits are derived and
independently audited. The `N=30`, `K=3`, `T=10^7` numerical specification,
hard discrepancy metric, target hashes, interval method, and checkpoint
contract are frozen in `configs/g1.toml` and
`docs/predictions/GATE_G1.md`. The streamed verifier and provenance-locked
runner are implemented and committed at
`fe9e69123469496135cdffe516778a1f58206b3f`. Neither the preregistered master
stream nor the distinct benchmark stream has been drawn.

## Session objective

Completed this session: implement the frozen G1 verifier test-first, including
streamed sufficient statistics, immutable resumable checkpoints, independent
intercept-OLS inference checks, target preflight, clean-source identity, and
deterministic result publication. The pre-draw implementation boundary is now
committed; stop condition for this session is a clean ledger commit recording
that exact provenance before hosted verification.

## Current evidence

- The repository began with one runtime-only `initial` commit containing three
  OMX mission files and a configured public GitHub remote; it contained no
  research code, preregistration, result, or project ledger.
- The durable `xid` autoresearch goal and professor-critic rubric exist under
  local OMX state.
- The G0 smoke contract was written test-first. Strict configuration and
  failure-safe publication regressions cover unsafe paths, interrupted publish,
  recovery, hashes, deterministic regeneration, and the module CLI.
- The full locked parity suite is locally green. Two clean timed runs after the
  publication fix each completed in 0.04 seconds with maximum RSS of 28,180,480
  and 28,229,632 bytes; all committed artifacts were byte-identical.
- Commit `3abbad1dc3bfa6114434ce2bb5d2de0140b0dafa` passed hosted CI run
  `29416847411`: <https://github.com/ITheClixs/spurious-or-structural/actions/runs/29416847411>.
- The hostile G0 memo records the strongest unresolved objection: data capacity
  remains conditional on unmeasured G3 archive and compression distributions.
- `data/manifest.json` records zero external bytes and no datasets.
- Compute and sampling figures remain conditional on G3 archive-size and
  compression measurements.
- `docs/derivations/GATE_G1_PROBABILITY_LIMITS.md` derives uncontrolled and
  noisy-proxy-controlled population coefficients from the simultaneous reduced
  form. Independent audits agreed on the matrix orientation, confounding term,
  simultaneity term, and limiting cases.
- Deterministic formula evaluation at the frozen G1 fixture gives population
  target ranges `[0.7724315313, 0.9138344678]` and
  `[0.7719001593, 0.9201821590]`. The combined ten-decimal target hash is
  `80e6026821d67708587eb3abe606c05a7f58c5e4499430e6db72ae6d36faee1d`.
- G1 software tests use only explicit test-only seeds (`1729`, `9191`, and
  `314159`). No test or command has drawn the frozen master seed `2026071501`
  or benchmark seed `2026071599`.
- The G1 runner validates the sealed analytic hashes before RNG access, verifies
  both structural equations per shard, checkpoints only count/mean/centered
  scatter, and refuses mismatched config/source/numerical-runtime/RNG
  identities. Reloaded telemetry makes the eight-minute shard stop, RSS stops,
  eight-hour cumulative stop, and 6.4-hour forecast survive resumption.
- The result publisher recomputes inference from checkpoint moments, includes
  every coefficient's target, standard error, and 95% Bonferroni simultaneous
  interval, excludes nondeterministic timing metadata, and writes `_SUCCESS`
  last. Fault injection proves an interrupted publication is invalid and
  recoverable.
- The locked local quality gate passes Ruff, format, strict mypy, 38 tests, the
  deterministic demo, and generated-result drift checks. The G1-specific suite
  contains 25 tests; the exact `10^7` simulation is intentionally not in CI.
- The clean implementation commit is
  `fe9e69123469496135cdffe516778a1f58206b3f`; its execution-input digest is
  `8a25de8d3cd268284157df20ef3190d5519b714574e90a17c79729462e086a2b`,
  and the raw frozen-config digest is
  `2a71f58d1eec7eb39e68e7333ce5cb385a3fcdc85466ee234d334299c8886efd`.

## In flight

1. Push the implementation boundary plus this ledger record and require hosted
   CI success before stochastic research execution.
2. Run one 100,000-row timing/RSS shard using only benchmark seed `2026071599`.
3. If the benchmark satisfies A013, run the single frozen `10^7` stream; do not
   alter the fixture, target, seed, metric, or tolerance in response to output.

## Blockers

- No current blocker prevents hosted verification of the committed G1
  implementation.
- The 150 MB/symbol-day and 50 compressed bytes/bin projections are untested;
  they are explicit G3 stop/go assumptions, not evidence that the empirical
  sample fits yet.

## Data and holdout status

- External market data accessed: **no**.
- Lifetime market-data download ledger: **0 bytes**.
- Training sample: **not constructed**.
- Holdout: **not constructed and not opened**.
- Empirical specifications tried: **0**.

## Cold-resume next action

Read the four ledgers and the G1 section of `docs/GATES.md`, then state: "lock
hosted verification to implementation commit `fe9e691` before drawing either
registered RNG stream." Do not benchmark until hosted CI passes the pushed
boundary; do not draw the frozen sample until the distinct-seed benchmark
passes A013.
