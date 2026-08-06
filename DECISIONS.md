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

## D0056 — Close portability only on the fail-closed hosted boundary

- **Date:** 2026-07-15
- **Diagnosis:** Local M4 KATs and hostile review could establish the authorized
  path, but only hosted Linux could prove that the frozen verification-class
  hash passes while registered preflight rejects before `SeedSequence`.
- **Decision:** Commit `ff3a343e9c4cfbf672d7cae5614081733c4b695e`
  passed hosted run `29455143418`, including all 119 tests and the full quality
  and demo path. This closes C0002 and the contract/RNG/DGP first slice. It
  opens only test-first sufficient-statistic and estimator implementation with
  seeds `1729` and `9191`; registered resource, validation, and research
  authority remain blocked.
- **Rejected:** Treat the local M4 pass alone as portability closure or use the
  hosted pass to expose the resource seed before estimators and checkpointing
  recover truth under the same contract.
- **Residual risk:** Linux does not reproduce the authorized research
  realization, and finite KATs do not cover every unseen libm tail. A006's
  machine-bound limitation remains a reported reproducibility constraint.
- **Reopen if:** The hosted run is invalidated, a future runtime fingerprint
  changes, or any production constructor can reach a registered seed without
  consuming the successful A006 preflight fingerprint.

## D0057 — Use covariance-unit Schur moments

- **Date:** 2026-07-16
- **Diagnosis:** The sealed prose required globally centered weighted
  cross-products but did not say whether the Schur outputs were retained as raw
  scatters or divided by weighted row mass. The two routes produce the same
  exact-arithmetic coefficients because the condition and floor penalties
  scale with the covariance, but they differ in binary64 diagnostics and can
  differ at numerical failure boundaries.
- **Decision:** Aggregate raw date cross-products, partial the single global
  intercept, then divide every centered block by the weighted row mass before
  proxy partialling or solving. This is the only route that reproduces the
  covariance-unit oracle and observable penalties already sealed in
  `configs/g2_population_targets.json`. Apply the same convention to pooled
  homogeneous slopes.
- **Rejected:** Leave raw scatters in the eigensolver merely because the
  coefficient is scale invariant. That would report a differently scaled
  penalty and leave the sealed diagnostic unexplained.
- **Residual risk:** Division adds one rounding step even though the real-number
  estimator is unchanged. Analytic direct-row and moment-route tests must lock
  the selected path before test-seed recovery.
- **Reopen if:** A sealed population penalty cannot be reproduced in covariance
  units, any implementation centers dates separately, or weighted centering is
  applied before date aggregation.

## D0058 — Freeze one packed and weighted aggregation path

- **Date:** 2026-07-16
- **Diagnosis:** The compute plan fixed sufficient-statistic counts but not
  triangle layout or accumulation order. A Python date loop would be easier to
  reason about but would sit inside 1,796,400 registered bootstrap aggregation
  units and threaten the 12-hour validation budget.
- **Decision:** Pack row-major upper triangles with `numpy.triu_indices`; store
  all panels C-contiguous, date-major, and in ascending `date_index`; flatten
  nonsymmetric fields in C order; and aggregate each field panel with exactly
  one `numpy.matmul(weights, panel)` call. Require float64 nonnegative integer
  weights with exact total equal to the number of dates. Point estimates use
  float64 ones, while zero bootstrap counts keep their original positions.
- **Rejected:** Python-loop accumulation, normalized fractional weights, a
  caller-selected triangle, or silently sorting a weight vector independently
  of its panel. These either change the byte path, weaken the bootstrap
  capability boundary, or waste the declared hardware budget.
- **Residual risk:** NumPy matrix multiplication is runtime/BLAS dependent. A006
  already makes the registered numerical runtime machine-bound; hosted Linux
  remains a tolerance-based software surface rather than an alternative draw.
- **Reopen if:** The resource kernel cannot meet its projection with this path,
  a checkpoint does not preserve ascending provenance, or two fields require
  different aggregation semantics.

## D0059 — Keep pure math underneath a sealed estimator contract

- **Date:** 2026-07-16
- **Diagnosis:** The existing typed G2 contract projected the DGP but omitted
  condition caps, ridge floor, PCA eigengap, and pooled rank thresholds already
  present in the sealed config. Embedding them only as model-module constants
  would create hidden run state, while hard-coding `N=30` in every linear-
  algebra helper would make analytic orientation tests needlessly opaque.
- **Decision:** Extend the exact typed contract and validator with every smooth
  estimator numerical field. Validate text-encoded rules against their exact
  sealed strings before projecting their numeric multipliers. Put dimension-
  generic, deterministic PCA/packing/solve kernels below contract-bound date
  and panel builders that enforce `N=30`, `T=330`, `L=10`, float64 finiteness,
  and provenance. Use default-lower-triangle `numpy.linalg.eigh` without an
  extra PCA symmetrization and `numpy.linalg.svd(..., compute_uv=False)` for the
  pooled rank check.
- **Rejected:** Re-read the config independently inside the model module,
  expose arbitrary estimator thresholds through the production API, or hide
  them as unrelated literals. Each creates a second authority surface.
- **Residual risk:** Adding fields to `G2Contract` widens its validation surface;
  mutation, representation, and altered-string tests must fail before any RNG
  construction.
- **Reopen if:** An estimator can be constructed from an unvalidated threshold,
  a generic helper becomes a production bypass, or PCA/SVD calls differ from
  the frozen routines.

## D0060 — Treat provenance as data, not a shape convention

- **Date:** 2026-07-16
- **Diagnosis:** C0003's first hostile review constructed two invalid but
  accepted inputs: a forged `G2Date` with arbitrary phase/scenario metadata,
  and an aggregate pairing `X_A'X_A` with `X_B'Y_B` at the same date index.
  Exact class, dimensions, and ordering are necessary but do not bind origin.
- **Decision:** Mint transformed dates inside `transform_date` with a weak
  module-owned receipt, make every transformed array read-only, and validate
  object identity, provenance, content, and cleanup before contract-bound
  estimator use. Carry a versioned SHA256 of the exact `X0` design and the
  validated filtered-base identity through base/cell moments and panels; reject
  any mismatch before weighted aggregation. Add a contract-bound response
  moment builder so different structural cells are allowed only on the same
  base realization/date.
- **Rejected:** Trust a caller-supplied token, compare only `date_index`, or
  hash only response-independent shapes. The first is self-attestation, the
  second reproduces the diagnosed bug, and the third cannot detect a changed
  design matrix.
- **Residual risk:** Content validation adds hashing to each transformed date.
  The resource benchmark must measure the cost and can still reject this
  implementation. SHA256 collision risk is negligible for accidental or
  adversarial mixing but is not a mathematical proof of array equality.
- **Reopen if:** Legitimate common-base structural cells cannot share a design,
  a forged/rewrapped date reaches a contract builder, a checkpoint drops the
  aligned digest tuple, or measured receipt hashing breaks the resource cap.

## D0061 — Make completeness and fit authority explicit types

- **Date:** 2026-07-16
- **Diagnosis:** Strictly ascending indices prove order, not completeness. The
  old stack could omit a failed date and redefine `D`; the old fit functions
  also validated a sealed contract without requiring the aggregate to have the
  contract's N=30/T=330/L=10 dimensions or minted origin.
- **Decision:** Carry exact source coordinates through each contract moment and
  require the complete declared date range under one panel prefix. Separate
  analytic-origin aggregates from contract-origin aggregates. Keep generic
  covariance extraction and solvers available for small deterministic tests,
  but let high-level G2 fit functions return coefficients only for a complete
  contract-origin aggregate matching all sealed dimensions.
- **Rejected:** Infer completeness from supplied length, accept a prefix as a
  smaller panel, or rely on callers to choose the production wrapper. Each
  permits the diagnosed no-drop or authority bypass.
- **Residual risk:** The contract-origin high-level fit will not receive a full
  stochastic integration test until the separately registered checkpoint and
  recovery slice. Deterministic provenance/completeness tests must cover its
  admission predicate now; later recovery remains mandatory before any
  registered estimator run.
