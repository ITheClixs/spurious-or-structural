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

## D0021 — Accept the G1 compute design from the sealed resource shard

- **Date:** 2026-07-15
- **Diagnosis:** G1 could not consume its frozen master stream until the actual
  M4 Air resource profile was shown to fit the preregistered memory, shard, and
  phase budgets.
- **Decision:** Accept A013 after acceptance-ledger commit
  `3c56fa96f3dbc730503cb2f8bbcc586dbd9c57ad` passed hosted run
  `29422623200` and benchmark seed `2026071599` generated its sole 100,000-row
  shard. Generation took 0.086404708 seconds, the in-process run took
  0.087642709 seconds, and peak RSS was 381,517,824 bytes. Multiplying total
  elapsed by 100 gives 8.7643 seconds; dividing throughput by 60% and adding the
  declared 25% time margin gives 18.2589 seconds, inside the three-hour expected
  and eight-hour hard budgets. The checkpoint payload SHA256 is
  `df847a45cb74f65a450607070536c4b0338e881390cd7ee3898f8b241b93ee1c`;
  no coefficient result was published. Permit the master draw only after this
  evidence is committed and hosted-green.
- **Rejected:** Run the master stream before sealing the resource result, or
  weaken the memory/runtime design because the benchmark was unexpectedly
  cheap. Both would discard a preregistered gate boundary without evidence.
- **Residual risk:** A single short shard does not measure sustained thermal
  throttling. The 18.2589-second derated projection leaves over two orders of
  magnitude of slack to the expected budget; the frozen run remains the direct
  check, while A010 stays untested for genuinely long later phases.
- **Reopen if:** The frozen run breaches 1.5 GB, a shard exceeds eight minutes,
  cumulative time exceeds eight hours, or the execution-input digest changes.

## D0022 — Treat the sole frozen result as a substantive G1 pass

- **Date:** 2026-07-15
- **Diagnosis:** The only admissible decision is the preregistered strict
  comparison of both 30-by-30 finite-sample regression matrices with their
  derived population targets; interval coverage is secondary evidence and
  cannot substitute for that test.
- **Decision:** Record a substantive G1 pass. At `T=10,000,000`, uncontrolled
  OLS had maximum elementwise no-floor relative discrepancy
  `5.639467093140219e-4`, and noisy-proxy-controlled OLS had
  `5.123714186295689e-4`; the gate statistic is their maximum and is strictly
  below `10^-3`. All 1,800 targets lie inside 95% family-wise classical
  homoskedastic Student-t Bonferroni intervals. The sole master seed was not
  changed or retried. Preserve `results/g1` as the immutable evidence and keep
  G2 locked until the closeout commit passes hosted CI.
- **Rejected:** Recast G1 as evidence that cross-impact is identified or that
  the noisy control solves confounding. G1 validates only the derived
  pseudo-true regression coefficients under the frozen conditional DGP.
- **Evidence hashes:** summary
  `b590b8ba079c70917e3e768ff1079051f2b8a6c8007336367aa2d299ec3c5d54`;
  estimates `f5129b0fc7695e7db13074dad64ac6123263992ccca920f579d85205bba8f06f`;
  success marker
  `6d2d75323f0a30705b852be85354ec2143fa9876dab92ead60a495bf81bd52cf`.
- **Residual risk:** Every target is large and positive, and the simulation is
  IID Gaussian with mutually uncorrelated shocks. It does not test the
  near-zero, sign-sensitive off-diagonals or empirical dependence central to
  the economic dispute; G2 must confront those rather than inherit this pass.
- **Reopen if:** An independent recomputation disagrees, the artifact hashes
  fail, hosted parity fails for the closeout, or the recorded run provenance
  shows any alternate seed or specification.

## D0023 — Close G1 only after the evidence commit reproduces in CI

- **Date:** 2026-07-15
- **Diagnosis:** A local substantive pass was not yet a durable gate transition;
  the generated artifacts, hostile review, and ledgers had to survive the same
  public software checks as the implementation that produced them.
- **Decision:** Close G1 after evidence commit
  `44965d0370810f756ad1c5cc7938a289cb943906` passed hosted CI run
  `29426776688`. Open G2 for literature, calibration, derivation, and prediction
  work only; no empirical tape is permitted under D0003.
- **Rejected:** Start G2 while the closeout evidence was merely local. That
  would cross a gate whose durable artifacts had not yet passed public checks.
- **Residual risk:** CI validates software and committed-byte stability, not the
  economic premise. G2 remains a genuine kill switch.
- **Reopen if:** The hosted run is invalidated or a hash/provenance audit finds
  that the committed evidence differs from the reviewed frozen result.

## D0024 — Use one primary one-minute calibration, not a cross-study tuple

- **Date:** 2026-07-15
- **Diagnosis:** The first G2 design combined one-minute equity OFI spectra, a
  five-minute trade-sign propagator, one-second E-mini feedback, and an
  unsourced temporal process. Standardizing each number did not make the tuple
  jointly observed or frequency invariant.
- **Decision:** Match only Capponi--Cont's dimensionless one-minute leading
  flow/return shares and factor-score alignment in the confirmatory observable
  law. Set `B = 0` so the gate isolates confounding. Treat Benzaquen's
  absolute `0.29` diagonal and the cross/own interval as structural
  sensitivities rather than one-minute coefficients,
  Hasbrouck--Seppi as a 15-minute historical comparator, Takahashi as a
  nonconfirmatory feedback reference, and AR(1) `0.60` as a dependence stress.
- **Rejected:** Derive an aggregation bridge from incompatible summaries by
  assuming their standardized coefficients are invariant. The necessary
  shared-filter and variable-equivalence assumptions are not in the sources.
- **Residual risk:** The positive result remains conditional on a source-matched
  observable law and source-informed structural sensitivity; it is not an
  empirical structural calibration.
- **Reopen if:** G3 or a newly opened primary source supplies same-variable,
  same-frequency structural quantities under a defensible sampling design.

## D0025 — Remove asset ordering and make confounding the pass requirement

- **Date:** 2026-07-15
- **Diagnosis:** A001's Fourier PC2/PC3 geometry made the chosen off-diagonal
  depend on an unsourced ordering. Its confirmatory response mapping re-added
  the factor direction and was algebraically uncontrolled OLS, while every cell
  also contained positive feedback.
