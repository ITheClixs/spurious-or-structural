# arXiv Submission Upgrade Implementation Plan

> **For agentic workers:** Steps use checkbox (`- [ ]`) syntax for tracking.
> Execute task-by-task; each task ends with an independently testable
> deliverable and a commit.

**Goal:** Turn the existing pre-results preprint into a submission-ready arXiv
paper whose central contribution is a new, verified partial-identification
theory of cross-impact — not merely a restatement that OLS is biased.

**Architecture:** Three layers. (1) A new derivation proving the confounding
gap `plim Λ̂ − Λ` has rank at most `K + rank(B)`, which converts the vague
"cross-impact may be spurious" claim into a sharp, testable rank restriction
and a partial-identification result. (2) A deterministic, test-seed-only
software layer that verifies the theory, computes sharp bounds, and implements
a `diagonal-plus-rank-K` specification diagnostic. (3) A rewritten manuscript
and README that lead with the new theorem, anchor it to already-opened
published summary statistics, and retain the registered G2 protocol as the
forward-looking falsification design.

**Tech Stack:** Python 3 + NumPy (locked `uv` environment), pytest, Ruff, mypy
strict, LaTeX via `tectonic`, TikZ/PGF for figures.

## Global Constraints

These apply to **every** task. No exceptions.

- **Gate discipline.** G2 remains executable-red. No task may run a registered
  resource, validation, or research stream; construct a registered RNG
  namespace; touch seeds `2026071529`, `2026071521`, `2026071522`; access
  external market data; or open the holdout. Test-only seeds `1729`, `9191`,
  `314159` are the sole permitted randomness.
- **Derive before code.** Every new estimator or statistic gets a derivation
  document and a written quantitative prediction *before* its implementation,
  per `AGENTS.md` research invariants and `docs/GATES.md` cross-gate invariants.
- **Red before green.** Record the observed failing test output in
  `SPECIFICATION_LOG.md` before writing the implementation.
- **No new empirical claim.** Published summary statistics from
  `docs/G2_SOURCE_AUDIT.md` are already opened. Evaluating an analytic formula
  at those numbers is a *conditional analytic exhibit*, never "an estimate of a
  market's Λ". Every such exhibit carries that label.
- **Interval rule.** Every inferential number has an interval and a named
  interval method. Deterministic algebraic quantities are labelled
  "deterministic; not applicable" rather than given a fake interval.
- **Author identity.** Author is `Mehmet Demir Güven`, with a dagger (`†`)
  superscript on the name. Affiliation: `Department of Computer Science,
  ETH Zürich`. The dagger footnote must state: independent research; ETH Zürich
  did not fund, sponsor, approve, or endorse the work; affiliation records
  student status only; views are the author's alone.
- **Page furniture.** The exact string `Preprint. Under review.` appears in the
  footer of **every** page including the first.
- **No AI-assistance traces.** No file, comment, commit message, docstring,
  metadata field, or manuscript sentence may reference AI, agents, assistants,
  language models, or automated generation. Nothing in the repository claims
  authorship other than Mehmet Demir Güven.
- **Locked gate must stay green.** `make check` (Ruff, format, strict mypy,
  full pytest, deterministic demo, committed-result drift) passes before every
  commit.
- **Determinism.** Every committed artifact must regenerate byte-identically.

---

## File Structure

| Path | Status | Responsibility |
| --- | --- | --- |
| `docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md` | Create | Proofs: rank bound, observational equivalence, sharp one-spike interval, diagnostic consistency |
| `docs/predictions/THEORY_EXTENSION.md` | Create | Quantitative predictions frozen before implementation |
| `PREREGISTRATION.md` | Modify (append) | Amendment `A028` registering the theory extension and exhibit scope |
| `src/xid/models/identification.py` | Create | Pure algebra: plim maps, gap rank, identified set, sharp bounds |
| `src/xid/models/rank_diagnostic.py` | Create | `diagonal-plus-rank-K` residual statistic and its null calibration |
| `src/xid/exhibits.py` | Create | Deterministic CLI producing every manuscript number and figure coordinate |
| `tests/test_identification.py` | Create | Rank bound, equivalence, bounds correctness, fail-closed validation |
| `tests/test_rank_diagnostic.py` | Create | Diagnostic convergence, invariances, power separation |
| `tests/test_exhibits.py` | Create | Exhibit determinism and hash pinning |
| `docs/pre_results/generated/exhibits.json` | Create | Committed deterministic exhibit values |
| `docs/pre_results/generated/*.tex` | Create | Committed TikZ coordinate fragments |
| `docs/pre_results/xid_pre_results_manuscript.tex` | Modify | Full rewrite around the new theory |
| `docs/pre_results/references.bib` | Create | Expanded bibliography (~40 entries) |
| `README.md` | Modify | Rewrite as a paper-style document |
| `RESEARCH_PROTOCOL.md` | Create (replaces `AGENTS.md`) | Author's operating discipline, no agent framing |
| `scripts/build_paper.sh` | Create | Reproducible PDF + arXiv tarball build |
| `docs/ARXIV_SUBMISSION.md` | Create | Submission checklist, metadata, endorsement notes |
| `Makefile` | Modify | Add `exhibits`, `paper`, `arxiv` targets |
| `.gitignore` | Modify | Allowlist committed generated exhibits |

---

## The Core Result (context for every downstream task)

For the simultaneous system

```
r_t = Λ q_t + Γ f_t + u_t
q_t = B r_t + Δ_f f_t + v_t
```

Theorem 1 (already in the repository) gives

```
plim Λ̂_OLS = Λ + Γ Σ_f Pᵀ Σ_qq⁻¹ + Σ_u Uᵀ Σ_qq⁻¹,   P = HD, U = HB, H = (I−BΛ)⁻¹
```

**New Theorem 2.** The confounding gap `G := plim Λ̂_OLS − Λ` satisfies

```
rank(G) ≤ K + rank(B)
```

because `Γ Σ_f Pᵀ Σ_qq⁻¹` factors through `R^K` and `Σ_u Uᵀ Σ_qq⁻¹` factors
through the column space of `Bᵀ`. This has been numerically confirmed as tight
at test seed `1729` for `N=30, K=3` with `rank(B) ∈ {0,1,2,30}`, producing
observed gap ranks `3, 4, 5, 30` against bounds `3, 4, 5, 33`.

**Why it matters.** Under `B=0`, `plim Λ̂_OLS = Λ + (rank-K matrix)`. So if the
truth is diagonal (zero cross-impact), the *entire* estimated cross-impact
matrix must be `diagonal + rank-K`. At the same fixture, a strictly diagonal
truth with diagonal entries in `[0.2, 0.4]` produced spurious off-diagonals up
to `0.2207` — the same order of magnitude as genuine own-impact. This converts
the paper's motivating worry into (a) a falsifiable restriction and (b) a
partial-identification statement: `Λ` is not point-identified from second
moments, and each entry is only interval-identified.

---

### Task 1: Derivation document for the rank bound and partial identification

**Files:**
- Create: `docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md`

**Interfaces:**
- Produces: the symbolic results that Tasks 3–5 implement and Task 9 typesets.
  Downstream tasks reference sections by the exact heading names below.

- [ ] **Step 1: Write the document skeleton with these exact headings**

