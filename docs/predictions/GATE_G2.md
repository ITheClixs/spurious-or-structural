# G2 pre-run prediction

Written before G2 implementation, resource benchmarking, validation, or the
single frozen research draw. The first hostile review rejected an earlier
three-factor design and then rejected the oracle-only S0003 boundary before any
RNG access; S0004 is the only design
eligible for execution.

## Claim that may die

Conditional on diagonal sensitivity `d = 0.29` and the registered
off-diagonal sensitivity interval, a permutation-invariant one-factor model
matching the registered Capponi--Cont one-minute commonality will exhibit more
than 50% confounding error in a homogeneous off-diagonal impact coefficient
for an observable integrated-top-ten-OFI proxy-control ridge, two stronger
oracle-flow projections, and the binding published `CI_I` protocol check.

This is a conditional-existence claim. It is not an estimate of the real
market's structural tuple and does not claim that confounding explains the
published disagreement.

## Deterministic population prediction

The structural off-diagonal varies continuously from `0.0029` to `0.0046`
with diagonal `0.29`. Seventeen closed-grid points license the finite-sample
runner; the analytic formula in
`docs/derivations/GATE_G2_PREMISE.md` covers the continuous interval.

At proxy reliability `0.95`, the population predictions are:

| True off-diagonal | Homogeneous | Oracle ridge | Observable ridge | Observable error | Critical reliability: homogeneous / oracle / observable |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0029000 | 0.0098396929 | 0.0098396897 | 0.0097798675 | 237.24% | 99.260385% / 99.260383% / 99.226218% |
| 0.0046000 | 0.0109224510 | 0.0109224470 | 0.0108491633 | 135.85% | 98.634210% / 98.634207% / 98.573188% |

The upper structural endpoint is least favorable to the positive claim. Its
population observable-ridge error exceeds the 50% threshold by
`0.0039491633` in coefficient units before sampling uncertainty. Exact values
for all seventeen points are committed as canonical JSON in
`configs/g2_population_targets.json`; the raw-file SHA256 is
`f13adcff4259773485ca5952d23ae923d3c501c84d4edb102c1886460ada4a59`.
Because full-precision floating evaluation can vary by a few ULPs, the
independently reproducible 12-decimal semantic SHA256 is
`f437f3308d92e5035abfed796112502a90daf281a585e8cf1a5013bd4fed511a`.
Every registered command must validate both roles before obtaining an RNG:
the raw digest protects the committed bytes, while the semantic digest checks
an independent derivation under the frozen canonicalization rule.

The directional prediction at reliability 0.95 is a positive overestimate. At
reliability one, homogeneous OLS recovers `Lambda`, oracle ridge retains only
the floor shrinkage `10^-6 / (1 + 10^-6)`, and observable ridge targets
`0.9816922278202821 o` because OFI measurement error remains. All three
negative-control targets are sealed analytically.

The historical Hasbrouck--Seppi comparator is nonconfirmatory. A prior
continuous calculation combining its dimensionless factor summaries with the
one-minute point gives a least favorable 77.15% population error at 95%
reliability. This is robustness evidence only, not a joint calibration.

## Strongest-opponent prediction

All three smooth confirmatory candidates must pass at all seventeen structural
grid points:

1. `ORACLE_Q_PROXY95_CONDITION_RIDGE` receives all 30 true flows and the proxy,
   partials out the proxy, and uses a positive condition-capped ridge inverse;
2. `ORACLE_Q_PROXY95_HOMOGENEOUS_OLS` is additionally told the true homogeneous
   symmetry and pools every asset row on own flow, the sum of other flows, and
   the proxy while preserving whole-date clusters. Its cross-sum coefficient
   is one off-diagonal; and
3. `INTEGRATED_OFI_PROXY95_CONDITION_RIDGE` observes only date-estimated,
   L1-normalized top-ten PC scores plus the proxy. This is the gate-binding
   observable factor-control opponent.

The second model is a no-strawman veto: it removes the high-dimensional
covariance inversion and estimates only three slopes. No truth-assisted model
selection occurs after the draw.

