# G2 smooth design-wrapper and response-label authority

Written after the C0004--C0006 repair was locally green and before the next
repair was implemented. No resource, validation, research, empirical,
evaluation, or holdout stream informed this diagnosis. The only stochastic
objects used by the estimator tests remain those drawn under test seed `1729`.

## 1. Diagnosed design-wrapper gap

Issuing `SmoothBaseDateMoments` is not sufficient if the contract cell builder
later multiplies a separately carried `SmoothDateDesign.x0` by the response.
Under the locally green boundary, a caller can construct

```text
forged_design = replace(
    issued_design,
    x0 = X_bad,
    source_receipt = issued_design.source_receipt,
    design_sha256 = issued_design.design_sha256,
    base_moments = issued_design.base_moments,
)
```

The issued base Gram still validates, while `X_bad'Y` is computed under the
copied digest. Aggregation can then combine the legitimate `X'X` with the
forged `X_bad'Y`. This is the same self-attestation class diagnosed in C0003,
one wrapper later in the chain.

## 2. Repair

The exact contract-built `SmoothDateDesign` object must receive its own weak,
module-owned issuance record. Its token binds the full source receipt, design
digest, `X0` payload, PCA diagnostic payload, and issued base-moment digest.
The contract cell builder validates this design receipt before reading `X0`.
A replaced, relabeled, content-mutated, or stale wrapper therefore fails even
when it reuses an otherwise legitimate issued base moment.

Every issued smooth-moment token also includes the array contract relevant to
safe reuse: exact `numpy.ndarray` runtime type, float64 dtype, shape,
C-contiguity, read-only state, finiteness, and C-order bytes. Toggling an issued
payload writable is therefore a receipt mismatch even before its bytes change.
An equality-compatible ndarray subclass is rejected because later transpose,
matrix multiplication, indexing, or array-protocol dispatch could otherwise
change computation without changing the hashed storage bytes.

The same rule applies to retained provenance values. Before a receipt enters
an issuance token or response-label comparison, the receipt, provenance,
response map, stream enum, and every scalar field must have their exact sealed
runtime types. A duck-typed or stateful equality-compatible object is not a
receipt: it could emit one payload during aggregate-token validation and a
different response map during the subsequent fit-label check.

Finally, every issued wrapper validates its complete scalar/container schema
before token projection: exact dataclass type; exact Python `int`, `float`, and
`str` fields; exact tuples rather than JSON-equivalent lists; exact tuple-member
types; and exact nested smooth dataclasses. Value-equal scalar subclasses are
not interchangeable because reflected arithmetic can dispatch through them.
For example, a `float` subclass can preserve `row_mass.hex()` while overriding
`1.0 / row_mass` during covariance extraction.

Issuance writes occur inline only in the exact public contract wrapper that has
just validated its live upstream object. The dimension-generic private kernels
never register an object merely because a caller supplied a constructible
`G2DateReceipt`, and there is no callable generic registrar. This preserves the
same raw-origin rule already fixed by D0054.

## 3. Response identity at the fit boundary

An aggregate retaining response-map metadata is not enough if the fit caller
can silently attach a different structural-cell label. Both high-level fits
must receive one exact expected `G2ResponseMapIdentity`. The structural
coordinates `(target_index, paper_recovery, phi)` must equal the common
response law retained by the issued aggregate, and the separately supplied fit
reliability must equal the expected identity's reliability. This check precedes
extraction or a linear solve.

Reliability is different: the frozen polynomial moments contain `f` and `e`
separately, so changing `R` changes only `tau=sqrt(1/R-1)` during extraction.
It does not change `Q`, `W`, `r`, `X0'X0`, `X0'Y`, or `Y'Y`. To preserve the
sealed reliability-frontier reuse rule, all smooth contract moments are minted
from the canonical `R=0.95` transformed-date anchor. Their complete date
receipt still records that anchor. A fit at another registered reliability
reuses the same aggregate, asserts the same structural response law, and binds
the requested reliability through its expected identity plus fit argument.

The expected identity is a label assertion, not a new estimator input. It does
not change any stored moment; it prevents a valid numeric aggregate from being
reported under the wrong target, recovery flag, AR law, or requested proxy
reliability without duplicating reliability-neutral artifacts.

## 4. Pre-run predictions

Before the repair, a deterministic one-date construction using a replaced
design wrapper and altered `X0` reaches contract cell-moment construction.
After the repair it fails as an unissued design before `X0'Y` is evaluated.
Likewise, changing a response-map label or an issued array's writable state
invalidates its receipt. A pure response-map validator accepts exact identity
and rejects any changed target, recovery flag, `phi`, or reliability. The
full successful issued-aggregate fit remains reserved for the separately
registered complete-panel recovery slice.

## 5. Stop condition

This repair ends when the new hostile tests, the prior 41 focused tests, the
full repository gate, and independent read-only review pass. It does not add a
checkpoint loader, resource authority, validation runner, research command, or
registered RNG path.
