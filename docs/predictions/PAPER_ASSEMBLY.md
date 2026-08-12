# Paper-assembly pre-run prediction

Registered on 2026-08-12 after the derivation in
`docs/derivations/GATE_G2_PAPER_ASSEMBLY.md` and before any assembly driver,
synthetic panel, or date cache existed.

## Scope

Covers amendment A031 only. G2 remains open and executable-red. Registered
resource seed `2026071529`, validation seed `2026071521`, and research seed
`2026071522` are not accessed, and no external market data, evaluation data, or
holdout is touched. The only randomness is test seed `1729`, used to draw a
synthetic issued panel for deterministic verification.

## Predictions

1. Assembly of a synthetic date produces exactly nine `(30,30)` float64
   matrices and one `(6,30,2)` loss array, all finite, and the codec packs them
   to exactly 8,460 fields.
2. `PI_1_direct` and `PI_I_direct` are exactly `0.0` at every off-diagonal
   entry and have at least one nonzero diagonal entry.
3. `cc_mean_projection_p_perp` is symmetric to `1e-12`, idempotent to `1e-10`,
   and has trace `29` to `1e-9`.
4. `PI_CC_full_response` differs from `PI_CC_purged` by a matrix of numerical
   rank one at tolerance `1e-10`.
5. Assembling the same panel twice produces byte-identical packed vectors.
6. Permuting the response order, permuting the specification order, or swapping
   a purged matrix into a full-response slot each changes the packed vector.
7. An `sst` computed from the scored-block mean rather than the outer-training
   mean differs from the contract value on the synthetic panel.
8. Averaging the ten block operators before forming the cross-sectional product
   gives a different `PI_CC_full_response` than forming the product per block
   and averaging afterwards.

## Intervals and reporting

Every quantity is a deterministic algebraic evaluation, so the named interval
method is **not applicable**. The multiple-testing count is **zero**: no
stochastic draw and no coefficient-to-truth comparison is part of this slice.

## Failure interpretation fixed before implementation

- A nonfinite or misshapen output falsifies the composition and stops the
  slice.
- A nonzero off-diagonal in an own-flow specification means the structural zero
  convention was not applied and is a defect, not a discovery.
- If prediction 6 or 8 fails, the placement or averaging-order contract is
  vacuous. It is re-derived rather than declared satisfied, because a contract
  that no permutation can violate constrains nothing.
- Tolerances are stated in relative terms where the quantity is a reduction
  over many float64 products, following the recurrence note in
  `SPECIFICATION_LOG.md`.
