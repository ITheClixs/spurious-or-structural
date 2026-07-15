# G2 derivation: an observable, label-invariant noisy-control premise test

Derived before G2 implementation, resource benchmarking, validation, or any
registered G2 random draw.

## 1. Claim and boundary

G2 tests a conditional existential claim: can confounding alone be materially
large in a transparent model whose observable factor strength and flow
collinearity match opened primary-source summaries? It does **not** claim that
the real structural tuple or factor-proxy reliability is identified.

The gate-binding observable opponent receives integrated top-ten OFI, the
correct scalar factor direction, and an independent factor proxy with 95%
reliability. Two oracle-flow opponents separately remove measurement error and
high-dimensional inefficiency as explanations. Setting `B = 0` removes
simultaneity. A pass therefore cannot be caused solely by price chasing,
multi-level OFI measurement error, covariance inversion, or arbitrary asset
ordering.

## 2. Permutation-invariant observable law

Let `N = 30` and

```text
m = 1_N / sqrt(N).
```

For a leading flow-correlation share `s_q` and return-correlation share `s_r`,
define

```text
q1 = N s_q,       q0 = (N - q1) / (N - 1),
r1 = N s_r,       r0 = (N - r1) / (N - 1).
```

The maximum-entropy one-spike convention is

```text
Sigma_qq = q0 I + (q1 - q0) m m',
Sigma_rr = r0 I + (r1 - r0) m m'.                 (G2.1)
```

Both are correlation matrices. Every permutation leaves `m`, the covariances,
and every off-diagonal unchanged. At the confirmatory one-minute
Capponi--Cont point,

```text
s_q = 0.2827,  s_r = 0.32,  rho = 0.8726,
q1 = 8.481,    q0 = 0.7420344827586206,
r1 = 9.6,      r0 = 0.7034482758620689.
```

The implied mean pairwise flow correlation is

```text
(q1 - 1) / (N - 1) = 0.2579655172413793,
```

which reproduces the published `0.26` to its reported precision. The leading
share is the primary constraint; the source does not identify the residual
eigenstructure. Isotropy is a declared modeling convention, not an empirical
claim.

Hasbrouck--Seppi's 15-minute signed-flow values
`(s_q, s_r, rho) = (4.06/30, 6.32/30, 0.82)` define a separately labeled
historical comparator, not a second one-minute calibration.

## 3. Homogeneous structural sensitivity and feasibility

Let diagonal impact be `d = 0.29`, let `kappa = o/d`, and set

```text
kappa in [0.01, 0.0046 / 0.29],
Lambda = (d - o) I + N o m m'.
```

Thus the market and orthogonal eigenvalues are

```text
lambda1 = d + (N - 1) o,
lambda0 = d - o.                                  (G2.2)
```

Both `d = 0.29` and the ratio interval are structural sensitivities rather than
identified one-minute OFI coefficients. The 1% lower ratio is a preregistered
economic-materiality floor and conservative round-down from Capponi--Cont's
approximately 1.2% reduced-form mean ratio; it is not an empirical lower
confidence bound. The upper ratio is motivated by Benzaquen et al.'s normalized
homogeneous propagator. No point in the interval is called a one-minute
structural calibration.

Set `Var(f) = 1` and construct

```text
q = hq m f + v,           Var(v) = q0 I,
hq = sqrt(q1 - q0),
r = Lambda q + gamma m f + u.
```

The observed market-mode return--flow covariance is

```text
c1 = rho sqrt(r1 q1).
```

Writing the reduced return loading as `hr = lambda1 hq + gamma`, structural
shock orthogonality gives

```text
hr    = (c1 - lambda1 q0) / hq,
gamma = (c1 - lambda1 q1) / hq.                  (G2.3)
```

Set the orthogonal return--flow covariance to `lambda0 q0`. Independent return
shock variances are then

```text
sigma_u1^2 = r1 - hr^2 - lambda1^2 q0,
sigma_u0^2 = r0 - lambda0^2 q0.                  (G2.4)
```

The implementation must verify both are strictly positive before RNG access.
Across the 16 corners of the wider primary-plus-historical-comparator box

```text
s_q in {4.06/30, 0.2827},  s_r in {6.32/30, 0.32},
rho in {0.82, 0.8726},     o in {0.0029, 0.0046},
```

an independent recomputation found minimum market and orthogonal shock
variances `0.921906847090` and `0.629719273262`; the minimum `gamma` is
`0.867222458560`. The confirmatory point is therefore not perched on a
covariance-feasibility boundary. These wider-box values are nonconfirmatory
feasibility diagnostics, not a joint one-minute calibration.