The `CI_I` CCZ protocol reconstruction is also binding at the primary
observable calibration and upper structural endpoint because it is the only
published CCZ equation with integrated top-ten OFI and explicit off-diagonal
coefficients. Its predeclared `(0,1)` coefficient must pass the same rule under
the shared 499 date weights. The other five CCZ reconstructions are mandatory
fidelity diagnostics reported separately.
Factor-residual operators are compared with their fair projected target
`Lambda P_perp`; their full response-equivalent maps are not silently
substituted for that estimand. No diagnostic can rescue a failed smooth
candidate or failed `CI_I` veto.

## Interval, size, and power prediction

The confirmatory standard error is the sample standard deviation of 499
whole-date multinomial-weight bootstrap estimates. Each replicate preserves
date order and all within-date bins/assets, and refits the complete smooth
candidate from date sufficient statistics. The reported 95% intervals are a
bootstrap-SE normal interval with `ddof=1` and critical value
`1.959963984540054`, and a basic date-cluster interval using Hyndman--Fan type
7 quantiles at 0.025 and 0.975.

The gate uses a stricter form of the brief's rule:

```text
abs(estimate - truth) - 0.50 abs(truth) > 3 bootstrap_se.
```

Thus the margin beyond 50%, rather than error merely relative to zero, must
clear three standard errors.

Before the research seed is available, 100 independent panels must license the
exact final procedure:

- a null-grid superpanel runs nine proxy-noise-amplitude nodes from `R = 1` to
  each candidate/cell's semantic-hash-sealed 50%-materiality boundary, for 459
  strict events; the one-sided 95% Clopper--Pearson upper bound on the family
  indicator that **any** event passes is at most 5%; and
- a power superpanel runs all 51 smooth components at proxy reliability 0.95; the
  one-sided 95% Wilson lower bound on the gate indicator that **every**
  component passes is at least 80%.

With 100 superpanels, the first rule permits at most one family-union success
and the second requires at least 87 gate-intersection successes. Reliability
one also supplies a 51-component analytic-target recovery diagnostic. This is
a frozen null-grid calibration, not a continuum-uniform size proof. Marginal
component rates receive unadjusted, descriptive, non-gating one-sided 95%
Clopper--Pearson upper intervals for null components and Wilson lower intervals
for power components.

All 51 actual alternatives supply the joint power license; no impossible
exactly-50% alternative is planted. The upper endpoint alone supplies the
reduced 48-/96-date and reliability frontiers. Their six candidate-by-date and
twelve candidate-by-extra-reliability passage rates each receive an unadjusted,
descriptive, non-gating one-sided 95% Wilson lower interval over 100
superpanels. A failed validation seed is not retried. The heavier published
`CI_I` branch separately must recover homogeneous
diagonal `0.29` and focal cross-impact `0.0046` at actual `N=30` and 252 dates
before its binding research run.
That recovery retains the confirmatory equicorrelated flow law but removes price
confounding (`Gamma = 0`), so it cannot pass by replacing the hard collinear
design with independent flows, exact measured flows, isotropic return noise, or
a zero cross coefficient. It preserves every research upper-endpoint
distribution parameter and deterministic map except `Gamma`, but uses its own
disjoint phase-25/scenario-4 addressed normals so validation cannot inspect the
phase-30 research realization.
All 31 truth values must lie inside their Bonferroni date-bootstrap-normal
intervals, every point error must be strictly below 50%, and the focal
material-bias declaration must be false. This does not upgrade one recovery
panel into a Monte Carlo size/power license.

The finite null grid has a frozen maximum proxy-noise-amplitude gap of
`0.015038828627620739` and maximum adjacent reliability gap of
`0.003307437435413063`. These gaps ship with the outcome. Any nonfinite result,
declared required-full-rank/conditioning failure, weak PCA, named cell failure,
or solver nonconvergence fails validation outright; it is not treated as
evidence of size control.

## Dependence and resource prediction

All latent components use stationary Gaussian AR(1) paths with coefficient
`0.60`, independent stationary initialization by date, and no cross-date
innovations. This unsourced value is an explicitly hostile dependence stress,
not empirical calibration. An IID path is diagnostic.

Validation uses reliability-polynomial date moments. A shared base plus one
252-date structural cell is `8,811,936` bytes; all retained numeric validation
output is below 238 MB and a 2x allocation remains below 500 MB. The paper path
streams one raw date and retains a roughly 17.1 MB research summary.

### Historical resource-bundle prediction — superseded by A022--A026