- **Reopen if:** A required date can disappear without an exception, a 252-date
  prefix passes as a frontier, or an analytic aggregate reaches a high-level G2
  fit.

## D0062 — Use digests for equality and receipts for authority

- **Date:** 2026-07-16
- **Diagnosis:** The base identity is intentionally shared across structural
  cells and therefore cannot label `r`. Separately, a digest copied into a new
  dataclass is evidence about claimed bytes, not evidence that the object was
  minted by the contract builder.
- **Decision:** Retain a response-map identity `(target_index, paper_recovery,
  phi, reliability)` through transformed dates and cell moments. Mint weak,
  module-owned receipts for every contract date-moment, complete-panel, and
  aggregate object, binding payload content and provenance. Only an issued
  aggregate may reach high-level G2 fits; analytic objects stop at extraction
  and generic solvers.
- **Rejected:** Treat the filtered-base token as a cell label, or add a boolean
  `contract_origin` field without issuance. The former erases the structural
  cell distinction; the latter repeats the forged-dataclass failure.
- **Residual risk:** Receipt validation and hashing add CPU work and remain an
  in-memory capability only. The future checkpoint loader needs an independent
  manifest-validation design and the resource benchmark can reject the cost.
- **Reopen if:** A copied digest can mint authority, response-map metadata is
  lost, or two legitimate cells on the same base cannot remain distinct.

## D0063 — Issue every numeric wrapper that crosses an authority boundary

- **Date:** 2026-07-16
- **Diagnosis:** The C0004--C0006 repair issued the base date moment but the
  contract cell builder consumed `SmoothDateDesign.x0`. Replacing the unissued
  design wrapper while retaining its issued base moment allowed a different
  cross-moment to be computed under copied provenance. The high-level fits also
  accepted a free reliability argument without asserting the aggregate's full
  response-map label.
- **Decision:** Mint and validate an exact weak receipt for each contract-built
  design before it can form cell moments. Bind array contract state as well as
  bytes in every smooth issuance token. Require high-level callers to supply
  the expected response-map identity and match the fit reliability to it.
- **Rejected:** Recompute only the Gram, because row transformations can
  preserve `X'X` while changing `X'Y`; trust the copied design hash, because
  that repeats self-attestation; or leave response labels solely to result
  manifests, because a mislabeled estimate would already have escaped the
  licensed fit boundary.
- **Residual risk:** Exact-object receipts are process-local and hashing cost
  remains subject to A022's resource benchmark. The future checkpoint loader
  must mint fresh authority only after independent manifest validation.
- **Reopen if:** A replaced design can reach `X0'Y`, writable issued payloads
  validate, or a fit can use a response identity different from its aggregate.

## D0064 — Anchor stored moments once and inline every issuance write

- **Date:** 2026-07-16
- **Diagnosis:** A011's first wording would require response-receipt reliability
  to equal every fit reliability, contradicting the sealed rule that reliability
  changes reuse the same `f/e/Q/W/r` moments. Separately, `_register_issued` and
  private kernels accepting public receipts would be callable minting surfaces,
  which D0054 already rejects for raw draws.
- **Decision:** Mint smooth moment artifacts only from the canonical 0.95 date
  anchor. Match high-level fits to the aggregate on target, recovery flag, and
  `phi`; bind the requested reliability to the caller's expected identity while
  allowing it to differ from the stored anchor. Put each weak-registry write
  inline in its exact validated contract builder/stack/aggregate function and
  remove the generic registrar.
- **Rejected:** Rebuild or reissue identical date moments for all reliability
  nodes, because that violates the compute contract; ignore response labels,
  because that permits misreporting; or retain a convenience registrar, because
  it can mint a forged object with one private call.
- **Residual risk:** The canonical-anchor rule must remain explicit in the
  future checkpoint schema and resource counts. Fit extraction still hashes
  issued aggregate content and remains subject to A022.
- **Reopen if:** Reliability changes duplicate stored moments, a non-anchor date
  mints a smooth artifact, or any callable generic helper can insert authority.

## D0065 — Bind exact array semantics, not only storage bytes

- **Date:** 2026-07-16
- **Diagnosis:** A numpy subclass can share identical float64 C-order read-only
  bytes while overriding transpose, indexing, ufunc, or matrix-multiplication
  behavior. The first issued-token repair hashed only storage metadata and
  bytes, so same-wrapper mutation through `object.__setattr__` could preserve
  the token but alter downstream dispatch.
- **Decision:** Issued smooth payload validation requires exact `np.ndarray`,
  exact float64, C-contiguous, read-only, and finite arrays before hashing.
- **Rejected:** Rely on `np.asarray` coercion at every later use, because it
  spreads the capability boundary across numerical code and can be omitted in
  one path; or accept subclasses whose bytes match, because storage equality
  does not imply operator equality.
- **Residual risk:** Deliberate mutation of private registries remains outside
  the supported API threat model. Exact ndarray validation must remain in the
  common issued-token path for every stage.
- **Reopen if:** Any issued token accepts an array subclass or a downstream
  contract calculation dispatches through an unvalidated array object.

## D0066 — Treat provenance projection as an exact typed boundary

- **Date:** 2026-07-16
- **Diagnosis:** `_receipt_payload` read attributes from arbitrary objects. On a
  same-object aggregate mutation, a stateful substitute could project the
  original receipt into the token and a different response map into the fit
  label check.
- **Decision:** Validate exact receipt, provenance, response-map, stream-enum,
  and scalar runtime types in the common receipt projection before hashing or
  comparison.
- **Rejected:** Rely on dataclass field equality or one earlier validator;
  retained values cross new authority stages and frozen wrappers can be changed
  with `object.__setattr__` under the project's adversarial model.
- **Residual risk:** Concurrent mutation between sequential validations remains
  outside the single-threaded execution contract. Same-thread duck typing and
  representation substitution are closed.
- **Reopen if:** Any retained receipt is consumed through attribute duck typing
  or a response-map comparison uses an object not validated by the token path.

## D0067 — Validate issued wrappers before canonical projection

- **Date:** 2026-07-16
- **Diagnosis:** Canonical JSON and `.hex()` preserve values, not operator
  semantics. Lists can project like tuples, integer subclasses like integers,
  and a float subclass can preserve `row_mass.hex()` while changing reflected
  division after the token passes.
- **Decision:** Put exact schema validation inside every stage-specific issued
  token function before canonical projection: wrapper, nested dataclasses,
  scalar fields, tuple containers/members, receipts, and arrays.
- **Rejected:** Coerce values before each later calculation, because that would
  distribute the authority boundary through the estimator and leave metadata
  relabeling paths; hash class names only, because exact checks are simpler and
  already match builder output.
- **Residual risk:** Unsupported direct mutation of private issuance registries
  remains out of scope. All public contract paths remain exact-type surfaces.
- **Reopen if:** A value-equal subclass or JSON-equivalent container preserves
  an issued token or reaches numerical arithmetic.

## D0068 — Validate one immutable snapshot of every caller sequence

- **Date:** 2026-07-16
- **Diagnosis:** `stack_contract_cell_moments` validated a caller-supplied
  `Sequence` and then traversed it again to build arrays and metadata. A
  state-changing sequence returned issued moments for validation and altered,
  unissued moments for stacking; the resulting panel and aggregate were still
  minted. Exact item validation is ineffective if the container can change
  between reads.
- **Decision:** Convert every smooth stacker input to one exact local tuple at
  entry and use only that tuple thereafter. Contract stackers validate and mint
  from the same snapshot; analytic stackers adopt the same one-read boundary so
  later refactors cannot reintroduce the ambiguity.
- **Rejected:** Require callers to pass a tuple, because a runtime annotation is
  not an authority check and needlessly narrows the public numeric API; or hash
  the container between traversals, because a stateful container controls both
  projections and the extra read recreates the race.
- **Residual risk:** Concurrent mutation of the already-snapshotted moment
  objects remains governed by the existing single-threaded execution contract
  and per-object token validation. Private registry mutation remains out of
  scope.
- **Reopen if:** Any stacker rereads the caller container after snapshotting or
  a panel can be minted from numeric items different from those whose issuance
  was checked.

