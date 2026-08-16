# Testing the cross-block restriction on dependent data

## Claim being derived

Theorem 9 is a population statement: under the maintained null,
`sigma_{K+1}(A_{I,J}) = 0` exactly. Estimated from data that singular value is
positive almost surely, so the theorem is not yet a test. This document builds
one and reports what it can and cannot detect.

The binding difficulty is dependence. High-frequency panels have `N T`
observations but nothing like `N T` independent ones: order flow and returns
are serially correlated within a trading day. Any procedure that resamples bins
independently is asserting an independence the data does not have.

## 1. The statistic and the bootstrap

Let dates `d = 1..D` each contribute `B` bins. Accumulate per-date sufficient
statistics `S_rq^d = sum_t r_t q_t'` and `S_qq^d = sum_t q_t q_t'`, so that for
any nonnegative date weights `w`,

```
A(w) = [ sum_d w_d S_rq^d ] [ sum_d w_d S_qq^d ]^{-1}.
```

The observed statistic is `T_obs = sigma_{K+1}(A(1)_{I,J})` for disjoint
`I, J`. To bootstrap it we must impose the null, since the null fixes a
singular value at zero rather than fixing a parameter. Let `A^{(K)}` be the
rank-`K` truncation of the observed block. One bootstrap replicate draws date
weights `w*`, forms the perturbation `Delta* = A(w*)_{I,J} - A(1)_{I,J}`, and
computes

```
T* = sigma_{K+1}( A^{(K)} + Delta* ).                                    (1)
```

The `p`-value is the fraction of replicates with `T* >= T_obs`. Recentring on
`A^{(K)}` is what makes the bootstrap distribution a null distribution: it
transplants the estimated sampling variation onto a block that satisfies the
restriction exactly.

**Date-cluster scheme.** `w*` is the multiplicity vector of `D` dates drawn
with replacement. Whole days move together, so within-day dependence of any
form is preserved without being modelled.

**Independent-bin scheme (for comparison only).** `w*` is a multinomial draw
over `D B` bins, rescaled. This is the procedure implied by treating bins as
independent observations.

## 2. What the two schemes do

Simulated panels with `N = 20`, `K = 2`, `B = 100` bins per date, AR(1)
persistence `rho = 0.6` in factors, idiosyncratic flow, and return
disturbances; `I = {0..5}`, `J = {10..15}`; 299 bootstrap replicates; 200
Monte Carlo replications.

| scheme | rejection at 5% under the null | at 10% |
| --- | ---: | ---: |
| date-cluster | **0.040** | **0.080** |
| independent-bin | **1.000** | **1.000** |

The independent-bin bootstrap rejects a true null **every single time**. This
is not a mild size distortion to be noted and moved past: the procedure is
worthless, and any cross-impact rank test that resamples high-frequency
observations independently will manufacture rejections out of serial
correlation alone. The date-cluster bootstrap holds its nominal level.

## 3. What the test can detect

Rejection rate at the 5% level, date-cluster scheme, 150 replications. The
alternative adds a dense off-diagonal perturbation to a diagonal `Lambda`,
scaled so its largest entry is `cross`, against own-impact terms in
`[0.2, 0.4]`.

| dates `D` | `cross = 0` | 0.05 | 0.10 | 0.20 | 0.40 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 50 | 0.040 | 0.227 | 0.873 | 1.000 | 1.000 |
| 200 | 0.053 | 0.920 | 1.000 | 1.000 | 1.000 |

Size is correct at both panel lengths. Power is real but not free: at fifty
dates the test needs cross-impact around a quarter of own-impact before it
reliably rejects, while at two hundred dates it detects a fifth of that. **A
non-rejection on a short panel is close to uninformative**, and any application
must report `D` alongside the `p`-value rather than the `p`-value alone.

**Provenance.** Both tables above were regenerated from the shipped
implementation (`xid.crossblock_study.rejection_rate`) and agree with the
exploratory run to the last digit reported. The four registered predictions are
executed as tests behind `XID_RUN_SLOW_INFERENCE=1`, taking roughly a minute.

## 4. Reporting rule

The restriction is stated for a given factor budget, and the budget is not
observable. Applications must therefore report the whole map

```
K  |-->  p_K
```

over a prespecified range of `K`, together with `D`, `B`, the index sets used,
and the number of bootstrap replicates. Selecting `K` to obtain a preferred
outcome and reporting only that value is exactly the practice this design
exists to prevent.

## 5. Predictions frozen before implementation

Deterministic given seeds; Monte Carlo seed `4242`, panel seeds `9000 + r`.

1. Under the null at `D = 50`, the date-cluster rejection rate at the 5% level
   lies in `[0.01, 0.09]`, and at the 10% level in `[0.05, 0.15]`.
2. Under the same null the independent-bin rejection rate at the 5% level
   exceeds `0.5`, demonstrating that ignoring within-day dependence invalidates
   the test.
3. Power at `D = 50` is increasing in `cross` across `{0, 0.05, 0.10, 0.20}`
   and reaches at least `0.8` by `cross = 0.10`.
4. Power at `D = 200` exceeds power at `D = 50` at `cross = 0.05`, by at least
   `0.3` in absolute terms.
5. The `p`-value is invariant to relabelling the bootstrap draws: two runs at
   the same seed agree exactly, and the statistic itself is unchanged by
   permuting the order of dates in the sufficient statistics.

## 6. What this does not claim

- One dependence structure. AR(1) within dates with independent dates is a
  caricature: real panels have overnight effects, intraday seasonality, and
  cross-date persistence. Independence *across* dates is assumed and is the
  assumption the date-cluster scheme rests on.
- No asymptotic theory. The bootstrap's consistency for `sigma_{K+1}` under
  this recentring is not proved here; the evidence is the simulated size in
  Section 2, at one design.
- `K` is given, not selected. Section 4 states the reporting rule that follows.
- Simulated data only. No market data, no registered stream, and no claim
  about any real market is made or implied.
- The alternative is one family — dense off-diagonal perturbations. Sparse or
  structured cross-impact may be easier or harder to detect.
