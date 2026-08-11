# Confounding rank and partial identification of cross-impact

## Claim being derived

Theorem 1 of `GATE_G1_PROBABILITY_LIMITS.md` establishes that the population
return-on-flow coefficient differs from the structural impact matrix by a
latent-factor term and a simultaneity term. That result says a discrepancy
exists. It does not say how large the discrepancy can be, what structure it
has, or whether the structural matrix can be recovered from observable second
moments at all.

This document answers all three questions.

1. The discrepancy is **low rank**: its rank is at most `K + rank(B)`, where
   `K` is the number of latent factors and `B` is the same-bin feedback matrix.
2. Consequently the structural matrix is **not point-identified** from second
   moments. Its identified set is a low-rank-perturbation family restricted by
   positive-semidefiniteness.
3. In the registered permutation-invariant one-spike geometry, the identified
   set for a single off-diagonal entry has an exact **closed-form interval**.

The rank restriction is falsifiable, which converts the qualitative worry
"cross-impact estimates may be spurious" into a testable statement about the
estimated coefficient matrix.

## Dimensions, conventions, and assumptions

All conventions of `GATE_G1_PROBABILITY_LIMITS.md` carry over unchanged:

- `r_t, q_t, u_t, v_t ∈ R^N` and `f_t, ε_t ∈ R^K`.
- `Λ, B ∈ R^{N×N}`, `Γ, Δ_f ∈ R^{N×K}`.
- All variables are centered.
- `f_t, u_t, v_t, ε_t` are mutually uncorrelated at time `t`, with covariances
  `Σ_f, Σ_u, Σ_v, Σ_ε`.
- A law of large numbers holds and second moments are finite.
- `L = I_N − BΛ`, `H = L^{-1}`, `D = BΓ + Δ_f`, `P = HD`, `U = HB`, `V = H`, and
  `L`, `Σ_qq`, `Q_h` are nonsingular.

The structural system is

```
r_t = Λ q_t + Γ f_t + u_t                                        (1)
q_t = B r_t + Δ_f f_t + v_t                                      (2)
```

Write the **confounding gap**

```
G := plim Λ̂_OLS − Λ = Γ Σ_f Pᵀ Σ_qq^{-1} + Σ_u Uᵀ Σ_qq^{-1}      (3)
```

Equation (3) is Theorem 1 rearranged; nothing new is assumed to state it.

## 1. The confounding gap is low rank

**Theorem 2 (rank of the confounding gap).**
Under the assumptions above,

```
rank(G) ≤ K + rank(B).
```

If `B = 0`, then `U = 0`, `P = Δ_f`, and the bound sharpens to

```
rank(G) ≤ min{K, rank(Γ), rank(Δ_f)}.
```

*Proof.* Consider the two summands of Eq. (3) separately.

The first summand factors as `Γ · (Σ_f Pᵀ Σ_qq^{-1})`, a product of an `N×K`
matrix and a `K×N` matrix. The rank of a product is at most the minimum rank of
its factors, and both factors have rank at most `K`, so
`rank(Γ Σ_f Pᵀ Σ_qq^{-1}) ≤ K`. When `B = 0` the same argument applied to each
factor gives the refinement `≤ min{K, rank(Γ), rank(Δ_f)}`, because
`P = Δ_f` and `Σ_f`, `Σ_qq^{-1}` are nonsingular.

The second summand is `Σ_u Uᵀ Σ_qq^{-1} = Σ_u Bᵀ Hᵀ Σ_qq^{-1}`. Its rank is at
most `rank(Bᵀ) = rank(B)`, since `Σ_u`, `Hᵀ`, and `Σ_qq^{-1}` cannot raise the
rank of the product.

Rank is subadditive over matrix sums, so
`rank(G) ≤ K + rank(B)`. When `B = 0` the second summand vanishes identically.
∎

**Remark (the bound is tight).** Both inequalities are attained generically. At
test seed `1729` with `N = 30`, `K = 3`, dense random primitives, and
`rank(B) ∈ {0, 1, 2, 30}`, the numerically observed ranks of `G` at relative
tolerance `10^{-10}` are `3, 4, 5, 30`, against bounds `3, 4, 5, 33`. The bound
binds exactly whenever `K + rank(B) ≤ N`.

**Corollary 2.1 (spurious cross-impact is low rank).**
Suppose the structural impact matrix is diagonal, `Λ = D`, and there is no
same-bin feedback, `B = 0`. Then

```
plim Λ̂_OLS = D + G,      rank(G) ≤ K.
```

Every off-diagonal entry of the population coefficient matrix is then
attributable to confounding, and the coefficient matrix lies in the set

```
𝓓_K := { D + R : D diagonal, rank(R) ≤ K }.                       (4)
```