## 4. A directly comparable noisy-factor coefficient

The observed control is an independent oracle-loading proxy

```text
z = f + e,   e independent of (f, u, v),
R = Var(f) / Var(z) = 1 / (1 + Var(e)).           (G2.5)
```

The confirmatory reliability is `R = 0.95`, so `Var(e) = 1/19`. The estimator
observes `q` and `z` but is not told `Var(e)` and performs no reliability
correction. Its coefficient on `q` in `r ~ [q, z]` targets `Lambda` in the same
original flow units.

After partialling out `z`, the flow-covariance eigenvalues are

```text
qtilde1 = q0 + (1 - R) (q1 - q0),
qtilde0 = q0.
```

The population controlled-regression eigenvalues are

```text
a1 = lambda1
   + (1 - R) hq gamma / (q0 + (1 - R) hq^2),
a0 = lambda0.                                      (G2.6)
```

Therefore every estimated off-diagonal is identical:

```text
ohat_R = o
       + (1 - R) (c1 - lambda1 q1)
         / {N [q0 + (1 - R)(q1 - q0)]}.           (G2.7)
```

At `R = 1`, the true factor is observed and Eq. (G2.7) recovers `o`. At every
registered `R < 1`, `c1 - lambda1 q1 > 0`, so the bias is positive.

The flow PC score's reliability under the one-spike decomposition is

```text
R_PC = 1 - q0 / q1 = 0.9125062512960004
```

at the one-minute point. Giving the opponent an independent, correctly loaded
95%-reliable proxy is therefore deliberately more favorable than that
fixture-implied decomposition.

## 5. Continuous population frontier

Let

```text
A = c1 - lambda1 q1,
H = q1 - q0,
M = lambda1 - lambda0 = N o.
```

The relative focal error is

```text
E(R) = (1 - R) A / {M [q0 + (1 - R) H]}.          (G2.8)
```

It decreases strictly in reliability. At the confirmatory one-minute point and
`R = 0.95`, write
`A = (c1 - d q1) - (N - 1)q1 o`. All other terms in Eq. (G2.8) are constant in
`o`, so

```text
d E / d o
= -(1 - R)(c1 - d q1)
  / {N o^2 [q0 + (1 - R)H]} < 0.
```

The least favorable endpoint is therefore the largest `o`. Full-precision
values are immutability-sealed in `configs/g2_population_targets.json` before
any registered stream is available. The independently reproducible semantic
seal recursively rounds every finite float to 12 decimal places before sorted,
compact JSON serialization with one trailing LF; the raw-file seal and semantic
seal have distinct roles.

As a nonconfirmatory robustness calculation, allowing the three historical
comparator endpoints and `kappa in [0.012, 0.0159]` gives a continuous error
range of `77.1526758197%` to `193.365071733%` at `R = 0.95`. The lowest proxy
reliability at which any point in that wider box reaches 50% is
`0.972062315648`. This comparator result cannot upgrade the historical data to
one-minute OFI calibration; it only shows that the confirmatory point is not a
single favorable asset labeling.

For any fixed cell, the reliability at which relative error reaches threshold
`theta = 0.5` is

```text
Rcrit = 1 - theta M q0 / (A - theta M H).          (G2.9)
```

The denominator must be checked positive. The reliability frontier, including
the recovery at `R = 1`, is reported rather than hidden.

## 6. Observable integrated-OFI population target

The published multi-level construction must be gate binding, not inferred from
an oracle result. For ten normalized levels,

```text
x_i,ell = q_i + eta_i,ell,
```

where level errors are independent across assets and levels and follow the
same within-date AR filter as the other components. A leading within-asset
share `s_L = 0.8906` implies

```text
rho_L = (10 s_L - 1) / 9 = 3953 / 4500,
Var(eta_i,ell) = 1 / rho_L - 1 = 547 / 3953.
```

The population L1-normalized first PC is the equal-weight mean

```text
w_i = q_i + n_i,
Var(n_i) = omega = (547 / 3953) / 10
         = 0.013837591702504428.                 (G2.10)
```

After partialling out `z`, put `x = 1 - R`. The measured-flow Schur covariance
has eigenvalues

```text
s0 = q0 + omega,
s1 = s0 + x H,
```

and the partial return--flow cross-covariance has eigenvalues

```text
k1 = x c1 + (1 - x) q0 lambda1,
k0 = q0 lambda0.
```