- **Decision:** Use the permutation-invariant one-spike covariance with
  isotropic residual eigenvalues, homogeneous `Lambda`, and `B = 0`. Every
  population off-diagonal is identical. Give the opponent oracle `q`, the
  correct scalar factor direction, and an independent proxy with 95%
  reliability. Compare the direct coefficient on `q` with `Lambda`.
- **Rejected:** Keep the old response-equivalent factor map and call it the
  strongest factor-controlled estimate. That changes the opponent's estimand
  and cannot isolate confounding.
- **Residual risk:** Isotropic residuals are a transparent maximum-entropy
  convention, not a claim about real residual covariance. Proxy reliability is
  deliberately favorable but not empirically identified.
- **Reopen if:** A source identifies the lower spectrum/loading orientation or
  an empirical proxy-reliability bound without opening the holdout.

## D0026 — Give the opponent the true symmetry and keep CCZ targets fair

- **Date:** 2026-07-15
- **Diagnosis:** A 30-dimensional penalized fit could fail from covariance
  estimation rather than the noisy-control moment. Conversely, factor-residual
  coefficients cannot fairly be compared with directions their feature map
  projects out.
- **Decision:** Require two smooth confirmatory candidates: a full-flow positive
  condition-ridge projection and a pooled three-slope OLS projection told the
  true homogeneous structure. Both receive oracle flow and the same proxy and
  both must pass every structural grid point. CCZ protocol reconstructions are
  secondary; purged operators target `Lambda P_perp`, while full response maps
  are separately labeled descriptive results.
- **Rejected:** Use a truth-assisted selector over LASSO paths or accuse an
  own/residual-only model of failing to recover unavailable directions. Both
  would make the positive result easier through an unfair comparison.
- **Residual risk:** The confirmatory candidates are projection diagnostics,
  not identified structural estimators; that limitation is the point of G2.
- **Reopen if:** A smoother and strictly stronger observable-factor baseline is
  derived before any registered draw and passes the same estimand audit.

## D0027 — Test the margin beyond materiality and license the exact procedure

- **Date:** 2026-07-15
- **Diagnosis:** A001's exactly-50% planted alternative could not attain 80%
  power under a strict `> 50%` rule. Separately requiring 50% error and three
  SE from zero does not show that the materiality margin is statistically
  resolved.
- **Decision:** Require
  `abs(error) - 0.5 * abs(truth) > 3 * bootstrap_se`. Use 499 whole-date
  multinomial-weight bootstrap replicates. Before research, 100 panels must put
  the one-sided 95% Clopper--Pearson upper bound at or below 5% for a
  superpanel indicator that any candidate/grid component passes at its own
  50%-materiality boundary. A power superpanel at the actual 95%-reliability
  alternative must put the one-sided 95% Wilson lower bound at or above 80% for
  the indicator that every component passes. Reliability one remains a
  recovery diagnostic, not a size design; marginal component intervals are
  descriptive only. No validation-seed retry is allowed.
- **Rejected:** Preserve the literal weaker conjunction or validate a different
  analytic/low-dimensional procedure. The license must cover the final gate
  algorithm.
- **Residual risk:** A negative 95%-reliability result cannot kill the market
  premise because weaker proxies are source compatible. Only a sharp
  source-compatible bias upper bound can support that null.
- **Reopen if:** The finite-sample license fails before research; any redesign is
  a new logged specification, not a seed retry.

## D0028 — Bound G2 by small sufficient statistics and measured fit counts

- **Date:** 2026-07-15
- **Diagnosis:** The first checkpoint promise could not reconstruct paper-block
  preprocessing and understated millions of CV-selected LASSO refits. A naive
  date-by-cell 360-dimensional scatter design could also exceed the checkpoint
  allocation.
- **Decision:** Confirmatory work stores 2,016 float64 sufficient-statistic
  entries per date (`16,128` bytes), processes grid points/panels sequentially,
  and vectorizes bootstrap aggregation. Paper reconstructions stream one raw
  date at a time and retain date summaries. A distinct benchmark must measure
  a full panel, a 25-bootstrap batch, and one complete reconstruction date,
  then extrapolate the exact `2,844,300` validation bootstrap aggregation /
  `3,992,000` validation candidate-fit counts plus the fully enumerated
  secondary workload before the validation seed is
  available. Phase hard stops total 21 hours, below the G0 32-hour G2 envelope.
- **Rejected:** Build block-level high-dimensional scatter lakes or accept a
  wall-time assertion without an executable fit count.
- **Reopen if:** The sealed benchmark projects beyond any subphase hard budget,
  a task/batch exceeds eight minutes, RSS exceeds 3.5 GB, or checkpoint storage
  exceeds 2 GB.

## D0029 — Treat the second hostile audit as a failed boundary, then repair it

- **Date:** 2026-07-15
- **Diagnosis:** Independent reviewers reproduced S0003's population economics
  but rejected execution. The raw float JSON was immutable but not
  independently byte-derivable; the size experiment used the distant `R = 1`
  recovery control instead of the 50%-materiality boundary; A001 was not
  mechanically denied execution; and source/gate prose still leaked S0002 or
  premise-killing language. A wider-box feasibility line also retained stale
  values from the rejected interval.
- **Decision:** Keep the full-precision raw SHA only as a byte-integrity seal and
  add an independent 12-decimal semantic seal. Add design/config/target schema
  identity and hard rejection conditions. Hash-seal candidate-specific
  materiality-boundary reliabilities, validate family size with a superpanel
  union indicator there, validate joint power with a superpanel intersection
  indicator at `R = 0.95`, retain `R = 1` only as a recovery diagnostic, and
  require the pooled homogeneous veto. Correct the feasibility evidence and
  narrow every positive/null statement to the actual conditional claim.
- **Rejected:** Call the recovery control a size test, or paper over ULP-level
  regeneration differences with a raw-file hash. Neither would validate the
  actual gate procedure.
- **Residual risk:** The Python semantic generator and hard-fail tests do not
  yet exist; the clean documentation boundary must pass hosted CI before that
  implementation starts, and no RNG is authorized until those tests pass.
- **Reopen if:** A fresh audit cannot reproduce the semantic digest, the
  candidate-specific critical reliabilities, or the intersection-union
  acceptance logic.

## D0030 — Make every stochastic and published-opponent branch executable

- **Date:** 2026-07-15
- **Diagnosis:** The inference reviewer found that named seeds were not an RNG
  schedule, “six reconstructions” was not an estimator table, and the claimed
  exact workload omitted 45.6 million small LASSO solutions. Bootstrap interval
  names also omitted `ddof`, critical values, and quantile algorithms. Those
  gaps permit implementations with materially different power and runtime.
