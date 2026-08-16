# What non-identification costs a trader

## Claim being derived

The paper establishes that the impact matrix is only partially identified and
that the cost of a given trade inherits an interval. It does not yet answer the
question a desk would ask: **if I optimise my execution against the confounded
matrix instead of the true one, how much do I actually lose?**

The answer is more favourable than the identification results alone suggest,
and it is worth stating precisely because it bounds the practical damage.

## Setup

Let `Lambda_s = sym(Lambda)` be the true symmetric cost matrix, positive
definite, and let `A_s = sym(A) = Lambda_s + G_s` be its confounded
counterpart. Only the symmetric part matters, since `x' M x = x' sym(M) x`.

A trader must complete a position described by one linear constraint
`c' x = 1` and minimises believed cost:

```
x_A = argmin { x' A_s x : c' x = 1 } = A_s^{-1} c / (c' A_s^{-1} c),
```

and pays the true cost `x_A' Lambda_s x_A`. Define

```
Regret = x_A' Lambda_s x_A  -  x_L' Lambda_s x_L,     x_L = x(Lambda_s).
```

## 1. An exact identity

**Theorem D.** With `delta = x_A - x_L`,

```
Regret = delta' Lambda_s delta.                                          (1)
```

*Proof.* Both trades satisfy the constraint, so `c' delta = 0`. The objective
is quadratic and `x_L` is its minimiser on the affine set, so the gradient
`2 Lambda_s x_L` is orthogonal to every feasible direction, giving
`delta' Lambda_s x_L = 0`. Expanding
`(x_L + delta)' Lambda_s (x_L + delta)` and cancelling the cross term leaves
(1). ∎

Regret is therefore non-negative always, and equals the true cost of the
*error in the trade*, not of the error in the matrix. Verified to `1.1e-17`.

## 2. The damage is second order

**Theorem E.** Write `A_s = Lambda_s + eps G_s` and let

```
Pi = I - c c' Lambda_s^{-1} / (c' Lambda_s^{-1} c).
```

Then `delta = -eps Lambda_s^{-1} Pi G_s x_L + O(eps^2)`, and consequently

```
Regret = eps^2 (Pi G_s x_L)' Lambda_s^{-1} (Pi G_s x_L) + O(eps^3).       (2)
```

*Proof.* The first-order condition is `A_s x = mu c` with `c' x = 1`.
Perturbing, `Lambda_s delta + eps G_s x_L = (d mu) c + O(eps^2)`, so
`delta = Lambda_s^{-1}((d mu) c - eps G_s x_L)`. Imposing `c' delta = 0` gives
`d mu = eps (c' Lambda_s^{-1} G_s x_L)/(c' Lambda_s^{-1} c)`, which is the
stated first-order form. Substituting into (1) gives (2), the `O(eps^2)` term
of `delta` contributing only at order `eps^3`. ∎

**This is the practically important statement in the paper.** A
*first-order* error in the impact matrix produces only a *second-order* loss in
execution cost. Non-identification of the parameter is far less damaging to the
decision than to the estimate.

### Numerical verification

At `N = 20`, seed `1729`, with `||G_s||_F = 1`, the predicted leading constant
is `0.003388738`:

| `eps` | Regret | `delta' Lambda_s delta` | identity error | `Regret / eps^2` |
| ---: | ---: | ---: | ---: | ---: |
| 0.20000 | 1.2956505e-04 | 1.2956505e-04 | 1.11e-17 | 0.003239126 |
| 0.10000 | 3.3098731e-05 | 3.3098731e-05 | 7.40e-18 | 0.003309873 |
| 0.05000 | 8.3706340e-06 | 8.3706340e-06 | 3.59e-18 | 0.003348254 |
| 0.02500 | 2.1051424e-06 | 2.1051424e-06 | 2.44e-18 | 0.003368228 |
| 0.01250 | 5.2787740e-07 | 5.2787740e-07 | 1.62e-17 | 0.003378415 |
| 0.00625 | 1.3217030e-07 | 1.3217030e-07 | 6.76e-18 | 0.003383560 |

The ratio rises monotonically to the predicted constant, and successive
halvings of `eps` divide the regret by `3.91, 3.95, 3.98`, approaching the
factor of four that a second-order law requires.

At `eps = 0.4` the regret is `0.87%` of the optimal cost; at `eps = 0.05` it is
`0.015%`. For context, the identified *interval* for the cost of a fixed trade
at comparable confounding is wide enough to be economically meaningful. The
interval and the regret are different objects, and only the second is what a
trader loses by acting.

## 3. When the gap is free

**Theorem F.** `Regret = 0` if and only if `Pi G_s x_L = 0`, equivalently
`G_s x_L in span(c)`.

*Proof.* Immediate from (1) and the first-order form of `delta`, using positive
definiteness of `Lambda_s`. ∎

**Corollary F.1.** Any `G_s = alpha Lambda_s` gives zero regret: the confounded
matrix is a rescaling, the argmin is scale invariant, and the trader's action
is unchanged. Verified: `||Pi G_s x_L|| = 7.1e-17` and regret `-1.4e-17`.

This is the decision-side analogue of Theorem B. Theorem B says a trade whose
flow exposure avoids `col(W)` has a point-identified cost. Theorem F says a
*confounding gap* that acts on the optimal trade only along the constraint
direction costs nothing at all, whatever it does to the matrix entries.

## 4. Predictions frozen before implementation

Deterministic checks at seed `1729`, `N = 20`, `||G_s||_F = 1`.

1. Identity (1) holds to `1e-15` absolute at every `eps` in the Section 2 grid.
2. `Regret >= 0` at every `eps` on the grid, and at 200 random symmetric gaps.
3. `Regret / eps^2` is monotonically increasing over the grid and lies within
   `2%` of `0.003388738` at `eps = 0.00625`.
4. Successive halvings give ratios in `(3.8, 4.0)` and increasing.
5. `G_s = alpha Lambda_s` gives regret below `1e-14` for `alpha` in
   `{-0.5, 0.6, 2.0}`, while a generic gap at `eps = 0.05` gives regret above
   `1e-8`.

**Correction, made at implementation and recorded rather than silently
applied.** Prediction 5 was first written as "a generic gap *of the same
Frobenius norm*" as `alpha Lambda_s`. That comparison is ill-posed: those gaps
have norm `|alpha| ||Lambda_s||_F`, and a generic perturbation that large
drives the believed matrix indefinite — its smallest eigenvalue was `-0.537` —
so the trader's minimisation is unbounded and no trade exists to be compared.
The rescaling gaps are exempt only because they preserve positive definiteness
for `alpha > -1`, which is precisely why they are a special case. The
prediction now fixes the generic comparison at `eps = 0.05`, inside the
admissible region. The substantive claim is unchanged; the ill-posed
normalisation is not.

## 5. What this does not claim

- One linear constraint only. A trader facing several constraints, inventory
  bounds, or a multi-period schedule is outside this statement.
- `Lambda_s` positive definite. Where it is not, the minimisation is unbounded
  and regret is not defined.
- Static and frictionless: no risk term, no alpha, no participation limit. The
  quadratic cost is the entire objective.
- Second-order **locally**. The constant in (2) can be large, and the
  expansion says nothing at gaps that are not small relative to `Lambda_s`.
  At `eps = 0.4` the observed ratio already differs from the limit by `4%`.
- It does not restore identification. The trader still cannot learn `Lambda`;
  the result says only that this particular decision is insensitive to what
  cannot be learned.
