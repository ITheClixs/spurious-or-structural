# G2 checkpoint authority and recovery contract

Written before checkpoint code, before the 252-date test-seed recovery, before
the A022 resource benchmark, and before any registered G2 seed is available.

## 1. What persistence can and cannot prove

Let `P` be a serialized sufficient-statistic payload, `M` its manifest, and
`H(P,M)` the complete set of unkeyed content hashes stored beside them.
Validation of `H(P,M)` proves only that the bytes read by the loader agree with
the bytes named by the manifest. It does **not** prove that those bytes were
created by the licensed in-memory issuance chain:

```text
for any forged (P*, M*), an actor who may rewrite the checkpoint can compute
H(P*, M*) and publish a self-consistent forged artifact.
```

This is not repaired by adding more SHA256 fields. Origin authentication
requires one of:

1. a secret or externally anchored signing key;
2. an append-only trusted service outside the writable checkpoint boundary; or
3. deterministic replay of the full upstream computation and byte comparison.

Options 1 and 2 violate the local, free, reproducible operating contract.
Option 3 defeats checkpoint reuse and contaminates the resource measurement it
is meant to support. Therefore the supported checkpoint threat model is
explicit:

- the local writer process and checkpoint directory are trusted as the origin
  boundary;
- the loader must detect crashes, torn publication, stale code/runtime/config,
  copied or mixed artifacts, missing/extra files, accidental corruption,
  relabeling, malformed schemas, and payload substitution that does not also
  recompute the entire trusted artifact; and
- coordinated same-user forgery that rewrites payloads, manifests, and all
  hashes consistently is outside the supported boundary and remains the
  strongest residual objection.

The paper and README may call this an integrity-checked local checkpoint, not a
cryptographically authenticated scientific record.

## 2. Persistence granularity

Raw rows, `X0`, PCA score matrices, and weak in-memory receipts are never
serialized. The two persisted artifact kinds are:

```text
base-panel:
  date-major packed X0'X0 for one complete addressed panel

cell-panel:
  date-major X0'Y and packed Y'Y for one complete addressed response panel
```

Base and cell artifacts remain separate because design identity is reusable
across structural responses while response authority is not. An aggregate-only
artifact is insufficient: whole-date bootstrap weights require the per-date
fields, and an aggregate cannot independently re-establish base/cell alignment.

The stored arrays are exact little-endian float64, C-contiguous, finite values:

```text
base.x0tx0_upper: (D, W(W+1)/2)
cell.x0ty:        (D, W, N)
cell.yty_upper:   (D, N(N+1)/2)

W = 3 + 2N.
```

On load they are copied into exact read-only `numpy.ndarray` values before any
authority is minted.

## 3. Kind-specific completion coordinates

The earlier phrase “full seed key and completed replicate range” is ambiguous
for a date panel. A base or cell artifact spans five DGP component keys over a
complete date domain and has no bootstrap replicate domain. Its canonical
address domain is:

```text
(master_seed,
 config_schema_version,
 rng_key_schema_version,
 phase_id,
 scenario_id,
 parent_phase_id=0,
 parent_scenario_id=0,
 n_dates,
 panel_index,
 cell_key=0,
 date_range=[0,n_dates),
 component_ids=[1,2,3,4,5],
 replicate_index=0)
```

Thus panel manifests carry `completed_date_range=[0,n_dates]` and
`completed_replicate_range=null`. Future bootstrap-batch artifacts require a
separate schema with an explicit half-open replicate range; they are not
licensed by this derivation.

The complete future persistence inventory is partitioned by role so a panel
schema cannot be silently reused for another object:

1. base panel;
2. cell panel;
3. smooth bootstrap batch;
4. paper-date/cache;
5. paper-bootstrap batch;
6. resource-bundle/run ledger; and
7. phase result plus success marker.

Only variants 1 and 2 are executable as reusable checkpoints in this slice.
A019 separately licenses one narrow, immutable seed-9191 recovery evidence
receipt and success marker; it is not a generic phase-result checkpoint and
cannot be reused by validation or research. All other variants 3--7 require
their own pre-code amendment, derivation, exact key/range inventory, and hostile
tests before A022. A loader rejects an unknown or later artifact kind rather
than interpreting it as a panel.