- **Decision:** Freeze the full `SeedSequence` entropy vector, zero-based
  namespace tables, shapes, AR recursion, CRN transforms, and shared bootstrap
  weights. Define all six CCZ fits row by row, including penalization,
  fold-local PCA/scaling, lambda path, coordinate/warm-start rules, OOS SST,
  and cached-date bootstrap target. Freeze the interval formulas and one-sided
  family thresholds. Make both frontiers, recovery, IID, measured-OFI, and
  paper branches mandatory and expose their exact fit/path counts to the
  resource benchmark.
- **Rejected:** Treat paper reconstruction as optional because it is secondary,
  or benchmark only confirmatory ridge. The gate explicitly requires a
  faithful strongest published opponent and the laptop budget applies to the
  full promised workload.
- **Residual risk:** The 45,586,800 LASSO solutions may breach the four-hour
  research hard stop despite their tiny dimensions and warm starts. One full
  date is therefore a mandatory pre-validation benchmark; a breach fails the
  design rather than authorizing fewer dates or lambdas.
- **Reopen if:** The fresh audit finds any unkeyed random draw, implementation
  choice absent from the six-row table, optional workload branch, or count that
  the benchmark cannot reconstruct.

## D0031 — Reject oracle dominance and bind the observable opponent

- **Date:** 2026-07-15
- **Diagnosis:** The fresh math audit reproduced S0003, but the professor audit
  identified a logical gap: oracle-flow coefficient failure does not imply
  measured or published-algorithm failure because measurement attenuation,
  regularization, and factor purging can cancel confounding. S0003 could pass
  without testing H1's observable opponent.
- **Decision:** Supersede S0003 before code or RNG with S0004. Make the
  integrated-top-ten-OFI plus 95%-reliable proxy condition ridge binding at all
  17 cells. Retain oracle condition ridge and pooled homogeneous OLS as binding
  no-strawman checks. Make the CCZ `CI_I` reconstruction a separate published
  direct-flow veto at the primary point and upper endpoint; require an
  actual-`N`, actual-`T` no-confounding recovery panel first.
- **Rejected:** Infer observable failure from a Blackwell-style “more
  information” intuition. The estimators and estimands differ, so no
  coefficient-error ordering follows.
- **Residual risk:** The `CI_I` reconstruction fills numerical choices omitted
  by the paper and cannot receive a 100-panel exact power study within the
  laptop budget. Its sole predeclared result therefore has a named date
  bootstrap and recovery check but is not included in the smooth-family Monte
  Carlo power claim.
- **Reopen if:** A primary-source author implementation or a stronger exact
  observable factor-control baseline becomes available before the research
  seed is consumed.

## D0032 — License a finite null grid and exact execution rates, not a theorem

- **Date:** 2026-07-15
- **Diagnosis:** Population monotonicity in proxy reliability does not prove
  that finite-sample passage probability is maximal at `Rcrit` once estimated
  PCs, sample ridge branches, and bootstrap SEs vary. Separately, bootstrap
  entropy collided across parent scenarios/date counts; pooled centering,
  fold-local LASSO paths, block-varying CC loadings, and cold/warm throughput
  remained underdefined.
- **Decision:** Evaluate a nine-node proxy-noise-amplitude grid between `R=1`
  and every candidate/cell materiality boundary and call it exactly what it is:
  a 459-event null-grid calibration, not continuum-uniform size control. Give
  RNG key schema 2 dedicated parent phase/scenario/date-count slots. Freeze one
  global weighted pooled intercept, common penalty-ratio-index CV, block-formed
  CC maps plus mean `P_perp`, and fourteen separately timed cold/warm kernels.
  The full workload is 26,405,400 smooth validation fits, 15,195,600 `CI_I`
  recovery LASSO solutions, and 45,586,800 research LASSO solutions. Use the
  complete one-/12-/three-/16-hour expected-cap schedule; the benchmark vetoes
  execution if measured rates do not fit. The two-/24-/six-/32-hour hard limits
  remain runtime stops rather than preflight slack.
- **Rejected:** Call a boundary experiment “size,” silently reuse one entropy
  key for differently shaped vectors, or extrapolate a full phase from one
  convenient kernel. Each would manufacture confidence or compute feasibility.
- **Residual risk:** Nine points do not certify the continuum between them.
  The frozen maxima are `0.015038828627620739` in proxy-noise amplitude and
  `0.003307437435413063` in adjacent reliability. Those and every cellwise gap
  must ship with results, and a continuous size claim remains prohibited
  without a certified samplewise supremum. Invalid numerical outcomes fail the
  license; they may not masquerade as null nonpasses.
- **Reopen if:** The deterministic benchmark fails, in which case S0004 fails
  pre-validation; five nodes or fewer paper fits require a new logged design,
  not an in-place budget edit.

## D0033 — Require the published LASSO to recover nonzero cross-impact

- **Date:** 2026-07-15
- **Diagnosis:** The first `CI_I` recovery fixture set every structural
  off-diagonal to zero. A LASSO that always erased small cross coefficients
  could therefore pass recovery and later appear more than 50% wrong against a
  nonzero truth for a reason unrelated to confounding.
- **Decision:** Keep the actual `N=30`, 252-date, collinear flow law, noisy
  ten-level measurement, upper-endpoint modal return-noise distribution and
  deterministic maps, remove only price confounding with `Gamma = 0`, and set the
  homogeneous truth to diagonal `0.29` and off-diagonal `0.0046`. All 30
  diagonal targets and focal `(0,1)` cross target must lie inside their frozen
  Bonferroni date-bootstrap-normal intervals; all 31 point errors must be
  strictly below 50%, and the focal material-bias declaration must be false.
- **Rejected:** Validate only a zero cross coefficient, exact measured flow,
  isotropic return noise, or infer recoverability from the much larger diagonal.
  None tests whether the published procedure can preserve the same small object
  under the same non-confounding inputs later used for the accusation.
- **Residual risk:** One full-size recovery panel is not a Monte Carlo size or
  power license for `CI_I`; a 100-panel exact study would require roughly 1.52
  billion small LASSO solutions and violates the laptop budget. The fully
  licensed observable hybrid remains the primary opponent, while `CI_I` is a
  binding published-protocol veto with this explicitly narrower safeguard.