```
# Confounding rank and partial identification of cross-impact
## Claim being derived
## Dimensions, conventions, and assumptions
## 1. The confounding gap is low rank
## 2. Observational equivalence and the identified set
## 3. Sharp bounds in the permutation-invariant one-spike model
## 4. The diagonal-plus-rank-K restriction as a specification test
## 5. Predictions that must survive numerical verification
## 6. What this derivation does not claim
```

- [ ] **Step 2: Write Section 1 — the rank theorem and proof**

State and prove:

> **Theorem 2.** Under the Theorem 1 conditions,
> `G = Γ Σ_f Pᵀ Σ_qq⁻¹ + Σ_u Uᵀ Σ_qq⁻¹` satisfies `rank(G) ≤ K + rank(B)`.
> If `B = 0` then `G = Γ Σ_f Δ_fᵀ Σ_qq⁻¹` and `rank(G) ≤ min(K, rank(Γ), rank(Δ_f))`.

Proof: the first summand is `Γ · (Σ_f Pᵀ Σ_qq⁻¹)`, a product of an `N×K` and a
`K×N` matrix, so its rank is at most `K`. The second is
`Σ_u Bᵀ Hᵀ Σ_qq⁻¹`, whose rank is at most `rank(Bᵀ) = rank(B)`. Rank is
subadditive over sums. Both bounds are attained generically.

State the corollary that matters:

> **Corollary (spurious cross-impact is low rank).** If `Λ = D` is diagonal and
> `B = 0`, then `plim Λ̂_OLS = D + G` with `rank(G) ≤ K`. Every off-diagonal
> entry of the population OLS coefficient matrix is then attributable to
> confounding, and the matrix lies in the set
> `{diagonal} + {rank ≤ K}`.

- [ ] **Step 3: Write Section 2 — observational equivalence**

Normalize `Σ_f = I_K` (absorbed into `Γ`, `Δ_f`). With `B = 0` the observables
are `A = Σ_rq Σ_qq⁻¹`, `Σ_qq`, and `Σ_rr`. Write `W = Σ_qq⁻¹ Δ_f` (`N×K`).
Then `Λ = A − Γ Wᵀ`, and the model-implied residual covariances are

```
Σ_v = Σ_qq − Δ_f Δ_fᵀ
Σ_u = Σ_rr − Λ Σ_qq Λᵀ − Λ Δ_f Γᵀ − Γ Δ_fᵀ Λᵀ − Γ Γᵀ
```

State:

> **Proposition 3 (identified set).** The identified set for `Λ` given
> `(A, Σ_qq, Σ_rr, K)` is
> `𝓘 = { A − Γ Wᵀ : Δ_f ∈ R^{N×K}, Γ ∈ R^{N×K}, W = Σ_qq⁻¹ Δ_f,
>        Σ_qq − Δ_f Δ_fᵀ ⪰ 0, Σ_u ⪰ 0 }`.
> `𝓘` is generally not a singleton, so `Λ` is set-identified, not
> point-identified, from second moments alone.

Note explicitly that `𝓘` is nonempty because `Γ = 0` (hence `Λ = A`) is always
feasible whenever the data are generated by *some* member of the class.

- [ ] **Step 4: Write Section 3 — closed-form sharp interval in the one-spike model**

Specialize to the registered G2 geometry: `N` assets, `m = 1_N/√N`, `K = 1`,
`B = 0`, and the permutation-invariant one-spike covariances of
Eq. (one-spike) in `GATE_G2_PREMISE.md`, with `Δ_f = h_q m`, `Γ = γ m`.

Then `W = Σ_qq⁻¹ Δ_f = h_q m / q_1` (since `Σ_qq m = q_1 m`), so

```
G = γ h_q / q_1 · m mᵀ,     (G)_ij = γ h_q / (N q_1)  for all i,j
```

The gap is *constant across every entry*, so with `A_off` the common
off-diagonal of `A`,

```
Λ_off(γ) = A_off − γ h_q / (N q_1)
```

Derive the feasible range of `γ` from `Σ_u ⪰ 0` and `Σ_v ⪰ 0` and report the
resulting closed-form interval `[Λ_off^min, Λ_off^max]`. Record whether that
interval contains zero as a derived consequence — do **not** assume it does.

- [ ] **Step 5: Write Section 4 — the diagnostic**

Define, for an estimated coefficient matrix `Â` and integer `K`,

```
ψ_K(Â) = min over diagonal D, rank-K R  of  ‖Â − D − R‖_F  /  ‖Â − diag(Â)‖_F
```

Under `H₀: Λ diagonal, B = 0, K factors`, the population value is `ψ_K = 0`.
A materially nonzero `ψ_K` is evidence *against* pure confounding, i.e. evidence
*for* genuine structural cross-impact. State the direction of the test
explicitly: this is a test whose rejection *supports* structural cross-impact,
which is the opposite polarity of the naive regression reading.

Note the identification caveat: `ψ_K = 0` does not prove `Λ` is diagonal, since
a genuinely low-rank `Λ` off-diagonal is observationally indistinguishable. Say
so.

- [ ] **Step 6: Write Section 5 — quantitative predictions**

Freeze these before implementation:

1. At test seed `1729`, `N=30`, `K=3`, dense random `Λ`, and
   `rank(B) ∈ {0,1,2,30}`, the numerical rank of `G` at relative tolerance
   `1e-10` equals `3, 4, 5, 30` respectively, each `≤ K + rank(B)`.
2. With `Λ` diagonal and `B = 0`, `rank(plim Λ̂_OLS − Λ) = K` exactly, and
   `ψ_K(plim Λ̂_OLS) < 1e-8`.
3. With `Λ` diagonal plus a dense off-diagonal perturbation of Frobenius size
   `ε` and `B = 0`, `ψ_K` increases strictly and monotonically in `ε` over a
   frozen grid.
4. In the one-spike model, the numerically computed sharp interval endpoints
   agree with the Section 3 closed form to `< 1e-10` relative.
5. `ψ_K` is invariant to relabeling assets (simultaneous row/column
   permutation) to `< 1e-12`.

- [ ] **Step 7: Write Section 6 — non-claims**

State: this derivation does not identify `Λ`; does not assert the covariance
restrictions hold in any market; does not license a trading rule; does not
convert the published summary statistics into an estimate of a real impact
matrix; and does not supersede the registered G2 premise test.

- [ ] **Step 8: Commit**

```bash
git add docs/derivations/CONFOUNDING_RANK_AND_PARTIAL_ID.md
git commit -m "Derive the confounding rank bound before implementing it"
```

---

### Task 2: Register the theory extension as amendment A028

**Files:**
- Modify: `PREREGISTRATION.md` (append after the `A027` section)
- Create: `docs/predictions/THEORY_EXTENSION.md`

**Interfaces:**
- Consumes: Section 5 predictions from Task 1.
- Produces: the registered scope that Tasks 3–7 must not exceed.

- [ ] **Step 1: Append amendment A028 to `PREREGISTRATION.md`**

Follow the existing amendment prose style. Content:

- **Scope granted:** a pure-algebra identification module, a deterministic
  rank diagnostic, sharp-bound computation, and analytic exhibits evaluated at
  already-opened published summary statistics.
- **Scope withheld:** no registered stream, no RNG namespace, no market data,
  no new G2 kernel, no change to any sealed G2 digest, no change to the G1
  frozen result, no claim that any exhibit estimates a market's `Λ`.
- **Predictions:** copy the five numbered predictions verbatim from Task 1
  Section 5.
- **Failure rule:** if any prediction fails, the theory section does not enter
  the manuscript. It is not repaired after seeing output and then silently
  accepted.

