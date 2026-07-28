# G2 pre-run red-team memo

Date: 2026-07-15. This memo attacks the design boundary, not a result. No G2
implementation, benchmark, validation panel, or research draw existed when the
attacks were made.

## Initial verdict: fail, RNG forbidden

Three independent reviews rejected the first source-box design. Its eight
population projections were algebraically correct and feasible, but that did
not make the test scientifically admissible.

### Attack 1 — impossible power alternative

The design demanded 80% power for an estimator centered at exactly the strict
50% decision boundary. Such an estimator crosses that boundary only about half
the time. This was not a low-power implementation; it was an incoherent power
definition.

**Repair:** power now uses the actual least-favorable registered population
error. Passage additionally requires the margin beyond 50% to exceed three
bootstrap standard errors. The exact final procedure must pass a finite-sample
size/power license before the research seed exists.

### Attack 2 — adversarial estimand substitution

The first strengthened factor model mapped factor loadings back into original
flow units. With factor scores plus all residual flows, that response map is
just uncontrolled OLS. Treating it as the opponent's factor-purged cross-impact
coefficient mechanically reintroduced the common component the opponent meant
to remove.

**Repair:** the confirmatory regression uses an independent noisy proxy and
the direct coefficient on oracle `q`, which is comparable with `Lambda` without
an estimand switch. CCZ residual operators are compared only with their fair
projected target `Lambda P_perp`; response-equivalent maps are descriptive.

### Attack 3 — incompatible calibration collage

The first structural tuple combined one-minute equity OFI covariances, a
five-minute trade-sign propagator, one-second E-mini feedback, and an unsourced
AR(1) coefficient as though they were one calibrated market.

**Repair:** the confirmatory observable point uses the dimensionless one-minute
Capponi--Cont triple. `B = 0` isolates confounding and removes the cross-frequency
feedback bridge. The absolute diagonal and cross/own interval are explicitly
structural sensitivities, not one-minute estimates: the lower ratio is a
conservative round-down from Capponi--Cont's reduced-form mean and the upper is
motivated by Benzaquen. Hasbrouck--Seppi and Takahashi are nonconfirmatory
comparators. AR(1) `0.60` is labeled a dependence stress.

### Attack 4 — arbitrary eigenvectors and focal ordering

Fourier PC2/PC3 loadings made pair `(0,1)` depend on an unsourced asset order,
and raw eigenvalues from `N = 67` were reused at `N = 30` without preserving
shares.

**Repair:** the replacement covariance is permutation invariant with one
market spike and isotropic residuals. Every population off-diagonal is equal.
The focal serialization no longer selects a favorable pair.

### Attack 5 — underdefined opponent, bootstrap, RNG, and compute

The first config mixed paper block fits with pooled CV, promised preprocessing
refits that per-date scatters could not support, omitted a seed-key schedule,
claimed a studentized interval without an inner SE, and understated millions of
potential LASSO/CV refits.

**Repair:** two smooth confirmatory candidates use small sufficient statistics;
one receives the true homogeneous structure. Paper protocol reconstructions
are secondary and date-local. Exact key namespaces, bootstrap weights, batch
counts, storage arithmetic, and subphase budgets are frozen. Unsupported
studentization is removed.

## Strongest objection that remains

The redesigned positive claim is asymmetric. A 95%-reliable proxy is a strong,
favorable opponent, but its reliability and the real structural cross/own ratio
are not identified by the opened sources. Passing establishes a conditional
source-matched counterexample; it does not show that the real market lies in
that class or that confounding explains the literature. Conversely, failing at
95% reliability cannot kill the market premise because weaker proxies remain
source compatible.

No prose can repair that identification gap. The repository must keep the
claim conditional, publish the reliability frontier, and forbid a
premise-killing null unless a sharp upper bound over all source-compatible
latent decompositions/reliabilities also lies below 50% with adequate power.

## Second verdict: fail, RNG still forbidden

The second independent audit reproduced all 17 population targets, the
continuous least-favorable errors, the Schur/homogeneous estimands, and the
small-statistic storage arithmetic. It nevertheless rejected execution for
eight contract defects:

