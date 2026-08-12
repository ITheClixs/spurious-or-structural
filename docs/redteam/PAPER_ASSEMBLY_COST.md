# Resource finding — the paper workload needs a machine this one is not

> **CORRECTION, same day.** The first version of this memo concluded that the
> registered workload was 48x over budget and that the plan was infeasible.
> **That conclusion was wrong.** It divided the workload by a single core
> without checking the sealed configuration, which registers
> `maximum_worker_count = 64`. At the registered worker count the workload fits
> the registered envelope. The corrected analysis is in the section
> "Corrected: the envelope is a provisioning requirement" below, and the
> original single-core arithmetic is retained beneath it because it is still
> the correct per-core price. The error was mine and it inverted the headline
> finding.

Recorded 2026-08-12 during the A031 assembly implementation, before any
rehearsal or registered run. This is a measurement, not an estimate, and it
changes what the project can claim about G2 feasibility.

## What was measured

A single warm-started 40-ratio LASSO path over the sealed grid, on a realistic
structured feature block: 24 training bins, 30 penalized flow columns, built
from a common-factor plus level-correlation panel through the actual
`fit_paper_feature_transform` and `apply_paper_feature_transform` kernels.

Solver settings are the sealed ones: coordinate-descent tolerance `1e-10`,
KKT tolerance `1e-9`, maximum `10,000` sweeps.

| Quantity | Measured |
| --- | ---: |
| Full 40-ratio warm path | 3.356 s |
| Per-solve median | 45.2 ms |
| Per-solve maximum | 259.4 ms |
| Sweeps, median | 413 |
| Sweeps, maximum | 2,146 |
| Solves hitting the 10,000-sweep cap | **0 / 40** |

**The solver is not misbehaving.** No solve approaches the iteration cap and the
median converges in 413 sweeps. This is the normal cost of the registered
numerics, not a pathological case that a better fixture would remove.

## Corrected: the envelope is a provisioning requirement

The sealed resource configuration registers `maximum_worker_count = 64` and
`single_thread = true` with every BLAS thread variable pinned to one. The design
therefore parallelises across processes, not within them, and the workload must
be divided by the worker count rather than run on one core.

| Workers | Wall time | Against the envelopes |
| ---: | ---: | :--- |
| 1 | 763 h | — |
| 16 | 47.7 h | exceeds the 32 h hard stop |
| 32 | 23.8 h | fits the 32 h hard stop |
| **48** | **15.9 h** | **fits the 16 h expected cap** |
| 64 | 11.9 h | fits comfortably |

**The registered design is feasible within the registered envelope.** It
requires about 24 cores to fit the hard stop and about 48 to fit the expected
cap, against a registered maximum of 64 workers.

**It is not feasible on the development machine**, which has 10 cores and would
take about 76 hours, well past the hard stop. That is a provisioning
requirement, not a design defect and not an amendment. G2 execution needs a
host with at least 48 cores.

## Single-core price, which is what was actually measured

`docs/G2_COMPUTE_PLAN.md` enumerates the solution counts but never prices a
solution. Applying the measured median:

| Quantity | Value |
| --- | ---: |
| Registered research LASSO solutions | 45,586,800 |
| Registered recovery LASSO solutions | 15,195,600 |
| Total | 60,782,400 |
| At 45.2 ms per solve | **763 hours, 31.8 days** |
| Expected envelope | 16 hours |
| Hard envelope | 32 hours |
| Overrun against expected | **48x** |
| Overrun against hard | **24x** |

Equivalently, fitting the registered LASSO count inside the 16-hour expected
envelope requires **948 microseconds per solve**, against **45,200 measured**.

This excludes the 26,405,400 smooth candidate fits, which are additional.

## Why this was not caught earlier

The compute plan counts solutions and normalises unequal paper caches, but no
document in the project states a per-solve cost, and no measurement existed
until now. The plan therefore validated the *shape* of the workload without
pricing it. A022 resource admission exists precisely to catch this class of
error before a registered run, and it has: the gate is executable-red and no
registered stream has been opened.

The cost of the omission is bounded. No registered seed was consumed and no
rehearsal was launched against an infeasible plan.

## What this does and does not establish

**Establishes:** the per-core price is 45.2 ms per solve, so the registered
workload needs roughly 24 cores to fit the hard stop and 48 to fit the expected
cap. The development machine has 10 and cannot host the run.

**Does not establish:** that the design or the budget needs amending. Neither
does. The following routes were considered and are recorded only so the
reasoning is not repeated:

