# Restoring identification with two proxies

## Claim being derived

Everything established so far is negative or partial: the structural matrix is
set-identified, the identified set is wide enough to contain zero, and the
pure-confounding explanation is refutable but not the only explanation for a
rejection. This document supplies the constructive counterpart.

**One noisy factor proxy does not identify the structural impact matrix. Two,
with independent measurement errors, identify it exactly — and not merely a
diagonal one, but a general `Lambda`.**

## 1. Setting

Take the no-feedback system

```
r = Lambda q + Gamma f + u,        q = Delta f + v,
```

with `f`, `u`, `v` mutually uncorrelated, and suppose two proxies are observed:

```
h1 = f + e1,        h2 = f + e2,
```

with `e1` and `e2` uncorrelated with each other and with `f`, `u`, `v`. Write
`Cov(x,y) = E[x y']` throughout, so `Sigma_rq` is `N x N`, `Sigma_rh` is
`N x K`, and `Delta` is `N x K`.

## 2. The identification chain

**Theorem 11 (two-proxy point identification).** Under the assumptions above,
with `Sigma_f` and `Sigma_v` nonsingular,

```
Sigma_f  = Cov(h1, h2)                                                  (1)
Delta    = Cov(q, h1) Sigma_f^{-1}                                      (2)
Lambda   = [ Sigma_rq - Sigma_rh Delta' ] [ Sigma_qq - Delta Sigma_f Delta' ]^{-1}
                                                                        (3)
```

and `Lambda` is point identified.

*Proof.* Because `e1` and `e2` are uncorrelated with each other and with `f`,
`Cov(h1,h2) = Cov(f,f) = Sigma_f`, giving (1) — the step a single proxy cannot
take, since `Cov(h,h) = Sigma_f + Sigma_e` confounds the factor covariance with
the measurement error. Next `Cov(q,h1) = Cov(Delta f + v, f + e1) =
Delta Sigma_f`, giving (2). Then
`Cov(r,h1) = (Lambda Delta + Gamma) Sigma_f`, so
`Gamma = Sigma_rh Sigma_f^{-1} - Lambda Delta`. Substituting into
`Sigma_rq = Lambda Sigma_qq + Gamma Sigma_f Delta'` gives

```
Sigma_rq = Lambda Sigma_qq + Sigma_rh Delta' - Lambda Delta Sigma_f Delta'
         = Lambda ( Sigma_qq - Delta Sigma_f Delta' ) + Sigma_rh Delta',
```

which rearranges to (3). The bracket being inverted is exactly `Sigma_v`, the
idiosyncratic flow covariance, since
`Sigma_qq = Delta Sigma_f Delta' + Sigma_v`. ∎

**Remark.** The inverted matrix is `Sigma_v`, not `Sigma_qq`. Identification
therefore requires idiosyncratic flow variation: if every asset's order flow
were driven purely by the common factors, `Sigma_v` would be singular and no
amount of proxy information would help.

### Numerical verification

At `N = 12`, `K = 3`, seed `1729`, with a **general** (non-diagonal)
`Lambda`, using exact population moments:

| Quantity | Error |
| --- | ---: |
| `Cov(h1,h2)` against `Sigma_f` | 0.000e+00 |
| `Delta` from (2) | 4.44e-16 |
| **`Lambda` from (3)** | **1.79e-15** |
| Inner bracket against `Sigma_v` | 2.22e-15 |

Every dimension, transpose and covariance convention in (1)–(3) was checked
against these moments before the result was written down.

## 3. One proxy is not enough

With a single proxy `h = f + e`, `Cov(h,h) = Sigma_f + Sigma_e` overstates the
factor covariance, so (2) returns an attenuated `Delta` and (3) inherits the
error. On the same fixture:

| Estimator | max abs error in `Lambda` |
| --- | ---: |
| Naive regression coefficient `Sigma_rq Sigma_qq^{-1}` | 0.463 |
| One noisy proxy | 0.330 |
| **Two independent proxies** | **1.8e-15** |

A single proxy removes roughly a third of the error and leaves the rest. This
is the quantitative form of the paper's earlier remark that a factor control
moves the estimate *along* the confounding directions rather than out of them.

## 4. The independence assumption is a cliff, not a slope

The result requires the two measurement errors to be uncorrelated. That
requirement is far more brittle than "approximately independent is
approximately fine".

Correlating the proxy errors with coefficient `rho`:

| `rho` | 0 | 0.1 | 0.3 | 0.6 | 1.0 |
| --- | ---: | ---: | ---: | ---: | ---: |
| max abs error in `Lambda` | 1.8e-15 | **0.128** | 0.143 | 0.147 | 0.149 |

At `rho = 0.1` the error is already **86%** of the error at perfect
correlation. Identification does not degrade gracefully: it is destroyed almost
entirely by a small violation and barely worsens thereafter.

**Practical consequence.** Two proxies constructed from overlapping data — two
order-flow aggregates over intersecting venues, or two factor estimates sharing
a preprocessing step — will not deliver this result. The assumption to defend
is not "the proxies are different" but "their errors share nothing", and the
table above is the cost of being wrong about that.

## 5. Where this sits on the identification frontier

| Information available | Factor confounding | Feedback | `Lambda` |
| --- | --- | --- | --- |
| `r, q` only | unresolved | unresolved | set identified |
| one noisy factor proxy | reduced, not removed | unresolved | not identified |
| two independent proxies, `B = 0` | resolved | absent by assumption | **point identified** |
| instruments plus proxies, `B != 0` | potentially resolved | potentially resolved | open |

The last row is not addressed here. Two proxies resolve the factor-confounding
channel; they say nothing about same-bin feedback, which needs an exclusion
restriction or a timing argument rather than more measurement of `f`.

## 6. Predictions frozen before implementation

Deterministic checks on exact population moments at seed `1729`, `N = 12`,
`K = 3`, general non-diagonal `Lambda`.

1. `Cov(h1,h2)` equals `Sigma_f` exactly.
2. `Delta` from (2) matches the truth below `1e-12` relative.
3. `Lambda` from (3) matches the truth below `1e-12` relative.
4. The inverted bracket equals `Sigma_v` below `1e-12` relative.
5. The one-proxy estimator and the naive coefficient both have error above
   `0.1`, so the improvement from the second proxy is not marginal.
6. With proxy-error correlation `0.1` the error exceeds `0.1`, confirming the
   cliff rather than a gradual degradation.

## 7. What this does not claim

- **`B = 0` throughout.** With same-bin feedback the derivation breaks at the
  first substitution, and two proxies do not repair it. Feedback needs a
  different instrument.
- **Population moments only.** No sampling theory, no standard errors, no
  finite-sample behaviour. Equations (1)–(3) are identification statements.
- **No claim that two such proxies exist in any market.** Constructing two
  order-flow or factor proxies with genuinely uncorrelated errors is an
  empirical problem this document does not solve, and Section 4 shows the bar
  is high.
- **Unit loading assumed.** Both proxies load on `f` with the identity. General
  loading matrices are a natural extension and are not treated here.
- No registered stream, market data, or holdout was involved.
