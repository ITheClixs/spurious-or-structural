# G1 pre-run prediction

Registered on 2026-07-15 after the symbolic derivation and before any G1
simulation implementation or simulation draw. The numerical calculations in
this document are deterministic evaluations of the derived population
covariances, not fitted or simulated results.

## Question and frozen gate statistic

The experiment asks whether a streamed finite sample from the stated
simultaneous system converges to both derived population regression matrices.
For analytic targets $A^*$ (uncontrolled OLS) and $C^*$ (OLS controlling
for $\widehat f=f+\epsilon$), define

$$
D_{\mathrm{OLS}}=\max_{ij}
\frac{|\widehat A_{ij}-A^*_{ij}|}{|A^*_{ij}|},
\qquad
D_{\mathrm{proxy}}=\max_{ij}
\frac{|\widehat C_{ij}-C^*_{ij}|}{|C^*_{ij}|},
$$

$$
D_{\mathrm{gate}}=\max(D_{\mathrm{OLS}},D_{\mathrm{proxy}}).
$$

G1 passes this numerical criterion if and only if
$D_{\mathrm{gate}}<10^{-3}$. There is no denominator floor, element
exclusion, seed retry, or average-error substitute. Any such change is a new
simulation specification and must be logged before it runs.

## Frozen data-generating process

`configs/g1.toml` is authoritative. It sets $N=30$, $K=3$, and
$T=10{,}000{,}000$ IID observations. Indices below are one-based. Design
constants are fixed inputs and therefore have no sampling interval.

$$
\Lambda_{ij}=0.75+0.08\frac{i}{31}+0.06\frac{j}{31}
+0.02\mathbf 1\{i=j\},
$$

$$
B_{ij}=0.00012+0.00004\frac{i}{31}+0.00003\frac{j}{31}
+0.012\mathbf 1\{i=j\},
$$

$$
\Gamma_{ik}=0.30+0.06\sin(ik/7)+0.02k,
$$

$$
(\Delta_f)_{ik}=0.45+0.08\cos(i(k+1)/9)+0.03k.
$$

The four shocks are mutually independent, centered Gaussian vectors. The two
factor covariance matrices are written explicitly in the config. The
idiosyncratic covariances are Toeplitz:

$$
(\Sigma_u)_{ij}=0.05(0.25)^{|i-j|},
\qquad
(\Sigma_v)_{ij}=0.30(0.15)^{|i-j|}.
$$

This fixture is intentionally the declared operating dimension, not a scalar
or toy matrix. Its deterministic diagnostics are

- $\rho(B\Lambda)=0.4104240454$;
- $\kappa_2(I-B\Lambda)=1.6961688362$;
- $\kappa_2(\Sigma_{qq})=348.0879052636$;
- $\kappa_2(\Sigma_{qq\mid\widehat f})=92.4159904675$; and
- $\kappa_2(\Sigma_{[q,\widehat f]})=353.1305179714$.

These are analytic fixture properties, not uncertain estimates. The
conditioning is deliberate: a validator that works only for nearly orthogonal
flow is not a useful check of this problem.

## Quantitative predictions fixed before simulation

The uncontrolled target spans $[0.7724315313,0.9138344678]$, and the
proxy-controlled target spans $[0.7719001593,0.9201821590]$. The smallest
absolute target among all 1,800 coefficients is $0.7719001593$, so the hard
relative-error statistic is not stabilized by an arbitrary epsilon.

The exact target matrices are frozen by canonical JSON hashes. Each element is
rounded to ten decimal places, matrices are row-major, JSON uses sorted keys and
compact separators, and no trailing newline is hashed:

- uncontrolled target:
  `e20709d129b00561cdefc69bb361cd35550665125ed56604456344d2ea6cd854`;
- proxy-controlled target:
  `c4dfb1bc3aca138cb631ba2ff90e129f249c6aa2b15aba3f57cc7f0f0c466995`;
- combined object with keys `controlled` and `ols`:
  `80e6026821d67708587eb3abe606c05a7f58c5e4499430e6db72ae6d36faee1d`.

Two algebraically independent evaluations—the reduced-form covariance path and
the primitive-only bias formulas—agree to maximum absolute discrepancies of
$1.72\times10^{-13}$ for uncontrolled OLS and
$4.45\times10^{-16}$ for proxy-controlled OLS. Those calculations predict
that the implementation must reject the following mutations:

| Mutation | Maximum relative target error, uncontrolled | Maximum relative target error, proxy-controlled |
| --- | ---: | ---: |
| Omit simultaneity numerator | 0.0023259 | 0.0023343 |
| Omit confounding numerator | 0.0320631 | 0.0283317 |
| Compare row-regression output without transposing | 0.0321191 | 0.0301025 |
| Replace matrix proxy reliability by rowwise scalar attenuation | not applicable | 0.0076652 |