1. raw binary64 JSON was immutable but not independently byte-derivable;
2. stale wider-box feasibility values remained;
3. size used the distant `R = 1` recovery control rather than the 50% boundary;
4. marginal power did not license the probability that all 34 gate events pass;
5. RNG keys named fields without defining an executable namespace;
6. pooled homogeneous fitting and interval algorithms were underdefined;
7. the six CCZ reconstructions lacked an estimator table; and
8. the “exact” workload omitted 45,586,800 LASSO solutions and other mandatory
   branches.

No G2 implementation or registered random stream existed. The repair separates
raw and 12-decimal semantic seals, corrects feasibility evidence, stores both
candidate boundary roots, uses size-union and power-intersection superpanel
indicators, freezes the full RNG/interval algorithms, pools every homogeneous
row, specifies all six paper algorithms, and enumerates every mandatory fit.

## Fresh pre-implementation admission criteria

The replacement remains non-executable until a fresh hostile audit confirms:

1. raw-byte integrity and independent 12-decimal semantic regeneration both
   reproduce, including config/design/target schema identity and both critical
   reliability roots;
2. feasibility values and both continuous monotonicity proofs match an
   independent calculation;
3. both directly comparable confirmatory estimands, pooled homogeneous fit,
   and `R = 1` recovery targets are unambiguous;
4. candidate-boundary family size and actual-alternative joint power use the
   exact one-sided formulas, integer thresholds, and fit counts;
5. every stochastic draw has one frozen entropy vector, shape, index origin,
   CRN convention, and bootstrap-sharing rule;
6. the six-row CCZ reconstruction, PCA/CV/LASSO/OOS choices, 45,586,800 LASSO
   solutions, and all other mandatory branches are executable under the
   measured benchmark license; and
7. all living ledgers state the conditional positive scope and asymmetric null.

## Third verdict: fail, RNG still forbidden

The fresh math lane passed S0003's oracle algebra and both hashes, but the
inference and professor lanes rejected the design. This is the highest-value
failure so far: G2 could have passed without demonstrating failure of an
observable or published opponent.

1. **Oracle failure did not imply observable failure.** Multi-level measurement
   attenuation or regularization can cancel confounding. The measured
   integrated-OFI ridge is now a third binding candidate at all 17 cells. Its
   independently derived upper-endpoint error is still 135.85%, but its exact
   finite-sample PCA procedure must earn its own license.
2. **The published fit was nonbinding.** `CI_I` is now a binding veto at the
   primary observable point and upper structural endpoint. It is the only CCZ
   equation containing both integrated top-ten OFI and explicit off-diagonal
   coefficients. A separate full-`N`, full-`T` no-confounding recovery run is
   required before its research result.
3. **A boundary was mislabeled as composite size.** Population monotonicity
   does not order finite-sample bootstrap SEs or estimated-PC/ridge branches.
   The replacement evaluates 459 events on a frozen nine-node proxy-noise
   amplitude grid. This is called a null-grid calibration, never
   continuum-uniform size control.
4. **Bootstrap keys collided.** Parent scenario and date count were absent, so
   48-, 96-, and 252-date vectors could share a key. RNG key schema 2 gives
   parent phase, parent scenario, and `n_dates` dedicated entropy slots.
5. **The pooled fit omitted its intercept contract.** It now uses one global
   weighted intercept, global centering after date weights, no fixed effects,
   and an exact three-by-three solve from date cross-products.
6. **The paper path discarded changing loadings.** Each block now forms purged
   and full CC maps before averaging; the date cache also retains mean
   `P_perp`, so a weighted `Lambda P_perp` target is reconstructible.
7. **Fold-local `lambda_max` was not transferable.** CV now selects a common
   penalty-ratio index across fold-local paths and maps that ratio to the
   outer-training `lambda_max` for one zero-initialized final solve.
8. **The benchmark formula was not executable.** Fourteen kernels now receive
   a cold rate and a last-three-bundle warm rate after at least 600 seconds.
   Every exact workload maps to one kernel before the one-/12-/three-/16-hour
   expected-cap license can pass; hard limits are runtime stops only.

No implementation, benchmark, validation panel, or research RNG existed when
S0004 replaced S0003.

## S0004 pre-implementation admission criteria