Every panel date must be present exactly once in ascending order. A 48- or
96-date frontier is a complete artifact under its own licensed address prefix,
not a truncation of a 252-date artifact.

## 4. Manifest identity

Both artifact kinds bind:

- schema version and exact artifact kind;
- all four frozen G2 seals;
- exact contract schema/design identifiers and dimensions;
- the complete canonical RNG address domain above;
- one common canonical-0.95 design-source response map;
- exact date indices, filtered-base identities, source-date content hashes,
  and response-independent design SHA256 values;
- tracked-plus-untracked execution-source snapshot SHA256 over
  `src/xid`, `configs/g2.toml`, `configs/g2_population_targets.json`,
  `pyproject.toml`, `uv.lock`, `.python-version`, and the Make-only public
  launcher `Makefile`;
- the creating Git commit and whether the execution-source paths were clean;
- the full numerical-runtime fingerprint and its canonical SHA256;
- exact payload file names, dtypes, shapes, byte counts, and SHA256 values;
- task elapsed seconds, cumulative elapsed seconds, and peak RSS bytes; and
- the kind-specific completion coordinates.

The design-source anchor is not caller-selected. It is exactly target index
`16`, canonical reliability `0.95`, and the stream-derived `phi`. Its
`paper_recovery` flag is true only for
`VALIDATION_PAPER_RECOVERY`; all other base/cell panel streams use the ordinary
non-recovery anchor. A panel whose source receipts do not share that one map is
not checkpointable even though the lower-level in-memory stacker can represent
it.

A cell artifact additionally binds exact response-date content hashes and one
common response map. For every date its design and response receipts must have
identical provenance and filtered-base identity. The cell design digest vector
must later equal the loaded base digest vector exactly before aggregation.

The execution-source snapshot includes untracked non-ignored files below the
declared execution paths so test-only development checkpoints cannot silently
omit a new source module. It also includes the root `Makefile`, because the
sole public A019 launcher fixes environment and performs filesystem mutation
before Python import. Registered execution will later require a clean snapshot;
this slice authorizes only test seeds `1729` and `9191`.

Final paths are derived internally below a caller-supplied trusted checkpoint
root. The expectation object contains only `(master_seed, stream, n_dates,
panel_index, response_map)`; the target-16 design anchor is derived internally
from the contract and stream and is never accepted from the caller. Define

```text
map_sha = SHA256(CJSON([target, paper_recovery, phi.hex, reliability.hex]))
prefix  = panel-v1/<stream>/seed-<10-digit uint32>/dates-<3-digit D>/
          panel-<10-digit uint32 panel index>/

base = <root>/<prefix>/base-<full design map_sha>
cell = <root>/<prefix>/cell-<full response map_sha>-
       parent-<full base artifact SHA256>
```

The root itself may be a temporary test root or the runner's internally rooted
G2 checkpoint directory, but it must already exist as an exact non-symlink
directory. Every existing path component below it must also be a non-symlink
directory. The root's resolved path must be disjoint from every declared
execution-source path: it may be neither an ancestor nor a descendant of one.
Callers do not supply an arbitrary final artifact path.

Execution-source snapshot version 1 is exact:

1. require the supplied repository root to equal `git rev-parse
   --show-toplevel`;
2. enumerate tracked plus untracked, non-ignored files below the seven declared
   execution paths with `git ls-files --cached --others --exclude-standard`;
3. require UTF-8 normalized relative POSIX paths, reject duplicates, missing
   files, directories, symlinks, and non-regular files;
4. sort by UTF-8 path bytes;
5. encode one canonical JSON row per file as
   `[relative_path, "100755"|"100644", byte_count, SHA256(file_bytes)]`,
   where the executable mode is derived from the actual file mode; and
6. hash the ASCII namespace `xid-g2-source-snapshot-v1\n` followed by the
   newline-delimited canonical rows.

The manifest also records the creating Git commit and clean/dirty status of the
declared paths. Loader equality binds the source-snapshot SHA256, not the Git
commit, so a documentation-only commit with identical execution bytes does not
invalidate an artifact. Registered authority will later require `clean=true`;
test authority may use an exactly bound dirty snapshot.