*Interpretation.* Corollary 2.1 is the formal content of the paper's title.
Under zero true cross-impact, the estimated cross-impact matrix is not
approximately diagonal — it is generically dense — but it is confined to the
low-dimensional set `𝓓_K`. Membership in `𝓓_K` is therefore the sharp dividing
line between an entirely spurious cross-impact matrix and one with genuine
structural content.

**Remark (magnitude).** Low rank does not mean small. At test seed `1729` with
`N = 30`, `K = 3`, a strictly diagonal `Λ` with entries drawn uniformly from
`[0.2, 0.4]`, and `B = 0`, the induced spurious off-diagonals reach `0.2207` in
absolute value — the same order of magnitude as the genuine own-impact
diagonal. Confounding does not merely perturb the cross-impact matrix; it can
manufacture one of realistic size from nothing.

## 2. Observational equivalence and the identified set

Fix `B = 0` for this section, matching the registered G2 geometry, and
normalize `Σ_f = I_K` by absorbing the factor scale into `Γ` and `Δ_f`. The
observables are the second moments

```
Σ_qq,     Σ_rr,     A := Σ_rq Σ_qq^{-1}.                          (5)
```

`A` is the population OLS coefficient matrix and is identified directly. Define

```
W := Σ_qq^{-1} Δ_f  ∈ R^{N×K}.                                    (6)
```

From Eq. (3) with `B = 0`, the gap is `G = Γ Δ_fᵀ Σ_qq^{-1} = Γ Wᵀ`, so

```
Λ = A − Γ Wᵀ.                                                     (7)
```

The model-implied residual covariances are

```
Σ_v = Σ_qq − Δ_f Δ_fᵀ                                             (8)
Σ_u = Σ_rr − Λ Σ_qq Λᵀ − Λ Δ_f Γᵀ − Γ Δ_fᵀ Λᵀ − Γ Γᵀ              (9)
```

**Proposition 3 (identified set).**
Given `(A, Σ_qq, Σ_rr)` and a factor count `K`, the identified set for the
structural impact matrix is

```
𝓘 = { A − Γ Wᵀ  :  Δ_f, Γ ∈ R^{N×K},  W = Σ_qq^{-1} Δ_f,
                   Σ_qq − Δ_f Δ_fᵀ ⪰ 0,  Σ_u ⪰ 0 }                (10)
```

with `Σ_u` given by Eq. (9). Every element of `𝓘` reproduces the observed
second moments exactly, so no estimator based on second moments alone can
distinguish among them. `Λ` is set-identified, not point-identified.

*Proof.* Necessity: any structural tuple consistent with the observables must
satisfy Eqs. (7)–(9) by construction, and covariance matrices must be positive
semidefinite. Sufficiency: given any `(Γ, Δ_f)` satisfying the two
semidefiniteness constraints, set `Λ = A − ΓWᵀ`, `Σ_v` by Eq. (8), and `Σ_u` by
Eq. (9). The resulting tuple is a valid instance of the model in Eqs. (1)–(2)
with `B = 0`, and by reversing the algebra it reproduces `Σ_qq`, `Σ_rr`, and
`Σ_rq`. ∎

**Remark (nonemptiness).** `Γ = 0` is always feasible and yields `Λ = A`, the
naive reading. The scientific question is how far `𝓘` extends away from that
point, which is the subject of Section 3.

**Remark (why one factor control does not close the gap).** Controlling for a
noisy proxy `h_t = f_t + ε_t` moves the estimate from `A` to
`Λ + Γ R_f Pᵀ Q_h^{-1}` by Theorem 1. That is a *different point in the same
family* `A − ΓWᵀ`: the control moves the estimate **along the confounding
directions**, not out of `𝓘`. A proxy sharpens the estimate only to the extent
that `R_f ≺ Σ_f`, and it never identifies `Λ` unless `R_f = 0` exactly.

## 3. Sharp bounds in the permutation-invariant one-spike model

Specialize to the registered G2 geometry of `GATE_G2_PREMISE.md`: `K = 1`,
`B = 0`, `N` assets, `m = 1_N/√N`, and the maximum-entropy one-spike
covariances

```
Σ_qq = q_0 I + (q_1 − q_0) m mᵀ,   q_1 = N s_q,  q_0 = (N − q_1)/(N − 1)
Σ_rr = r_0 I + (r_1 − r_0) m mᵀ,   r_1 = N s_r,  r_0 = (N − r_1)/(N − 1)
```

with `Δ_f = h_q m`, `Γ = γ m`, and `Var(f) = 1`. Matching `Σ_qq` to the model
implies `h_q² = q_1 − q_0`.

Since `Σ_qq m = q_1 m`, we have `Σ_qq^{-1} m = m / q_1`, so

```
G = γ m (h_q m)ᵀ Σ_qq^{-1} = (γ h_q / q_1) m mᵀ,
```