S0004 remains non-executable until new independent lanes confirm:

1. config/design/target schema 3, raw SHA256
   `f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59`,
   semantic SHA256
   `f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`,
   and all three sets of 17 roots/targets reproduce independently;
2. observable measurement variance, recovery attenuation, continuous
   least-favorable proof, and wider-box feasibility are correct;
3. all 459 null-grid and 51 power events, one-sided formulas, exact counts, and
   the explicit non-uniform-size limitation agree across config and prose;
4. every stochastic draw has one collision-free 13-field key and exact shape,
   and the float64 AR-filter-first symmetric modal transform reproduces so CRN
   coupling is not left to a Cholesky/eigenvector choice;
5. the global pooled operator, fold-relative LASSO, `CI_I` veto/recovery, and
   nine-matrix paper cache are executable without hidden choices;
6. all 26,405,400 smooth validation fits, 15,195,600 recovery LASSO solutions,
   and 45,586,800 research LASSO solutions map to the fourteen-kernel benchmark
   through the frozen phase-by-kernel unit table, startup rule, and unequal-cache
   normalization, with projections inside every expected cap and the 16-hour
   total rather than merely below hard stops; and
7. every living ledger makes S0002/S0003 mechanically dead, keeps later gates
   locked, and states the asymmetric null honestly.

The review must also confirm that the declared amplitude/reliability gaps
(`0.015038828627620739` and `0.003307437435413063`) reproduce from all 51 roots,
that the published recovery retains the confirmatory collinear flow law, and
that every invalid numerical outcome fails rather than improves the validation
indicator.

## Fourth verdict: fail, contract repaired, RNG still forbidden

The first exact S0004 admission review did not pass. It reproduced the smooth
population economics, all 51 roots, both target-hash roles, finite-grid gaps,
critical values, fit counts, and memory arithmetic, but found defects that could
change or overstate the result:

1. the exact variance `547/39530` conflicted by 12 ULP with the raw target;
2. `CI_I` recovery used a zero cross truth, allowing a cross-erasing LASSO to
   look competent before being accused of bias against `0.0046`;
3. keys and marginal covariances did not freeze the symmetric modal CRN map;
4. fourteen kernel names did not supply the promised `W_phase,k` table;
5. LASSO preprocessing, coefficient reconstruction, KKT evaluation, and the
   best-level index still admitted different implementations; and
6. H1 shorthand risked attributing an integrated-OFI-plus-factor hybrid to a
   paper that publishes those ingredients only in separate equations.

A subsequent inference pass also found that two preprocessing clauses allowed
nonfinite LASSO column scales to be dropped as zeros despite the global
fail-closed rule. The repaired contract drops only finite exact-zero pre-FWL or
finite near-zero post-FWL columns; any nonfinite scale or norm fails the cell
and therefore the validation license or research publication.

The final math pass then found 512 omitted finalization units: 510 promised
descriptive marginal Monte Carlo intervals and the two family-level intervals.
Those units now enter the validation work matrix, and the bootstrap aggregation
unit explicitly covers one structural cell/weight vector shared by all three
smooth candidates.

The final contract pass found that observable-PCA centering and sign were frozen
but its covariance divisor and eigensolver were not. The gate-binding branch now
forms float64 `X_c'X_c/330` and takes the largest eigenpair from symmetric
`numpy.linalg.eigh`; SVD and unscaled-scatter alternatives are unlicensed.

The same pass found that zero population means had hidden finite-sample ridge
choices. Both full-flow candidates now use one globally weighted intercept and
centering after date aggregation, fail a nonpositive proxy Schur variance, and
freeze `numpy.linalg.eigvalsh` plus transposed `numpy.linalg.solve` rather than
an inverse or pseudoinverse.

A final numerical pass disambiguated roundoff clipping: tolerated negative
Schur eigenvalues retain their raw values in condition/penalty arithmetic and
the once-symmetrized matrix is not projected before the regularized solve. A
nonpositive `smax`, more-negative eigenvalue, or post-ridge condition ratio above
`K(1+1000 eps)` fails the cell.

