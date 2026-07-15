# Research state

Last updated: 2026-07-15

## Current gate

**G0 — Environment and compute plan: passed on 2026-07-15.**

**G1 — The derivation: open, not started.** No G1 estimator or simulation code
exists. The next session begins with algebra and a quantitative pre-run
prediction, not implementation.

## Session objective

Completed: bootstrap the research repository and pass G0 without writing any
estimator or accessing any external market data.

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

## In flight

1. Read the G1 criteria and create the symbolic derivation artifact before any
   simulation code.
2. Derive `plim Lambda_hat_OLS` from the simultaneous reduced form, with matrix
   orientation and covariance assumptions explicit.
3. Derive the noisy-proxy-controlled probability limit using partialled-out
   covariance matrices and state its limiting cases.
4. Record the analytic predictions and only then write the chunked `10^7`
   simulation verifier under the eight-hour hard machine budget.

## Blockers

- No current blocker prevents starting the G1 derivation.
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

Read the four ledgers and the G1 section of `docs/GATES.md`, then state: "derive
both probability limits and their limiting-case predictions before writing the
simulation verifier." Do not implement an estimator or access external market
data during the derivation step.
