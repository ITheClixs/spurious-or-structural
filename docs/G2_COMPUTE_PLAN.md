# G2 executable compute plan

Written before implementation or registered G2 RNG access. S0004 must project
inside the one-/12-/three-/16-hour expected-cap schedule before validation;
the two-/24-/six-/32-hour hard limits remain runtime stops. The measured
benchmark rejects the design if the expected schedule is not credible.

## Work units and sufficient statistics

The smooth path never checkpoints raw simulated rows. Reliability changes only
the scale of a common proxy-noise path, so each date stores shared polynomial
moments for

```text
X0 = [1, f, proxy_noise, oracle_q_1..30, integrated_q_1..30]  (63 columns)
```

and cell-specific return moments for `Y = [r_1..r_30]`:

```text
shared packed X0'X0: 63 * 64 / 2 = 2,016 doubles/date
per-cell X0'Y:        63 * 30     = 1,890 doubles/date
per-cell packed Y'Y: 30 * 31 / 2 =   465 doubles/date
per-cell total                       2,355 doubles/date.
```

The largest active base plus one 252-date cell is

```text
(2,016 + 2,355) * 252 * 8 = 8,811,936 bytes.
```

All seventeen cells at once would be `84,774,816` bytes, but cell construction
and checkpoints remain sequential. The pooled homogeneous date statistic is
derived from these moments for columns `[1, own_q, sum_other_q, z]`; it does not
create a raw stacked-row allocation.

The full paper path streams one raw date. Its state has
`300 level flows + 30 q + 30 r + z + f = 362` float64 fields across 330 bins,
or `955,680` bytes. A research date cache stores four direct maps, two purged
CC maps, two full CC response maps, one block-mean `P_perp`, and 360
response-level SSE/SST values:

```text
9 * 30 * 30 + 360 = 8,460 doubles/date
8,460 * 252 * 8   = 17,055,360 bytes/panel.
```

The `CI_I` recovery cache needs its 30-by-30 direct map plus 30 SSE/SST pairs:
`960` doubles/date, or `1,935,360` bytes for 252 dates.

## Exact RNG namespaces

Every stochastic component constructs exactly one
`numpy.random.Generator(PCG64DXSM(SeedSequence(entropy)))`. The zero-based,
nonnegative, version-2 entropy vector is

```text
[master_seed, config_schema_version, rng_key_schema_version,
 phase_id, scenario_id, parent_phase_id, parent_scenario_id, n_dates,
 panel_index, cell_key, date_index, component_id, replicate_index].
```

DGP keys use parent sentinels zero, `cell_key = 0`, and
`replicate_index = 0`. Within a fixed phase/scenario, structural cells,
candidates, reliabilities, and the six paper estimator views are deterministic
transforms of common base normals; phase-25 recovery and phase-30 research never
share them. Each component key makes exactly one call
`generator.standard_normal(size=tuple(configured_shape), dtype=np.float64)`.
The returned array must already be C-contiguous; reshaping, custom Gaussian
transforms, `normal`, and sequential reuse are unlicensed. The first time slice is the independent
stationary AR(1) state; later slices are innovations scaled by
`sqrt(1-phi^2)`. No state crosses a date.

The transform is also frozen. Filter every float64 raw component along time
before scaling or modal construction. With `m=1/sqrt(N)`, use
`v=sqrt(q0)g_v`, `q=hq*f*m+v`, the symmetric modal return-noise root
`u=sqrt(sigma_u0_sq)g_u + (sqrt(sigma_u1_sq)-sqrt(sigma_u0_sq))*(g_u@m)*m`,
and `r=q@Lambda.T+gamma*f*m+u`. Set `z=f+sqrt(1/R-1)e` and
`x=q[...,None]+sqrt(547/3953)*eta`. Paper recovery reuses the upper-endpoint
distribution, measured-level and modal return-noise maps, and `Lambda`, and
changes only `Gamma` to zero. It uses disjoint phase-25/scenario-4 base normals;
validation never reads phase-30 research normals. Cholesky,
rotated/eigenvector roots, post-map filtering, and
sequential generator reuse are invalid alternatives.

The only licensed active phase/scenario assignments are:

| Stream | Phase | Scenario | Generator? |
| --- | ---: | ---: | --- |
| Resource smooth bundle | 10 | 0 | yes |
| Resource paper bundle | 10 | 1 | yes |
| Validation size | 20 | 0 | yes |
| Validation power | 21 | 0 | yes |
| Validation date frontier | 22 | 2 | yes |
| Validation reliability frontier | 22 | 3 | no; metadata-only reuse |
| Validation smooth recovery | 23 | 0 | yes |
| Validation IID diagnostic | 24 | 0 | yes |
| Validation `CI_I` recovery | 25 | 4 | yes |
| Research | 30 | 0 | yes |

No unlisted phase/scenario pairing is a valid DGP namespace.