and because `(m mᵀ)_{ij} = 1/N` for all `i, j`,

```
G_ij = γ h_q / (N q_1)   for every entry (i, j).                  (11)
```

**The gap is a single constant added to every entry of the coefficient
matrix.** This is the permutation-invariant specialization of Theorem 2: a
rank-one gap whose loading vector is the equal-weight direction.

Write `g := γ h_q / (N q_1)` for that constant and `t := N g`. Let `A_diag` and
`A_off` denote the common diagonal and off-diagonal entries of `A`. Then by
Eq. (7),

```
d = A_diag − g,        o = A_off − g,                             (12)
```

where `d` and `o` are the structural diagonal and off-diagonal sensitivities of
`Λ = (d − o) I + N o m mᵀ`. Writing `λ_1 = d + (N−1) o` for the leading
structural eigenvalue and `a_1 = A_diag + (N−1) A_off` for the leading
eigenvalue of `A`, Eq. (12) gives the exact relation

```
λ_1 = a_1 − t.                                                    (13)
```

**Proposition 4 (sharp interval).**
In this model the positive-semidefiniteness constraints reduce to the single
scalar inequality

```
t² ≤ T²,        T² := (r_1 − q_1 a_1²)(q_1 − q_0) / (q_1 q_0),    (14)
```

which is feasible if and only if `r_1 ≥ q_1 a_1²`. The identified set for the
structural off-diagonal is therefore the exact interval

```
Λ_off ∈ [ A_off − T/N ,  A_off + T/N ].                           (15)
```

*Proof.* Decompose every matrix in the `m` direction and its orthogonal
complement, on which all matrices act as multiples of the identity.

`Σ_v = Σ_qq − Δ_f Δ_fᵀ = q_0 I + (q_1 − q_0) m mᵀ − h_q² m mᵀ = q_0 I ⪰ 0`,
which holds automatically and imposes no restriction on `t`.

For `Σ_u`, note `Λ m = λ_1 m` and `Λ` acts as `(d − o) I` on `m^⊥`. From
Eq. (9) with `Γ = γ m` and `Cov(q_t, f_t) = h_q m`,

```
Σ_u = Σ_rr − Λ Σ_qq Λᵀ − (2 γ h_q λ_1 + γ²) m mᵀ.
```

On `m^⊥` this gives the eigenvalue `r_0 − (d − o)² q_0`. By Eq. (12),
`d − o = A_diag − A_off`, so this eigenvalue does not depend on `t` and imposes
no restriction on the identified set.

On the `m` direction the eigenvalue is
`r_1 − λ_1² q_1 − 2 γ h_q λ_1 − γ²`, so `Σ_u ⪰ 0` requires

```
γ² + 2 λ_1 h_q γ + λ_1² q_1 − r_1 ≤ 0.
```

Substitute `γ = t q_1 / h_q` (from `t = N g = γ h_q / q_1`) and
`λ_1 = a_1 − t` from Eq. (13). The two middle terms combine as

```
2 t q_1 (a_1 − t) + q_1 (a_1 − t)² = q_1 (a_1 − t)(a_1 + t) = q_1(a_1² − t²),
```

so the constraint becomes

```
t² q_1² / (q_1 − q_0) + q_1 a_1² − q_1 t² ≤ r_1,
```

that is `t² q_1 q_0 / (q_1 − q_0) ≤ r_1 − q_1 a_1²`, which is Eq. (14).
Since `Λ_off = o = A_off − g = A_off − t/N`, the interval (15) follows. ∎

**Numerical verification.** At the registered source-matched calibration
(`N = 30`, `s_q = 0.2827`, `s_r = 0.32`, `d = 0.29`), a bisection search over
the exact positive-semidefiniteness boundary reproduces the closed-form `T` of
Eq. (14) to relative error `9.8 × 10^{-16}`.

**Evaluation at the registered calibration.** For the two registered structural
endpoints:

| `o` | `A_off` | `T` | Identified interval for `Λ_off` | Contains 0 |
| ---: | ---: | ---: | :--- | :--- |
| 0.0029 | 0.0105537 | 2.8291865 | `[−0.083753, +0.104860]` | yes |
| 0.0046 | 0.0122537 | 2.7125872 | `[−0.078166, +0.102673]` | yes |

At the upper endpoint the identified half-width `T/N = 0.0904196` is **7.38
times** the observed off-diagonal coefficient itself. The identified set
contains zero, contains the entire registered structural sensitivity range
`[0.0029, 0.0046]`, and contains off-diagonals of both signs.

**Corollary 4.1 (sign non-identification).** At the source-matched calibration,
the structural off-diagonal is not identified even in sign from second moments
under the one-spike convention. Any claim that a positive estimated
cross-coefficient demonstrates positive structural cross-impact requires an
identifying restriction beyond the observed second moments.