## D0069 — Close the smooth estimator core, not the execution pipeline

- **Date:** 2026-07-16
- **Diagnosis:** The first numerically green implementation was not defensible:
  successive hostile passes found forged provenance, crossed base/response
  moments, incomplete panels, analytic-to-contract authority bypasses,
  unissued designs, relabelable response maps, callable minting helpers,
  equality-compatible runtime substitutes, and finally a multi-traversal
  sequence substitution. Each defect could preserve plausible numerical output
  while violating the claimed estimator origin.
- **Decision:** Accept only the in-memory smooth estimator core after C0004--
  C0013, 49 focused tests, the 157-test repository gate, the complete timed
  48-date issued path, and independent mathematical and contract re-audits.
  Keep checkpoint loading, registered recovery, resource admission, validation,
  and research authority closed as separate future slices.
- **Rejected:** Treat the earlier 138- or 156-test green states as sufficient,
  because each preceded a reproduced authority failure; or fold checkpoint and
  resource work into this commit, because their manifests, resume invariants,
  and hashing-inclusive throughput have not been derived or tested.
- **Residual risk:** A022 remains untested. Exact hashing and weak-registry
  validation may still make the frozen workload too slow or memory-intensive,
  and no serialized checkpoint can yet regain in-memory authority. The
  favorable 95% proxy-reliability calibration remains a substantive conditional
  assumption rather than a market fact.
- **Reopen if:** A public path can fit unissued/mislabeled content, any focused
  hostile regression fails, or the later checkpoint/resource design requires
  weakening the admitted provenance boundary.

## D0070 — Separate reusable design identity from response authority

- **Date:** 2026-07-16
- **Diagnosis:** `_design_sha256` consumed `_receipt_payload`, which includes
  the structural target, recovery flag, reliability, and response-content
  digest. Two designs with the same filtered base and byte-identical `X0`
  therefore hashed differently across response cells. This contradicted the
  derived response-independent design identity and would make a shared base
  checkpoint/cache depend on an incidental response anchor.
- **Decision:** Hash only the filtered-base identity for contract designs and a
  literal versioned analytic namespace for analytic designs. Continue to bind
  the full transformed-date receipt inside weak issuance tokens and cell
  response receipts. Design equality and response authority remain separate
  objects with separate jobs.
- **Rejected:** Declare response-dependent design hashes intentional, because
  A008 and the derivation explicitly promised common-base cross-cell reuse; or
  remove response receipts from issuance, because that would reopen relabeling
  attacks fixed by C0006--C0011.
- **Residual risk:** Future checkpoint manifests must carry both the reusable
  source/design identity and the structural response identity explicitly. A
  single overloaded digest would recreate this defect.
- **Reopen if:** Identical `X0` on one filtered base hashes differently across
  cells, or different filtered bases can collide under the design identity.

## D0071 — Reaccept the estimator core only after C0014 and final re-audit

- **Date:** 2026-07-16
- **Diagnosis:** D0069 accepted the in-memory core after C0013, but final code
  review then found that `design_sha256` depended on the response receipt. The
  implementation therefore contradicted its own derived shared-design identity
  even though every estimator output and authority test was green.
- **Decision:** Treat D0069 and the eighth red-team verdict as reopened, not as
  final evidence. Accept the in-memory estimator core only after C0014's exact
  red mismatch, the response-independent design-digest repair, 49 focused
  tests, the 157-test repository gate, the complete 48-date issued-path smoke,
  and fresh mathematical, contract, code, ledger, and verification audits.
  Checkpoint loading, registered recovery, resource admission, validation, and
  research authority remain closed.
- **Rejected:** Call the digest mismatch documentation-only, because the digest
  is the future checkpoint/cache identity promised by A008; or broaden this
  acceptance to execution, because no serialized manifest or hashing-inclusive
  resource benchmark exists.
- **Residual risk:** A022 remains untested, no checkpoint loader can restore
  in-process authority, and the favorable 95% proxy reliability remains a
  conditional calibration rather than an identified market fact.
- **Reopen if:** A final repository check or hosted CI fails, a shared base can
  produce response-dependent design hashes again, or the checkpoint/resource
  design requires weakening the admitted provenance boundary.

## D0072 — Close the estimator-core slice on hosted parity evidence

- **Date:** 2026-07-16
- **Diagnosis:** Local acceptance alone does not satisfy the repository's CI
  contract or prove that the locked Linux test surface can reproduce the exact
  reviewed estimator-core revision.
- **Decision:** Close only the smooth estimator-core implementation slice at
  commit `5500611da123bdc1dedd2124b0f2fd26e04525db` after hosted CI run
  `29492765654` completed the parity job successfully in 31 seconds. Preserve
  checkpoint/recovery, resource, validation, and research as separate closed
  authority surfaces.
- **Rejected:** Begin checkpoint work before recording the hosted evidence, or
  treat hosted success as resource admission. CI exercises deterministic and
  test-seed software checks; it does not run the frozen throughput workload or
  any registered G2 stream.
- **Residual risk:** GitHub warned that two actions targeting Node.js 20 were
  forced onto Node.js 24. This is a CI-maintenance warning, not a failed parity
  step or scientific result; update action versions in a separately verified
  engineering change rather than mixing it into this acceptance record.
- **Reopen if:** The hosted run is invalidated, the committed revision cannot be
  reproduced locally, or later checkpoint/resource work requires weakening the
  exact provenance and design-identity contracts.

## D0073 — Make the checkpoint trust boundary explicit before writing a loader

- **Date:** 2026-07-16
- **Diagnosis:** A manifest plus unkeyed hashes can prove byte consistency but
  cannot prove that a writable local artifact originated in the licensed
  in-memory issuance chain. Any same-user actor who can replace the payload can
  also recompute every SHA256. More hashes would disguise, not solve, that
  impossibility. Full upstream replay would prove origin but erase checkpoint
  savings and invalidate the frozen resource measurement.
- **Decision:** Treat the local writer process and checkpoint directory as the
  trusted origin boundary. Defend rigorously against crash/torn publication,
  stale source/runtime/config, mixed artifacts, malformed schemas, accidental
  corruption, ordinary substitution, relabeling, and hash-then-reopen races.
  State explicitly that coordinated same-user recomputation is out of scope.
  Persist separate complete base and cell date panels, use exact NPY files,
  validate one in-memory snapshot of every file, and restore authority only in
  exact stage-specific loaders with inline registry writes.
- **Rejected:** Claim content hashes authenticate origin; embed a private key in
  source; depend on an external signing service; replay all RNG/PCA/moment work
  at load; serialize only the aggregate; or expose a generic decoded-object
  registrar.
- **Residual risk:** A malicious actor with write access to the checkpoint tree
  and execution ability can forge a self-consistent artifact. This limitation
  must remain prominent. A022 must still measure actual hash/I/O/issuance cost.
- **Reopen if:** A defensible external trust anchor becomes available, the
  checkpoint directory cannot be treated as trusted, a loader hashes different
  bytes from those it decodes, or bootstrap execution requires a different
  artifact granularity.

## D0074 — Reject the first checkpoint test shape before codec implementation

- **Date:** 2026-07-16
- **Diagnosis:** The first red suite correctly failed because the loader module
  did not exist, but hostile pre-code review found that its positive contract
  was internally inconsistent. It pytest-collected the one-shot seed-9191
  recovery, called a draw-capable namespace “without RNG,” accepted a
  caller-selected design anchor, did not validate writer issuance or the
  referenced base artifact, and left the exact manifest, success hash, global
  allocation lock, import binding, timeout, and RSS evidence underspecified.
- **Decision:** Keep the missing-module red as evidence, then rewrite the
  contract and tests before codec code. Ordinary checkpoint tests use only seed
  1729 and a true target-16-design/target-0-response cross-cell. Seed 9191 moves
  to one dedicated success-last CLI after deterministic green. Writers and
  loaders require exact test authority, exact live panel issuance, internally
  derived design identity, stable source/runtime/import identity, a root-wide
  lock, immutable publication, and exact byte/hash recovery. The fresh-process
  claim is narrowed to no RNG draws or upstream replay.
