# Cross-block rank restrictions

## Claim being derived

`psi_K` measures distance from the diagonal-plus-rank-`K` set by alternating
projection. That statistic has two defects this document removes. It solves a
nonconvex problem whose value depends on the starting point, and it must
estimate a nuisance diagonal it does not care about.

Both disappear under one observation. If

```
A = D + R,   D diagonal,   rank(R) <= K,
```

and `I` and `J` are **disjoint** index sets, then no diagonal entry lies in the
submatrix `A_{I,J}`, so

```
A_{I,J} = R_{I,J}    and therefore    rank(A_{I,J}) <= K.            (1)
```

The nuisance is gone, the restriction is exact, and testing it needs one
singular value decomposition of a submatrix rather than an iterative solve.

## 1. The cross-block theorem

**Theorem 9 (cross-block rank).**
Let the structural impact matrix be diagonal, let `B = 0`, and let there be at
most `K` latent confounding factors, so that the population coefficient matrix
satisfies `A = Lambda + G` with `Lambda` diagonal and `rank(G) <= K` by
Corollary 2.1. Then for every pair of disjoint index sets `I, J`,

```
rank(A_{I,J}) <= K,
```

and consequently every `(K+1) x (K+1)` minor of `A_{I,J}` vanishes.

*Proof.* For `i in I` and `j in J` disjointness gives `i != j`, so
`A_{ij} = Lambda_{ij} + G_{ij} = G_{ij}`. Hence `A_{I,J} = G_{I,J}`, a
submatrix of a matrix of rank at most `K`, and a submatrix cannot exceed the
rank of its parent. Vanishing of all `(K+1)`-minors is the determinantal
characterisation of that rank bound. ∎

**Corollary 9.1 (tetrads at `K = 1`).** With a single latent factor, for
distinct `i, k in I` and distinct `j, l in J`,

```
A_{ij} A_{kl} - A_{il} A_{kj} = 0.
```

These are observable restrictions on four coefficient entries containing no
diagonal and no unknown parameter of any kind.

### Numerical verification

At `N = 30`, `K = 3`, seed `1729`, with `I = {0..9}` and `J = {15..24}`:

| Quantity | Value |
| --- | ---: |
| `max abs(A_{I,J} - G_{I,J})` | **0.000e+00** |
| Singular values of `A_{I,J}` | `0.5945, 0.3824, 0.1714, 4.2e-17, ...` |
| Numerical rank | **3** |

Under a dense off-diagonal perturbation of Frobenius size `eps` added to `A`,
the first violated singular value responds immediately:

| `eps` | 0 | 0.01 | 0.05 | 0.20 |
| --- | ---: | ---: | ---: | ---: |
| `sigma_{K+1}(A_{I,J})` | 4.23e-17 | 1.27e-03 | 6.36e-03 | 2.53e-02 |

At `K = 1`, across 784 tetrads formed from disjoint index sets, the largest
absolute tetrad is `1.7e-18`. Evaluating the same tetrads on a `K = 3` matrix
gives `5.9e-02`, so the restriction discriminates the factor count rather than
holding vacuously.

## 2. Why this replaces the distance statistic

`psi_K` requires minimising over a diagonal and a rank-`K` matrix jointly. The
problem is biconvex, not convex, and the alternating projection converges to a
stationary point whose value depends on initialisation. Section 4 below shows
that dependence is severe.

Equation (1) requires no minimisation. The null implies an exact zero for
`sigma_{K+1}(A_{I,J})`, computable by one singular value decomposition of an
`|I| x |J|` block. There is no nuisance parameter, no starting point, and no
convergence criterion.

## 3. The converse, and what is actually established

The natural converse asks whether small cross-block ranks force the existence
of a diagonal `D` with `rank(A - D) <= K`. Equivalently: given all off-diagonal
entries of a rank-`K` matrix, is its diagonal determined?

**Local identification holds in every configuration tested.** For a rank-`K`
matrix `R`, perturbing the diagonal by `t*d` with `d` a unit vector and
`t = 1e-3`, the smallest observed value of
`sigma_{K+1}(R + diag(t d)) / sigma_1` over 500 random directions was strictly
positive in every case:

| `N` | `K` | dim of rank-`K` manifold | `dim + N - N^2` | min `sigma_{K+1}/sigma_1` |
| ---: | ---: | ---: | ---: | ---: |
| 7 | 3 | 33 | −9 | 3.46e-05 |
| 8 | 3 | 39 | −17 | 2.67e-05 |
| 10 | 3 | 51 | −39 | 2.65e-05 |
| 30 | 1 | 59 | −811 | 1.04e-05 |
| 30 | 3 | 171 | −699 | 8.93e-06 |
| 30 | 10 | 500 | −370 | 5.65e-06 |
| 30 | 14 | 644 | −226 | 4.07e-06 |
| 6 | 2 | 20 | −10 | 7.20e-05 |
| 5 | 2 | 16 | −4 | 4.63e-05 |

The dimension count is consistent: the rank-`K` variety has dimension
`K(2N-K)`, the matrices agreeing with `R` off the diagonal form an affine set of
dimension `N`, and the excess `K(2N-K) + N - N^2` is negative throughout, so a
generic intersection is isolated rather than a positive-dimensional family.

**This is numerical evidence for local identification, not a proof, and it is
not a global statement.** A global uniqueness theorem, with an explicit
exceptional set and an exact `(N, K)` condition, is not established here.

## 4. A negative result that must be recorded

Recovering the diagonal by alternating projection **is not reliable**, and the
failure has the same shape as the one that afflicts `psi_K`.

Starting the completion from the observed matrix `A` recovers `diag(G)` to
`4.4e-16`, and hence the structural diagonal `Lambda_{ii} = A_{ii} - G_{ii}` to
`4.2e-16`. That looks like clean identification. It is not: starting the same
completion from twenty random diagonals drawn at scale `5.0` produced solutions
whose spread was **24.66**, with a maximum error against `diag(G)` of `15.37`.
The procedure has many stationary points and finds the right one only when
started near it.

The same procedure also failed to recover the diagonal at `N = 5, 6, 7` with
`K = 3` while succeeding for `N >= 8`. The direct local-identification test in
Section 3 shows the diagonal is identified at `N = 7, K = 3` and at
`N = 5, K = 2` regardless, so **those failures are algorithmic and not
identification failures.** The distinction matters: an estimator built on the
completion inherits a defect the underlying identification does not have.

The practical consequence is the argument for Equation (1). Cross-block rank
avoids the nonconvex completion entirely. Any procedure that instead estimates
the diagonal must confront the initialisation problem documented here.

## 5. Predictions to be frozen before implementation

Deterministic checks at test seed `1729`, no registered stream involved.

1. For `A = D + R` with `rank(R) = K = 3` at `N = 30` and disjoint
   `I = {0..9}`, `J = {15..24}`, `A_{I,J}` equals `R_{I,J}` exactly and has
   numerical rank `3` at relative tolerance `1e-10`.
2. `sigma_{K+1}(A_{I,J})` is below `1e-12` relative to `sigma_1` under the null
   and strictly increasing in the size of a dense off-diagonal perturbation
   over the grid `{0, 0.01, 0.05, 0.20}`.
3. At `K = 1`, all 784 tetrads on disjoint index sets are below `1e-12`
   relative to the largest entry product, and the same tetrads on a `K = 3`
   matrix exceed `1e-3`.
4. Overlapping index sets (`I ∩ J != ∅`) do **not** satisfy the restriction:
   the rank of `A_{I,J}` there exceeds `K` for the same matrix, confirming the
   disjointness hypothesis is load-bearing rather than decorative.
5. The local-identification statistic `min sigma_{K+1}/sigma_1` over 500
   diagonal directions is strictly positive for every `(N, K)` in the Section 3
   table.

## 6. What this derivation does not claim

- It does not prove a global converse. Section 3 is numerical local evidence
  with a supporting dimension count.
- It does not supply inference. Under sampling, `sigma_{K+1}` is positive even
  under the null, and a distribution for it under realistic dependence is a
  separate registered design.
- It does not select `K`. The restriction is stated for a given factor budget,
  and any application must report the whole map from `K` to its test outcome
  rather than one chosen value.
- It does not identify `Lambda` when `Lambda` is not diagonal. The theorem
  assumes the maintained null it is designed to falsify.
- It does not touch the registered G2 streams, market data, or the holdout.