Bootstrap keys use phase 40, scenario zero, the exact parent phase and parent
scenario in their dedicated slots, the exact date count (`48`, `96`, or
`252`), `cell_key = date_index = 0`, component 6, and replicate `0..498`.
Construct `pvals = np.full(n_dates, 1.0 / float(n_dates), dtype=np.float64)`,
then make exactly one
`generator.multinomial(n=n_dates, pvals=pvals, size=None)` call and cast the
returned counts to float64 weights. Each vector is shared across every
candidate/cell/null node in that superpanel. Reliability-frontier
fits reuse phase-21/scenario-0 power base moments and weights; phase 22,
scenario 3 is metadata-only and instantiates no generator. Research confirmatory and paper
outputs share the same research-parent weights. No key denotes two arrays of
different shape, and no unspecified sequential generator state exists.

The null-grid amplitude gap is evaluated as `tau_crit` times the largest
adjacent configured fraction difference. It is not recovered by subtracting
already-rounded `tau` nodes, which can differ by one ULP. Reliability gaps use
the generated nodes `R=1/(1+tau^2)` and adjacent binary64 subtraction, exactly
as frozen in `configs/g2.toml`.

## Exact smooth-validation workload

For candidate `c` and cell `j`, the null grid has nine proxy-noise amplitudes
from exact-factor recovery to its sealed population materiality boundary:

```text
tau_crit = sqrt(1/Rcrit - 1)
tau_k = (k/8) tau_crit, k=0..8
R_k = 1/(1+tau_k^2).
```

One null superpanel therefore contains `3 * 17 * 9 = 459` candidate events.
Reliability-polynomial moments let one date-weight aggregation serve all 27
candidate/node fits for a structural cell. Exact totals are:

Across the 51 sealed critical roots, the largest adjacent proxy-noise-amplitude
gap is `0.015038828627620739` and the largest adjacent reliability gap is
`0.003307437435413063`. Both maxima and every cellwise gap are result metadata;
the grid is not a continuum-size certificate.

| Validation unit | Count |
| --- | ---: |
| Unique base panel-dates | 115,200 |
| Structural cell-dates | 1,324,800 |
| Null-grid bootstrap aggregations | 848,300 |
| Null-grid candidate fits | 22,904,100 |
| Power bootstrap aggregations | 848,300 |
| Power candidate fits | 2,544,900 |
| 48-/96-date frontier aggregations | 99,800 |
| 48-/96-date frontier fits | 299,400 |
| Reliability-frontier extra aggregations | 0 (reuses power moments) |
| Reliability-frontier fits | 598,800 |
| **Total bootstrap aggregations** | **1,796,400** |
| **Total bootstrap candidate fits** | **26,347,200** |
| Point fits | 58,200 |
| **Total smooth candidate fits** | **26,405,400** |
| Within-asset PCA eigenfits | 3,456,000 |
| Success-last bootstrap batches | 72,000 |

Point fits decompose exactly as

```text
null grid          100 * 17 * 9 * 3 = 45,900
joint power        100 * 17 * 3     =  5,100
date frontier      100 * 2 * 3      =    600
reliability front. 100 * 4 * 3      =  1,200
R=1 recovery       100 * 17 * 3     =  5,100
IID diagnostic     100 * 1 * 3      =    300
total                                     58,200.
```

Recovery uses `ddof=1` Bonferroni Student-t intervals for 51 mean coefficients
(`df=99`, critical `3.3975886554479495`) and requires every analytic target
inside. The three-component IID diagnostic uses critical
`2.4353393004016732` and is descriptive.

Retained bootstrap estimates occupy `210,777,600` bytes: `183,232,800` null,
`20,359,200` power, `2,395,200` date-frontier, and `4,790,400`
reliability-frontier bytes. Including active moments, smooth research output,
paper summaries, and point estimates, the numeric payload is below 238 MB; a
2x allocation remains below 500 MB and the hard checkpoint cap is 2 GB.

## Published-protocol validation and research workload

Before the binding `CI_I` research result, one validation panel uses actual
`N=30`, 252 dates, the same within-date AR(1), homogeneous `Lambda` with
diagonal `0.29` and off-diagonal `0.0046`, no confounding, the same upper-endpoint
modal return-noise variances, and the same noisy ten-level construction. Only
`Gamma` differs from research. It runs only `CI_I`:

```text
outer contexts      1 * 30 * 252 * 10       =     75,600
CV solutions        75,600 * 5 * 40         = 15,120,000
final fits          1 * 30 * 252 * 10       =     75,600
total LASSO solutions                         15,195,600
integrated-PC fits  30 * 252 * 10 * (1 + 5) =    453,600
OOS maps            1 * 30 * 252 * 10       =     75,600.
```

The 30 diagonal coefficients and predeclared `(0,1)` cross coefficient must
contain `0.29` and `0.0046`, respectively, in 95% Bonferroni bootstrap-normal
intervals (31 components, critical `3.1535631591215094`). All 31 point errors
must also be strictly below 50% of their truth, and the focal material-bias
event must be false. Its 499 cached-date aggregations use 20 batches.

The frozen smooth research draw has 252 base dates, 4,284 structural
cell-dates, 8,483 bootstrap aggregations, and 25,500 three-candidate fits
including 51 points. Its integrated-OFI construction uses 7,560 eigenfits and
340 checkpoint batches.

The research CCZ reconstruction runs all six variants at the primary
observable point and `o = 0.0046`. Exact counts are

