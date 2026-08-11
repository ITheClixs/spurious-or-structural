# Spurious or Structural?

## Probability Limits and a Registered Falsification Design for Cross-Asset Price Impact

**Mehmet Demir Güven**

Department of Computer Science, ETH Zürich

*Sole-author independent research. The affiliation identifies the author's
student status only; ETH Zürich did not sponsor, fund, or endorse this work.*

**Preprint · Version 0.1 · 6 August 2026 · [CC BY 4.0](LICENSE-PREPRINT.md)**

[![CI](https://github.com/ITheClixs/spurious-or-structural/actions/workflows/ci.yml/badge.svg)](https://github.com/ITheClixs/spurious-or-structural/actions/workflows/ci.yml)

> **Evidence status — 6 August 2026.** This repository currently supports a
> pre-results manuscript. G0 and G1 have passed. G2 is open: the scientific
> design and document authority are registered, but executable resource
> admission is incomplete. No registered G2 resource benchmark, validation
> panel, research draw, external market data, training sample, holdout, or
> economic evaluation has been accessed.

The current preprint is available as a
[PDF](output/pdf/xid_pre_results_manuscript.pdf), with
[LaTeX source](docs/pre_results/xid_pre_results_manuscript.tex) and a scoped
[license notice](LICENSE-PREPRINT.md).

## Abstract

Cross-asset return-on-flow regressions are often interpreted as estimates of a
structural price-impact matrix. That interpretation is not automatic. Latent
common factors and same-bin feedback can generate off-diagonal population
coefficients even when the corresponding structural entries are zero. This
project derives the probability limits of ordinary least squares and of least
squares with a noisy factor proxy in a simultaneous multi-asset system. The
decomposition separates latent-factor confounding from simultaneity and states
precisely what a noisy control can and cannot remove.

The formulas were evaluated in a preregistered known-truth experiment with
30 assets, three factors, and ten million observations. The sole frozen draw
passed a strict maximum elementwise relative-discrepancy threshold of
\(10^{-3}\): the uncontrolled and proxy-controlled discrepancies were
\(5.6395\times10^{-4}\) and \(5.1237\times10^{-4}\), respectively. All 1,800
targets lay inside named 95% family-wise Bonferroni intervals. This verifies the
algebra and numerical implementation under the stated simulation law; it does
not identify real-market impact.

G2 is a registered, source-constrained premise test that must pass before market
data is used. It combines an observable integrated-order-flow opponent, two
oracle-flow no-strawman checks, six frozen published-protocol reconstructions,
whole-date bootstrap inference, and explicit size, power, resource, and failure
rules. Its stochastic and empirical outcomes are not reported because the
relevant gates are not open.

**Keywords:** cross-impact; order-flow imbalance; latent factors;
simultaneity; measurement error; preregistration; bootstrap inference.

## 1. Research Question

Suppose the return of asset \(i\) covaries with the contemporaneous order flow
of asset \(j\). The association may represent a direct causal channel from
\(j\)'s flow to \(i\)'s price. It may instead reflect a common information
factor, market-wide liquidity demand, contemporaneous price chasing,
measurement error, or a combination of these mechanisms.

The scientific question is therefore not whether a cross coefficient can be
estimated, but which structural object that coefficient targets. This matters
in practice because structural impact matrices enter execution-cost models,
liquidity stress tests, and manipulation constraints. A reduced-form predictor
may still forecast well while being unsuitable as a structural primitive.

The project is organized around a falsifiable claim sequence:

```text
structural system
    -> population regression target
    -> known-truth recovery
    -> premise stress test
    -> market identification
    -> sealed holdout and economics
```

A failure at any arrow stops downstream interpretation rather than being
rewritten as a positive result.

## 2. Simultaneous System

Let returns \(r_t\), flows \(q_t\), and idiosyncratic shocks \(u_t,v_t\) lie in
\(\mathbb{R}^N\), with latent factors \(f_t\in\mathbb{R}^K\):

\[
\begin{aligned}
r_t &= \Lambda q_t + \Gamma f_t + u_t, \\
q_t &= B r_t + \Delta_f f_t + v_t.
\end{aligned}
\]

Here \(\Lambda\) is the structural contemporaneous impact matrix and \(B\) is
same-bin return-to-flow feedback. Define

\[
L=I_N-B\Lambda,\qquad H=L^{-1},\qquad
P=H(B\Gamma+\Delta_f),\qquad U=HB,\qquad V=H.
\]

The reduced form for flow is

\[
q_t=P f_t+Uu_t+Vv_t,
\]

with covariance

\[
\Sigma_{qq}=P\Sigma_fP^\top+U\Sigma_uU^\top+V\Sigma_vV^\top.
\]

### Theorem 1 — Pseudo-true cross-impact matrices

Under the finite-moment, zero-contemporaneous-cross-covariance, law-of-large-
numbers, and nonsingularity conditions stated in the manuscript, the population
coefficient from regressing \(r_t\) on \(q_t\) is

\[
\operatorname{plim}\widehat\Lambda_{\mathrm{OLS}}
=\Lambda+\Gamma\Sigma_fP^\top\Sigma_{qq}^{-1}
+\Sigma_uU^\top\Sigma_{qq}^{-1}.
\]

If the regression controls for \(h_t=f_t+\varepsilon_t\), define the residual
factor covariance

\[
R_f=\Sigma_f-\Sigma_f(\Sigma_f+\Sigma_\varepsilon)^{-1}\Sigma_f
\]

and

\[
Q_h=PR_fP^\top+U\Sigma_uU^\top+V\Sigma_vV^\top.
\]

Then

\[
\operatorname{plim}\widehat\Lambda_{q\mid h}
=\Lambda+\Gamma R_fP^\top Q_h^{-1}
+\Sigma_uU^\top Q_h^{-1}.
\]

The result has two immediate implications.

1. A more precise factor proxy reduces residual factor variation in positive-
   semidefinite order, but individual coefficient biases need not decrease
   monotonically because the inverse regressor covariance changes at the same
   time.
2. A zero structural entry \(\Lambda_{ij}=0\) does not imply a zero population
   regression coefficient. Latent-factor and feedback terms can both be
   off-diagonal.

The complete derivation and proof are in
[GATE_G1_PROBABILITY_LIMITS.md](docs/derivations/GATE_G1_PROBABILITY_LIMITS.md)
and the manuscript appendix.

## 3. Completed Known-Truth Verification

The G1 derivation was frozen before simulation code and random-number access.
The accepted experiment used one master draw split into 100 immutable shards.
Each shard held 100,000 observations and published only mergeable sufficient
statistics. The complete run therefore contained \(T=10^7\) observations for
\(N=30\) assets and \(K=3\) factors.

| Quantity | Verified value |
| --- | ---: |
| Assets / factors / observations | 30 / 3 / 10,000,000 |
| Reported coefficient targets | 1,800 |
| Uncontrolled OLS maximum relative discrepancy | 0.0005639467093140219 |
| Proxy-controlled maximum relative discrepancy | 0.0005123714186295689 |
| Preregistered gate threshold | 0.001 |
| Targets inside simultaneous intervals | 1,800 / 1,800 |
| Interval method | Student-t, Bonferroni 95% FWER |

The immediate replay reused all validated checkpoints and reproduced the
summary, estimates, and success marker byte for byte. G1 is closed; the frozen
draw must not be rerun or replaced.

Accepted evidence is stored in [results/g1](results/g1), with the exact design,
predictions, and audit trail in:

- [G1 prediction](docs/predictions/GATE_G1.md)
- [G1 derivation](docs/derivations/GATE_G1_PROBABILITY_LIMITS.md)
- [G1 red-team memo](docs/redteam/GATE_G1.md)

## 4. Registered G2 Premise Test

The next gate asks a deliberately narrower question before empirical data is
opened:

> Can confounding alone produce economically material off-diagonal coefficient
> error in a transparent model constrained by opened primary-source summaries,
> even when the estimator receives a favorable factor proxy?

The registered system sets \(B=0\) so that same-bin feedback cannot explain a
positive result. It retains \(N=30\), uses one permutation-invariant factor,
sets proxy reliability to 0.95, and evaluates 17 frozen homogeneous structural
off-diagonal values from 0.0029 through 0.0046.

Three smooth estimators are binding at every grid point:

1. an observable integrated-top-ten-OFI proxy-control condition-ridge
   estimator;
2. an oracle-flow condition-ridge estimator; and
3. an oracle-flow homogeneous three-slope OLS estimator.

The published-protocol reconstruction fits six specifications—\(PI_1\),
\(PI_I\), \(CI_1\), \(CI_I\), \(PI_{CC}\), and \(CI_{CC}\)—with training-only
feature construction and five contiguous validation folds. \(CI_I\) is the
binding published-protocol veto because it combines integrated top-ten OFI
with explicit off-diagonal coefficients. The remaining specifications are
mandatory diagnostics and cannot rescue a failed binding event.

For focal estimate \(\widehat\Lambda_{01}\), truth \(o\), and whole-date
bootstrap standard error \(SE_{\mathrm{boot}}\), passage requires

\[
\left|\widehat\Lambda_{01}-o\right|-0.50|o|
>3SE_{\mathrm{boot}}.
\]

The registered inference uses 499 shared whole-date bootstrap weight vectors.
The smooth-estimator license additionally requires a 100-superpanel finite null
grid with at most one family-union success and a 100-superpanel power panel with
at least 87 all-event successes. The published \(CI_I\) branch has a separate
full-dimension recovery panel; it is a no-strawman recovery check, not a Monte
Carlo size or power claim.

**Current status:** the contract, test-only random-number namespace, pure data-
generating maps, smooth estimator core, checkpoint/recovery boundary, and
several deterministic paper-reconstruction kernels are implemented and tested.
The A022--A027 resource authority is documented, including the deterministic
paper-cache field order and in-memory codec, but executable resource admission
and rehearsal are not complete. Therefore no registered G2 stream is licensed.

## 5. Gate Status

| Gate | Status | Licensed statement |
| --- | --- | --- |
| G0 — environment and compute plan | Passed | Reproducible software and bounded compute skeleton |
| G1 — derivation and known-truth recovery | Passed | Derived population targets recovered under the frozen simulation law |
| G2 — premise test / kill switch | Open | Design authority and deterministic software evidence only; no G2 result |
| G3–G7 — data, identification, estimation, validation, holdout | Locked | No market-data, predictive, causal, trading, or economic claim |
| G8 — final-results paper and release | Locked | This pre-results preprint adds no downstream result or submission-facing empirical claim |

The authoritative live state is [STATE.md](STATE.md). Amendments and rejected
specifications remain visible in [PREREGISTRATION.md](PREREGISTRATION.md),
[DECISIONS.md](DECISIONS.md), [ASSUMPTIONS.md](ASSUMPTIONS.md), and
[SPECIFICATION_LOG.md](SPECIFICATION_LOG.md).

## 6. Reproducibility

Install the locked environment and run the deterministic repository gate:

```bash
uv sync --locked --extra dev
make check
```

`make check` performs linting, formatting verification, strict type checking,
the deterministic/test-seed suite, the G0 software smoke, and committed-result
drift checks. It does not open a registered G2 stream.

The fresh local deterministic gate used for preprint version 0.1 reported:

| Check | Result |
| --- | --- |
| Ruff lint | Pass |
| Ruff format | 28 files checked |
| Strict mypy | Pass, 28 source files |
| Pytest | 317 passed in 37.07 seconds |
| Deterministic G0 demo | 64 rows; expected hashes reproduced |
| Committed-result drift | Pass; no drift |

These are software and artifact-consistency checks, not additional scientific
trials and not a license to run a registered G2 stream.

The deterministic smoke path alone is:

```bash
make demo
```

The consumed G1 command and every registered G2 command are intentionally not
replay instructions. Do not run `make mc`, `make g1-benchmark`, or any G2
resource, validation, or research entry point without the exact authority
recorded in the current gate ledger.

### Evidence map

| Artifact | Role |
| --- | --- |
| [configs/g1.toml](configs/g1.toml) | Frozen G1 design |
| [results/g1/summary.json](results/g1/summary.json) | Accepted G1 gate statistic and interval summary |
| [configs/g2.toml](configs/g2.toml) | Hash-sealed S0004 scientific contract |
| [GATE_G2_PREMISE.md](docs/derivations/GATE_G2_PREMISE.md) | G2 estimands, algorithms, and decision rules |
| [GATE_G2_RESOURCE_ADMISSION.md](docs/derivations/GATE_G2_RESOURCE_ADMISSION.md) | Conditional resource-admission derivation |
| [src/xid/models/g2_paper.py](src/xid/models/g2_paper.py) | Deterministic paper-reconstruction kernels |
| [tests/test_g2_paper.py](tests/test_g2_paper.py) | Known-answer and fail-closed paper-kernel tests |
| [src/xid/models/g2_paper_cache.py](src/xid/models/g2_paper_cache.py) | A027 no-RNG semantic field order and in-memory codec |
| [tests/test_g2_paper_cache.py](tests/test_g2_paper_cache.py) | Bijection, orientation, immutability, and scope-boundary tests |
| [data/manifest.json](data/manifest.json) | Zero-external-data manifest |

## 7. Limitations

The completed evidence is deliberately narrow.

- G1 is Gaussian, known-truth, and large-sample. Its dense positive coefficients
  do not reproduce the small, sign-sensitive off-diagonals central to the
  empirical question.
- One frozen realization verifies recovery under its stated law; it is not an
  estimate of repeated-sampling coverage.
- The G2 one-spike residual spectrum is a declared maximum-entropy convention,
  not an identified feature of an exchange.
- The 95% proxy reliability, structural-sensitivity interval, and dependence
  stress are registered sensitivity inputs assembled from nonidentical sources
  and units.
- Resource admission remains conditional. Tiled cache fixtures cannot establish
  heterogeneous 252-date lifetime, full-mixture scaling, or future thermal
  behavior.
- Predictive performance, structural identification, market impact, execution
  savings, transaction costs, capacity, and profitability are unresolved.

The present evidence does not support a trading rule, deployment claim, or
return claim. Those questions become meaningful only after the identification,
dependence-robust inference, cost, and sealed holdout gates survive.

## 8. Selected References

1. Kyle, A. S. (1985). Continuous auctions and insider trading.
   *Econometrica*, 53(6), 1315–1335.
   [doi:10.2307/1913210](https://doi.org/10.2307/1913210)
2. Hasbrouck, J. (1991). Measuring the information content of stock trades.
   *Journal of Finance*, 46(1), 179–207.
   [doi:10.1111/j.1540-6261.1991.tb03749.x](https://doi.org/10.1111/j.1540-6261.1991.tb03749.x)
3. Hasbrouck, J., & Seppi, D. J. (2001). Common factors in prices, order flows,
   and liquidity. *Journal of Financial Economics*, 59(3), 383–411.
   [doi:10.1016/S0304-405X(00)00091-X](https://doi.org/10.1016/S0304-405X(00)00091-X)
4. Cont, R., Kukanov, A., & Stoikov, S. (2014). The price impact of order book
   events. *Journal of Financial Econometrics*, 12(1), 47–88.
   [doi:10.1093/jjfinec/nbt003](https://doi.org/10.1093/jjfinec/nbt003)
5. Benzaquen, M., Mastromatteo, I., Eisler, Z., & Bouchaud, J.-P. (2017).
   Dissecting cross-impact on stock markets. *Journal of Statistical Mechanics:
   Theory and Experiment*, 2017(2), 023406.
   [doi:10.1088/1742-5468/aa53f7](https://doi.org/10.1088/1742-5468/aa53f7)
6. Capponi, F., & Cont, R. (2020). Multi-asset market impact and order flow
   commonality. SSRN Working Paper 3706390.
   [doi:10.2139/ssrn.3706390](https://doi.org/10.2139/ssrn.3706390)
7. Cont, R., Cucuringu, M., & Zhang, C. (2023). Cross-impact of order flow
   imbalance in equity markets. *Quantitative Finance*, 23(10), 1373–1393.
   [doi:10.1080/14697688.2023.2236159](https://doi.org/10.1080/14697688.2023.2236159)
8. White, H. (2000). A reality check for data snooping. *Econometrica*, 68(5),
   1097–1126.
   [doi:10.1111/1468-0262.00152](https://doi.org/10.1111/1468-0262.00152)
9. Hansen, P. R. (2005). A test for superior predictive ability. *Journal of
   Business & Economic Statistics*, 23(4), 365–380.
   [doi:10.1198/073500105000000063](https://doi.org/10.1198/073500105000000063)

## 9. License and Citation

Copyright © 2026 Mehmet Demir Güven. The preprint manuscript, manuscript source,
and original paper figures are licensed under
[CC BY 4.0](LICENSE-PREPRINT.md). Those identified paper artifacts are outside
the “Software” covered by the repository's MIT license. The MIT license
continues to govern the software and its associated documentation; the scoped
preprint notice grants no additional rights in the README, configurations,
data, checkpoints, or result artifacts.

No arXiv identifier exists yet. Until one is assigned, cite this version as:

> Mehmet Demir Güven (2026). “Spurious or Structural? Probability Limits and a
> Registered Falsification Design for Cross-Asset Price Impact.” Preprint,
> version 0.1, 6 August 2026.

For a reproducible reference to the repository state, include the commit hash
and access date.
