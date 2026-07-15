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

## D0009 — Pass G0 only on exact-SHA hosted reproduction

- **Date:** 2026-07-15
- **Diagnosis:** Local checks, timing, hashes, and hostile review all passed, but
  the gate contract separately required clean hosted reproduction.
- **Decision:** Pass G0 after CI run `29416847411` completed successfully for
  candidate SHA `3abbad1dc3bfa6114434ce2bb5d2de0140b0dafa`. Open G1 for
  derivation only.
- **Rejected:** Begin the G1 simulation while CI was pending. That would make
  gate order depend on confidence rather than evidence.
- **Residual risk:** Archive size, compression, and long-run thermal assumptions
  remain untested and are explicit G3/phase stop conditions, not silent facts.
- **Reopen if:** The G0 artifacts or lock are later shown not to reproduce from
  this commit.

## D0010 — State the covariance restriction instead of hiding it

- **Date:** 2026-07-15
- **Diagnosis:** The requested G1 probability limits cannot be expressed using
  only `Sigma_f`, `Sigma_u`, and `Sigma_v` if contemporaneous shock
  cross-covariances are unrestricted. Silent zeroing would make the derivation
  look more general than it is.
- **Decision:** Derive G1 under explicit mutual zero-covariance assumptions for
  `f`, `u`, `v`, and proxy noise. Independence is imposed only in the Gaussian
  validation fixture. State that empirical use requires testing or extending
  this restriction.
- **Rejected:** Add unnamed cross-covariances to the formulas. They are not among
  the brief's primitive parameters and would change the stated problem.
- **Reopen if:** A later structural specification explicitly parameterizes the
  cross-covariances.

## D0011 — Validate at the declared matrix dimension

- **Date:** 2026-07-15
- **Diagnosis:** A scalar or four-asset check can catch algebraic mistakes but
  does not expose transpose errors, matrix proxy reliability, or the flow
  conditioning expected near the planned `N=30`, `K=3` operating point.
- **Decision:** Freeze one `N=30`, `K=3`, `T=10^7` Gaussian fixture with 100
  independently keyed shards. Every analytic target stays above 0.7719 in
  absolute value, while omitted confounding, omitted simultaneity, transpose,
  and scalar-reliability mutations all breach the `10^-3` gate tolerance.
- **Rejected:** Use a hand-computable bivariate fixture as the only G1 run. It
  would make the gate easier without validating the matrix operations that
  downstream work depends on.
- **Reopen if:** The pre-run timing shard violates the 1.5 GB phase RSS or
  eight-hour wall-clock contract; any redesign is a new logged specification.

## D0012 — Use sufficient statistics, not retained simulated rows

- **Date:** 2026-07-15
- **Diagnosis:** Ten million rows are needed only to estimate second moments;
  retaining them adds disk and memory pressure without adding information to
  the G1 regression.
- **Decision:** Checkpoint immutable shard count/mean/centered-scatter records
  and merge them in fixed order with the Chan--Golub--LeVeque identity. Bind
  each shard to config hash, code SHA, NumPy version, RNG key, and payload hash.
- **Rejected:** Store generated observations or sum separately demeaned shard
  scatters. The former wastes resources; the latter drops between-shard
  variation and changes the estimator.
- **Reopen if:** A later gate requires path-dependent simulated outputs rather
  than second moments.

## D0013 — Name the interval justified by the frozen DGP

- **Date:** 2026-07-15
- **Diagnosis:** G1 needs intervals, but importing later empirical HAC or
  bootstrap machinery would obscure that this fixture is IID and jointly
  Gaussian.
- **Decision:** Report classical homoskedastic Student-t intervals with a 95%
  Bonferroni family-wise correction across both 30-by-30 matrices. Use the full
  `[q, fhat]` design covariance for proxy standard errors. Pin NumPy and SciPy
  only when the test-first implementation begins.
- **Rejected:** Reuse unadjusted marginal intervals or claim G1's Gaussian
  intervals apply to dependent market data.
- **Reopen if:** The simulation DGP is amended away from IID joint Gaussianity
  before any draw; that amendment is a new specification.

## D0014 — Keep software tests outside both registered random streams

- **Date:** 2026-07-15
- **Diagnosis:** Prefixes of the master seed used in unit tests would constitute
  an unreported look at the frozen experiment even if no gate statistic were
  printed. CI repetition would also repeatedly consume the registered stream.
- **Decision:** Use only explicit test-only seeds (`1729`, `9191`, `314159`) in
  software tests. Reserve `2026071599` for the one-shard resource benchmark and
  `2026071501` for S0001. Validate all sealed target hashes before any runner can
  reach RNG generation. Pin NumPy 2.5.1 and SciPy 1.18.0 in the lockfile because
  their RNG and inference behavior is part of the frozen implementation.
- **Rejected:** Treat small frozen-seed prefixes as harmless smoke tests. They
  leak stochastic evidence before the registered run and make attempt counting
  ambiguous.
- **Reopen if:** Never; a new seed is a newly logged simulation specification,
  not an amendment to S0001.

## D0015 — Bind resumability to source content, with commit provenance separate

- **Date:** 2026-07-15
- **Diagnosis:** A caller-supplied SHA or `HEAD` from a nested path can launder
  dirty execution inputs. Conversely, binding only to the whole commit makes a
  documentation-only commit invalidate otherwise identical checkpoints.
