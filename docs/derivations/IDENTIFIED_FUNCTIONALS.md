# Which functionals of the impact matrix survive non-identification

## Claim being derived

The paper's partial-identification result is entrywise, and its one economic
consequence — that a dollar-neutral trade has a point-identified cost — was
stated for a single geometry. Both are instances of something general.

With `B = 0` and `Sigma_f = I_K`, write `W = Sigma_qq^{-1} Delta_f`. Every
member of the identified set has the form `Lambda = A - Gamma W'`, so a
functional is identified exactly when the `Gamma W'` term cannot move it.

The answer, for both linear and quadratic functionals, depends only on whether
the functional's **flow argument** is orthogonal to the column space of `W`.

## 1. Linear functionals

**Theorem A.** For `a, b` in `R^N` with `a != 0`, the functional
`L(Lambda) = a' Lambda b` is point identified over the identified set if and
only if `W' b = 0`.

*Proof.* `a' Lambda b = a' A b - (a' Gamma)(W' b)`. The first term is
observable. Since `Gamma` ranges over an open set, `a' Gamma` ranges over a
neighbourhood in `R^K` whenever `a != 0`, so the second term is constant across
the identified set exactly when `W' b = 0`, in which case it is zero. ∎

**Remark (the asymmetry is real).** The condition constrains `b`, the flow
argument, and says nothing about `a`. Choosing a response direction orthogonal
to the confounding subspace buys nothing. Verified: with `b` free the spread of
`a' Lambda b` across the identified set is `6.65`; making `a` orthogonal to
`col(W)` leaves it at `7.40`; making `b` orthogonal collapses it to `3.0e-15`.

## 2. Quadratic functionals, and the general form of the cost result

**Theorem B.** For `x != 0`, the execution cost `C_x(Lambda) = x' Lambda x` is
point identified if and only if `W' x = 0`.

*Proof.* Theorem A with `a = b = x`. ∎

Measured spread across the identified set: `13.4` for a free `x`, and
`3.6e-15` for `x` orthogonal to `col(W)`.

**Corollary B.1 (the dollar-neutral case is one instance).** In the
permutation-invariant one-spike geometry, `Delta_f = h_q m` and
`Sigma_qq m = q_1 m`, so `W = (h_q/q_1) m` and `col(W) = span(m)` — verified to
`|cos| = 1.000000000000`. The condition `W' x = 0` therefore reduces to
`m' x = 0`, that is, dollar-neutrality. The corollary the manuscript reports is
the one-spike instance of Theorem B and holds for no other reason.

This is the general statement the paper should make: **parameter identification
and decision identification are different objects.** A decision whose flow
exposure avoids the confounding subspace is identified even though no entry of
the matrix producing it is.

## 3. The width of the identified interval

**Theorem C.** Let the admissible loadings satisfy `||Gamma||_F <= R`. Then

```
width { x' Lambda x : Lambda in I(A) } = 2 R ||x|| ||W' x||.            (1)
```

*Proof.* `x' Gamma W' x = <Gamma, x w'>` in the Frobenius inner product, with
`w = W' x`. The supremum of a linear functional over a Frobenius ball of radius
`R` is `R ||x w'||_F = R ||x|| ||w||`, attained at
`Gamma* = R (x w') / ||x w'||_F`, and the infimum is its negative. ∎

Verification against the attaining `Gamma*`:

| `||x||` | `||W'x||` | closed form (1) | attained at `Gamma*` |
| ---: | ---: | ---: | ---: |
| 3.7203 | 0.107090 | 0.796807 | 0.796807 |
| 3.2824 | 0.214180 | 1.406033 | 1.406033 |
| 5.0904 | 0.428360 | 4.361077 | 4.361077 |
| 5.6159 | 0.856719 | 9.622523 | 9.622523 |

**A wrong first attempt, recorded.** The width was initially conjectured
proportional to `||W' x||` alone. Measured ratios were `3.44, 4.28, 2.58,
5.28` — not constant, which is what exposed the error: the trade norm enters
too. A random search over 20,000 directions also undershot the true supremum by
roughly a factor of two, since it cannot find a maximiser in a `K N`-dimensional
ball. Both the closed form and its attaining point are needed; sampling the
constraint set is not a substitute.

## 4. Predictions frozen before implementation

Deterministic checks at seed `1729`, `N = 20`, `K = 3`.

1. With `b` orthogonal to `col(W)`, the spread of `a' Lambda b` over 200
   members of the identified set is below `1e-12`; with `b` free it exceeds
   `1.0`.
2. Making `a` orthogonal to `col(W)` while leaving `b` free does **not** reduce
   the spread below `1.0`, confirming the asymmetry.
3. With `x` orthogonal to `col(W)`, the spread of `x' Lambda x` is below
   `1e-12`; with `x` free it exceeds `1.0`.
4. In the one-spike geometry `col(W) = span(m)` to `1e-10`.
5. The closed-form width (1) matches the value attained at `Gamma*` to `1e-10`
   relative, across the four trade scales tabulated above.

## 5. What this does not claim

- `B = 0` throughout, and `Sigma_f = I_K` by normalisation.
- The admissible set is idealised as a Frobenius ball of radius `R`. The true
  constraint is positive semidefiniteness of the implied residual covariances,
  which is contained in such a ball but is not one; (1) is therefore an upper
  bound on the true width, tight when the binding constraint is spherical.
- No sampling theory. These are population statements about an identified set.
- Nothing here identifies `Lambda` itself; it partitions functionals into those
  that survive non-identification and those that do not.
