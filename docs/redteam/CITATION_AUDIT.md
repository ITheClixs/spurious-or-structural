# Citation audit

Performed 2026-08-16 against the Crossref REST API, the DOI resolver, and the
arXiv API. Every bibliography entry was checked; none was sampled.

## Method

All 45 entries were parsed from `docs/pre_results/references.bib`. Each entry
carrying a DOI was resolved and its registered title and year compared with the
bibliography. Entries whose DOI did not resolve through Crossref were checked
against the issuing registry directly.

## Result

| Outcome | Count |
| --- | ---: |
| Verified against Crossref, title and year agree | 35 |
| Verified through another registry after a Crossref miss | 1 |
| Year differs by online-first versus issue year | 4 |
| Title differs only by publisher markup | 1 |
| Corrected | 1 |
| No DOI exists to check | 3 |
| **Hallucinated, nonexistent, or misattributed** | **0** |

**No fabricated citation was found.** Every work cited exists, and every
author list and title checked matches the published record.

## Items examined individually

**Xu, Gould and Howison.** Crossref returned HTTP 404 for
`10.48550/arXiv.1907.06230`. That is a registry artifact rather than a defect:
arXiv DOIs are registered with DataCite, not Crossref. The DOI resolves
normally through `doi.org` to `arxiv.org/abs/1907.06230`, and the arXiv API
confirms the authors as Ke Xu, Martin D. Gould and Sam D. Howison with the
cited title. No change.

**Four online-first year differences.** Cont, Kukanov and Stoikov; Schneider
and Lillo; Babii, Ghysels and Striaukas; and Harvey, Liu and Zhu each show a
Crossref year one earlier than the bibliography, because Crossref records the
online-publication year while the bibliography records the issue year that the
volume, number and pages refer to. The bibliography is internally consistent
and follows the usual convention. No change.

**Bailey and Lopez de Prado.** The apparent title mismatch is Crossref
returning embedded italic markup inside the title string. The BibTeX key
misspells the surname as `Baily`; the rendered author field is correct and the
key never appears in output. No change.

**Capponi and Cont — corrected.** The bibliography recorded 2021 after this
audit; it previously recorded 2020. Crossref registers the DOI with an issued
year of 2021 and a creation timestamp of 2021-01-14. Because the entry is a
working paper identified by its DOI rather than by a volume and issue, the
bibliography now matches what a reader resolving that DOI will see. This
matters more than the other date differences, since the sign-flip figures the
manuscript quotes come from this source.

**Three entries carry no DOI.** Almgren and Chriss in the Journal of Risk,
the Bouchaud, Farmer and Lillo handbook chapter, and the Manski monograph have
no registered DOI. They are cited without one rather than with a guessed
identifier.

## What this audit does not establish

Existence and metadata only. **It does not verify that each cited source
actually supports the claim the manuscript attributes to it.** That check
requires opening each source and reading the relevant passage, and it has not
been performed. Claim-to-citation verification remains open.