With the same condition cap and trace floor as the oracle ridge candidate,

```text
ell_cond = max(0, (s1 - K s0) / (K - 1)),
ell_floor = 10^-6 {s1 + (N - 1)s0} / N,
ell = max(ell_cond, ell_floor),

ohat_measured(R,o)
  = {k1 / (s1 + ell) - k0 / (s0 + ell)} / N.     (G2.11)
```

At `R = 0.95`, `s0 = 0.755872074461125`,
`s1 = 1.1428203503231944`, the condition number is
`1.5119229681000343`, and the condition cap is inactive. The floor is
`7.687703503231941e-7`, and

```text
ohat_measured(0.95,o)
  = 0.007955774783884128 + 0.6289974937449405 o.
```

Consequently its signed relative error decreases strictly in `o`:

```text
E_measured(o)
  = 0.007955774783884128 / o - 0.3710025062550595,
d E_measured / d o
  = -0.007955774783884128 / o^2 < 0.             (G2.12)
```

The least-favorable upper endpoint still has error
`1.3585137511110557`. At `R = 1`, exact factor observation does not undo OFI
measurement error; the recovery target is

```text
ohat_measured(1,o)
  = o q0 / {(q0 + omega)(1 + 10^-6)}
  = 0.9816922278202821 o.                         (G2.13)
```

Each measured candidate's 50%-materiality reliability is the unique root of
`(ohat_measured(R,o)-o)/o = 0.50` on `[0.95,1]`, found with the same frozen
binary64 bisection used for condition ridge. All 17 estimates, roots, floor
penalties, relative errors, and recovery targets are raw- and semantic-hash
sealed before execution.

## 7. Finite-sample confirmatory estimators

Three smooth candidates must pass at every structural grid point; no post-draw
model selector is used. The observable integrated-OFI condition ridge is the
primary opponent. The oracle-flow condition ridge shows that its failure is
not created by OFI measurement error. The pooled homogeneous OLS is told the
true symmetry and shows that failure is not created by a 30-dimensional
covariance inversion.

The full-flow candidate is condition-capped ridge, not unshrunk `Lambda`. It
uses one global weighted intercept, global centering over all date-bin rows
after date weights are applied, and no date or asset fixed effects. Per-date
cross-products for intercept, proxy, flows, and all responses are reaggregated
before centering. A nonfinite or nonpositive centered proxy variance fails the
cell. Partial out `z` by a Schur complement:

```text
S = S_qq - S_qz S_zz^-1 S_zq,
C = S_rq - S_rz S_zz^-1 S_zq.
```

Symmetrize `S` once, then obtain its eigenvalues with float64
`numpy.linalg.eigvalsh`. Let `smax` and `smin` be the extremes. For condition
cap `K = 10,000`, define

```text
lambda_cond = max(0, (smax - K smin) / (K - 1)),
lambda_floor = 10^-6 trace(S) / N,
lambda_ridge = max(lambda_cond, lambda_floor),
Lambdahat = C (S + lambda_ridge I)^-1.             (G2.14)
```

The implementation evaluates Eq. (G2.14) as
`numpy.linalg.solve((S+lambda_ridge I).T, C.T).T`; an explicit matrix inverse is
not licensed. A raised solve or nonfinite result fails the cell.

The proxy and intercept are unpenalized. The population unshrunk coefficient
in Eqs. (G2.6)--(G2.8) diagnoses moment-condition bias; the positive ridge floor
prevents the prohibited unshrunk matrix from being the reported estimator.
The population ridge target is also hash-sealed so shrinkage cannot be blamed
or tuned after the draw.

At the population law, `S`, its eigenvalues, and `lambda_ridge` do not depend on
`o`. Put `D1 = q0 + (1 - R)H` and `ell = lambda_ridge`. The ridge off-diagonal
has the affine form

```text
ohat_ridge = (C0 + C1 o) / N,
C0 = [(1-R)c1 + R d q0] / (D1 + ell)
   - d q0 / (q0 + ell),
C1 = R(N-1)q0 / (D1 + ell) + q0 / (q0 + ell).
```

At `R = 0.95`, the unregularized population condition number is
`D1 / q0 = 1.521469399136`, far below 10,000. The condition-cap branch is
therefore inactive and the trace floor is constant in `o`. Moreover,
`C0 / N = 0.007992633067236 > 0`, so the positive relative error is

```text
E_ridge(o) = C0 / (N o) + C1 / N - 1,
d E_ridge / d o = -C0 / (N o^2) < 0.
```