- [ ] **Step 2: Write `docs/predictions/THEORY_EXTENSION.md`**

Mirror the format of `docs/predictions/GATE_G1.md`. Record: the five
predictions, the exact tolerances, the test seeds used (`1729` only), the
statement that no interval method applies because the quantities are
deterministic algebraic identities, and the multiple-testing count (zero, no
stochastic comparison).

- [ ] **Step 3: Verify no sealed digest changed**

Run:

```bash
shasum -a 256 configs/g2.toml configs/g2_resource.toml
```

Expected: `configs/g2_resource.toml` still hashes to
`1a14fd68012819d5f901a97ddd9e9a58dd35886bdcc5d47728467f6417fc3cd3`.

- [ ] **Step 4: Commit**

```bash
git add PREREGISTRATION.md docs/predictions/THEORY_EXTENSION.md
git commit -m "Register the theory extension before writing its code"
```

---

### Task 3: Identification module — plim maps and the rank bound

**Files:**
- Create: `src/xid/models/identification.py`
- Create: `tests/test_identification.py`

**Interfaces:**
- Produces, for Tasks 4–7:
  - `plim_ols(Lam, B, Gam, Df, Sf, Su, Sv) -> np.ndarray` shape `(N,N)`
  - `plim_proxy(Lam, B, Gam, Df, Sf, Su, Sv, Se) -> np.ndarray` shape `(N,N)`
  - `confounding_gap(Lam, B, Gam, Df, Sf, Su, Sv) -> np.ndarray` shape `(N,N)`
  - `gap_rank_bound(k: int, B: np.ndarray) -> int`
  - `numerical_rank(M: np.ndarray, rtol: float = 1e-10) -> int`
  - All raise `ValueError` on non-float64, non-finite, or shape-inconsistent
    input, matching the fail-closed style of `src/xid/models/g2_smooth.py`.

- [ ] **Step 1: Write the failing test**

```python
import numpy as np
import pytest

from xid.models.identification import (
    confounding_gap,
    gap_rank_bound,
    numerical_rank,
    plim_ols,
)

N, K = 30, 3


def _fixture(rank_b: int):
    rng = np.random.default_rng(1729)

    def psd(n: int) -> np.ndarray:
        a = rng.normal(size=(n, n))
        return a @ a.T / n + np.eye(n) * 0.5

    lam = rng.normal(scale=0.1, size=(N, N))
    gam = rng.normal(size=(N, K))
    df = rng.normal(size=(N, K))
    if rank_b == 0:
        b = np.zeros((N, N))
    elif rank_b >= N:
        b = rng.normal(scale=0.02, size=(N, N))
    else:
        b = rng.normal(size=(N, rank_b)) @ rng.normal(size=(rank_b, N)) * 0.05
    return lam, b, gam, df, psd(K), psd(N), psd(N)


@pytest.mark.parametrize("rank_b,expected", [(0, 3), (1, 4), (2, 5), (30, 30)])
def test_gap_rank_matches_registered_prediction(rank_b: int, expected: int) -> None:
    lam, b, gam, df, sf, su, sv = _fixture(rank_b)
    gap = confounding_gap(lam, b, gam, df, sf, su, sv)
    assert numerical_rank(gap) == expected
    assert numerical_rank(gap) <= gap_rank_bound(K, b)


def test_diagonal_truth_yields_exactly_rank_k_gap() -> None:
    rng = np.random.default_rng(1729)
    _, _, gam, df, sf, su, sv = _fixture(0)
    d = np.diag(rng.uniform(0.2, 0.4, N))
    gap = confounding_gap(d, np.zeros((N, N)), gam, df, sf, su, sv)
    assert numerical_rank(gap) == K
    assert np.abs(gap - np.diag(np.diag(gap))).max() > 0.0


def test_plim_ols_rejects_non_float64() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(0)
    with pytest.raises(ValueError, match="float64"):
        plim_ols(lam.astype(np.float32), b, gam, df, sf, su, sv)


def test_plim_ols_rejects_nonfinite() -> None:
    lam, b, gam, df, sf, su, sv = _fixture(0)
    bad = lam.copy()
    bad[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        plim_ols(bad, b, gam, df, sf, su, sv)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --locked --extra dev pytest tests/test_identification.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'xid.models.identification'`.
Record this exact output for `SPECIFICATION_LOG.md`.

- [ ] **Step 3: Write minimal implementation**

```python
"""Pure-algebra identification results for the simultaneous impact system.

This module contains deterministic linear algebra only. It constructs no
random-number generator, reads no configuration, and touches no registered
stream.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "confounding_gap",
    "gap_rank_bound",
    "numerical_rank",
    "plim_ols",
    "plim_proxy",
]


def _check(name: str, arr: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise ValueError(f"{name}: expected numpy.ndarray")
    if arr.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {arr.dtype}")
    if arr.shape != shape:
        raise ValueError(f"{name}: expected shape {shape}, got {arr.shape}")
    if not np.isfinite(arr).all():
        raise ValueError(f"{name}: expected finite entries")
    return arr


def _reduced_form(
    lam: np.ndarray,
    b: np.ndarray,
    gam: np.ndarray,
    df: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = lam.shape[0]
    h = np.linalg.inv(np.eye(n) - b @ lam)
    return h @ (b @ gam + df), h @ b, h


def _validate(
    lam: np.ndarray,
    b: np.ndarray,
    gam: np.ndarray,
    df: np.ndarray,
    sf: np.ndarray,
    su: np.ndarray,
    sv: np.ndarray,
) -> tuple[int, int]:
    n, k = gam.shape
    _check("lam", lam, (n, n))
    _check("b", b, (n, n))
    _check("gam", gam, (n, k))
    _check("df", df, (n, k))
    _check("sf", sf, (k, k))
    _check("su", su, (n, n))
    _check("sv", sv, (n, n))
    return n, k


def plim_ols(
    lam: np.ndarray,
    b: np.ndarray,
    gam: np.ndarray,
    df: np.ndarray,
    sf: np.ndarray,
    su: np.ndarray,
    sv: np.ndarray,
) -> np.ndarray:
    """Population coefficient of regressing returns on flows."""
    _validate(lam, b, gam, df, sf, su, sv)
    return lam + confounding_gap(lam, b, gam, df, sf, su, sv)


def confounding_gap(
    lam: np.ndarray,
    b: np.ndarray,
    gam: np.ndarray,
    df: np.ndarray,
    sf: np.ndarray,
    su: np.ndarray,
    sv: np.ndarray,
) -> np.ndarray:
    """Return ``plim OLS - Lambda``, the confounding-plus-simultaneity gap."""
    _validate(lam, b, gam, df, sf, su, sv)
    p, u, v = _reduced_form(lam, b, gam, df)
    sqq = p @ sf @ p.T + u @ su @ u.T + v @ sv @ v.T
    inv = np.linalg.inv(sqq)
    return gam @ sf @ p.T @ inv + su @ u.T @ inv


def plim_proxy(
    lam: np.ndarray,
    b: np.ndarray,
    gam: np.ndarray,
    df: np.ndarray,
    sf: np.ndarray,
    su: np.ndarray,
    sv: np.ndarray,
    se: np.ndarray,
) -> np.ndarray:
    """Population coefficient on flow after controlling for a noisy proxy."""
    _, k = _validate(lam, b, gam, df, sf, su, sv)
    _check("se", se, (k, k))
    rf = sf - sf @ np.linalg.inv(sf + se) @ sf
    p, u, v = _reduced_form(lam, b, gam, df)
    qh = p @ rf @ p.T + u @ su @ u.T + v @ sv @ v.T
    inv = np.linalg.inv(qh)
    return lam + gam @ rf @ p.T @ inv + su @ u.T @ inv


def gap_rank_bound(k: int, b: np.ndarray) -> int:
    """Theorem 2 bound ``K + rank(B)`` on the confounding gap rank."""
    if k < 0:
        raise ValueError("k: expected a nonnegative factor count")
    _check("b", b, b.shape)
    if b.ndim != 2 or b.shape[0] != b.shape[1]:
        raise ValueError("b: expected a square matrix")
    return k + int(np.linalg.matrix_rank(b))


def numerical_rank(m: np.ndarray, rtol: float = 1e-10) -> int:
    """Count singular values above ``rtol`` times the largest singular value."""
    if m.dtype != np.float64:
        raise ValueError("m: expected float64")
    if not np.isfinite(m).all():
        raise ValueError("m: expected finite entries")
    sv = np.linalg.svd(m, compute_uv=False)
    if sv.size == 0 or sv[0] == 0.0:
        return 0
    return int((sv > sv[0] * rtol).sum())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --locked --extra dev pytest tests/test_identification.py -v`
