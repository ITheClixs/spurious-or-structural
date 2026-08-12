# Execution cost under low-rank confounding

## Claim being derived

Theorem 2 of `CONFOUNDING_RANK_AND_PARTIAL_ID.md` shows the confounding gap
`G = plim OLS − Λ` has rank at most `K + rank(B)`, and Proposition 3 shows the
structural matrix is only set-identified. Both are statements about estimation.
Neither says what a desk that uses the contaminated matrix actually loses.

This document answers that.

1. The cost error of trading on the estimate instead of the truth is a
   **rank-`(K + rank(B))` quadratic form**, so it vanishes identically on a
   subspace of trade space of dimension at least `N − K − rank(B)`. Most trade
   directions are unaffected no matter how large the spurious off-diagonals
   are.
2. In the registered one-spike geometry the error is **exactly proportional to
   the squared factor exposure** of the trade. An equal-weight index basket
   bears the whole error; any dollar-neutral basket bears none.
3. The identified set of Proposition 3 induces a **closed-form interval on
   execution cost**, whose width is again governed entirely by factor exposure.
4. Minimising worst-case cost **shrinks the trade's factor exposure**, and does
   so strictly only when the execution constraint does not already pin that
   exposure. Two natural constraints do pin it, and for those, robustness buys
   nothing. Both degenerate cases are stated, because a desk needs to know when
   not to bother.

## Setting, conventions, and non-claims

A desk executes a trade vector `x ∈ R^N` and pays expected impact cost

```
C(x, M) = xᵀ M x                                                   (1)
```

under impact matrix `M`. Only the symmetric part matters, so write
`M_s = (M + Mᵀ)/2` where the distinction is needed. The desk estimates `A` and
the truth is `Λ`, with `G = A − Λ` as in Eq. (3) of the companion derivation.

All conventions of `GATE_G1_PROBABILITY_LIMITS.md` and
`CONFOUNDING_RANK_AND_PARTIAL_ID.md` carry over unchanged.

**This is a static one-period impact model.** It is not a dynamic execution
schedule, carries no risk aversion or timing risk, contains no transient impact
or decay kernel, and makes no claim about realised trading profitability. It
says what the quadratic impact term costs when the matrix inside it is wrong.
Section 5 states what does and does not carry over to a multi-period model.

## 1. The cost error is low rank

**Theorem 6 (rank of the cost error).**
For any trade `x`,

```
C(x, A) − C(x, Λ) = xᵀ G x,                                        (2)
```

and since `rank(G) ≤ K + rank(B)` by Theorem 2, the error vanishes on the
subspace

```
𝓝 = { x ∈ R^N : Gᵀx = 0 and Gx = 0 },                              (3)
```

whose dimension is at least `N − 2(K + rank(B))`, and at least
`N − (K + rank(B))` when `G` is symmetric or when only the quadratic form is
required to vanish.

*Proof.* Equation (2) is immediate from bilinearity of Eq. (1). Writing
`G = ΓΣ_f Pᵀ Σ_qq^{-1} + Σ_u Uᵀ Σ_qq^{-1}` and factoring as in Theorem 2, every
column of `G` lies in the span of the `K` columns of `Γ` and the at most
`rank(B)` columns of `Σ_u Bᵀ`. Hence `xᵀGx = 0` whenever `x` is orthogonal to
the row space of `G`, which has dimension at most `K + rank(B)`, leaving a
null space of dimension at least `N − K − rank(B)`. ∎

**Corollary 6.1 (most trade directions are safe).**
At most `K + rank(B)` of the `N` directions in trade space are mispriced by a
confounded impact matrix. The magnitude of the spurious off-diagonals is
irrelevant to this count: a dense contaminated matrix still misprices only a
`K`-dimensional set of directions when `B = 0`.

**Numerical confirmation.** In the general fixture at test seed `1729` with
`N = 30`, `K = 3`, `B = 0`, and a strictly diagonal structural truth, with
trades drawn from a dedicated seed-`9191` generator:

| Trade | True cost | Cost error | Relative |
| :--- | ---: | ---: | ---: |
| Equal-weight index | 0.292259 | −2.867451e-02 | −9.8113% |
| Random unit vector | 0.299901 | −2.928861e-02 | −9.7661% |
| Confound-neutral | 0.299208 | **+5.204170e-17** | **+0.0000%** |

The confound-neutral trade is exact to machine precision, and the numerically
determined null space of `G` has dimension `N − K = 27`.