## 4. The diagonal-plus-rank-K restriction as a specification test

Corollary 2.1 states that a purely spurious cross-impact matrix lies in
`𝓓_K` of Eq. (4). This is a proper subset of `R^{N×N}` whenever `K < N − 1`, so
it is refutable.

**Definition.** For a coefficient matrix `Â` and factor count `K`, define

```
ψ_K(Â) := min_{ D diagonal, rank(R) ≤ K } ‖Â − D − R‖_F
          / ‖Â − diag(Â)‖_F.                                      (16)
```

The denominator normalizes by the total off-diagonal energy, making `ψ_K`
scale-free and invariant to simultaneous row-and-column permutation of the
assets.

**Proposition 5 (population zero).** Under `H₀`: `Λ` diagonal, `B = 0`, and
exactly `K` latent factors, the population coefficient matrix satisfies
`ψ_K(plim Λ̂_OLS) = 0`.

*Proof.* Immediate from Corollary 2.1: `plim Λ̂_OLS = D + G` with `D = Λ`
diagonal and `rank(G) ≤ K`, so the minimand in Eq. (16) attains zero. ∎

**Direction of the test.** A materially nonzero `ψ_K` is evidence **against**
pure confounding and therefore **for** genuine structural cross-impact. This
polarity is the reverse of the naive reading, under which a large off-diagonal
coefficient is itself taken as evidence of cross-impact. Under the present
result, off-diagonal magnitude carries no such information; only departure from
`𝓓_K` does.

**Computation.** The minimization in Eq. (16) is biconvex and is solved by
alternating projection: with `R` fixed the optimal `D` is `diag(Â − R)`, and
with `D` fixed the optimal `R` is the rank-`K` truncated singular value
decomposition of `Â − D`. Each half-step is the exact Frobenius minimizer over
its block, so the objective is nonincreasing and bounded below, hence
convergent. The limit is a stationary point; `ψ_K` as computed is therefore an
**upper bound** on the true distance, which makes the test conservative in the
direction of failing to reject `H₀`.

**Identification caveat.** `ψ_K = 0` does not prove `Λ` is diagonal. A
structural matrix that is itself diagonal-plus-rank-`K` is observationally
indistinguishable from a diagonal matrix contaminated by `K` factors. The test
refutes; it does not confirm.

**Misspecified `K`.** The statistic depends on the assumed factor count.
Overstating `K` shrinks `ψ_K` toward zero mechanically and weakens the test;
understating `K` inflates `ψ_K` and can produce spurious rejection. Any
application must report `ψ_K` across a range of `K` rather than at a single
value.

## 5. Predictions that must survive numerical verification

These are frozen before implementation. Each is a deterministic algebraic
check at test seed `1729`; no registered stream, market data, or stochastic
inference is involved, so no interval method applies.

1. With `N = 30`, `K = 3`, dense random primitives, and
   `rank(B) ∈ {0, 1, 2, 30}`, the numerical rank of `G` at relative tolerance
   `10^{-10}` equals `3, 4, 5, 30` respectively, and each is at most
   `K + rank(B)`.
2. With `Λ` diagonal and `B = 0`, `rank(G) = K` exactly, the induced
   off-diagonals are nonzero, and `ψ_K(Λ + G) < 10^{-8}`.
3. With `Λ` diagonal plus a dense off-diagonal perturbation of Frobenius size
   `ε` and `B = 0`, `ψ_K` is strictly increasing over the frozen grid
   `ε ∈ {0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3}`.
4. In the one-spike model, the closed-form `T` of Eq. (14) agrees with a
   bisection search over the exact positive-semidefiniteness boundary to
   relative error below `10^{-10}`.
5. `ψ_K` is invariant to simultaneous row-and-column permutation to below
   `10^{-12}`.
6. In the one-spike model, `G_ij` is constant across all `N²` entries to below
   `10^{-12}`, matching Eq. (11).

## 6. What this derivation does not claim

- It does not identify `Λ`. It proves the opposite: `Λ` is set-identified from
  second moments, and Section 3 measures how wide that set is.
- It does not assert that the mutual zero cross-covariance restrictions, the
  one-spike convention, or the isotropic residual spectrum hold in any market.
  Each is a declared modeling choice, and Eq. (15) inherits their
  conditionality.
- It does not estimate any market's structural impact matrix. The evaluation in
  Section 3 is a conditional analytic exhibit at a source-motivated
  calibration.
- It does not supersede or weaken the registered G2 premise test. G2 remains
  open and executable-red, and nothing in this document licenses a registered
  resource, validation, or research stream.
- It does not establish finite-sample behavior of `ψ_K`. Proposition 5 is a
  population statement; a sampling distribution for `ψ_K` under `H₀` is not
  derived here and would require its own registered design.
- It does not support any trading, execution-cost, or profitability claim.