```text
LASSO outer contexts     3 * 30 * 252 * 10          =    226,800
CV lambda solutions      226,800 * 5 * 40           = 45,360,000
final selected fits      3 * 30 * 252 * 10          =    226,800
total LASSO solutions                                 45,586,800
OLS response fits        3 * 30 * 252 * 10          =    226,800
integrated-PC full/CV    30 * 252 * 10 * (1 + 5)    =    453,600
cross-PC full/CV         252 * 10 * (1 + 5)          =     15,120
total PCA eigenfits                                      468,720
OOS response-block maps  6 * 30 * 252 * 10          =    453,600.
```

The binding `CI_I` coefficient is already in the cache and adds no research
fit. The 499 shared date-weight vectors aggregate all 8,460 cached fields,
construct weighted projected targets, and compute intervals/OOS losses without
refitting the 45,813,600 regression solutions. One 25-draw paper batch produces
211,500 doubles and performs 53,298,000 weighted-date accumulation terms.

## Deterministic benchmark license

The resource stream times fourteen separate kernels; one kernel's rate may
never substitute for another:

1. base-date generation, AR filtering, integrated PCA, and base moments;
2. cell-date return/cross-moment construction;
3. weighted bootstrap-moment aggregation;
4. oracle-ridge fit;
5. globally centered homogeneous fit;
6. observable-ridge fit;
7. 499-estimate interval/decision finalization;
8. largest null-batch serialize/reload/hash;
9. base-panel artifact serialize/reload/hash;
10. cell artifact serialize/reload/hash;
11. one full exact six-spec paper date;
12. one exact `CI_I`-recovery date;
13. paper-summary bootstrap aggregation and batch I/O; and
14. final success-last publication.

The unit contract is frozen as follows. `base_date` and `cell_date` each mean
one 330-bin date. A smooth fit is one point/bootstrap solution. An interval unit
is one scalar estimand's complete configured package of endpoints, standard
error, and gate/descriptive status from at most 499 values; the benchmark uses
499 and charges shorter 100-value or single-interval packages as full units.
Null-batch I/O uses the
largest 25-replicate, 27-fit null batch; the final 24 and all smaller branches
are charged as full units. Base/cell artifact I/O uses a 252-date artifact, so
48-/96-date variants are charged as full units. Paper-date kernels include all
CV paths, selected refits, PCA, maps, and OOS work for that date.

Paper-bootstrap work is normalized instead of treating unequal cache widths as
equal batches: one unit is one cached-field x date x replicate weighted
accumulation term including amortized batch I/O. The benchmark measures both
the 960-field recovery and 8,460-field research variants and uses the smaller
normalized rate before applying the cold/warm derating. Exact term counts are
`499*960*252 = 120,718,080` and
`499*8,460*252 = 1,063,828,080`.

The complete `W_phase,k` matrix is:

| Kernel unit | Validation | Research |
| --- | ---: | ---: |
| base date | 115,200 | 252 |
| cell date | 1,324,800 | 4,284 |
| bootstrap moment aggregation | 1,796,400 | 8,483 |
| oracle ridge fit | 8,801,800 | 8,500 |
| homogeneous fit | 8,801,800 | 8,500 |
| observable ridge fit | 8,801,800 | 8,500 |
| scalar interval/finalization | 53,415 | 7,431 |
| largest smooth batch I/O/hash | 72,000 | 340 |
| full-size base-panel I/O/hash | 600 | 1 |
| full-size cell I/O/hash | 5,400 | 17 |
| exact six-spec paper date | 0 | 252 |
| exact `CI_I` recovery date | 252 | 0 |
| paper-bootstrap accumulation term | 120,718,080 | 1,063,828,080 |
| atomic success-last publication | 1 | 1 |

The 53,415 validation finalizations are 52,800 within-superpanel
bootstrap-based smooth events, 459 descriptive null-grid marginal Monte Carlo
intervals, 51 descriptive power marginal Monte Carlo intervals, six descriptive
48-/96-date frontier rate intervals, twelve descriptive reliability-0.96--0.99
frontier rate intervals, one family Clopper--Pearson interval, one family Wilson
interval, 51 recovery t intervals, three IID t intervals, and 31
published-recovery intervals. The 7,431 research
finalizations are 51 smooth events plus all 7,200
entries of the eight reported paper coefficient maps and 180 response-level
OOS R-squared values. The ninth cached matrix (`mean P_perp`) and 360 cached
SSE/SST components are internal inputs, not separately claimed results.
The 459 null marginals use unadjusted, one-sided 95% Clopper--Pearson upper
endpoints; the 51 power marginals use unadjusted, one-sided 95% Wilson lower
endpoints. Each of the six candidate-by-date and twelve
candidate-by-extra-reliability frontier passage rates uses an unadjusted,
one-sided 95% Wilson lower endpoint with denominator 100. All 528 marginal and
frontier intervals are descriptive and non-gating, while the two family
intervals alone license size/power behavior.

Each phase has one startup invocation. Four fresh resource-only subprocesses
run the zero-work config/preflight/checkpoint-inventory path for validation and
research; `t_startup,p` is the maximum of the four wall times. These probes do
not instantiate a registered validation or research generator.

### A022--A026 resource-admission authority