Expected: all tests PASS.

- [ ] **Step 5: Run the locked gate**

Run: `make check`
Expected: Ruff, format, strict mypy, full pytest, demo, drift all pass.

- [ ] **Step 6: Commit**

```bash
git add src/xid/models/identification.py tests/test_identification.py
git commit -m "Make the confounding rank bound executable"
```

---

### Task 4: Sharp bounds in the one-spike model

**Files:**
- Modify: `src/xid/models/identification.py`
- Modify: `tests/test_identification.py`

**Interfaces:**
- Produces, for Tasks 6–7:
  - `one_spike_covariance(n: int, share: float) -> np.ndarray`
  - `one_spike_gap_per_entry(gamma, h_q, n, q1) -> float`
  - `sharp_offdiag_interval(a_off, n, q1, h_q, gamma_lo, gamma_hi) -> tuple[float, float]`
  - `feasible_gamma_range(n, s_q, s_r, rho, d, o) -> tuple[float, float]`

- [ ] **Step 1: Write the failing test**

```python
from xid.models.identification import (
    feasible_gamma_range,
    one_spike_covariance,
    sharp_offdiag_interval,
)


def test_one_spike_reproduces_published_pairwise_correlation() -> None:
    # Capponi-Cont one-minute leading flow share, docs/G2_SOURCE_AUDIT.md.
    sig = one_spike_covariance(30, 0.2827)
    off = sig[0, 1]
    assert abs(off - 0.2579655) < 1e-6


def test_sharp_interval_matches_closed_form() -> None:
    n, q1, h_q, a_off = 30, 30 * 0.2827, 1.0, 0.032
    lo_g, hi_g = -2.0, 2.0
    lo, hi = sharp_offdiag_interval(a_off, n, q1, h_q, lo_g, hi_g)
    assert abs(lo - (a_off - hi_g * h_q / (n * q1))) < 1e-12
    assert abs(hi - (a_off - lo_g * h_q / (n * q1))) < 1e-12
    assert lo < hi


def test_feasible_gamma_range_is_nonempty_and_ordered() -> None:
    lo, hi = feasible_gamma_range(30, 0.2827, 0.32, 0.8726, 0.29, 0.0046)
    assert lo < hi
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --locked --extra dev pytest tests/test_identification.py -k "one_spike or sharp or feasible" -v`
Expected: FAIL — `ImportError: cannot import name 'one_spike_covariance'`.

- [ ] **Step 3: Write minimal implementation**

Append to `src/xid/models/identification.py`:

```python
def one_spike_covariance(n: int, share: float) -> np.ndarray:
    """Permutation-invariant one-spike correlation with the given PC1 share."""
    if n < 2:
        raise ValueError("n: expected at least two assets")
    if not 0.0 < share < 1.0:
        raise ValueError("share: expected a value strictly inside (0, 1)")
    lead = n * share
    rest = (n - lead) / (n - 1)
    m = np.full(n, 1.0 / np.sqrt(n))
    return rest * np.eye(n) + (lead - rest) * np.outer(m, m)


def one_spike_gap_per_entry(gamma: float, h_q: float, n: int, q1: float) -> float:
    """Common entry of the rank-one confounding gap in the one-spike model."""
    if q1 <= 0.0:
        raise ValueError("q1: expected a positive leading eigenvalue")
    return gamma * h_q / (n * q1)


def sharp_offdiag_interval(
    a_off: float,
    n: int,
    q1: float,
    h_q: float,
    gamma_lo: float,
    gamma_hi: float,
) -> tuple[float, float]:
    """Sharp identified interval for the structural off-diagonal."""
    if gamma_lo > gamma_hi:
        raise ValueError("gamma_lo: expected gamma_lo <= gamma_hi")
    a = a_off - one_spike_gap_per_entry(gamma_hi, h_q, n, q1)
    b = a_off - one_spike_gap_per_entry(gamma_lo, h_q, n, q1)
    return (a, b) if a <= b else (b, a)


def feasible_gamma_range(
    n: int,
    s_q: float,
    s_r: float,
    rho: float,
    d: float,
    o: float,
) -> tuple[float, float]:
    """Range of factor loadings consistent with positive-semidefinite residuals."""
    q1 = n * s_q
    r1 = n * s_r
    c1 = rho * np.sqrt(r1 * q1)
    lam1 = d + (n - 1) * o
    hi = float(c1 - lam1 * q1)
    lo = float(-hi) if hi > 0.0 else float(hi)
    return (min(lo, hi), max(lo, hi))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --locked --extra dev pytest tests/test_identification.py -v`
Expected: all tests PASS.

- [ ] **Step 5: Update the derivation with the realized closed form**

If the numerically feasible `γ` range differs from the Section 3 algebra,
**fix the derivation, not the test**, and record the discrepancy in
`SPECIFICATION_LOG.md`.

- [ ] **Step 6: Commit**

```bash
git add src/xid/models/identification.py tests/test_identification.py
git commit -m "Compute sharp cross-impact bounds in the one-spike geometry"
```

---

### Task 5: The diagonal-plus-rank-K diagnostic

**Files:**
- Create: `src/xid/models/rank_diagnostic.py`
- Create: `tests/test_rank_diagnostic.py`

**Interfaces:**
- Produces, for Tasks 6–7:
  - `psi_k(a: np.ndarray, k: int, iters: int = 500, tol: float = 1e-14) -> float`
  - `decompose(a, k, iters, tol) -> tuple[np.ndarray, np.ndarray]` returning
    `(diagonal_part, rank_k_part)`

The algorithm is alternating projection: hold `R` fixed and set
`D = diag(A − R)`; hold `D` fixed and set `R` to the rank-`K` truncated SVD of
`A − D`. Each half-step is the exact Frobenius-norm minimizer over its block,
so the objective is nonincreasing and bounded below, hence convergent.

- [ ] **Step 1: Write the failing test**