The upper endpoint is consequently least favorable for both ridge candidates
over the continuous structural interval; the 17-point grid remains the
finite-sample guard against implementation and sampling departures from that
population monotonicity.

The hostile efficiency candidate is told the true homogeneous structure. For
each date `d`, bin `t`, and asset `i`, stack

```text
r_dti = beta_0 + beta_d q_dti
      + beta_o sum_{j != i} q_dtj + alpha z_dt + error.         (G2.15)
```

There is one global intercept and no asset or date fixed effect. Given date
weights `m_d`, aggregate the per-date cross-products for
`[1, q_i, sum_other_q, z]` over all date-bin-asset rows. Partial the global
intercept by its Schur complement, which is exactly global weighted centering,
then solve the full-rank three-by-three slope system with `numpy.linalg.solve`.
Thus bootstrap centering changes with the date weights. No within-date,
within-asset, or unweighted preprocessing is permitted.

The slope matrix is symmetrized once as `(S + S') / 2`. Its singular values are
computed in binary64. The fit fails if the global weight mass is nonpositive,
the largest singular value is nonfinite, the smallest singular value is at most
`3 eps` times the largest, the two-norm condition number exceeds `10^12`, or
`numpy.linalg.solve` raises or returns a nonfinite value. These are numerical
failure conditions, not observations that may be dropped.

`beta_o` is directly one structural off-diagonal. Pooling uses every row rather
than selecting the focal row, while whole-date resampling preserves the strong
cross-sectional dependence. This model avoids the high-dimensional covariance
inversion entirely and is the strongest smooth linear opponent for the
registered homogeneous truth. In population its off-diagonal equals Eq.
(G2.7). Neither oracle candidate is exposed as an identified structural API.

## 8. Multi-level finite-sample estimation and paper-protocol reconstructions

Within every date and asset, the finite-sample observable candidate estimates
the first PC from the 330-by-10 centered level matrix. In float64 it forms the
symmetric covariance `X_c'X_c/330`, calls `numpy.linalg.eigh`, takes the largest
eigenpair, applies the frozen sign rule, divides its score by loading L1 norm,
and then fits Eq. (G2.14) using the estimated score in place of `q`. A nonfinite
or nonpositive covariance trace, nonfinite leading eigenpair, or top eigengap
at or below `10^-10` times the trace fails the cell. SVD or an unscaled scatter
matrix is not an equivalent licensed implementation. Date
bootstrap refits weighted global
centering and ridge from cached date statistics but does not recompute a date's
PCA. Its exact-procedure null-grid and power simulations are gate binding.

Every Schur covariance is symmetrized once. A nonfinite or nonpositive `smax`
fails. An eigenvalue in `[-100 eps max(1, abs(smax)), 0)` is accepted as
roundoff, but its raw value remains `smin` in the condition-penalty formula and
the once-symmetrized `S` remains the matrix in the regularized solve; no PSD
projection occurs. A more negative eigenvalue fails the fit. After choosing
`ell`, a nonfinite or nonpositive `smin+ell` fails, as does
`(smax+ell)/(smin+ell) > K(1+1000 eps)`. Nonfinite sufficient statistics,
eigenpairs, penalties, solutions, bootstrap estimates, intervals, or losses are
also failures. In validation, any such outcome invalidates the entire license;
it is never converted into a null-grid nonpass or removed from a denominator.
Every later rule labeled `fail_cell` or `fail_response_cell`, including a weak
finite eigengap or zero OOS SST, has the same global consequence. In research
it fails G2 and prevents success-last publication.

The six CCZ equations and their 30-minute/next-30-minute schedule are
reconstructed separately. Because the paper omits several numerical choices,
the code is labeled `paper_protocol_reconstruction`, not byte-exact author
code:

| ID | Feature map | Fit | Unpenalized | Penalized |
| --- | --- | --- | --- | --- |
| `PI_1` | own best-level OFI | per-response OLS | intercept, own flow | none |
| `PI_I` | own integrated top-ten OFI | per-response OLS | intercept, own flow | none |
| `CI_1` | all best-level OFIs | per-response LASSO | intercept | all 30 flows |
| `CI_I` | all integrated top-ten OFIs | per-response LASSO | intercept | all 30 flows |
| `PI_CC` | cross-sectional best-level PC1 plus own residual | per-response OLS | all columns | none |
| `CI_CC` | cross-sectional PC1 plus all residuals | per-response LASSO | intercept, PC1 | all 30 residuals |