The last byte-exact pass found six more authority defects. The mathematical
LASSO ratio formula admitted binary64 implementations differing at 7 of 40
indices, so the executable vector is now literal- and hash-sealed. The CRN
narrative now names the active phase/scenario while DGP parent-key slots remain
zero sentinels. D0026--D0028 are explicitly historical S0003 records with no
S0004 execution authority. Finally, the benchmark prose now says four total
bundles, not four additional bundles after the cold run. A complete assignment
table now gives every DGP stream exactly one active phase/scenario pair and
marks reliability-frontier `22/3` as generator-free metadata.

The same pass found that mandatory reduced-frontier passage rates had retained
all 499-replicate event estimates but no Monte Carlo intervals or finalization
units. All six date-frontier and twelve extra-reliability rates now receive
descriptive one-sided 95% Wilson lower intervals, and the exact validation
finalization count is 53,415.

Two final executable-wording defects also changed possible outputs. The
absolute CV tie rule now defines `MSE` as fold-ordered pooled SSE divided once
by 30 and uses an inclusive `<= min + 1e-12` comparison. The benchmark now
counts only post-cold complete-bundle time toward its 600-second warm minimum,
while the cold bundle still counts toward four total bundles.

The final RNG replay check found that exact keys and shapes still allowed
different Gaussian transforms. Every component now uses one exact float64
`Generator.standard_normal` call at its configured shape, and the bootstrap
probability constructor plus exact `Generator.multinomial` call are frozen too.

All twenty were diagnosed before implementation or registered RNG. S0004 now uses
the exact rational/raw seal, requires nonzero `CI_I` recovery with strict
point-accuracy and nonbias checks under the same noisy-level/modal-noise law,
keeps that recovery's phase-25/scenario-4 realization disjoint from sealed
phase-30 research, freezes the float64 AR-filter-first symmetric map, publishes
the exact work matrix, defines the complete LASSO map, and
separates the strengthened hybrid from six labeled protocol reconstructions.
One arithmetic self-check also corrected research paper-bootstrap work to
`1,063,828,080` accumulation terms.

These repairs are not an admission pass. A new independent review must verify
the post-repair revision; implementation and every registered G2 stream remain
locked until that review, a raw config seal, a clean documentation commit, and
hosted CI all pass.

## Fifth verdict: sealed pass; registered RNG still forbidden

Three independent read-only lanes now pass the final mathematical, inferential,
and executable content after all twenty defects above. The frozen raw config
SHA256 is
`f6291894462db2215ec9d94b2b936f5b969e47b61cdbbe50de7ae0782a83defc`;
the target raw/semantic and LASSO-ratio seals are recorded in A005. A005 also
mechanically retires every pre-D0031 execution clause.

Three fresh seal-only re-reads independently reproduced all four digests and
confirmed that A005 is the only executable authority surface. S0004 therefore
passes pre-implementation contract admission. Local verification, a clean
commit/push, and hosted-green CI are still mandatory before test-first G2 code.
No resource, validation, or research seed is exposed by this verdict.

The exact sealed files were committed as
`a5c7f1c02e941a0d6fdef3d645dfea63884cdfd7` and passed hosted CI run
`29448917107`. That evidence opens only test-first implementation with
test-only seeds. It does not validate unimplemented G2 estimators or relax any
later resource/validation/research admission.

The strongest objection is substantive rather than mechanical: 95% proxy
reliability and the latent decomposition are favorable source-compatible
choices, not identified market facts. A positive result would establish a
conditional counterexample; a miss would not establish that confounding is
immaterial in the market.

## Sixth verdict: first software slice passes; production RNG still forbidden

The first implementation did not pass its first hostile review. Reviewers
reproduced all of the following with test-only seeds before the current
boundary was admitted:

1. a one-ULP or sub-tolerance population-target change passed regeneration;
2. equality-compatible float, signed-zero, string/enum, integer/enum, and
   mutable-container substitutions passed typed validation;
3. address and namespace subclasses routed registered seed values to an
   intercepted `SeedSequence`, and bootstrap reread an address after validation;
4. recovery and IID parents could mint unused bootstrap addresses;
5. filtered arrays could be rewrapped as raw and filtered twice;
6. dates, components, and phase-30 research arrays could be relabeled or mixed
   into phase-25 recovery; and
