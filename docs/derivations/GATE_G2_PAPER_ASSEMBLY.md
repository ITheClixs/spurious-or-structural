# Semantic paper-matrix assembly

## Claim being derived

`GATE_G2_PREMISE.md` fixes the six-specification protocol, the eleven-block
train/score schedule, and the five contiguous six-bin folds.
`GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md` fixes the artifact envelope, and A027
fixes the field-to-column bijection. `src/xid/models/g2_paper.py` implements the
kernels and `src/xid/models/g2_paper_cache.py` implements the codec.

Nothing yet states how the kernels compose into the nine matrices and the six
loss tables that the codec consumes. That composition is currently the only
undefined step between an issued date panel and a
`PaperResearchDateCache`, and inferring it from the kernel signatures would
allow a silent mis-assignment: a purged operator written into a full-response
slot, or a specification's coefficients written into a neighbouring
specification's rows, would both produce a numerically plausible cache.

This document fixes that composition before it is implemented.

## Inherited authority, not restated here

The following are already binding and are **not** re-derived:

- eleven 30-minute blocks per date, blocks 0--9 fit and blocks 1--10 score
  (`GATE_G2_PREMISE.md`, line 466);
- five contiguous six-bin validation folds with complement training and a
  common ratio-index grid (line 468);
- per-fold refit of preprocessing on its 24 training bins (line 483);
- fold paths warm-start in descending penalty order while every outer refit
  begins at zero (line 493);
- original-unit coefficients and training-defined transforms score the next
  block (line 537);
- PCA uses float64 training-column centering (line 542);
- out-of-sample loss pools next-block SSE against a training-mean benchmark,
  averaged within date and then equally across dates (line 553).

Any conflict between this document and those clauses resolves in favour of the
earlier clause.

## 1. Assembly order

For one date, assembly proceeds in exactly this order, and the order is part of
the contract because a different order changes which floating-point reduction
is performed:

```
for outer_block in 0..9:                      # ascending, no exceptions
    fit training transforms on outer_block
    for spec in (PI_1, PI_I, CI_1, CI_I, PI_CC, CI_CC):   # sealed spec order
        for response in 0..29:                # ascending asset index
            fit the specification's estimator
            score block outer_block + 1
```

Specification order is the sealed A027 loss order
`(PI_1, PI_I, CI_1, CI_I, PI_CC, CI_CC)`. Response order is ascending sealed
asset index. Both are fixed so that a reordering is a contract violation rather
than a performance choice.

## 2. Which estimator each specification uses

| Spec | Feature map | Estimator | Unpenalized | Penalized |
| --- | --- | --- | --- | --- |
| `PI_1` | own best-level OFI | `fit_full_rank_ols` | intercept, own flow | none |
| `PI_I` | own integrated top-ten OFI | `fit_full_rank_ols` | intercept, own flow | none |
| `CI_1` | all best-level OFIs | LASSO path | intercept | all 30 flows |
| `CI_I` | all integrated top-ten OFIs | LASSO path | intercept | all 30 flows |
| `PI_CC` | cross-sectional PC1 and own residual | `fit_full_rank_ols` | all columns | none |
| `CI_CC` | that PC1 and all residual OFIs | LASSO path | intercept, PC1 | all 30 residuals |

The LASSO path is `prepare_lasso_problem`, then
`solve_lasso_coordinate_descent` across the sealed 40-ratio grid, then
`select_lasso_ratio` on pooled fold validation error, then one outer refit from
zero at the selected ratio, then `reconstruct_lasso_coefficients` to
original units.

## 3. Coefficient placement, the step that was undefined

Let `C_spec^(b)` be the `30 x 30` matrix whose row `i` holds the original-unit
flow coefficients of response `i` under a specification fitted on outer block
`b`, with column `j` the coefficient on asset `j`'s flow. Rows are responses and
columns are flows, matching A027's stated orientation.

`GATE_G2_PREMISE.md` line 553 requires that coefficient operators are averaged
equally across the ten blocks within a date. Every cached matrix below is
therefore the equal-weight block mean

```
C_spec = (1/10) * sum over b in 0..9 of C_spec^(b),                    (A)
```

and the average is taken **after** each block's operator is fully formed in
original units, never by averaging intermediate scaled or residualised
quantities. For the cross-sectional specifications the product forming the
full-response operator is likewise taken per block and averaged afterwards, per
the same clause.

**Direct specifications.** `PI_1`, `PI_I`, `CI_1`, and `CI_I` write directly:

```
PI_1_direct  <- C_{PI_1}     (block mean, Eq. A)
PI_I_direct  <- C_{PI_I}
CI_1_direct  <- C_{CI_1}
CI_I_direct  <- C_{CI_I}
```

For the two own-flow specifications the off-diagonal entries are structurally
absent rather than estimated, and are written as exact `0.0`. Writing an
estimated value there would be a contract violation, and writing `NaN` would be
one too, because A027 requires finite float64 throughout.