- **Reopen if:** The recovery point or intervals fail, or an equivalent exact
  size/power validation becomes feasible without weakening `N`, `T`, folds,
  lambda paths, or the published reconstruction.

## D0034 — Let the exact level-share rational control the raw target seal

- **Date:** 2026-07-15
- **Diagnosis:** The derivation implied exact
  `omega=(547/3953)/10=547/39530`, but the first target payload stored
  `0.013837591702504448`, 12 ULP above the nearest binary64 representation of
  that rational. The discrepancy came from evaluating decimal `0.8906` through
  a different binary operation order.
- **Decision:** Make the exact source-decimal rational authoritative and store
  binary64 `0.013837591702504428`. The raw target SHA is now
  `f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59`;
  the 12-decimal semantic SHA remains
  `f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`.
  Independent recomputation confirmed every coefficient, root, penalty, and
  recovery attenuation is otherwise bit-identical.
- **Rejected:** Preserve the earlier raw byte merely because it was already
  hashed. A seal protects an understood contract; it does not make contradictory
  arithmetic correct.
- **Residual risk:** Implementations must derive the rational directly or match
  both seals; reconstructing it through an unfrozen float-expression order is
  forbidden.
- **Reopen if:** Any regenerated downstream target differs or the semantic
  canonicalizer no longer reproduces the unchanged digest.

## D0035 — Freeze the joint simulation and executable workload, not just marginals

- **Date:** 2026-07-15
- **Diagnosis:** Fresh inference review found that covariance/AR marginals and
  13-field keys did not determine the common-random-number joint law: Cholesky,
  symmetric, or rotated square roots change the 459-union/51-intersection
  outcome. It also found that a list of fourteen kernels plus `sum W/v` was not
  executable without a phase-by-kernel work matrix. The paper LASSO still left
  preprocessing order and KKT evaluation implicit.
- **Decision:** Freeze an AR-filter-first float64 symmetric modal transform for
  `q`, `u`, proxy, levels, and returns; freeze pre-FWL scaling, FWL equations,
  coordinate updates, KKT formula, coefficient reconstruction, and best-level
  index; and publish the exact validation/research work matrix and unit
  dominance rules. Unequal 960-/8,460-field paper caches use normalized
  accumulation terms and the slower benchmarked rate. Expected projections,
  not hard-stop slack, license execution.
- **Rejected:** Treat any covariance square root as equivalent, let a library
  choose LASSO preprocessing, or infer whole-phase cost from a convenient
  kernel. Those alternatives change joint validation probabilities, reported
  coefficients, or compute feasibility.
- **Residual risk:** The work table is a pre-run model until measured. A fresh
  arithmetic check corrected the research paper-bootstrap total from an
  erroneous `1,063,072,080` to exact `1,063,828,080`; the distinct resource
  benchmark remains the veto on all rate assumptions.
- **Reopen if:** Any work unit is unmapped, a shorter variant is faster-charged
  without the declared dominance rule, or independent implementation cannot
  reproduce the CRN or LASSO map exactly.

## D0036 — Keep the recovery realization disjoint from sealed research

- **Date:** 2026-07-15
- **Diagnosis:** Recovery prose said the validation counterfactual reused the
  research endpoint's addressed normals, but RNG schema 2 deliberately assigns
  paper recovery to phase 25/scenario 4 and research to phase 30/scenario 0.
  Literal reuse would contradict the namespace contract and expose the sealed
  research realization before validation passed.
- **Decision:** Interpret the no-confounding recovery as a distribution-matched
  counterfactual. It preserves the upper-endpoint `q`, measured-level,
  symmetric-modal-`u`, `Lambda`, AR, and date-reset laws and changes only
  `Gamma`, while drawing its own phase-25/scenario-4 addressed normals. The
  research phase-30 stream remains untouched until every preflight and
  validation condition passes.
- **Rejected:** Reuse phase-30 normals in validation, or weaken the counterfactual
  to exact flows, independent flows, isotropic noise, or a zero cross truth.
  The former leaks the research realization; the latter changes the procedure's
  recovery problem.
- **Residual risk:** Distribution matching does not provide a paired-realization
  treatment contrast. The recovery is only a no-strawman capability check, not
  a causal decomposition or a Monte Carlo size/power license.
- **Reopen if:** Any implementation instantiates phase 30 before recovery and
  smooth validation have passed, or changes any recovery distributional input
  other than `Gamma`.

## D0037 — Never turn nonfinite preprocessing into sparsity

- **Date:** 2026-07-15
- **Diagnosis:** The global numerical contract failed validation on every
  nonfinite input or statistic, but two LASSO clauses said a nonfinite pre-FWL
  RMS or post-FWL norm could be dropped and fixed to zero. That contradiction
  could convert numerical corruption into an apparently valid sparse fit.
- **Decision:** Only a finite, exactly zero pre-FWL RMS or a finite post-FWL
  squared norm at or below `100 eps` may fix a penalized column to zero. Any
  nonfinite scale or norm fails the cell; the existing global policy then fails
  the entire validation license or G2 research publication. The same escalation
  applies to every named `fail_cell` or `fail_response_cell` outcome, including
  a finite weak eigengap or zero OOS SST.
- **Rejected:** Treat nonfinite values like structural zeros. A structural zero
  is an estimand property; nonfiniteness is an invalid computation.
- **Residual risk:** Near-zero finite columns remain algorithmically removed by
  the frozen post-FWL threshold. Their frequency and identities must be
  reported; an unexpectedly common removal pattern is a substantive diagnostic.
- **Reopen if:** Any solver, PCA, scale, norm, loss, coefficient, interval, or
  sufficient statistic can be omitted, imputed, or zeroed after becoming
  nonfinite.

## D0038 — Count every promised Monte Carlo interval

- **Date:** 2026-07-15
- **Diagnosis:** The validation work table counted 52,800 within-superpanel
  smooth event finalizations plus recovery/IID/published intervals, but omitted
  the 459 null-grid and 51 power marginal Monte Carlo intervals promised as
  descriptive outputs and the two family-level CP/Wilson intervals used for
  admission. The aggregation unit also said “candidate cell” although its count
  relies on sharing one cell/weight aggregation across all three candidates.