7. provenance hashes and wrapper-owned receipts were self-attestation, while a
   callable registrar could mint the same false origin.

No registered generator was instantiated in these attacks. The repaired code
now requires exact executable representations and a derivative target-row
digest, consumes one nonvirtual validated entropy snapshot, narrows bootstrap
parents, and keeps raw issuance state outside the wrapper. The sole registry
write is inline after the five method-owned draws in exact
`TestRngNamespace.draw_base_normals`; the generic packaging helper cannot mint
authority. A weak-reference cleanup regression prevents issued test bases from
accumulating indefinitely.

Three focused hostile re-reviews now pass. They independently rejected
reconstruction, coordinated mutation and retokening, private-factory
repackaging, cross-date/component swaps, phase-21-to-25 relabeling, and
phase-30-to-25 mixing. They also reproduced every one of the 17 population
cells with maximum algebra discrepancy `0.0`. The stabilized local boundary has
79 targeted tests and no production entry point.

The strongest new mechanical objection is performance: every transform hashes
the five raw component arrays. Correctness requires that check, but its warm
throughput and RSS cost are unmeasured. It enters the already required resource
benchmark and can block resource admission. The strongest substantive objection
remains the favorable, unidentified 95% proxy reliability and latent
decomposition. Neither objection licenses a registered stream yet.

## Seventh verdict: portability repair passes review; production remains locked

Hosted Linux falsified the initial assumption that a locked NumPy
`standard_normal` call is byte-identical across CPU/OS runtimes. Two staged,
test-seed-only diagnostics localized the entire 99,000-value discrepancy to one
ULP at global index 60,328: Linux returned
`0x1.f987e87be94a2p+1`, while the declared M4 target returned
`0x1.f987e87be94a3p+1`. The independently regenerated 150,000-word
PCG64DXSM digest, all preceding values, and all subsequent values matched.
Because the 3.95-sigma value exceeds NumPy 2.5.1's 3.654 Ziggurat cutoff and
the source implements that tail with platform `log1p`, the fault is in
distribution-transform rounding, not addressing, PCG state, or draw count.

Preregistration amendment A006 does not accept two research realizations. It
retains every A005 key, shape, one-call transform, threshold, and inferential
rule; freezes both observed runtime-class KAT outcomes for software testing;
and authorizes registered construction only on one exact Darwin/arm64
fingerprint after all five M4 Gaussian KATs and the universal raw-PCG KAT pass.
The fingerprint covers Python and NumPy versions/builds, the installed NumPy
Generator binary, OS build, architecture, and byte order. Linux must reject
before `SeedSequence`.

One hostile code audit passed the fail-closed ordering and found no production
authority in the current slice. A separate research-governance audit accepted
A006 as a pre-data portability amendment only after three overclaims were
removed: `Generator` and PCG guarantees are now distinguished, Linux is a
runtime-class test outcome rather than a locked production runtime, and the
five KATs are not called proof over unseen tail inputs.

The strongest unresolved objection is now explicit: byte-exact Gaussian replay
is machine-bound, and sparse KATs can detect known runtime drift but cannot
prove stability at every unseen libm tail input. Universal cross-machine replay
would require a new portable-transform specification before registered access.
No registered G2 seed has been constructed; the resource stream remains locked
until the remaining estimator, checkpoint, recovery, and resource gates pass.

Repair commit `ff3a343e9c4cfbf672d7cae5614081733c4b695e` passed hosted CI
run `29455143418`. This closes the portability objection for the first software
slice only; it does not weaken the machine-bound limitation or license any
registered stream.

## Eighth verdict: smooth estimator core passes; execution authority remains closed

The estimator core did not earn admission from its first green numerical
suite. Hostile review subsequently reproduced all of these defects before the
current verdict:

1. forged transformed dates and crossed `X_A'X_A`/`X_B'Y_B` panels passed;
2. incomplete date ranges and analytic-origin aggregates could approach the
   high-level contract fits;
3. copied digests and response-blind base identities were mistaken for
   authority over structural responses;
4. an unissued design wrapper could retain an issued Gram while changing
   `X0'Y`;
5. reliability reuse conflicted with response labels and generic/private
   helpers could mint from copied receipts;