**Cross-sectional specifications.** `PI_CC` and `CI_CC` regress on a
cross-sectional PC1 and residual flows, so their flow coefficients are not
comparable to an unrestricted impact matrix without a stated convention.
`GATE_G2_PREMISE.md` already requires that a residual coefficient matrix is not
relabelled as unrestricted, and that purged operators are compared against
`Lambda P_perp`. This document fixes the two matrices that follow from that
requirement:

```
W        = cross-sectional PC1 loading, unit norm, 30-vector
P_perp   = I_30 - W W^T
```

- **Purged operator.** `PI_CC_purged` and `CI_CC_purged` hold the residual-flow
  coefficient matrix as estimated, which is the operator acting on `P_perp`
  flow space. It is compared against `Lambda P_perp`, never against `Lambda`.
- **Full response operator.** `PI_CC_full_response` and
  `CI_CC_full_response` hold the response-equivalent operator on the full flow
  space, formed by adding the factor channel back:

  ```
  C_full = C_purged P_perp + b W^T
  ```

  where `b` is the 30-vector of estimated PC1 coefficients, one per response.
  The product is formed per block, **before** any averaging, and the ten
  resulting operators are then averaged by Eq. (A). Forming the product from
  already-averaged factors would be a different and wrong quantity, because the
  loading changes between blocks.

- **Projection.** `cc_mean_projection_p_perp` holds `P_perp` itself, averaged
  across the ten outer blocks of the date after each block's `W` is computed
  from that block's training rows. The average is of the projection matrices,
  not of the loadings, because `W` is sign-ambiguous and averaging loadings
  would cancel. `P_perp` is invariant to the sign of `W`, which is why the
  projection rather than the loading is the cached object.

## 4. Loss placement

The loss table is `6 x 30 x 2` in specification-major, response-major
`(sse, sst)` order, matching A027's index map `c = 8100 + 60 s + 2 i + l`.

For specification `s` and response `i`:

```
sse[s,i] = sum over scored bins of (y - yhat)^2
sst[s,i] = sum over scored bins of (y - ybar_train)^2
```

where `ybar_train` is the **training-block mean**, not the scored-block mean.
Using the scored-block mean would make `sst` an in-sample quantity and would
silently improve every reported out-of-sample ratio. Sums accumulate over the
ten scored blocks of the date in ascending block order before any averaging.

## 5. Fail-closed requirements

Assembly must fail rather than degrade:

- a nonfinite coefficient, `sse`, or `sst` fails the date;
- a nonconvergent LASSO solve fails the date, and is not retried at a looser
  tolerance;
- a weak PCA eigengap below the sealed threshold fails the date;
- a singular or rank-deficient OLS design fails the date;
- a scored block with zero bins fails the date;
- an `sst` of exactly zero fails the date, because the loss ratio is then
  undefined and silently substituting one would fabricate a diagnostic.

No cell is dropped, averaged over, or filled. A failed date is a failed date.

## 6. Predictions that must survive verification

Frozen before implementation. All are deterministic checks at test seed
`1729` on a synthetic issued panel; no registered stream is involved.

1. Assembly of a synthetic date produces exactly nine `(30,30)` float64
   matrices and one `(6,30,2)` loss array, all finite, and the codec packs them
   to exactly 8,460 fields.
2. `PI_1_direct` and `PI_I_direct` have exact `0.0` at every off-diagonal
   entry, and at least one nonzero diagonal entry.
3. `cc_mean_projection_p_perp` is symmetric to `1e-12`, idempotent to `1e-10`,
   and has trace `29` to `1e-9`, since it projects out one direction.
4. `PI_CC_full_response` differs from `PI_CC_purged` by exactly a rank-one
   matrix, to numerical rank tolerance `1e-10`.
5. Assembling the same panel twice produces byte-identical packed vectors.
6. Perturbing the response order, the specification order, or swapping a purged
   matrix into a full-response slot each changes the packed vector, so the
   placement contract is actually load-bearing rather than decorative.
7. An `sst` computed from the scored-block mean instead of the training-block
   mean differs from the contract value on the synthetic panel, confirming the
   two are distinguishable and the correct one is used.
8. Averaging the ten block operators before forming the cross-sectional product
   gives a different `PI_CC_full_response` than forming the product per block
   and averaging afterwards, confirming Eq. (A) ordering is load-bearing.

## 7. What this derivation does not claim

- It defines composition only. It adds no estimator, changes no kernel, and
  alters no sealed digest, threshold, or address.
- It does not implement an NPY serializer, a resource fixture, a bootstrap
  batch, a resource capability, a rehearsal, or any registered execution path.
  Those remain separately blocked.
- It does not license a registered resource, validation, or research stream,
  and it does not touch external market data. G2 remains open and
  executable-red.
- The synthetic panel used for verification is a software fixture. Assembling
  it is not a scientific trial and produces no coefficient-to-truth comparison.