Each date has eleven 30-minute blocks; blocks 0--9 fit and blocks 1--10 score.
Every model fits 30 separate response equations. LASSO uses five contiguous
six-bin validation folds with complement training and a common ratio-index
grid. The mathematical grid is

```text
rho_k = 10^(-4 k / 39),  k = 0, ..., 39.
```

That formula does not license runtime regeneration: scalar exponentiation and
`numpy.logspace` differ by several binary64 ULPs at some indices. The executable
grid is the ordered 40-literal `lambda_ratio_grid_values` vector in
`configs/g2.toml`, parsed directly as float64. Its little-endian float64 C-order
byte string has SHA256
`1da884c55b3f6e7bf79012973bddf092a92efb1ea098cd2717a804645a62c9a0`.
Any regenerated grid or digest mismatch fails the cell before fitting.

Each fold refits preprocessing on its 24 training bins, computes its own
response-specific `lambda_max`, and fits `rho_k lambda_max_fold`. For each ratio
index, accumulate float64 validation SSE in fold-index order 0 through 4 and
divide once by float64 30, the five six-bin validation folds, to define
`MSE_k`. After failing any nonfinite value, compute the minimum over all 40
`MSE_k` and select the smallest index (largest ratio) satisfying the inclusive
rule `MSE_k <= min_j MSE_j + float64(1e-12)`.
Outer preprocessing and `lambda_max_outer` are then refit on all 30 bins, and
the solver starts from zero once at `rho_selected lambda_max_outer`; no outer
path is run. A fold or outer fit with no penalized column or zero `lambda_max`
uses the zero penalized solution. Mixed zero and nonzero fold paths still score
the same 40 ratio indices.

“Best level” always means zero-based level index 0. Within each fold, construct
all PCA-derived features from training observations only. Center `y`, the named
factor, and every penalized column on training means. A nonfinite pre-FWL RMS
fails the cell. Drop and fix a penalized column to zero only if its finite
pre-FWL RMS `sqrt(sum(x_centered^2)/n)` is exactly zero; otherwise divide by
that RMS. If a named factor is present, use its unscaled centered vector `f_c`
and form

```text
y_res = y_c - f_c (f_c' y_c)/(f_c' f_c),
X_res = X_scaled - f_c (f_c' X_scaled)/(f_c' f_c).
```

A nonfinite or nonpositive `f_c'f_c` fails. After FWL, a nonfinite scaled-column
norm fails the cell; a finite column with `x_j'x_j/n <= 100 eps` is fixed to
zero. This order is frozen; scaling by the post-FWL norm is forbidden.

For objective `||y_res-X_res beta||^2/(2n)+lambda||beta||_1`, one ascending
coordinate update is

```text
rho_j = x_j' (y_res - X_res beta + x_j beta_j) / n,
den_j = x_j'x_j/n,
beta_j = soft_threshold(rho_j, lambda)/den_j.
```

Here `soft_threshold(a,l)=sign(a) max(abs(a)-l,0)` with `sign(0)=0`.

The descending fold path starts at zero and warm-starts by common ratio index;
the outer selected-lambda solve starts from zero. One iteration is a full
ascending-coordinate sweep. Convergence requires both maximum coefficient
update at most `10^-10 (1 + max(abs(beta)))` and maximum KKT violation at most
`10^-9`, with 10,000 sweeps a hard failure. With
`g=X_res'(X_res beta-y_res)/n`, KKT violation is
`abs(g_j+lambda sign(beta_j))` for nonzero coefficients and
`max(abs(g_j)-lambda,0)` for exact zeros.

Map penalized slopes back by dividing by their pre-FWL RMS. Recover the
unpenalized factor slope from
`f_c'(y_c-X_c beta_original)/(f_c'f_c)` and the intercept from
`ybar-Xbar beta_original-alpha fbar`; omit the factor term when absent. CV
predictions use these original-unit coefficients and only fold-training means,
PCA loadings, and transforms. OLS uses full-rank `lstsq` with
`rcond = machine_epsilon * max(shape)` and fails on rank loss.

Every within-asset level PC and cross-sectional PC is refit inside its CV fold
and on the outer training block. PCA uses float64 training-column centering,
covariance divisor `n`, symmetric `numpy.linalg.eigh` on the centered cross
product, the largest eigenpair, and a deterministic sign
whose largest-absolute loading is positive (feature-index tie broken low).
A nonfinite or nonpositive covariance trace, nonfinite leading eigenpair, or
top eigengap at or below `10^-10` times the covariance trace fails. Test
features use outer-training means, loadings, scales, and coefficients only.
OOS SST is measured around the outer-training response mean, never the test
mean.

