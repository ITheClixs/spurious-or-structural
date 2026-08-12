# Spurious or Structural?

## Low-Rank Confounding and Partial Identification of Cross-Asset Price Impact

**Mehmet Demir Güven †**

Department of Computer Science, ETH Zürich

> † Independent research. ETH Zürich did not fund, sponsor, approve, or endorse
> this work. The affiliation records the author's status as a student only, and
> the views expressed are the author's alone.

**Preprint · Version 0.2 · 12 August 2026 · [CC BY 4.0](LICENSE-PREPRINT.md)**

[![CI](https://github.com/ITheClixs/spurious-or-structural/actions/workflows/ci.yml/badge.svg)](https://github.com/ITheClixs/spurious-or-structural/actions/workflows/ci.yml)

> **Evidence status — 12 August 2026.** G0 and G1 have passed. G2 is open: the
> scientific design and document authority are registered, but executable
> resource admission is incomplete. No registered G2 resource benchmark,
> validation panel, research draw, external market data, training sample,
> holdout, or economic evaluation has been accessed.

Current preprint: [PDF](output/pdf/xid_pre_results_manuscript.pdf) ·
[LaTeX source](docs/pre_results/xid_pre_results_manuscript.tex) ·
[license notice](LICENSE-PREPRINT.md)

## Abstract

Cross-asset return-on-flow coefficients are routinely read as entries of a
structural price-impact matrix. That reading is not merely noisy; it is
generically unidentified, and this project characterises exactly how.

In a simultaneous \(N\)-asset system with \(K\) latent factors and same-bin
feedback \(B\), the gap between the population regression coefficient and the
structural impact matrix has rank at most \(K+\operatorname{rank}(B)\). When
the structural matrix is diagonal and feedback is absent, the entire estimated
cross-impact matrix is confined to the diagonal-plus-rank-\(K\) set, yet its
off-diagonal entries can be as large as genuine own-impact. Because the gap is
a free low-rank object, the structural matrix is set-identified rather than
point-identified from second moments. In the permutation-invariant one-spike
geometry the sharp identified interval is available in closed form, and at
published one-minute commonality statistics it contains zero. The rank
restriction is nonetheless refutable, which yields a scale-free diagnostic
whose rejection supports genuine cross-impact — the reverse of the usual
reading.

The derivations are verified in a preregistered known-truth experiment with
\(N=30\), \(K=3\), and \(T=10^7\). The empirical premise test is registered
here but not reported.

**Keywords:** cross-impact; order-flow imbalance; latent factors; partial
identification; low-rank structure; preregistration.

## 1. The Motivating Puzzle

Capponi and Cont regress one-minute returns on the order-flow imbalance of
every stock in a large cross-section and report a mean cross-asset coefficient
of **+0.032**, with **23.09%** of coefficients negative. Adding a single
cross-sectional principal-component control moves the mean to **−0.039** and
the negative share to **84.46%**.

One control flips the sign of average estimated cross-impact. Either the
uncontrolled regression was contaminated and the controlled one reveals the
truth, or the control absorbed real impact. This project's answer is that
**neither reading is identified**, and it makes that precise.

Structural impact matrices enter execution-cost models, liquidity stress tests,
and manipulation constraints, so the ambiguity is not academic.

## 2. Simultaneous System

Let returns \(r_t\), flows \(q_t\), and shocks \(u_t,v_t\) lie in
\(\mathbb{R}^N\), with latent factors \(f_t\in\mathbb{R}^K\):

\[
r_t = \Lambda q_t + \Gamma f_t + u_t,
\qquad
q_t = B r_t + \Delta_f f_t + v_t.
\]

With \(L=I_N-B\Lambda\), \(H=L^{-1}\), \(P=H(B\Gamma+\Delta_f)\), \(U=HB\), and
\(V=H\), the flow reduced form is \(q_t=Pf_t+Uu_t+Vv_t\).

### Theorem 1 — Pseudo-true cross-impact matrices

\[
\operatorname{plim}\widehat\Lambda_{\mathrm{OLS}}
=\Lambda+\Gamma\Sigma_fP^\top\Sigma_{qq}^{-1}
+\Sigma_uU^\top\Sigma_{qq}^{-1}.
\]

Controlling for \(h_t=f_t+\varepsilon_t\) replaces \(\Sigma_f\) with the
residual factor covariance
\(R_f=\Sigma_f-\Sigma_f(\Sigma_f+\Sigma_\varepsilon)^{-1}\Sigma_f\) and
\(\Sigma_{qq}\) with \(Q_h=PR_fP^\top+U\Sigma_uU^\top+V\Sigma_vV^\top\).

Write \(G:=\operatorname{plim}\widehat\Lambda_{\mathrm{OLS}}-\Lambda\) for the
**confounding gap**. Everything below concerns its structure.

## 3. The Confounding Gap Is Low Rank

### Theorem 2 — Rank of the confounding gap

\[
\operatorname{rank}(G)\;\le\;K+\operatorname{rank}(B).
\]

The factor channel passes through a \(K\)-dimensional bottleneck and the
feedback channel through the column space of \(B\); rank is subadditive. The
bound is attained generically.

| \(\operatorname{rank}(B)\) | Observed \(\operatorname{rank}(G)\) | Bound |
| ---: | ---: | ---: |
| 0 | 3 | 3 |
| 1 | 4 | 4 |
| 2 | 5 | 5 |
| 30 | 30 | 33 |

### Corollary — Spurious cross-impact is confined, but not small

If \(\Lambda\) is diagonal and \(B=0\), the population coefficient matrix lies
in \(\mathcal{D}_K=\{D+R : D \text{ diagonal},\ \operatorname{rank}(R)\le K\}\).

This bounds the *shape*, not the *size*. At the registered fixture a strictly
diagonal truth induces spurious off-diagonals reaching **0.2207** against
genuine own-impact spanning **0.2061** to **0.3953**. Confounding does not
perturb a cross-impact matrix; it manufactures one of realistic magnitude out
of nothing.

### Proposition 3 — The structural matrix is set-identified

With \(B=0\), \(\Sigma_f=I_K\), and \(W=\Sigma_{qq}^{-1}\Delta_f\), any
\(\Lambda = A - \Gamma W^\top\) satisfying the positive-semidefiniteness
constraints reproduces the observed second moments exactly. Cross-impact is a
**partial identification** problem; a factor control moves the estimate *along*
the confounding directions rather than out of the identified set.

### Proposition 4 — Sharp interval in the one-spike geometry

In the registered permutation-invariant geometry the gap collapses to a single
constant added to *every* entry, and

\[
\Lambda_{\mathrm{off}}\in
\left[A_{\mathrm{off}}-\tfrac{T}{N},\; A_{\mathrm{off}}+\tfrac{T}{N}\right],
\qquad
T^2=\frac{(r_1-q_1a_1^2)(q_1-q_0)}{q_1q_0}.
\]

At the source-matched calibration (\(N=30\), \(s_q=0.2827\), \(s_r=0.32\),
\(d=0.29\)):

| \(o\) | \(A_{\mathrm{off}}\) | Half-width | Identified interval | Contains 0 |
| ---: | ---: | ---: | :--- | :--- |
| 0.0029 | 0.010554 | 0.094306 | \([-0.083753,\ 0.104860]\) | yes |
| 0.0046 | 0.012254 | 0.090420 | \([-0.078166,\ 0.102673]\) | yes |

The identified half-width is **7.4 to 8.9 times** the observed coefficient it
is meant to pin down. Under the stated conventions the structural off-diagonal
is **not identified even in sign**.

A bisection over the exact positive-semidefiniteness frontier reproduces the
closed form to relative error below \(10^{-10}\).

### Definition — A refutable diagnostic

\[
\psi_K(\widehat A)=
\frac{\min_{D,\ \operatorname{rank}(R)\le K}\|\widehat A-D-R\|_F}
     {\|\widehat A-\operatorname{diag}(\widehat A)\|_F}.
\]

Its population value is zero under pure confounding, so a materially nonzero
\(\psi_K\) is evidence **for** genuine structural cross-impact. This inverts
the conventional reading: off-diagonal magnitude carries no information, only
departure from \(\mathcal{D}_K\) does.

Two caveats are stated up front. \(\psi_K=0\) does not prove diagonality — the
test refutes, it does not confirm. And \(\psi_K\) depends on the assumed factor
count, so a sweep is mandatory:

| Assumed \(K\) | 1 | 2 | **3** | 4 | 6 | 10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| \(\psi_K\) | 0.6396 | 0.3748 | **0.0391** | 0.0377 | 0.0328 | 0.0250 |

The elbow at the true \(K=3\) is a practical way to read the factor count off
the coefficient matrix itself.

The full derivation and proofs are in
[CONFOUNDING_RANK_AND_PARTIAL_ID.md](docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md),
registered before implementation as amendment A028.

## 4. Completed Known-Truth Verification

The G1 derivation was frozen before simulation code and random-number access.
One master draw was split into 100 immutable shards of 100,000 observations
each, publishing only mergeable sufficient statistics, for \(T=10^7\)
observations at \(N=30\) and \(K=3\).

| Quantity | Verified value |
| --- | ---: |
| Assets / factors / observations | 30 / 3 / 10,000,000 |
| Reported coefficient targets | 1,800 |
| Uncontrolled OLS maximum relative discrepancy | 0.0005639467093140219 |
| Proxy-controlled maximum relative discrepancy | 0.0005123714186295689 |
| Preregistered gate threshold | 0.001 |
| Targets inside simultaneous intervals | 1,800 / 1,800 |
| Interval method | Student-t, Bonferroni 95% FWER |

Replay reused all validated checkpoints and reproduced the summary, estimates,
and success marker byte for byte. G1 is closed; the frozen draw must not be
rerun.

## 5. Confronting Published Evidence

Because the one-spike gap is a constant added to every entry, a single factor
control should shift every cross-coefficient by the same amount. Two
implications follow, and they **disagree**.

**Dispersion invariance holds.** The reported mean cross coefficient moves from
0.032 to −0.039, a shift of −0.071, while the cross-sectional standard
deviation stays at 0.06 and the own-coefficient standard deviation moves only
from 0.78 to 0.77. Both are at or within reported precision. This check is
unit-free.

**The shape implication fails.** Under an exactly constant shift the
post-control negative fraction should equal the pre-control mass below the
shift magnitude, which a Gaussian approximation puts at 0.7422 against a
reported 0.8446 — a gap of 0.1024, exceeding the declared 0.05 tolerance.

The failure is reported rather than removed; the registered protocol forbids
retuning the one-spike convention to close it. It points at loading
heterogeneity beyond one common factor and does not bear on Theorem 2, which
is an inequality in \(K\).

Both are **conditional analytic exhibits at published summary statistics, not
estimates of any market's impact matrix.**

## 6. Registered Premise Test

The next gate asks a deliberately narrow question before empirical data is
opened:

> Can confounding alone produce economically material off-diagonal coefficient
> error in a transparent model constrained by opened primary-source summaries,
> even when the estimator receives a favourable factor proxy?

The registered system sets \(B=0\) so same-bin feedback cannot explain a
positive result, retains \(N=30\), uses one permutation-invariant factor, sets
proxy reliability to 0.95, and evaluates 17 frozen structural off-diagonal
values from 0.0029 to 0.0046. Three smooth estimators bind at every grid point;
a six-specification published-protocol reconstruction supplies a separate veto.
Passage requires

\[
\left|\widehat\Lambda_{01}-o\right|-0.50|o|>3\,SE_{\mathrm{boot}}
\]

with 499 shared whole-date bootstrap replicates, after 100 validation
superpanels license the exact procedure.

**Current status:** contract, test-only RNG namespace, pure DGP maps, smooth
estimator core, checkpoint/recovery boundary, deterministic paper kernels, and
the A027 paper-cache codec are implemented and tested. Executable resource
admission and rehearsal are incomplete, so no registered G2 stream is licensed.

## 7. Gate Status

| Gate | Status | Licensed statement |
| --- | --- | --- |
| G0 — environment and compute plan | Passed | Reproducible software and bounded compute skeleton |
| G1 — derivation and known-truth recovery | Passed | Derived population targets recovered under the frozen simulation law |
| G2 — premise test / kill switch | Open | Design authority and deterministic software evidence only; no G2 result |
| G3–G7 — data, identification, estimation, validation, holdout | Locked | No market-data, predictive, causal, trading, or economic claim |
| G8 — final-results paper and release | Locked | This pre-results preprint adds no downstream result |

Authoritative live state: [STATE.md](STATE.md). Amendments and rejected
specifications remain visible in [PREREGISTRATION.md](PREREGISTRATION.md),
[DECISIONS.md](DECISIONS.md), [ASSUMPTIONS.md](ASSUMPTIONS.md), and
[SPECIFICATION_LOG.md](SPECIFICATION_LOG.md). Working standards are in
[RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md).

## 8. Reproducibility

```bash
uv sync --locked --extra dev
make check        # lint, format, strict types, tests, smoke, drift
make exhibits     # regenerate every manuscript number; fails on drift
make paper        # build the preprint PDF
```

Fresh local gate for preprint version 0.2:

| Check | Result |
| --- | --- |
| Ruff lint | Pass |
| Ruff format | 34 files checked |
| Strict mypy | Pass, 34 source files |
| Pytest | 372 passed |
| Deterministic G0 demo | 64 rows; expected hashes reproduced |
| Committed-result drift | Pass; no drift |

These are software and artifact-consistency checks, not scientific trials, and
they do not license a registered G2 stream. **Every quantitative value in the
manuscript is regenerated by `make exhibits`; none is transcribed by hand.**

Do not run `make mc`, `make g1-benchmark`, or any G2 resource, validation, or
research entry point without the exact authority recorded in the current gate
ledger.

### Evidence map

| Artifact | Role |
| --- | --- |
| [CONFOUNDING_RANK_AND_PARTIAL_ID.md](docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md) | Rank bound, identified set, sharp interval, diagnostic |
| [THEORY_EXTENSION.md](docs/predictions/THEORY_EXTENSION.md) | Six predictions frozen before implementation |
| [identification.py](src/xid/models/identification.py) | Probability limits, confounding gap, one-spike bounds |
| [rank_diagnostic.py](src/xid/models/rank_diagnostic.py) | The \(\psi_K\) statistic |
| [exhibits.py](src/xid/exhibits.py) | Deterministic generator for every manuscript number |
| [generated/exhibits.json](docs/pre_results/generated/exhibits.json) | Committed exhibit values |
| [GATE_G1_PROBABILITY_LIMITS.md](docs/derivations/GATE_G1_PROBABILITY_LIMITS.md) | Theorem 1 derivation |
| [results/g1/summary.json](results/g1/summary.json) | Accepted G1 gate statistic |
| [configs/g2.toml](configs/g2.toml) | Hash-sealed S0004 scientific contract |
| [GATE_G2_PREMISE.md](docs/derivations/GATE_G2_PREMISE.md) | G2 estimands, algorithms, decision rules |
| [G2_SOURCE_AUDIT.md](docs/G2_SOURCE_AUDIT.md) | Primary-source audit of published statistics |
| [data/manifest.json](data/manifest.json) | Zero-external-data manifest |

## 9. Limitations

- Theorem 2 is an inequality, so a high observed rank is uninformative if \(K\)
  is misspecified, and the gap's rank is not separately observable from that of
  a genuinely low-rank \(\Lambda\).
- Proposition 3 assumes \(B=0\); with feedback the identified set is larger,
  not smaller, so the sign non-identification result is conservative in that
  direction only.
- The closed-form interval is conditional on the one-spike and
  isotropic-residual conventions, which are declared maximum-entropy choices
  and not identified features of any exchange.
- \(\psi_K\) is an upper bound from a stationary point of an alternating
  projection, has no derived sampling distribution here, and cannot confirm
  diagonality.
- The G1 fixture is Gaussian, known-truth, and large-sample; its dense positive
  targets do not reproduce the small, sign-sensitive off-diagonals central to
  the empirical question.
- The published-evidence exercise uses summary statistics carrying no
  inferential intervals, so it supports consistency statements only.
- Predictive performance, structural identification, market impact, execution
  savings, transaction costs, capacity, and profitability are unresolved. The
  present evidence supports no trading rule, deployment claim, or return claim.

## 10. Selected References

The manuscript carries 45 references. The most directly relevant:

1. Kyle, A. S. (1985). Continuous auctions and insider trading. *Econometrica*,
   53(6), 1315–1335.
2. Hasbrouck, J., & Seppi, D. J. (2001). Common factors in prices, order flows,
   and liquidity. *Journal of Financial Economics*, 59(3), 383–411.
3. Cont, R., Kukanov, A., & Stoikov, S. (2014). The price impact of order book
   events. *Journal of Financial Econometrics*, 12(1), 47–88.
4. Benzaquen, M., Mastromatteo, I., Eisler, Z., & Bouchaud, J.-P. (2017).
   Dissecting cross-impact on stock markets. *JSTAT*, 2017(2), 023406.
5. Capponi, F., & Cont, R. (2020). Multi-asset market impact and order flow
   commonality. SSRN 3706390.
6. Cont, R., Cucuringu, M., & Zhang, C. (2023). Cross-impact of order flow
   imbalance in equity markets. *Quantitative Finance*, 23(10), 1373–1393.
7. Manski, C. F., & Tamer, E. (2002). Inference on regressions with interval
   data on a regressor or outcome. *Econometrica*, 70(2), 519–546.
8. Chandrasekaran, V., Parrilo, P. A., & Willsky, A. S. (2012). Latent variable
   graphical model selection via convex optimization. *Annals of Statistics*,
   40(4), 1935–1967.
9. Miao, W., Geng, Z., & Tchetgen Tchetgen, E. J. (2018). Identifying causal
   effects with proxy variables of an unmeasured confounder. *Biometrika*,
   105(4), 987–993.

Full bibliography: [references.bib](docs/pre_results/references.bib).

## 11. License and Citation

Copyright © 2026 Mehmet Demir Güven. The preprint manuscript, its source, and
its original figures are licensed under [CC BY 4.0](LICENSE-PREPRINT.md), and
are outside the "Software" covered by the repository's MIT license. The MIT
license governs the software and its associated documentation.

No arXiv identifier exists yet. Until one is assigned, cite as:

> Mehmet Demir Güven (2026). "Spurious or Structural? Low-Rank Confounding and
> Partial Identification of Cross-Asset Price Impact." Preprint, version 0.2,
> 12 August 2026.

For a reproducible reference to the repository state, include the commit hash
and access date.