6. byte-identical ndarray subclasses, duck-typed receipts, JSON-equivalent
   containers, and value-equal scalar subclasses reproduced tokens while
   changing runtime behavior; and
7. after all of those repairs, a state-changing caller `Sequence` returned
   issued moments during validation and unissued zeroed cross-moments during
   construction. The old cell stacker minted the resulting panel and aggregate;
   all 90,720 stacked cross-moment entries were zero although every validated
   issued input entry was nonzero.

The repaired boundary issues every numeric wrapper that crosses authority,
binds exact immutable float64 arrays and exact typed receipts, distinguishes
base identity from response-map identity, requires complete one-stream panels,
separates analytic extraction/solvers from sealed high-level fits, and performs
all stack validation and construction from one local tuple snapshot. Dynamic
mutation and weak-cleanup checks now cover the date, panel, and aggregate
stages. Target, `paper_recovery`, `phi`, reliability, and N/T/L relabels or
mutations fail before a coefficient.

The final complete 48-date issued-path smoke uses only test seed `1729`, makes
no comparison with truth, and returns finite oracle ridge, observable ridge,
and pooled homogeneous outputs at the frozen shapes. Under a 60-second alarm it
completed in 0.64 seconds with maximum RSS 63,045,632 bytes. The focused suite
has 49 passing tests; the full local gate passes Ruff, formatting, strict mypy,
157 tests, deterministic demo, and committed-result drift. The final math audit
passed. The contract audit first found the sequence substitution and then
passed the one-snapshot repair. No registered resource, validation, recovery,
IID, paper-recovery, or research stream ran.

The strongest unresolved mechanical objection is deliberately not softened:
A022 is untested. Content hashing and weak issuance may still violate the
hashing-inclusive warm-throughput or memory projection, and there is no
checkpoint loader capable of independently validating serialized manifests and
minting fresh in-process authority. This verdict therefore closes only the
in-memory estimator core. It does not admit checkpoint/recovery, the resource
stream, validation, or research. The strongest substantive objection also
survives: the 95% proxy reliability and latent decomposition define a favorable
source-compatible conditional counterexample, not an identified market fact.

## Ninth verdict: the eighth verdict was reopened; C0014 now passes

The eighth verdict was premature. Final code review compared two contract
designs built from one issued base at targets 0 and 16. Their `X0` arrays,
packed Grams, and filtered-base identity were byte-identical, yet the old
`design_sha256` values differed because the digest included the full structural
response receipt. That violated the response-independent shared-design identity
derived before implementation and would have made a future design checkpoint
or cache depend on the response cell.

C0014 recorded the mismatch before repair. The design digest now binds only a
versioned namespace, exact dimensions/date, response-independent source
identity, and exact `X0` contract/bytes. Contract designs use the validated
filtered-base identity; analytic designs use a separate literal namespace.
Full response receipts remain in the wrapper issuance tokens, so target 0 and
target 16 share a design digest but retain distinct response authority. The
common-base cross-cell builder still passes, and an analytic design with the
same `X0` cannot collide with the contract design.

The final post-C0014 evidence is 49 focused G2 tests, a green 157-test
repository gate, clean Ruff/format/strict mypy, deterministic demo and committed
result drift, plus fresh mathematical, contract, code, ledger, and verification
audits. The renewed complete 48-date issued-path smoke used only test seed
`1729`, finished under a 60-second alarm in 0.65 seconds, and reached maximum
RSS 63,766,528 bytes. It asserts only finite output shapes and authority
transitions; it makes no recovery, bias, size, power, or target claim. No
registered G2 stream ran.

The strongest unresolved mechanical objection remains A022: neither this smoke
nor the unit suite measures the frozen hashing-inclusive cold/warm workload, and
no checkpoint loader can yet validate a serialized manifest and mint new
in-process authority. The strongest substantive objection also remains the
favorable, unidentified 95% proxy reliability and latent decomposition. The
next slice must derive checkpoint/recovery authority and then test resource
admission; this verdict licenses neither.