- **Decision:** Add all 512 omitted finalization units, raising validation
  `interval_finalize` from 52,885 to 53,397. Define one bootstrap-moment
  aggregation as one structural-cell/date-weight aggregation shared by the
  three smooth candidates; candidate-specific solves remain separately counted.
  Each null marginal gets the same one-sided 95% Clopper--Pearson upper endpoint
  as the family union, and each power marginal gets the same one-sided 95%
  Wilson lower endpoint as the family intersection. All 510 are unadjusted,
  descriptive, non-gating intervals.
- **Rejected:** Drop the promised marginal intervals after using them to describe
  validation behavior, or silently charge one aggregation per candidate. The
  former weakens reporting; the latter contradicts the exact work arithmetic.
- **Residual risk:** Finalization is expected to be cheap, but it remains a
  separately benchmarked kernel and may not borrow throughput from a fit or I/O
  kernel.
- **Reopen if:** Any declared validation or research scalar lacks a mapped
  finalization unit, or implementation cannot share the cell/date-weight moment
  aggregation without changing candidate-specific estimates.

## D0039 — Freeze the gate-binding observable PCA algorithm

- **Date:** 2026-07-15
- **Diagnosis:** The observable integrated-OFI opponent fixed within-date scope,
  centering, sign, eigengap, and L1 score normalization, but did not name a
  covariance divisor or eigensolver. Covariance `eigh`, raw-scatter `eigh`, and
  SVD are algebraically related yet can differ at finite-sample rounding and
  eigengap boundaries, changing the exact 459/51 validation procedure.
- **Decision:** For each 330-by-10 date/asset level matrix, form float64
  `X_c'X_c/330`, use symmetric `numpy.linalg.eigh`, select the largest eigenpair,
  then apply the existing deterministic sign and L1 score normalization. No
  bootstrap recomputes a date PCA.
- **Rejected:** Let the implementation inherit an unstated library default or
  infer the observable rule from the separately nested paper-reconstruction
  PCA keys. Gate-binding algorithms must be explicit at their own surface.
- **Residual risk:** Near-degenerate leading eigenvalues can still make the
  loading unstable; the frozen trace-relative eigengap failure rule is therefore
  gate binding and escalates globally.
- **Reopen if:** An implementation uses SVD, an unscaled scatter matrix, a
  different divisor, a nonsymmetric solver, or recomputes PCA under bootstrap
  weights.

## D0040 — Make smooth-ridge centering and solves global and explicit

- **Date:** 2026-07-15
- **Diagnosis:** Population means are zero, but finite-sample date bootstrap
  coefficients depend on whether the intercept is global, date-local, or
  omitted and on whether the Schur system is inverted or solved. The pooled
  candidate froze these choices; the two full-flow ridge candidates had not.
- **Decision:** Both ridge candidates use one global weighted intercept, global
  centering after date weights, no fixed effects, and reaggregated per-date
  cross-products. Nonfinite or nonpositive centered proxy variance fails the
  cell. Symmetrize `S` once, use float64 `numpy.linalg.eigvalsh`, and evaluate
  Eq. (G2.14) with transposed `numpy.linalg.solve`, never an explicit inverse.
- **Rejected:** Per-date demeaning, omitted intercepts, explicit inversion, or
  silent pseudoinverses. Each changes either the finite-sample estimand or the
  registered numerical path.
- **Residual risk:** BLAS/LAPACK can still create tiny cross-platform rounding
  differences. Semantic target tolerances and fail-closed numerical checks must
  be tested on hosted Linux before any registered seed is available.
- **Reopen if:** Bootstrap centering occurs before date-weight aggregation,
  proxy variance is regularized rather than failed, or a solver path differs
  from the frozen NumPy calls.

## D0041 — Retain roundoff eigenvalues and verify the ridge condition cap

- **Date:** 2026-07-15
- **Diagnosis:** “Clip a tiny negative eigenvalue to zero” left two legitimate
  implementations: reconstruct a PSD matrix from eigenvectors, or change only a
  scalar used by the penalty formula. Either can make the solved matrix's actual
  condition number differ from the advertised cap.
- **Decision:** After `eigvalsh`, fail a nonfinite or nonpositive `smax`; accept
  eigenvalues in the closed roundoff band
  `[-100 eps max(1,|smax|),0]` but retain their raw values in the condition
  penalty and once-symmetrized solve. More negative eigenvalues fail. After
  adding the ridge, require a positive finite minimum eigenvalue and actual
  eigenvalue ratio at most `K(1+1000 eps)`.
- **Rejected:** Eigenvector reconstruction or silent PSD projection. Neither is
  needed for the declared roundoff guard and both introduce another numerical
  path.
- **Residual risk:** The `1000 eps` allowance is numerical rather than
  statistical; every realized ratio is still reported, and any material excess
  fails.
- **Reopen if:** Cross-platform tests need a larger allowance, a tolerated
  negative is comparable with the ridge floor, or any implementation projects
  `S` before solving.

## D0042 — Seal the LASSO ratio vector as binary64 data

- **Date:** 2026-07-15
- **Diagnosis:** The mathematical grid `10^(-4k/39)` did not select a unique
  binary64 vector. In the locked environment, scalar exponentiation and
  `numpy.logspace` disagree at 7 of 40 indices by as much as eight ULPs. That
  difference can cross the absolute `10^-12` CV tie tolerance and select a
  different outer penalty.
- **Decision:** Store all 40 descending ratio values as config literals, parse
  them directly as float64, and require little-endian float64 C-order SHA256
  `1da884c55b3f6e7bf79012973bddf092a92efb1ea098cd2717a804645a62c9a0`.
  Runtime regeneration from a formula or `logspace` is unlicensed.
- **Rejected:** Treat algebraically equivalent constructors as numerically
  interchangeable. The selected-ratio index is part of the estimator.
- **Residual risk:** Decimal-to-binary parsing is delegated to the pinned Python
  TOML runtime; implementation tests must verify all 40 bit patterns and the
  digest on macOS and hosted Linux before any registered seed is accessible.
- **Reopen if:** The parsed vector fails its digest, is not strictly descending
  with exact endpoints one and `0.0001`, or a supported runtime parses a literal
  differently.

## D0043 — Retire every pre-S0004 execution clause

- **Date:** 2026-07-15
- **Diagnosis:** D0026--D0028 correctly document S0003's evolution but use
  generic future-tense language, including two candidates, secondary-only CCZ
  fits, old fit counts, and a 21-hour stop. A parser or hurried reader could
  mistake that history for live S0004 authority despite D0031 onward.