Before hashing, the writer and loader also require the imported
`xid.sim.g2`, `xid.models.g2_smooth`, and `xid.models.g2_checkpoint` module
files to resolve to the corresponding files below the supplied repository
root. For each module, the loader's current code object must equal a fresh
compilation of the same stable, no-follow source-byte snapshot, and the
import-time source SHA256 must still equal those current bytes. The first check
rejects a stale timestamp-based `.pyc`; the second rejects a source edit after
import. Together they prevent authenticating one source tree while executing
different local bytecode under the supported trusted-process boundary.

The source snapshot is taken once before and once after loading the sealed G2
contract, and both complete identities must match. This prevents publishing a
contract parsed from one config/target state under a later source identity.

The checkpoint runtime identity is the full
`current_g2_runtime_fingerprint()` projection plus the exact values (including
absence) of `BLIS_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS`,
`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and
`VECLIB_MAXIMUM_THREADS`. Define `CJSON(x)` as sorted-key, compact, ASCII,
`allow_nan=false` JSON plus exactly one terminal LF. `runtime_sha256` is
`SHA256(CJSON([fingerprint_object, thread_environment_object]))`; the digest
field is excluded from its own preimage. It must match at load.

## 5. Atomic state machine

The only valid states are:

```text
ABSENT
  -> write sibling staging directory
  -> write and fsync exact payload files
  -> write and fsync canonical metadata
  -> write and fsync _SUCCESS last
  -> fsync staging directory
  -> atomic same-parent rename
  -> fsync parent directory
PUBLISHED
```

An existing destination is immutable and is never overwritten. A staging
directory, missing `_SUCCESS`, hash mismatch, unexpected file, symlink, or
non-regular file is invalid and never repaired in place. The runner may reuse
only a fully loaded artifact whose exact expected coordinates validate; it may
create an absent artifact, but it may not silently regenerate over an invalid
one.

The loader snapshots each file once into memory after an exact size cap, hashes
that snapshot, and decodes that same snapshot. This removes the ordinary
hash-then-reopen TOCTOU gap. The sealed base/cell payloads are each below
5 MiB, so this does not threaten the 4 GB memory limit. NPY payloads are used
instead of a multi-member NPZ archive so extra/duplicate ZIP members and ZIP
bombs are outside the format.

The exact artifact files are `manifest.json`, `_SUCCESS`, and either
`x0tx0_upper.npy` or both `x0ty.npy` and `yty_upper.npy`. No other entry is
valid. JSON is UTF-8 canonical JSON with sorted keys, no whitespace except one
terminal newline, `allow_nan=false`, exact key sets, and duplicate-key
rejection. Telemetry floats are stored as binary64 `.hex()` strings.

### 5.1 Exact manifest schema

`manifest.json` has exactly these top-level keys:

```text
schema_version artifact_kind contract execution_source runtime address
dimensions design_response_map response_map date_indices source_receipts
design_receipts response_receipts design_sha256s parent payloads panel_token
telemetry completion
```

Their exact nested key sets are:

```text
contract:
  config_schema_version target_schema_version target_config_schema_version
  rng_key_schema_version design_id target_design_id seals
contract.seals:
  config_sha256 target_raw_sha256 target_semantic_sha256 lasso_ratio_sha256
execution_source:
  snapshot_schema snapshot_sha256 git_commit declared_paths_clean
runtime:
  python_implementation python_version numpy_version system machine byteorder
  rng_runtime_sha256 thread_env runtime_sha256
runtime.thread_env:
  BLIS_NUM_THREADS MKL_NUM_THREADS NUMEXPR_NUM_THREADS OMP_NUM_THREADS
  OPENBLAS_NUM_THREADS VECLIB_MAXIMUM_THREADS
address:
  master_seed stream config_schema_version rng_key_schema_version phase_id
  scenario_id parent_phase_id parent_scenario_id n_dates panel_index cell_key
  component_ids completed_date_range completed_replicate_range replicate_index
dimensions:
  n_rows n_assets n_levels x0_width
response-map object:
  target_index paper_recovery phi reliability
receipt object:
  master_seed stream phase_id scenario_id n_dates panel_index date_index
  base_identity target_index paper_recovery phi reliability
  date_content_sha256
parent:
  base_artifact_sha256 base_panel_token
payload descriptor:
  name npy_format dtype shape data_bytes file_bytes sha256
