# Decision ledger

Judgement calls are append-only. Each entry records the diagnosis that preceded
the choice, alternatives, and the evidence that would reopen it.

## D0001 — Keep the G0 demo inference-free

- **Date:** 2026-07-15
- **Diagnosis:** The repository needs a real end-to-end smoke path, but G1 owns
  the derivation and simulation verification of the structural system. A G0
  OLS/bootstrap figure would implement statistical work before its algebra and
  prediction exist.
- **Decision:** G0 streams deterministic synthetic records and reports only
  configuration, row count, and SHA256. It explicitly reports no research
  claim and no inferential interval.
- **Rejected:** Simulate the simultaneous system and estimate OLS in G0. This
  would make a more impressive figure but violate gate order and bias later
  derivation toward an implementation already written.
- **Reopen if:** G1 has passed and the demo is deliberately upgraded under a
  new prediction and specification-log entry.

## D0002 — Minimize the G0 runtime dependency surface

- **Date:** 2026-07-15
- **Diagnosis:** Real schemas are unknown and no numerical estimator is allowed
  yet. Installing the full future Polars/SciPy/Numba stack would add platform and
  CI failure modes without exercising those packages.
- **Decision:** G0 runtime uses the Python standard library. Hatchling is pinned
  for builds; pytest, Ruff, and mypy are pinned as development dependencies.
  Scientific dependencies are added only at the gate that proves a need.
- **Rejected:** Preinstall the entire requested scientific toolchain. It would
  make the lock look complete while hiding that none of it is validated or used.
- **Reopen if:** A passed gate introduces code that requires a named package.

## D0003 — Resolve the G2-before-G3 calibration conflict without early tape access

- **Date:** 2026-07-15
- **Diagnosis:** G2 requires realistic calibration, while G3 is the explicit
  byte-level data-reality gate. Quietly downloading market tape for G2 would
  cross the preregistered discovery boundary and muddle gate chronology.
- **Decision:** G2 first uses numerical calibration envelopes from opened,
  verified primary papers or public aggregate sources. If they cannot support a
  defensible calibration, G2 remains failed rather than borrowing G3 data.
- **Rejected:** Pull a convenient market sample during G2 and document it later.
  That creates an unlogged data-snooping channel and turns G3 into retrospective
  paperwork.
- **Reopen if:** The operating brief is amended explicitly or a blocker memo
  demonstrates that no defensible published calibration exists.

## D0004 — Use a conditional capacity envelope with hard byte guards

- **Date:** 2026-07-15
- **Diagnosis:** The machine ceilings are absolute, but real archive sizes and
  retained Parquet compression are unknown until G3.
- **Decision:** Plan against 150 MB per symbol-day and 50 bytes per retained
  250 ms symbol-bin, with a 348.6 GB lifetime projection, a 360 GB downloader
  stop, a 25 GB steady allocation, and a 29 GB transient guard. G3 must measure
  and either validate or redesign before bulk acquisition.
- **Rejected:** Call the budgets proven from vendor schema descriptions or mean
  file sizes. Neither is byte-level evidence and both ignore tails and retries.
- **Reopen if:** G3 measurements violate either planning envelope.

## D0005 — Treat hosted CI as part of G0, not as a YAML artifact

- **Date:** 2026-07-15
- **Diagnosis:** A workflow file and a local green run do not prove that a clean
  remote runner can reproduce the result.
- **Decision:** G0 remains in progress until the reviewed commit is pushed and
  its GitHub Actions job is green. Local parity is necessary but insufficient.
- **Rejected:** Mark G0 passed after `make check` locally. This would weaken the
  brief's explicit `CI green` criterion.
- **Reopen if:** The remote runner is unavailable for reasons documented in a
  blocker memo; even then the gate is reported as unpassed, not waived.

## D0006 — Publish the demo as a validity-marked artifact set

- **Date:** 2026-07-15
- **Diagnosis:** Individually atomic data and summary replacements can still
  leave a mixed pair after a crash, and fixed temporary names race concurrent
  invocations.
- **Decision:** Stage under a unique same-filesystem directory, serialize the
  publish step with `flock`, remove prior validity before replacement, and write
  a hash-bearing `_SUCCESS` marker last. Consumers reject any set without a
  matching marker. Fault injection must prove invalidation and recovery.
- **Rejected:** Keep the simpler pair of `Path.replace` calls. It protects each
  file, not the artifact set the reader actually consumes.
- **Reopen if:** A later artifact store supplies a stronger transactional
  primitive with equivalent interruption tests.

## D0007 — Keep OMX goal state local, research state public

- **Date:** 2026-07-15
- **Diagnosis:** The runtime-only initial commit tracked three `.omx` mission
  files. Hooks may mutate them, creating dirty worktrees and exposing workflow
  mechanics as if they were research evidence.
- **Decision:** Remove `.omx` from the Git index while preserving it locally and
  ignoring future runtime mutations. `STATE.md` and the append-only research
  ledgers are the public resumption surface.
- **Rejected:** Continue tracking the runtime ledger. It duplicates state
  ownership and can change for reasons unrelated to the research result.
- **Reopen if:** A future reproducibility requirement names a stable exported
  goal artifact rather than live runtime state.

## D0008 — Cap dense linear-algebra copies explicitly

- **Date:** 2026-07-15
- **Diagnosis:** The first RAM table ambiguously read as a base weight matrix
  plus three additional factorization copies, which would exceed the project's
  own 3.7 GB abort guard.
- **Decision:** Permit three weight/factorization matrices total (base plus two
  copies), two 64 MB columnar buffers, and 302 MB general array scratch. With a
  separate 1.5 GB overhead allowance, the projected dense phase is 3.345 GB.
- **Rejected:** Preserve four dense copies and rely on the nominal 4 GB ceiling.
  That erases the operating margin and invites allocator-driven failure.
- **Reopen if:** Measured G4/G5 code demonstrates a smaller structured
  representation or proves the current copy cap infeasible.