1. A compiled or vectorised coordinate descent. Measured and bounded: 92% of
   the per-solve cost is removable Python and NumPy wrapping, but `np.dot`
   defines the reduction order and costs 3.5 ms of the 45.2 ms, so the maximum
   speedup that stays bit-identical while keeping `np.dot` as a Python call is
   **13x**. That is short of 24x and was not needed once the worker count was
   accounted for.
2. Solving the 40-ratio path as a single vectorised sweep across ratios rather
   than 40 sequential calls, preserving the warm-start order.
3. Reducing the registered workload, which would be a scientific amendment and
   not an optimisation.
4. Accepting a longer envelope, which is a governance decision and would
   require re-registering the budget.

## Required next action

The A022 quantitative prediction seal must not be written against the current
implementation, because the projection it would record is known to be wrong by
more than an order of magnitude. Either a throughput repair lands and is
measured, or the envelope is re-registered, before any resource rehearsal is
scheduled.

Until then G2 stays executable-red for a reason that is now quantitative rather
than procedural.

## Scope

Measurement only. No registered resource seed `2026071529`, validation seed
`2026071521`, research seed `2026071522`, rehearsal, market data, or holdout was
accessed. The benchmark used test seed `1729` on a synthetic panel and produced
no coefficient-to-truth comparison.

---

# Addendum — a rejected optimisation and a protocol defect

Recorded 2026-08-12, same session, after attempting the throughput repair.

## 1. The vectorised solver was tried and is rejected

Responses within a block share the design matrix and the column denominators
and differ only in the response vector and in `lambda_max`, so a coordinate
descent batched across the thirty responses replaces thirty tiny NumPy calls
per coordinate with one. That is the natural repair, and it fails on both of
its acceptance criteria.

**It is not bit-identical.** Batching turns each per-response `np.dot` into a
column of a matrix product, and BLAS reduces a GEMV differently from a DOT.
Measured maximum absolute coefficient differences against the sealed scalar
solver were `2.220e-16`, `7.216e-16`, and `2.734e-15` at ratio indices 0, 10,
and 20. The differences are tiny, and that is beside the point: the sealed
numerics define the estimator, so a solver that does not reproduce them
exactly is a different estimator and would require re-registration rather than
adoption.

**It is not fast enough either.** Observed speedups were `33.7x` at ratio index
0 but `5.2x` and `5.0x` at indices 10 and 20, because a batched sweep must keep
iterating until the *slowest* response in the batch converges, so total work is
set by the worst response rather than by the sum. Against the `48x` required to
reach the expected envelope, a `5x` repair does not close the gap even if the
exactness problem were solved.

**Not adopted.** The batched solver is not added to the codebase.

## 2. A protocol defect: the mandated outer refit does not converge

`GATE_G2_PREMISE.md` line 493 requires that fold paths warm-start in descending
penalty order while **every outer refit begins at zero**. Convergence from zero
degrades sharply as the penalty shrinks, on the registered fold geometry of 24
training rows against 30 penalized columns:

| Ratio index | Penalty | From zero | Warm-started |
| ---: | ---: | ---: | ---: |
| 0 | 1.000e+00 | 1 sweep | 1 |
| 10 | 9.427e-02 | 203 | 177 |
| 20 | 8.886e-03 | 625 | 549 |
| 25 | 2.728e-03 | 1,905 | 1,577 |
| 30 | 8.377e-04 | 3,641 | 1,436 |
| 35 | 2.572e-04 | 8,706 | 1,326 |
| **39** | **1.000e-04** | **fails at the 10,000 cap** | **1,171** |

The warm-started path converges at every ratio. The from-zero path fails at the
smallest sealed ratio, with a final maximum update of `4.56e-08` against a
`1e-10` tolerance and a KKT violation of `4.47e-08` against `1e-9`.

**Consequence.** If cross-validation selects a penalty at or near the bottom of
the sealed forty-ratio grid, the mandated outer refit from zero raises rather
than returning, and by the A031 fail-closed rule that fails the date. This is
not an implementation bug: the from-zero requirement is explicit in the
registered protocol, and the solver is behaving as specified.

The defect was invisible in the earlier forty-ratio benchmark because that
benchmark warm-started throughout, which is the fold path rather than the outer
path. Only the outer refit is affected.

**Required decision.** Either the sweep cap is raised, which worsens the
already-failing cost projection, or the outer refit is permitted to warm-start,
which changes the registered estimator and needs an amendment, or the ratio grid
is truncated above the failing region, which is also an amendment. None of the
three is an implementation choice, and none is made here.
