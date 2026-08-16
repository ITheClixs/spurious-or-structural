# Does the cross-block restriction characterise the model?

## Claim being derived

Theorem 9 shows that a diagonal-plus-rank-`K` matrix has every disjoint
cross-block of rank at most `K`. The converse is the question that decides
whether the restriction is a *characterisation* or merely a *consequence*:

> If every disjoint cross-block of `A` has rank at most `K`, must there exist a
> diagonal `D` with `rank(A - D) <= K`?

Equivalently: do the off-diagonal entries of a matrix determine whether it can
be completed to rank `K`? This is the asymmetric form of the classical Frisch
problem of factor analysis, and we do not resolve it in general. We do settle
`K = 1` completely, establish the general case locally, and give the exact
condition under which the restriction has any content at all.

## 1. When the restriction is non-vacuous

Off-diagonals of rank-`K` matrices form a set of dimension `K(2N - K)` inside
the `N^2 - N` dimensional space of off-diagonal patterns. The cross-block
conditions can constrain something only while the first is strictly smaller.

**Proposition 12 (content boundary).** The disjoint cross-block restriction is
non-vacuous if and only if

```
K (2N - K) < N^2 - N,   equivalently   K < N - sqrt(N).              (1)
```

*Proof.* `K(2N-K) < N(N-1)` rearranges to `(N-K)^2 > N`, and `K < N` gives
`N - K > sqrt(N)`. ∎

| `N` | `K` | `K(2N-K)` | `N^2-N` | content? |
| ---: | ---: | ---: | ---: | :---: |
| 5 | 1 | 9 | 20 | yes |
| 5 | 3 | 21 | 20 | **no** |
| 8 | 3 | 39 | 56 | yes |
| 8 | 5 | 55 | 56 | yes (slack 1) |
| 10 | 7 | 91 | 90 | **no** |
| 30 | 3 | 171 | 870 | yes |
| 30 | 23 | 851 | 870 | yes (slack 19) |

Condition (1) sits alongside Corollary 10.1 as a second budget constraint on
the theory. Corollary 10.1 says the *gap* carries no low-rank structure once
`K + rank(B) >= N`; Proposition 12 says the *cross-block test* has nothing to
detect once `K >= N - sqrt(N)`. For `N = 30` these bite at `K = 30` and
`K = 25` respectively, so in the registered geometry both are slack by a wide
margin.

## 2. The converse holds outright at one factor

**Theorem 11 (global converse at `K = 1`).** Let `N >= 4` and suppose every
disjoint tetrad of `A` vanishes,

```
A_{ij} A_{kl} - A_{il} A_{kj} = 0    for distinct i,k and distinct j,l
                                     with {i,k} disjoint from {j,l}.
```

Suppose further that the anchor entries `A_{01}`, `A_{12}`, `A_{20}` are
nonzero. Then there exist vectors `x, y` with `A_{ij} = x_i y_j` for every
`i != j`, and hence a diagonal `D` — namely `D_{ii} = x_i y_i` — with
`rank(A - D) <= 1`.

*Proof.* Set `x_i = A_{i1}` for `i != 1` and `y_j = A_{0j} / A_{01}` for
`j != 0`; then `y_1 = 1` and `x_0 = A_{01}`. For `i != 1`, `j != 0`, `i != j`
the tetrad on `I = {i, 0}`, `J = {j, 1}` — disjoint whenever `i != j`,
`i != 1`, `j != 0` — gives `A_{ij} A_{01} = A_{i1} A_{0j}`, that is
`A_{ij} = x_i y_j`. The two remaining families are recovered from a third
index, which exists because `N >= 4`: `x_1 = A_{12} / y_2` and
`y_0 = A_{20} / x_2`. Setting `D_{ii} = x_i y_i` replaces the diagonal of `A`
by that of `x y'`, leaving `A - D + diag(x y') = x y'` of rank one. ∎

### Numerical verification

Reconstructing `x, y` from off-diagonal entries alone, at a matrix built as
`x y'` with an arbitrary unrelated diagonal:

| `N` | max tetrad | max `|A_ij - x_i y_j|` off-diagonal | `rank(A - D*)` |
| ---: | ---: | ---: | ---: |
| 4 | 1.81e-17 | 5.55e-17 | **1** |
| 5 | 3.17e-17 | 5.55e-17 | **1** |
| 6 | 8.53e-17 | 2.22e-16 | **1** |
| 8 | 3.54e-16 | 4.44e-16 | **1** |
| 12 | 1.76e-15 | 4.44e-16 | **1** |