Estimator-core commit `5500611da123bdc1dedd2124b0f2fd26e04525db`
subsequently passed hosted CI run `29492765654`; its parity job completed in 31
seconds. That closes the local-versus-hosted software parity objection for this
revision only. It does not answer A022, serialize authority, or license any
registered G2 stream.

## Tenth verdict: checkpoint/recovery passes local hostile closeout; A019 remains locked

The first numerically green C0015 implementation did not survive review.
Hostile probes reproduced a direct writer-authority bypass, acceptance of stale
timestamp-valid bytecode, transient 2 GiB cap breaches of 94 and 31 bytes,
loader/writer TOCTOU, redirectable private child roles, missing pre-draw
source/runtime reinspection, partial final evidence, process-group leakage
after leader exit, mutation through a symlinked root, a false post-`SIGKILL`
cleanup success, replay through a named FIFO, missing teardown after an
unexpected sampler exception, and simultaneous success/failure evidence after
a directory-fsync fault. Compound fault injection then showed that stage
cleanup `OSError` or `KeyboardInterrupt` could erase an already-uncertain
publication outcome. Make itself could be redirected before Python import and
could mutate through a symlinked `data` ancestor.

Every one of those cases now fails closed under the declared A024 boundary.
The codec reserves the whole logical/allocated checkpoint tree before mutation
and holds directory-descriptor leases through write or load-authority
transitions. Child roles require inherited anonymous-pipe capabilities; roots,
source, runtime, attempt, and process groups are rechecked at their authority
boundaries. Terminal publication either becomes durably authoritative, becomes
durably absent before the opposite outcome, or remains explicitly uncertain
with the attempt consumed and no opposite marker. Make freezes the literal
bootstrap/thread contract and rejects observed symlink ancestors before its
first `mkdir`.

Closeout found two further evidence defects. The sole public `Makefile`
launcher was absent from the execution-source snapshot, and the seed-1729
recovery *procedure* printed `VALIDATION_RECOVERY` `23/0` although it actually
drew the licensed `VALIDATION_DATE_FRONTIER` `22/2` test address. The repaired
snapshot binds `Makefile` as its seventh declared path. Test spec, attempt,
checkpoints, draws, and result now all report date-frontier `22/2`; public A019
alone remains recovery `23/0`.

The fresh stable evidence is 86/86 checkpoint tests, 26/26 recovery tests, and
112/112 across the combined surface. The complete locked local gate passes
Ruff, Ruff format, strict mypy over 22 source files, all 269 tests,
deterministic demo, and committed-result drift. Independent hostile review
also reran recovery 26/26 and four focused launcher/load-authority probes 4/4.
The exact A019 result, checkpoint, and scratch paths remain absent. Neither
seed 9191 nor any registered G2 stream was run.

One governance defect cannot be repaired retroactively. The live session
recorded A020's prediction, failing Makefile-omission test, and source repair in
that order, but no immutable repository-local red log preserves the sequence.
The still-uncommitted worktree and later A021 edits make current mtimes
non-probative. A020 therefore receives only a qualified chronology pass. Future
authority repairs must commit, or otherwise immutably preserve, prediction and
red evidence before implementation.

The strongest remaining mechanical objections are explicit: Linux
anonymous-pipe identity still needs committed hosted execution; 50 ms RSS
sampling can miss a shorter peak; a power loss or compound publication
uncertainty can consume A019 with only its attempt; and advisory locks plus
unkeyed hashes cannot defeat the coordinated same-user writer/race excluded by
A024. A022 also remains entirely untested: the checkpoint smoke is not the
hashing-inclusive cold/warm resource benchmark.

The deterministic local checkpoint/recovery revision passes hostile closeout
with the A020 chronology qualification. This verdict does **not** license A019
from the dirty worktree and does not license resource, validation, research, or
empirical access. A019 may be consumed once only after this exact source state
is committed, pushed, and passes hosted CI, with the worktree clean and the
canonical attempt path still absent.

### Hosted addendum and external one-shot authority

Commit `5aca8111540064b9449ef55a806427795cb800bd` subsequently passed
hosted CI run `30349473867` in 1 minute 22 seconds. This closes the pending
Linux anonymous-pipe objection for that source state; the job ran the complete
locked parity suite and emitted only the existing Node 20 action-deprecation
warning.

