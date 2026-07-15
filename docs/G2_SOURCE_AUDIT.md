# G2 primary-source audit

Opened and checked on 2026-07-15 before G2 implementation or any G2 random
draw. Page references are printed pages unless marked as PDF pages. Reported
dispersion statistics are not silently promoted to confidence intervals.

## What the published opponent actually is

Cont, Cucuringu, and Zhang, [*Cross-impact of order flow imbalance in equity
markets*](https://arxiv.org/abs/2112.13213), arXiv v4 PDF SHA256
`8a8559063f7bbe93827407cddd21b41d5b7ba80870772f2800a835b77cee44c9`,
does **not** publish a single regression combining multi-level integrated OFI
with a cross-sectional flow-factor control.

The equation-exact specification suite is below. Because the paper omits
several numerical implementation details, the executable version is a
preregistered protocol reconstruction rather than byte-exact author code:

- `PI[1]`, Eq. (6), p. 9: return on own best-level OFI, OLS.
- `PI^I`, Eq. (7), p. 9: return on own integrated top-ten-level OFI, OLS.
- `CI[1]`, Eq. (8), pp. 9--10: return on every asset's best-level OFI, LASSO.
- `CI^I`, Eq. (9), p. 10: return on every asset's integrated OFI, LASSO.
- `PI^CC`, Appendix C Eqs. (20) and (22), pp. 36--37: return on cross-sectional
  best-level OFI PC1 and own residual OFI.
- `CI^CC`, Appendix C Eqs. (20) and (21), pp. 36--37: return on that PC1 and all
  residual OFIs, with LASSO in the second step.

The paper uses one-minute physical-time bins, excludes the first and last 30
minutes, fits non-overlapping 30-minute blocks between 10:00 and 15:30, and
tests on the following block (pp. 5, 11, 16). The paper says LASSO penalties are
chosen separately by cross-validation, but does not disclose feature scaling,
fold chronology, lambda grid, selection rule, solver tolerance, or whether the
factor is penalized. Those omissions are implementation uncertainty, not
license to choose after seeing G2 output.

The top-ten-level construction is exact: every level OFI uses the common mean
depth denominator in Eq. (3), and integrated OFI is the first within-asset PC
score divided by the loading vector's L1 norm in Eq. (4), pp. 5--7. Across
stock-days, PC1 explains 89.06% of the ten-level variance, with cross-sectional
SD 6.12 percentage points; all reported pairwise level correlations exceed
75% (Fig. 1 and Table 2, pp. 7--8). These are within-asset depth statistics,
not cross-asset flow-factor strength.

The strongest exact own model, `PI^I`, has mean out-of-sample R-squared 83.83%
(cross-sectional/window SD 16.90 points), while `CI^I` has 83.62% (SD 14.53),
Table 5, p. 16. Appendix C reports 64.78% (SD 19.95) for `PI^CC` and 65.36%
(SD 18.68) for `CI^CC`, Table C.1, p. 37. These dispersion figures are not
confidence intervals. Because CCZ does not publish the desired combined
estimator, S0004 does not label an integrated-OFI-plus-factor hybrid as paper
exact. Instead, that observable hybrid is a deliberately strengthened
gate-binding opponent with a declared 95%-reliable proxy. Two oracle-`q` fits
are gate-binding no-strawman checks. `CI_I`, the only published CCZ equation
with both integrated top-ten OFI and explicit off-diagonal coefficients, is a
separate gate-binding published-protocol veto at the upper structural endpoint.
The other five CCZ reconstructions remain mandatory estimand-specific
diagnostics.

## Cross-asset commonality and factor alignment

Capponi and Cont, [*Multi-Asset Market Impact and Order Flow
Commonality*](https://ssrn.com/abstract=3706390), DOI
[10.2139/ssrn.3706390](https://doi.org/10.2139/ssrn.3706390), was opened from
the SSRN record and the author-uploaded full text. It studies 67 continuously
covered NASDAQ-100 stocks at one-minute frequency from January 2008 through
June 2010.

- Mean pairwise OFI correlation is 0.26 with cross-sectional SD 0.09; mean
  cross-stock return--OFI correlation is 0.25 with SD 0.07 (p. 10, Fig. 2).
- OFI correlation eigenvalues are 18.94, 1.29, and 1.21, explaining 28.27%,
  1.92%, and 1.80%; no inferential intervals or lower spectrum are reported
  (p. 13, Table 1).
- Return correlation eigenvalues are 21.44, 1.70, and 1.48, explaining 32.00%,
  2.54%, and 2.21%; no inferential intervals are reported (p. 13, Table 1).
- Correlations between corresponding return and OFI factor scores are 87.26%,
  53.88%, and 37.16%; no inferential intervals are reported (pp. 14--15,
  Fig. 7).
- Before factor control, mean own and cross coefficients are 2.64 (SD 0.78)
  and 0.032 (SD 0.06), so the mean cross/own ratio is about 1.2%; 23.09% of
  cross coefficients are negative (pp. 10--11, Figs. 4--5).
- After PC1 control, mean own, cross, and factor coefficients are 2.57
  (SD 0.77), -0.039 (SD 0.06), and 2.50 (SD 0.39); 84.46% of cross
  coefficients are negative (pp. 17--19, Fig. 9). This is evidence of
  coefficient instability, not proof that the controlled coefficient is
  causal.
- Adding all residual cross flows changes mean adjusted R-squared from 43.31%
  to 43.84%, both with cross-sectional SD about 9.8 points (pp. 17--18,
  Fig. 10). These are not inferential intervals.

Hasbrouck and Seppi, [*Common Factors in Prices, Order Flows and
Liquidity*](https://w4.stern.nyu.edu/finance/docs/WP/1999/pdf/wpa99011.pdf),
author PDF SHA256
`74ebf62a498de0372728e290eb72efc6a4aee7d4ddac5a513d93aa4f42b487bb`,
provides the lower-strength comparator. For 30 Dow stocks over all 252 trading
days of 1994 in 15-minute bins, return PC1 is 6.32/30 = 21.07% and signed
square-root-dollar-flow PC1 is 4.06/30 = 13.53% (printed pp. 23--24, Tables
2--3). The first return/flow principal components correlate 0.82, and the first
canonical correlation is 0.83. No inferential interval is reported for these
factor quantities; the paper gives an approximate SE 0.12 for the return PC1
eigenvalue only (p. 11).

The one-minute Capponi--Cont triple `(28.27%, 32.00%, 87.26%)` is the
confirmatory observable point. Hasbrouck--Seppi's `(13.53%, 21.07%, 82%)`
triple uses 15-minute signed square-root-dollar flow in an older universe and
is therefore a historical comparator, not the lower endpoint of a joint
one-minute confidence box. Neither paper supplies inferential intervals for
the triple.

## Cross-impact scale

Benzaquen, Mastromatteo, Eisler, and Bouchaud, [*Dissecting cross-impact on
stock markets*](https://arxiv.org/abs/1609.02395), PDF SHA256
`e403b9a5e9689eb4261b050063adae2f7fd78515c07097671c48c3869d168703`,
uses 275 normalized US-equity return and trade-sign series in five-minute bins.
Its homogeneous propagator has `G_diag = 0.29` and `G_off = 0.0046`, a 1.59%
ratio (p. 15, Eqs. 14--16). No coefficient interval is reported. The authors
explicitly state that individual entries of the unrestricted matrix cannot be
estimated reliably (p. 15). Both `d = 0.29` and
`o / d in [0.0100, 0.015862...]` are structural sensitivity choices, not
identified one-minute OFI coefficients. The 1% lower endpoint is the
preregistered economic-materiality floor and a conservative round-down from
Capponi--Cont's approximately 1.2% reduced-form mean ratio; it is not an
empirical lower confidence bound. The upper endpoint is motivated by
Benzaquen et al.'s normalized propagator ratio. No point in this interval is
called a one-minute structural calibration.

The paper also documents a negative-lag response: current returns predict
subsequent sign imbalance (p. 7, Fig. 1), but supplies no scalar simultaneous
feedback coefficient there.

## Own price-chasing feedback

Takahashi, [*Returns and Order Flow Imbalances: Intraday Dynamics and
Macroeconomic News Effects*](https://arxiv.org/abs/2508.06788), PDF SHA256
`79bb14f8e7d8d859e971187825433511c6d0ce00f1ff267be24887a48bbb95b2`,
estimates the bivariate simultaneous system on 34,512,298 one-second E-mini
S&P 500 observations from 2008--2013 using identification through
heteroskedasticity (Eqs. 2--9, pp. 6--8).

Across 37,029 identified 15-minute intervals, the return-to-flow coefficient
has mean 0.301, median 0.246, interquartile range 0.133--0.419, and empirical
5th--95th percentiles 0--0.772; 71% have absolute t-statistic above two
(p. 12, Table 3). These percentiles are empirical dispersion, not confidence
intervals. Returns are in basis points and OFI in thousands of contracts;
sample SDs are 0.91 and 0.52 respectively (p. 4, Table 1). The dimensionless
standardized median is therefore `0.246 * 0.91 / 0.52 = 0.4302692308`, and the
standardized first quartile is `0.23275`.

This is a single-asset own-feedback estimate at a different frequency and for a
different market. No opened source identifies a contemporaneous cross-asset
feedback matrix or supplies a defensible aggregation bridge. The redesigned G2
confirmatory fixture therefore sets `B = 0` and makes a confounding-only claim.
The Takahashi values remain reference sensitivities and do not enter the gate.

## What remains unidentified before G2

No opened primary source supplies the full structural tuple
`(Lambda, B, Gamma, Delta_f, Sigma_f, Sigma_u, Sigma_v, Sigma_epsilon)`.
In particular, none identifies cross-asset `B`, a factor-proxy error covariance,
or the lower spectrum/condition number of cross-asset OFI. G2 cannot infer
those objects from the source summaries.

The redesigned test addresses that gap without pretending to identify it:

1. the confirmatory observable covariance is the unique
   permutation-invariant one-spike correlation law with Capponi--Cont's
   one-minute leading shares; its implied pairwise flow correlation is
   `0.2579655`, reproducing the published `0.26` to reported precision;
2. residual eigenvalues are isotropic by a declared maximum-entropy convention,
   eliminating unsourced asset ordering and PC2/PC3 orientation choices;
3. `B = 0` isolates confounding. The primary observable opponent uses the
   paper's integrated top-ten construction plus an independent oracle-loading
   proxy; two oracle-flow opponents separately rule out measurement error and
   high-dimensional inversion as explanations;
4. 95% proxy reliability is deliberately favorable to the opponent and is not
   called an empirical estimate; the estimator is not given the proxy-error
   variance, matching the real identification problem;
5. the absolute diagonal and cross/own interval are labeled structural
   sensitivities: the 1% floor is a conservative round-down from
   Capponi--Cont's reduced-form mean ratio and the upper ratio comes from
   Benzaquen, while Hasbrouck--Seppi and Takahashi remain nonconfirmatory
   comparators; and
6. the published `CI_I` protocol reconstruction is a binding veto because it is
   the only opened CCZ equation with integrated OFI and off-diagonal
   coefficients; and
7. a positive result is conditional-existence evidence only. A negative result
   is unadjudicated unless a sharp upper bound over all source-compatible
   decompositions and reliabilities is also below the materiality threshold.

The operating brief's attribution `arXiv:2009.10863` for Capponi--Cont is
incorrect: that identifier is an unrelated computational-fluid-dynamics paper.
The verified record is SSRN 3706390 / DOI 10.2139/ssrn.3706390.
