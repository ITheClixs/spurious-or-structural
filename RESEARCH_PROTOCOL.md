# Research protocol

This repository is a gate-driven research project, not a feature backlog. The
protocol below is binding on the work recorded here. A failed gate is not
crossed, and an open methodological question is not silently converted into an
implementation assumption.

## Working ledgers

Four files carry the live state of the project and are read before any work
resumes:

1. `STATE.md` — current gate, evidence, blockers, and cold-resume instructions
2. `DECISIONS.md` — decisions taken and the reasoning behind them
3. `ASSUMPTIONS.md` — declared modelling conventions and their status
4. `SPECIFICATION_LOG.md` — every attempted specification, including rejected
   ones

The pass criteria for the open gate live in `docs/GATES.md`. All four ledgers
are updated, the gate red-team memo is added or revised, and a resumable state
is committed before work stops.

## Research invariants

- Derive before coding a statistical estimator.
- Record a quantitative prediction before every research run.
- Recover known truth in simulation before touching empirical data.
- Every inferential number has an interval and a named interval method.
  Deterministic algebraic quantities are labelled as such rather than given a
  fabricated interval.
- Record every attempted specification, including the failures.
- Never open the holdout before G7, and never tune after it is opened.
- Never access external market data unless the preregistration explicitly
  permits that exact discovery, calibration, training, or holdout use.
- Report a check that fails alongside the checks that pass. A registered
  prediction that misses is diagnosed and logged, never quietly retuned.
- Long jobs are chunked, checkpointed, and resumable with no more than ten
  minutes of lost work.
- Keep process resident memory below 4 GB, steady disk at or below 25 GB,
  transient disk at or below 30 GB, and lifetime downloads at or below 400 GB.

## Registered randomness

Test seeds `1729`, `9191`, and `314159` are available for deterministic
software checks at any time. The registered resource, validation, and research
seeds are consumed at most once each, only after their derivation, quantitative
prediction, configuration bytes, input hashes, random-number address map,
interval method, failure rules, and compute budget are frozen and the
corresponding commit is green in hosted continuous integration.

## Commit messages

An intent-first subject line stating what the change accomplishes, followed by
a body explaining why it was necessary. Decision trailers such as
`Constraint:`, `Rejected:`, `Confidence:`, `Scope-risk:`, `Tested:`, and
`Not-tested:` are used where they carry information the diff does not.

## Verification

`make check` runs the locked deterministic gate: linting, format verification,
strict type checking, the full test suite, the deterministic software smoke,
and committed-result drift checks. It passes before every commit. It does not
open a registered stream.

`make exhibits` regenerates every quantitative value used in the manuscript and
fails if a regenerated artifact differs from the committed one.