The nonvanishing hypothesis is not removable: at `N = 3` no four distinct
indices exist, the tetrad family is empty, and the restriction says nothing.

## 3. The general case, locally

For `K >= 2` we do not have a global proof. We do have a decisive local
statement, obtained by comparing tangent spaces at a generic point of the
model.

Let `A = U V' + diag(d)` with `U, V` of size `N x K` generic. Two sets live in
the `N^2 - N` dimensional space of off-diagonal patterns:

- `S_1`, the off-diagonals of rank-`K` matrices, of dimension `K(2N - K)`;
- `S_2`, the variety cut out by vanishing of every minimal disjoint cross-block
  `(K+1)`-minor.

Theorem 9 gives `S_1 subset S_2`. If their tangent spaces agree at a generic
point of `S_1`, then `S_2` has the same local dimension, and — containing an
irreducible set of equal dimension — coincides with `S_1` near that point.

**Finding.** The tangent dimensions agree in every configuration tested.

| `N` | `K` | off-diagonal dim | minors | `rank(J)` | `dim T S_2` | `dim S_1 = K(2N-K)` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 1 | 20 | 30 | 11 | **9** | **9** |
| 6 | 1 | 30 | 90 | 19 | **11** | **11** |
| 7 | 1 | 42 | 210 | 29 | **13** | **13** |
| 8 | 1 | 56 | 420 | 41 | **15** | **15** |
| 6 | 2 | 30 | 20 | 10 | **20** | **20** |
| 7 | 2 | 42 | 140 | 18 | **24** | **24** |
| 8 | 2 | 56 | 560 | 28 | **28** | **28** |
| 8 | 3 | 56 | 70 | 17 | **39** | **39** |
| 9 | 3 | 72 | 630 | 27 | **45** | **45** |

**Corollary 11.1 (local converse).** Near a generic diagonal-plus-rank-`K`
matrix, satisfying every disjoint cross-block rank bound is *equivalent* to
being completable to rank `K`. The restriction is therefore a local
characterisation, not merely a necessary condition.

## 4. What remains open, stated plainly

Tangent-space equality at generic points of `S_1` does **not** rule out other
irreducible components of `S_2` lying elsewhere. A global converse would
require showing `S_2` has no component disjoint from `S_1`, and we have neither
proved that nor found a counterexample. Concretely:

- **Open:** for `K >= 2`, is there an `A` all of whose disjoint cross-blocks
  have rank `<= K` while no diagonal `D` achieves `rank(A - D) <= K`?
- The symmetric analogue is the Frisch problem, where non-identified
  configurations are known to exist above the Ledermann bound
  `phi(N) = (2N + 1 - sqrt(8N+1))/2`. That bound governs a different counting
  problem — symmetric covariance rather than an asymmetric coefficient matrix —
  and we do not import it. Condition (1) is the count that applies here.
- The practical consequence is small and should be stated as such: a rejection
  of the cross-block restriction refutes the maintained null regardless, since
  Theorem 9 is a one-way implication and rejection uses only that direction. It
  is *non*-rejection whose interpretation would tighten if the global converse
  were settled.

## 5. Predictions frozen before implementation

Deterministic; seeds `7` and `11`; tolerance `1e-9` relative on ranks.

1. Condition (1) reproduces the content column of the Section 1 table exactly,
   and `K(2N-K) < N^2-N` agrees with `K < N - sqrt(N)` at every
   `N` in `{5, 8, 10, 20, 30}` and every `K` in `1..N`.
2. The `K = 1` reconstruction of Section 2 returns off-diagonal error below
   `1e-14` and `rank(A - D*) = 1` for every `N` in `{4, 5, 6, 8, 12}`.
3. At `N = 3` the disjoint tetrad family is empty.
4. For every row of the Section 3 table, the minor values vanish at the
   generic point to `1e-8`, and `dim T S_2` equals `K(2N-K)` exactly.
5. `S_1 subset S_2` holds constructively: every `D + rank-K` matrix has all
   minimal disjoint cross-block `(K+1)`-minors below `1e-8` relative.

## 6. What this derivation does not claim

- No global converse for `K >= 2`. Section 3 is a local statement at generic
  points, supported by a Jacobian rank computation, not a proof of variety
  equality.
- Tangent ranks are computed by finite differences at `h = 1e-6` and read at a
  relative threshold of `1e-6`; they are numerical ranks, not exact ones.
- Theorem 11 requires three specific anchor entries to be nonzero. It says
  nothing about matrices with sparse off-diagonal support.
- No sampling theory anywhere. These are statements about population matrices.