A corrected final eligibility check then proved clean HEAD, the same hosted
SHA, absent canonical result/checkpoint/scratch roots, and the exact Make-only
dry run. Submission of the real Make command was rejected before process
creation by the external safety gate because the user had not explicitly
authorized consumption of the sole irreversible A019 attempt. No workaround
is permitted, no A019 state exists, and the rejection is not counted as an
attempt. A019 therefore remains locked pending explicit user authorization and
a fresh eligibility check.

## Eleventh verdict: A019 passes once; no substantive G2 claim is licensed

The user subsequently authorized the exact irreversible
`make g2-checkpoint-recovery` command, explicitly naming seed `9191`, one
consumption, and no retry. The fresh eligibility check immediately before
execution found an empty porcelain status, HEAD
`a75ea69d85c5425bd5fe824361869c3a7edb55e7`, successful hosted CI run
`30350204001` on that exact SHA, all three canonical roots absent, and the
fixed Make-only dry run. The real command was submitted exactly once and
exited zero.

The result matches the frozen address: seed `9191`,
`VALIDATION_RECOVERY`, 252 dates, panel 0, design target 16, response target 0,
and phase/scenario `23/0`. Its immutable attempt digest is
`18c70c205ad75d608ad0dc70f3c9873df96d2a636f351b22411599889ddb01c1`.
The run took 18.907810209 seconds and observed 178,864,128 bytes peak
process-tree RSS. Its complete base/cell checkpoint tree allocates 9,183,232
bytes. These are respectively 15.76%, 11.11%, and 72.98% of the frozen hard
wall, RSS, and artifact stops. No hard stop fired.

Independent read-only checks recomputed the SHA256 of `attempt.json`,
`result.json`, both manifests, and all three NPY payloads. Every value matches
its parent receipt: result SHA256
`7061e9d5a734115cadad728e262eceb177d5eddb9f1cb6391a1f81aa040e7a3c`
matches the terminal `_SUCCESS`; each manifest and payload digest matches its
checkpoint `_SUCCESS`; the worker claim binds the attempt digest; and no
failure marker exists. Before/after array, receipt, design-digest, and all
three coefficient hashes are exactly equal. The fresh process reproduces the
oracle, observable, and homogeneous coefficient hashes with
`fresh_process_rng_draw_count=0`.

Two bounded independent audits passed. They separately reconstructed the
24-file source snapshot as
`7eb724851b44a747743452a829ad7ff2619fe4234723f9ce5df53dfd456971d3`,
the Darwin/arm64 runtime identity as
`17b80bd40159b4e921983528b04a0050912f19360d99560f8cebfbea0be9513b`,
all 252 unique date receipts, the data-only array hashes, and the shared design
digest. They found exactly one worker claim, one base artifact, one cell
artifact, no symlink or unexpected checkpoint file, empty worker
stdout/stderr, empty bytecode-cache directories, and no surviving claimed
worker PID.

The hostile interpretation is narrower than the green status. A019 proves that
this source/runtime/address recovered its sufficient statistics and coefficient
bytes once on this machine. It does not compare a coefficient with truth, test
bias or power, calibrate a market parameter, admit a registered
resource/validation/research realization, or pass the G2 premise gate. It also
does not resolve A024: unkeyed hashes cannot authenticate origin against a
coordinated same-user writer. The 50-ms RSS sampler can miss a shorter peak,
and the scratch trace is audit evidence rather than a cryptographic transcript.

The strongest remaining mechanical objection is A022. The successful
18.91-second recovery is not the preregistered hashing-inclusive cold/warm
resource workload, so extrapolating it to the 15,195,600 validation or
45,586,800 research LASSO fits would be invalid. The next permitted action is
derivation and pre-recording of A022 only. A019 is consumed permanently and
must never be rerun.

### Hosted A019-evidence addendum

Evidence commit `e328a33f0792ff81c8a0a3e6d54b7ad0a7563f7e` passed hosted CI
run `30386325383`; its parity job completed in 1 minute 19 seconds with every
required step green. This proves that the committed receipts and living-ledger
closeout coexist with the locked deterministic suite. It does not replay A019
and does not weaken any A022 or registered-stream lock.