- **Decision:** D0026, D0027, D0028, and every pre-D0031 G2 candidate, workload,
  validation, veto, or budget clause are historical S0003 records only and
  grant no S0004 execution authority. The live S0004 contract is D0031 onward,
  the latest preregistration amendment, and the sealed schema-3 config; any
  conflict is a hard failure rather than a choice among versions. DGP keys share
  common normals within the active phase/scenario; their parent slots remain
  zero sentinels except for bootstrap provenance.
- **Rejected:** Rely on chronological implication alone. Mechanical retirement
  is required because stale counts and candidate scopes are executable-looking.
- **Residual risk:** Historical prose remains searchable by design. The final
  admission amendment must repeat this authority rule and bind one raw config
  digest so automated checks have a single executable surface.
- **Reopen if:** Any implementation, benchmark, or review cites a pre-D0031
  count, candidate set, veto status, budget, key-sharing rule, or estimator map
  as current authority.

## D0044 — Assign every DGP stream one phase/scenario pair

- **Date:** 2026-07-15
- **Diagnosis:** Named phase and scenario IDs plus a disjointness rule did not
  uniquely pair the two fields for ordinary size, power, recovery, IID, or
  resource draws. An implementation could choose an unlisted non-base scenario
  and still claim a collision-free 13-field key.
- **Decision:** Freeze the only licensed assignments as resource smooth `10/0`,
  resource paper `10/1`, size `20/0`, power `21/0`, date frontier `22/2`, smooth
  recovery `23/0`, IID `24/0`, paper recovery `25/4`, and research `30/0`.
  Reliability frontier `22/3` remains metadata-only reuse of `21/0` and creates
  no generator. DGP parent slots are zero sentinels; only phase-40 bootstrap
  keys carry the exact parent phase/scenario.
- **Rejected:** Infer scenario zero by convention wherever no special scenario
  was named. The address, not an informal default, defines the random variable.
- **Residual risk:** Bootstrap implementation must still prove that every
  phase-40 key carries the correct named parent and date count; hard-fail key
  tests precede all registered access.
- **Reopen if:** Any stochastic DGP draw uses an unlisted pair, metadata-only
  `22/3` instantiates a generator, or a DGP key has nonzero parent slots.

## D0045 — Give every mandatory frontier rate an interval

- **Date:** 2026-07-15
- **Diagnosis:** The work ledger counted every within-superpanel frontier fit
  but omitted inferential finalization for six date-frontier and twelve extra
  reliability-frontier passage rates. Calling these outputs mandatory
  frontiers while reporting naked rates would violate the project's
  number/interval contract.
- **Decision:** For each of the three candidates at 48 and 96 dates and at each
  extra reliability 0.96--0.99, report an unadjusted, one-sided 95% Wilson lower
  interval over 100 superpanel indicators. These 18 intervals are descriptive
  and non-gating. Reliability 0.95 reuses the already counted power marginals;
  252 dates is the main operating point; reliability one retains its separate
  recovery interval. Increase validation `interval_finalize` from 53,397 to
  53,415.
- **Rejected:** Publish frontier point rates without intervals or quietly call
  the retained bootstrap panels non-inferential. Both contradict the declared
  purpose of a failure frontier.
- **Residual risk:** Reduced frontiers vary one dimension at one endpoint and
  are not the full G4 failure surface. Their narrow descriptive scope must stay
  explicit.
- **Reopen if:** Any frontier rate lacks its Wilson endpoint, is treated as a
  gate, or the phase work table omits one of the 18 finalization units.

## D0046 — Define the CV tie statistic and boundary exactly

- **Date:** 2026-07-15
- **Diagnosis:** The paper reconstruction pooled five validation SSEs but
  selected ratios within an absolute MSE tolerance without defining the
  denominator, accumulation order, or equality boundary. SSE, SSE/30, and
  fold-mean MSE share a minimizer but not the same `10^-12` tie set.
- **Decision:** For each literal ratio, accumulate float64 validation SSE in
  fold order 0 through 4, divide once by float64 30, fail any nonfinite value,
  then select the lowest ratio index satisfying
  `MSE_k <= min_j(MSE_j) + float64(1e-12)`. This inclusive set maps to the one
  zero-initialized outer solve already frozen.
- **Rejected:** Apply the tolerance to pooled SSE or leave equality to an
  implementation-specific comparison. Either can select a different penalty.
- **Residual risk:** BLAS rounding inside each fold loss can still differ by
  platform; cross-platform fixtures must exercise an intentionally near-tied
  path before registered access.
- **Reopen if:** A solver averages fold MSEs, divides before SSE accumulation,
  compares strictly, regenerates the ratio vector, or selects any later index
  within the tolerance set.

## D0047 — Exclude the cold bundle from the warm-time clock

- **Date:** 2026-07-15
- **Diagnosis:** Config and prediction required 600 post-cold seconds, but the
  compute plan said only 600 seconds and could count the cold bundle toward the
  warm minimum while still claiming four total bundles.
- **Decision:** The first complete bundle supplies the cold measurement and
  counts toward the minimum four total bundles. Only elapsed time of subsequent
  complete bundles counts toward the 600-second warm clock; throughput remains
  the last three complete hash-checked bundles.
- **Rejected:** Count cold time as warm exposure. That would weaken the thermal
  stress without changing the displayed threshold.
- **Residual risk:** Four total bundles and 600 post-cold seconds will usually
  imply more than three warm bundles; the implementation must retain the last
  three rather than the first three.
- **Reopen if:** Any benchmark report cannot separately reproduce cold elapsed,
  post-cold elapsed, total completed bundles, and the identities of the three
  bundles entering warm throughput.

## D0048 — Freeze the RNG distribution calls, not only their keys

- **Date:** 2026-07-15
- **Diagnosis:** PCG64DXSM, SeedSequence entropy, component shapes, and C-order
  consumption did not uniquely map generator bits to Gaussian arrays.
  `standard_normal`, `normal`, or a custom transform can share every declared
  key while producing different draws. The multinomial prose likewise named
  equal probabilities without one constructor.
- **Decision:** Every DGP component key makes exactly one
  `Generator.standard_normal(size=tuple(shape), dtype=np.float64)` call and
  requires its C-contiguous return without reshape. Every bootstrap key builds
  `np.full(n_dates, 1.0/float(n_dates), dtype=np.float64)`, makes exactly one
  `Generator.multinomial(n=n_dates, pvals=pvals, size=None)` call, and converts
  counts to float64 weights.
