# Red-team memo — A028 theory extension

Written after implementation and before the ledgers were closed. The purpose is
to attack the new results, not to summarise them. Objections are recorded even
where they are unresolved.

## Scope of what is being attacked

Theorem 2 (`rank(G) <= K + rank(B)`), Corollary 2.1 (diagonal truth implies
diagonal-plus-rank-`K`), Proposition 3 (identified set), Proposition 4 (sharp
one-spike interval), Proposition 5 (`psi_K` population zero), and the published
summary-statistic exhibit.

## Objections that were raised and answered

**The rank theorem is trivial.** Partly true, and the manuscript says so: the
proof is three lines of rank subadditivity. Triviality of proof is not
triviality of consequence. The consequence — that a diagonal truth confines the
entire estimated cross-impact matrix to a low-dimensional set, which is
therefore refutable — does not appear in the cross-impact literature, and it
converts a qualitative worry into a testable restriction. The risk is
presentational, not mathematical: a reviewer may undervalue it because the
proof is short.

**This is just robust PCA / sparse-plus-low-rank.** The decomposition is
indeed standard, and the manuscript cites Chandrasekaran et al. and Candès and
Recht explicitly for it rather than leaving the reader to notice. The
contribution is the economic theorem that the confounding gap in a simultaneous
impact system *must* have this structure, with the rank tied to the latent
factor count and the feedback rank. The algorithm is borrowed; the restriction
is not.

**The identified set is trivially large because `Gamma` is unrestricted.** This
is the correct reading, not an objection to it. The point of Proposition 3 is
that nothing in the second moments restricts `Gamma` beyond
positive-semidefiniteness, which is exactly why the set is wide. If a reader
believes `Gamma` is restricted in practice, that restriction is an identifying
assumption they must state, which is the paper's thesis.

**`psi_K` uses a local optimum.** True. Alternating projection converges to a
stationary point, not a certified global minimum, so the computed statistic is
an upper bound on the true distance. This makes the test conservative in the
direction of failing to reject the pure-confounding null, which is the safe
direction for a test whose rejection supports the more interesting conclusion.
Stated in the derivation, the manuscript, and the module docstring.

## Unresolved objections

**1. `K` is unknown, and the diagnostic is not robust to getting it wrong.**
This is the strongest unresolved objection. The factor-count sweep shows
`psi_K` moving from `0.6396` at `K=1` to `0.0391` at `K=3` to `0.0250` at
`K=10` on the same matrix. An understated `K` manufactures rejection; an
overstated `K` destroys power. The elbow at the true `K` is suggestive but is
not a test, has no stated decision rule, and was observed on a single fixture
where the true `K` was known by construction. Nothing here establishes that the
elbow is visible when `K` is genuinely unknown or when factor strength is
heterogeneous. **Any empirical application of `psi_K` is currently
underdetermined for this reason.**

**2. There is no sampling distribution for `psi_K`.** **Resolved by A030,
partially.** A parametric plug-in bootstrap now supplies a critical value, and
a confirmatory study at a fresh seed found realised size `0.040` against a
nominal `0.05` at `T = 5000`, with power `0.870` against a Frobenius-`0.20`
alternative. `psi_K` is therefore a test, not merely a descriptive statistic.

What remains unresolved is the small-sample behaviour, and it is severe. At
`T = 500` the realised size is `0.267`, more than five times nominal, and it is
still `0.100` at `T = 2000`. The test is usable only above roughly
`T = 5 N^2`. The cause is diagnosed: the plug-in null is refitted to the noisy
estimate, so the low-rank fit absorbs part of the estimation error and the
bootstrap statistics are centred too low. The obvious remedy, inflating the
bootstrap error scale by the degrees-of-freedom factor `1.1347`, was tried and
**fails completely**, driving realised size to exactly zero at every sample
size and removing all power, because the bias is in the centre of the null
distribution rather than its scale. A centre correction such as a double
bootstrap would need its own registered design.

**3. The sharp interval inherits the one-spike convention entirely.**
Proposition 4 is exact given the permutation-invariant one-spike geometry and
isotropic residual spectrum. Both are declared maximum-entropy conventions, not
identified features of any exchange. A different residual spectrum gives a
different interval, and no bound is offered over the class of admissible
spectra. Corollary 4.1's sign non-identification is therefore conditional, and
a reader who rejects the convention is not obliged to accept the corollary.

**4. `B = 0` in the identification section.** Proposition 3 assumes no same-bin
feedback while Theorem 2 does not. The direction is favourable — feedback
enlarges the identified set — so the reported set is a subset of the true one
and the sign non-identification conclusion is conservative. But the paper does
not characterise the set under feedback, so the closed form does not extend.

**5. The published-evidence exhibit disagrees with itself.** The dispersion
implication is consistent with the reported figures; the distribution-shape
implication is not, with a gap of `0.1024` against a declared tolerance of
`0.05`. The stated explanation, loading heterogeneity beyond one common factor,
is plausible but untested. It is also convenient, since it is exactly the
explanation that preserves Theorem 2 while sacrificing only the one-spike
specialisation. A hostile reader is entitled to note that the surviving
implication is the weaker one: mean-shift-with-fixed-dispersion is consistent
with many mechanisms, not only rank-one confounding.

**6. The published figures carry no inferential intervals.** Capponi and Cont
report cross-sectional dispersion, not standard errors, and report to two
decimal places. The dispersion check therefore cannot be given a p-value, and
"the standard deviation is unchanged" is a statement about rounded numbers. The
exhibit supports consistency language only, and the manuscript uses only that
language.

**7. The rank bound cannot be inverted.** A high observed rank does not
establish structural cross-impact unless `K` is known, and a low observed rank
does not establish its absence, since a genuinely low-rank `Lambda` is
observationally indistinguishable from confounding. Both directions are stated
in the manuscript, but together they mean the theorem constrains interpretation
more than it enables inference.

## The main objection after A030

Objection 1 stands unchanged: the factor count is still assumed. A030 fixes a
selection rule in advance, the Ahn-Horenstein eigenvalue ratio on the
off-diagonal part, and that rule recovers the true count on the fixture. But no
study here establishes that it recovers the count when factor strength is
heterogeneous or when the true count is genuinely unknown, and the size and
power results are all conditional on the rule having selected correctly.

**Strongest unresolved objection, restated.** The test is valid only for large
samples relative to the parameter count, and both the validity threshold and
the factor-count rule were established on a single Gaussian, homoskedastic,
serially independent fixture. Market data violates every one of those
conditions. A dependent bootstrap and a heterogeneous-loading study are
required before `psi_K` can be applied empirically, and neither is attempted
here.

## Gate impact

None. A028 is derivation and deterministic software evidence. G2 remains open
and executable-red, no registered stream was opened, no registered seed was
accessed, and no external market data was touched. The sealed G2 configuration
digests were verified unchanged before and after the slice.
