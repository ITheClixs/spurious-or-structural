# Research state

Last updated: 2026-07-15

## Current gate

**G0 — Environment and compute plan: passed on 2026-07-15.**

**G1 — The derivation: in progress.** Both probability limits are derived and
independently audited. The `N=30`, `K=3`, `T=10^7` numerical specification,
hard discrepancy metric, target hashes, interval method, and checkpoint
contract are frozen in `configs/g1.toml` and
`docs/predictions/GATE_G1.md`. No G1 random draw or simulation implementation
exists yet.

## Session objective

Completed this session: derive both G1 probability limits and register a
quantitative validation prediction before implementation or simulation.

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
- No G1 random number has been drawn. All G1 numerical values currently in the
  repository are deterministic population calculations or design constants.

## In flight

1. Write the G1 regression tests before implementation: fixture invariants,
   analytic equivalence, transpose/missing-term mutations, centered-scatter
   merge, structural equations, checkpoint validation, and limiting cases.
2. Add only the pinned NumPy/SciPy dependencies required by the frozen verifier.
3. Implement the streamed sufficient-statistic runner and pass the small test
   suite without drawing the frozen G1 sample.
4. Commit the implementation so checkpoint metadata can bind to a clean Git
   SHA; then run the distinct-seed timing/RSS shard before the frozen run.

## Blockers

- No current blocker prevents starting the test-first G1 implementation.
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
the G1 derivation in failing tests before implementing the streamed verifier."
Do not run the frozen sample before the implementation is tested and committed.