Preregistration amendment A022 supersedes the original bundle paragraphs
below, A023 narrows A022's transfer interpretation, and A024 freezes operand
lifetime, record order, cleanup journaling, and replay. A025 closes the
remaining receipt, cleanup, interruption, RNG-lifecycle, telemetry, and
terminal-publication state-machine gaps, the replay-comparator selection gap,
and the later hostile findings on durable child birth, Darwin absence evidence,
watchdog provenance, final-boundary adoption, and terminal-file size before
implementation. A026 then closes interruption-tainted rate evidence, launch-
only quiescence, and terminal-entry consumed-no-outcome states. The historical
paragraphs remain diagnosis only and must not be implemented or used for
admission. A022--A026 preserve the
fourteen kernels, common slower-normalized kernel-13 rule, complete `W`,
startup probes, budgets, hard stops, and fixed trace vectors, but replace the
one-unit bundle, last-three rate, and scalar projection with the
operand-complete cold/equal/phase experiment and exact integer formulas in:

- `docs/derivations/GATE_G2_RESOURCE_ADMISSION.md`; and
- `docs/derivations/GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md`.

If the historical prose below conflicts with A022--A026, the later amendment
controls. In particular, registered execution may not use one-unit bundles,
last-three-bundle throughput, binary64 rate division, the old scalar `v_k`
formula, or claim that the fixed phase traces validate transfer to the full
`W` mixture. Final phase projections are explicitly conditional on per-kernel
linear extrapolation. Six same-phase held-out rows test temporal stability;
72 opposite-phase rows test per-kernel and aggregate robustness only for
kernels `1..10,14`. All six temporal and 72 cross-context rows are one-sided
replay-monotone comparisons: predictor/reference operands use `Rplus`, while
held/current operands use `Aplus`.

Receipt order is
`k1,k2,k3,k4,k5,k6,k7,k9,k10,k8,k11,k12,k13-recovery,k13-research,k14`;
k1+k2 share the first work boundary.

For the existing 13-word DGP address `D(s,d,c)` and bootstrap address
`B(s,r)`, successful RNG calls occur only in this record-position order:
position 0 uses
`[D(resource_smooth,d,c) for d in 0..251, then c in 1..5]`; position 2 uses
`[B(resource_smooth,r) for r in 0..24]`; positions 10 and 11 respectively use
the five `D(resource_paper,0,c)` and `D(resource_paper,1,c)` calls when their
unit is positive; and the first positive kernel-13 position uses
`[B(resource_paper,r) for r in 0..24]`. Every other position is empty. The
exact 15-position call-count vectors are:

```text
equal/rehearsal [1260,0,25,0,0,0,0,0,0,0,5,5,25,0,0]
validation      [1260,0,25,0,0,0,0,0,0,0,0,5,25,0,0]
research        [1260,0,25,0,0,0,0,0,0,0,5,0,0,25,0]
```

Their order is date-major/component-ascending for DGP calls and
replicate-ascending for bootstrap calls; no successful inventory or replay
copy may sort, deduplicate, or reconstruct a different sequence.

A022--A026 also make the repository's ten-minute recovery rule quantitative.
A canonical uninterrupted or rehearsal trace has one initial worker-ready
boundary, one boundary after the indivisible k1+k2 epoch, and one after each of
the remaining 13 records: 15 boundary leaves with next-position vector
`[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15]`. Each rehearsal also has four
cleanup-intent markers, so the three fixed rehearsals expose 45 boundary
leaves and 12 cleanup intents: 57 capped ordinary checkpoint intervals. A025
adds one root terminal accounting row, yielding 58 resource-accounting rows in
total. The earlier unqualified 57-row statement is historical; 57 remains the
correct ordinary-checkpoint count.
An interruption inside any cold/equal/validation/research rate-bearing trace
selects terminal failure, contributes no rate operand, and cannot add a
replacement trace. An interruption between completed rate traces may add a
worker-ready recovery leaf without advancing the measurement schedule, but a
later warm trace first requires an uninterrupted fresh 600-second thermal
cycle. Registered trace and measurement receipts are followed by their own
boundaries.

Work from one checkpoint/work marker through the next cutoff is capped at 480
seconds; atomic marker publication has a 60-second upper, so the maximum
durable-marker interval is 540 seconds. Governance receipts do not reset that
clock. A partial rate-bearing trace is retained only as failure evidence and
never enters admission. The replay-penalty formulas remain deterministic
falsifiers for any durable record, but A026 requires every successful
rate-bearing trace to be uninterrupted, every admitted rate record to have
`replay_count=0`, and therefore `Rplus=Aplus`. At record `i`,
`Rplus_i=duration_plus_ns_i=D_i+2*h_i` and
`Aplus_i=admission_duration_plus_ns_i=Rplus_i+480000000000*r_i`.
Predictor/reference operands use only `Rplus`; held/current operands and every
cold, conservative/projected task, block, phase, combined, or final absolute
projection or budget use `Aplus`. Raw `D` remains the diagnostic and
successful-work stop clock. Incrementing any replay count with raw durations,
units, and clock resolution fixed must leave every reference prediction
unchanged; among timing comparator and projection operands it may only weakly
increase affected held/current and absolute-projection operands, and it must
never change an acceptance Boolean from false to true. An uncommitted artifact final is
inventoried and deleted before replay, while only an exact marked trace or
measurement receipt may complete its uniquely derived following boundary.
Successful completed work, not replay penalty, controls the 600-/200-second
warmup stops. Bootstrap from the first supervisor instruction through durable
`attempt.json` also has a 480-second watchdog. These rules supersede any
historical whole-bundle restart implication below.