- **Rejected:** Treat test collection order as a one-shot gate; use fake
  telemetry; let an equality-compatible panel become a checkpoint; accept an
  evidence dataclass without revalidating its on-disk base artifact; or start
  coding while the serialized protocol remained ambiguous.
- **Residual risk:** Content hashes still do not authenticate origin against a
  coordinated same-user rewrite. The one-shot runner and full hostile suite
  remain unexecuted until the deterministic codec is green.
- **Reopen if:** Seed 9191 enters ordinary pytest, a writer can serialize an
  unissued panel, a loader draws or replays upstream data, or the 2 GB cap can
  race across coordinates.

## D0075 — Consume A019 only from an accepted clean checkpoint revision

- **Date:** 2026-07-16
- **Diagnosis:** `attempt.json` makes the seed-9191 recovery intentionally
  non-rerunnable. Running it from a dirty or locally unverified checkpoint
  implementation would turn an ordinary software defect into an irreversible
  loss of the sole recovery attempt. The earlier prediction named wall/RSS
  stops but did not fully specify process-tree accounting or the failure
  receipt.
- **Decision:** Freeze the exact supervisor/worker state machine and receipt
  schemas before runner code. The public command has no seed/date overrides,
  requires a clean declared source snapshot and all six numerical thread
  variables fixed at one, and is eligible only after deterministic local
  checks, hostile review, a committed revision, and hosted CI pass. Publish
  `attempt.json` before spawning the one claimed worker; poll the complete
  worker process tree; publish either success-last result evidence or an
  immutable failure receipt; never retry.
- **Rejected:** Treat a local green test as enough for an irreversible run;
  monitor only the direct worker PID; let the worker choose an address; delete
  a failed attempt; or interpret sampled RSS as proof that no sub-poll spike
  occurred.
- **Residual risk:** A power loss can leave only `attempt.json`, and sampled
  RSS can miss a shorter transient peak. Both limitations are explicit; the
  former consumes A019 and the latter narrows the resource claim to observed
  process-tree samples.
- **Reopen if:** Hosted deterministic verification fails, the public runner
  exposes address overrides, a second worker can draw after the claim exists,
  or the supervisor cannot terminate the complete process group at a hard
  stop.

## D0076 — Treat disk-cap admission and load/write exclusion as pre-mutation invariants

- **Date:** 2026-07-27
- **Diagnosis:** The first apparently green checkpoint codec enforced the
  2 GiB root cap only after creating its writer marker and created prefix/stage
  directories before reserving them. Exact sparse-tree probes reached
  2,147,483,742 logical bytes during marker creation and 2,147,483,679 bytes
  after a reservation that omitted logical directory growth: 94 and 31 bytes
  above the sealed cap. Separately, loaders checked the durable marker before
  decoding but could return newly issued panel authority after a cooperating
  writer appeared later.
- **Decision:** Take a nonblocking exclusive advisory lease on the pinned root
  directory for every writer and a shared lease for the complete
  decode/reconstruct/registry-issuance interval. Keep the create-exclusive
  marker as crash evidence, not as the live mutual-exclusion primitive.
  Conservatively reserve marker bytes and entry growth before the first
  mutation; reserve all missing prefixes, the stage, file entries, payloads,
  and rename slack before directory creation; repeat remaining-stage
  admission; and check actual logical and allocated usage after every
  mutation. Final marker checks remain defense against uncoordinated local
  mutation.
- **Rejected:** Keep a marker-only protocol with one final check; count only
  payload bytes; create directories and then decide whether they fit; or call a
  post-write cap exception compliance. Each alternative permits the forbidden
  transient state even if cleanup later succeeds.
- **Evidence:** All three original hostile probes failed before repair. The
  repaired exact one-byte-below-cap test refuses before even the marker write,
  the directory-growth reservation refuses the previously admitted payload,
  an injected late marker returns no authority, and a live shared reader lease
  blocks the cooperating writer through issuance. The complete checkpoint
  suite passes 85 tests.
- **Residual risk:** Advisory locks require cooperating processes. A
  coordinated same-user actor can ignore them and can forge content under
  A024's explicit trusted-origin boundary. The final marker checks detect the
  tested uncoordinated appearance but are not a cryptographic trust root.
- **Reopen if:** Any mutation can transiently exceed the root cap, a writer can
  acquire its lease while loaded authority is being minted, a handled failure
  leaks a kernel descriptor, or the target filesystem does not support the
  tested directory-descriptor `flock` semantics.

## D0077 — Make private recovery roles capabilities, not alternate public CLIs

- **Date:** 2026-07-27
- **Diagnosis:** The first A019 supervisor let `_worker` and `_fresh` accept
  arbitrary serialized roots and labels, so a direct child invocation could
  bypass the canonical public supervisor. The primary worker also trusted only
  the parent's earlier source/runtime preflight, allowing a later identity
  change to reach the panel construction. Follow-on fault injection showed
  that an interrupted create-exclusive evidence write exposed a partial final
  file and that an exited leader could leave descendants without process-group
  cleanup.
- **Decision:** Make the public surface the exact Make target only. Bind every
  private child to a one-shot inherited FIFO capability carrying its role,
  immediate parent PID, immutable attempt digest, and exact internal-spec
  digest; require the canonical scratch path before reading the spec. Require
  exact public repository/result/checkpoint/scratch roots, keep every bytecode
  prefix below the scratch root, and re-inspect live source/runtime/clean-state
  against `attempt.json` before the worker claim or any draw and again for the
  fresh reload. Publish evidence by fsynced staging plus no-overwrite hard link,
  and detect/terminate a surviving process group even after its leader exits.
- **Rejected:** Rely on underscore-prefixed CLI names; let a private child
  select its roots; accept source/runtime verification only in the parent;
  write final evidence in place; or stop monitoring once the leader PID exits.
  These are naming conventions or happy-path behavior, not one-shot authority.
- **Evidence:** Six initial capability/path/identity tests and two later
  evidence/process-group tests failed before their respective repairs. The
  final seed-1729-only supervisor suite passes 15 tests in 3.39 seconds,
  including an exact fresh-process zero-draw round trip. Targeted Ruff, format,
  and mypy pass; `make -n g2-checkpoint-recovery` confirms the fixed launcher
  without executing it.
- **Residual risk:** The inherited pipe and Make marker prevent ordinary or
  accidental alternate invocation; they cannot defeat a coordinated same-user
  actor inside A024's excluded threat model. Process-tree RSS is sampled every
  50 ms and may miss a shorter spike, exactly as preregistered.
- **Reopen if:** A child can read an arbitrary spec without the one-shot
  capability, any identity mismatch reaches the claim or first draw, a partial
  final receipt becomes visible, a descendant survives a stop, or any public
  address/path override appears.

## D0078 — Make one-shot recovery fail closed under compound host faults

- **Date:** 2026-07-27
- **Diagnosis:** Hostile closeout found five gaps after the earlier 15-test
  recovery suite was green. A symlinked ancestor admitted filesystem mutation
  before later child rejection; a group reported alive after `SIGKILL` was
  treated as gone; a named FIFO could replay the child payload twice; an
  unexpected sampler exception escaped without teardown; and one
  post-link directory-fsync fault produced both `_SUCCESS` and `_FAILURE`.
  Five focused regressions failed together before repair. A sixth compound
  probe then exercised failed success-link fsync, failed retry, and failed
  rollback fsync.
- **Decision:** Require absolute canonical identity for every root before
  mutation and strict identity after creation. Attest child descriptors as
  anonymous Darwin kernel pipes or exact Linux `/proc` pipe identities and
  reject unsupported platforms. Bracket every successful `Popen` with
  unconditional process-group cleanup; require post-`SIGKILL` disappearance
  or raise. Retry the final-link directory durability barrier once, otherwise
  durably roll back; if rollback durability is uncertain, publish no opposite
  terminal outcome. Refuse failure publication while success is visible.
- **Rejected:** Treat a final-component `lstat` as path canonicality; assume
  `SIGKILL` success from the syscall return; call every FIFO one-shot; clean up
  only named monitor failures; suppress directory-fsync errors; or let an
  uncertain rollback become a failure receipt. Each can consume or contradict
  the sole A019 attempt.
