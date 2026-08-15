# The minimum confounding dimension

## Claim being derived

Asking "given `K`, is the coefficient matrix consistent with pure confounding?"
requires committing to a factor budget before looking. The inverse question is
better posed and more interpretable:

```
K_min(A) = min over diagonal D of rank(A - D),                          (1)
```

the smallest latent dimension that could rationalise the observed coefficient
matrix using diagonal structural impact alone. Pure confounding is falsified
when `K_min` exceeds the factor budget the order flow itself supports.

## 1. Falsification needs a lower bound, and cross-blocks certify one

To reject the pure-confounding explanation one must show

```
K_min(A) > K_flow,
```

which requires a **lower** bound on `K_min`. That asymmetry matters, because
the two bounds have completely different reliability.

**Proposition 10 (certified lower bound).** For any disjoint index sets `I, J`,

```
K_min(A) >= rank(A_{I,J}),                                              (2)
```

and therefore `K_min(A) >= max over disjoint (I,J) of rank(A_{I,J})`.

*Proof.* Let `D` attain the minimum in (1), so `rank(A - D) = K_min`. For
disjoint `I, J` no diagonal entry enters the block, so
`A_{I,J} = (A - D)_{I,J}`, a submatrix of a rank-`K_min` matrix. A submatrix
cannot exceed the rank of its parent. ∎

The bound is computed by singular value decomposition of a submatrix. There is
no nuisance parameter and no nonconvex minimisation.

**Why this is the useful direction.** An upper bound on `K_min` requires
exhibiting a diagonal that achieves a given rank, which means solving the
completion problem that `CROSS_BLOCK_RANK.md` Section 4 documents as
start-dependent: twenty random initialisations produced answers spreading by
`24.66`. Falsification does not need that bound. **The unreliable computation
is off the critical path.**

### Population verification

At `N = 30`, seed `1729`, six random balanced disjoint splits, exact rank at
relative tolerance `1e-10`:

| True `K` | 1 | 2 | 3 | 5 | 8 | 12 | 15 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Certified lower bound | 1 | 2 | 3 | 5 | 8 | 12 | 15 |

The bound is attained exactly in every case.

## 2. The bound is exact in population and saturates under noise

Adding a dense off-diagonal perturbation of Frobenius size `eps` to the same
matrix and recomputing the exact rank at tolerance `1e-10`:

| `eps` | 0 | 1e-6 | 1e-4 | 1e-2 | 0.1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Lower bound | 3 | **15** | 15 | 15 | 15 |

A perturbation of `1e-6` — negligible by any economic standard — saturates the
bound at the block dimension. **Exact rank is not usable on sample data.** Any
procedure that reports `K_min` from a numerical rank at a fixed tolerance will
report the block dimension and reject always.

This is a real limitation of Proposition 10 as stated, not a fixture artifact,
and it is why Section 3 exists.

## 3. The separation survives even though the rank does not

The relative singular spectrum of the disjoint block shows why the situation is
recoverable. Structural directions stay `O(1)`; everything beyond them scales
**linearly in the noise**:

| `eps` | `s1` | `s2` | `s3` | `s4` | `s5` | `s6` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1.00 | 0.462 | 0.381 | 7.8e-17 | 4.6e-17 | 2.6e-17 |
| 1e-6 | 1.00 | 0.462 | 0.381 | 1.9e-07 | 1.7e-07 | 1.5e-07 |
| 1e-4 | 1.00 | 0.462 | 0.381 | 1.9e-05 | 1.7e-05 | 1.5e-05 |
| 1e-2 | 1.00 | 0.462 | 0.382 | 1.9e-03 | 1.7e-03 | 1.5e-03 |
| 0.1 | 1.00 | 0.460 | 0.383 | 1.9e-02 | 1.7e-02 | 1.5e-02 |

The gap ratio `sigma_{K+1}/sigma_K` tracks the noise level almost exactly,
taking the values `2.0e-16`, `4.9e-07`, `4.9e-05`, `4.9e-03`, `4.9e-02` across
the same grid. A fixed absolute tolerance cannot work — at `tau = 1e-3` the
reported rank is `3` at `eps = 1e-4` but `14` at `eps = 0.1` — while the
*shape* of the spectrum separates structure from noise at every level tested.

**The consequence for the empirical program.** `K_min` is estimable in
principle, but only with a cut calibrated to the sampling distribution of the
noise singular values rather than to a fixed threshold. That calibration is the
inference problem, and it is **not solved in this document**.

## 4. Predictions frozen before implementation

Deterministic checks at seed `1729`, `N = 30`, six balanced disjoint splits.

1. For `A = D + R` with `rank(R) = k`, the certified lower bound equals `k`
   exactly for `k` in `{1, 2, 3, 5, 8, 12, 15}`.
2. The bound never exceeds the true `K_min` for any admissible matrix, since it
   is a lower bound by Proposition 10.
3. Under a perturbation of size `1e-6` the exact-rank bound saturates at the
   block dimension `15`, confirming that exact rank is unusable on noisy input.
4. The gap ratio `sigma_{K+1}/sigma_K` is below `1e-12` under the null and
   grows monotonically over the grid `{0, 1e-6, 1e-4, 1e-2, 0.1}`.
5. Overlapping index sets do not certify anything: the routine refuses them,
   because the diagonal would enter the block.

## 5. What this does not claim

- **No inference.** Section 2 shows the exact-rank statistic saturates under
  arbitrarily small noise. A sampling distribution for the gap ratio under
  realistic dependence is a separate registered design and is not attempted.
- **No upper bound.** `K_min` is bounded below only. Reporting a point estimate
  of `K_min` would require the completion documented as unreliable.
- **No factor-count comparison.** The empirical comparison against `K_flow`
  needs both a calibrated cut and an independently estimated flow-factor count,
  neither of which exists here.
- **No market data**, no registered stream, no holdout.