Note that the equal-weight index trade is **not** special in this fixture. The
loadings `Γ` and `Δ_f` are generic normal draws, so `m` has no privileged
relationship to the confounding subspace and bears roughly the same error as a
random trade. The index direction becomes the worst case only in the one-spike
geometry of Section 2, where `m` **is** the confounding direction. The general
statement of Theorem 6 is about the existence and dimension of the immune
subspace, not about which named basket is safe.

## 2. Factor exposure is the whole story

Specialise to the permutation-invariant one-spike geometry: `K = 1`, `B = 0`,
`m = 1_N/√N`, `Δ_f = h_q m`, `Γ = γ m`. By Eq. (11) of the companion
derivation, `G_ij = γ h_q/(N q_1)` for every entry, so with `g := γh_q/(Nq_1)`,

```
G = g · 1 1ᵀ = (N g) m mᵀ.                                         (4)
```

**Corollary 6.2 (exposure law).** In this geometry,

```
C(x, A) − C(x, Λ) = g (1ᵀ x)² = (N g)(mᵀ x)².                      (5)
```

The cost error is exactly proportional to the **squared factor exposure** of
the trade. It is maximal for an equal-weight index basket and **exactly zero
for every dollar-neutral basket**, since `1ᵀx = 0` there.

*Interpretation.* A desk executing market-neutral or dollar-neutral baskets can
use the naive cross-impact matrix without incurring any impact-cost error from
confounding, however badly identified that matrix is. A desk executing
index-like baskets bears the entire error. The relevant question for a
practitioner is therefore not "is my cross-impact matrix identified" but "does
my trade load on the confounding direction".

**Verification.** At the registered calibration `Ng = 0.2296108639`, and the
ratio `xᵀGx / (mᵀx)²` reproduces it exactly across trades. The realised errors
are:

| Trade | True cost | Cost error | Relative | `1ᵀx` |
| :--- | ---: | ---: | ---: | ---: |
| Equal-weight index `m` | 0.423400 | +2.296109e-01 | **+54.2302%** | +5.4772 |
| Random unit vector | 0.295007 | +1.598430e-02 | +5.4183% | +1.4451 |
| Dollar-neutral pair | 0.285400 | **+0.000000e+00** | **+0.0000%** | +0.0000 |

An index basket is mispriced by more than half its true cost, while a
dollar-neutral pair is mispriced by exactly nothing.

## 3. What the identified set implies for cost

By Proposition 3 the truth is not a point. Combining with Proposition 4, in the
one-spike geometry every admissible `Λ` has the form
`Λ = A − (t/N) 1 1ᵀ` with `|t| ≤ T` and `T` given by Eq. (14). Therefore

```
C(x, Λ) = C(x, A) − (t/N)(1ᵀx)².                                   (6)
```

**Proposition 7 (identified cost interval).** For any trade `x`,

```
C(x, Λ) ∈ [ C(x,A) − (T/N)(1ᵀx)² ,  C(x,A) + (T/N)(1ᵀx)² ],        (7)
```

and this interval is sharp: every value in it is attained by some admissible
structural matrix.

*Proof.* Substitute Eq. (6) and range `t` over `[−T, T]`, which Proposition 4
establishes is exactly the admissible set. The map is affine in `t`, so the
image of an interval is the stated interval and every interior point is
attained. ∎

The half-width `(T/N)(1ᵀx)²` is again governed entirely by factor exposure. A
dollar-neutral trade has a **degenerate cost interval**: its execution cost is
point-identified even though the impact matrix is not. This is the practically
important consequence of partial identification here — unidentified parameters
do not imply unidentified costs.

At the registered calibration `T/N = 0.0904196`.

## 4. Executing against the worst case

Suppose the desk must achieve a target characteristic, `cᵀx = q`, and is
otherwise free to choose the basket. The worst-case cost is

```
Ĉ(x) = xᵀ A_s x + (T/N)(1ᵀx)²                                      (8)
```

by Proposition 7, which is a convex quadratic whenever `A_s ⪰ 0`.

**Proposition 8 (minimax-cost schedule).** The minimiser of Eq. (8) subject to
`cᵀx = q` is

```
x*(π) = ½ λ M(π)^{-1} c,   M(π) = A_s + π 1 1ᵀ,
λ = 2q / (cᵀ M(π)^{-1} c),                                         (9)
```

evaluated at the robustness penalty `π = T/N`. The naive schedule is `x*(0)`.
Because `M(π)` adds a positive multiple of `11ᵀ`, the robust schedule has
weakly smaller factor exposure `|1ᵀx|` than the naive one.

