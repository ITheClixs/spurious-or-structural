# Low-rank departure test pre-run prediction

Registered on 2026-08-12 after the derivation in
`docs/derivations/PSI_NULL_DISTRIBUTION.md` and its disclosed exploratory
pilot, and before any bootstrap implementation or confirmatory run existed.

## Pilot disclosure

The size and power tables in Section 4 of the derivation were produced at test
seeds `1729` and `9191` **before** this registration. They are exploratory
pilot evidence used to form the predictions below and are not confirmatory. The
confirmatory run uses a fresh sampling seed `314159`.

## Confirmatory design, fixed before the run

Fixture seed `1729`; sampling seed `314159`; `N = 30`; `K = 3`; `M = 150`
replicates; `B = 199` bootstrap draws; `alpha = 0.05`; one-spike regressor
covariance at `s_q = 0.2827`; unit residual scale. Rejection rates are Monte
Carlo proportions with binomial standard error approximately `0.018` at
`M = 150`, which is the named interval method.

## Predictions

1. **Size at the usable sample size.** At `T = 5000` the realised rejection
   rate lies within `0.05 +/- 0.045`.
2. **Small-sample failure is real.** At `T = 500` the realised rejection rate
   exceeds `0.15`.
3. **Monotone improvement.** Realised size is nonincreasing across
   `T in {500, 1000, 2000, 5000}`, allowing one Monte Carlo standard error of
   slack per adjacent pair.
4. **The variance inflation over-corrects.** The variance-inflated variant has
   realised size below `0.01` at every `T` in that set.
5. **Power.** At `T = 5000`, power against a dense off-diagonal perturbation of
   Frobenius size `eps = 0.20` exceeds `0.80`, and power against `eps = 0.05`
   does not exceed `0.20`.

## Intervals and reporting

Rejection rates are Monte Carlo proportions and are reported with the binomial
standard error at `M = 150`. No other quantity in this slice is inferential;
the manifold dimension, the inflation factor, and the statistic itself are
deterministic.

## Failure interpretation fixed before the run

- If prediction 1 fails, the bootstrap does not control size at any examined
  sample size. The manuscript then reports `psi_K` as a descriptive statistic
  with a documented size distortion and withdraws the claim that it is a test.
- If prediction 2 fails, the small-sample failure was a seed artifact and the
  usage bound is re-derived rather than asserted.
- If prediction 4 fails, the variance inflation is re-examined and may be
  adopted; it is currently registered as not adopted.
- If prediction 5 fails, the test is reported as size-correct but underpowered,
  and the manuscript states the alternative sizes it can and cannot detect.
- No fixture, seed, replicate count, or bootstrap size is re-drawn to recover a
  predicted number.