Coefficient operators are averaged equally across the ten blocks within date
and then equally across dates. OOS loss pools next-block SSE and training-mean
SST. The date cache stores four direct maps, two purged CC maps, two full CC
response maps, the block-mean `P_perp`, and 360 response-level SSE/SST values.
The 499 whole-date bootstrap replicates reaggregate these date-level fields
under shared weights and do not refit the LASSO paths.

The published result reports all 7,200 entries of the first eight coefficient
maps, including explicit exact zeros imposed by a model's unavailable
directions, and 180 response-level OOS R-squared values. Every reported scalar
receives the named normal and basic date-bootstrap intervals. Mean `P_perp` and
the 360 SSE/SST cache entries are internal inputs used to reconstruct targets
and R-squared; they are not separately presented as inferential results.

Factor-residual models have a different legitimate estimand. For a training
loading matrix `W`, let `P_perp = I - W W'`. Their purged prediction operator is
compared with

```text
Lambda P_perp,
```

using a minimum-norm/prediction-equivalent residual representation. The full
response map `c W' + phi P_perp` is reported against `Lambda` only as a
descriptive alternative. No residual coefficient is relabeled as an estimate
of unrestricted `Lambda`.

Concretely, in every outer block `PI_CC` embeds its 30 own-residual slopes in
diagonal matrix `D` and forms `D P_perp`; `CI_CC` forms `Phi P_perp` from its
30-by-30 residual-slope matrix. Their factor coefficients form column `c`, so
the full response maps are `c W' + D P_perp` and `c W' + Phi P_perp`. These
products and `P_perp` are formed **before** block averaging. Under date weights,
the fair target is reconstructed as `Lambda` times the correspondingly
weighted mean projection. An average `c` is never multiplied by an average
`W`; that invalid shortcut is unrecoverable when loadings vary.

`CI_I` is the binding published direct-flow veto because it is the only CCZ
specification with both integrated top-ten OFI and explicit off-diagonal
coefficients. At the primary observable calibration and `o = 0.0046`, map its
coefficients back to original integrated-OFI units, average each 30-by-30
coefficient matrix equally over ten blocks and 252 dates, and evaluate the
predeclared `(0,1)` element with Eq. (G2.16) and the same 499 date weights. G2
cannot pass unless this event and all 51 smooth candidate/grid events pass.
The other five published-protocol fits remain mandatory diagnostics and cannot
rescue a failed binding event.

Before that research fit, the frozen recovery panel uses the same
one-factor/equicorrelated `q` law from Eq. (G2.1) and Section 3's construction,
including unit factor variance and independent isotropic flow innovation, but
sets `Gamma = 0`. Thus order flow
retains the registered cross-sectional collinearity while the price equation is
unconfounded. It sets homogeneous `Lambda` to diagonal `0.29` and every
off-diagonal `0.0046`. Every other upper-endpoint input is held fixed: the
symmetric return-noise market/orthogonal variances are
`2.082896495599317`/`0.6430072224124138`, each level is
`q + sqrt(547/3953) eta`, and the AR(1) plus date-reset laws are unchanged.
Only `Gamma` moves from `1.5395102172741495` to zero. The recovery realization
uses its own disjoint phase-25/scenario-4 addressed normals and never reads the
phase-30 research stream. The 30
diagonal coefficients and the predeclared `(0,1)` cross coefficient must contain
`0.29` and `0.0046`, respectively, in the frozen 31-component Bonferroni
date-bootstrap-normal intervals. Every point estimate must also have absolute
error strictly below 50% of its own truth, and the focal Eq. (G2.16) material-bias
event must be false. A LASSO that erases small cross coefficients therefore
cannot earn the recovery license. This is a one-panel recovery/no-strawman
check, not a 100-panel size or power claim. No easier zero-cross, exact-flow,
independent-flow, isotropic-noise, or longer-window recovery law is allowed.

## 9. Dependence, bootstrap, and gate statistic

For the finite-sample stress design, `f`, `v`, `u`, proxy error, and level errors
each follow the same stationary Gaussian AR(1) recursion with `phi = 0.60`.
Innovations are scaled by `sqrt(1 - phi^2)`. Every date starts from an
independent stationary draw; no innovation crosses a date boundary. Applying
the common filter preserves the contemporaneous covariances above. `phi = 0`
is a diagnostic, not the confirmatory calibration.

