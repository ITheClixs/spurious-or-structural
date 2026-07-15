# Research state

Last updated: 2026-07-15

## Current gate

**G0 — Environment and compute plan: in progress.** No later gate is open.

Pass requires the scaffold, locked environment, deterministic sub-five-minute
demo, written budget arithmetic, green local parity checks, a green hosted CI
run for the reviewed commit, a hostile G0 memo, current ledgers, and a clean
resumable commit.

## Session objective

Bootstrap the research repository and reach a defensible G0 review without
writing any estimator or accessing any external market data.

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
- `data/manifest.json` records zero external bytes and no datasets.
- Compute and sampling figures remain conditional on G3 archive-size and
  compression measurements.

## In flight

1. Complete the hostile G0 memo and remove local OMX runtime state from Git
   tracking while preserving it on disk.
2. Re-run lock, lint, format, type, tests, timing, memory, and artifact hashes
   after the final documentation changes.
3. Commit with a Lore message, push, and inspect hosted CI.
4. If CI is green, append the final G0 pass review and make the state-only close
   commit; otherwise keep G0 open and diagnose the remote failure.

## Blockers

- Full G0 pass cannot be claimed until hosted CI is green for the reviewed
  commit. `gh auth status` currently reports an invalid token, although the
  configured Git remote may use a separate credential helper. Push will test
  that path; authentication failure leaves G0 open.
- The 150 MB/symbol-day and 50 compressed bytes/bin projections are untested;
  they are explicit G3 stop/go assumptions, not current blockers for the G0
  engineering scaffold.

## Data and holdout status

- External market data accessed: **no**.
- Lifetime market-data download ledger: **0 bytes**.
- Training sample: **not constructed**.
- Holdout: **not constructed and not opened**.
- Empirical specifications tried: **0**.

## Cold-resume next action

Read the four ledgers and `docs/GATES.md`, then run `git status` and continue the
G0 verification checklist. Do not start G1 derivations until G0 has a written
pass and hosted CI evidence.