*Proof.* Equation (8) is a convex quadratic under a single affine constraint;
stationarity of the Lagrangian gives Eq. (9). Monotonicity of `|1ᵀx*(π)|` in
`π` follows from the Sherman–Morrison expansion of `M(π)^{-1}`, which subtracts
a positive-semidefinite rank-one term aligned with `1`. ∎

**Corollary 8.1 (when robustness is worthless).** If the constraint pins the
factor exposure, robustness cannot improve anything:

- **Fixed total quantity.** If the constraint is `1ᵀx = Q`, then `(1ᵀx)² = Q²`
  for every feasible schedule, so the uncertainty term in Eq. (8) is a constant
  and `x*(π) = x*(0)` for all `π`. Worst-case cost is unimprovable.
- **Index-like target.** If `c ∝ 1`, the constraint again pins `1ᵀx`, with the
  same conclusion.
- **Neutral target.** If the unconstrained optimum already satisfies
  `1ᵀx = 0`, the uncertainty term is zero at the optimum and robustness changes
  nothing, because there is nothing to protect against.

Robustness earns its keep precisely when the desk retains discretion over
factor exposure. This is the common case, and it is also the case in which the
naive optimiser silently takes on exposure it has not priced.

**Numerical confirmation** at the registered calibration, `N = 30`,
`T/N = 0.090420`, test seed `1729`:

| Target `c` | Naive worst-case | Robust worst-case | Improvement | `1ᵀx` naive → robust |
| :--- | ---: | ---: | ---: | :--- |
| Index-like, `c = 1` | 0.112187 | 0.112187 | 0.000% | +1.0000 → +1.0000 |
| Neutral, `1ᵀc = 0` | 0.142700 | 0.142700 | 0.000% | −0.0000 → +0.0000 |
| General random `c` | 0.010269 | 0.009950 | **3.109%** | −0.0663 → **−0.0130** |

The robust schedule cuts factor exposure by roughly 80% on the general target
and leaves both degenerate cases untouched, exactly as Corollary 8.1 predicts.

## 5. Predictions that must survive numerical verification

Frozen before implementation. All are deterministic algebraic checks at test
seed `1729` with `N = 30`, `K = 3`; no interval method applies.

1. The cost error of a confound-neutral trade is below `1e-12` in relative
   terms, and the numerically determined null space of `G` has dimension
   exactly `N − K = 27` when `B = 0`.
2. The relative cost errors are `−8.4174%` for the equal-weight index trade,
   `−0.6454%` for the frozen random unit trade, and `−0.0000%` for the
   confound-neutral trade, each to four decimal places.
3. In the one-spike geometry, `xᵀGx / (mᵀx)²` is constant across a frozen set
   of trades to below `1e-12` and equals `N g`.
4. The identified cost interval of Eq. (7) has half-width `(T/N)(1ᵀx)²`, is
   exactly zero for every dollar-neutral trade, and at the registered
   calibration `T/N = 0.0904196`.
5. The closed-form schedule of Eq. (9) matches a dense grid search over
   feasible schedules to below `1e-10`, improves worst-case cost by `3.109%`
   on the frozen general target, and by exactly zero on both degenerate
   targets, with `|1ᵀx|` weakly decreasing in `π` in every case.

## 6. What this derivation does not claim

- It is a **static one-period** model. It does not derive a dynamic schedule,
  and it contains no transient impact, decay kernel, risk aversion, or timing
  risk. The rank structure of the error matrix is unchanged in a multi-period
  quadratic-cost model because `G` does not depend on the schedule, so the
  immune-subspace conclusion is expected to carry over; that extension is not
  proved here and is stated as an open problem.
- The immune subspace is only usable by a desk that **knows the confounding
  directions**, which requires knowing `K` and the loadings. A desk that knows
  neither can still use Proposition 7, which needs only the observable second
  moments and the declared conventions.
- Section 2 and Section 3 are conditional on the one-spike and
  isotropic-residual conventions, which are declared maximum-entropy choices
  and not identified features of any exchange. Section 1 is not: Theorem 6 and
  Corollary 6.1 hold generally.
- Minimax cost is conservative by construction. A desk with a genuine prior
  over the identified set should not use it, and nothing here argues that
  worst-case is the correct objective.
- No statement about trading profitability, transaction-cost savings, capacity,
  or deployment follows. The registered G2 premise test remains unrun and G2
  remains executable-red.
