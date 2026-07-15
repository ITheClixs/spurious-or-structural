# G2 smooth estimators: sufficient statistics and numerical path

Written before implementation of the smooth estimators and before any G2
resource, validation, or research stream is available.  This document refines
the binary64 path of the already sealed S0004 estimators; it does not change an
estimand, threshold, seed, population target, or stochastic law.

## 1. Target and stop condition

The implementation slice must provide four deterministic kernels:

1. within-date, within-asset integrated-OFI PCA with the registered sign and
   eigengap rules;
2. date-level polynomial sufficient statistics shared by every reliability and
   smooth candidate;
3. oracle and observable global-intercept, proxy-partialled, condition-capped
   ridge fits; and
4. the globally centered pooled homogeneous OLS fit derived from the same
   moments without allocating stacked asset rows.

The slice stops after analytic fixtures and a test-only end-to-end smoke are
green locally and on hosted CI.  It creates no production RNG authority,
checkpoint runner, recovery experiment, resource benchmark, validation
command, or research command.

## 2. Alternatives considered

The chosen design stores one polynomial moment basis per date.  Two simpler
alternatives are rejected:

- Candidate-specific moments would repeat PCA and cross-product work for
  reliabilities that are polynomial transforms of the same `f` and proxy-noise
  columns.  They also contradict the shared work unit in the sealed compute
  plan.
- Refitting from raw rows would make bootstrap work depend on retained
  simulated panels, violate the streaming checkpoint design, and allocate the
  pooled asset rows explicitly.

One shared moment basis is both the lowest-memory licensed design and the one
that exposes every centering operation to deterministic tests.

## 3. Date moments

For date `d`, let `T=330`, `N=30`, and define

```text
X0_d = [1, f, e, Q_1..Q_N, W_1..W_N],
Y_d  = [r_1..r_N].
```

`e` is the filtered unit-variance proxy-noise component, `Q` is oracle flow,
and `W` is the cached integrated-OFI score.  Store raw, not date-centered,
moments

```text
G_d = X0_d' X0_d,       shape 63 x 63,
H_d = X0_d' Y_d,        shape 63 x 30,
J_d = Y_d' Y_d,         shape 30 x 30.
```

Raw moments preserve between-date variation.  Centering any date before the
bootstrap weights are known would change the registered global-intercept
estimator.

Symmetric matrices use the row-major upper triangle returned by
`numpy.triu_indices(n)`.  Thus the exact stored sizes are 2,016, 1,890, and 465
float64 values per date.  Panel arrays are C-contiguous and date-major in
ascending `date_index` order.  `H_d` is flattened in C order only for weighted
aggregation and is reshaped back to `(63,30)` without changing element order.

For a date-weight vector `m`, aggregate each date-major two-dimensional panel
with exactly one `numpy.matmul(m, panel)` call.  Point estimates use
`numpy.ones(D, dtype=numpy.float64)`.  Bootstrap weights are the already frozen
nonnegative integer multinomial counts cast to float64.  The estimator-side
guard requires finite C-contiguous float64 weights, exact integer values, and
an exact sum of `D`; zero-count dates remain in their original positions.

## 4. Covariance normalization and global centering

Let

```text
G = sum_d m_d G_d,   H = sum_d m_d H_d,   J = sum_d m_d J_d,
n = G[0,0].
```

The registered bootstrap counts always sum to the number of dates, so `n` is
the weighted number of date-bin rows.  First take the intercept Schur
complement on the aggregated raw cross-products, then divide by `n`.  In other
words, for any two non-intercept blocks `a,b`,

```text
Cov_m(a,b) = (G_ab - G_a0 G_00^-1 G_0b) / n.
```

This selects covariance rather than scatter units.  It is not an arbitrary
scale choice: the sealed target file reports the oracle and observable ridge
penalties as `7.549327586206895e-7` and
`7.687703503231941e-7`, respectively, which are the population covariance-unit
trace floors.  A raw-scatter calculation gives the same coefficient in exact
arithmetic because both ridge penalties are homogeneous of degree one, but it
would not reproduce those sealed diagnostics or the same binary64 path.

No within-date, date-fixed-effect, asset-fixed-effect, or pre-weight centering
is licensed.

## 5. Reliability polynomial and ridge moments

For reliability `R in [0.95,1]`, define

```text
tau = sqrt(1/R - 1),
z   = f + tau e.
```

Let `I` select either `Q` (oracle ridge) or `W` (observable ridge) in `X0`.
The required raw blocks are extracted from `G,H` without reconstructing rows:

```text
s_z  = G_01 + tau G_02,
s_F  = G_I0,
s_Y  = H_0:,
g_zz = G_11 + 2 tau G_12 + tau^2 G_22,
g_Fz = G_I1 + tau G_I2,
g_FF = G_II,
g_zY = H_1: + tau H_2:,
g_FY = H_I:.
```

After global intercept centering and division by `n`, orient the moments as

```text
S_zz : scalar,
S_Fz : N x 1,
C_Yz : N x 1,
S_FF : N x N,
C_YF : N x N  (response by flow).
```

Partial the unpenalized proxy:

```text
S = S_FF - S_Fz S_Fz' / S_zz,
C = C_YF - C_Yz S_Fz' / S_zz.
```

`n` and `S_zz` must be finite and strictly positive.  Nonfinite input or output
fails the fit; nothing is dropped or regularized silently.

## 6. Condition-capped ridge

Symmetrize `S` exactly once:

```text
Ss = 0.5 * (S + S.T).
```

Use float64 `numpy.linalg.eigvalsh(Ss)`.  For `K=10,000`, floor ratio
`rho=1e-6`, and machine epsilon `eps`, define

