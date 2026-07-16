# G2 smooth-moment provenance repair

Written after the first hostile review of C0003 failed and before the repair is
implemented. No resource, validation, research, empirical, evaluation, or
holdout stream informed this design. The only stochastic estimator smoke seen
before this document used test seed `1729` and made no population-target claim.

## 1. Diagnosed failure

The numerical estimators recover the intended algebra, but their current input
boundary is not closed under provenance.

First, an exact `G2Date` dataclass can be constructed outside `transform_date`.
Checking only the class and the `(330,30,10)` shapes therefore does not show
that the arrays were minted from one licensed base draw, phase/scenario, cell,
and deterministic transform.

Second, date moments currently identify a date only by `date_index` and
dimensions. The following invalid composition is therefore accepted:

```text
base panel: G_A = X_A' X_A
cell panel: H_B = X_B' Y_B, J_B = Y_B' Y_B
```

when `A` and `B` share a date index and dimensions. Aggregating `G_A` with
`H_B,J_B` changes every estimator while preserving superficially plausible
shapes. This is a software-contract failure, not sampling noise.

## 2. Minted transformed-date receipt

`transform_date` must return read-only arrays and mint a module-owned weak
receipt for the exact `G2Date` object. The receipt binds:

```text
provenance snapshot =
  (master_seed, stream, phase_id, scenario_id,
   n_dates, panel_index, date_index)

object identities =
  (filtered, v, q, u, r, z, x)

base identity = filtered.provenance_token
date content token = SHA256(
  versioned header || provenance snapshot || base identity ||
  each output name || shape || dtype || C-order bytes
)
```

The public validator must reject before estimator construction unless:

1. the object and all nested dataclasses have their exact declared types;
2. the weak receipt still names the exact object;
3. current provenance and object identities equal the issuance snapshot;
4. the configured phase/scenario and stream coordinates remain licensed;
5. every filtered and transformed array is finite float64, C-contiguous,
   read-only, and has its sealed shape;
6. the filtered-base token recomputes exactly; and
7. the date content token recomputes exactly and equals issuance.

The weak-reference callback removes dead receipts. A rewrapped, relabeled,
mixed, mutated-and-retokened, or manually constructed date is not licensed by
an equality-compatible payload.

The base identity is intentionally independent of the structural response
cell. All S0004 cells reuse one addressed base realization, while `r` changes
with the structural cell. Thus a base design may be paired with different
cell responses only when both transformed dates carry the same validated
filtered-base identity.

## 3. Design digest

Every `SmoothDateDesign` receives two immutable identifiers:

```text
source_identity
design_sha256 = SHA256(
  "xid-g2-smooth-design-v1" ||
  date_index || n_rows || n_assets || n_levels ||
  source_identity || X0 dtype/shape/C-order bytes
)
```

For the contract-bound builder, `source_identity` is the validated filtered-
base token returned by the transformed-date validator. For the generic
analytic builder it is the literal versioned analytic namespace; the design
digest still changes with the exact `X0` bytes.

`SmoothBaseDateMoments` and every `SmoothCellDateMoments` copy both identifiers
from the exact design used to form their cross-products. Date-major panels
retain the aligned identifier tuples. Aggregation requires exact equality of
date indices, source identities, and design digests before any weighted matrix
multiplication. It never sorts or repairs a mismatch.

A contract-bound cell builder additionally validates the response `G2Date`,
requires its `date_index` and filtered-base identity to match the design, and
only then forms `X0'Y` and `Y'Y`. This permits the registered common-base,
different-cell construction and rejects a response from another panel/date.

## 4. Observable integration fixture

The first test set separately checked PCA and ridge but did not prove that the
primary observable ridge selects the integrated-OFI block. The repair test uses
centered orthogonal binary columns with

```text
Cov(Q) = I,
W = 2 Q,
Y = Q B' + z alpha'.
```

With the trace floor binding, the pre-run prediction is

```text
oracle:     B_hat = B / (1 + 1e-6),       floor = 1e-6
observable: B_hat = B / (2 * (1 + 1e-6)), floor = 4e-6.
```

A mutation that points the observable branch at oracle `Q` must fail this
fixture even if PCA and oracle tests remain green.

## 5. Stop condition

The repair slice passes only if red tests first reproduce both provenance
failures, then the minted-date, mixed-moment, different-base response, weak
receipt cleanup, observable-integration, and already registered numerical
tests all pass locally and under hosted CI. No checkpoint runner, recovery
experiment, resource benchmark, or registered RNG authority is created.