telemetry:
  task_elapsed_seconds cumulative_elapsed_seconds peak_rss_bytes
completion:
  completed_date_range completed_replicate_range
```

`schema_version` is integer `1`; `artifact_kind` is exactly `base-panel` or
`cell-panel`; `snapshot_schema` is
`xid-g2-source-snapshot-v1`; `npy_format` is `1.0`; all SHA256 values are
lowercase 64-character hex; `phi`, `reliability`, and the two elapsed fields
are exact binary64 `.hex()` strings.

For a base artifact, `response_map`, `design_receipts`,
`response_receipts`, and `parent` are JSON null; `source_receipts` is the
complete date-ordered receipt array; and `payloads` is the one-element ordered
array for `x0tx0_upper.npy`. For a cell artifact, `source_receipts` is null;
the two receipt arrays are complete and ordered; `parent` is present; and
`payloads` is the ordered pair `x0ty.npy`, `yty_upper.npy`. The
`design_response_map` is always the internally derived target-16 anchor.

The manifest cannot contain its own or the artifact's hash. Define:

```text
manifest_sha256 = SHA256(exact manifest.json bytes)
artifact_sha256 = SHA256(CJSON(
  ["xid-g2-panel-artifact-v1", artifact_kind, manifest_sha256,
   [[payload_name, payload_sha256], ...]]))