```text
ell_cond  = max(0, (smax - K*smin)/(K - 1)),
ell_floor = rho * trace(Ss)/N,
ell       = max(ell_cond, ell_floor).
```

Fail a nonfinite or nonpositive `smax`.  Values of `smin` in the closed interval

```text
[-100 eps max(1,abs(smax)), 0]
```

are retained as raw roundoff; more negative values fail.  No eigenvector
reconstruction, clipping, or PSD projection occurs.  Require finite positive
`smin+ell` and

```text
(smax+ell)/(smin+ell) <= K*(1+1000 eps).
```

Evaluate the coefficient matrix only as

```text
numpy.linalg.solve((Ss + ell I).T, C.T).T.
```

The result orientation is response asset by flow asset.  Diagnostics retain
`smin`, `smax`, both candidate penalties, the chosen penalty, and the realized
post-ridge condition ratio.

## 7. Observable PCA

For one date and asset, let `L` be the `T x 10` level matrix.  In float64:

```text
Lc = L - mean(L, axis=0),
V  = Lc.T @ Lc / float(T),
(eigenvalues, eigenvectors) = numpy.linalg.eigh(V).
```

Use the NumPy default lower-triangle `UPLO='L'` path and do not symmetrize `V`
again.  Fail a nonfinite input, nonfinite or nonpositive trace, nonfinite top
two eigenvalues or leading eigenvector, or

```text
eigenvalues[-1] - eigenvalues[-2] <= 1e-10 * trace(V).
```

Let `k = numpy.argmax(abs(v))`; NumPy's first maximum implements the
smallest-level-index tie rule.  If `v[k] < 0`, orient `v = -v`.  Then compute,
in this order,

```text
score = (Lc @ v) / sum(abs(v)).
```

Do not force the finite-sample score mean to zero after the matrix product and
do not recompute PCA under bootstrap weights.  Store score, loading, trace,
leading eigenvalue, and eigengap as read-only float64 diagnostics.

## 8. Pooled homogeneous moments

Use oracle `Q`.  Let `A=Q'Q`, `D=Q'Y`, `v=Q'z`, `e=1_N`, and let `z2=z'z`.
All are extracted from the aggregated polynomial moments.  Across the implicit
`n*N` bin-asset rows, the predictor order is
`[own_q, sum_other_q, z]`.  Its raw sums are

```text
p = [e'Q'1,
     (N-1)e'Q'1,
     N z'1].
```

The raw slope Gram is

```text
K_11 = trace(A),
K_12 = e'Ae - trace(A),
K_22 = (N-2)e'Ae + trace(A),
K_13 = e'v,
K_23 = (N-1)e'v,
K_33 = N z2.
```

For response vector formed by stacking `Y` over assets, let

```text
k_1 = trace(D),
k_2 = e'De - trace(D),
k_3 = (z'Y)e,
s_y = 1'Y e.
```

With pooled mass `M=N*n`, globally center and covariance-normalize:

```text
Sp = (K - p p'/M) / M,
cp = (k - p s_y/M) / M.
```

Symmetrize `Sp` once.  Compute singular values only with
`numpy.linalg.svd(Sp, compute_uv=False)`.  Fail nonfinite or nonpositive mass,
nonfinite singular values, `smin <= 3 eps smax`, or `smax/smin > 1e12`.
Solve only with `numpy.linalg.solve(Sp, cp)` and fail a raised solve or
nonfinite result.  The slope order is `(beta_d,beta_o,alpha)` and `beta_o` is
one off-diagonal, not a cross-sum divided by `N-1`.

## 9. Typed contract and public boundary

The existing sealed config already contains the estimator thresholds, but the
typed `G2Contract` did not project them.  The implementation must extend that
typed projection and exact validator for:

- ridge condition cap and trace-floor ratio;
- PCA eigengap-to-trace ratio;
- pooled rank multiplier and condition cap; and
- the two ridge roundoff multipliers.

Text-encoded numerical rules are first checked against their exact sealed
strings; their numeric projections are then fixed.  Estimator code receives
these fields from the validated contract rather than hiding them as unrelated
module state.

Low-level linear-algebra helpers remain dimension-generic so deterministic
analytic fixtures can expose orientation and boundary errors.  The
contract-bound date/panel builders separately require the sealed `T=330`,
`N=30`, `L=10`, finite float64 inputs and ascending provenance.

## 10. Predictions written before implementation

The deterministic tests must establish all of the following before any
test-seed recovery is interpreted:

1. upper-triangle packing round-trips exactly and rejects malformed data;
2. date moments plus global centering match explicitly stacked rows, while
   within-date centering does not;
3. the ridge response-by-flow orientation recovers a known nonsymmetric matrix
   divided by `1+1e-6` when the floor binds;
4. the condition penalty lands at the cap and the positive floor prevents an
   unshrunk result even when the unregularized condition number is acceptable;
5. the tolerated negative-eigenvalue boundary is inclusive and one ULP beyond
   it fails;
6. PCA centering, first-index sign tie, L1 normalization, row permutation, and
   additive-level invariance match analytic fixtures;
7. zero trace, tied top eigenvalues, constant proxy, nonfinite values, singular
   pooled slopes, and over-cap condition numbers all fail closed;
8. algebraically derived pooled moments match explicit stacked rows and recover
   known `(beta_d,beta_o,alpha)` without dividing `beta_o`.

A 252-date test-seed recovery belongs to the later recovery/checkpoint slice
and is not authorized by this document.  Its exact sample, numerical tolerance,
and pass prediction must be registered before that later stochastic call.  This
estimator-core slice stops at the eight deterministic claims above plus
test-only end-to-end smoke coverage that does not evaluate a population target.