The benchmark times fourteen distinct kernels, including base/cell
construction, each of the three fits, weighted aggregation, interval
finalization, every checkpoint boundary, a complete six-spec paper date, and a
`CI_I`-recovery date. It runs until at least four total complete bundles and at
least 600 post-cold seconds have elapsed; the last three complete bundles
determine warm throughput. Each phase
uses 1.25 times planned work divided by the smaller of warm throughput and 60%
of cold throughput. Any one-/12-/three-/16-hour expected-cap projection breach,
480-second task/batch, 3.5 GB RSS, or 2 GB checkpoint breach stops before
validation. The two-/24-/six-/32-hour hard limits are runtime kill thresholds,
not admission slack.

This paragraph is preserved for diagnosis only; it is not admission or
implementation authority.

## Interpretation of every outcome

- **All three smooth candidates and `CI_I` pass their frozen scopes after the
  smooth null-grid/power license and published recovery check:** G2
  supports material confounding in the registered source-matched model class.
- **A nonbinding CCZ diagnostic differs:** report the estimand-specific
  discrepancy; it cannot rescue a failed binding event.
- **Any smooth confirmatory candidate or the `CI_I` veto fails:** no-strawman veto; G2 does
  not pass.
- **Population bound crosses 50%:** deterministic design failure; no RNG is
  permitted.
- **Size, power, or compute license fails:** unadjudicated design failure; the
  research seed remains sealed.
- **The sole research draw misses a registered event after adequate smooth
  power:** the preregistered finite-sample demonstration fails. With an 80%
  power floor this does not logically falsify the analytically known population
  fixture, and it is not a premise-killing market null.
- **Premise-killing null:** permitted only after a separately preregistered
  sharp source-compatible bias upper bound lies below 50% with adequate power.

The research seed is consumed once, after a clean implementation boundary and
hosted CI. It is never retried under another seed or silent specification.

## A025 resource-execution correction before implementation

Appended on 2026-07-29 before resource-run code, any rehearsal, or any
registered resource access. The scientific claim, estimators, truth values,
intervals, thresholds, validation trials, research draw, budgets, and
interpretation above remain frozen. This document remains the scientific G2
prediction, but it is not part of the A022 terminal source-seal tuple. The
executable resource prediction is
`docs/predictions/GATE_G2_RESOURCE.md`, together with the two bound A022
derivations and the bound preregistration/compute amendments. The bullets below
are a non-authoritative cross-document synopsis: they cannot override those
sealed files or independently license resource execution. They include A025's
replay-comparator correction so that an interruption cannot improve a resource
acceptance result, plus the later freeze repairs for durable child birth,
Darwin absence evidence, watchdog provenance, terminal-entry nonadoption, and
all-terminal size preflight.

The A025 resource synopsis is:

- The fixed record order remains
  `k1,k2,k3,k4,k5,k6,k7,k9,k10,k8,k11,k12,k13-recovery,k13-research,k14`.
  Its exact successful RNG call-count vectors are
  `[1260,0,25,0,0,0,0,0,0,0,5,5,25,0,0]` for equal/rehearsal,
  `[1260,0,25,0,0,0,0,0,0,0,0,5,25,0,0]` for validation, and
  `[1260,0,25,0,0,0,0,0,0,0,5,0,0,25,0]` for research. DGP calls are
  date-major/component-ascending and bootstrap calls
  replicate-ascending; inventories and replay copies preserve that order
  without sorting or deduplication.
- Durable resume state has exactly seven rows: base panel, cell panel, smooth
  bootstrap weights, oracle focals, homogeneous focals, observable focals, and
  one role-resolved paper-weight row. The `(25,252)`
  `resource-resume-paper-bootstrap-weights-v1` artifact is drawn at the first
  positive kernel-13 position, shared by both positive equal variants, and
  cleaned at the last positive kernel-13 position. Its
  producer/last-consumer/cleanup coordinates are `12/13/13`,
  `12/12/12`, and `13/13/13` for equal/rehearsal, validation, and research.
  A zero-unit variant draws nothing.
- A successful three-panel rehearsal has exactly 13 artifact kinds, 51
  artifact rows, 45 canonical boundaries, 12 cleanup intents, 57 capped
  ordinary checkpoint intervals, one root terminal accounting row, and 58
  resource-accounting rows. Earlier 48-boundary,
  12-kind/48-row, and 57-interval statements are historical.
