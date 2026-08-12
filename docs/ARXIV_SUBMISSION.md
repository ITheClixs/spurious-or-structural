# arXiv submission

Everything needed to submit the preprint, in the order the submission form asks
for it. Build the package first:

```bash
make arxiv
```

This regenerates the exhibits, fails if any committed exhibit has drifted,
compiles with the bibliography, writes `output/pdf/`, and produces
`output/arxiv.tar.gz`.

## 1. Pre-upload verification

Never upload without extracting the tarball into an empty directory and
building it there. If that fails, arXiv fails.

```bash
rm -rf /tmp/arxivcheck && mkdir -p /tmp/arxivcheck/out
tar xzf output/arxiv.tar.gz -C /tmp/arxivcheck
cd /tmp/arxivcheck && latexmk -pdf xid_pre_results_manuscript.tex
```

If TeX Live is not installed locally, `tectonic -X compile
xid_pre_results_manuscript.tex --outdir out` is an acceptable substitute; note
that it exercises XeTeX rather than the pdfLaTeX path arXiv uses.

Last verified standalone build: **11 pages, 0 undefined references,
bibliography present, `Preprint. Under review.` on every page, dagger footnote
and affiliation disclaimer on page 1.**

## 2. Package contents

The tarball contains exactly:

| File | Purpose |
| --- | --- |
| `xid_pre_results_manuscript.tex` | The manuscript |
| `xid_pre_results_manuscript.bbl` | Formatted bibliography — **arXiv does not run BibTeX** |
| `references.bib` | Source bibliography, so local verification builds reproduce the same result |
| `generated/fig_bounds.tex` | Figure coordinates, generated |
| `generated/fig_diagnostic.tex` | Figure coordinates, generated |
| `generated/fig_psi_study.tex` | Size and power figure coordinates, generated |

No `.aux`, `.log`, `.out`, `.synctex.gz`, or `.pdf` ships. All figures are
inline TikZ/pgfplots, so there are no external image files.

**Upload the tarball, not the PDF.** arXiv rebuilds from source.

## 3. Categories

- **Primary:** `q-fin.TR` — Trading and Market Microstructure
- **Cross-list:** `q-fin.ST` — Statistical Finance
- **Cross-list:** `econ.EM` — Econometrics

The `econ.EM` cross-list is worth doing. The partial-identification result is
the part of this paper most legible to econometricians, and it is where the
citing audience beyond microstructure lives.

## 4. Endorsement — check this before submission day

arXiv requires **endorsement** for a first submission to `q-fin`. Submitting
from an ETH Zürich institutional email address normally triggers automatic
endorsement, because the domain is on arXiv's auto-endorse list. If it does
not, an endorsement request must be sent to an existing `q-fin` author, and
that can take days.

This is a real prerequisite and the most likely cause of a delayed upload.
Verify endorsement status by starting a submission before the paper is final.

## 5. Metadata

**Title**

```
Spurious or Structural? Low-Rank Confounding and Partial Identification of Cross-Asset Price Impact
```

**Authors**

```
Mehmet Demir Güven
```

**Abstract.** Paste the manuscript abstract as plain text. It is **1,590
characters**, within arXiv's 1,920-character limit. Inline math in `$...$` is
accepted; no custom macros survive, so `\rank` must be written out as `rank`
in the metadata field.

**Comments**

```
11 pages, 4 figures. Pre-results preprint: reports derivations and a
preregistered known-truth simulation; the empirical premise test is registered
but not reported. Code, preregistration, and ledgers at
https://github.com/ITheClixs/spurious-or-structural
```

**JEL codes:** `G14`, `C58`, `C18`

**MSC codes (optional):** `91G80`, `62P05`

**License:** CC BY 4.0, matching `LICENSE-PREPRINT.md`.

## 6. Technical notes

- `\pdfoutput=1` appears in the first lines, guarded so local XeTeX builds also
  work. arXiv's scanner reads the literal string; the guard does not hide it.
