# A finite-sample null distribution for the low-rank departure statistic

## Claim being derived

`docs/redteam/THEORY_EXTENSION.md` records as its strongest unresolved
objection that `psi_K` has no sampling distribution: Proposition 5 is a
population statement, "materially nonzero" was never operationalised, and the
statistic as shipped was a descriptive quantity rather than a test.

This document supplies the missing distribution, and reports honestly where it
works and where it does not.

1. Under `H0` the estimated coefficient matrix is a noisy observation of a
   point in the diagonal-plus-rank-`K` set, so `psi_K` measures the part of the
   estimation error that the low-rank fit cannot absorb. It converges to zero
   at rate `T^{-1/2}`.
2. A **parametric plug-in bootstrap** supplies a critical value.
3. That bootstrap **controls size only for large samples.** At `N = 30` it is
   accurate for `T` of about 5,000 and above, and is severely oversized below:
   the realised rejection rate at nominal 5% is 0.327 at `T = 500`.
4. A **degrees-of-freedom variance inflation fails.** It over-corrects to a
   realised size of exactly zero at every sample size tested, destroying power
   entirely. It is reported because it is the obvious fix and it does not work.

The practical conclusion is a stated minimum sample size, not a general test.

## 1. Sampling model

Row `i` of the coefficient matrix is the population regression of `r_i` on `q`.
Under the standard conditions of `GATE_G1_PROBABILITY_LIMITS.md`, the ordinary
least squares estimator of that row satisfies

```
sqrt(T) ( Â_i· − A_i· )  ->d  N( 0 , sigma_i^2 Sigma_qq^{-1} ),        (1)
```

with rows independent when `Sigma_u` is diagonal. Writing `E = Â − A`, the
finite-sample working model is therefore

```
E = (1/sqrt(T)) Z L^T,     Z_ij iid N(0,1),    L L^T = Sigma_qq^{-1},  (2)
```

scaled rowwise by `sigma_i`. This is a working model, not a theorem about any
market: it inherits the homoskedastic, serially independent, correctly
specified conditions under which Eq. (1) holds.

## 2. The statistic under the null

Under `H0` the population `A` lies in `𝓓_K`, so `psi_K(A) = 0` by
Proposition 5. For the estimate,

```
psi_K(Â) = min_{D, rank(R) <= K} || A + E − D − R ||_F
           / || Â − diag(Â) ||_F.                                      (3)
```

The numerator is `O_p(T^{-1/2})`, because `D` and `R` can be chosen to absorb
`A` exactly and the residual is the component of `E` orthogonal to the tangent
space of `𝓓_K` at `A`. The denominator is `O_p(1)`, being dominated by the
population off-diagonal energy of the rank-`K` term. Hence

```
psi_K(Â) = O_p(T^{-1/2}),                                              (4)
```

so the statistic is consistent against any fixed alternative outside `𝓓_K`, and
its null distribution is tight. The tightness matters: Section 4 shows that a
13.5% inflation of the error scale is enough to move realised size from 0.04 to
exactly 0.

The manifold `𝓓_K` has dimension

```
dim(𝓓_K) = N + K(2N − K),                                             (5)
```

which is `201` at `N = 30`, `K = 3`, against `N^2 = 900` free parameters in an
unrestricted coefficient matrix. The null is therefore a genuine restriction of
codimension `699`.

## 3. The parametric bootstrap

Fixed before use:

1. Compute the observed statistic `psi_K(Â)`.
2. Form the **null projection** `Â_0 = D̂ + R̂` from
   `decompose(Â, K)`, the alternating-projection fit of Definition `psi`.
3. For each of `B` replicates, draw `E*` from Eq. (2) with the estimated
   `Sigma_qq` and `sigma_i`, set `Â* = Â_0 + E*`, and compute `psi_K(Â*)`.
4. The critical value is the upper `1 − alpha` empirical quantile of the `B`
   bootstrap statistics, taken with NumPy's default linear interpolation.
5. Reject `H0` when `psi_K(Â)` exceeds that critical value.

Registered defaults are `B = 199` and `alpha = 0.05`. Ties are impossible at
float64 resolution and no tie rule is required.

**Factor-count rule.** The statistic depends on an assumed `K`, and a free `K`
was half of the original objection. The registered rule is the eigenvalue-ratio
criterion of Ahn and Horenstein applied to the off-diagonal part
`Â − diag(Â)`: choose `K` maximising the ratio of consecutive singular values
over `1 <= k <= k_max` with `k_max = 10`. The rule is fixed before use and is
not re-selected after seeing a rejection.