The durable resume state has exactly seven rows: base panel, cell panel,
smooth bootstrap weights, oracle focals, homogeneous focals, observable
focals, and one role-resolved paper-bootstrap-weight row. The smooth rows have
producer/last-consumer/cleanup positions
`0/8/9,1/8/9,2/5/9,3/9/9,4/9/9,5/9/9`. The paper row is one immutable
`resource-resume-paper-bootstrap-weights-v1` artifact of shape `(25,252)`,
drawn at the first positive kernel-13 position, shared by both positive equal
variants, and deleted by the last positive kernel-13 position's cleanup
intent. Its producer/last-consumer/cleanup positions are `12/13/13` for
equal/rehearsal, `12/12/12` for validation, and `13/13/13` for research; a
zero-unit variant draws nothing. A successful three-panel rehearsal therefore
retains exactly 13 artifact-kind counts and 51 artifact rows.

A025 normalizes ordinary receipt recovery before any transition. A receipt-only
valid stage is completed; a valid complete staged pair is no-overwrite renamed
and parent-fsynced; a valid visible final is reused. Only a successor that first
proves the encoded publisher dead may adopt a valid stage. Marker-only,
partial, corrupt, extra-entry, mismatched, and conflicting states remain
forensically incomplete. Every adoptable claim/receipt encodes and revalidates
that unique publisher. Worker-birth stages, the registered
`terminal_entry=true` final block-3 boundary, the final rehearsal boundary,
and cleanup-complete final failure-resume stages are non-adoptable after
publisher death. Their same live publisher may finish an exact stage, but a
dead terminal-entry publisher authorizes only A026's immutable terminal-
nonpass intent and never another terminal check or selected/opposite outcome.
A hidden birth stage is not adopted as identity; exact supervisor death plus
fresh-open acquisition of the launch-intent's stable `flock` lease instead
selects pre-RNG failure. Cleanup and debris are
entry-level, not whole-leaf:
the immutable sequence is child-before-parent; file rows bind mode, logical
and allocated bytes, and SHA256; directory rows bind type/mode with null
byte/hash fields. A legal crash state has one exact absent row prefix, a
byte-valid remaining suffix, and no extra path. Chained interruptions retain
the target/row bytes while advancing the completed-prefix count and
remaining-suffix digest from the actual filesystem. Entry membership uses the
unique deepest matching target; terminal root fallbacks own every remaining
ancestor/ordinary entry; target slices are positive and contiguous; and every
checkpoint/scratch mutation first passes the prospective 512-row plan.

Terminal-failure selection remains immutable before deletion, but cleanup is
now checkpointed. Between one and 641 contiguous failure-resume receipts are
mandatory, including a final receipt published only after every cleanup row is
absent and every parent fsync is durable. Resume zero names predecessor kind
`"failure-intent"` and its digest; each successor names `"failure-resume"` and
the immediately preceding receipt. Each receipt binds prior durable
wall/perf/cumulative anchors, current resume and cutoff samples, the same-boot
monotonic or cross-boot wall gap, current active work, and the exact cumulative
sum. Every segment samples resume after predecessor publication/adoption and
before its first deletion/fsync, then samples cutoff after all prefix work and
fsyncs charged to that segment. Resume zero has prefix count zero and is
cleanup-complete iff the intent has zero entries. Cleanup work is at most 480
seconds; each failure-intent/resume row receives a fixed 60-second publication
accounting charge; and the accounted sum is at most 540 seconds. The charge is
not an observed or enforced receipt-close latency bound. Every later nonfinal
receipt advances the cleanup prefix or binds a
newly dead publisher. A dead-publisher nonfinal stage may be
adopted and bound by the next receipt only with a remaining slot/death row,
but a last-slot nonfinal stage is forensically incomplete rather than
duplicated. An exact cleanup-complete stage is never adopted as failure; after
publisher death it may only select terminal nonpass.

Success, failure, and forensic nonpass each become visible only as one atomic
terminal outcome directory:

```text
terminal/success/{result.json,_SUCCESS}
terminal/failure/{failure.json,_FAILURE}
terminal/nonpass/{nonpass.json,_NONPASS}
```

Nonpass is legal only after an exact success/failure terminal-entry object and
publisher death or live post-entry failure. Its ordinary
`resource-terminal-nonpass-intent-v1` binds the selection and a stable locked
`publication.lock`; the two outcome files are pure functions of that intent,
contain `admission_pass=false` and `retry_permitted=false`, and can be rebuilt
byte-for-byte by a successor that freshly acquires the same lock inode. It
runs no Git check, RNG, kernel, timing, or opposite-outcome publication.