- Every package used (`amsmath`, `amssymb`, `amsthm`, `mathtools`, `booktabs`,
  `array`, `graphicx`, `microtype`, `xcolor`, `enumitem`, `caption`, `tikz`,
  `pgfplots`, `fancyhdr`, `hyperref`, `geometry`) is in TeX Live and available
  on arXiv.
- `\pgfplotsset{compat=1.16}` is pinned so a newer pgfplots on arXiv cannot
  change the rendering.
- The `]` character must never appear unbraced at brace level zero inside the
  `\twocolumn[...]` title block. It silently terminates the optional argument
  and produces a `Missing $ inserted` error far from the real cause. This bit
  once already, in the abstract.

## 7. After acceptance

Record the assigned identifier in `README.md` and `STATE.md`, and update the
citation block in both. Replace the "no arXiv identifier exists yet" note.

Version 0.2 is a pre-results preprint. A version 1.0 replacement is expected
once the registered premise test closes and the empirical gates open; that
replacement, not this one, is the paper the G8 gate governs.

---

## 8. Realistic citation projection

An honest projection, grounded in comparables rather than optimism. Written
before submission so it cannot be revised into whatever happens.

### Base rates

Cross-impact is a small, active niche. The well-cited empirical anchors —
Cont, Kukanov and Stoikov (2014); Benzaquen et al. (2017); Cont, Cucuringu and
Zhang (2023) — sit in the tens to low hundreds of citations after five or more
years. Those are the **ceiling for the subfield**, not an expectation for a new
entrant. The median `q-fin.TR` preprint receives roughly **0–2 citations in
three years**.

### What raises the estimate here

- A clean named theorem with a short proof. Reviewers and citers can restate
  `rank(G) ≤ K + rank(B)` in one line.
- A **usable test, not just a statistic.** `ψ_K` now ships with a bootstrap
  null, a factor-count rule fixed in advance, and a stated validity range.
  Methods that can be applied get cited; statistics without critical values do
  not.
- **An execution result with a memorable form.** "Only `K` of `N` trade
  directions are mispriced", "an index basket is wrong by 54% and a
  dollar-neutral basket by exactly zero", and "cost can be identified where the
  matrix is not" are quotable, and they reach the optimal-execution literature,
  which is considerably larger than the cross-impact niche.
- A **partial-identification framing** that reaches econometricians as well as
  microstructure researchers.
- Direct, checkable engagement with the most-cited recent paper in the niche,
  using its own published numbers.
- Fully public code where every reported number regenerates with one command.

### What lowers it

- **No empirical result yet.** This is by far the largest discount. This
  literature cites empirical findings far more than identification critiques.
- Sole authorship with no established citation network and no co-author
  circulation.
- No institutional promotion, no seminar circuit, no lab affiliation carrying
  the paper.
- Negative-result papers and "your estimator is unidentified" papers are
  structurally under-cited relative to their influence, because people who
  accept the argument often stop working on the problem rather than citing it.

### Projection

| Scenario | Three-year citations |
| --- | --- |
| Current pre-results form, no follow-up | **5–15** |
| Premise test closes, empirical gate opens, resubmitted with results | **20–50** |
| The `ψ_K` test or the immune-subspace result is adopted by another group | 50+, not the base case |

**Revised upward from an earlier 3–10 / 15–40.** The reason is specific rather
than optimistic: the paper stopped being only a critique. It now contains a
test a reader can run, with a validity range, and an execution consequence with
a closed-form schedule. Papers that hand over an instrument accumulate
citations from people who use it, which a pure identification critique does
not. The revision is roughly a factor of one and a half, not an order of
magnitude, because the largest discount is unchanged.

The middle row is the one worth working toward, and it depends on finishing G2
and G3 rather than on anything further that can be done to the manuscript.

Claims above this range are not supportable for a first solo preprint in a
niche this size, and are deliberately not made here.