The mutation values are deterministic formula diagnostics, so sampling
intervals are not applicable. Every mutation is separated from the gate
tolerance before a random number is drawn.

Under the Gaussian fixture, the largest analytic coefficient standard error at
$T=10^7$, divided by its absolute target, is predicted to be
$1.7930730\times10^{-4}$. Thus the gate boundary is 5.577 worst-case
standard errors from the target. This is a power calculation for the numerical
recovery check, not evidence that the formulas have passed.

## Sampling, accumulation, and resumption contract

The run consists of 100 immutable shards of 100,000 observations. NumPy
`PCG64DXSM` streams are keyed by
`(master_seed, shard_index, component_id)` through `SeedSequence`; component
IDs are fixed as `f=0`, `u=1`, `v=2`, and `epsilon=3`. A mutable RNG state is
never used as the resume boundary. All arithmetic is `float64`.

Each shard stores only the count, mean, and centered scatter of the combined
vector ordered as `[q(30), r(30), fhat(3)]`. Global statistics are merged in
shard-index order with the Chan--Golub--LeVeque parallel mean/scatter identity.
Summing independently centered shard scatters without the between-shard term is
a known-wrong implementation and must fail a regression test.

Every shard is published atomically and records its config hash, implementation
Git SHA, NumPy version, RNG key, row count, elapsed time, peak RSS, and payload
SHA256. Resume skips only a checksum-valid shard with matching configuration,
code SHA, package version, and RNG key. A mismatch refuses reuse. Final
aggregation always rereads shards 0 through 99 in order.

The peak live-array forecast is below 350 MB; the phase abort is 1.5 GB and the
project-wide absolute abort is 3.7 GB. Checkpoint payload is forecast below
4 MB total. The existing three-hour expected and eight-hour hard wall budgets
remain binding. A distinct-seed one-shard timing run may measure throughput and
RSS but must suppress coefficient output. Approaching eight minutes for one
shard is a design failure; at 6.4 hours the runner must recompute its completion
forecast and stop cleanly if the eight-hour bound would be crossed.

## Intervals and reporting

Both regressions include an intercept through globally centered sufficient
statistics. Because the frozen DGP is jointly Gaussian, each population linear
projection residual is independent of its regressors. The named interval method
is therefore the classical homoskedastic Student-$t$ interval, Bonferroni
adjusted to 95% family-wise coverage across all 1,800 reported coefficients.
Proxy-regression variances use the full `[q, fhat]` design inverse before the
`q` block is extracted.

The predicted Bonferroni critical value is approximately 4.191, giving a
worst-case relative half-width of approximately
$7.515\times10^{-4}$. The exact critical value, every coefficient interval,
and signed relative-error interval will be generated from the locked run.
Target inclusion in the simultaneous intervals is a secondary integrity check;
it does not replace the hard $10^{-3}$ discrepancy criterion.

## Failure interpretation fixed before the run

- A target-hash mismatch stops before simulation and means the formula or
  fixture implementation drifted from this preregistration.
- A structural-equation residual above floating-point tolerance stops the shard
  and means the reduced-form generator is wrong.
- A gate discrepancy at or above $10^{-3}$ is G1 attempt 1 failed. The seed,
  sample size, target, and tolerance remain frozen while the mismatch is
  diagnosed.
- A runtime or RSS stop is a compute-design failure and is recorded in
  `DECISIONS.md`; it is not converted into a smaller silent run.
- Gaussian G1 intervals validate this controlled simulation only. They are not
  licensed for the dependent empirical tape in later gates.

## Pre-draw implementation note: stronger resume provenance

This note was appended after implementation review and before either registered
seed was drawn. It does not change the fixture, estimator, target hashes,
sample size, interval, discrepancy metric, threshold, or attempt count.

The original contract above names an implementation Git SHA as the checkpoint
code identity. Review exposed two narrower failure modes: documentation-only
commits would invalidate identical numerical code, while a restarted process
could discard prior checkpoint timing. The implementation therefore records
the clean Git commit separately for provenance and binds reuse to a SHA256 of
the tracked execution-input blobs and paths. It additionally requires a
single-thread BLAS environment, fingerprints the numerical runtime, reloads
and validates elapsed/RSS telemetry, applies the eight-minute shard stop to
both new and reused shards, and accumulates generated-shard time across
resumptions for the eight-hour stop and 6.4-hour completion forecast. These are
anti-laundering controls on the already registered run, not new statistical
choices.