- **Decision:** Require the exact Git top level and a clean path set covering
  `src/xid`, `configs/g1.toml`, `pyproject.toml`, `uv.lock`, and
  `.python-version`. Record the clean
  commit for provenance, but bind checkpoints to a SHA256 of the tracked modes,
  blob IDs, and paths for those execution inputs.
  Also bind each shard to a numerical-runtime fingerprint covering Python,
  NumPy build metadata, machine, OS release, and the active BLAS/thread-control
  environment so checkpoints from different numerical runtimes cannot be
  silently merged. Production commands require all supported thread controls
  to equal one before numerical work. The CLI computes raw config and source
  hashes internally and exposes no override flags.
- **Rejected:** Trust a user-provided `code_sha`, or bind checkpoints only to
  `HEAD`. The former is forgeable; the latter confuses unrelated prose changes
  with changes to the generated sample.
- **Reopen if:** The execution surface expands beyond the hashed path set.

## D0016 — Commit statistical evidence, not machine-timing accidents

- **Date:** 2026-07-15
- **Diagnosis:** Elapsed time, peak RSS, and new-versus-reused shard counts vary
  across valid resumptions. Including them in result JSON would violate the
  byte-reproducibility contract even when every statistical number agrees.
- **Decision:** Keep resource measurements in the public ledgers, while the
  committed G1 artifact contains only deterministic provenance, targets,
  coefficients, standard errors, simultaneous intervals, diagnostics, and the
  strict gate decision. Recompute estimates from checkpoint moments before
  publishing, refuse replacement of valid differing evidence, and write a
  hash-bearing `_SUCCESS` marker last.
- **Rejected:** Serialize the runner object wholesale. It mixes scientific
  evidence with nondeterministic execution telemetry.
- **Reopen if:** A deterministic benchmark artifact is defined separately from
  the statistical result.

## D0017 — Make phase-budget failures survive a restart

- **Date:** 2026-07-15
- **Diagnosis:** The first runner retained elapsed/RSS telemetry in checkpoint
  JSON but returned only moments on reuse. Restarting therefore reset the
  eight-hour clock and could reuse a shard that had already breached the
  eight-minute design stop.
- **Decision:** Validate and reload shard telemetry, reject over-limit RSS and
  eight-minute shard records on reuse, check new-shard duration before atomic
  publication, and accumulate all generated-shard durations for the hard stop
  and 6.4-hour completion forecast. Preserve current-invocation wall time as a
  second, stricter stop.
- **Rejected:** Treat each resumed process as a fresh phase budget. That turns
  checkpointing into a way to bypass the precommitted compute design.
- **Reopen if:** Phase timing moves to a stronger append-only run ledger that
  also accounts for prior-process startup overhead.

## D0018 — Seal one clean implementation boundary before benchmark evidence

- **Date:** 2026-07-15
- **Diagnosis:** Checkpoint provenance is meaningful only if the candidate code
  is already immutable when the first registered stream is accessed.
- **Decision:** Seal commit
  `fe9e69123469496135cdffe516778a1f58206b3f` after the hostile pre-draw review
  passed with 38 tests. Its execution-input SHA256 is
  `8a25de8d3cd268284157df20ef3190d5519b714574e90a17c79729462e086a2b`;
  the raw config SHA256 is
  `2a71f58d1eec7eb39e68e7333ce5cb385a3fcdc85466ee234d334299c8886efd`.
  Require hosted CI before the distinct benchmark draw.
- **Rejected:** Benchmark from an uncommitted or merely locally reviewed tree.
  That would leave no independently reproducible implementation boundary.
- **Reopen if:** Hosted CI fails this boundary; repair code only under a new
  logged implementation commit before any registered draw.

## D0019 — Bound algebraic equivalence above observed LAPACK rounding

- **Date:** 2026-07-15
- **Diagnosis:** Hosted run `29422105528` found a single uncontrolled-target
  entry differing by `2.24931185e-13` between the primitive-bias and full
  reduced-form paths. The local Accelerate build differed by at most
  `1.72e-13`; both are rounding-level deviations from differently ordered dense
  solves, not target or formula disagreements.
- **Decision:** Use the production preflight's existing absolute equivalence
  bound `5e-13` in the cross-platform regression test. Keep the ten-decimal
  target hashes and `10^-3` simulation gate unchanged.
- **Rejected:** Change matrix formulas to force operation ordering, or weaken
  the scientific gate. The former would destroy an independent-path check; the
  latter is unrelated by roughly nine orders of magnitude.
- **Reopen if:** Any platform exceeds `5e-13` or changes a sealed target hash.

## D0020 — Accept the repaired boundary only after hosted parity

- **Date:** 2026-07-15
- **Diagnosis:** The first hosted boundary failed a rounding-level assertion;
  local green evidence was therefore insufficient for stochastic execution.
- **Decision:** Accept repair commit
  `1adc73921da9f112f4eed56789b7a92a74b67f47` after hosted run `29422306505`
  completed successfully with all 38 tests and parity checks. Permit only the
  distinct benchmark seed after the ledger-only acceptance head also passes.
- **Rejected:** Run the benchmark immediately after local repair verification.
  That would repeat the exact evidence-ordering mistake caught by the first
  hosted run.
- **Residual risk:** GitHub reports a Node 20 action-runtime deprecation warning;
  the runner forced Node 24 and the workflow passed, so this is maintenance
  debt rather than a G1 validity failure.
- **Reopen if:** Hosted results are invalidated or the accepted execution-input
  digest changes before the benchmark.