- Receipt recovery first normalizes absent, valid receipt-only stage, valid
  complete staged pair, or valid visible-final states. Successor adoption
  requires proof that the encoded publisher is dead; malformed, partial,
  extra, mismatched, or conflicting states remain forensically incomplete.
  Worker-birth stages, the registered `terminal_entry=true` boundary, the
  final rehearsal boundary, and cleanup-complete final failure-resume stages
  are non-adoptable after publisher death; only their same live publisher may
  finish them.
  Cleanup and debris freeze child-before-parent entry rows, so a crash is
  represented only by an exact absent prefix plus a byte-valid remaining
  suffix with no extra path. Publisher identity is encoded in every adoptable
  payload, target membership/slices are deterministic, and each prospective
  checkpoint/scratch mutation must preserve a representable 512-row plan.
- Failure cleanup is not an uncheckpointed suffix. Between one and 641
  contiguous failure-resume receipts are mandatory, including a final
  cleanup-complete receipt after all rows and required parent fsyncs are
  complete. The chain
  binds immediate predecessors and exact wall/perf/gap/active/cumulative
  clocks. Each resume sample precedes that segment's first deletion/fsync and
  its cutoff follows every charged prefix advance/fsync; resume zero has prefix
  count zero and has `cleanup_complete=true` iff the intent is empty. Each
  failure-intent or failure-resume receipt records at most 480 seconds of work,
  a fixed 60-second publication-accounting charge, and an accounted interval of
  at most 540 seconds. The charge is not an observed or enforced bound on
  failure-receipt publication latency. Every later
  nonfinal receipt advances the prefix or binds a new death; a
  dead-publisher nonfinal stage needs another slot/death row, while a last-slot
  or cleanup-complete stage fails closed rather than duplicating the final.
- Success and failure become visible only through atomic directories
  `terminal/success/{result.json,_SUCCESS}` and
  `terminal/failure/{failure.json,_FAILURE}`. Exactly three non-overlapping
  twelve-child Git checks are legal: the bootstrap check before the first
  worker; the terminal-pre-JSON check after every issued worker identity is
  closed, no worker is alive, and every currently waitable direct child has
  been reaped; and the distinct post-JSON check bound by the marker.
  `attempt.json` persists the complete twelve-child bootstrap full check.
  Terminal JSON persists that check's digest, the complete twelve-child
  terminal-pre-JSON full check, and their count-two inventory/hash; the 24
  Git-child rows are jointly reconstructible from
  `attempt.json` plus terminal JSON. The marker persists the final 12 rows.
  Intermediate source/control seals reconstruct stable bytes in-process before
  and after sealed contract/resource-config loading, immediately before and
  after every nonterminal resource-root mutation, before every worker
  capability, and after every measurement block; they launch no Git
  subprocess. At each cutoff, the rusage high-water envelope
  is supervisor high-water plus the larger of the cumulative worker high-water
  and the available preterminal Git-child high-water. Observed RSS is the
  maximum of the sampled tree peak and that envelope; admission then applies
  the 25% current margin and carried durable-upper maximum. Bootstrap Git
  high-water is present at every durable cutoff, terminal-pre-JSON joins only
  at the terminal cutoff, and post-JSON remains in the marker's separate
  publication-RSS envelope.

  Publication of the final success boundary or cleanup-complete final
  failure-resume receipt is the non-resumable terminal-entry point. The same
  publisher must execute the terminal-pre-JSON check, write and fsync the
  hidden JSON stage, execute the post-JSON check under the sampler, write and
  fsync the marker, pass the no-subprocess final seal, rename the outcome, and
  fsync the terminal parent. A failed or incomplete check, publisher death, or
  later publication failure makes the attempt forensically incomplete; no
  successor may retry a Git check, publish the selected outcome, or select its
  opposite.

  The final success boundary, final rehearsal boundary, and final failure
  resume bind a terminal-size preflight. A frozen fixture schema covers
  failure intent, every failure-resume shape, rehearsal/registered
  success/failure JSON, and both markers at all applicable maxima, including
  64 waits, 128 deaths, 512 cleanup rows, 641 resumes, 24 preterminal and 12
  post-JSON Git rows, and 1,201 publication-RSS samples. Every canonical file
  stays at or below 1 MiB; a one-past mutation fails before publication.

  The marker persists every post-JSON
  wait/rusage/stdout/stderr/parsed-result row, complete source and Git-control
  rows, runtime/module/boot/publisher identities, publication-local sampler
  rows, and recomputed RSS upper. After marker/stage fsync, a no-subprocess
  final seal repeats those identities, proves no descendants, waits for a
  post-guard sample, stops/joins the sampler, requires only the publisher
  thread to remain, and takes the final self-resident/RUSAGE_SELF sample.
  Every final gap is at most one second, observed RSS is at most 2.8 GB, and
  the recomputed 25%-margin admission upper is at most 3.5 GB; only then does
  it license rename plus parent fsync. Final pre-JSON work is at most 480
  seconds and the later terminal suffix receives a fixed 60-second accounting
  charge, giving an accounted sum at most 540 seconds without claiming an
  end-to-end close-time bound. No JSON-only, post-terminal, or post-success
  rehearsal-cleanup branch is licensed. Forward cutover requires exclusive
  hidden-stage creation plus successful parent fsync; an absent post-crash
  stage from the intervening window is pre-cutover, while an exact surviving
  stage conservatively locks its kind. An exact visible final is reusable only
  after a current-live terminal-parent fsync. The fixed 60 seconds are an
  accounting charge, while visible-directory existence attests the final
  seal.