The common-random-number coupling is part of the estimator license, not an
implementation detail. For each component key, draw the entire configured
float64 C-order standard-normal array with exactly one
`generator.standard_normal(size=tuple(configured_shape), dtype=np.float64)`
call, then filter every trailing component independently along time. The return
must already be C-contiguous; a custom Gaussian transform, `Generator.normal`,
reshaping, or sequential generator reuse changes the registered random variable
and is forbidden:

```text
g_0 = xi_0,
g_t = phi g_{t-1} + sqrt(1-phi^2) xi_t.
```

Only after filtering, with `m = 1/sqrt(N)`, form

```text
v = sqrt(q0) g_v,
q = hq f m + v,
u = sqrt(sigma_u0^2) g_u
  + {sqrt(sigma_u1^2)-sqrt(sigma_u0^2)} (g_u m) m,
r = q Lambda' + gamma f m + u,
z = f + sqrt(1/R - 1) e,
x_i,ell = q_i + sqrt(547/3953) eta_i,ell.          (G2.15a)
```

This is the symmetric market/orthogonal square root. Cholesky factors, random
rotations, eigenvector-dependent roots, filtering after the modal map, and
sequential reuse of one generator are forbidden. Within one fixed active phase
and scenario, all structural cells, reliabilities, candidates, and the six
paper estimator views reuse the same addressed filtered base normals; only the
sealed deterministic coefficients change. The recovery view is a
distribution-matched upper-endpoint counterfactual with identical
`q`, measured-level, modal-`u`, and `Lambda` maps; only `Gamma` is set to zero.
Its phase-25/scenario-4 base normals are disjoint from the phase-30 research
realization, preserving the sealed research draw.

The active phase/scenario pairs are exactly resource smooth `10/0`, resource
paper `10/1`, size `20/0`, power `21/0`, date frontier `22/2`, smooth recovery
`23/0`, IID diagnostic `24/0`, paper recovery `25/4`, and research `30/0`.
Reliability-frontier `22/3` is metadata-only and deterministically reuses
`21/0`; it never constructs a generator. DGP parent-phase and parent-scenario
slots are zero sentinels. Only phase-40 bootstrap keys populate those slots
with the exact active parent pair.

Only `(0, 1)` is serialized as the focal pair, but permutation invariance makes
it equal to every population off-diagonal. For estimate `Lhat_01`, truth `o`,
and whole-date bootstrap standard error `SE_boot`, passage requires the
strictly stronger event

```text
abs(Lhat_01 - o) - 0.50 abs(o) > 3 SE_boot.        (G2.16)
```

Thus the materiality margin itself, not merely error relative to zero, must
clear three bootstrap standard errors. For each bootstrap key, construct
`pvals=np.full(n_dates, 1.0/float(n_dates), dtype=np.float64)`, call
`generator.multinomial(n=n_dates, pvals=pvals, size=None)` exactly once, and
cast the counts to float64 weights. These weights apply to the original ordered
dates, preserve all within-date bins and assets, and refit centering, the Schur
complement, and ridge. With 499
replicates, the final checkpoint batch contains 24 replicates. The same date
weights are applied to all smooth candidates and the cached `CI_I` veto. If the
499 bootstrap estimates are `theta_b*`, then

```text
SE_boot = sd(theta_1*, ..., theta_499*, ddof=1),
I_normal = thetahat +/- Phi^-1(0.975) SE_boot,
I_basic  = [2 thetahat - Q_0.975, 2 thetahat - Q_0.025].
```

`Phi^-1(0.975) = 1.959963984540054`; both quantiles use Hyndman--Fan type 7
(`numpy` method `linear`). No unsupported studentized interval is claimed.

Before the frozen research draw, the exact smooth rule is licensed by 100
superpanels. For the homogeneous candidate, Eq. (G2.9) supplies the
cell-specific critical reliability. For each ridge candidate, its exact
trace-floor rule is retained and a unique root on `[0.95, 1]` solves

```text
(ohat_ridge(R, o) - o) / o = 0.50.
```

Each ridge root uses binary64 bisection on the closed bracket `[0.95, 1]` until
its width is at most `10^-14`, then takes the midpoint; this reproduces every
stored root after frozen 12-decimal semantic rounding. All three
candidate-specific roots are semantic-hash-sealed for all 17 points.

A null-grid superpanel does not assume the population boundary is also
finite-sample least favorable. For candidate `c` and structural cell `j`, put