```

The payload pair order is the manifest order frozen above. `_SUCCESS` is
canonical JSON with exactly:

```text
schema_version artifact_kind manifest_sha256 artifact_sha256
payload_sha256s complete
```

`schema_version` is `1`, `complete` is `true`, and `payload_sha256s` is an
exact object keyed by the allowed payload names. `_SUCCESS` is excluded from
`artifact_sha256`, avoiding a circular hash; its exact bytes are nevertheless
size-capped, canonical, and checked against the independently recomputed
manifest and payload hashes.

NPY payloads use format version 1.0, exact dtype `<f8`, `fortran_order=false`,
header length at most 4096 bytes, exact expected shape, finite data, and exact
EOF with no trailing bytes. `manifest.json` is capped at 1 MiB, `_SUCCESS` at
16 KiB, and each payload at its exact expected data byte count plus 4096 bytes.

The loader opens and pins the artifact directory with no-follow semantics,
lists it through that directory descriptor, and opens every child relative to
the same descriptor with no-follow semantics. Every child must be a regular
single-link file. It hashes and decodes the same one-read byte snapshot.

The writer first takes a nonblocking exclusive advisory lease on the pinned
root-directory descriptor. This serializes every cooperating reader and writer
across all artifact coordinates, so the 2 GB cap is a global invariant rather
than a per-coordinate race. Before any filesystem mutation, it reserves the
exact crash-marker payload plus a conservative directory-entry quantum against
the current logical and allocated tree sizes. Only then does it create
`<root>/.xid-g2-checkpoint.lock` with no-follow, create-exclusive semantics and
mode `0600`; the marker's canonical JSON contains exactly `schema_version`,
`pid`, and `final_relative_path`. The advisory lease prevents a live
cooperating race; the durable marker blocks reuse after a crash, when the
kernel lease has necessarily disappeared.

While holding both, the writer reserves the complete publication before
creating any prefix or stage directory. The projection includes every exact
file length rounded to the filesystem allocation quantum, conservative
directory-object and parent-entry growth for every missing prefix and the
stage, one quantum per future file entry, and rename slack. It then creates and
fsyncs each prefix, creates the mode-0700 same-parent stage, repeats the
remaining-stage reservation against actual usage, and checks actual root usage
after every directory creation, file write, and rename. It fsyncs each file,
recomputes and matches source/runtime identity, refuses any existing final
destination, renames once, and fsyncs the parent. Before rename, an ordinary
handled exception removes only its known stage, fsyncs the stage parent,
removes the marker, and releases the lease. If stage removal or its parent
fsync is uncertain, the marker remains as a blocker even though the process
releases its kernel lease. After rename, any cap, fsync, or publication
uncertainty likewise leaves the marker in place; it must never advertise a
possibly non-durable artifact as safely reusable. A marker left by a crashed
writer is not guessed stale or deleted automatically.

## 6. Authority restoration

Weak registry entries are process-local and are not serialized. The only
restoration entry points are the exact stage-specific loaders:

```text
load_contract_base_panel_checkpoint(...)
load_contract_cell_panel_checkpoint(...)
```

Before writing any byte, each writer validates the exact live base/cell panel
against its existing weak registry token. Cell writing additionally validates
the exact issued base panel, the exact issued cell panel, their receipt/design
alignment, and the supplied already-published base evidence. A copied,
hand-built, or equality-compatible panel cannot be converted into a trusted
checkpoint.

Each stage-specific loader holds a nonblocking shared advisory lease on the
pinned root directory from its initial marker check through reconstruction,
token validation, and inline weak-registry issuance. A cooperating writer
cannot acquire its exclusive lease during that interval. The loader also
rechecks the durable marker after source/runtime stability is established and
again before releasing the shared lease, so an uncoordinated marker appearance
fails the load rather than returning authority.

Each loader:

1. requires the exact live `TestRngNamespace` capability in this slice and
   validates its contract/seed against the current sealed contract and expected
   stream/date/panel coordinates; only seeds `1729` and `9191` are licensed,
   and there is no `allow_registered` switch;
2. validates the current source snapshot, runtime, and exact expected response
   map(s);
3. validates the exact directory schema, success marker, metadata, hashes,
   payload headers, shapes, dtypes, layout, finiteness, and resource telemetry;
4. reconstructs exact immutable `G2DateReceipt` tuples and the corresponding
   exact panel dataclass;
5. recomputes the existing stage token; and
6. writes one weak-registry entry inline in that exact loader while the shared
   lease is still held.

No generic registrar and no function accepting an already-decoded caller
object may mint authority. A loaded base and cell panel must still pass the
existing `aggregate_contract_smooth_moments` alignment checks before an
aggregate receipt can be minted.

Every cell manifest's `parent` object carries both `base_artifact_sha256` and
`base_panel_token`. Cell loading requires the already loaded and issued base
checkpoint object and checks both parent fields plus exact receipt/design
alignment before the cell registry write.

`validate_g2_date_receipt_metadata` is only a syntax-and-law validator. It does
not license a seed, panel, or response map. The stage loader separately checks
every receipt against the exact expected seed, stream, phase/scenario, date
domain, panel index, internally derived design map, and caller-expected
response map before the registry write.

Registered and otherwise unlicensed master seeds fail before filesystem access
or authority restoration in this slice.
Opening them requires a later, separately tested registered-run capability that
first passes the A006 runtime preflight and A022 resource gate.

## 7. Resource recovery

The manifest carries both task and cumulative elapsed time. On resume, the
runner adds no new time for reused work but reloads the prior cumulative work
and maximum RSS into every hard-stop and forecast calculation. Restarting a
process cannot reset a phase budget.

Checkpoint byte accounting includes payload, metadata, success marker, and
filesystem-visible artifact size. Base and cell serialization, hashing,
loading, validation, and fresh issuance are timed separately in A022.

The sealed 2 GB checkpoint allocation is the maximum of logical bytes and
filesystem allocated bytes summed across the active
G2 checkpoint tree for one phase, including every published artifact and every
staging directory. It is not a per-artifact allowance. Transient staging bytes
count at their simultaneous peak, so atomic publication includes the stage in
the allocation before rename.

An interrupted replay of an unpublished exact address under the same frozen
manifest is the same software/resource attempt. A valid published artifact must
be reused. Deleting or replacing it, changing any address/seed/threshold/schema
semantics, or substituting another panel is a new specification/attempt and is
forbidden without an amendment. Deterministic TDD red/green failures under
C0015 do not consume a scientific trial.

## 8. Pre-run failure predictions

Before implementation, the current repository has no loader and therefore
cannot restore a panel after live weak receipts die. The red suite is predicted
to fail because the named stage-specific APIs do not exist.

After implementation:

1. exact base and cell round trips preserve every numeric byte and regain only
   their own stage authority;
2. a fresh process can load, align, aggregate, and fit the same checkpoint
   bytes without any RNG draw or upstream replay; creating the exact test-only
   namespace capability is allowed and every draw method is instrumented to
   fail if called;
3. the enumerated structural fault classes—missing/extra/symlink files,
   interrupted publication, metadata/payload/success tampering, wrong kind,
   endian, dtype, order, shape, length, or nonfinite values—fail before
   issuance;
4. every seal, source, runtime, seed, stream, phase/scenario, date count, panel
   index, response map, receipt, digest, and completion-range mismatch fails;
5. incomplete, duplicate, or out-of-order dates and mixed base/cell artifacts
   fail;
6. existing destinations are never overwritten, and an invalid existing
   artifact is not silently regenerated;
7. cumulative time and RSS survive reload; and
8. registered seeds fail before any RNG constructor or restored authority.

The test cannot prove resistance to a coordinated same-user actor who forges
all bytes and recomputes all hashes; claiming otherwise would contradict
Section 1.

## 9. A019 one-shot supervisor and evidence receipt

The seed-9191 recovery is not a reusable estimator runner. It is one
irreversible software-recovery attempt with a parent supervisor, one primary
worker, and one fresh-process reload worker. The public command has no
seed/date/panel overrides. Before publishing the attempt it must require:

1. the exact frozen A019 address and response maps;
2. the six numerical thread variables in Section 4 to equal the string `"1"`;
3. a clean declared execution-source snapshot;
4. absent attempt, result, success, failure, and worker-claim files;
5. an empty, non-symlink checkpoint root and a non-symlink scratch root whose
   sole entry is the exact empty supervisor bootstrap prefix below the
   repository's ignored `data/` tree; and
6. a deterministic repository revision whose checkpoint tests, full tests,
   lint, format, and type checks have already passed.

The canonical public paths are:

```text
results/g2_checkpoint_recovery/attempt.json
results/g2_checkpoint_recovery/result.json
results/g2_checkpoint_recovery/_SUCCESS
results/g2_checkpoint_recovery/failure.json
results/g2_checkpoint_recovery/_FAILURE
data/g2_checkpoint_recovery/checkpoints/
data/g2_checkpoint_recovery/scratch/
data/g2_checkpoint_recovery/scratch/bootstrap-pycache/
```

The sole public interface, `make g2-checkpoint-recovery`, creates and verifies
the empty bootstrap cache before Python imports the supervisor module; direct
module invocation fails before constructing the A019 specification or writing
`attempt.json`. The primary and fresh workers then run with separate, unique,
initially empty `PYTHONPYCACHEPREFIX` directories below the same exact scratch
root. Each private child consumes a one-shot inherited pipe capability bound to
its role, immediate parent PID, immutable attempt digest, exact internal-spec
bytes, and canonical scratch path. This prevents both a pre-existing timestamp
cache from deciding any of the three process imports and an ordinary direct
private-child invocation from supplying alternate roots or replaying the
primary draw. The checkpoint codec's independent fresh-compilation equality
remains mandatory inside each process.

These checks are preflight and consume no attempt. The supervisor then
publishes canonical `attempt.json` with create-exclusive, success-last file
publication before it starts the worker. Once `attempt.json` exists, every
later public invocation fails before spawning a process or constructing an RNG
namespace. A crash therefore consumes the attempt. The worker independently
rechecks the live source snapshot, import origins, numerical runtime, and clean
status against the immutable attempt, then creates an exclusive ignored
`worker-claim.json` before its first DGP draw, so an accidental direct second
worker invocation also fails before RNG access. Each evidence file is first
fully written and fsynced to a create-exclusive sibling stage, then exposed
atomically by a no-overwrite hard link and directory fsync; an interrupted
write never exposes a partial final path.

`attempt.json` has exactly:

```text
schema_version status seed stream phase_id scenario_id n_dates panel_index
design_target_index response_target_index paper_recovery phi reliability
source_snapshot_sha256 runtime_sha256 checkpoint_root scratch_root
hard_stops supervision
```

`schema_version` is integer `1`; `status` is `"started"`; `phi`,
`reliability`, the 120-second wall stop, and the 0.05-second polling period are
canonical binary64 `.hex()` strings. Repository paths are normalized relative
POSIX paths. `hard_stops` contains exactly `artifact_bytes`,
`wall_seconds`, and `peak_rss_bytes`; `supervision` contains exactly
`poll_seconds`, `timeout_method`, and `rss_normalization_method`.

The supervisor starts the primary worker in a new process group, redirects its
bounded stdout and stderr to ignored scratch files, and polls:

```text
ps -axo pid=,ppid=,rss=
```

RSS is interpreted as KiB, multiplied by 1024, and summed over the complete
descendant closure rooted at the worker PID. The reported peak is the maximum
observed process-tree sum. The enforceable claim is termination on the first
observed sample above 1.5 GiB, not proof that no shorter unsampled spike
occurred. Monotonic elapsed time is checked on every poll. A polling failure,
first observed RSS breach, or 120-second breach kills the complete process
group and is an A019 failure. The supervisor also checks for surviving
process-group descendants after the leader exits, kills any such descendants,
and records a failure rather than accepting an orphaned child.

The primary worker:

1. constructs the exact 252-date target-16 design and target-0 response panel;
2. computes the homogeneous, observable-ridge, and oracle-ridge point
   coefficients;
3. publishes the base then cell checkpoints;
4. retains only hashes, shapes, finiteness flags, evidence, and resource
   counters, then drops every raw date, transformed date, design, date moment,
   panel, and aggregate and forces garbage collection;
5. freezes the runtime fingerprint, instruments every namespace draw method
   and direct NumPy RNG constructor to raise, loads the checkpoints,
   reaggregates, and refits;
6. requires exact raw-byte hashes for all arrays and coefficients and exact
   canonical hashes for receipt and design-digest tuples; and
7. spawns one fresh process which repeats only step 5 and returns the same
   three coefficient hashes with draw count zero.

Artifact logical and allocated bytes are measured independently with
`lstat`; both combined totals must be strictly below 12 MiB. The supervisor
accepts only one exact canonical worker-result schema and independently checks
the address, source/runtime identities, coefficient/hash equality, zero fresh
draws, and all three hard stops.

The committed `result.json` has exactly:

```text
schema_version status seed stream phase_id scenario_id n_dates panel_index
source_snapshot_sha256 runtime_sha256 base_artifact_sha256
cell_artifact_sha256 array_sha256_before array_sha256_after
receipt_sha256_before receipt_sha256_after design_digest_sha256_before
design_digest_sha256_after coefficient_sha256_before coefficient_sha256_after
coefficient_shapes coefficient_finite fresh_process_coefficient_sha256
fresh_process_rng_draw_count artifact_logical_bytes artifact_allocated_bytes
elapsed_seconds timeout_method peak_rss_bytes rss_normalization_method
hard_stops
```

The three array-hash objects have exact keys `base_x0tx0_upper`,
`cell_x0ty`, and `cell_yty_upper`. Receipt-hash objects have exact keys
`base_source_receipts`, `cell_design_receipts`, and
`cell_response_receipts`. Design-digest objects have exact keys
`base_design_sha256s` and `cell_design_sha256s`. Coefficient objects have exact
keys `homogeneous`, `observable`, and `oracle`. Byte-count objects have exact
keys `base`, `cell`, and `combined`. `elapsed_seconds` is a canonical
binary64 `.hex()` string. `hard_stops` records each exact limit, observed
value, and Boolean pass result.

`_SUCCESS` is published after `result.json` and has exactly:

```text
schema_version status result_sha256 complete
```

with status `"passed"` and `complete=true`. If the attempt fails after
publication, the supervisor instead publishes immutable `failure.json` then
`_FAILURE`. The failure receipt binds the attempt SHA256, failure stage/type
and bounded message, worker return code when available, elapsed/RSS evidence,
supervision methods, hard stops, and stdout/stderr SHA256 values. It is not a
retry license. If the supervisor itself is killed before it can publish a
failure receipt, `attempt.json` remains the authoritative consumed-attempt
record.

## 10. Fail-closed recovery invariants under filesystem and process faults

Let `P` be a configured root path and `R(P)` its non-strict canonical
resolution before creation. Pre-attempt path admission requires

```text
P.is_absolute() and R(P) == P.
```

The same equality with strict resolution is required after creation. A
symlink in any existing ancestor makes `R(P) != P`; rejection therefore occurs
before `attempt.json`, not later when a child decodes the resolved internal
specification. This is a fail-closed same-process preflight invariant, not a
claim of resistance to a coordinated actor racing every pathname operation.

For a successfully spawned worker process group `G`, supervision has the
postcondition

```text
return or raise from supervisor  =>  not exists(G),
```

except when the teardown operation itself raises and retains the recovery in a
failed, non-accepted state. TERM teardown is followed by a bounded existence
loop; if `G` remains, KILL is followed by a second bounded existence loop.
The helper raises rather than returning when the second loop expires. The
whole supervision body is bracketed by an unconditional finalizer after
successful `Popen`, so unexpected exceptions and interrupts have the same
teardown obligation as registered hard stops.

A child capability descriptor `d` must be a kernel-created anonymous pipe, not
merely any object for which `S_ISFIFO(fstat(d).st_mode)` is true. Named FIFOs
have a filesystem name and can be reopened with the same payload. The
platform-specific admission predicate is intentionally narrow:

```text
Darwin: S_ISFIFO(mode) and st_dev == 0 and st_nlink == 0
Linux:  S_ISFIFO(mode) and readlink("/proc/self/fd/d") == "pipe:[digits]"
other:  reject
```

This predicate distinguishes the `os.pipe()` capability used by the parent
from the tested reopenable FIFO. Role, immediate-parent PID, attempt digest,
and exact spec digest remain mandatory content bindings.

For create-exclusive evidence, let `L` mean that the fully written,
file-fsynced stage has been linked to the final name. The allowed state
transitions are

```text
not L                    -> raise, final absent
L and first fsync fails  -> retry
L and retry succeeds     -> success, final authoritative
L and retry fails        -> unlink final, fsync parent, then raise
rollback fsync fails     -> raise publication-state-uncertain
```

The supervisor never publishes the opposite terminal outcome after the final
branch, and `failure.json`/`_FAILURE` refuse publication while `_SUCCESS` is
visible. Thus an injected durability fault may yield success, failure, or an
unresolved consumed attempt, but never simultaneous success and failure
markers.

### 10.1 Cleanup-error precedence

Let `E_p` be the primary publication result and `E_c` a later error removing
the non-authoritative stage. Once `E_p` is
`publication-state-uncertain`, replacing it with `E_c` loses the only type
information that prevents opposite-outcome publication. The required
precedence is therefore

```text
E_p is not None  =>  propagate E_p; stage-cleanup OSError is suppressed
E_p is None      =>  a durable final link remains authoritative even if
                      best-effort stage cleanup fails