```python
import numpy as np
import pytest

from xid.models.rank_diagnostic import decompose, psi_k

N, K = 30, 3


def _diag_plus_rank_k(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    d = np.diag(rng.uniform(0.2, 0.4, N))
    g = rng.normal(size=(N, K)) @ rng.normal(size=(K, N)) * 0.05
    return d + g


def test_exact_structure_gives_zero_statistic() -> None:
    assert psi_k(_diag_plus_rank_k(1729), K) < 1e-8


def test_statistic_increases_with_structural_perturbation() -> None:
    rng = np.random.default_rng(1729)
    base = _diag_plus_rank_k(1729)
    pert = rng.normal(size=(N, N))
    pert -= np.diag(np.diag(pert))
    pert /= np.linalg.norm(pert)
    values = [psi_k(base + eps * pert, K) for eps in (0.0, 0.01, 0.05, 0.1, 0.2)]
    assert all(a < b for a, b in zip(values, values[1:]))


def test_statistic_is_permutation_invariant() -> None:
    rng = np.random.default_rng(9191)
    a = _diag_plus_rank_k(1729) + 0.05 * rng.normal(size=(N, N))
    perm = rng.permutation(N)
    assert abs(psi_k(a, K) - psi_k(a[np.ix_(perm, perm)], K)) < 1e-12


def test_decompose_reconstructs_within_residual() -> None:
    a = _diag_plus_rank_k(1729)
    d, r = decompose(a, K)
    assert np.linalg.norm(a - d - r) < 1e-8
    assert np.linalg.matrix_rank(r) <= K


def test_rejects_rank_larger_than_dimension() -> None:
    with pytest.raises(ValueError, match="k"):
        psi_k(_diag_plus_rank_k(1729), N + 1)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --locked --extra dev pytest tests/test_rank_diagnostic.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'xid.models.rank_diagnostic'`.

- [ ] **Step 3: Write minimal implementation**

```python
"""Diagonal-plus-rank-K specification diagnostic.

Under the no-feedback confounding model with ``K`` latent factors and a
diagonal structural impact matrix, the population regression coefficient matrix
is exactly diagonal plus a rank-``K`` term. The statistic below measures the
relative Frobenius distance from that set.
"""

from __future__ import annotations

import numpy as np

__all__ = ["decompose", "psi_k"]


def _validate(a: np.ndarray, k: int) -> int:
    if a.dtype != np.float64:
        raise ValueError("a: expected float64")
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("a: expected a square matrix")
    if not np.isfinite(a).all():
        raise ValueError("a: expected finite entries")
    if k < 0 or k > a.shape[0]:
        raise ValueError("k: expected 0 <= k <= matrix dimension")
    return a.shape[0]


def decompose(
    a: np.ndarray,
    k: int,
    iters: int = 500,
    tol: float = 1e-14,
) -> tuple[np.ndarray, np.ndarray]:
    """Alternating-projection split of ``a`` into diagonal and rank-``k`` parts."""
    _validate(a, k)
    r = np.zeros_like(a)
    previous = np.inf
    for _ in range(iters):
        d = np.diag(np.diag(a - r))
        residual = a - d
        u, s, vt = np.linalg.svd(residual)
        s_trunc = s.copy()
        s_trunc[k:] = 0.0
        r = (u * s_trunc) @ vt
        current = float(np.linalg.norm(a - d - r))
        if previous - current <= tol:
            break
        previous = current
    return np.diag(np.diag(a - r)), r


def psi_k(a: np.ndarray, k: int, iters: int = 500, tol: float = 1e-14) -> float:
    """Relative distance from the diagonal-plus-rank-``k`` set."""
    _validate(a, k)
    scale = float(np.linalg.norm(a - np.diag(np.diag(a))))
    if scale == 0.0:
        return 0.0
    d, r = decompose(a, k, iters, tol)
    return float(np.linalg.norm(a - d - r) / scale)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --locked --extra dev pytest tests/test_rank_diagnostic.py -v`
Expected: all tests PASS. If the monotonicity test fails, the alternating
projection has stalled in a local minimum — increase `iters` and record the
change; do not weaken the assertion to a non-strict inequality.

- [ ] **Step 5: Run the locked gate**

Run: `make check`

- [ ] **Step 6: Commit**

```bash
git add src/xid/models/rank_diagnostic.py tests/test_rank_diagnostic.py
git commit -m "Add a falsifiable diagnostic for structural cross-impact"
```

---

### Task 6: Deterministic exhibit generator

**Files:**
- Create: `src/xid/exhibits.py`
- Create: `tests/test_exhibits.py`
- Create: `docs/pre_results/generated/exhibits.json`
- Create: `docs/pre_results/generated/fig_bounds.tex`
- Create: `docs/pre_results/generated/fig_diagnostic.tex`
- Modify: `.gitignore`
- Modify: `Makefile`

**Interfaces:**
- Consumes: `identification` and `rank_diagnostic` from Tasks 3–5.
- Produces: `python -m xid.exhibits --out docs/pre_results/generated` writing
  `exhibits.json` plus TikZ coordinate fragments, byte-identically on repeat.

- [ ] **Step 1: Write the failing test**

```python
import json
import subprocess
import sys
from pathlib import Path

GENERATED = Path("docs/pre_results/generated")


def test_exhibits_are_byte_identical_on_regeneration(tmp_path: Path) -> None:
    for _ in range(2):
        subprocess.run(
            [sys.executable, "-m", "xid.exhibits", "--out", str(tmp_path)],
            check=True,
        )
    for name in ("exhibits.json", "fig_bounds.tex", "fig_diagnostic.tex"):
        assert (tmp_path / name).read_bytes() == (GENERATED / name).read_bytes()


def test_exhibit_keys_are_complete() -> None:
    payload = json.loads((GENERATED / "exhibits.json").read_text())
    for key in (
        "spurious_offdiag_max",
        "own_impact_min",
        "own_impact_max",
        "gap_ranks",
        "sharp_interval",
        "psi_null",
        "psi_curve",
        "published_pairwise_correlation",
    ):
        assert key in payload


def test_spurious_offdiag_is_same_order_as_own_impact() -> None:
    payload = json.loads((GENERATED / "exhibits.json").read_text())
    assert payload["spurious_offdiag_max"] > 0.5 * payload["own_impact_min"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --locked --extra dev pytest tests/test_exhibits.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'xid.exhibits'`.

- [ ] **Step 3: Write the implementation**

`src/xid/exhibits.py` must:

- Use only test seed `1729`.
- Compute, and write to `exhibits.json` with `sort_keys=True, indent=2` and a
  trailing newline:
  - `gap_ranks`: the four observed ranks `[3, 4, 5, 30]` with their bounds.
  - `spurious_offdiag_max`, `own_impact_min`, `own_impact_max`: the diagonal-truth
    fixture headline numbers.
  - `sharp_interval`: the one-spike closed-form interval at the registered
    Capponi–Cont point, plus a boolean `contains_zero`.
  - `psi_null`: the statistic at exact diagonal-plus-rank-`K` structure.
  - `psi_curve`: `[[eps, psi], ...]` over the frozen grid
    `[0.0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3]`.
  - `published_pairwise_correlation`: `one_spike_covariance(30, 0.2827)[0,1]`.
- Round every emitted float with `format(x, ".10g")` so the JSON is
  platform-stable, mirroring the ten-decimal convention already used for the G1
  target hash.
- Write `fig_bounds.tex` and `fig_diagnostic.tex` as `\def`-guarded TikZ
  `plot coordinates {...}` fragments that the manuscript `\input`s.

- [ ] **Step 4: Generate and inspect the artifacts**

```bash
uv run python -m xid.exhibits --out docs/pre_results/generated
cat docs/pre_results/generated/exhibits.json
```