```text
tau_crit,cj = sqrt(1 / Rcrit,cj - 1),
tau_cjk = (k / 8) tau_crit,cj,  k = 0, ..., 8,
R_cjk = 1 / (1 + tau_cjk^2).
```

It evaluates all `3 * 17 * 9 = 459` strict gate events and records one family
indicator: did **any** event pass? The one-sided 95% Clopper--Pearson upper
bound on that union probability must be at most 5%. This is explicitly a
frozen nine-node null-grid calibration, not a proof of continuum-uniform size;
the frozen global maximum proxy-noise-amplitude gap is computed directly as
`tau_crit` times the largest adjacent configured fraction difference—not by
subtracting rounded binary64 nodes—and equals `0.015038828627620739`. The
maximum adjacent reliability gap, computed from the generated reliability
nodes, is
`0.003307437435413063`, and both global and cellwise gaps are reported with the
result. `R = 1` also supplies the
51-component recovery diagnostic: homogeneous OLS targets truth, oracle ridge
targets its sealed floor-shrunken truth, and observable ridge targets Eq.
(G2.13).

A power superpanel runs all 51 smooth candidate/grid components at the actual
`R = 0.95` alternative and records one gate indicator: did **every** component
pass? The one-sided 95% Wilson lower bound on this intersection probability
must be at least 80%. With 100 superpanels the family size rule permits at most
one union success and the joint power rule requires at least 87 intersection
successes. Componentwise rates and intervals are descriptive only.
Each of the 459 null-component rates receives the same one-sided 95%
Clopper--Pearson upper endpoint formula as the family union, and each of the 51
power-component rates receives the same one-sided 95% Wilson lower endpoint
formula as the family intersection. These 510 marginal intervals are
unadjusted, descriptive, and non-gating; they cannot replace either family
decision.

The reduced frontiers also report passage probabilities rather than naked
counts. At the upper structural endpoint, the three candidates at 48 and 96
dates produce six rates, and the three candidates at each of reliabilities
0.96, 0.97, 0.98, and 0.99 produce twelve additional rates. Each rate uses its
100 superpanel indicators and an unadjusted, one-sided 95% Wilson lower
endpoint. Reliability 0.95 is already represented among the 51 power marginals;
252 dates is the main power operating point; reliability one is the separate
analytic-target recovery. These 18 frontier intervals are descriptive and
non-gating, but mandatory.

The research gate itself is an intersection-union test, but 51 marginal Monte
Carlo intervals would not jointly license its family behavior. The superpanel
union/intersection indicators avoid that overclaim without a post-hoc
multiplicity choice. Validation uses the same estimator, 499-replicate
bootstrap, AR(1), date count, and decision rule. Failure cannot be retried under
a new validation seed. The computationally much heavier `CI_I` protocol veto
is not smuggled into this smooth-family Monte Carlo claim: it receives a
separate full-`N`, full-`T` no-confounding recovery panel, then its sole frozen
research output is judged by the named date bootstrap in Eq. (G2.16).

For a size-superpanel union count `k` out of `n = 100`, the one-sided 95%
Clopper--Pearson upper endpoint is

```text
Beta^-1(0.95; k + 1, n - k),
```

with value one when `k = n`. For a power-superpanel intersection count, the
one-sided Wilson lower endpoint uses `p = k/n`, `z = Phi^-1(0.95)`, and

```text
{p + z^2/(2n) - z sqrt[p(1-p)/n + z^2/(4n^2)]} / {1 + z^2/n}.
```

The frozen integer rules are `k_size <= 1` and `k_power >= 87`; the reported
endpoints at those boundaries are `0.046559811454` and `0.804806264079`.

## 10. Decision scope and the null

A positive G2 result supports only this claim:

> Conditional on `d = 0.29` and the registered off-diagonal structural
> sensitivity interval, a permutation-invariant one-factor model matching the
> registered one-minute observable commonality exhibits material confounding
> bias in the homogeneous off-diagonal for an integrated top-ten-OFI
> proxy-control ridge, two stronger oracle-flow projections, and the frozen
> `CI_I` published-protocol reconstruction at the upper structural endpoint.

It does not establish the real market's `Lambda`, latent decomposition, or
proxy reliability.

A negative result at `R = 0.95` is not a premise-killing null because weaker
source-compatible proxies could still fail. The premise may be declared dead
only if a separately preregistered sharp upper bound over all source-compatible
latent decompositions and reliabilities is below 50% with adequate power.
Otherwise the honest outcome is **unadjudicated for insufficient calibration**,
and G2 does not pass.