## 4. What the bootstrap actually delivers

The following are **exploratory pilot results** at test seed `1729` for the
fixture and `9191` for the sampling draws. They are pilot evidence used to form
the registered predictions of Section 5, and are not themselves the
confirmatory check.

Realised rejection rate under `H0` at nominal 5%, `N = 30`, `K = 3`, `M = 150`
replicates, `B = 199`, Monte Carlo standard error about `0.018`:

| `T` | `T / N^2` | Plug-in bootstrap | Variance-inflated |
| ---: | ---: | ---: | ---: |
| 500 | 0.6 | **0.327** | 0.000 |
| 1,000 | 1.1 | **0.147** | 0.000 |
| 2,000 | 2.2 | 0.087 | 0.000 |
| 5,000 | 5.6 | **0.040** | 0.000 |
| 10,000 | 11.1 | 0.033 | 0.000 |

Realised power at `T = 5,000`, against a dense off-diagonal perturbation of
Frobenius size `eps` added to the null matrix, `M = 100`:

| `eps` | 0.05 | 0.10 | 0.20 | 0.40 |
| --- | ---: | ---: | ---: | ---: |
| Rejection rate | 0.070 | 0.210 | 0.940 | 1.000 |

**Diagnosis of the small-sample failure.** The plug-in null `Â_0` is fitted to
the noisy `Â`, so the low-rank fit absorbs part of the estimation error. The
bootstrap statistics are therefore centred below the true null distribution of
`psi_K`, the critical value is too small, and the test over-rejects. The defect
is in the **centre** of the plug-in null, not its scale.

**A failed correction, reported.** The obvious remedy is to inflate the
bootstrap error scale by the degrees-of-freedom factor
`sqrt(N^2 / (N^2 − dim 𝓓_K)) = sqrt(900/699) = 1.1347`. It fails completely:
realised size becomes exactly `0.000` at every sample size tested, so the test
never rejects and has no power at all. This is consistent with Eq. (4): the
null distribution of `psi_K` is tight, so a 13.5% scale change moves the
critical value past essentially the whole distribution. Because the bias is in
the centre rather than the scale, a scale correction cannot fix it. **This
correction is not adopted.** A centre correction, such as a double bootstrap or
an analytic bias adjustment for the fitted low-rank component, would require
its own registered design and is not attempted here.

## 5. Predictions that must survive confirmatory verification

The Section 4 table is a pilot. These predictions are frozen for a
**confirmatory run at a fresh sampling seed** `314159`, with the same fixture
seed `1729`, `M = 150`, `B = 199`, `alpha = 0.05`, Monte Carlo standard error
about `0.018`.

1. At `T = 5000` the realised size lies within `0.05 +/- 0.045`, that is within
   two and a half Monte Carlo standard errors of nominal.
2. At `T = 500` the realised size exceeds `0.15`, confirming severe
   over-rejection in small samples rather than a seed artifact.
3. Realised size is monotonically nonincreasing across
   `T in {500, 1000, 2000, 5000}` up to Monte Carlo error of one standard
   error per adjacent pair.
4. The variance-inflated variant has realised size below `0.01` at every
   `T` in that set, confirming that the correction over-corrects rather than
   merely being imperfect.
5. At `T = 5000`, power against `eps = 0.20` exceeds `0.80`, and power against
   `eps = 0.05` does not exceed `0.20`.

If prediction 1 fails, the test is reported as size-distorted at every sample
size examined and `psi_K` returns to being a descriptive statistic. If
prediction 4 fails, the variance inflation is re-examined rather than
discarded.

## 6. What this derivation does not claim

- The sampling model of Eq. (2) is homoskedastic, serially independent, and
  correctly specified. Market data satisfies none of these, and a dependent
  bootstrap would be a separate registered design.
- The test is **not** valid at small samples. At `N = 30` it should not be used
  below roughly `T = 5000`, and the paper states that bound rather than
  implying general validity.
- `psi_K` remains an upper bound from a stationary point of an alternating
  projection, so the test stays conservative in that respect while being
  anti-conservative in the plug-in respect at small `T`. The two biases are not
  shown to cancel.
- Rejection is evidence against pure confounding within the assumed factor
  count. It does not identify `Lambda`, and non-rejection does not establish
  that the structural matrix is diagonal.
- No registered G2 stream, market data, or holdout is involved. G2 remains open
  and executable-red.