```

The stage has already been file-fsynced and is never consulted as final
evidence. Its possible persistence is bounded litter, whereas erasing `E_p`
can create contradictory terminal evidence after a crash. The latter is the
strictly larger failure and controls the policy.

`E_c` ranges over `BaseException`, not merely `OSError`, because asynchronous
`KeyboardInterrupt` and `SystemExit` can arrive in the same cleanup window.
Suppression is conditional on `E_p` already being
`publication-state-uncertain`; in every other state, a non-`OSError` cleanup
interrupt propagates normally. This preserves both terminal-evidence ordering
and ordinary cancellation semantics.

### 10.2 Pre-import Make authority

Python cannot reject a path mutation that Make already performed. The
bootstrap path and thread environment are therefore constants at the Make
layer, not ordinary caller-overridable variables. Before creating

```text
data/g2_checkpoint_recovery/scratch/bootstrap-pycache
```

the recipe requires each existing component in that literal chain not to be a
symlink. Only then may `mkdir -p` run. Python independently repeats canonical
resolution and exact-path checks after import. The two layers establish:

```text
Make preflight passes -> no observed symlink ancestor before mkdir
Python preflight passes -> created path resolves to the frozen public root
```

This is a same-process/ordinary-launch invariant. A coordinated actor with
write access can race separate shell operations and remains excluded by A024.

### 10.3 Procedure kind is not RNG-stream identity

Let `s_spec` be the stream printed in the attempt/result and `s_draw` the stream
used to derive every date address. Honest evidence requires

```text
s_spec == s_draw
phase_scenario_receipt == contract.phase_scenario(s_draw).
```

The test-only recovery *procedure* uses the already licensed
`VALIDATION_DATE_FRONTIER` stream at seed 1729 and 48 dates. It may not print
`VALIDATION_RECOVERY` merely because it exercises checkpoint recovery. The
public A019 procedure separately uses `VALIDATION_RECOVERY`, seed 9191, and 252
dates. No helper may silently substitute one stream between the spec and draw
path.
