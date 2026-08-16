# The generic rank of the confounding gap

## Claim being derived

Theorem 2 bounds the confounding gap by `rank(G) <= K + rank(B)` and the
manuscript calls the bound "generically attained" without proving it. An
inequality that is never tight would make the low-rank contamination story
vacuous, so the bound has to be turned into an equality with stated conditions
and a characterised exceptional set.

## 1. The gap factors through `K + rank(B)` columns

With `M = (I - B Lambda)^{-1}`, `P = M (B Gamma + Delta_f)`, and
`Sigma_qq = P Sigma_f P' + M B Sigma_uu B' M' + M Sigma_vv M'`, the gap is

```
G = Gamma C_1 + Sigma_uu B' M' Sigma_qq^{-1},
      C_1 = Sigma_f P' Sigma_qq^{-1}.                                    (1)
```

Factor `B = B_L B_R` with `B_L` of size `N x b`, `B_R` of size `b x N`, both of
full rank `b = rank(B)`. Then (1) becomes a product of an `N x (K+b)` matrix
and a `(K+b) x N` matrix:

```
G = L R,    L = [ Gamma | Sigma_uu B_R' ],    R = [ C_1 ; B_L' M' Sigma_qq^{-1} ].
```

The bound `rank(G) <= K + b` is immediate from this shape. The content of the
theorem below is the reverse inequality.

## 2. Theorem 10 (generic rank of the confounding gap)

**Theorem 10.** Assume `Sigma_uu`, `Sigma_vv`, and `Sigma_f` are positive
definite, `rank(Gamma) = K`, `rank(B Gamma + Delta_f) = K`, and
`K + rank(B) <= N`. Assume further that

```
col(Gamma)  intersect  Sigma_uu col(B')  =  {0}.                         (2)
```

Then

```
rank(G) = K + rank(B).
```

*Proof.* Write `b = rank(B)`. The matrix `M' Sigma_qq^{-1}` is invertible, so
`R`'s second block `B_L' M' Sigma_qq^{-1}` has full row rank `b`. Positive
definiteness of `Sigma_f` and `rank(P) = rank(M (B Gamma + Delta_f)) = K` make
`C_1 = Sigma_f P' Sigma_qq^{-1}` of full row rank `K`. The two blocks of `R`
have independent row spaces under (2) — a nontrivial relation among them would
produce a nonzero vector in the intersection — so `rank(R) = K + b`.

For `L`: `rank(Gamma) = K`, `Sigma_uu B_R'` has rank `b` since `Sigma_uu` is
invertible and `B_R` has full row rank, and (2) says their column spaces meet
only at zero. Hence `rank(L) = K + b`.

Both factors have full rank `K + b`, and their inner dimension is exactly
`K + b`. Sylvester's rank inequality gives

```
rank(L R) >= rank(L) + rank(R) - (K + b) = K + b,
```

and the factorisation gives `rank(L R) <= K + b`. ∎

**Theorem 10' (the capped case).** When `K + rank(B) > N` the inner dimension
exceeds `N` and Sylvester is no longer binding. The generic value is then
`min(N, K + rank(B)) = N`. Each of the conditions of Theorem 10 is the
non-vanishing of a polynomial in the primitives, as is `rank(L R) = N`; a
single draw at which the polynomial is nonzero proves it is not identically
zero, so its zero set is a proper algebraic subvariety and therefore Lebesgue
null. Section 3 exhibits such draws. **This is a genericity argument supported
by witnesses, not a closed-form proof of the capped case**, and it is labelled
as such wherever it is used.

**Corollary 10.1.** Under the conditions of Theorem 10, the bound of Theorem 2
is attained exactly, so the low-rank description of the confounding gap is
sharp rather than merely an upper envelope. When `K + rank(B) >= N` the gap is
generically of full rank and carries no low-rank restriction at all — the
testable content of the theory requires a factor-plus-feedback budget strictly
below the cross-section size.

## 3. Numerical verification

Forty independent draws per configuration. The observed rank was the *same
single value* in every draw of every cell, and it equals `min(N, K + rank(B))`
throughout. The two-term expression (1) was checked against the definition
`plim OLS - Lambda` in every draw; the largest discrepancy was `1.3e-14`.

| `N` | `K` | `rank(B)` | `K + rank(B)` | `min(N, K+rank(B))` | observed `rank(G)` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 20 | 3 | 0 | 3 | 3 | **3** |
| 20 | 3 | 2 | 5 | 5 | **5** |
| 20 | 3 | 5 | 8 | 8 | **8** |
| 20 | 1 | 0 | 1 | 1 | **1** |
| 20 | 1 | 1 | 2 | 2 | **2** |
| 8 | 3 | 4 | 7 | 7 | **7** |
| 8 | 3 | 6 | 9 | 8 | **8** |
| 8 | 5 | 5 | 10 | 8 | **8** |
| 6 | 4 | 4 | 8 | 6 | **6** |
| 30 | 10 | 15 | 25 | 25 | **25** |

The last four rows are the capped regime and witness Theorem 10'.

## 4. The exceptional set is load-bearing

Each hypothesis of Theorem 10 was violated in turn, at `N = 20`, `K = 3`,
`rank(B) = 4`, generic target `7`, over thirty draws each. Every violation
lowers the rank by exactly the amount the proof predicts.

| Violated hypothesis | `rank(G)` | drop |
| --- | ---: | ---: |
| none (generic draw) | 7 | 0 |
| `Gamma = 0` | 4 | 3 |
| `rank(Gamma) = K - 1` | 6 | 1 |
| one column of `Gamma` inside `Sigma_uu col(B')`, violating (2) | 6 | 1 |
| `Sigma_f` singular (one factor with no variance) | 6 | 1 |
| `B = 0` and `Delta_f = 0`, so `P = 0` and `C_1 = 0` | 0 | 3 |

The third row is the one worth naming: condition (2) is not a technical
convenience. When a priced-risk direction coincides with a feedback direction
transported by `Sigma_uu`, the two confounding channels overlap and the gap
carries strictly less rank than the budget allows. Economically, a factor whose
return premium is aligned with the direction along which flow responds to
returns is counted once by the data, not twice.

## 5. Predictions frozen before implementation

Deterministic checks at seeds `1000..1039` and `2000..2029`, `rtol = 1e-9`.

1. The factorisation `G = L R` reproduces `confounding_gap` to `1e-12`
   relative in every configuration of the Section 3 table.
2. `rank(G) = min(N, K + rank(B))` in all forty draws of each of the ten
   configurations of Section 3, with no draw disagreeing.
3. `rank(L) = rank(R) = min(N, K + rank(B))` in the uncapped configurations,
   which is the hypothesis Sylvester consumes.
4. Each of the five violations in the Section 4 table produces exactly the
   tabulated rank, in all thirty draws.
5. Setting `Gamma = 0` yields `rank(G) = rank(B)` exactly, and setting `B = 0`
   with `Delta_f` generic yields `rank(G) = K` exactly.

## 6. What this derivation does not claim

- The capped case `K + rank(B) > N` is established by genericity plus
  witnesses, not by a closed-form proof. Theorem 10 proper covers
  `K + rank(B) <= N`.
- "Generic" is with respect to Lebesgue measure on the primitives. It says
  nothing about whether real markets sit in the exceptional set, and
  condition (2) is exactly the kind of alignment a factor model might produce.
- No sampling theory. `rank(G)` is a population object; estimated gaps have
  full rank almost surely and require the inference of A032.
- The result strengthens the *sharpness* of Theorem 2. It does not identify
  `Lambda`, and it does not bear on the diagonal restriction.