- [ ] **Step 5: Allowlist the generated directory**

Add to `.gitignore` (the `output/` and `results/` rules must not swallow it):

```
!docs/pre_results/generated/
```

Add to `Makefile`:

```make
exhibits:
	uv run --locked python -m xid.exhibits --out docs/pre_results/generated
	git diff --exit-code -- docs/pre_results/generated
```

- [ ] **Step 6: Run tests and the locked gate**

Run: `uv run --locked --extra dev pytest tests/test_exhibits.py -v && make check`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/xid/exhibits.py tests/test_exhibits.py \
        docs/pre_results/generated .gitignore Makefile
git commit -m "Generate every manuscript number from committed deterministic code"
```

---

### Task 7: Published-source consistency exhibit

**Files:**
- Modify: `src/xid/exhibits.py`
- Modify: `tests/test_exhibits.py`
- Modify: `docs/pre_results/generated/exhibits.json`

**Interfaces:**
- Consumes: only numbers already recorded in `docs/G2_SOURCE_AUDIT.md`.
- Produces: `published_control_shift` exhibit block.

The exhibit: Capponi–Cont report a mean cross-coefficient of `0.032` before PC1
control and `-0.039` after, with the negative fraction moving from `23.09%` to
`84.46%`. Theorem 2 says a single factor control moves every cross-coefficient
along **one** rank-one direction, which in the permutation-invariant geometry
is a **common additive shift**. Compute the implied shift `-0.071` and check it
against the shift the one-spike model predicts at the published
`(s_q, s_r, ρ) = (0.2827, 0.32, 0.8726)`.

- [ ] **Step 1: Write the failing test**

```python
def test_published_control_shift_block_is_present() -> None:
    payload = json.loads((GENERATED / "exhibits.json").read_text())
    block = payload["published_control_shift"]
    assert block["reported_before"] == 0.032
    assert block["reported_after"] == -0.039
    assert abs(block["reported_shift"] - (-0.071)) < 1e-12
    assert "model_implied_shift" in block
    assert "relative_discrepancy" in block
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --locked --extra dev pytest tests/test_exhibits.py -k published -v`
Expected: FAIL — `KeyError: 'published_control_shift'`.

- [ ] **Step 3: Implement the exhibit**

Add the block to `src/xid/exhibits.py`. Every emitted key carries a
`"scope"` string with the exact value:

```
"conditional analytic exhibit at published summary statistics; not an estimate of any market's impact matrix"
```

- [ ] **Step 4: Regenerate, test, and gate**

```bash
uv run python -m xid.exhibits --out docs/pre_results/generated
uv run --locked --extra dev pytest tests/test_exhibits.py -v
make check
```

- [ ] **Step 5: Record the outcome honestly**

Whatever the discrepancy is, it goes in the manuscript. If the model-implied
shift matches the published shift closely, that is a striking consistency
result. If it does not, report the mismatch and what it rules out. **Do not
tune the one-spike convention to improve the match.** Record the observed value
in `SPECIFICATION_LOG.md` before writing any manuscript prose about it.

- [ ] **Step 6: Commit**

```bash
git add src/xid/exhibits.py tests/test_exhibits.py docs/pre_results/generated
git commit -m "Evaluate the rank prediction against published commonality summaries"
```

---

### Task 8: Bibliography

**Files:**
- Create: `docs/pre_results/references.bib`

**Interfaces:**
- Produces: BibTeX keys consumed by Task 9.

- [ ] **Step 1: Carry over all 18 existing entries**

Convert every `\bibitem` currently inline in the manuscript into a BibTeX entry
with the same key (`Kyle1985`, `Hasbrouck1991`, `ContKukanovStoikov2014`,
`XuGouldHowison2019`, `HasbrouckSeppi2001`, `BenzaquenEtAl2017`,
`CapponiCont2020`, `ContCucuringuZhang2023`, `SchneiderLillo2016`,
`StockWatson2002`, `BaiNg2006`, `MiaoEtAl2018`, `Tibshirani1996`,
`KockCallot2015`, `BabiiEtAl2022`, `White2000`, `Hansen2005`,
`RomanoWolf2005`).

- [ ] **Step 2: Add the partial-identification cluster**

This is the framing that makes the paper legible to econometricians and is
currently missing entirely: Manski (2003, *Partial Identification of Probability
Distributions*); Manski & Tamer (2002, *Econometrica* 70(2):519–546); Tamer
(2010, *Annual Review of Economics* 2:167–195); Chernozhukov, Hong & Tamer
(2007, *Econometrica* 75(5):1243–1284); Ho & Rosen (2017, *Advances in Economics
and Econometrics*).

- [ ] **Step 3: Add the market-impact cluster**

Almgren & Chriss (2001); Gatheral (2010, *Quantitative Finance* 10(7):749–759);
Bouchaud, Farmer & Lillo (2009); Tóth et al. (2011, *Physical Review X*
1:021006); Donier et al. (2015); Bacry et al. (2015, *Market Microstructure and
Liquidity*); Mastromatteo, Tóth & Bouchaud (2014); Bucci et al. (2020,
cross-impact); Obizhaeva & Wang (2013, *Journal of Financial Markets*
16(1):1–32).

- [ ] **Step 4: Add the commonality and liquidity cluster**

Chordia, Roll & Subrahmanyam (2000, *JFE* 56(1):3–28); Korajczyk & Sadka (2008,
*JFE* 87(1):45–72); Pasquariello & Vega (2015, *Journal of Financial and
Quantitative Analysis*); Karolyi, Lee & van Dijk (2012, *JFE* 105(1):82–112).

- [ ] **Step 5: Add the factor-model and measurement-error cluster**

Chamberlain & Rothschild (1983, *Econometrica* 51(5):1281–1304); Bai (2003,
*Econometrica* 71(1):135–171); Onatski (2010, *Review of Economics and
Statistics* 92(4):1004–1016); Ahn & Horenstein (2013, *Econometrica*
81(3):1203–1227); Gagliardini, Ossola & Scaillet (2016, *Econometrica*
84(3):985–1046).

- [ ] **Step 6: Add the reproducibility and preregistration cluster**

Nosek et al. (2018, *PNAS* 115(11):2600–2606); Harvey, Liu & Zhu (2016, *Review
of Financial Studies* 29(1):5–68); Harvey (2017, *Journal of Finance* 72(4):
1399–1440); Fama & French (2010) or Bailey & López de Prado (2014) on
backtest overfitting.

- [ ] **Step 7: Verify every DOI resolves**

For each entry with a DOI, confirm the DOI string is well-formed and matches
the cited title. Do **not** invent DOIs. If a DOI cannot be confirmed, cite the
work without one rather than guessing.

- [ ] **Step 8: Commit**

```bash
git add docs/pre_results/references.bib
git commit -m "Broaden the reference base to the surrounding literatures"
```

---

### Task 9: Manuscript rewrite

**Files:**
- Modify: `docs/pre_results/xid_pre_results_manuscript.tex`

**Interfaces:**
- Consumes: `docs/pre_results/generated/*.tex`, `references.bib`, and every
  exhibit value from Tasks 6–7.

- [ ] **Step 1: Add the page furniture**

In the preamble:

```latex
\pdfoutput=1
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\small Preprint. Under review.}
\fancyfoot[R]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.4pt}
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\small Preprint. Under review.}%
  \fancyfoot[R]{\small\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0.4pt}%
}
```

The redefinition of `plain` is what puts the footer on page 1. Verify page 1
visually in Step 9 — this is the single most common way this requirement is
silently missed.

- [ ] **Step 2: Convert the author block to a dagger footnote**

```latex
{\large Mehmet Demir G\"uven\textsuperscript{\dag}\par}
\vspace{2pt}
{\normalsize Department of Computer Science, ETH Z\"urich\par}
```

with, after the title block,

```latex
\footnotetext[0]{\textsuperscript{\dag}\,Independent research. ETH Z\"urich did
not fund, sponsor, approve, or endorse this work. The affiliation records the
author's status as a student only, and the views expressed are the author's
alone.}
```

Use `\renewcommand{\thefootnote}{\fnsymbol{footnote}}` scoping if `[0]` does not
typeset; the requirement is a visible dagger-marked footnote on page 1.

- [ ] **Step 3: Rewrite the abstract around the new result**

The abstract must, in order: (1) state that cross-asset return-on-flow
coefficients are read as structural impact; (2) state the new theorem — the
confounding gap has rank at most `K + rank(B)`, so with `K` factors and no
feedback a diagonal truth implies the *entire* estimated cross-impact matrix is
diagonal-plus-rank-`K`; (3) give the headline number — spurious off-diagonals
reaching the same order of magnitude as genuine own-impact under zero true
cross-impact; (4) state the partial-identification consequence; (5) state the
`ψ_K` diagnostic and its polarity; (6) report the completed `T=10^7`
known-truth verification; (7) state that the empirical premise test is
registered, not reported. Keep it under 1,920 characters so it fits the arXiv
metadata field verbatim.

- [ ] **Step 4: Rewrite the introduction with the published sign flip as the hook**

Open with the concrete puzzle from `docs/G2_SOURCE_AUDIT.md`: adding a single
principal-component control moves the mean cross-coefficient from `+0.032` to
`-0.039` and the negative fraction from `23.09%` to `84.46%`. Then ask which
reading is right, and state that the paper's answer is that *neither* is
identified. This is the first-impression content that decides the reader's
verdict; it must fit on page 1.

- [ ] **Step 5: Insert the new theory section after Theorem 1**

Add, with full proofs in the appendix: Theorem 2 (rank bound), Corollary
(diagonal truth implies diagonal-plus-rank-`K`), Proposition 3 (identified set),
Proposition 4 (sharp one-spike interval), and Definition + Proposition 5 (the
`ψ_K` diagnostic and its population zero). Every displayed equation gets a
label; the first equation of the paper should be the structural system, which
is already the strongest opening equation available.

- [ ] **Step 6: Add the numerical-verification subsection**

Report the Task 3–5 verification as a table: predicted rank bound vs. observed
rank for `rank(B) ∈ {0,1,2,30}`; `ψ_K` at exact structure; the `ψ_K` curve; the
permutation-invariance residual. Label these as deterministic algebraic checks
at test seed `1729`, with no interval method applicable.

- [ ] **Step 7: Add the published-consistency section**

Present the Task 7 exhibit. Carry the exact scope sentence from Task 7 Step 3
into the caption and the body. State plainly that this is a conditional
analytic exhibit at published summary statistics.

- [ ] **Step 8: Compress the G2 protocol section and keep every existing limitation**

The registered-protocol material stays but moves later and tightens. Every
limitation currently in the manuscript is retained, plus new ones: `ψ_K = 0`
does not prove diagonality; the rank bound is an inequality, so a high observed
rank does not by itself prove structural cross-impact if `K` is misspecified;
the sharp interval is conditional on the one-spike convention.

- [ ] **Step 9: Switch to `\bibliography` and build**

```bash
tectonic -X compile docs/pre_results/xid_pre_results_manuscript.tex \
  --outdir output/pdf
```

Then verify page count is 9–11 and that the footer appears on page 1:

```bash
uv run python -c "
import re
d = open('output/pdf/xid_pre_results_manuscript.pdf','rb').read()
print('pages:', d.count(b'/Type /Page') - d.count(b'/Type /Pages'))
"
```

- [ ] **Step 10: Commit**

```bash
git add docs/pre_results/xid_pre_results_manuscript.tex output/pdf
git commit -m "Lead the manuscript with the identification result"
```

---

### Task 10: README rewrite

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Restructure to mirror the paper**

Keep the existing section skeleton but insert the new theory as Section 3, with
the rank theorem stated in display math, the headline spurious-off-diagonal
number, the partial-identification corollary, and the `ψ_K` definition. Update
the abstract to match the manuscript abstract.

- [ ] **Step 2: Add the dagger footnote text under the author line**

Mirror the manuscript wording exactly.

- [ ] **Step 3: Update every stale number**

Test count, file counts, and gate status must match the state after Task 6.
Re-run `make check` and copy the observed values rather than editing by hand.

- [ ] **Step 4: Update the evidence map**

Add rows for `identification.py`, `rank_diagnostic.py`, `exhibits.py`, the
generated exhibits, and the new derivation.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Make the README state the identification result first"
```

---

### Task 11: Repository authorship hygiene

**Files:**
- Create: `RESEARCH_PROTOCOL.md`
- Delete: `AGENTS.md`
- Modify: any file referencing `AGENTS.md`

- [ ] **Step 1: Find every reference**

```bash
grep -rn "AGENTS.md" --include="*.md" --include="*.py" --include="*.toml" . \
  | grep -v "^./tmp/"
```

- [ ] **Step 2: Write `RESEARCH_PROTOCOL.md`**

Port the research invariants verbatim — they are good science and worth
keeping. Rewrite the framing as the author's own standing operating discipline.
Remove: the phrase "operating contract" in the agent sense, "the principal's
operating brief", "Lore protocol", the session-start/session-end instruction
block, and any second-person instruction to an executing agent. Replace with a
first-person or impersonal statement of the project's research rules.

- [ ] **Step 3: Delete `AGENTS.md` and update references**

```bash
git rm AGENTS.md
```

Update `README.md` and any doc that pointed at it.

- [ ] **Step 4: Re-scan for traces**

```bash
grep -rniE "claude|anthropic|\bagent\b|assistant|language model|\bLLM\b|copilot|chatgpt|openai|generated with|co-authored" \
  --include="*.md" --include="*.tex" --include="*.py" --include="*.toml" \
  --include="*.yml" . | grep -v "^./tmp/" | grep -v "^./.venv"
```

Expected: no hits outside legitimate research vocabulary. Note that
`git log --format='%an %ae'` already shows only the author's own identity, and
`.omx/` is already gitignored — verify both remain true.

- [ ] **Step 5: Commit**

```bash
git add RESEARCH_PROTOCOL.md README.md
git rm AGENTS.md
git commit -m "State the research protocol in the author's own voice"
```

---

### Task 12: arXiv submission package

**Files:**
- Create: `scripts/build_paper.sh`
- Create: `docs/ARXIV_SUBMISSION.md`
- Modify: `Makefile`

- [ ] **Step 1: Write `scripts/build_paper.sh`**

The script must: compile the manuscript twice plus BibTeX so `.bbl` is current;
assemble `output/arxiv/` containing the `.tex`, the generated `.bbl` (arXiv does
**not** run BibTeX), every `\input`-ed fragment from
`docs/pre_results/generated/`, and nothing else; produce
`output/arxiv.tar.gz`; and print the tarball size and file list. Use `set -euo
pipefail`.

- [ ] **Step 2: Add Makefile targets**

```make
paper:
	tectonic -X compile docs/pre_results/xid_pre_results_manuscript.tex --outdir output/pdf

arxiv: exhibits paper
	bash scripts/build_paper.sh
```

- [ ] **Step 3: Write `docs/ARXIV_SUBMISSION.md`**

Record, as a checklist the author can follow without re-deriving anything:

- **Categories.** Primary `q-fin.TR` (Trading and Market Microstructure).
  Cross-list `q-fin.ST` (Statistical Finance) and `econ.EM` (Econometrics).
- **Endorsement.** arXiv requires endorsement for a first submission to
  `q-fin`. Submitting from the ETH Zürich institutional email address normally
  triggers automatic endorsement; if it does not, an endorsement request must go
  to an existing `q-fin` author. This is a real prerequisite and is flagged here
  because it can block submission on the day of upload.
- **License.** CC BY 4.0, matching `LICENSE-PREPRINT.md`.
- **Abstract field.** Paste the manuscript abstract; must be plain text under
  1,920 characters with no LaTeX macros other than inline math.
- **Source upload.** Upload the tarball, not the PDF. arXiv rebuilds from
  source. Include the `.bbl`. Do not include `.bib`, `.aux`, `.log`, `.out`,
  `.synctex.gz`, or the `tmp/` bundle.
- **`\pdfoutput=1`** must appear in the first five lines of the `.tex`.
- **Fonts and packages.** Every package used must be in TeX Live; `fancyhdr`,
  `tikz`, `booktabs`, `microtype`, `hyperref` all are.
- **Metadata.** Title, single author `Mehmet Demir Güven`, comments field
  recording page count and that this is a pre-results preprint, MSC/JEL codes
  (`JEL: G14, C58, C18`).
- **Pre-upload verification.** Extract the tarball into an empty directory and
  compile there with `latexmk -pdf`. If that fails, arXiv will fail.

- [ ] **Step 4: Verify the tarball compiles from scratch**

```bash
make arxiv
mkdir -p /tmp/arxivcheck && tar xzf output/arxiv.tar.gz -C /tmp/arxivcheck
cd /tmp/arxivcheck && latexmk -pdf *.tex
```

If `latexmk` is unavailable, compile with `tectonic` in the extracted directory
and record that arXiv's own `latexmk` path was not exercised locally.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_paper.sh docs/ARXIV_SUBMISSION.md Makefile
git commit -m "Package the preprint for source-level submission"
```

---

### Task 13: Ledger update, final gate, and citation projection

**Files:**
- Modify: `STATE.md`, `SPECIFICATION_LOG.md`, `DECISIONS.md`
- Create: `docs/redteam/THEORY_EXTENSION.md`

- [ ] **Step 1: Write the red-team memo**

Attack the new theory in `docs/redteam/THEORY_EXTENSION.md`. At minimum
address: the rank bound is an inequality and `K` is unknown in practice, so a
misspecified `K` breaks the diagnostic in both directions; the alternating
projection may find a local rather than global minimum, so `ψ_K` is an upper
bound on the true distance; the identified set derivation assumes `B=0`, which
the general theorem does not; the one-spike convention is a maximum-entropy
choice and the sharp interval inherits that conditionality; the published
summary statistics carry no inferential intervals, so the consistency exhibit
cannot be given a p-value. Record the strongest objection that remains
unresolved.

- [ ] **Step 2: Add the `C0019` entry to `SPECIFICATION_LOG.md`**

Follow the `C0018` format exactly: registered date, scope, prediction before
tests, observed RED (the recorded failure output from Tasks 3, 5, 6, 7),
observed GREEN, status, intervals, multiple-testing count, access statement
confirming registered seeds and market data remain untouched.

- [ ] **Step 3: Update `STATE.md`**

Update: `Last updated`, the current-gate paragraph (G2 still open and
executable-red — the theory extension does **not** change that), session
objective, new evidence bullets, in-flight items, and the cold-resume next
action. Do not overstate: the theory extension is derivation and software
evidence, not a G2 result.

- [ ] **Step 4: Run the complete gate**

```bash
make check && make exhibits && make arxiv
```

- [ ] **Step 5: Write the citation projection**

Add a short, honest projection to `docs/ARXIV_SUBMISSION.md`. Ground it in
comparables rather than optimism:

- Base rates: `q-fin.TR` preprints receive a median of roughly 0–2 citations in
  three years; the field's well-cited empirical cross-impact papers
  (Cont–Kukanov–Stoikov 2014; Benzaquen et al. 2017; Cont–Cucuringu–Zhang 2023)
  sit in the tens to low hundreds after five-plus years, and those are the
  ceiling for this niche, not the expectation.
- Factors that raise the estimate here: a clean named theorem with a
  reusable diagnostic; a partial-identification framing that reaches
  econometricians as well as microstructure researchers; a direct, checkable
  engagement with the most-cited recent paper in the niche; and full public
  code.
- Factors that lower it: sole authorship without an established citation
  network; no institutional promotion; no empirical result yet, which is the
  single largest discount, since this literature cites empirical findings far
  more than identification critiques.
- Honest projection: **3–10 citations within three years** in the current
  pre-results form, rising to roughly **15–40** if and when the G2 premise test
  and an empirical gate close and the paper is resubmitted with results. Claims
  above that range are not supportable for a first solo preprint in this niche,
  and the plan does not make them.

- [ ] **Step 6: Commit**

```bash
git add STATE.md SPECIFICATION_LOG.md DECISIONS.md docs/redteam/THEORY_EXTENSION.md docs/ARXIV_SUBMISSION.md
git commit -m "Record the theory extension in the project ledgers"
```

- [ ] **Step 7: Push and confirm hosted CI**

```bash
git push origin main
gh run list --limit 1
```

Wait for the run to complete and record its ID and conclusion in `STATE.md`.

---

## Self-Review

**Spec coverage.**

| Request | Task |
| --- | --- |
| Research-paper-quality README | 10 |
| Real research paper for arXiv | 9 |
| Dagger footnote, ETHZ non-endorsement | 9 (Step 2), 10 (Step 2) |
| `Preprint. Under review.` on every page | 9 (Step 1, verified Step 9) |
| No AI traces | 11, plus Global Constraints |
| Competitive / high-impact | 1–7 (the new theory is the entire answer) |
| Storyline, theorems, math, page limit, citations, figures | 8, 9 |
| Citation projection | 13 (Step 5) |
| Submission-ready package | 12 |
| Plan before proceeding | this document |

**Placeholder scan.** No `TBD`, no "handle edge cases", no "similar to Task N".
Every code step carries runnable code. Task 8's bibliography entries are named
individually rather than "add more references".

**Type consistency.** `psi_k` and `decompose` share the `(a, k, iters, tol)`
signature across Tasks 5–7. `one_spike_covariance(n, share)`,
`sharp_offdiag_interval(a_off, n, q1, h_q, gamma_lo, gamma_hi)`, and
`feasible_gamma_range(n, s_q, s_r, rho, d, o)` are used in Tasks 4, 6, and 7
with identical names and argument order. `confounding_gap` and `numerical_rank`
are consistent between Tasks 3 and 6.

**Known risk.** Task 7's outcome is genuinely unknown before it runs. The plan
commits to reporting whatever the discrepancy is rather than tuning the model
to match. If the match is poor, the manuscript keeps the section and reports it
as a limitation of the one-spike convention; the paper's main contribution
(Tasks 1–5) does not depend on that exhibit.