- **Evidence:** The five original probes failed together, then passed 5/5
  after repair. The three-fsync compound probe leaves `attempt.json` present
  with neither terminal marker. The seed-1729 recovery suite passes 21 tests,
  the checkpoint/recovery surface passes 106 tests, and the complete locked
  repository gate passes Ruff, format, strict mypy over 22 source files, all
  263 tests, deterministic demo, and committed-result drift. Seed 9191 and all
  registered G2 streams remain unrun.
- **Residual risk:** Path checks are same-process preflight, not protection
  against a coordinated same-user actor racing every pathname operation.
  Anonymous endpoint attestation prevents named replay but is not a secret
  against a same-user process that can execute project code. Power loss can
  leave a consumed attempt without a terminal marker, and sampled RSS can miss
  a sub-50-ms peak.
- **Reopen if:** Any alias reaches mutation, a named endpoint reaches payload
  parsing, supervision exits while its group remains, both terminal markers
  can coexist, Linux hosted CI rejects the anonymous-pipe predicate, or an
  uncertain publication emits the opposite terminal outcome.

## D0079 — Put pre-import launch and cleanup exceptions inside the authority boundary

- **Date:** 2026-07-28
- **Diagnosis:** The first compound repair still left two authority surfaces
  outside its model. Make accepted a command-line bootstrap override and
  followed a symlinked `data` ancestor before Python preflight. Separately,
  stage cleanup could replace `_PublicationStateUncertain`: first through
  `OSError`, then through an asynchronous `KeyboardInterrupt`. In each cleanup
  case the supervisor could publish `_FAILURE` although the earlier `_SUCCESS`
  unlink was not durably established. Three Make/cleanup tests and the later
  interrupt variant were recorded red before repair.
- **Decision:** Freeze the recovery bootstrap path and six-thread environment
  with Make `override :=` constants. Test every literal path component for a
  symlink before the pre-import `mkdir`, with Python retaining an independent
  canonical post-creation check. In `_exclusive_write`, capture the primary
  publication outcome before cleanup. Suppress any cleanup `BaseException`
  only when an already-active publication uncertainty must retain precedence;
  otherwise preserve ordinary interrupt propagation.
- **Rejected:** Trust Python to reject a mutation Make already made; leave
  research-critical Make variables caller-overridable; suppress only ordinary
  filesystem exceptions; suppress every cleanup interrupt unconditionally; or
  allow cleanup exception type to choose whether opposite terminal evidence is
  legal.
- **Evidence:** The override dry-run emits only the canonical path/thread
  contract. A copied Make surface with `data` symlinked outside fails with the
  outside directory still empty. Three fsync faults plus either stage-cleanup
  `OSError` or `KeyboardInterrupt` leave a consumed attempt with neither
  terminal marker nor failure receipt, while the no-uncertainty interrupt
  control propagates. Recovery passes 26 tests; checkpoint plus recovery passes
  111 tests; the complete locked gate passes Ruff, format, strict mypy over 22
  source files, all 268 tests, deterministic demo, and committed-result drift.
  Seed 9191 and all registered G2 streams remain unrun.
- **Residual risk:** Separate Make shell checks cannot defeat a coordinated
  same-user actor racing components between checks and `mkdir`; A024 excludes
  that threat. A power loss may still leave only the authoritative consumed
  attempt, and Linux anonymous-pipe attestation still needs hosted execution
  on the committed candidate.
- **Reopen if:** Any Make assignment redirects the public address or thread
  contract, a symlinked ancestor is mutated before rejection, cleanup masks an
  active uncertainty, an ordinary interrupt is silently swallowed without
  uncertainty, hosted Linux rejects its exact pipe identity, or both terminal
  markers can coexist.

## D0080 — Bind the launcher and report the address actually drawn

- **Date:** 2026-07-28
- **Diagnosis:** Final closeout found two evidence-identity defects after the
  recovery behavior itself was green. First, the root `Makefile` had become the
  sole public constructor of the frozen A019 environment, but the declared
  execution-source snapshot still covered only six Python/config/runtime paths.
  A changed launcher could therefore remain outside both the source digest and
  clean-source predicate. Second, the seed-1729/48-date smoke reported
  `VALIDATION_RECOVERY` phase/scenario `23/0` in its spec and terminal receipt
  while a private helper actually drew `VALIDATION_DATE_FRONTIER` `22/2`.
  Calling the procedure a recovery did not license relabeling its RNG address.
- **Decision:** Make the root `Makefile` the seventh declared source path and
  bind its exact mode, bytes, size, and digest into every checkpoint/recovery
  source identity. Freeze test-mode specs to
  `VALIDATION_DATE_FRONTIER` and public mode to `VALIDATION_RECOVERY`; delete
  the substitution helper and use `spec.stream` for expectations, draws,
  attempt evidence, checkpoint receipts, and terminal results. A019 remains
  exactly seed 9191, 252 dates, `VALIDATION_RECOVERY`, phase/scenario `23/0`,
  outside pytest.
- **Rejected:** Treat the Make recipe as deployment scaffolding outside the
  scientific source boundary; infer the draw address from a private helper
  while printing a different public label; or silently change the seed-1729
  draw to match its old receipt. The first leaves authority construction
  unhashed, the second makes evidence false, and the third would consume a new
  stochastic input instead of correcting the record.
- **Evidence:** A behavioral source-enumeration test observes `Makefile` and a
  byte-altered launcher changes the source snapshot. The exact seed-1729
  supervisor round trip now reports date-frontier `22/2` from spec through
  result while retaining zero draws in the fresh reload. Checkpoint passes 86
  tests, recovery passes 26, the combined surface passes 112, and the complete
  locked gate passes Ruff, format, strict mypy over 22 source files, all 269
  tests, deterministic demo, and committed-result drift. No A019 artifact or
  registered G2 realization was opened.
- **Chronology limitation:** The live session recorded the A020 prediction,
  failing omission test, and repair in that order, but no immutable
  repository-local red log preserves it. The worktree was still uncommitted,
  later A021 edits changed relevant mtimes, and current mtimes are therefore
  non-probative. A020 receives a qualified deterministic-closeout pass, not an
  independently git-verifiable chronology pass. Future authority repairs must
  commit, or otherwise preserve immutable, the prediction and red evidence
  before implementation.
- **Residual risk:** A024 still excludes coordinated same-user source or
  checkpoint forgery. Linux anonymous-pipe attestation remains a hosted-CI
  prerequisite, sampled RSS may miss a sub-50-ms peak, and power loss can
  consume A019 with only `attempt.json`.
- **Reopen if:** Any launcher byte can change without changing source identity,
  any test receipt differs from the address actually drawn, pytest can
  instantiate the exact A019 tuple, hosted Linux rejects the anonymous-pipe
  predicate, or the chronology qualification is presented as stronger evidence
  than the repository contains.

## D0081 — Preserve A019 when external safety authority requires explicit consent

- **Date:** 2026-07-28
- **Diagnosis:** Exact commit
  `5aca8111540064b9449ef55a806427795cb800bd` passed hosted CI run
  `30349473867`, satisfying the deterministic and Linux parity prerequisites.
  A first non-mutating eligibility shell used zsh's reserved `path` variable as
  a loop name and consequently erased that subprocess's `PATH`; it stopped at
  `make -n` with `command not found`, before any mutation or A019 command. The
  corrected preflight then proved clean HEAD, matching hosted SHA, absent
  canonical roots, and the exact dry-run command. Submission of
  `make g2-checkpoint-recovery` was rejected before process creation by the
  external safety gate because the user had not explicitly authorized this
  exact irreversible one-shot.
- **Decision:** Treat the safety rejection as an authority boundary, not a
  software failure or consumed attempt. Preserve the clean hosted-green state,
  record that no A019 path exists, and require explicit user authorization
  before submitting the exact Make command again. Never use an indirect
  invocation or alternate tool to evade the gate.