- **Rejected:** Define only a target distribution. Registered replay requires
  the deterministic NumPy transform from addressed generator state to bytes.
- **Residual risk:** A future NumPy release may change distribution internals;
  the pinned lockfile and cross-platform known-answer fixtures must therefore
  gate stream access.
- **Reopen if:** Any draw uses `normal`, an inverse-CDF/custom transform,
  multiple calls per component key, a non-C-contiguous reshape, or differently
  constructed bootstrap probabilities.

## D0049 — Freeze one post-audit S0004 config digest

- **Date:** 2026-07-15
- **Diagnosis:** S0004 could not become a mechanical preregistration while its
  config changed after each valid hostile finding. A digest taken before the
  final content pass would merely seal an ambiguity.
- **Decision:** After independent math, inference, and whole-contract content
  passes, freeze the raw schema-3 `configs/g2.toml` SHA256 as
  `f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc`.
  Bind it with target raw/semantic hashes
  `f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59` /
  `f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`
  and LASSO-ratio hash
  `1da884c55b3f6e7bf79012973bddf092a92efb1ea098cd2717a804645a62c9a0`.
  A005 is the single authority clause; all pre-D0031 execution details are
  historical and non-executable.
- **Rejected:** Seal a moving config or rely only on semantic prose. Neither
  prevents stale S0002/S0003 machinery from being selected mechanically.
- **Residual risk:** The sealed contract proves a reproducible conditional
  experiment, not that 95% proxy reliability or the latent decomposition is
  empirically identified. That remains the strongest unanswered objection.
- **Reopen if:** Any digest fails, the sealed-surface reviewer finds a conflict,
  or an executable config byte must change. Reopening creates a new
  specification and amendment before any stream access.

## D0050 — Admit the sealed contract only to the hosted boundary

- **Date:** 2026-07-15
- **Diagnosis:** A hash seal is not enough if independent readers cannot
  reproduce it or if an older authority clause remains live. Conversely, a
  sealed documentation pass is not evidence that unimplemented estimators or
  resource projections work.
- **Decision:** Three independent final re-reads reproduced all four A005 seals,
  parsed the exact estimator/RNG/workload contract, and confirmed that S0002,
  S0003, and every pre-D0031 execution clause are mechanically retired. S0004
  therefore passes pre-implementation contract admission. This authorizes only
  the clean documentation commit/push, hosted CI, and—after hosted green—test-
  first implementation with test-only seeds. It does not expose any registered
  G2 stream.
- **Rejected:** Treat content review as implementation validation or skip the
  hosted boundary because local checks are green. Neither tests the final
  committed cross-platform surface.
- **Residual risk:** The strongest objection remains the favorable unsourced
  95% reliability/latent decomposition. Passage can support conditional
  existence only; failure cannot kill the market premise without the separate
  sharp source-compatible bound.
- **Reopen if:** Hosted CI changes or rejects any sealed artifact, the raw config
  digest moves, a stale design becomes executable, or implementation reveals an
  unlicensed choice. Any such event returns S0004 to pre-run review.

## D0051 — Open only the test-first implementation lane

- **Date:** 2026-07-15
- **Diagnosis:** Local and independent review cannot substitute for verifying
  the committed sealed bytes on the hosted Linux parity path. Passing that path
  still does not license resource, validation, or research draws.
- **Decision:** Commit `a5c7f1c02e941a0d6fdef3d645dfea63884cdfd7` passed hosted CI
  run `29448917107`, including the locked parity suite. The schema-3 config
  remained at SHA256
  `f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc`.
  This closes the documentation admission and opens only test-first S0004
  implementation with explicit test-only seeds.
- **Rejected:** Run the registered resource benchmark immediately after the
  documentation pass. The resource stream requires completed implementation,
  estimator-recovery tests, local/hosted parity, and hostile code review first.
- **Residual risk:** Hosted CI currently exercises the existing G0/G1 package,
  not unimplemented G2 algorithms. Its green status validates the sealed
  boundary, not the future estimator.
- **Reopen if:** The acceptance-ledger commit fails hosted CI, the implementation
  cannot hard-fail altered digests/schemas, or a registered seed appears in any
  test or development command.

## D0052 — Make executable identity stricter than Python equality

- **Date:** 2026-07-15
- **Diagnosis:** The first typed contract validator compared tuples and values
  with ordinary Python equality. That admitted operationally different objects:
  float dimensions equal to integers, `-0.0` equal to `0.0`, plain strings equal
  to `StrEnum` members, integers equal to `IntEnum` members, mutable lists in
  place of tuples, and target-row changes below a regeneration tolerance. Some
  passed validation and failed only in a downstream NumPy or identity lookup.
- **Decision:** Validate the exact runtime dataclass, container, element, enum,
  integer, and Python-float representations before semantic checks. Compare all
  calibration floats by exact hexadecimal binary64 identity. Add a derivative
  little-endian binary64 SHA256 over the 17-by-4 target matrix,
  `2ff803d9cf5e14f916266293d0c52e2712da2db7d5d0b6f5a410c4eaefff39c7`,
  and reject a one-ULP target mutation. This derivative guard does not alter the
  A005 files or their four authority seals.
- **Rejected:** Treat equality plus `allclose(..., atol=5e-13)` as adequate typed
  authority. Mathematical regeneration tolerances are appropriate diagnostics,
  not permission for a different executable payload.
- **Residual risk:** Python callers can deliberately monkeypatch private module
  state; the boundary guarantees supported package behavior, not hostile-code
  isolation inside one interpreter.
- **Reopen if:** Any equality-compatible representation passes validation, the
  derivative target digest changes, or a validated contract later fails because
  a field has an unexpected runtime type.

## D0053 — Consume one validated entropy snapshot per stochastic call

- **Date:** 2026-07-15
- **Diagnosis:** A subclass could override `RNGAddress.entropy()` after benign
  fields were validated, a namespace subclass could override its seed guard,
  and bootstrap construction reread a frozen address after `np.full`. Hostile
  tests routed a registered seed value to an intercepted `SeedSequence` without
  instantiating that stream. The initial bootstrap surface also admitted
  recovery and IID parents that have no date-bootstrap procedure.
