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
stream has been drawn. The distinct benchmark stream was consumed once, after
its committed and hosted-green boundary, and passed A013.

## Session objective

Completed this session: seal the hosted-green G1 implementation boundary and
run the one permitted distinct-seed resource benchmark. Stop condition for the
current branch is a committed, hosted-green benchmark evidence boundary before
the frozen master stream is accessed.

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
  `314159`). No test or command has drawn the frozen master seed `2026071501`.
  The distinct benchmark seed `2026071599` was drawn once by the preregistered
  resource command after all preconditions passed.
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
- Hosted CI run `29422105528` failed before any stochastic command because one
  Linux LAPACK entry differed between the two analytic paths by
  `2.24931185e-13`, exceeding the Mac-derived test tolerance `2e-13` while
  remaining below the production preflight bound `5e-13`. The cross-platform
  regression is being aligned to the already implemented `5e-13` bound; this
  changes no formula, target hash, seed, simulation, or gate tolerance.
- Repair commit `1adc73921da9f112f4eed56789b7a92a74b67f47` passed hosted CI
  run `29422306505`: all 38 tests, Ruff, format, strict mypy, deterministic
  demo, and result drift checks succeeded on Linux. The only annotation is a
  nonblocking GitHub Actions Node 20 deprecation warning; no research command
  ran in CI.
- Acceptance-ledger commit
  `3c56fa96f3dbc730503cb2f8bbcc586dbd9c57ad` passed hosted CI run
  `29422623200` before the benchmark draw.
- The single 100,000-row benchmark generated its shard in 0.086404708 seconds,
  completed the in-process run in 0.087642709 seconds, and peaked at
  381,517,824 bytes RSS. Straight-line extrapolation to 100 shards is 8.7643
  seconds; the preregistered 60%-throughput plus 25%-time-margin calculation is
  18.2589 seconds, against a three-hour expected and eight-hour hard budget.
  The shard checkpoint occupies 44 KiB, uses execution-input digest
  `8a25de8d3cd268284157df20ef3190d5519b714574e90a17c79729462e086a2b`,
  and has payload digest
  `df847a45cb74f65a450607070536c4b0338e881390cd7ee3898f8b241b93ee1c`.
  No `results/g1` output was published.

## In flight

1. Commit and push this benchmark evidence; require hosted parity for its exact
   head.
2. Once green, run the single frozen `10^7` master stream under `caffeinate -i`;
   do not alter the fixture, target, seed, metric, or tolerance in response to
   output.
3. Compare the sole result with the preregistered strict threshold, then record
   either a G1 pass or attempt-1 failure without a seed retry.

## Blockers

- No current blocker prevents the frozen G1 master run after this benchmark
  evidence head passes hosted parity.
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

Read the four ledgers and the G1 section of `docs/GATES.md`, then state: "A013
passed on the distinct benchmark stream; keep master seed `2026071501` sealed
until the benchmark-evidence head is hosted-green." Once that exact head is
green, run only `caffeinate -i make mc` and judge the immutable result against
the frozen strict threshold without retuning or retrying the seed.