- **Rejected:** Interpret the general instruction to proceed as sufficient
  external consent; execute the private supervisor directly; alter the command
  shape; or call the rejected submission an A019 attempt. The safety reviewer
  explicitly forbade workarounds, and no A019 process or state was created.
- **Evidence:** Hosted job `90243303390` completed all steps successfully in
  1 minute 22 seconds. Immediately after the rejected submission, git remained
  clean and `results/g2_checkpoint_recovery`,
  `data/g2_checkpoint_recovery/checkpoints`, and
  `data/g2_checkpoint_recovery/scratch` were all absent. Seed 9191 and every
  registered stream remain unaccessed.
- **Residual risk:** A019 is now blocked on explicit human consent rather than
  code or CI. Once consent is supplied, a fresh non-mutating eligibility check
  is still required because repository or hosted state may have changed.
- **Reopen if:** Any canonical root appears before explicit consent, the
  approved command differs from the exact Make target, HEAD or hosted evidence
  changes, or anyone attempts to bypass the external safety decision.

## D0082 — Accept the sole A019 outcome as software-recovery evidence only

- **Date:** 2026-07-28
- **Diagnosis:** The user explicitly authorized the exact irreversible
  `make g2-checkpoint-recovery` command, consuming A019 seed `9191` once with
  no retry. A fresh read-only preflight immediately before execution proved a
  clean worktree at `a75ea69d85c5425bd5fe824361869c3a7edb55e7`,
  successful hosted run `30350204001` on that exact SHA, absent canonical
  result/checkpoint/scratch roots, and the fixed Make-only launcher. The
  single public command and its supervised process tree then exited zero.
- **Decision:** Treat `attempt.json` as irreversible consumption of A019 and
  accept the terminal outcome as a pass of C0015's software-recovery claim
  only. Preserve the result and success receipt, never retry seed `9191`, and
  move next to a derived and pre-recorded A022 resource benchmark. Do not
  interpret exact coefficient replay as recovery of structural truth, G2
  premise passage, resource admission, or permission for a registered
  resource/validation/research realization.
- **Rejected:** Rerun A019 to demonstrate repeatability; widen or reinterpret
  the frozen address; compare these coefficients with truth after seeing them;
  discard the scratch evidence; or count the three coefficient hashes as
  scientific trials. Each would violate the one-shot or software-only
  preregistration.
- **Evidence:** Attempt SHA256
  `18c70c205ad75d608ad0dc70f3c9873df96d2a636f351b22411599889ddb01c1`
  binds seed `9191`, `VALIDATION_RECOVERY`, 252 dates, panel 0,
  design/response targets 16/0, and phase/scenario `23/0`. The immutable result
  passed in 18.907810209 seconds at 178,864,128 bytes peak RSS; allocated
  checkpoint size was 9,183,232 bytes. These use 15.76%, 11.11%, and 72.98%
  of the 120-second, 1.5-GiB, and 12-MiB hard stops. Actual manifest and NPY
  SHA256 values match both checkpoint `_SUCCESS` receipts. Before/after array,
  receipt, design-digest, and all three coefficient hashes match exactly; a
  fresh process reproduced all three coefficient hashes with
  `fresh_process_rng_draw_count=0`. Result SHA256
  `7061e9d5a734115cadad728e262eceb177d5eddb9f1cb6391a1f81aa040e7a3c`
  matches the terminal `_SUCCESS`; no failure marker exists.
- **Hosted closeout:** Evidence commit
  `e328a33f0792ff81c8a0a3e6d54b7ad0a7563f7e` passed hosted CI run
  `30386325383`; the parity job completed in 1 minute 19 seconds with every
  required step green. The only annotation is the pre-existing Node 20 action
  deprecation warning.
- **Residual risk:** A019 validates one same-machine recovery at the frozen
  address. It does not test A022 throughput, statistical bias, power, or the
  premise. The 50-ms process-tree sampler can miss shorter RSS spikes, and
  A024 still excludes coordinated same-user checkpoint/source forgery because
  the evidence has no external signing root.
- **Reopen if:** Any second A019 attempt is executed, a failure marker appears,
  a committed byte fails its recorded digest, later prose upgrades the result
  to a coefficient-truth claim, or A022/resource authority is inferred without
  its own derivation, prediction, and stop rules.

## D0083 — Derive an operand-complete A022 before implementing the resource runner

- **Date:** 2026-07-28
- **Diagnosis:** The frozen fourteen-kernel work matrix is meaningful, but its
  old one-unit benchmark bundle is not executable: one date cannot honestly
  produce a 252-date base/cell artifact or paper cache, cheap operations may
  lie below timer resolution, equal-context rates need not transfer to the
  validation/research mixtures, and capability/artifact/resume/process/disk
  semantics were incomplete. These are design defects, not evidence that the
  M4 Air is inadequate. The diagnosis was written before method selection,
  code, or registered resource access.
- **Decision:** Append preregistration amendment A022 and freeze a complete
  engineering admission experiment before implementation. Preserve the
  fourteen kernels, full `W`, science, addresses, seeds, and budgets. Use
  fixed operand-complete cold/equal blocks; three non-adaptive seed-1729
  measurability rehearsals; contiguous registered panel claims from zero;
  600-second thermalization; exactly three warm blocks; total/phase
  stationarity and leave-one-block-out mixture transfer; slowest-context
  integer projection; a separate anonymous-pipe `ResourceRngNamespace`;
  byte-level artifact authority; PID/start plus `wait4` RSS evidence; and
  crash-persistent three-root disk/cumulative-time accounting.
- **Rejected:** Time private surrogate kernels; generate required operands
  outside the clock; adapt powers-of-two after timing; choose panel gaps after
  seeing registered durations; retain the old last-three rate as admission;
  let interrupted epochs erase adverse evidence; rename existing
  `base-panel`/`cell-panel` artifacts; or execute the resource seed before a
  quantitative prediction seal. Each alternative creates discretion or omits
  frozen production work.
- **Hostile-review evidence:** Two independent pre-code reviews both failed
  the first draft. They identified absent A022 preregistration authority,
  non-unique panel allocation, undefined held-out normalization, adaptive
  microbatch discretion, unnamed artifact schemas, erasable sampler gaps,
  incomplete process/disk accounting, and descriptive provenance. The repair
  makes panel claims contiguous, fixes `k7=4096`, removes all adaptive counts,
  defines exact indexed transfer arithmetic, makes live accounting gaps
  terminal, freezes source paths/resume clocks, and delegates bytes to
  `GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md`.
- **Residual risk:** Repeating one issued paper-date summary across a
  benchmark-only cache does not reproduce 252-date heterogeneity or a
  12-hour object-lifetime trajectory. A022 can therefore establish only
  conditional machine/runtime admission. Validation and research retain
  runtime reforecast and hard-stop authority.
- **Reopen if:** A fixed test subblock is below 100 ms, an exact artifact
  schema cannot fit the 5-MiB payload ceiling, hostile re-review fails, any
  implementation introduces data-dependent workload/address selection, or a
  registered resource/validation/research seed is accessed before the
  prediction seal and explicit one-shot authorization.

## D0084 — Keep A022 conditional and make every resource byte derivable

- **Date:** 2026-07-29
- **Diagnosis:** Fresh independent review found one methodological
  overstatement and six persistence ambiguities. A022's phase traces are not
  proportional to `W`; its same-phase held-out formula tests temporal
  stability, not full-mixture transfer. Exact proportional scaling is
  infeasible because unit kernel-14 work forces the full phase. Separately,
  the design omitted new-wrapper registry accounting, one rehearsal source
  identity, literal NPY headers, deterministic stage/debris bytes, retained
  rehearsal inventory rows, and exact disk mode/allocation-unit encodings.
- **Decision:** Append A023 without rewriting A022. Preserve every frozen
  trace vector and address. Rename the active claim as conditional per-kernel
  extrapolation, retain six same-phase temporal checks, and add 72
  opposite-phase per-kernel/aggregate robustness checks over kernels
  `1..10,14`. Count one ninth `_RESOURCE_ARTIFACT_REGISTRY`; bind all three
  rehearsal source identities while requiring only executable equality across
  stages; freeze a literal 118-byte NPY header, deterministic stage paths,
  complete debris/final digests, full rehearsal inventory rows, and exact
  no-follow disk/statvfs rows.
