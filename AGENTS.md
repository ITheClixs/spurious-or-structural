# xid research operating contract

This repository is a gate-driven research project, not a feature backlog. The
principal's operating brief is authoritative. Do not cross a failed gate and do
not turn an open methodological question into an implementation assumption.

At the start of every session, read these files in order:

1. `STATE.md`
2. `DECISIONS.md`
3. `ASSUMPTIONS.md`
4. `SPECIFICATION_LOG.md`
5. The pass criteria for the open gate in `docs/GATES.md`

Then state one sentence describing the session objective. At session end,
update all four ledgers, add or update the gate red-team memo, and commit a
resumable state.

Research invariants:

- Derive before coding statistical estimators.
- Record a quantitative prediction before every research run.
- Recover known truth in simulation before touching empirical data.
- Every inferential number has an interval and a named interval method.
- Record every attempted specification, including failures.
- Never open the holdout before G7, and never tune after it is opened.
- Never access external market data unless the preregistration explicitly
  permits that exact discovery, calibration, training, or holdout use.
- Long jobs are chunked, checkpointed, and resumable with no more than ten
  minutes of lost work.
- Keep process RSS below 4 GB, steady disk at or below 25 GB, transient disk at
  or below 30 GB, and lifetime downloads at or below 400 GB.

Commit messages follow the Lore protocol documented in the principal's brief:
an intent-first subject plus decision trailers such as `Constraint:`,
`Rejected:`, `Confidence:`, `Scope-risk:`, `Directive:`, `Tested:`, and
`Not-tested:` when they carry useful context.
