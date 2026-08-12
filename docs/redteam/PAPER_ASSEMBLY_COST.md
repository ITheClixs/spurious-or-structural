# Resource finding — the registered paper workload is far over budget

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

## What it implies for the registered workload

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

**Establishes:** the current pure-Python coordinate-descent implementation
cannot execute the registered workload within the registered envelope, by a
factor of roughly 24 against the hard stop.

**Does not establish:** that the *design* is infeasible. The gap is an
implementation-throughput gap, and several routes remain open, none of which
this memo endorses or costs:

1. A compiled or vectorised coordinate descent. A 24-to-48-fold speedup is
   plausible for this kernel, which is the range required, but it must be
   measured rather than assumed, and it must reproduce the sealed numerics
   exactly or it is a different estimator.
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