- **Decision:** Reject address and namespace subclasses at runtime, invoke
  validators class-qualified, and have validation return one nonvirtual
  13-field uint32 entropy tuple consumed unchanged by `SeedSequence` and all
  downstream shape/date logic. Whitelist only resource smooth/paper, validation
  size/power/date-frontier/paper-recovery, and research bootstrap parents. Spy
  tests require the exact four-event Gaussian and five-event bootstrap call
  traces, including exactly one distribution call.
- **Rejected:** Rely on frozen dataclasses or call `entropy()` again after
  validation. `object.__setattr__` and virtual dispatch make both claims false
  under the same adversarial model used by the project tests.
- **Residual risk:** NumPy distribution internals remain version-dependent; the
  lockfile, known-answer hashes, and future hosted parity boundary remain
  mandatory.
- **Reopen if:** Any RNG path rereads an address after validation, accepts a
  subclass, instantiates metadata-only `22/3`, admits an unused bootstrap parent,
  or makes more than one configured distribution call per address.

## D0054 — Keep raw-origin authority outside the raw wrapper

- **Date:** 2026-07-15
- **Diagnosis:** Provenance labels, byte hashes, and a receipt stored inside
  `RawBaseNormals` were self-attestation. Reviewers rewrapped filtered arrays,
  mixed dates and components, relabeled phase 21 as phase 25, inserted phase-30
  research arrays into recovery, and reconstructed or coordinately mutated the
  exposed receipt. A callable generic registrar had the same flaw.
- **Decision:** Only exact `TestRngNamespace.draw_base_normals` may insert into a
  module-owned weak issuance registry, inline after its five method-owned draws.
  The registry stores the original provenance snapshot, exact five component
  identities, and original byte token against the exact wrapper identity.
  `transform_date` rejects every unregistered constructor/factory result and any
  later label, object, or content mutation. Weak references remove dead bases;
  a GC regression locks cleanup and the validator checks `weakref() is base` to
  defeat stale identity reuse. The generic private packaging helper cannot mint
  registry authority.
- **Rejected:** Replay each component RNG during validation. It is definitive but
  would make a second `standard_normal` call for one address, violating D0048
  and contaminating resource timing. Also rejected: wrapper-owned keyed or
  unkeyed receipts, because any receipt exposed on the object can be copied or
  mutated with it.
- **Residual risk:** Per-transform hashing cost is not yet benchmarked and must
  enter the fourteen-kernel resource admission. Arbitrary direct mutation of the
  underscore registry remains outside the supported API threat model.
- **Reopen if:** More than one registry write exists, a generic factory or public
  constructor can mint an accepted base, registry entries retain dead arrays,
  or any cross-date/component/phase mixture reaches the deterministic map.

## D0055 — Diagnose the hosted Gaussian mismatch below the distribution boundary

- **Date:** 2026-07-15
- **Diagnosis:** Commit `682a38152fbbbe971b1c59258a9de98df2151add`
  passed every local check but hosted Linux run `29453577345` failed one of 117
  tests: the 99,000-value level-noise `standard_normal` SHA256 was
  `6061c2e6e38a7228701bfaa2e77ab7699154948d0bdca9fa6a0d992f6a848b64`
  instead of the M4 value
  `593fe9b8e8f102bce0e58303a49b26cd713121c38e2219c9005ebaaf1c074091`.
  Four smaller, independently addressed component arrays matched. NumPy's
  `Generator` compatibility policy is conditional on the same build,
  environment, machine, call sequence, and arguments; `PCG64DXSM` separately
  guarantees that a fixed seed produces the same integer stream. Changing an
  expected distribution hash before locating the layer of divergence would
  therefore erase evidence.
- **Prediction before diagnostic run:** For the exact level-noise address, Linux
  will reproduce the M4 150,000-word `PCG64DXSM.random_raw` digest
  `4b513e5dee9968d985cca87af4640a9e466238afedcf6bece87784ab56ccfdf4`.
  The first mismatch will occur only in a later 1,000-value block of the normal
  transform, consistent with an architecture-dependent rare slow path rather
  than address packing or PCG state initialization.
- **Decision:** Add a test-seed-only raw-stream known answer plus failure-only
  platform, raw-digest, first-value, and chunk-digest telemetry. Run it on the
  same locked macOS and hosted-Linux environments before changing production
  code, the sealed call, or the acceptance rule.
- **Diagnostic result, stage one:** Hosted run `29453989738` reproduced the raw
  digest and all first eight normal values exactly. Programmatic comparison of
  99 nonoverlapping 1,000-value hashes found exactly one differing block,
  zero-based block 60; blocks 0--59 and 61--98 matched. This falsifies seed,
  address, PCG, bulk-call-shape, and state-consumption drift. Before the stage-two
  run, the prediction is that only one or a few values in indices 60,000--60,999
  differ at the last bits while all neighboring values match, implicating a
  platform math result in a rare slow path.
- **Diagnostic result, stage two:** Hosted run `29454185569` and the M4 reference
  differ at exactly one of the isolated 1,000 values: global index 60,328 is
  `0x1.f987e87be94a2p+1` on Linux and
  `0x1.f987e87be94a3p+1` on M4, one ULP. Its magnitude exceeds NumPy 2.5.1's
  `3.6541528853610088` Ziggurat cutoff, and the official source computes that
  tail through `npy_log1p`; later values remain equal. Root cause is therefore
  platform libm rounding in the Gaussian tail transform, not PCG state,
  addressing, array size, or branch consumption.
- **Remedy:** Preregistration amendment A006 keeps the sealed draw unchanged,
  makes the raw PCG stream and exact call trace universal CI invariants, records
  two frozen runtime-class KAT outcomes for test-only verification, and makes
  the exact declared Darwin/arm64 fingerprint plus its M4 known answers the
  sole registered execution authority. Unknown fingerprints fail closed before
  `SeedSequence`.
- **Rejected:** Accept both full-array hashes, round generated normals, or
  replace NumPy's transform on the strength of one aggregate mismatch. Each
  hides or outruns the causal diagnosis; the last two would also alter the
  A005 execution contract and require a preregistration amendment.
- **Residual risk:** Exact Gaussian replay is machine-bound. Five KAT arrays do
  not prove that every unseen platform-math tail input is stable; they only
  fail closed on known fingerprint drift. A Linux replication can produce a
  different sharp-threshold decision and is not interchangeable research
  evidence. Universal cross-machine replay would require a new portable-
  transform design before registered access.
- **Reopen if:** The raw PCG digest differs, the mismatch starts at the first
  normal value, or NumPy/CPU versions differ from the locked environments.