- **Rejected:** Relabel same-phase temporal prediction as mixture transfer;
  run a rounded five-percent workload trace that would consume roughly 60% of
  each phase across the minimum warm blocks; reduce validation fits below the
  mandatory 25-by-nine null-batch atom; or leave implementation to choose
  equivalent encodings. The first overclaims evidence, the middle alternatives
  violate budget/artifact contracts, and the last restores discretion.
- **Residual risk:** Passing temporal and cross-context checks cannot validate
  linear scaling to `W`, excluded kernels 11--13, heterogeneous 252-date cache
  lifetime, or a future 12-hour thermal path. Assumption A026 remains explicitly
  untested; validation and research reforecast/hard stops remain binding.
- **Reopen if:** Any active document calls A022 a measured full-mixture
  guarantee, a registry vector has other than nine positions, rehearsal omits
  a source identity or full inventory rows, a byte can have two valid
  encodings, hostile re-review fails, or any A022/registered seed runs before
  the corrected package is accepted.

Historical unqualified `A024` references in D0076--D0082 denote assumption
A024, the trusted-origin assumption. `Amendment A024` denotes the independent
preregistration restartability correction below.

## D0085 — Make A022 restartable without preserving raw statistical state

- **Date:** 2026-07-29
- **Diagnosis:** Recovery review rejected the A023-corrected package before
  implementation or rehearsal. A durable boundary after k1 could not supply
  k2's required live raw/design/PCA operands, while k8 named k9/k10 artifact
  parents before those artifacts existed. Further hostile review found
  resettable trace/replay evidence, unchained supervisor loss, incomplete RNG
  upper digests and accounting anchors, and destructive terminal-failure
  cleanup before an outcome-selection journal.
- **Decision:** Append amendment A024. Freeze receipt order
  `k1,k2,k3,k4,k5,k6,k7,k9,k10,k8,k11,k12,k13-recovery,k13-research,k14`;
  make k1+k2 one timed indivisible epoch with one non-durable internal
  accounting cutoff; and persist only resume panels, weights, and focal
  outputs. Recompute aggregates through the same ordinary/resume path. Journal
  every last-use cleanup; publish 15 canonical boundary leaves plus four
  cleanup intents per rehearsal trace; delete and bind uncommitted artifact
  finals before replay; carry the full trace prefix through chained
  interruptions; and charge one lost first-epoch ordinal fully to both
  eventual records while counting physical elapsed once. Before destructive
  terminal cleanup, publish an immutable failure intent whose resumable suffix
  cannot reopen work or select a different outcome.
- **Rejected:** Persist raw normals, `X0`, PCA, aggregates, or fit objects;
  redraw RNG; retain a durable k1-only boundary; run k8 before k9/k10; treat an
  uncommitted final as timed evidence; reset replay on a clean continuation; or
  delete terminal artifacts before durably selecting failure. Each alternative
  either breaks restartability, adds scientific state, or permits
  interruption/outcome selection.
- **Evidence:** The corrected config freezes 15 record positions, 45 rehearsal
  boundary leaves, 12 cleanup intents, and 57 checkpoint intervals. Its current
  exact ASCII bytes and parsed type tree reproduce the hashes recorded in the
  artifact authority. The first hostile A024 pass failed nine concrete state
  transitions; the draft now addresses each. No test-seed rehearsal,
  registered resource namespace, validation/research stream, empirical data,
  or holdout was accessed.
- **Residual risk:** Resume I/O, deterministic reconstruction, cleanup journals,
  terminal-failure closure, and added receipt validation may themselves fail
  the resource budget. The repaired A024 package still requires two fresh
  hostile passes, the locked local suite, and hosted CI; no rehearsal has run.
- **Reopen if:** Any consumer bypasses the resume artifacts, an aggregate
  crosses a boundary, a clean/chained interruption changes the pending replay
  count incorrectly, a terminal-cleanup crash can change outcome, config bytes
  drift without a new freeze, hostile review fails, or any registered stream is
  accessed before the later quantitative seal and explicit authorization.

## D0086 — Close A024's remaining state-machine branches with finite A025 authority

- **Date:** 2026-07-29
- **Diagnosis:** Three fresh independent hostile reviews attacked the
  A024-corrected package before code and all failed it. Ordinary receipt stages
  could be misclassified as debris; whole-leaf cleanup could not checkpoint a
  child unlink; terminal cleanup lacked a final durable checkpoint and exact
  clock; process-death bytes, reservation ancestry, and post-interruption
  thermal state were underdetermined; lost-supervisor telemetry could be
  erased; terminal evidence had no finite root-JSON liveness bound; the paper
  bootstrap weights had no durable lifecycle; and terminal success had no
  bounded interval.
- **Decision:** Append amendment A025 without changing A022--A024's seeds,
  addresses, record order, numerical kernels, work matrix, estimators,
  thresholds, budgets, or conditional interpretation. Freeze exact successful
  RNG call sequences; one role-resolved paper-bootstrap-weight artifact; seven
  resume-state rows; idempotent ordinary receipt-stage adoption; entry-level
  child-before-parent cleanup/debris prefixes; at least one contiguous
  failure-resume checkpoint including an exact final cleanup receipt; exact
  process-death nullability and ordering; immutable reservation-creator
  ancestry; mandatory thermal requalification after interruption; fail-closed
  unknown-loss telemetry; finite worker/interruption/trace/path/row envelopes;
  category-contiguous failure prefixes; and one fixed terminal-success
  accounting row whose visible-directory existence attests the later final
  seal without claiming an end-to-end latency bound. The successful
  three-panel rehearsal therefore retains exactly 13
  artifact kinds and 51 artifact rows and contains 45 canonical boundaries,
  12 cleanup intents, 57 capped ordinary checkpoint intervals, and one terminal
  accounting row, for 58 resource-accounting rows total.
- **Rejected:** Treat a valid receipt stage as disposable debris; record
  cleanup only at whole-target granularity; allow a zero-checkpoint or
  unbounded terminal suffix; infer current-worker equality by rewriting the
  original reservation; preserve favorable telemetry across an unclosed
  process segment; reuse pre-interruption thermal qualification; redraw paper
  bootstrap weights; or let count/path growth widen a root receipt beyond 1
  MiB. Each alternative restores crash-, identity-, evidence-, or
  timing-selected discretion.
- **Evidence:** The A025 authority freezes the seven-row, 13-kind,
  51-artifact, and 58-resource-accounting-row counts. The amended config
  recomputed at the A025 freeze to 9,061 bytes, SHA256
  `1a196dc09b9fdee9b9df6389d44b43bf24f10cd07cfef0140a6696ebcb1ec9fe`,
  184 type rows, and type-tree SHA256
  `838f74d41bd4f553bd5c01dceebe279de0ed7fa998d88ba0cff510e470a40df6`;
  fresh independent verification remains required and these values are not
  acceptance evidence. D0085's 57-interval value is retained only as the
  historical A024 boundary that A025 supersedes. A025 was derived from
  source/document inspection and deterministic byte/count calculations only.
  No implementation, test-seed rehearsal, registered resource command,
  registered resource/validation/research seed, empirical data, evaluation
  data, or holdout was accessed.
- **Residual risk:** A025 is a response to failed reviews, not acceptance.
  Receipt recovery, entry-level deletion, chained failure checkpoints,
  telemetry closure, and finite evidence encoding may still be internally
  inconsistent or exceed the resource budget. Fresh independent methods,
  systems, and schema reviews, then the locked deterministic suite and hosted
  CI, remain mandatory before test-seed implementation.
- **Reopen if:** Any A025 byte/count differs across active documents, an
  ordinary stage has more than one transition, cleanup progress can skip an
  entry, a failure or success suffix can exceed its clock/size bound, a
  reservation loses its original-claim ancestry, unknown-loss telemetry can
  pass admission, a fresh hostile review fails, or implementation/rehearsal/
  registered access occurs before the required reviews and design seal.

## D0087 — Close A025's interruption and consumed-terminal dead ends with A026

