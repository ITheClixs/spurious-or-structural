# G2 response identity and in-memory issuance chain

Written after a pre-implementation critique of A008/A009 and before the
provenance repair was executed. It corrects two remaining self-attestation
routes.

## 1. Response-map identity is distinct from base identity

All structural cells deliberately reuse the same addressed base realization.
Therefore `filtered_base_identity`, date index, and the `X0` design digest are
supposed to agree across cells. They cannot identify the response map.

Every transformed date receipt must separately bind

```text
response_map_identity =
  (target_index, paper_recovery, phi, reliability)
```

plus the exact `r/u/z` content already covered by the date hash. Cell moments
and cell panels retain this identity and require one common response-map prefix
across dates. Same-base/different-cell construction remains valid only through
an explicit contract cell builder, and the resulting aggregate reports which
response map it contains. Relabeling a cell or gamma-zero recovery response is
not equivalent to sharing a base.

## 2. Digests diagnose equality; receipts license authority

A copied `design_sha256` cannot prove that a manually constructed moment
record was produced from that design. Contract-origin authority therefore uses
a module-owned weak issuance chain:

```text
validated G2Date receipt
  -> issued contract base/cell date moments
  -> issued complete contract base/cell panels
  -> issued contract aggregate
  -> high-level G2 fit
```

Each issuance record binds the exact wrapper object identity, immutable
provenance snapshot, aligned design/response identities, and a versioned
content token over the exact ndarray runtime contract and numeric bytes.
Validation recomputes the token before minting the next stage. It deliberately
does not bind ndarray object identity: replacing an array with an exact
float64, C-contiguous, read-only ndarray carrying the same bytes is payload-
equivalent, while the enclosing wrapper still needs its own live issuance
receipt. Dead wrappers remove their weak receipt.

Generic analytic moments, panels, aggregates, extraction functions, and
solvers remain ordinary numeric objects. They cannot mint any receipt in this
chain. High-level G2 fits accept only an aggregate whose exact live object has
an issued aggregate receipt.

## 3. Checkpoint boundary

Weak in-memory receipts are not serialized. A future checkpoint loader may
mint a replacement panel or aggregate receipt only after independently
checking the sealed config/target/runtime fingerprints, complete provenance
manifest, payload schema, row counts, aligned design/response digests, and
content hashes. That loader is not part of the estimator-core slice and creates
no authority now.

## 4. Pre-run predictions

The repair tests must reject:

1. a cell moment or panel whose copied digest was not issued by the contract
   builder;
2. a complete-looking aggregate assembled from hand-built contract flags;
3. response dates with the same base but a silently changed target or
   `paper_recovery` label; and
4. any stale or content-mutated object at every issuance stage.

They must accept two legitimately minted structural response maps sharing one
validated base identity while preserving their distinct response-map metadata.

## 5. Caller-sequence snapshot amendment

The issuance proof applies to one fixed collection of moments. It is invalid to
validate one traversal of a caller-owned sequence and construct from another:
the sequence itself can be stateful even when every returned moment wrapper is
frozen. Each stacker therefore performs exactly one projection

```text
caller Sequence -> exact local tuple -> validate -> construct -> issue
```

and every subsequent read uses the local tuple. In particular, the contract
cell stacker may not reread the caller between item issuance checks and the
`X0'Y`/`Y'Y` stacks. A deterministic red construction returned live issued
moments for the validation traversals and unissued zeroed cross-moments for the
construction traversals; the old implementation minted the resulting panel and
aggregate. The one-snapshot rule removes that time-of-read substitution without
changing any valid list or tuple result.