Exactly three non-overlapping twelve-child Git checks are legal in a complete
terminal attempt. Before the first worker starts, the bootstrap check is
reaped and persisted in `attempt.json`. Intermediate source and Git-control
seals are subprocess-free and reconstruct stable bytes against the bootstrap
enumeration. They run before and after sealed contract/resource-config loading,
immediately before and after every nonterminal resource-root mutation, before
every worker capability, and after every measurement block; they may select
ordinary failure before terminal entry but may not launch Git. After every
issued worker identity is closed, no worker is alive, and every currently
waitable direct child has been reaped,
publication of the final success boundary or cleanup-complete final
failure-resume receipt is the non-resumable terminal-entry point. The same
publisher then runs and reaps the terminal-pre-JSON check before hidden-stage
construction. Terminal JSON
persists the bootstrap check digest, the complete terminal-pre-JSON check, and
their count-two inventory/hash. The 24 preterminal
wait/rusage/stdout/stderr/parsed rows remain jointly reconstructible from
`attempt.json` plus terminal JSON. Its cumulative rusage high-water envelope
adds the supervisor high-water to the larger of the cumulative worker
`ru_maxrss` high-water and the high-water over those 24 Git children. Observed
RSS is the maximum of the sampled process-tree peak and that envelope, and the
admission upper then applies the 25% current margin and carried durable-upper
maximum. Bootstrap Git high-water is present at every durable cutoff,
terminal-pre-JSON joins only at the terminal cutoff, and post-JSON Git rusage
remains in the marker's separate publication envelope. Missing or incomplete
bootstrap evidence fails before entry; missing or incomplete terminal-pre-JSON
evidence after entry forbids retry and selects terminal nonpass.

Before either terminal-entry receipt is published, it carries a schema-bound
terminal-size preflight. The registered success boundary checks
`result.json/_SUCCESS`; the cleanup-complete failure resume checks
`failure.json/_FAILURE`; and the final rehearsal boundary uses the rehearsal
success schema. The frozen fixture schema separately instantiates
failure-intent, every failure-resume shape, both rehearsal and registered
success/failure JSON shapes, and both markers with all applicable maxima:
64 waits, 128 deaths, 512 cleanup rows, 641 resumes, 240-byte paths, 24
preterminal Git rows, 12 post-JSON Git rows, and 1,201 publication-RSS
samples. A026 adds maximum-width nonpass intent/JSON/marker and fixed-lock
fixtures, with the intent capped at 131,072 bytes. Every exact canonical file
must remain at or below 1 MiB and every
one-past mutation fails before publication. A missing or failing success
preflight selects ordinary failure before terminal entry; after failure
selection, a missing or failing final preflight stops before the final resume
or terminal-stage mutation.

The accounting cutoff follows the terminal-pre-JSON check. The hidden stage is
then created and its parent fsynced, and the JSON written/fsynced. The third
and distinct twelve-child post-JSON Git check runs under the live sampler; the
marker binds the JSON and persists every Git
wait/rusage/stdout/stderr/parsed-result row, source/Git-control row inventory,
runtime/module/boot/publisher identity, publication-local sampler rows, and
recomputed 25%-margin RSS upper. No other Git subprocess is legal, and no Git
child may overlap a worker or another Git child. After marker/stage fsync, a
no-subprocess final seal recomputes those identities, proves no descendants,
waits for a post-guard sample, stops/joins the sampler, requires only the
publisher thread to remain, and takes the final self-resident/RUSAGE_SELF
sample. Every final gap is at most one second, observed RSS is at most 2.8 GB,
and the recomputed 25%-margin admission upper is at most 3.5 GB; only then does
it license the no-overwrite rename and terminal-parent fsync. This remains a
sampled empirical envelope: child high-water evidence covers short child
spikes, but 25% headroom does not prove that a sub-sample publisher spike is
impossible.

Success measures at most 480 seconds from the final durable boundary through
the pre-JSON cutoff and assigns the later publication suffix a fixed 60-second
accounting charge. Failure uses the same charge after its mandatory final
cleanup-complete receipt. The resulting at-most-540-second sum is an accounted
value, not a bound on end-to-end terminal latency. Neither branch admits a
visible JSON without its marker, post-terminal work, or a post-success
rehearsal cleanup suffix; `TC` and `TS` remain immutable success evidence.
Forward cutover occurs only after exclusive stage creation and successful
terminal-parent fsync; an absent post-crash stage from the intervening window
is pre-cutover, while an exact surviving stage conservatively locks its kind.
The terminal-entry publisher must remain continuously alive from publication
of the final success boundary or final failure-resume receipt through
outcome-directory visibility. If it dies, if the terminal-pre-JSON check fails
or is incomplete, or if any later publication step fails, no successor may
retry a Git check, publish the selected outcome, or select its opposite. The
only close is the successor-rebuildable terminal nonpass bound to the original
entry and death/failure evidence. An exact visible success/failure final is
reusable only after a current-live terminal-parent fsync. Terminal JSON and the marker
certificate bind the publisher. The fixed 60 seconds are a conservative
accounting charge, not an observed or enforced
marker/final-seal/rename/parent-fsync latency upper; visible-directory existence
attests the final seal.