- **Date:** 2026-08-06
- **Diagnosis:** Fresh independent A025 review produced one schema pass and two
  blocking verdicts. Methods review found that interruption inside a
  rate-bearing trace could alter thermal state while the resumed suffix still
  entered admission. Systems review found a same-boot launch-only state and a
  post-terminal-entry state that consumed the attempt while authorizing no
  terminal close. These were deterministic design failures before code or RNG.
- **Decision:** Append amendment A026 without changing any scientific address,
  kernel, estimator, threshold, budget, artifact shape, or successful-
  rehearsal count. An interruption inside a rate-bearing trace now selects
  terminal failure and excludes the trace from every rate operand; only
  between-trace recovery may continue after a fresh uninterrupted 600-second
  thermal cycle. Each launch intent now atomically binds a stable inherited
  Darwin `flock` lease; after supervisor death, fresh acquisition of the same
  inode proves launch quiescence under a frozen no-unlock/no-dup/no-pass/no-
  descendant discipline and selects pre-RNG failure. An uncertifiable exact
  success/failure terminal-entry state now closes only through an immutable
  lock-bearing nonpass intent and successor-rebuildable
  `terminal/nonpass/{nonpass.json,_NONPASS}` with admission and retry both
  false.
- **Rejected:** Let a suspended timing trace complete; discard and replace an
  interrupted trace; treat `flock` alone as child-death evidence; infer
  quiescence from PID absence; let a successor certify the originally selected
  success/failure; retry either terminal Git check; or leave a consumed exact
  terminal-entry state without a durable outcome. These alternatives permit
  timing selection, process ambiguity, outcome switching, or an unbounded
  consumed state.
- **Evidence:** Primary Darwin documentation and XNU source agree that
  `fork`/`dup` references share the open-file-object lock, a separate
  nonblocking exclusive acquisition fails while an incompatible holder
  remains, and final close releases the lock. The amended config independently
  recomputes to 9,799 ASCII bytes, SHA256
  `3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
  194 leaf-type rows, and type-tree SHA256
  `e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.
  Successful rehearsal remains `3/45/12/57+1/58/13/51/7`. No implementation,
  rehearsal, registered command, registered seed, external data, or holdout
  was accessed.
- **Residual risk:** The lease is valid only under exact descriptor discipline
  and a local filesystem supporting Darwin `flock`; it proves quiescence, not
  PID death. Nonpass publication needs exhaustive repeated-successor crash and
  maximum-width fixtures. A026 is a response to failed review, not acceptance.
- **Reopen if:** A live/unknown lease holder can be bypassed, the lease inode or
  bytes can be substituted, any interrupted rate trace enters admission, a
  terminal-entry failure can retry Git/RNG or publish success/failure, nonpass
  bytes depend on successor-local state, config seals diverge, fresh review
  fails, or implementation/rehearsal begins before all required passes.

## D0088 — Accept A026 document authority after three independent review lanes

- **Date:** 2026-08-06
- **Decision:** Accept the settled A022--A026 derivation, preregistration,
  prediction, compute-plan, state-machine, artifact-authority, and byte-schema
  package as the sole document authority for later test-seed implementation.
  This decision does not accept the executable resource gate and does not
  authorize rehearsal or registered access.
- **Evidence:** Fresh methods review passed the rule that every interrupted
  rate-bearing trace selects terminal failure and contributes no admission
  operand, including the fresh 600-second between-trace recovery cycle. Fresh
  systems review passed the Darwin same-inode launch-quiescence lease and the
  deterministic successor-rebuildable terminal-nonpass state machine without
  RNG, capability, retry, or opposite-outcome leakage. Schema review initially
  failed because the recorded type-tree hash omitted the canonical CJSON LF,
  then failed one stale abbreviated prefix. After those clerical corrections,
  the third independent check passed: 9,799 ASCII config bytes, SHA256
  `3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
  194 leaf rows, 9,473 LF-terminated CJSON bytes, type-tree SHA256
  `e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`,
  and no stale prior-seal residue. The post-acceptance locked deterministic gate
  passed Ruff, format, strict mypy over 22 source files, all 269 tests, the
  deterministic demo, and committed-result drift. No implementation,
  rehearsal, registered command, registered seed, external data, or holdout
  was accessed.
- **Rejected:** Treat either failed schema check as a pass; change the CJSON
  definition to fit the wrong digest; conceal the stale prefix; or infer that
  document review licenses resource execution. Those alternatives would break
  the byte authority or cross a still-failed execution gate.
- **Residual risk:** Every accepted mechanism remains unimplemented. Descriptor
  discipline, crash-total publication, finite evidence envelopes, exact
  interval accounting, and successful-rehearsal counts require deterministic
  fixtures and later seed-1729 execution before any quantitative resource
  prediction can be sealed.
- **Reopen if:** Implementation cannot realize the exact document state
  machine, any authoritative byte or count drifts, a deterministic fixture
  exposes an unclassified transition, or a review/test failure is softened
  instead of recorded and repaired.

## D0089 — Project sealed paper-cache semantics without inventing representation order

- **Date:** 2026-08-06
- **Decision:** Extend `PaperReconstructionContract` only with the nine
  cache/aggregation fields already sealed in `configs/g2.toml`: coefficient,
  prediction, and bootstrap aggregation; exact-Boolean bootstrap refit;
  date-cache matrix and loss identities; reported coefficient and OOS counts;
  and cache-only fields. Validate both runtime types and exact sealed identity.
  This is semantic capability, not authority to assemble or serialize a paper
  cache.
- **Evidence:** The focused RED failed on the first missing contract attribute.
  The implementation then passed the two focused tests, all 10 G2 contract
  tests, Ruff, format, strict mypy, the full 306-test deterministic suite, the
  G0 demo, result-drift checks, and an independent read-only audit. Commit
  `916022bb2b76` records the implementation. No RNG, registered command,
  external data, or holdout was accessed.
- **Rejected:** Infer a flattening order, build a tiled resource fixture, or
  treat cache field names as a byte representation. The authority seals the
  meanings and counts but does not yet freeze the 8,460-field serialization
  order.
- **Residual risk:** Paper matrix assembly, per-date cache construction,
  serialization, bootstrap reaggregation, and the resource supervisor remain
  absent. A future representation choice could silently permute coefficients
  unless it is derived, frozen, and independently reviewed first.
- **Reopen if:** The projected values drift from the sealed config, a non-Boolean
  value is accepted for `bootstrap_refit`, a serializer appears before an exact
  order is authorized, or any registered stream is touched.

## D0090 — Distribute only a pre-results paper while G8 remains locked

- **Date:** 2026-08-06
- **Decision:** Maintain a paper-style README and an eight-page version-0.1
  preprint that report the G1 theorem and accepted known-truth result, then
  distinguish the registered but unrun G2 design from every later empirical,
  holdout, and economic claim. Identify Mehmet Demir Güven, Department of
  Computer Science, ETH Zürich, in the front matter. License only the
  manuscript, its LaTeX source, and original paper figures under CC BY 4.0;
  leave the repository's MIT software scope unchanged.
- **Evidence:** The compiled PDF contains the author and title metadata, renders
  to eight inspected pages, has no colored front-page status box or orphaned
  page, and contains one completed-evidence panel plus one explicitly analytic
  pre-run sensitivity panel. Independent prose and claim audits found no
  scientific overclaim or attribution trace after the ledger and license-scope
  repairs. The manuscript and README name the 306-test software gate as
  software evidence only.
- **Rejected:** Present the draft as the G8 final-results paper; report an unrun
  G2 quantity as evidence; claim market identification, performance, or
  profitability; pad the paper to a page target; or place the README and
  software under the preprint license.
- **Residual risk:** The preprint has no arXiv identifier and G2 remains open.
  A later arXiv license selection is irrevocable, and later venue requirements
  may require a different submission style. No submission or external upload
  is authorized by this decision.
- **Reopen if:** A caption loses its evidence label, G2/G8 status changes, an
  empirical or economic claim appears without a passed gate, the PDF artifact
  is missing, or the paper-license scope conflicts with a later venue policy.