- Attempts bind the initial supervisor PID, kernel start identity, and boot
  digest. Every claimed-worker `wait4` appends one cumulative hash-bound
  claim/identity/status/`ru_maxrss`/sample/deadline row. Every superseded
  identity has one exact death proof:
  `wait4-reaped`, `double-process-identity-absence`, or
  `boot-identity-changed`; only the first has wait/rusage fields. Kernel 14's
  receipt probe is not a child role. Git execution is limited to the three
  sequential twelve-child sets above: the first 24 rows live in
  `attempt.json` plus terminal JSON, and the last 12 live in the marker.
  Intermediate seals launch no process, no Git child overlaps a worker, and
  missing Git wait/rusage evidence is unclosable rather than convertible to a
  worker death proof. Reservations retain their creator-claim digest;
  resumed current claims prove a contiguous predecessor chain rooted at that
  immutable claim instead of rewriting it.
- Every child spawn is preceded by a durable launch intent with nonce
  commitment and distinct precomputed work/reap deadlines. The
  parent-liveness-gated bootstrap child publishes PID/start/boot birth first;
  claim, worker-ready, and capability follow only a validated launch/birth
  pair, and each complete birth later joins exact wait/death evidence.
  Arm-bearing boundaries, cleanups, and interruptions are durable before work,
  and later clocks cannot invent or extend their deadlines.
- Darwin double absence passes only two zeroed-buffer samples 50 ms to 1 s
  apart that are both zero/`ESRCH` or full reads naming the same replacement
  PID/start identity. All mixed, present-target, permission, ambiguous,
  malformed, short/oversize, ABI, PID-mismatch, or boot-change cases fail.
  Factorizing the common verdict/identity over two raw
  `[time,return_bytes,errno]` rows preserves the 512-byte death-row cap.
- Every admitted interruption resets thermal qualification, including one at a
  trace or measurement boundary. The suspended prefix completes but does not
  count toward the new epoch; before the next warm trace, fresh
  `validation,research,research,validation` panels must contribute at least
  600 successful seconds. No reset work is required if no later warm trace
  exists.
- Replay comparisons are one-sided. At record `i`,
  `Rplus_i=duration_plus_ns_i=D_i+2*h_i` and
  `Aplus_i=admission_duration_plus_ns_i=Rplus_i+480000000000*r_i`.
  Predictor/reference operands use `Rplus`; held/current operands and all
  cold, conservative/projected task, block, phase, combined, and final
  absolute projections or budgets use `Aplus`. For measurement block `j`,
  `N_j` is its complete balanced-pair count; for
  `s in {overall,validation,research}`, `Rplus[j,s]` and `Aplus[j,s]` sum the
  corresponding fields over the named phase traces excluding `EQUAL`, with
  `overall` combining both phases. Thus sequential stationarity is
  `20*N_j*Rplus[j-1,s] >= 19*N_(j-1)*Aplus[j,s]`; same-phase `H` and
  cross-phase `X` references use only `Rplus`, while their tested sides use
  `Aplus`. With raw durations, units, and clock resolution fixed, incrementing
  any replay count must leave every reference prediction and successful-work
  stop clock unchanged, weakly increase affected held/current and
  absolute-projection operands, and never change any resource acceptance
  Boolean from false to true.