Every attempt binds the initial supervisor PID, kernel start identity, and boot
digest. Every superseded process identity is proved dead exactly once by one
of three byte-authoritative methods. Each claimed-worker `wait4` first appends one
cumulative hash-bound row carrying claim/identity, raw status, byte-normalized
`ru_maxrss`, post-wait sample, and deadline. `attempt.json` plus complete
terminal JSON jointly bind the 24 preterminal Git-child wait rows, and the
marker binds the 12 post-JSON Git-child wait rows. `wait4-reaped` binds that
same worker row;
`double-process-identity-absence` with two same-boot checks at least 50 ms
apart and null wait/rusage/deadline fields; or `boot-identity-changed` with
unequal boot digests and null perf/wait/rusage/deadline fields. Kernel 14's
receipt probe is work within its ordinary worker, not a process role. Git
children are wait-only, so missing Git wait/rusage evidence is forensically
incomplete and cannot be replaced by a worker death proof. A reservation permanently
retains its creator claim. An initial capability requires direct
payload/claim/reservation/worker-ready equality; a resumed capability requires
payload/current-claim/worker-ready equality plus a finite gap-free backward
walk to the unique immutable creator claim, with every suffix link authorized
by one contiguous interruption. Process-death identities are deduplicated
attempt-wide across interruption, failure-intent, and failure-resume receipts.

Before every spawn, the supervisor durably publishes a launch intent containing
the nonce commitment and an arithmetically derived 480-second work deadline
plus a distinct 60-second reap deadline. That atomic intent also contains the
exact mode-`0600` `quiescence.lock`; the supervisor holds its exclusive Darwin
`flock` before visibility and the bootstrap child inherits the sole duplicate
open-file-object reference. The child also inherits a parent-liveness
descriptor and publishes its PID/start/boot birth record as
its first durable action; only a validated launch/birth pair may enter a worker
claim, reservation, worker-ready boundary, and capability release. A complete
birth must later join an exact wait/death proof. Every boundary, cleanup
intent, or interruption that can precede worker work persists the next arm
before that work; wait/death evidence references the exact arm digest and may
not invent or recompute a deadline. Launch-only code may not unlock, reopen,
duplicate, pass, leak, unlink, or replace the lease or spawn descendants. A
same-boot successor may select failure only after proving the supervisor dead
and acquiring `LOCK_EX|LOCK_NB` through a fresh no-follow open of the same
bound inode; `EWOULDBLOCK` authorizes no mutation.

Darwin double-absence evidence uses two zeroed-buffer
`proc_pidinfo(PROC_PIDTBSDINFO)` observations 50 ms to 1 s apart. Only
zero/`ESRCH` twice or two full reads naming the same stable replacement
PID/start identity prove absence. Presence of the target, mixed classes,
changing replacement identity, permission error, ambiguous zero/zero, short
or oversize read, malformed struct, PID mismatch, ABI failure, or boot change
between samples fails that method. The common verdict/replacement identity is
factorized once with two raw `[time,return_bytes,errno]` samples so the
maximum canonical process-death row is reproducibly within its 512-byte cap.

An interruption inside any rate-bearing trace selects terminal failure; the
trace cannot complete, resume, or be replaced and contributes no timing
operand. An interruption strictly between completed rate traces preserves the
earlier evidence but resets thermal qualification. Before any later warm
trace, fresh contiguous panels in the
`validation,research,research,validation` cycle must contribute at least 600
uninterrupted successful seconds. Interruption inside that recovery discards
the partial thermal trace and restarts the cycle and clock from zero. No reset
work is needed when no later warm trace exists.

Telemetry pass authority comes only from durably closed process segments.
Abrupt supervisor loss or direct boot loss uses predecessor-close method
`"unknown-loss"` and assigns the exact fail-closed uppers RSS
`3,500,000,001`, checkpoint tree `2,000,000,001`, created roots
`6,000,000,001`, and absolute workspace `30,000,000,001` bytes. It selects
`"select-terminal-failure-telemetry-gap"` before another worker, capability,
RNG call, or thermal trace. Complete segments carry the maximum of their prior
durable upper and current observed margin without relabeling a bound as a
sample or applying the 25% margin twice; the separate 1.6-GB pre-mutation
checkpoint ceiling remains binding.

Evidence is finite by construction: at most 64 launch intents, 64 worker
births, 64 worker claims, 63
interruptions, 4,096 traces, 641 failure resumes, 512 terminal-cleanup rows,
128 attempt-wide process-death rows, 64 cumulative worker-wait rows, and 240
ASCII bytes per canonical path. Cleanup, death, and worker-wait rows encode in
at most 1,024, 512, and 512 canonical bytes. The 131,072-byte non-row term is
the exact failure intent with all three row arrays replaced by `[]`, including
all delimiters/enclosures. Hence the intent envelope is at most
`512*1024 + 128*512 + 64*512 + 131072 = 753,664` bytes, below the 1,048,576-byte root
receipt cap. Before failure selection, reaching a cap selects preregistered
terminal failure before the one-past object is created. After selection,
resume/death/encoding-cap exhaustion stops the consumed failure as
forensically incomplete before mutation.

The active A026 config seal is exactly 9,799 ASCII bytes, SHA256
`3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
194 leaf-type rows, and type-tree SHA256
`e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.
The maximum nonpass intent is 131,072 bytes. Successful rehearsal counts remain
`3/45/12/57+1/58/13/51/7`. Fresh methods, systems, and schema reviews must pass
this A022--A026 package before any test-seed implementation.

