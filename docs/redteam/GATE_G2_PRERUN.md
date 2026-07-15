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
