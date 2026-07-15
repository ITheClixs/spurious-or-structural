# Gate register

The principal's operating brief is authoritative. This file is the compact
session routing surface; it does not weaken any requirement in that brief.

## Cross-gate invariants

- Gates are sequential. A later gate stays locked until the current gate has a
  written pass review and red-team memo.
- Derivations and quantitative predictions precede research code and runs.
- No estimator touches empirical data before recovering known truth at its
  actual planned `N`, `T`, and regime contrast.
- Every inferential number has an interval and a named method.
- Every failed specification is logged.
- The holdout is opened once, in G7, with no post-open tuning.
- Three failed attempts at one gate trigger a blocker diagnosis and escalation.

## G0 — Environment and compute plan (passed 2026-07-15)

Required evidence:

1. The repository is scaffolded to the project layout.
2. `make demo` runs a genuine deterministic end-to-end skeleton in less than
   300 seconds without accessing external data or making a research claim.
3. `docs/COMPUTE_PLAN.md` shows the arithmetic for RAM below 4 GB, steady disk
   at or below 25 GB, transient disk at or below 30 GB, and lifetime downloads
   at or below 400 GB. Every phase has an expected and hard wall-clock budget.
4. Long work is chunked, checkpointed, and resumable.
5. The dependency lock is reproducible; Ruff, formatting, mypy, pytest, and the
   demo pass locally from the locked environment.
6. Hosted CI is green for the reviewed commit.
7. `docs/redteam/GATE_G0.md` attacks the result, all living ledgers are current,
   and the committed worktree is resumable.

All seven items passed for commit
`3abbad1dc3bfa6114434ce2bb5d2de0140b0dafa`; hosted CI run `29416847411`
completed successfully.

## G1 — Derivation (passed 2026-07-15)

Derive the probability limits of OLS and noisy-proxy-controlled OLS in terms of
the structural parameters. Verify with about `10^7` streamed samples. Maximum
elementwise relative discrepancy must be below `10^-3`.

The sole frozen `N=30`, `K=3`, `T=10^7` run produced maximum no-floor relative
discrepancies `5.639467093140219e-4` for uncontrolled OLS and
`5.123714186295689e-4` for noisy-proxy-controlled OLS. All 1,800 population
targets lie inside the preregistered 95% family-wise classical homoskedastic
Student-t Bonferroni intervals. Independent algebra, raw-checkpoint, artifact,
and provenance audits found no blocker or high-severity defect.

The substantive criterion passed. `results/g1`, the written pass review,
`docs/redteam/GATE_G1.md`, and all current ledgers were committed at
`44965d0370810f756ad1c5cc7938a289cb943906`; hosted CI run `29426776688`
completed successfully.

## G2 — Premise test / kill switch (open)

Faithfully implement the strongest published own-flow-plus-factor-control
opponent. In a defensibly calibrated parameter region, an off-diagonal sign
must flip or have more than 50% error, with the error greater than three named
bootstrap standard errors. Otherwise the premise is dead and the project stops
for a null write-up.

## G3 — Data reality (locked)

Inspect actual bytes and schemas for exactly the preregistered discovery files;
document timestamps, gaps, format changes, access restrictions, sizes, and
look-ahead checks. The resulting sampling plan must remain inside the compute
budget, and the real-data demo must remain below five minutes.

## G4 — Identification proof (locked)

Write the moment function and compute its true-parameter Jacobian in simulation.
Report the full singular spectrum. Pass requires
`sigma_min(J) / sigma_max(J) > 10^-8`, recovery inside a named bootstrap
interval, a mapped failure frontier, and evidence that the planned empirical
operating point lies inside it.

## G5 — Scale the open problem (locked)

Numerically demonstrate at least two distinct failure modes of the naive
estimator before abandoning it. Design the replacement from that diagnosis,
then make it pass the G4 criteria at target `N`. Publish the strongest objection
that remains unanswered.

## G6 — Train empirics (locked)

Estimate on train only. Report all diagnostics and intervals. Keep the holdout
sealed. Use the complete specification-trial count for the preregistered
multiple-testing correction.

## G7 — Falsification and economics (locked)

Derive theoretical admissibility from opened primary sources. Compare estimator
distances to the admissible set, bootstrap their differences, and calculate
round-trip manipulation profit. Open the holdout once. Evaluate liquidation
regret in known-truth Monte Carlo and genuinely external forced-liquidation
events without circular simulation.

## G8 — Write-up (locked)

Ship the honest claim supported by the gates: paper, 90-second README,
reproducible package, small committed results, and a deck of at most ten slides.
