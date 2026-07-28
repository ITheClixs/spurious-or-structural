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
base-panel and cell-panel variants before A022. Cumulative time and maximum RSS
reload on resume so restarting cannot reset a stop. The 2 GB allocation applies
to the complete active phase checkpoint tree, including simultaneous staging
bytes, rather than to each artifact independently. A root-wide advisory
reader/writer lease serializes cooperating access; every lock, prefix, stage,
file, and rename mutation is conservatively reserved before it occurs and
checked against actual logical and allocated usage immediately afterward.