### Historical bundle design — superseded by A022

The first complete hash-checked bundle supplies each kernel's cold region
time. The benchmark then repeats the identical bundle with distinct resource
panel indices until at least 600 post-cold seconds and four total complete
bundles have finished. The cold bundle contributes to the four-bundle total but
not to the 600-second warm clock. Warm throughput is the aggregate throughput
of the last three complete bundles. For each kernel `k`,

One bundle runs one unit of kernels 1--12 and 14 in the listed order. Kernel 13
runs both one 25-replicate/960-field recovery batch and one
25-replicate/8,460-field research batch; its normalized rate is the minimum of
the two size variants before the cold/warm rule. Paper-date units include
serialize/reload/hash of their date summaries. A new resource panel index is
used for every bundle.

```text
v_k = min(v_warm,k, 0.60 * v_cold,k).
```

For phase `p`, with every planned work count mapped to exactly one kernel,

```text
T_hat_p = 1.25 * {t_startup,p + sum_k W_p,k / v_k}.
```

Missing regions, hash mismatches, incomplete bundles, or unmapped work counts
invalidate the benchmark. The report separately projects the longest panel,
cell, bootstrap batch, paper date, and checkpoint task against the 480-second
cap, and measures RSS and steady/transient disk. Validation cannot access its
seed unless all projections fit.

Preflight slack cannot be borrowed from a hard stop. Actual benchmark elapsed
must be at most one expected hour (and two hard hours), projected validation
must be at most 12 expected hours, projected research at most three expected
hours, and actual benchmark elapsed plus both projections at most 16 expected
hours. The 24-/6-/32-hour figures remain runtime kill thresholds if realized
work is slower; they do not rescue a failed expected projection.

Any nonfinite statistic, invalid PCA, declared required-full-rank/conditioning
failure, declared `fail_cell`/`fail_response_cell`, LASSO nonconvergence,
incomplete bootstrap vector, or missing mapped work unit fails the license
immediately. It is not counted as a convenient null nonpass and no panel, cell,
response, block, or replicate may be dropped.

## Budgets and stops

| Subphase | Expected | Hard | Seed consequence on failure |
| --- | ---: | ---: | --- |
| Resource benchmark | 1 h | 2 h | validation and research remain sealed |
| Smooth + `CI_I` recovery validation | 12 h | 24 h | no validation-seed retry |
| Frozen smooth + six-spec research | 3 h | 6 h | no research-seed retry |
| **Total** | **16 h** | **32 h** | G2 remains unpassed |

Additional hard stops:

- process RSS: `3.5 GB`;
- checkpoint allocation: `2 GB`;
- one panel/cell/paper-date task: `480 s`;
- one bootstrap batch: `480 s`;
- bootstrap batch size: 25, with a final batch of 24;
- at 80% of a subphase hard budget, stop if measured completion projection
  exceeds the cap;
- single-threaded BLAS; one thermally heavy process; `caffeinate -i` for a long
  foreground run, without relying on it for recovery.

Every success-last checkpoint binds the raw config hash, both target hashes,
the LASSO-ratio hash, tracked execution-source digest, numerical-runtime fingerprint, its
kind-specific complete RNG-address domain, completion inventory, resource
telemetry, and payload hash. Date-panel artifacts bind all five DGP component
keys over the exact complete half-open date range and have no replicate range;
bootstrap artifacts bind their exact parent coordinates and half-open replicate
range. The versioned variant rules are derived before each variant becomes
executable; `docs/derivations/GATE_G2_CHECKPOINT_AUTHORITY.md` licenses only
base-panel and cell-panel variants before A022. On resume, cumulative time
reloads exactly; actual pre-boundary RSS/disk observations and nondecreasing
conservative boundary resume uppers reload separately, so restarting cannot
reset a stop or relabel an upper observed. The 2 GB allocation applies
to the complete active phase checkpoint tree, including simultaneous staging
bytes, rather than to each artifact independently. A root-wide advisory
reader/writer lease serializes cooperating access; every lock, prefix, stage,
file, and rename mutation is conservatively reserved before it occurs and
checked against actual logical and allocated usage immediately afterward.

## A027 paper-cache coordinate plan

The research date vector now has one exact coordinate system. Columns
`0:8100` are the nine declared 30-by-30 matrices in declared order, each
flattened as response/output row then flow/input column. Columns `8100:8460`
are the six declared specifications, then response, then `(SSE,SST)`. The
compact recovery vector places the `CI_I` matrix in `0:900` and its loss pairs
in `900:960`; it is not a prefix of the research vector. Its full-vector
projection selects `2700:3600` and `8280:8340`.

This closes representation order only. It does not change the 8,460/960 work
counts, cache shapes, bootstrap term counts, NPY envelope, or phase budget.
The active A027 resource config is 10,863 bytes with SHA256
`1a14fd68012819d5f901a97ddd9e9a58dd35886bdcc5d47728467f6417fc3cd3`;
its 209-row type tree has SHA256
`81eed87be58bf04a897fdcf3dd39cf142944647824a9f97938d46f341803a2ff`.
Only deterministic in-memory order/codec tests are licensed after independent
review. Artifact serialization, fixtures, rehearsal, and registered access
remain blocked.