- Only durably closed telemetry segments preserve pass authority. An abrupt
  supervisor or direct boot loss records `"unknown-loss"` and assigns exact
  limit-plus-one uppers of `3,500,000,001`, `2,000,000,001`,
  `6,000,000,001`, and `30,000,000,001` bytes for RSS, checkpoint tree,
  created roots, and absolute workspace, respectively, selecting
  `"select-terminal-failure-telemetry-gap"` before new work.
- Liveness is finite: at most 64 launch intents, 64 worker births, 64 worker
  claims, 63 interruptions, 4,096
  traces, 641 failure resumes, 512 terminal-cleanup rows, 128 attempt-wide
  process-death rows, 64 cumulative worker-wait rows, and 240 ASCII bytes per
  path. Cleanup, death, and worker-wait rows are capped at 1,024, 512, and 512
  canonical bytes; the 131,072-byte non-row term is the exact intent with all
  three row arrays replaced by `[]`, keeping the failure-intent envelope at
  most `753,664` bytes, below the
  `1,048,576`-byte root-receipt cap. Before failure selection, hitting a cap
  selects terminal failure before the one-past object. After selection,
  resume/death/encoding-cap exhaustion stops the consumed failure as
  forensically incomplete before mutation.

These are falsifiable engineering predictions, not observed results. No A025
rehearsal or registered resource, validation, or research address has been
accessed, and the deferred quantitative registered timing/RSS/disk prediction
remains sealed.

## A026 resource-execution correction before implementation

Appended on 2026-08-06 before resource-run code, rehearsal, or registered
access. A026 leaves the scientific design and successful rehearsal tuple
unchanged and predicts three additional fail-closed properties:

- interruption inside any rate-bearing trace selects terminal failure and
  contributes no rate/comparison/projection operand; between-trace recovery
  requires a fresh uninterrupted 600-second thermal cycle, and interruption
  inside that cycle restarts it from zero. Every admitted rate record has
  `replay_count=0` and `Rplus=Aplus`;
- each visible launch intent binds an exact inherited Darwin `flock` lease. A
  same-boot launch-only successor may select pre-RNG failure only after the
  existing supervisor-death proof plus fresh-open acquisition of the same
  stable inode; a live holder returns `EWOULDBLOCK`, and the lock is never
  mislabeled a PID-only death proof; and
- after an exact success/failure terminal-entry object, any dead publisher or
  post-entry failure closes only as successor-rebuildable
  `terminal/nonpass/{nonpass.json,_NONPASS}` with
  `admission_pass=false`, `retry_permitted=false`, no Git retry, no RNG/timing
  work, and no selected/opposite success/failure publication.

The active config prediction is exactly 9,799 ASCII bytes, SHA256
`3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
194 leaf-type rows, and type-tree SHA256
`e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.
Successful rehearsal remains three traces, 45 boundaries, 12 cleanup intents,
57 ordinary intervals plus one terminal row, 58 resource-accounting rows, 13
artifact kinds, 51 artifact rows, and seven resume-state rows per trace.

These are falsifiable engineering predictions, not observations. No A026
rehearsal or registered resource, validation, or research address has been
accessed. Implementation remains blocked until fresh independent methods,
systems, and schema reviews pass the settled A022--A026 authority.

## A027 representation-order prediction

A027 predicts that a unique, invertible semantic index map can be implemented
without changing a scientific result or constructing RNG. The full date vector
must contain nine row-major 30-by-30 operators followed by spec-major,
response-major `(SSE,SST)` pairs; the compact `CI_I` recovery vector must map
to full positions `2700:3600` and `8280:8340`, not to `0:960`. Literal
asymmetric sentinels must detect every transpose, boundary shift, and loss-kind
swap. The order manifest and updated resource config must reproduce the exact
hashes registered in A027. Failure of any invariant leaves the resource gate
closed. Passing them licenses no stochastic or empirical claim.
