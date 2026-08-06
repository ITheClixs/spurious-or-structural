# G2 resource artifact and receipt authority

Written on 2026-07-28 before resource-run code or any registered G2 resource,
validation, or research RNG access. The exact resource config was added and
this authority was amended on 2026-07-29 and 2026-08-06 before implementation
or rehearsal.

This document is the byte-level persistence authority for A022 as narrowed by
append-only amendments A023, A024, A025, and A026. It does not license the
registered resource seed. It defines the exact artifacts and receipts that the
deterministic test-seed implementation must recover before the resource command
can become eligible.

## 1. Scope and inherited authority

The resource benchmark needs more persistent objects than the already
implemented smooth-panel checkpoint codec. Reusing a panel kind for a
paper cache, bootstrap batch, publication envelope, or timing receipt would
erase the distinction between scientific sufficient statistics and benchmark
fixtures. That is forbidden.

The existing checkpoint authority remains unchanged:

```text
artifact kind  base-panel
artifact kind  cell-panel
```

Their paths, manifest schemas, payload names, digest namespace
`xid-g2-panel-artifact-v1`, success-marker schema, trusted-origin boundary,
and C0015 test-stage entry points remain exactly those in
`GATE_G2_CHECKPOINT_AUTHORITY.md`. A022 adds separate exact resource-stage
panel writer/loader entry points which accept only the separately derived exact
`ResourceRngNamespace`. The C0015 entry points continue to accept only the
exact `TestRngNamespace` and test seeds. Neither path dispatches on a caller
Boolean or a common public union type. A022 may not:

1. rename either artifact kind;
2. add, remove, reinterpret, or reorder a manifest field or payload;
3. change either artifact-path formula;
4. change, wrap around, or bypass a C0015 test-stage entry point;
5. add an `allow_registered` Boolean;
6. expose a generic registrar; or
7. let a resource panel mint validation or research authority.

All new binary artifacts use a separate namespace and exact kinds:

```text
resource-null-batch-v1
resource-paper-full-date-v1
resource-paper-recovery-date-v1
resource-paper-cache-fixture-v1
resource-paper-bootstrap-batch-v1
resource-publication-envelope-v1
resource-resume-base-panel-v1
resource-resume-cell-panel-v1
resource-resume-bootstrap-weights-v1
resource-resume-paper-bootstrap-weights-v1
resource-resume-candidate-focals-v1
```

All reservation, worker, resume-boundary, interruption, cleanup-intent, trace,
measurement, terminal-failure-intent, terminal-failure-resume,
terminal-nonpass-intent, attempt, result, failure, and nonpass records are
canonical JSON receipts, not disguised NPY artifacts.

As with the inherited checkpoint codec, unkeyed SHA256 proves byte integrity
and identity consistency inside the trusted local writer/checkpoint boundary.
It does not authenticate origin against a coordinated same-user actor who can
rewrite every payload, manifest, receipt, and digest consistently.

## 2. Exact primitive encodings

Define:

```text
CJSON(x) =
  json.dumps(
      x,
      sort_keys=True,
      separators=(",", ":"),
      ensure_ascii=True,
      allow_nan=False,
  ).encode("ascii") + b"\n"
```

Every JSON decoder rejects duplicate keys before constructing an object.
Every JSON file must decode to the expected exact built-in Python container
and scalar types and must satisfy `CJSON(decoded) == original_bytes`.
Subclasses, `bool` where an integer is required, binary64 JSON numbers,
unknown keys, missing keys, and extra whitespace fail.

The primitive domains are:

| Name | Exact domain |
| --- | --- |
| `u32` | exact JSON integer, `0 <= x < 2**32` |
| `u64` | exact JSON integer, `0 <= x < 2**64` |
| `pid` | exact JSON integer, `1 <= x < 2**31` |
| `sha256` | exact string of 64 lowercase hexadecimal characters |
| `f64hex` | exact string `s` for which finite `float.fromhex(s)` exists and `float.fromhex(s).hex() == s` |
| `relpath` | nonempty NFC-normalized relative POSIX path with no empty, `.`, `..`, backslash, or NUL component |
| `kind` | one literal kind enumerated by the containing schema |
| `ns` | `u64` nanoseconds from `perf_counter_ns`; it is never a JSON float |

All string fields are ASCII unless a failure message is explicitly permitted
to be UTF-8. SHA256 always means SHA256 over the exact named bytes, not over a
decoded object.

Every A022-defined JSON object that contains `schema_version` uses the exact
built-in integer `1`; the only exceptions are explicitly inherited C0015
panel manifests whose existing version remains byte-unchanged. The only
A025-defined version-2 objects are `resume_state` and the common deletion-plan
object when named `deletion_plan`, `cleanup_inventory`, or `debris`; every
other A025 object with `schema_version` uses integer `1`. Every A022/A025
terminal or receipt marker that contains `complete` uses exact Boolean `true`.
This global rule applies to attempts, claims, reservations, boundaries,
interruptions, traces, measurements, results, failures, and both terminal
markers even when the local schema does not repeat the value.

Both rehearsal and registered terminal failures use the same structured
reason contract. `failure_stage` is one literal from this ordered list:

```text
bootstrap
source-preflight
runtime-preflight
config-preflight
attempt-publication
worker-claim
reservation
kernel
boundary-publication
trace-publication
measurement-publication
resume
rss-accounting
disk-accounting
registry-accounting
stationarity
rate-robustness
projection
terminal-cleanup
terminal-publication
```

`failure_type` is one literal from this ordered list:

```text
schema
source-drift
runtime-drift
config-mismatch
capability
process-identity
boot-identity
timeout
sampler-gap
rss-limit
disk-limit
address
numerical
artifact
receipt
registry
stationarity
rate-robustness
task-budget
phase-budget
total-budget
interruption-proof
io
unexpected-exception
```

The stage is the first failed predicate in canonical execution order. If one
predicate maps to more than one type, the earliest type in the list wins.
`message` is diagnostic but byte-deterministic ASCII exactly
`failure_stage + ":" + failure_type`; raw exception text, paths, PIDs, times,
locale text, and operating-system messages go only to bounded stdout/stderr
evidence and never alter terminal JSON.

The hard file caps are:

```text
canonical JSON receipt or marker        1,048,576 bytes
artifact manifest.json                  1,048,576 bytes
artifact _SUCCESS                          16,384 bytes
each NPY payload                         5,242,880 bytes
NPY header                                   4,096 bytes
failure message                              1,024 UTF-8 bytes
worker stdout or stderr                    262,144 bytes each
```

No cap may be widened by configuration. A file is rejected before allocation
or decoding if its `st_size` exceeds its cap.

## 3. Canonical roots and path state

The registered resource roots are:

```text
R = results/g2_resource_benchmark
C = data/g2_resource_benchmark/checkpoints
S = data/g2_resource_benchmark/scratch
```

Before a new attempt, all three paths are absent. Their repository-relative
spellings are constants in Make and Python. Every existing ancestor is opened
without following symlinks; each created directory is mode `0700` and is
fsynced with its parent. Strict resolution after creation must equal the
precomputed absolute path. The roots are pairwise disjoint and disjoint from
every declared execution-source path.

The one-shot test-seed measurability rehearsal uses disjoint roots:

```text
TR = results/g2_resource_rehearsal
TC = data/g2_resource_rehearsal/checkpoints
TS = data/g2_resource_rehearsal/scratch
```

They are absent before the rehearsal command, obey the same ancestor,
permission, fsync, no-follow, cap, and disjointness rules, and can never be
passed to a registered-resource entry point.
`TR/terminal/success/{result.json,_SUCCESS}` is small committed evidence.
Binary rehearsal artifacts below `TC` are
deleted inside their combined kernels only after their exact immutable
inventory rows have been validated; the durable kernel and trace receipts
carry those rows into `TR/terminal/success/result.json`.

The complete persistent result-tree grammar is:

```text
R/
  attempt.json
  reservations/
    panel-<10-digit u32>/
      claim.json
      _SUCCESS
  worker-launches/
    launch-<10-digit u32>/
      claim.json
      _SUCCESS
  worker-births/
    birth-<10-digit u32>/
      claim.json
      _SUCCESS
  workers/
    worker-<10-digit u32>/
      claim.json
      _SUCCESS
  boundaries/
    boundary-<10-digit u32>/
      receipt.json
      _SUCCESS
  interruptions/
    interruption-<10-digit u32>/
      receipt.json
      _SUCCESS
  cleanups/
    cleanup-<10-digit u32>/
      receipt.json
      _SUCCESS
  traces/
    trace-<10-digit u32>/
      receipt.json
      _SUCCESS
  measurements/
    block-1/
      receipt.json
      _SUCCESS
    block-2/
      receipt.json
      _SUCCESS
    block-3/
      receipt.json
      _SUCCESS
  terminal/
    success/
      result.json
      _SUCCESS
```

or, instead of `terminal/success/`, the marked-failure grammar has:

```text
  terminal/
    failure-intent/
      receipt.json
      _SUCCESS
    failure-resumes/
      resume-<10-digit u32>/
        receipt.json
        _SUCCESS
    failure/
      failure.json
      _FAILURE
```

After a success/failure terminal-entry receipt has consumed its selected kind
but that kind cannot reach visible certified publication, amendment A026's
only legal forensic-close grammar is:

```text
  terminal/
    nonpass-intent/
      receipt.json
      _SUCCESS
      publication.lock
    nonpass/
      nonpass.json
      _NONPASS
```

There is exactly one failure-intent directory and a contiguous 1-to-641
failure-resume prefix beginning at index zero. `terminal/failure-intent`,
`terminal/failure-resumes`, and `terminal/failure` are absent on success;
`terminal/success` is absent on failure. A visible `terminal/nonpass` is
mutually exclusive with both visible outcomes, may retain only the exact
selected hidden success/failure stage bound by its intent, never passes
admission, and never licenses retry. Any other incomplete attempt may contain
only the exact prefix states permitted by Sections 10, 10.2, and 10.3; it is
neither successful nor a marked-failure grammar.

The complete new-artifact grammar below `C` is:

```text
C/
  resource-v1/
    panel-<10-digit u32>/
      null-batch/
      resume/
        base-panel/
        cell-panel/
        bootstrap-weights/
        paper-bootstrap-weights/
        focals/
          oracle/
          homogeneous/
          observable/
      paper/
        full-date/
        recovery-date/
        cache/
          recovery/
          research/
        bootstrap/
          recovery/
          research/
      publication/
        envelope/
```

Each leaf is either absent or one complete immutable artifact directory.
Existing `base-panel` and `cell-panel` leaves remain solely at their inherited
`panel-v1/...` paths. A caller supplies only `(root, expected coordinates)`;
no writer or loader accepts an arbitrary final leaf path.

`TC` uses the identical grammar with `TC` substituted for `C`, but only panel
indices `10000`, `10001`, and `10002` and only authority stage
`"test-rehearsal"` are valid.

The scratch root may contain only:

```text
S/bootstrap-pycache/
S/worker-<10-digit u32>/pycache/
S/worker-<10-digit u32>/stdout.bin
S/worker-<10-digit u32>/stderr.bin
S/worker-<10-digit u32>/tmp/
```

Every `TMPDIR`, `PYTHONPYCACHEPREFIX`, temporary log, and non-artifact stage
used by the command resolves below `S`. Artifact stages are same-parent hidden
directories below `C` so their final rename is atomic. Any write elsewhere in
the repository is a terminal failure.

The rehearsal applies the same rule with `TS` and `TC` substituted. Neither
command may write into the other command's roots.

## 4. Three explicit execution-source identities

Panel persistence, executable resource code, and the governance authority are
three simultaneously required identities. All use the A020 stable-file
algorithm; their declared path tuples and hash namespaces differ.

### 4.1 Inherited panel source identity

Every `base-panel` and `cell-panel` manifest retains checkpoint snapshot
schema `xid-g2-source-snapshot-v1` and exactly the existing seven paths:

```text
src/xid
configs/g2.toml
configs/g2_population_targets.json
pyproject.toml
uv.lock
.python-version
Makefile
```

Its snapshot algorithm, namespace, manifest object, and loader equality are
unchanged. A resource-stage panel writer/loader separately validates that
exact identity and returns the inherited artifact SHA256 and panel token.

### 4.2 Resource executable source identity

The executable tuple is the panel tuple plus one path:

```text
src/xid
configs/g2.toml
configs/g2_population_targets.json
configs/g2_resource.toml
pyproject.toml
uv.lock
.python-version
Makefile
```

Its namespace is `xid-g2-resource-executable-source-snapshot-v1\n`.
This exact eight-path digest must be identical in the fixed seed-1729
rehearsal and the registered resource run. `configs/g2_resource.toml` contains
only predeclared code-path, shape, schedule, cap, and fixed rehearsal-address
choices. It contains no observed duration, registered outcome, or its own
source hash.

The config authority is byte-exact, not merely semantic. After amendment A026,
the only admissible file is exactly `9799` ASCII bytes with SHA256
`3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`.
It has no BOM or carriage return and ends in exactly one LF. The loader first
checks those byte conditions and digest, decodes ASCII, parses with
`tomllib.loads`, and then compares the complete parsed object to the typed
`ResourceConfig` value compiled from the same frozen literals. Missing or
additional table/key paths, a Python `bool` accepted as an integer, a changed
array length/order, or any changed scalar fails before root mutation.

The exhaustive parsed type tree is independently bound as follows. Recursively
emit one row `[dotted_leaf_path,type]` for every non-table value; sort rows by
UTF-8 path bytes. Type is exactly `"string"`, `"integer"`, `"boolean"`, or,
recursively, `"array[<element-type>;<length>]"`; arrays must be homogeneous,
except that the same recursive descriptor permits the exact nested
`array[array[string;2];2]`. There are exactly `194` rows and:

```text
SHA256(CJSON([
  "xid-g2-resource-config-type-tree-v1",
  rows,
]))
= e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3
```

The three namespace values in the TOML intentionally omit LF. The exact
`source.namespace_suffix_rule` value is
`"append-one-lf-before-sha256-v1"`: the snapshot implementation appends one
and only one byte `0x0a` before hashing rows. A stored newline, absent appended
newline, or doubled newline fails the source-identity test.

Every new binary resource-artifact manifest binds this executable snapshot
object. It does not bind the governance documents directly; its
`attempt_sha256` binds the outer authority receipt that does.

### 4.3 Outer A022 authority source identity

The authority tuple is the executable tuple plus exactly five governance
paths:

```text
src/xid
configs/g2.toml
configs/g2_population_targets.json
configs/g2_resource.toml
PREREGISTRATION.md
docs/G2_COMPUTE_PLAN.md
docs/derivations/GATE_G2_RESOURCE_ADMISSION.md
docs/derivations/GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md
docs/predictions/GATE_G2_RESOURCE.md
pyproject.toml
uv.lock
.python-version
Makefile
```

The executable and authority snapshots each use the inherited stable-file,
tracked-plus-untracked algorithm:

1. require the supplied repository root to equal
   `git rev-parse --show-toplevel`;
2. enumerate tracked plus untracked, non-ignored regular files under the
   declared paths using
   `git ls-files --cached --others --exclude-standard`;
3. require every literal non-directory declared path to be present and at
   least one file below `src/xid`;
4. reject invalid UTF-8, non-NFC paths, duplicates, directories, symlinks,
   non-regular files, and a file whose identity changes while it is read;
5. sort by UTF-8 path bytes;
6. encode each row as
   `[relpath, "100755"|"100644", byte_count, file_sha256]`; and
7. hash the exact snapshot's ASCII namespace followed by the exact
   newline-terminated `CJSON(row)` bytes.

At attempt bootstrap, the supervisor resolves `git` once. It applies
`shutil.which("git")` to the inherited bootstrap `PATH`, requires an absolute
result, resolves every symlink component with `realpath`, and requires the
result to be an NFC UTF-8 absolute POSIX path naming a regular non-symlink file.
An `O_RDONLY|O_NOFOLLOW` open is bracketed by `lstat`/`fstat`; device, inode,
mode, byte count, mtime-ns, ctime-ns, and bytes must remain identical through
the read. The resulting `git_executable` object has exactly:

```text
path mode byte_count sha256
```

`mode="100755"`, `byte_count` is positive, and `sha256` hashes the exact
executable bytes. This object is persisted in `attempt.json`. Every successor
revalidates the same path/mode/count/hash before its first Git call, and every
later Git child/control inventory must equal it; a missing or changed binary
is source drift, never permission to resolve another `git`.

Every Git subprocess in this algorithm has cwd equal to the validated
repository root. Its exact command prefix is:

```text
[git_executable_absolute_path,
 "--no-optional-locks",
 "-c","core.fsmonitor=false",
 "-c","core.untrackedCache=false",
 "-c","core.sparseCheckout=false",
 "-c","core.sparseCheckoutCone=false",
 "-c","core.excludesFile=/dev/null",
 "-c","core.attributesFile=/dev/null"]
```

Its complete environment is exactly the key-sorted rows:

```text
[
 ["GIT_ATTR_NOSYSTEM","1"],
 ["GIT_CONFIG_GLOBAL","/dev/null"],
 ["GIT_CONFIG_NOSYSTEM","1"],
 ["GIT_DIR",".git"],
 ["GIT_INDEX_FILE",".git/index"],
 ["GIT_LITERAL_PATHSPECS","1"],
 ["GIT_NO_REPLACE_OBJECTS","1"],
 ["GIT_OPTIONAL_LOCKS","0"],
 ["GIT_WORK_TREE","."],
 ["LANG","C"],
 ["LC_ALL","C"],
]
```

No inherited environment key enters the child. The repository must use one
ordinary `.git` directory, an ordinary version-2 index whose only optional
extension is `TREE`, and a symbolic `HEAD` of exact form
`ref: refs/heads/<safe-ref>\n`, where every ref component satisfies the same
safe-component grammar as Section 3. Index extensions `link`, `sdir`, `UNTR`,
`FSMN`, `REUC`, `EOIE`, `IEOT`, and every unknown extension fail. Nonzero index
stages fail. The index header/version/count, every entry, optional `TREE`
extension, and trailing SHA-1 checksum must parse exactly. Every entry path is
unique NFC UTF-8 with no NUL or unsafe component; entry stage is zero; and
`assume-valid`, `skip-worktree`, `intent-to-add`, and every other
behavior-suppressing or extended entry flag are false. The index object-format
is SHA-1, so every admitted object ID is 20 bytes and terminal `commit` output
is 40 lowercase hex digits.

The direct loose path named by `HEAD`, when present, must be a stable regular
file containing exactly one 40-lowercase-hex object ID plus LF; it may not be
another symbolic ref. When that loose ref is absent, `.git/packed-refs` must
contain exactly one matching direct row for the `HEAD` target and supply its
40-hex object ID. A present packed-refs file is ASCII/LF and admits only an
optional first line whose exact bytes are
`# pack-refs with: peeled fully-peeled sorted \n`, unique
`40hex SP refs/<safe-ref>\n` rows in ref-byte order, and an optional
immediately following `^40hex\n` peeled row. A peeled row is not itself a
direct ref and cannot precede or outnumber its direct row. Symbolic rows,
duplicates, comments elsewhere, blank lines, malformed peeling, CR, or an
unsafe ref fail. Whichever direct source resolves `HEAD` must equal every
terminal `commit` child result.

The local `.git/config` must be ASCII/LF and parse under this deliberately
narrow byte grammar. A section line is exactly `[section]\n` or
`[section "subsection"]\n` with no leading or trailing whitespace. Every key
line is exactly `HTAB key SP = SP value LF`: the single leading byte is `0x09`,
both spaces are `0x20`, `section` and `key` each match
`[a-z][a-z0-9-]*`, a quoted `subsection` satisfies the safe-component grammar,
and `value` is nonempty printable ASCII with no leading or trailing space.
Every section has at least one key line. Blank lines, comments, any HTAB
elsewhere, continuations,
escapes, duplicate semantic `(section,subsection,key)` rows, and implicit
Booleans fail. The admitted semantic rows are exact:

- an unsubsectioned `core` section with
  `repositoryformatversion=0`, `filemode=true`, `bare=false`,
  `logallrefupdates=true`, `ignorecase=true`, and
  `precomposeunicode=true`, each appearing once;
- zero or more `remote "<safe-component>"` sections, each containing exactly
  one nonempty printable-ASCII `url` and one nonempty printable-ASCII `fetch`
  row; and
- zero or more `branch "<safe-component>"` sections, each containing exactly
  one nonempty printable-ASCII `remote`, one nonempty printable-ASCII `merge`,
  and at most one nonempty printable-ASCII `vscode-merge-base` row.

No other section, key, subsection grammar, control byte, leading/trailing value
whitespace, or duplicate row is admitted. In particular, `include`,
`includeIf`, `extensions`, `submodule`, `url`, and every unlisted `core` key
fail. The admitted `remote` and `branch` rows do not affect these four local
commands and remain byte-hash-bound; the six command-relevant `core` values are
fixed above rather than merely assumed inert. `.git/config.worktree`,
`.git/commondir`, `.git/worktrees`, `.git/reftable`,
`.git/objects/info/alternates`, and `.git/info/sparse-checkout` must be absent.
No `.git/sharedindex.*` name may exist. A missing rejection, option, or
environment equality fails. Any Git write or stable-identity change under
`.git` fails before root mutation. This makes the Section 18 inclusion of
`.git` compatible with repeated clean/source checks rather than silently
allowing an index refresh to mutate the outside baseline.

Each source object has exactly:

```text
snapshot_schema snapshot_sha256 git_commit declared_paths_clean
```

The executable `snapshot_schema` is
`"xid-g2-resource-executable-source-snapshot-v1"`; the authority schema is
`"xid-g2-resource-authority-source-snapshot-v1"` and its hash namespace is
`xid-g2-resource-authority-source-snapshot-v1\n`. `git_commit` is one
lowercase Git object digest, and
`declared_paths_clean` is the exact Boolean `true` for public resource
authority. Exactly two full Git-subprocess checks occur before terminal JSON
encoding. The bootstrap check runs before the first worker is created and is
persisted in `attempt.json`; the terminal pre-JSON check runs only after every
issued worker identity is closed, no worker is alive, and every currently
waitable direct child has been reaped, and it is persisted in the selected
terminal JSON. Between those
checks, before and after sealed contract/resource-config loading, immediately
before and after every nonterminal resource-root mutation, before every worker
capability, and after every measurement block, the supervisor performs the
in-process source/control seal defined below. It launches no subprocess and
must reproduce the bootstrap source/control rows, reconstruct all three
snapshot digests from the bootstrap `enumerate` arrays, and revalidate the
runtime/module/boot/publisher identities. The final pre-JSON full check remains
ordinary cumulative work; its twelve children are reaped and accounted before
the JSON cutoff values are encoded. No Git child overlaps a worker.

Terminal publication then uses the marker as a post-JSON resource certificate.
After the exact result/failure JSON is written and fsynced inside the hidden
stage, but before marker encoding, one final full three-identity check runs
while the resource sampler remains live. It launches exactly twelve direct Git
children: for `panel`, `executable`, and `authority` in that order, the roles
are exactly `top-level`, `enumerate`, `commit`, and `clean`; their arguments are
respectively the Section 4 `rev-parse --show-toplevel`, `ls-files`,
`rev-parse HEAD`, and `status --porcelain=v1 --untracked-files=all` commands
with that snapshot's literal path tuple. Every child has the fixed Git
environment/prefix above, a validated PID/start identity, signed `wait4`
status, and byte-normalized child `ru_maxrss`; all twelve must exit zero and be
reaped. An unexpected descendant, missing wait/rusage row, sampler gap, or
tuple/runtime/module/boot/publisher mismatch prevents marker publication.
For a snapshot path tuple `P`, the exact suffix arrays appended to the fixed
prefix are:

```text
top-level = ["rev-parse","--show-toplevel"]
enumerate = ["ls-files","--cached","--others","--exclude-standard",
             "-z","--",*P]
commit    = ["rev-parse","HEAD"]
clean     = ["status","--porcelain=v1","--untracked-files=all",
             "-z","--",*P]
```

No alternate flag, argument order, path order, or extra Git call is admitted.

At the resulting pre-marker guard cutoff, the supervisor performs two
consecutive identical no-follow traversals. Every literal authority file
contributes one row; `src/xid` contributes itself and every recursive directory
or regular-file entry, including Git-ignored entries. Directory rows are
`[relpath,"directory",0,null]`; file rows are
`[relpath,"100755"|"100644",byte_count,file_sha256]`. Rows are NFC UTF-8,
path-byte sorted, and reject a symlink, non-directory/non-regular entry,
duplicate inode alias, or any file/directory identity or child-name change
during either traversal. Define:

```text
terminal_source_seal_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-source-seal-v1",
  rows,
]))
```

The Git decision-input inventory has rows
`[role,path_id,present,mode_or_null,byte_count_or_zero,sha256_or_null]`.
`present` is an exact Boolean. A present path is a stable no-follow regular
file with mode `"100755"` when any execute bit is set and `"100644"` otherwise,
positive or zero byte count, and its exact SHA256. An absent path has exactly
`false,null,0,null`; a symlink, directory, other type, or unstable read fails
rather than becoming an absent row. Repository controls use safe relative
POSIX `path_id`; the executable row uses the literal
`absolute:` followed by the already normalized attempt path.

The role ordinals, cardinalities, paths, and presence rules are exactly:

| Ordinal | Role | Cardinality and `path_id` | Rule |
| --- | --- | --- | --- |
| 0 | `git-executable` | one `absolute:<attempt path>` | required; equals `attempt.git_executable` |
| 1 | `git-index` | one `.git/index` | required; exact restricted index above |
| 2 | `repository-config` | one `.git/config` | required; exact restricted config above |
| 3 | `worktree-config` | one `.git/config.worktree` | required absent |
| 4 | `repository-exclude` | one `.git/info/exclude` | optional file, but row always present |
| 5 | `head` | one `.git/HEAD` | required symbolic HEAD |
| 6 | `head-loose-ref` | one `.git/<safe-ref-from-HEAD>` | optional loose file, but row always present |
| 7 | `packed-refs` | one `.git/packed-refs` | optional file, but row always present |
| 8 | `commondir` | one `.git/commondir` | required absent |
| 9 | `linked-worktrees` | one `.git/worktrees` | required absent |
| 10 | `reftable` | one `.git/reftable` | required absent |
| 11 | `object-alternates` | one `.git/objects/info/alternates` | required absent |
| 12 | `sparse-checkout` | one `.git/info/sparse-checkout` | required absent |
| 13 | `gitignore` | one row for every candidate below | optional file, but every candidate has a row |
| 14 | `repository-attributes` | one `.git/info/attributes` | optional file, but row always present |
| 15 | `gitattributes` | one row for every candidate below | optional file, but every candidate has a row |

The `gitignore` and `gitattributes` candidate directory set is identical: the
repository root, every ancestor directory of every literal authority path, and
every directory row from the terminal source-seal traversal of `src/xid`.
Append `.gitignore` or `.gitattributes`, respectively, to each directory,
deduplicate within the role, and sort by path UTF-8 bytes. Thus absence is
hash-bound and a new ignore, worktree-attribute, or repository-local attribute
rule changes the final seal. The complete inventory is ordered by
`(role_ordinal,path_id_utf8_bytes)`; no lexical role sort or alternate absent
token is valid. The environment and command prefix above disable every
system/global/external config or attribute input; every repository/worktree
attribute, replacement-object, sparse-checkout, and exclude input that remains
relevant is either rejected or represented by this table.
Its digest is:

```text
git_control_input_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-git-control-input-v1",
  fixed_git_environment,
  fixed_git_command_prefix,
  rows,
]))
```

The twelve Git-child rows are:

```text
[child_ordinal, snapshot_kind, command_role, argv,
 pid, process_start_identity, wait_status, ru_maxrss_bytes,
 stdout_byte_count, stdout_sha256,
 stderr_byte_count, stderr_sha256, parsed_stdout]
```

`ru_maxrss_bytes` is the raw Darwin `wait4` value and the Linux value
multiplied by `1024`; any other platform is inadmissible. `child_ordinal` is
contiguous `0..11`, snapshot/role order is the fixed order above, and `argv`
includes the complete absolute-executable prefix plus suffix.
Each child is reaped by exactly
`wait4(issued_pid,&wait_status,0,&child_rusage)`: the return value must equal
`issued_pid`, `WIFEXITED(wait_status)` must be true, and
`WEXITSTATUS(wait_status)` must be zero. The persisted raw `wait_status` is
therefore exact zero. Any `wait4` error, different returned PID, signal exit,
missing rusage, or second reap fails. Stderr is exact empty bytes, so its count
is zero and its SHA256 is the digest of empty bytes. Stdout is capped at
1,048,576 bytes before allocation, and its count/hash cover the exact raw bytes.
`parsed_stdout` is role-specific and reconstructs those bytes exactly:

- `top-level`: the normalized repository-root string, whose raw stdout is its
  UTF-8 bytes plus one LF;
- `enumerate`: the emitted-order array of unique NFC safe relative paths,
  whose raw stdout is each UTF-8 path followed by NUL, or empty bytes for an
  empty array;
- `commit`: one lowercase 40-hex object ID, whose raw stdout is that ASCII
  digest plus one LF; and
- `clean`: the exact empty array and exact empty stdout.

The three `top-level` values equal the validated root, all three `commit`
values equal the attempt source objects' `git_commit`, and every clean array is
empty. For each snapshot, join the enumerate array to the matching file rows in
the enclosing full check's `source_seal`, retain only the declared path tuple,
sort
by path UTF-8 bytes, and apply the common snapshot row grammar with that
snapshot's own exact Section 4.1, 4.2, or 4.3 namespace; the reconstructed
digest must equal the named snapshot SHA256.
Every enumerated path must have exactly one joined file row and every
non-directory declared literal must be enumerated. Therefore a dirty zero-exit
`status`, changed top level/commit, divergent enumeration, or source-byte/mode
change is durable marker failure rather than an unaudited process exit.

```text
git_child_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-git-child-inventory-v1",
  rows,
]))
```

Every full preterminal check has exactly:

```text
check_kind source_seal git_control_inputs git_children check_sha256
```

`check_kind` is `"bootstrap"` or `"terminal-pre-json"`.
`source_seal`, `git_control_inputs`, and `git_children` have exactly
`count,rows,sha256`; their rows and digests are the exact objects above, and
`git_children.count=12`. The issuing supervisor is the parent of every row,
runs the children strictly sequentially while no worker is alive, and requires
the complete wait/output predicates before encoding the check. Exactly:

```text
check_sha256 =
SHA256(CJSON([
  "xid-g2-resource-preterminal-git-check-v1",
  check_kind,
  source_seal,
  git_control_inputs,
  git_children,
]))
```

`attempt.bootstrap_git_check` is the complete `"bootstrap"` object. Each
required intermediate in-process seal recomputes the source and Git-control
rows from stable bytes and requires them to equal that bootstrap object
byte-for-byte. For each of `panel`, `executable`, and `authority`, it then takes
the bootstrap Git-child row whose command role is `enumerate`, joins its
`parsed_stdout` path array to the current source-seal file rows, applies that
snapshot's exact row grammar and namespace, and requires the reconstructed
snapshot digest to equal `attempt.source_snapshots.<kind>.snapshot_sha256`.
It also revalidates the pinned Git executable, runtime, loaded-module
inventory, current boot, and publisher PID/start identity. A changed row,
missing join, extra declared source row, identity drift, or attempted
subprocess makes the current transition terminal.

Every terminal JSON carries `preterminal_git_checks` with exactly:

```text
count bootstrap_check_sha256 terminal_pre_json_check sha256
```

`count=2`; `bootstrap_check_sha256` equals the attempt object's exact
`check_sha256`; and `terminal_pre_json_check` is the complete
`"terminal-pre-json"` object. The terminal check's source/control rows equal
the bootstrap rows byte-for-byte, its three reconstructed source snapshots
equal the attempt snapshots, and:

```text
sha256 =
SHA256(CJSON([
  "xid-g2-resource-preterminal-git-check-inventory-v1",
  [bootstrap_check_sha256, terminal_pre_json_check.check_sha256],
]))
```

Thus the two preterminal child inventories, including all 24 wait/rusage rows,
remain reconstructible from `attempt.json` plus the selected terminal JSON.

The terminal marker's exact `terminal_guard` object is defined in Section 17.
It binds those two seals, all twelve child rows by count/digest, the three
source digests, runtime/module/boot/publisher identities, the dedicated
terminal-publication sampler and Git-child rusage evidence through this cutoff,
no-live-descendant/terminal-waits flags, and the recomputed 25%-margin
publication-RSS admission upper. The marker is written and fsynced only when
every guard predicate passes, then the stage directory is fsynced.

Immediately before rename, the same publisher performs one final in-process
seal. Without a subprocess, import, newly discovered compilation, worktree
mutation, or new thread, it recomputes the terminal source seal, Git
decision-input digest, runtime digest, loaded-module digest, boot identity, and
publisher PID/start identity from stable bytes and already imported objects.
It requires no descendant and waits for at least one successful post-guard
sample before asking the continuously sampling thread to stop. It then joins
the sampler and requires the publisher to be the only remaining live thread. It
then takes one synchronous self-resident/RUSAGE_SELF sample. Let
`last_sampler_sample_perf_counter_ns` be the final successful sampler timestamp,
`final_rss_perf_counter_ns` the synchronous sample timestamp, and
`post_guard_sampled_tree_peak_bytes` the in-memory maximum of every sampler
sample after the marker guard cutoff through sampler shutdown. Exactly:

```text
final_sample_gap_ns =
    final_rss_perf_counter_ns - last_sampler_sample_perf_counter_ns

final_rusage_evidence_bytes =
    final_self_rusage_highwater_bytes
        if terminal_guard.outcome_status == "passed"
    else terminal_guard.publication_rss.observed_publication_envelope_bytes

final_observed_envelope_bytes =
    max(
        terminal_guard.publication_rss.observed_publication_envelope_bytes,
        post_guard_sampled_tree_peak_bytes,
        final_self_resident_bytes,
        final_rusage_evidence_bytes
    )

final_current_margin_upper_bytes =
    ceil_div(5 * final_observed_envelope_bytes, 4)

final_rss_admission_upper_bytes =
    max(
        terminal_guard.publication_rss.rss_admission_upper_bytes,
        final_current_margin_upper_bytes
    )
```

All consecutive sampler gaps through the last sampler sample and
`final_sample_gap_ns` are nonnegative and at most `1000000000`;
`final_observed_envelope_bytes<=2800000000`; and
`final_rss_admission_upper_bytes<=3500000000`. The self-rusage value uses the
same platform-to-byte normalization as every other rusage row. Success can use
its lifetime high water because cumulative run telemetry must pass. Failure
cannot relabel a lifetime high water that selected failure as current
publication RSS, so its historical value remains in `failure.json` while the
dedicated publication segment supplies the close-safety component. After that
pass, only the already-open-dirfd, already-materialized-name no-overwrite
rename and terminal-parent fsync syscalls are legal. Exact visible final-
directory existence is the durable one-bit attestation that this final seal
and its ephemeral values passed.

The no-overwrite directory rename and terminal-parent fsync are the final
resource-root mutations and are not followed by an impossible self-attesting
receipt; source paths are disjoint from all three roots. All post-JSON work is
assigned the fixed `60000000000`-ns terminal-publication accounting charge.
That value is deliberately a conservative projection convention, not a false
observation of its own later marker/rename/parent-fsync latency. The 25% guard
requires the final observed envelope at or below `2800000000` bytes, leaving at
least `700000000` bytes before the hard cap for the syscall-only suffix.

An intermediate in-process tuple mismatch before the final success boundary
selects the ordinary failure lane. Publication of the final success boundary,
or of failure's cleanup-complete final-resume receipt, is the non-resumable
terminal-entry point. From that point, any terminal-pre-JSON check, later full
check, seal, publisher, sampler, process, wait, or RSS failure leaves the
selected attempt forensically incomplete; it cannot launch another full
preterminal check, be renamed or adopted by a successor, or be replaced by the
opposite outcome. No local artifact can
observe its own final parent fsync, and an uncooperative external writer can
still race the last stable read absent an immutable snapshot or enforced writer
lease. Those are explicit trust limits, not claimed evidence.

Every imported `xid` module backed by a `.py` file must resolve below the
snapshotted `src/xid` tree. Its import-time source SHA256, current stable
no-follow source bytes, and a fresh compilation of those same bytes must agree
with its live code object. At the attempt boundary the complete permitted
inventory is exactly:

```text
xid                         src/xid/__init__.py
xid.g2_resource_benchmark   src/xid/g2_resource_benchmark.py
xid.models                  src/xid/models/__init__.py
xid.models.g2_checkpoint    src/xid/models/g2_checkpoint.py
xid.models.g2_paper         src/xid/models/g2_paper.py
xid.models.g2_resource      src/xid/models/g2_resource.py
xid.models.g2_smooth        src/xid/models/g2_smooth.py
xid.sim                     src/xid/sim/__init__.py
xid.sim.g2                  src/xid/sim/g2.py
```

Missing or additional loaded `xid` modules are terminal; implementation may
not choose final module names after rehearsal. Sort the exact
`[qualified_module_name, relpath, source_sha256]` rows by qualified module-name
UTF-8 bytes. Their inventory digest is exactly:

```text
SHA256(CJSON(["xid-g2-resource-module-inventory-v1", rows]))
```

and enters `attempt.json`.

The fixed test-seed rehearsal publishes its observed-duration evidence below
the ignored result/scratch roots, outside all three source tuples. The later
prediction records and seals that evidence before registered authority; it
does not feed observed values back into `configs/g2_resource.toml`.

The rehearsal persists its own then-current authority snapshot. Appending the
quantitative prediction seal necessarily changes the governance tuple, so the
later registered authority snapshot may—and normally will—differ from the
historical rehearsal authority snapshot. Each must remain internally stable
for its own attempt. Only the executable snapshot is required to be identical
between rehearsal and registered execution; no authority-snapshot equality
check may replace that rule.

The attempt carries the three Section 4 source objects under its exact
`source_snapshots` key. Every worker claim, reservation, resume-boundary,
interruption, trace, measurement, result, and failure receipt separately
carries these three flat digest fields:

```text
panel_source_snapshot_sha256
executable_source_snapshot_sha256
authority_source_snapshot_sha256
```

Every trace that uses an inherited panel additionally binds both inherited
artifact SHA256 values and both panel tokens. Equality of one source identity
never stands in for equality of another.

### 4.4 Runtime identity

The runtime object is exactly the inherited checkpoint runtime object:

```text
python_implementation python_version numpy_version system machine byteorder
rng_runtime_sha256 thread_env runtime_sha256
```

`thread_env` has exactly:

```text
BLIS_NUM_THREADS MKL_NUM_THREADS NUMEXPR_NUM_THREADS OMP_NUM_THREADS
OPENBLAS_NUM_THREADS VECLIB_MAXIMUM_THREADS
```

Every value is the string `"1"` for the public command.
`runtime_sha256` remains:

```text
SHA256(CJSON([fingerprint_without_runtime_sha256, thread_env]))
```

The resource run is admitted only on Darwin/arm64 under the frozen M4 runtime.
Hosted Linux exercises fail-closed schemas and process supervision but cannot
substitute its timings.

### 4.5 Exact Darwin process and boot identities

On public Darwin, process start fields come only from
`proc_pidinfo(pid, PROC_PIDTBSDINFO=3, 0, ...)` in
`/usr/lib/libproc.dylib`. The call must return the complete
`struct proc_bsdinfo`, its `pbi_pid` must equal `pid`, and its unsigned
`pbi_start_tvsec` and `pbi_start_tvusec` must be nonnegative with
`pbi_start_tvusec < 1_000_000`. Define:

```text
process_start_identity =
SHA256(CJSON([
  "xid-darwin-process-start-v1",
  pid,
  pbi_start_tvsec,
  pbi_start_tvusec,
]))
```

It is one lowercase 64-hex string. Every process census key is the tuple
`(pid, process_start_identity)`. Failure, a short read, an ABI-size mismatch,
or inconsistent repeated query is terminal.

Boot fields come only from Darwin libc. The supervisor zero-initializes one
`struct timeval tv`, initializes `size_t oldlen=sizeof(struct timeval)`, calls
`sysctlbyname("kern.boottime",&tv,&oldlen,NULL,0)`, and requires return value
zero and `oldlen==sizeof(struct timeval)`. The returned signed `tv.tv_sec` must
be positive and `0 <= tv.tv_usec < 1_000_000`. Define:

```text
boot_identity_sha256 =
SHA256(CJSON([
  "xid-darwin-boot-identity-v1",
  tv_sec,
  tv_usec,
]))
```

This is one lowercase 64-hex string. The supervisor samples it before attempt
publication, in every worker claim, after every completed trace and
measurement block, and at the final complete-hidden-outcome/pre-rename check.
An identity change inside a live worker is terminal. Only the changed-boot
resume predicate in Section 16 may accept a different value. Hosted
non-Darwin tests use an explicitly injected test identity object and can never
satisfy public registered authority.

### 4.6 Exact Darwin resident-memory, descendant, and thread census

Every public RSS sample calls
`proc_pidinfo(pid, PROC_PIDTASKINFO, 0, struct proc_taskinfo)` from
`/usr/lib/libproc.dylib`, requires the complete ABI-sized return, and uses the
unsigned `pti_resident_size` as `instantaneous_resident_bytes`. It brackets
that call with two Section 4.5 start-identity reads; both identities must equal
the expected `(pid,process_start_identity)`. `pti_threadnum` is the native
thread count for that same stable process.

At bootstrap the supervisor preallocates two zeroed `pid_t[1024]` census
buffers and one non-reentrant `process_census_lock`. The sampler holds that
lock across each complete tree census and its task-info samples. The supervisor
holds it while it forks/spawns and then records a permitted worker or Git
PID/start identity, and while it records the eventual wait/reaped transition;
issued table rows are retained through terminal closure. Thus a child cannot be
born between the two fills without already being in the permitted table. One
complete child census for parent `p` is exactly:

1. zero one complete buffer, set `errno=0`, call
   `proc_listchildpids(p,buffer,1024*sizeof(pid_t))`, require unchanged zero
   errno, and require a returned count in `0..1023`;
2. retain exactly the returned prefix, reject a nonpositive PID or duplicate,
   and sort numerically; and
3. repeat steps 1--2 into the other buffer and require identical counts and
   sorted PID rows.

The fixed oversized fill is the truncation guard: a returned count of `1024`,
negative return, changed returned count, or unused nonzero buffer word fails.
The null-buffer form is forbidden because Darwin exposes it only as a sizing
hint and it is not the selected parent's child count. At each 50-ms tree sample, the supervisor
performs that complete census, validates every child's start identity, and
rejects a child outside the currently issued worker/Git table. It applies
the same complete census to every direct child and requires zero grandchildren.
An expected child that exits during a count/fill/identity bracket contributes
no favorable sample: that sample is discarded, the supervisor supplies its
exact `wait4`/rusage row, and the sampler retries; the one-second gap rule still
applies. An unexpected PID, reused identity, child-set change not explained by
an already-issued expected exit, or unclosed expected exit is terminal. A
successful sample is the sum of stable instantaneous resident bytes for the
supervisor and every validated live direct child. Any short task-info read,
nonzero grandchild set, overflow, or ABI mismatch fails that sample and cannot
become a favorable observation.

There is at most one issued worker child alive at a time. Kernel 14's
terminal-close “probe” is receipt work performed inside that ordinary worker;
it is not a distinct child-process role. Git children exist only in the
bootstrap, terminal pre-JSON, or terminal post-JSON full source checks. Each
twelve-child set runs sequentially: bootstrap before the first worker;
terminal pre-JSON after every issued worker identity is closed, no worker is
alive, and every currently waitable direct child has been reaped; and terminal
post-JSON after the selected JSON is fsynced. Intermediate source/control seals are
subprocess-free. Git children are wait-only: a missing Git wait/rusage row
makes that check or terminal publication forensically incomplete and can never
be replaced by a Section 16 process-death proof.

Every successful `wait4` return for a worker appends exactly one cumulative
worker-wait row:

```text
[worker_index, worker_claim_sha256, pid, process_start_identity,
 boot_identity_sha256, post_wait_perf_counter_ns,
 wait_status, ru_maxrss_bytes, watchdog_arm_kind, watchdog_arm_sha256,
 work_deadline_perf_counter_ns, reap_deadline_perf_counter_ns,
 termination_reason, termination_requested_perf_counter_ns]
```

`worker_index` and `worker_claim_sha256` join the exact durable claim whose
PID/start/boot fields equal the row. The supervisor zero-initializes
`struct rusage`, calls
`wait4(issued_pid,&wait_status,0,&child_rusage)`, requires the returned PID to
equal `issued_pid`, samples `post_wait_perf_counter_ns` immediately afterward,
requires it not later than the persisted reap deadline, requires
`child_rusage.ru_maxrss >= 0`, and converts that value to bytes exactly as in
Section 4.3. Raw `wait_status` is a signed 32-bit integer. Success additionally
requires a normal zero exit; a failure row preserves the actual raw status.
`watchdog_arm_kind` is `"worker-launch-intent"`, `"boundary"`,
`"cleanup-intent"`, or `"interruption"` and `watchdog_arm_sha256` identifies
the exact durable arm-bearing claim/receipt whose two deadline fields equal the
row. An ordinary exit uses `termination_reason="worker-exit"` and a null
termination-request time. A timeout uses `termination_reason="work-timeout"`,
requires a nonnull request time not later than the work deadline, and still
requires `wait4` not later than the separate reap deadline. No deadline may
first appear in a wait row or be recomputed from a later clock.
Rows are ordered by strictly increasing `worker_index`, with no omitted or
duplicate reaped worker. The row's canonical encoding including terminal LF
must be at most `maximum_worker_wait_row_bytes=512` before it is appended.

Every cumulative `worker_waits` object has exactly `count,rows,sha256`, where
`count=len(rows)` and:

```text
sha256 =
SHA256(CJSON([
  "xid-g2-resource-worker-wait-inventory-v1",
  rows,
]))
```

The canonical empty object has zero rows and that domain's empty digest.
Every boundary, cleanup intent, trace, interruption, and terminal RSS cutoff
persists the complete cumulative object then known. A later object must have
the earlier durable rows as an exact prefix and may append only newly reaped
workers. Its byte-normalized `ru_maxrss_bytes` values independently reconstruct
the worker component of every cumulative rusage envelope. A worker identity
closed only by double absence or boot change has no invented wait row.

At any preterminal cutoff,
`preterminal_git_rusage_highwater_bytes` is the maximum
`ru_maxrss_bytes` over every Git-child row in every complete full preterminal
check available by that cutoff: the bootstrap check at all durable cutoffs,
plus the terminal pre-JSON check only at the terminal cutoff. It is never
derived from the later post-JSON certificate. Because the bootstrap check, all
workers, and the terminal pre-JSON check are mutually nonoverlapping, every
cumulative rusage envelope uses:

```text
rusage_highwater_envelope_bytes =
    supervisor_rusage_highwater_bytes
    + max(
        max([row[7] for row in worker_waits.rows], default=0),
        preterminal_git_rusage_highwater_bytes
    )
```

The scalar must reconstruct exactly from `attempt.bootstrap_git_check` and,
when present, the selected terminal JSON's complete
`terminal_pre_json_check`. Omitting a complete check, row, or higher child
value fails the envelope.

After the terminal sampler joins, the final in-process seal repeats the
supervisor task-info/start-identity bracket and requires
`pti_threadnum==1`; this is the exact meaning of “the publisher is the only
remaining live thread.” Its `final_self_resident_bytes` is that same
`pti_resident_size`. For `final_self_rusage_highwater_bytes`, the supervisor
zero-initializes one `struct rusage ru`, calls
`getrusage(RUSAGE_SELF,&ru)`, requires return value zero and
`ru.ru_maxrss >= 0`, rejects conversion outside unsigned 64-bit range, and
persists the resulting Darwin byte count. Hosted non-Darwin tests use an
explicit injected census/RSS adapter and cannot satisfy registered authority.

## 5. Common immutable artifact state machine

Before any panel or new-artifact operation, the outer resource worker pins
`C`, acquires its nonblocking exclusive resource-run lease, publishes
mode-`0600` `C/.xid-g2-resource-owner`, and pre-reserves against the decimal
`2,000,000,000`-byte cap. The owner marker has exactly:

```text
schema_version attempt_sha256 worker_claim_sha256 pid
process_start_identity executable_source_snapshot_sha256
authority_source_snapshot_sha256 resource_config_sha256
```

The exact resource-stage panel entry points require a process-local owner
capability minted from that pinned descriptor. They use the existing panel
serialization/validation internals but never call, modify, or bypass a C0015
test-stage entry point. The outer owner performs the stricter decimal-cap
reservation before the inherited codec's generic ceiling is consulted.

On clean worker exit the marker is removed and `C` is fsynced. On an admitted
resume, a predecessor marker may be removed only after the Section 16
signal-or-boot predicate proves that its exact worker is dead and the removal
is durably fsynced. No other stale-marker guess is permitted.

Each new binary artifact has only these valid states:

```text
ABSENT
  -> acquire exclusive root lease
  -> reserve complete logical and allocated capacity
  -> create same-parent hidden stage
  -> write/fsync exact NPY payloads in manifest order
  -> write/fsync manifest.json
  -> write/fsync _SUCCESS last
  -> fsync stage
  -> no-overwrite same-parent rename
  -> fsync final parent
PUBLISHED
```

Stage names are byte-derived, not random or caller-selected. For an artifact
directory with final path `P/name/`, the only stage is
`P/.name.xid-g2-artifact-stage-v1/`. Creation is exclusive and any existing
stage is handled only by Section 16's exact debris rule; no alternate suffix,
counter, PID, nonce, or retry name is permitted.

This stage rule also applies to both separately derived A022
registered-resource-stage and test-rehearsal-stage `base-panel` and
`cell-panel` writers, while their final bytes, kinds, paths, manifests, and
digests remain inherited exactly. It does not alter or wrap the legacy C0015
test-stage writer, whose existing temporary-stage behavior remains outside
A022 authority.

An existing final destination is immutable. Missing or extra entries, a stage,
symlink, non-regular child, multiple-link child, missing `_SUCCESS`, noncanonical
JSON, bad NPY header, byte-count mismatch, hash mismatch, source/runtime/
attempt mismatch, or unexpected kind is invalid and is never repaired in
place.

The writer and loader inherit the checkpoint codec's pinned-root descriptor,
no-follow relative opens, one-read file snapshot, shared/exclusive advisory
lease, durable crash marker, complete pre-mutation reservation, post-mutation
cap check, file/directory fsync, and uncertain-publication behavior. The
binding tree limit is decimal `2,000,000,000` bytes, not the codec's larger
generic `2 * 1024**3` constant.

A valid inherited panel at its exact address is loaded and reused. An invalid,
partial, or unexpected inherited panel path is terminal and is never deleted
or regenerated in place.

## 6. Exact common manifest and digest

Every new binary artifact `manifest.json` has exactly:

```text
schema_version artifact_kind authority_stage contract execution_source runtime
attempt_sha256 creation address_domain benchmark_coordinate completion
parents payloads
```

`schema_version` is integer `1`. `artifact_kind` is one of the eleven new
kinds.
`authority_stage` is exactly `"test-rehearsal"` or
`"registered-resource"`. Its attempt, seed, namespace type, root, panel range,
and loader must all agree; a caller cannot select the string independently.

`contract` has exactly:

```text
config_schema_version target_schema_version target_config_schema_version
rng_key_schema_version design_id target_design_id seals
resource_config_sha256
```

`seals` has exactly:

```text
config_sha256 target_raw_sha256 target_semantic_sha256 lasso_ratio_sha256
```

Every schema version is a positive `u32`; both design identifiers are exact
nonempty ASCII strings; all five digest values are `sha256`.

`execution_source` is the exact four-key executable source object in
Section 4.2.
`runtime` is the exact runtime object in Section 4. `attempt_sha256` equals
SHA256 over exact `TR/attempt.json` bytes for stage `"test-rehearsal"` or
exact `R/attempt.json` bytes for stage `"registered-resource"`.

`creation` has exactly:

```text
trace_index kernel_id kernel_variant panel_index
```

`trace_index` and `panel_index` are `u32`; `kernel_id` is an integer in
`1..14`; and `kernel_variant` is exactly `"default"`, `"recovery"`, or
`"research"`. The artifact kind constrains the permitted kernel:

| Kind | Kernel | Variant |
| --- | ---: | --- |
| null batch | 8 | default |
| full paper date | 11 | default |
| recovery paper date | 12 | default |
| paper cache fixture | 13 | recovery or research |
| paper bootstrap batch | 13 | recovery or research |
| publication envelope | 14 | default |
| resume base panel | 1 | default |
| resume cell panel | 2 | default |
| resume bootstrap weights | 3 | default |
| resume paper bootstrap weights | 13 | recovery or research |
| resume candidate focals | 4, 5, or 6 | default |

`parents` is an ordered array of exact two-string arrays
`[role, artifact_sha256]`. Roles are ASCII, unique, and sorted by role bytes.
The exact per-kind parent roles are fixed in Section 8.

Each `payloads` entry has exactly:

```text
name npy_format dtype shape data_bytes file_bytes data_offset sha256
```

`name` is the exact filename from Section 7, `npy_format` is `"1.0"`,
`dtype` is `"<f8"`, `shape` is the exact positive-`u32` dimension array,
`data_bytes` is exactly `8 * product(shape)`, `data_offset` is exactly `128`,
`file_bytes` is exactly `data_bytes + 128`, and `sha256` hashes the complete
NPY file. Payload entries and payload writes use the Section 7 order.

For a positive dimension array `shape`, define the ASCII bytes:

```text
shape_literal =
    "(" + ", ".join(decimal(d) for d in shape)
        + ("," if len(shape) == 1 else "") + ")"

dict_bytes =
    b"{'descr': '<f8', 'fortran_order': False, 'shape': "
    + ASCII(shape_literal)
    + b", }"

header_len = 118
pad = 118 - len(dict_bytes) - 1
header = dict_bytes + b" " * pad + b"\n"
```

`decimal(d)` is unsigned base-10 ASCII with no sign or leading zero.
`pad` must be nonnegative and `len(header)` must equal `118`. The complete
file is exactly:

```text
b"\x93NUMPY"
+ b"\x01\x00"
+ uint16_little_endian(118)
+ header
+ little_endian_float64_C_order_data
```

so numeric data begins at byte `128` and EOF follows the exact data bytes.
The loader independently reconstructs these first 128 bytes and requires
byte-for-byte equality before decoding; semantic dictionary equivalence is
insufficient. If this grammar cannot represent a frozen shape, the
deterministic test fails rather than amending an observed resource run.
Pickle, object dtype, structured dtype, subdtype, Fortran order, nonfinite
payloads, trailing bytes, and a complete file over 5,242,880 bytes fail.

Define, with payload pairs in manifest order:

```text
manifest_sha256 = SHA256(exact manifest.json bytes)

artifact_sha256 = SHA256(CJSON([
  "xid-g2-resource-artifact-v1",
  artifact_kind,
  manifest_sha256,
  [[payload_name, payload_sha256], ...],
]))
```

`_SUCCESS` has exactly:

```text
schema_version artifact_kind manifest_sha256 artifact_sha256
payload_sha256s complete
```

`schema_version` is `1`, `complete` is exact `true`, and
`payload_sha256s` is the exact object mapping only the permitted payload names
to their SHA256 values. `_SUCCESS` is excluded from `artifact_sha256`.

Artifact manifests deliberately contain no duration, final tree size, or
post-publication RSS field. Those values cannot be known before the bytes that
would contain them are published. The later trace receipt binds the artifact
SHA256 and measures publication, reload, cleanup, RSS, and disk without a
self-referential hash.

## 7. Exact payload inventory

### 7.1 `resource-null-batch-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/null-batch/
  batch.npy
  manifest.json
  _SUCCESS
```

Payload:

| Name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| `batch.npy` | `(25, 3, 9)` | 5,400 | 5,528 |

For cold, equal-context, and validation traces, values are the 25 actual
bootstrap focal estimates for the three candidates and nine frozen nodes in
replicate/candidate/node order. For a research trace, the available
`(25, 3, 1)` focal values are copied byte-for-byte across the nine node slots.
The latter fill rule exercises the frozen largest-batch I/O unit and is not
represented as nine scientific estimates.

### 7.2 `resource-paper-full-date-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/paper/full-date/
  summary.npy
  manifest.json
  _SUCCESS
```

Payload:

| Name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| `summary.npy` | `(8460,)` | 67,680 | 67,808 |

The values are one actual issued full six-spec paper-date summary at paper
date index `0`.

### 7.3 `resource-paper-recovery-date-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/paper/recovery-date/
  summary.npy
  manifest.json
  _SUCCESS
```

Payload:

| Name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| `summary.npy` | `(960,)` | 7,680 | 7,808 |

The values are one actual issued `CI_I`-recovery summary at paper date index
`1`.

### 7.4 `resource-paper-cache-fixture-v1`

Recovery leaf:

```text
C/resource-v1/panel-<10-digit b>/paper/cache/recovery/
  cache-000.npy
  manifest.json
  _SUCCESS
```

Research leaf:

```text
C/resource-v1/panel-<10-digit b>/paper/cache/research/
  cache-000.npy
  cache-001.npy
  cache-002.npy
  cache-003.npy
  manifest.json
  _SUCCESS
```

Payloads:

| Variant/name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| recovery `cache-000.npy` | `(252, 960)` | 1,935,360 | 1,935,488 |
| research each `cache-000.npy` through `cache-003.npy` | `(63, 8460)` | 4,263,840 | 4,263,968 |

Recovery row `d` is an exact byte copy of the parent recovery summary.
Research global row `d = 63*s + i` in shard `s`, local row `i`, is an exact
byte copy of the parent full summary. The four research shards therefore
contain exactly 252 rows and 17,055,360 numeric bytes.

### 7.5 `resource-paper-bootstrap-batch-v1`

Recovery and research leaves are:

```text
C/resource-v1/panel-<10-digit b>/paper/bootstrap/recovery/
C/resource-v1/panel-<10-digit b>/paper/bootstrap/research/
```

Each contains:

```text
batch.npy
manifest.json
_SUCCESS
```

Payloads:

| Variant | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| recovery | `(25, 960)` | 192,000 | 192,128 |
| research | `(25, 8460)` | 1,692,000 | 1,692,128 |

For replicate `r` and field `c`, the exact operation is:

```text
batch[r,c] = sum(
    weights[r,d] * cache[d,c]
    for d in range(252)
)
```

using the production accumulation implementation and order. The 25 weight
rows are the actual resource-paper bootstrap replicates `0..24`; the cache is
the exact loaded fixture named as parent.

### 7.6 `resource-publication-envelope-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/publication/envelope/
  part-000.npy
  ...
  part-049.npy
  manifest.json
  _SUCCESS
```

Every shard has:

| Shape | Data bytes | File bytes |
| --- | ---: | ---: |
| `(595000,)` | 4,760,000 | 4,760,128 |

For shard `s in 0..49` and local index `j in 0..594999`:

```text
part_s[j] = float64(s * 595000 + j)
```

All integers are below `2**53` and therefore exactly represented. The ordered
50-shard envelope contains exactly `238,000,000` numeric bytes. Payload order
is `part-000.npy` through `part-049.npy`.

### 7.7 `resource-resume-base-panel-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/resume/base-panel/
  x0tx0_upper.npy
  manifest.json
  _SUCCESS
```

Payload:

| Name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| `x0tx0_upper.npy` | `(252, 2016)` | 4,064,256 | 4,064,384 |

The array equals the issued k1 base panel byte-for-byte. This artifact is
published only as part of the indivisible k1+k2 operand epoch and is never a
k9 timing artifact.

### 7.8 `resource-resume-cell-panel-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/resume/cell-panel/
  x0ty.npy
  yty_upper.npy
  manifest.json
  _SUCCESS
```

Payloads, in this order:

| Name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| `x0ty.npy` | `(252, 63, 30)` | 3,810,240 | 3,810,368 |
| `yty_upper.npy` | `(252, 465)` | 937,440 | 937,568 |

The arrays equal the issued k2 cell panel byte-for-byte. Together, the base
and cell resume payloads contain exactly `8,811,936` numeric bytes.

For both resume-panel kinds, `benchmark_coordinate` has exactly:

```text
resume_role panel_manifest panel_manifest_sha256 panel_artifact_sha256
```

`resume_role` is `"base-panel"` or `"cell-panel"`. `panel_manifest` is the
exact decoded C0015 `base-panel` or `cell-panel` manifest object from
`GATE_G2_CHECKPOINT_AUTHORITY.md` Section 5.1, including its complete receipt
arrays, design hashes, dimensions, response map, telemetry, completion, and
panel token. Its payload descriptors name and hash the same NPY files in the
outer resume artifact. For the cell object, its parent binds the resume base
object's exact `panel_artifact_sha256` and panel token. Define:

```text
panel_manifest_sha256 = SHA256(CJSON(panel_manifest))

panel_artifact_sha256 = SHA256(CJSON([
  "xid-g2-panel-artifact-v1",
  panel_manifest.artifact_kind,
  panel_manifest_sha256,
  [[payload.name, payload.sha256] for payload in panel_manifest.payloads],
]))
```

The four fields must reproduce the existing `_base_panel_token` or
`_cell_panel_token` result from the decoded immutable object. No elapsed,
receipt, response-map, source, or parent field may be synthesized on load.

### 7.9 `resource-resume-bootstrap-weights-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/resume/bootstrap-weights/
  weights.npy
  manifest.json
  _SUCCESS
```

Payload:

| Name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| `weights.npy` | `(25, 252)` | 50,400 | 50,528 |

Rows are the exact resource-smooth bootstrap replicate weights `0..24` in
replicate/date order. Every value is a finite nonnegative integer-valued
float64 and each row sums exactly to `252`.
`benchmark_coordinate` has exactly:

```text
resume_role weight_inventory_sha256 aggregate_count
aggregate_token_inventory_sha256
```

with `resume_role="bootstrap-weights"` and `aggregate_count=25`.
`weight_inventory_sha256` is Section 8's exact weight inventory over the
licensed addresses and row-byte hashes.
`aggregate_token_inventory_sha256` is:

```text
SHA256(CJSON([
  "xid-g2-resource-resume-aggregate-token-inventory-v1",
  [[r, aggregate_token_r] for r in range(25)],
]))
```

where `aggregate_token_r` is the exact existing
`xid-g2-smooth-aggregate-v1` token for the issued aggregate built from row
`r`. A resumed worker loads the saved rows, recomputes all 25 aggregates in
order, and requires this digest before any fit; it never constructs a
bootstrap RNG for completed k3 work.

### 7.9a `resource-resume-paper-bootstrap-weights-v1`

Leaf:

```text
C/resource-v1/panel-<10-digit b>/resume/paper-bootstrap-weights/
  weights.npy
  manifest.json
  _SUCCESS
```

The rehearsal substitutes `TC`. Its sole payload is:

| Name | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| `weights.npy` | `(25, 252)` | 50,400 | 50,528 |

Rows are the exact resource-paper bootstrap replicate weights `0..24` in
replicate/date order. Every value is a finite nonnegative integer-valued
float64 and each row sums exactly to `252`. `benchmark_coordinate` has exactly:

```text
resume_role weight_inventory_sha256 replicate_count date_count
producer_record_position last_consumer_record_position
```

`resume_role="paper-bootstrap-weights"`, `replicate_count=25`, and
`date_count=252`. Producer/last-consumer positions are `12/13` for
cold/equal/rehearsal, `12/12` for validation, and `13/13` for research.
`weight_inventory_sha256` is Section 8's exact paper-parent inventory over the
25 licensed entropy tuples and row-byte hashes.

Creation belongs to the first positive kernel-13 position and cleanup belongs
to the last positive kernel-13 position. Both positive equal-context
kernel-13 variants load this one artifact. A zero-unit variant neither draws
nor writes. The loaded private wrapper is registered in the existing
`_RESOURCE_ARTIFACT_REGISTRY`; this kind adds no registry name and every
scientific, validation, research, or generic loader rejects it.

### 7.10 `resource-resume-candidate-focals-v1`

Leaves:

```text
C/resource-v1/panel-<10-digit b>/resume/focals/oracle/
C/resource-v1/panel-<10-digit b>/resume/focals/homogeneous/
C/resource-v1/panel-<10-digit b>/resume/focals/observable/
```

Each contains:

```text
focals.npy
manifest.json
_SUCCESS
```

Payload:

| Role | Shape | Data bytes | File bytes |
| --- | --- | ---: | ---: |
| rehearsal/equal/validation | `(25, 9)` | 1,800 | 1,928 |
| research | `(25, 1)` | 200 | 328 |

Rows are bootstrap replicates and columns are the frozen node order. The
candidate path is `"oracle"`, `"homogeneous"`, or `"observable"` for k4, k5,
or k6 respectively. `benchmark_coordinate` has exactly:

```text
resume_role candidate node_count replicate_count fit_output_inventory_sha256
```

Fixed values are `resume_role="candidate-focals"`, `replicate_count=25`,
and `node_count=9` except research, where it is `1`. The fit-output inventory
is ordered replicate-major then node-major. For oracle/observable, each row
contains the coefficient-array SHA256 plus exact `.hex()` strings for
`smallest_eigenvalue`, `largest_eigenvalue`, `penalty_condition`,
`penalty_floor`, `penalty`, and `post_condition_number`. For homogeneous,
each row contains `intercept.hex()`, the slopes-array SHA256,
singular-values-array SHA256, and `condition_number.hex()`. Its digest is:

```text
SHA256(CJSON([
  "xid-g2-resource-resume-fit-output-inventory-v1",
  candidate,
  rows,
]))
```

The focal payload is derived from those same validated fit objects. It cannot
substitute for a fit in a scientific result or mint aggregate/fit authority.

## 8. Address, benchmark-coordinate, completion, and parent domains

`address_domain` is JSON null or has exactly:

```text
dgp bootstrap
```

A non-null `dgp` has exactly:

```text
master_seed config_schema_version rng_key_schema_version stream phase_id
scenario_id parent_phase_id parent_scenario_id n_dates panel_index cell_key
date_range component_ids replicate_index
```

A non-null `bootstrap` has exactly:

```text
master_seed config_schema_version rng_key_schema_version phase_id scenario_id
parent_phase_id parent_scenario_id n_dates panel_index cell_key date_index
component_id replicate_range
```

The only licensed values are:

```text
master_seed                1729 for authority_stage "test-rehearsal";
                           2026071529 for "registered-resource"
config/rng schema          exact frozen contract values
n_dates                    252
panel_index                creation.panel_index
cell_key                   0

smooth DGP                 stream resource_smooth, phase/scenario 10/0,
                           parents 0/0, components [1,2,3,4,5],
                           replicate_index 0
paper DGP                  stream resource_paper, phase/scenario 10/1,
                           parents 0/0, components [1,2,3,4,5],
                           replicate_index 0
smooth bootstrap           phase/scenario 40/0, parents 10/0,
                           date_index 0, component 6
paper bootstrap            phase/scenario 40/0, parents 10/1,
                           date_index 0, component 6
```

Test-rehearsal panel indices are exactly `10000..10002`; registered panel
indices are exactly those licensed by the contiguous reservation ledger
starting at zero. A stage/seed/panel mismatch fails before filesystem access
or `SeedSequence`.

Ranges are half-open two-element `u32` arrays. `benchmark_coordinate` is null
or the exact per-kind object below. `completion` always has exactly:

```text
completed_date_range completed_replicate_range completed_payload_range
```

Each range is null or a half-open two-element `u32` array.

The exact per-kind rules are:

| Kind/variant | DGP range | Bootstrap range | Completion | Parents | Benchmark coordinate |
| --- | --- | --- | --- | --- | --- |
| resume base panel | smooth dates `[0,252)` | null | dates `[0,252)`, reps null, payloads `[0,1)` | none | Section 7.7 exact object |
| resume cell panel | smooth dates `[0,252)` | null | dates `[0,252)`, reps null, payloads `[0,2)` | `resume-base-panel` | Section 7.8 exact object |
| resume bootstrap weights | smooth dates `[0,252)` | smooth reps `[0,25)` | dates `[0,252)`, reps `[0,25)`, payloads `[0,1)` | `resume-base-panel`, `resume-cell-panel` | Section 7.9 exact object |
| resume paper bootstrap weights | null | paper reps `[0,25)` | dates null, reps `[0,25)`, payloads `[0,1)` | none | Section 7.9a exact object |
| resume candidate focals, each candidate | smooth dates `[0,252)` | smooth reps `[0,25)` | dates `[0,252)`, reps `[0,25)`, payloads `[0,1)` | `resume-bootstrap-weights` | Section 7.10 exact object |
| null batch, actual | smooth dates `[0,252)` | smooth reps `[0,25)` | dates `[0,252)`, reps `[0,25)`, payloads `[0,1)` | production panels plus three resume-focal parents | `{"fill_rule":"actual-nine-node","variant":"validation-shape"}` |
| null batch, research | smooth dates `[0,252)` | smooth reps `[0,25)` | dates `[0,252)`, reps `[0,25)`, payloads `[0,1)` | production panels plus three resume-focal parents | `{"fill_rule":"repeat-single-node","variant":"research-shape"}` |
| full paper date | paper dates `[0,1)` | null | dates `[0,1)`, reps null, payloads `[0,1)` | none | null |
| recovery paper date | paper dates `[1,2)` | null | dates `[1,2)`, reps null, payloads `[0,1)` | none | null |
| recovery cache | null | null | dates null, reps null, payloads `[0,1)` | `paper-date` | exact object below |
| research cache | null | null | dates null, reps null, payloads `[0,4)` | `paper-date` | exact object below |
| recovery bootstrap | null | paper reps `[0,25)` | dates null, reps `[0,25)`, payloads `[0,1)` | `paper-cache`, `resume-paper-bootstrap-weights` | exact object below |
| research bootstrap | null | paper reps `[0,25)` | dates null, reps `[0,25)`, payloads `[0,1)` | `paper-cache`, `resume-paper-bootstrap-weights` | exact object below |
| publication envelope | null | null | dates null, reps null, payloads `[0,50)` | none | exact object below |

Cache benchmark coordinates have exactly:

```text
variant fill_rule source_artifact_sha256 row_count field_count shard_count
```

Values are:

```text
recovery "repeat-parent-row" <parent recovery SHA> 252 960 1
research "repeat-parent-row" <parent full SHA>     252 8460 4
```

Bootstrap benchmark coordinates have exactly:

```text
variant accumulation_rule cache_artifact_sha256 weight_inventory_sha256
replicate_count date_count field_count
```

`accumulation_rule` is
`"row-major-r-d-c-production-order-v1"`, replicate/date counts are `25` and
`252`, and field count is `960` or `8460`.

Publication benchmark coordinates have exactly:

```text
fill_rule shard_count elements_per_shard first_value last_value
```

with values:

```text
"global-nonnegative-integer-index-f64-v1" 50 595000 0 29749999
```

The exact parent-role arrays are:

```text
resume base panel:
  []

resume cell panel:
  [["resume-base-panel", <resume base artifact SHA>]]

resume bootstrap weights:
  [["resume-base-panel", <resume base artifact SHA>],
   ["resume-cell-panel", <resume cell artifact SHA>]]

each resume candidate-focals artifact:
  [["resume-bootstrap-weights", <resume weights artifact SHA>]]

null batch:
  [["base-panel", <inherited base artifact SHA>],
   ["cell-panel", <inherited cell artifact SHA>],
   ["resume-homogeneous-focals", <homogeneous resume artifact SHA>],
   ["resume-observable-focals", <observable resume artifact SHA>],
   ["resume-oracle-focals", <oracle resume artifact SHA>]]

cache:
  [["paper-date", <full or recovery date artifact SHA>]]

bootstrap:
  [["paper-cache", <cache fixture artifact SHA>],
   ["resume-paper-bootstrap-weights", <paper weights artifact SHA>]]

paper date, resume base panel, resume paper bootstrap weights, and publication:
  []
```

Every resume parent hash names the outer resource artifact SHA256, not the
embedded C0015 panel token. Parent order is the literal order above. The
resume base/cell inner manifest relationship is additionally validated by
Section 7.7--7.8, while the outer parent chain proves the exact attempt-local
durable operand lineage. A null batch whose three focal parents do not match
the exact k4/k5/k6 candidate paths for its trace is invalid.

The bootstrap weight inventory is not a persisted scientific payload. It is
the SHA256 of:

```text
CJSON([
  "xid-g2-resource-weight-inventory-v1",
  panel_index,
  [[replicate_index, entropy_13_words, weights_f64_le_sha256], ...],
])
```

in replicate order `0..24`.

## 9. Loader and issuance rules

There is no generic `load_resource_artifact(kind, path)` that can mint model
authority. Exact stage-specific entry points are required:

```text
write_resource_base_panel_checkpoint(...)
load_resource_base_panel_checkpoint(...)
write_resource_cell_panel_checkpoint(...)
load_resource_cell_panel_checkpoint(...)
write_resource_resume_base_panel(...)
load_resource_resume_base_panel(...)
write_resource_resume_cell_panel(...)
load_resource_resume_cell_panel(...)
write_resource_resume_bootstrap_weights(...)
load_resource_resume_bootstrap_weights(...)
write_resource_resume_paper_bootstrap_weights(...)
load_resource_resume_paper_bootstrap_weights(...)
write_resource_resume_oracle_focals(...)
load_resource_resume_oracle_focals(...)
write_resource_resume_homogeneous_focals(...)
load_resource_resume_homogeneous_focals(...)
write_resource_resume_observable_focals(...)
load_resource_resume_observable_focals(...)
load_resource_null_batch(...)
load_resource_paper_full_date(...)
load_resource_paper_recovery_date(...)
validate_resource_paper_cache_fixture(...)
load_resource_paper_bootstrap_batch(...)
validate_resource_publication_envelope(...)
```

Each has one separately named rehearsal peer:

```text
write_rehearsal_base_panel_checkpoint(...)
load_rehearsal_base_panel_checkpoint(...)
write_rehearsal_cell_panel_checkpoint(...)
load_rehearsal_cell_panel_checkpoint(...)
write_rehearsal_resume_base_panel(...)
load_rehearsal_resume_base_panel(...)
write_rehearsal_resume_cell_panel(...)
load_rehearsal_resume_cell_panel(...)
write_rehearsal_resume_bootstrap_weights(...)
load_rehearsal_resume_bootstrap_weights(...)
write_rehearsal_resume_paper_bootstrap_weights(...)
load_rehearsal_resume_paper_bootstrap_weights(...)
write_rehearsal_resume_oracle_focals(...)
load_rehearsal_resume_oracle_focals(...)
write_rehearsal_resume_homogeneous_focals(...)
load_rehearsal_resume_homogeneous_focals(...)
write_rehearsal_resume_observable_focals(...)
load_rehearsal_resume_observable_focals(...)
load_rehearsal_null_batch(...)
load_rehearsal_paper_full_date(...)
load_rehearsal_paper_recovery_date(...)
validate_rehearsal_paper_cache_fixture(...)
load_rehearsal_paper_bootstrap_batch(...)
validate_rehearsal_publication_envelope(...)
```

The rehearsal peers require exact `TestRngNamespace`, seed `1729`, the
test-rehearsal attempt digest, roots `TC/TS`, and panels `10000..10002`. The
resource peers require exact `ResourceRngNamespace`, seed `2026071529`, the
registered attempt digest, roots `C/S`, and the registered ledger. They share
private serialization/validation functions only; no public function accepts a
union namespace, stage flag, seed override, root override, or arbitrary path.
The three candidate-specific focal entry points reject a caller-supplied
candidate string; their path and role are constants. Resume writers are
reachable only from the exact record position named by Section 13, and resume
loaders are reachable only while reconstructing the next exact record
prelude. A resume loader can neither publish a production artifact nor return
a scientific receipt.

Every entry point derives its final path, exact expected kind, variant,
coordinates, parent hashes, payload inventory, source/runtime identity, and
attempt digest before filesystem access. Every decoded array is copied into an
exact C-contiguous native-float64 read-only array after verifying little-endian
bytes, shape, finiteness, and EOF.

Only the two paper-date loaders, null-batch loader, paper-bootstrap loader,
smooth-resume-weights loader, paper-resume-weights loader, and three
candidate-specific resume-focal loaders may mint one of the seven issuable new
wrapper classes. Every such issuance is
written inline to the module-owned weak
`_RESOURCE_ARTIFACT_REGISTRY` while the shared root lease is still held. No
other function may write that registry. The registry token binds:

```text
resource kind, exact wrapper identity, attempt SHA, source/runtime SHA,
panel/trace/kernel coordinate, parent artifact SHA values,
payload file SHA values, exact array identities, and array-byte SHA values
```

Cache and publication validators mint no authority. They return only immutable
evidence plus read-only arrays inside the private resource worker. The new
registry is distinct from every inherited registry and is included last in
all live-count vectors.

The two resume-panel loaders are the sole exception to the new-wrapper rule:
after validating the outer resume manifest and its embedded exact C0015
manifest, they reissue the existing read-only base/cell panel types through
the existing `_CONTRACT_BASE_PANEL_REGISTRY` and
`_CONTRACT_CELL_PANEL_REGISTRY` inline issuance paths. Their tokens must equal
the embedded panel tokens byte-for-byte. They cannot write the production
checkpoint path, and the production panel loaders reject the resume kinds.
All temporary resume-issued panels, weight wrappers, focal wrappers, and
recomputed aggregate objects are released and collected before the next
durable boundary.

Every new `resource-*` artifact is benchmark-only. Validation/research loaders,
scientific checkpoint aggregators, phase-result publishers, and any
coefficient-to-truth path reject these kinds before array issuance. A resource
paper summary is an actual computation at a resource address, but it is not a
validation or research summary. A tiled cache row is never a `G2DateReceipt`.
The research-shape null fill is never nine estimator outputs.

Rehearsal artifacts additionally reject every registered-resource loader and
registry; registered artifacts reject every rehearsal loader and registry.

The inherited `base-panel` and `cell-panel` resource objects may be loaded and
aggregated only under the same exact resource attempt and
`ResourceRngNamespace`. Seed/stream/address mismatch prevents their weak
authority from crossing into validation or research.

## 10. Receipt publication

Every reservation, worker-launch intent, worker-birth record, worker claim,
resume-boundary, interruption, cleanup-intent, trace, measurement,
terminal-failure-intent, terminal-failure-resume, and terminal-nonpass-intent
leaf uses one
atomic-directory publication:

```text
ABSENT
  -> create a same-parent hidden stage directory
  -> write/fsync claim.json or receipt.json
  -> write/fsync _SUCCESS last
  -> fsync the stage directory
  -> no-overwrite same-parent rename of the complete directory
  -> fsync parent
PUBLISHED
```

For a receipt directory with final path `P/name/`, the only stage is
`P/.name.xid-g2-receipt-stage-v1/`. It is created exclusively; no alternate
stage spelling is valid.

The A026 launch-intent and terminal-nonpass-intent exceptions create and lock
their one exact third regular file before writing the JSON, then follow the
same marker-last, directory-fsync, rename, and parent-fsync sequence. Their
claim/receipt binds that file's exact bytes and inode identity. No other
receipt kind admits a third entry.

The marker for reservation, worker launch, worker birth, worker claim, resume
boundary, interruption, cleanup-intent, trace, measurement,
terminal-failure-intent, terminal-failure-resume, or terminal-nonpass-intent
receipt has exactly:

```text
schema_version receipt_kind receipt_sha256 complete
```

`schema_version` is `1`, `complete` is `true`, and `receipt_sha256` hashes the
exact `claim.json` or `receipt.json` bytes. `receipt_kind` equals the contained
claim or receipt's exact literal `receipt_kind` byte-for-byte; it may not be a
generic marker label. An existing receipt or marker is immutable. The final
directory is valid only when both regular single-link files exist, the marker
binds the exact receipt, the hidden stage is absent, and no entry exists beyond
that pair except the one exact lock file required for an A026 launch or
nonpass intent. Because no child becomes visible at the final path before the
directory rename, a crash exposes either the prior state or one complete bound
inventory.
A valid complete final discovered after an uncertain rename is reused. An
ordinary hidden stage is protocol state, not debris. Before scheduling any
transition, the supervisor admits exactly one of:

```text
stage absent, final absent
stage has one exact canonical claim.json/receipt.json and no marker, final absent
stage has one exact canonical receipt plus its exact marker, final absent
stage absent, final is one exact complete receipt inventory
```

For either lock-bearing A026 intent, every staged/visible state above also
contains its exact already-locked third file; its absence or mismatch is not
an adoptable state.

For either staged form of an explicitly adoptable nonterminal receipt, a
successor first proves the encoded publisher dead under Section 16. It then
derives and publishes only the missing exact marker, if any, fsyncs the stage,
no-overwrite renames that complete unchanged stage, and fsyncs the parent. The
next durable receipt binds that death proof. A worker-birth stage and a
`terminal_entry=true` final-success boundary stage are never adoptable after
their publisher dies: payload-only and payload-plus-marker states are both
forensically incomplete. The same exception already applies to a
cleanup-complete final failure-resume and to either hidden terminal-outcome
stage.
The same still-live encoded publisher may finish an exact payload-only or
payload-plus-marker final-success boundary stage and then continue terminal
publication. A complete visible `terminal_entry=true` boundary is immutable
evidence, but if its publisher later dies it authorizes no successor Git
check, terminal stage creation, opposite outcome, or other receipt; terminal
publication is forensically incomplete. This boundary is therefore a
non-resumable process-identity cut, not an adoptable checkpoint.
The rehearsal `i=2,p=14` boundary has the same nonadoption rule. Its still-live
publisher may publish the uniquely derived final rehearsal trace receipt and
then enter terminal publication; after publisher death, neither that trace nor
any Git/terminal successor may be published.
Marker-only, partial/corrupt, extra-entry, mismatched, stage-plus-final, or
conflicting states are forensically incomplete. An absent work-boundary stage
commits no current record and therefore selects the exact replay transition.
An absent trace or measurement stage/final may be reconstructed only from its
complete durable prefix and followed by its uniquely derived boundary. Hidden
terminal-failure-intent stages obey the same normalization rule after failure
identity has been selected; their adoption is bound by failure-resume zero.
A hidden nonfinal terminal-failure-resume stage obeys that rule and binds
adoption in its next contiguous receipt. A hidden cleanup-complete
terminal-failure-resume stage whose publisher is dead is instead forensically
incomplete: no next resume may duplicate the cleanup-complete state. None of
these stages can be deleted as debris, changed, or used to reopen work.

Every adoptable ordinary receipt payload encodes its unique publisher.
Registered and rehearsal worker claims use `supervisor_pid` and
`supervisor_start_identity`; reservation, trace, measurement, boundary, and
cleanup-intent payloads use `publisher_supervisor_pid` and
`publisher_supervisor_start_identity`; interruption, failure-intent, and
failure-resume payloads use their already named publisher-supervisor fields.
Worker-launch intents use the publisher-supervisor fields. Worker births use
`publisher_worker_pid` and `publisher_worker_start_identity`, and are valid
only as complete visible pairs created by that still-live bootstrap child.
The encoded identity is revalidated immediately before marker publication.
The temporary kernel-14 terminal-close probe is not an adoptable checkpoint:
after loss, its exact stage/final is deletion-plan debris and kernel 14 is
replayed with the normal penalty.

Only `attempt.json` uses the distinct root-file publisher:

```text
ABSENT
  -> create/fsync sibling stage file
  -> expose final JSON with create-exclusive no-overwrite hard link
  -> fsync parent
  -> unlink stage
  -> fsync parent
  -> require final JSON st_nlink == 1 and stage absent
PUBLISHED
```

For a root or sibling file with final path `P/name`, the only stage file is
`P/.name.xid-g2-file-stage-v1`. It is created exclusively; no alternate
suffix, counter, PID, nonce, or retry name is valid.

The first visible complete `attempt.json` consumes the attempt and has no
marker.

Success and failure outcomes use the nonadoptable atomic-directory publisher
below. Amendment A026 adds a distinct successor-rebuildable forensic nonpass
publisher. For `X=R` or `TR`, the only final paths are:

```text
X/terminal/success/{result.json,_SUCCESS}
X/terminal/failure/{failure.json,_FAILURE}
X/terminal/nonpass/{nonpass.json,_NONPASS}
```

The only stages are respectively
`X/terminal/.success.xid-g2-terminal-stage-v1/` and
`X/terminal/.failure.xid-g2-terminal-stage-v1/`, plus
`X/terminal/.nonpass.xid-g2-terminal-stage-v1/`. A success/failure publisher exclusively
creates the stage and fsyncs `X/terminal`, writes and fsyncs the exact JSON,
writes and fsyncs its exact Section 17 post-JSON terminal-guard marker, fsyncs
the stage directory, performs Section 4.3's final in-process seal and
sampler/process/RSS shutdown checks, no-overwrite renames the whole complete
directory, and fsyncs `X/terminal`. The visible outcome therefore always
contains a complete
JSON/marker pair. A valid complete visible outcome is immutable and selects
that outcome; the opposite final and stage must be absent. Creation of either
unique hidden outcome stage followed by successful completion of its immediate
terminal-parent fsync is the forward-execution terminal cutover and
irrevocably selects that outcome kind. If a crash occurs between exclusive
stage creation and completion of that fsync, an absent stage after recovery is
pre-cutover; an exact surviving stage conservatively locks its outcome kind and
is handled as a dead-publisher hidden stage, so the opposite outcome is never
licensed. The same continuously live publisher may finish its exact
payload-only or complete stage. A valid complete visible
final discovered after an uncertain rename is revalidated and the current
live supervisor fsyncs `X/terminal`; only then is it reusable as durable
outcome evidence. A successor never normalizes a hidden success/failure stage
left by a dead publisher and can never publish the opposite selected outcome.
Instead, the exact terminal-entry receipt plus publisher-death or post-entry
failure evidence licenses only the A026 nonpass-intent and nonpass publisher
defined below. Marker-only, invalid, conflicting, multiple-kind, or uncertain
states can never select success or failure. Abrupt-supervisor-loss unknown
telemetry may select ordinary failure only before publication of the final
success boundary. Loss after that non-resumable terminal-entry point can close
only as terminal nonpass when the exact A026 prerequisites validate.

Every terminal JSON encodes
`publisher_supervisor_pid,publisher_supervisor_start_identity`. A success
publisher equals the final durable boundary publisher and must remain
continuously alive from that boundary's publication through hidden-stage
creation, both Git checks, marker fsync, directory rename, and therefore
outcome visibility. Death before visibility cannot select failure or authorize
another terminal-pre-JSON check; it licenses only terminal nonpass. A failure
publisher equals the mandatory cleanup-complete final-resume publisher and
obeys the same continuous-life rule from final-resume publication through
visibility. If it dies while both failure stage/final are absent, the already
selected failure cannot be certified as failure and a successor may publish
only terminal nonpass; if a hidden stage exists, the general
dead-publisher cutover rule applies; if the exact visible final exists, a
successor may only revalidate it and fsync the terminal parent as above. After
every issued worker identity is closed, no worker is alive, and every currently
waitable direct child has been reaped, the complete terminal-pre-JSON Git check
is performed and enters the selected terminal JSON plus its cumulative RSS
evidence. After JSON fsync, the distinct post-JSON Git certificate runs while
its children can still enter the marker's durable terminal-guard evidence.
Every earlier transition uses only Section 4.3's
subprocess-free in-process seal. The in-process source seal, Git decision
inputs, runtime/module/boot identities, and publisher identity are revalidated
after the marker/stage fsync and before the final resource checks and rename.
Publisher identity is also revalidated before the marker.

Inventory hashes use sorted relative paths:

```text
SHA256(CJSON([
  "xid-g2-resource-receipt-inventory-v1",
  [[relative_receipt_path, receipt_sha256], ...],
]))
```

For every durable inventory, `relative_receipt_path` is the final receipt
directory path relative to the current result root (`R` or `TR`), without a
trailing slash. It names neither `claim.json`/`receipt.json` nor `_SUCCESS`.
Examples are `workers/worker-0000000000`,
`worker-launches/launch-0000000000`,
`worker-births/birth-0000000000`,
`reservations/panel-0000000000`,
`worker-launches/rehearsal-0`,
`worker-births/rehearsal-0`,
`workers/rehearsal-0`, and
`boundaries/rehearsal-0/boundary-00`. Terminal paths are exactly
`terminal/failure-intent` and
`terminal/failure-resumes/resume-<10-digit j>`. Paths are NFC UTF-8, contain no
empty, `.` or `..` component, and are sorted by their UTF-8 bytes. Each
category inventory admits only its exhaustive grammar's directory paths; a
root prefix, category-relative abbreviation, filename suffix, or trailing
slash is invalid. The temporary `S`/`TS` terminal-close probe is deleted inside
its kernel and never enters a durable receipt inventory.

Kernel 14's temporary terminal-close probe uses the ordinary atomic receipt
directory primitive rather than either terminal-outcome publisher. Its leaf is:

```text
S/worker-<10-digit w>/tmp/terminal-close-probe/
  receipt.json
  _SUCCESS
```

and the rehearsal substitutes `TS`. `receipt.json` has exactly:

```text
schema_version receipt_kind status authority_stage attempt_sha256
panel_index padding complete
```

Fixed values are `schema_version=1`,
`receipt_kind="resource-terminal-close-probe-v1"`, `status="probe"`, and
`complete=true`. `authority_stage` is the exact current stage. `padding` is
ASCII `"x"` repeated exactly

```text
1,048,576 - len(CJSON(the same object with padding=""))
```

times, and the final canonical file must be exactly 1,048,576 bytes. A
negative padding length or any other byte count fails. The marker uses this
section's receipt marker schema. Publication, reload, validation,
single-link/stage checks, marker checks, deletion, and parent fsync are all
inside kernel 14. The kernel record binds
`SHA256(CJSON(["xid-g2-terminal-close-probe-evidence-v1",
receipt_sha256, marker_sha256]))`; the probe can mint no artifact or RNG
authority.

### 10.1 One-shot test-seed rehearsal evidence

The only timed measurability command is:

```text
make g2-resource-rehearsal
```

It is one logical, no-retry evidence attempt under seed `1729`; ordinary unit
tests do not create its exact three panel addresses. `TR`, `TC`, and `TS` must
be absent before submission.

Its successful persistent grammar is exactly:

```text
TR/
  attempt.json
  worker-launches/
    rehearsal-0/
      claim.json
      _SUCCESS
    rehearsal-1/
      claim.json
      _SUCCESS
    rehearsal-2/
      claim.json
      _SUCCESS
  worker-births/
    rehearsal-0/
      claim.json
      _SUCCESS
    rehearsal-1/
      claim.json
      _SUCCESS
    rehearsal-2/
      claim.json
      _SUCCESS
  reservations/
    rehearsal-0/
      claim.json
      _SUCCESS
    rehearsal-1/
      claim.json
      _SUCCESS
    rehearsal-2/
      claim.json
      _SUCCESS
  workers/
    rehearsal-0/
      claim.json
      _SUCCESS
    rehearsal-1/
      claim.json
      _SUCCESS
    rehearsal-2/
      claim.json
      _SUCCESS
  boundaries/
    rehearsal-0/
      boundary-00/
        receipt.json
        _SUCCESS
      ...
      boundary-14/
        receipt.json
        _SUCCESS
    rehearsal-1/
      boundary-00/ ... boundary-14/
    rehearsal-2/
      boundary-00/ ... boundary-14/
  cleanups/
    rehearsal-0/
      cleanup-00/
        receipt.json
        _SUCCESS
      ...
      cleanup-03/
        receipt.json
        _SUCCESS
    rehearsal-1/
      cleanup-00/ ... cleanup-03/
    rehearsal-2/
      cleanup-00/ ... cleanup-03/
  traces/
    rehearsal-0/
      receipt.json
      _SUCCESS
    rehearsal-1/
      receipt.json
      _SUCCESS
    rehearsal-2/
      receipt.json
      _SUCCESS
  terminal/
    success/
      result.json
      _SUCCESS
```

A marked terminal failure instead has the exact ordered-prefix grammar frozen
below and, after the trace-prefix leaves, exactly:

```text
  terminal/
    failure-intent/
      receipt.json
      _SUCCESS
    failure-resumes/
      resume-<10-digit j>/
        receipt.json
        _SUCCESS
    failure/
      failure.json
      _FAILURE
```

There is one failure intent and a contiguous 1-to-641 resume prefix from zero.
A forensically incomplete rehearsal may stop at only a Section 10/10.2
permitted stage or prefix and has no terminal marker. `TR/attempt.json` has
exactly:

```text
schema_version status authority_stage seed panel_indices contract
source_snapshots git_executable bootstrap_git_check runtime
module_inventory_sha256 resource_config_sha256
roots outside_baseline filesystem clock time_origin fixed_units
```

Fixed values are:

```text
schema_version   1
status           "started"
authority_stage  "test-rehearsal"
seed             1729
panel_indices    [10000,10001,10002]
```

`contract`, `git_executable`, `bootstrap_git_check`, `runtime`, module
inventory, config digest, and clock are the exact objects used by the
registered code. The bootstrap check is Section 4.3's complete
`"bootstrap"` object, was issued by `time_origin`'s supervisor before any
worker, and binds the pinned executable. `source_snapshots` has exactly
`panel`, `executable`, and `authority`; all three are reconstructed from that
check. The executable digest must later equal the registered attempt's digest
byte-for-byte. The authority object is the historical rehearsal authority and
follows Section 4.3's explicit stage-specific difference rule after the
prediction seal. `roots` names the literal `TR/TC/TS` paths.
`outside_baseline` and `filesystem` use the exact registered-attempt schemas
with rehearsal roots substituted mechanically.
`time_origin` is the exact registered-attempt object and is sampled at the
same bootstrap position. The rehearsal supervisor arms the same literal
`480000000000`-ns bootstrap watchdog before project import; therefore
`attempt_bootstrap_preflight.elapsed_ns` and only global boundary index zero
(rehearsal `0`, local position `0`) derive
`attempt_bootstrap_elapsed_ns` from `time_origin.perf_counter_ns`; the field is
null at all 44 later global boundaries, including local position zero for
rehearsals `1` and `2`. It is never reconstructed from a later timer.
`fixed_units` has exactly `k3`, `k4`, `k5`, `k6`, and `k7`, with integer
values `25`, `225`, `225`, `225`, and `4096`. Attempt publication and hashing
use Section 11's exact atomic procedure.

Each rehearsal has exactly one worker and one durable worker claim. For
rehearsal `i`, the supervisor follows Section 11's anonymous-pipe construction
and publication order, replacing only the capability domain with
`"xid-g2-resource-rehearsal-worker-capability-v1"` and admitting only the
in-worker `TestRngNamespace` factory. The exact payload is:

```text
CJSON([
  "xid-g2-resource-rehearsal-worker-capability-v1",
  attempt_sha256,
  i,
  10000 + i,
  supervisor_pid,
  supervisor_start_identity,
  worker_pid,
  worker_start_identity,
  panel_source_snapshot_sha256,
  executable_source_snapshot_sha256,
  authority_source_snapshot_sha256,
  runtime_sha256,
  resource_config_sha256,
  capability_nonce_64_lower_hex,
])
```

The nonce, pipe attestation, bounded complete read, mandatory EOF, process
identity checks, publication-before-release order, and separation from
scientific RNG accounting are exactly Section 11's rules. The only permitted
launch and birth paths are
`TR/worker-launches/rehearsal-<i>/claim.json` and
`TR/worker-births/rehearsal-<i>/claim.json`, each with the adjacent Section 10
marker. The launch intent is Section 11's exact registered schema with
`authority_stage,rehearsal_index,panel_index` inserted immediately after
`status`; their values are `"test-rehearsal"`, `i`, and `10000+i`.
`worker_index=i`, `resume_reason="initial"`, and the predecessor claim is
null. Its `receipt_kind` is
`"g2-resource-rehearsal-worker-launch-intent-v1"`. The birth is Section 11's
exact registered birth schema with those same three rehearsal fields inserted
after `status`, and
`receipt_kind="g2-resource-rehearsal-worker-birth-v1"`. All parent-liveness,
registration-deadline, publisher, identity, nonce-commitment, and initial-arm
joins are unchanged. A rehearsal launch without a complete birth, or a birth
without eventual wait/death evidence, is terminal and never permits another
rehearsal index to start.

The only permitted claim path is `TR/workers/rehearsal-<i>/claim.json`, with
the adjacent Section 10 success marker. The claim has exactly:

```text
schema_version receipt_kind status authority_stage attempt_sha256
rehearsal_index panel_index worker_index pid process_start_identity
supervisor_pid supervisor_start_identity
launch_intent_sha256 worker_birth_sha256 capability_sha256
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
boot_identity_sha256 claimed_wall_time_ns claimed_perf_counter_ns
resume_reason predecessor_worker_claim_sha256 initial_watchdog_arm
```

Its fixed values are:

```text
schema_version                  1
receipt_kind                    "g2-resource-rehearsal-worker-claim-v1"
status                          "claimed"
authority_stage                 "test-rehearsal"
rehearsal_index                 i
panel_index                     10000 + i
worker_index                    i
resume_reason                   "initial"
predecessor_worker_claim_sha256 null
```

Claim times and all remaining fields follow the registered claim definitions.
A claim's launch/birth hashes and initial arm equal that rehearsal's complete
visible precursor receipts byte-for-byte.
A rehearsal worker loss is terminal because this is one logical no-retry
evidence attempt; no successor claim or alternate worker index is valid.
Every kernel record and boundary for rehearsal `i` carries
`SHA256(exact claim.json bytes)`, and the trace receipt repeats that value.

After worker claim `i` and before its worker-ready boundary, the supervisor
publishes exactly one reservation at
`TR/reservations/rehearsal-<i>/claim.json` plus the Section 10 marker. Its
claim has exactly:

```text
schema_version receipt_kind status authority_stage attempt_sha256
rehearsal_index panel_index trace_index epoch_index role phase
measurement_block pair_index reservation_creator_worker_claim_sha256
recovery_trigger_interruption_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
licensed_address_domains
```

Fixed values are:

```text
schema_version     1
receipt_kind       "g2-resource-rehearsal-panel-reservation-v1"
status             "reserved"
authority_stage    "test-rehearsal"
rehearsal_index    i
panel_index        10000 + i
trace_index        i
epoch_index        i
role               "cold-equal"
phase              "equal"
measurement_block  0
pair_index         0
```

`reservation_creator_worker_claim_sha256` binds that rehearsal's exact claim
and `recovery_trigger_interruption_sha256` is null. Source/runtime/config
fields equal the attempt, and `licensed_address_domains` is Section 12's exact
full smooth/paper domain with seed `1729`, panel `10000+i`, and
`TestRngNamespace` substituted. The three test-only `"cold-equal"` roles do
not alter the registered rule that panel zero is its sole cold trace. Every
rehearsal boundary `trace_progress.reservation_sha256` and the trace receipt
hash these exact reservation bytes; a null, synthetic, or reset value is
invalid. No artifact path, scientific RNG factory, or kernel operation may be
entered before the reservation and its marker validate.

Each `TR/traces/rehearsal-<i>/receipt.json` has exactly:

```text
schema_version receipt_kind authority_stage attempt_sha256 rehearsal_index
panel_index reservation_sha256 worker_claim_sha256 panel_source_snapshot_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
kernel_records
boundary_receipt_sha256s boundary_publication_durations_ns
cleanup_intent_sha256s cleanup_intent_publication_durations_ns resume_state
artifact_inventory rng_address_inventory_sha256 rng_call_count
registries rss disk all_artifacts_valid complete
```

`receipt_kind` is `"g2-resource-rehearsal-trace-v1"`,
`authority_stage` is `"test-rehearsal"`, `rehearsal_index` is `0..2`, and
`panel_index` is `10000 + rehearsal_index`. `kernel_records` is the exact
15-position Section 13 vector for a complete equal-context operand block.
`worker_claim_sha256` hashes that rehearsal's exact durable worker claim and
must equal every kernel record and boundary worker-claim hash.
`reservation_sha256` hashes that rehearsal's exact durable reservation and
must equal every boundary trace-progress reservation hash.
`boundary_receipt_sha256s` and `boundary_publication_durations_ns` are exact
15-element arrays: local `0` is worker-ready, local `1` closes positions
`[0,1]`, and local `p=2..14` closes position `p`.
`cleanup_intent_sha256s` and its publication-duration array have four elements
for positions `9`, `12`, `13`, and `14`, in that order. `resume_state` is the
final Section 13 object with all seven rows deleted.

Each rehearsal boundary `receipt.json` has exactly:

```text
schema_version receipt_kind authority_stage attempt_sha256
rehearsal_index panel_index reservation_sha256 worker_claim_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
boundary_position boundary_index boundary_kind predecessor_boundary_sha256
predecessor_durable_marker_kind predecessor_durable_marker_sha256
boot_identity_sha256 trace_progress next_watchdog_arm terminal_size_preflight
cumulative_active_to_cutoff_ns
cutoff_wall_time_ns cutoff_perf_counter_ns chunk_work_elapsed_ns
boundary_publication_upper_ns chunk_upper_ns attempt_bootstrap_elapsed_ns
predecessor_durable_marker_publication_accounting_ns
predecessor_durable_marker_publication_method
next_record_accounting_anchor_cumulative_ns
rss_sample_count_to_cutoff rss_maximum_sample_gap_ns_to_cutoff
rss_sampled_tree_peak_to_cutoff_bytes
rss_supervisor_rusage_highwater_to_cutoff_bytes
rss_worker_waits_to_cutoff
rss_preterminal_git_rusage_highwater_to_cutoff_bytes
rss_rusage_highwater_envelope_to_cutoff_bytes
rss_observed_to_cutoff_bytes rss_admission_upper_bytes
rss_observation_complete_to_cutoff
created_roots_high_water_observed_bytes created_roots_at_cutoff_bytes
created_roots_resume_upper_bytes checkpoint_tree_high_water_bytes
checkpoint_tree_admission_upper_bytes disk_observation_complete_to_cutoff
absolute_workspace_resume_upper_bytes filesystem registries
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
complete
```

Fixed values are `schema_version=1`,
`receipt_kind="g2-resource-rehearsal-boundary-v1"`,
`authority_stage="test-rehearsal"`, `rehearsal_index=i`,
`panel_index=10000+i`, `reservation_sha256` and
`worker_claim_sha256` equal the exact rehearsal leaves, `boundary_position=p`,
`boundary_index=15*i+p`, `boundary_kind="worker-ready"` for `p=0` and
`"kernel-record"` otherwise, and `complete=true`.
`next_watchdog_arm` is the exact Section 11 object for `p=0..13`; at `p=14`
it is null because no later worker work occurs under that boundary and any
next rehearsal worker must first publish its own launch-intent arm.
`terminal_size_preflight` is null except at `i=2,p=14`. There it is Section
16.1's exact object with `terminal_kind="rehearsal-success"` and rows for
`terminal/success/result.json` and `terminal/success/_SUCCESS`. A failed
preflight selects rehearsal failure before any success-stage mutation.

`trace_progress` is always nonnull and has exactly the registered Section 16
keys. At `p=0` it carries the rehearsal's exact
trace/panel/reservation/epoch/role/phase/block/pair and start fields, with
`completed_kernel_positions=[]`, `next_kernel_position=0`,
`kernel_records=[]`, `first_operand_epoch=null`, and `pending_replay=null`.
At `p=1`, completed positions are `[0,1]`, next is `2`, and the exact
first-operand epoch object is nonnull. At `p=2..14`, completed positions are
`[0,...,p]` and next is `p+1`; at `p=14`, next is `15`. Rehearsal replay
remains null/zero because a worker loss is terminal. Every prefix carries
Section 13's exact resume-state transition.

All cumulative time, cutoff, chunk, publication, anchor, RSS, created-root,
checkpoint-tree, absolute-workspace, `filesystem`, and `registries` fields
use the registered Section 16 types and formulas without substitution.
`attempt_bootstrap_elapsed_ns` is nonnull only at global index zero.
Predecessor-marker publication fields are null only there and otherwise use
`"measured"` plus the exact prior boundary or cleanup-intent publication
duration; the rehearsal has no fixed-upper-after-loss branch. Immediate marker
kind is `"attempt"` at global boundary zero, `"cleanup-intent"` after the four
intents, and `"boundary"` otherwise. Source/runtime/config hashes equal the
attempt.
There is no registered `last_complete_trace_index`,
`completed_measurement_block`, `active_measurement_block`,
`next_panel_index`, or `next_trace_index` field in this test-stage schema.

The boundary leaves use Section 10's atomic-directory publisher.
For rehearsal `i` and local boundary position `p`, the path is exactly
`TR/boundaries/rehearsal-<i>/boundary-<two-digit p>/`, while the receipt's
`boundary_index` is the global integer `15*i+p`. The predecessor is null only
at global index zero and otherwise hashes global boundary `15*i+p-1`;
neither the index nor predecessor chain resets between rehearsals.
Each publication duration brackets stage construction through final-parent
fsync with `perf_counter_ns`; because it is known only after publication, it
is bound by the later trace receipt rather than self-reported in that
boundary.

Rehearsal cleanup intents use:

```text
TR/cleanups/rehearsal-<i>/cleanup-<two-digit c>/
```

for `c=0..3`, mapping to record positions `[9,12,13,14]`. Their global
`cleanup_index=4*i+c`. The receipt is Section 16.2's exact schema with
`authority_stage` and `rehearsal_index` added immediately after
`receipt_kind`, stage fixed to `"test-rehearsal"`, and `TR/TC/TS` roots
substituted. The predecessor logical boundaries are local positions
`[8,11,12,13]`. Each following boundary names the intent as its immediate
durable marker and forward-reports its exact publication duration. A rehearsal
loss after a complete intent may finish only its deletion suffix before
terminal failure closure; it may not retry numerical work.

Every artifact row in the inventory has stage `"test-rehearsal"` and a path
below `TC`. `artifact_inventory` has exactly the same
`schema_version,count,rows,kind_counts,sha256` object as the root rehearsal
inventory, restricted to this trace's exact ownership rows. Its digest uses
the Section 17 artifact-inventory formula with `TC`-relative paths. RNG
entropy rows are the exact seed-1729 resource-stream addresses actually
drawn. Registry, RSS, and disk objects use the same schemas and checks as a
registered trace.

`TR/terminal/success/result.json` has exactly:

```text
schema_version status authority_stage attempt_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
worker_launch_intent_sha256s worker_birth_sha256s
reservation_sha256s worker_claim_sha256s trace_receipt_sha256s
cleanup_intent_sha256s
measurability terminal_close_preflight attempt_bootstrap_preflight
resource_accounting_preflight
preterminal_git_checks rss artifact_inventory
rng_address_inventory_sha256 all_artifacts_valid
all_registries_restored all_passed
```

`status` is `"passed"`. `worker_launch_intent_sha256s`,
`worker_birth_sha256s`, `reservation_sha256s`, `worker_claim_sha256s`, and
`trace_receipt_sha256s` are the ordered three-item arrays by rehearsal index.
Each worker hash joins its exact launch/birth precursor, and each
reservation/worker hash must reproduce the corresponding trace receipt's
singular hash. `cleanup_intent_sha256s` is the exact twelve-item concatenation
of each trace's four hashes in rehearsal/cleanup-index order. `measurability`
is an ordered array by rehearsal then kernel
`3..7`;
each entry has exactly:

```text
rehearsal_index panel_index kernel_id units duration_ns
clock_resolution_ns duration_plus_ns minimum_ns passed
```

`minimum_ns` is `100000000`, units equal the fixed block, and every `passed`
must be true. `terminal_close_preflight` is the ordered three-row array by
rehearsal index. Every row has exactly:

```text
rehearsal_index panel_index kernel_id units duration_plus_ns
cold_margin_upper_ns limit_ns passed
```

`kernel_id=14`, `units=1`,
`cold_margin_upper_ns=ceil_div(25*duration_plus_ns,12)`,
`limit_ns=480000000000`, and every `passed` must be true. Rehearsal records
have `replay_count=0`, so this `duration_plus_ns` is exactly equal to
`admission_duration_plus_ns`; the persisted legacy field name is a zero-replay
alias and cannot authorize `Rplus` in a registered absolute projection. Root
`all_passed` also includes `resource_accounting_preflight`, an ordered 58-row
array. Its first 57 rows are the capped nonterminal checkpoint intervals, ordered by
rehearsal index and then the 19 durable work
markers in execution order. Within one rehearsal the order is boundaries `0..8`, cleanup `0`,
boundary `9..11`, cleanup `1`, boundary `12`, cleanup `2`, boundary `13`,
cleanup `3`, boundary `14`. Each row has exactly:

```text
rehearsal_index accounting_ordinal accounting_kind accounting_local_index
chunk_work_elapsed_ns publication_accounting_ns publication_method
accounted_interval_ns
work_limit_ns publication_accounting_limit_ns accounted_interval_limit_ns passed
```

For rehearsal `i` and local execution ordinal `e=0..18`,
`accounting_ordinal=19*i+e`, so the 57 ordinary ordinals are globally unique and
contiguous `0..56`. Kind is `"boundary"` or `"cleanup-intent"` and
`accounting_local_index` is the boundary index `0..14` or cleanup index `0..3`.
The final row has `rehearsal_index=null`, `accounting_ordinal=57`,
`accounting_kind="terminal-accounting"`, and `accounting_local_index=0`; its
work spans the final durable boundary through the pre-JSON cutoff, and its
publication value is the fixed terminal accounting charge. Method is
`"measured"` for the 57 no-retry work markers and
`"fixed-terminal-accounting-charge-v1"` for the terminal row.
The fixed limits are `480000000000`, `60000000000`, and `540000000000`;
`accounted_interval_ns=chunk_work_elapsed_ns+
publication_accounting_ns`. Every row must pass. Root `all_passed`
also requires `attempt_bootstrap_preflight`, which has exactly
`elapsed_ns`, `limit_ns=480000000000`, and `passed`. Root `all_passed`
includes every measurability, terminal-close, bootstrap, and
resource-accounting row. The final row is a projection convention, not an
observation or upper bound on marker encoding, final seal, rename, or parent
fsync latency. The frozen TOML names these quantities directly:
`rehearsal_resource_accounting_row_count=58`,
`rehearsal_terminal_accounting_row_count=1`,
`terminal.accounting_method="fixed-terminal-accounting-charge-v1"`, and
`terminal.accounting_charge_ns=60000000000`.

`preterminal_git_checks` is Section 4.3's exact two-check terminal object.
Rehearsal `rss` is Section 17's exact cumulative success object with rehearsal
roots substituted. Its `worker_waits` has exactly three rows, one for each
issued rehearsal worker in index order; its
`preterminal_git_rusage_highwater_bytes` is the maximum over the bootstrap and
terminal-pre-JSON child rows; its rusage formula includes both child classes;
and `all_wait_statuses_collected=true` requires those three worker rows plus
all 24 preterminal Git rows. Root `all_passed` includes
`preterminal_git_checks.count=2`, every Git child/output/wait predicate, the
exact cumulative RSS equality, complete issued-child coverage, and
`rss.passed=true`.

`rng_address_inventory_sha256` is exactly:

```text
SHA256(CJSON([
  "xid-g2-resource-rehearsal-address-inventory-v1",
  [[rehearsal_index, trace.rng_call_count,
    trace.rng_address_inventory_sha256], ...],
]))
```

with the three rows ordered by rehearsal index. The failure variant uses only
its `Tb` complete-trace prefix under the same domain and row grammar; it does
not claim an uncommitted failed-worker prefix.

`artifact_inventory` has exactly:

```text
schema_version count rows kind_counts sha256
```

`schema_version=1`. `rows` is the UTF-8-path-sorted array:

```text
[[TC-relative artifact leaf, artifact_kind, artifact_sha256], ...]
```

and `count` is its length. It includes every rehearsal `base-panel`,
`cell-panel`, and all eleven resource kinds. `kind_counts` has exactly these
thirteen keys:

```text
base-panel                               3
cell-panel                               3
resource-null-batch-v1                   3
resource-paper-full-date-v1              3
resource-paper-recovery-date-v1          3
resource-paper-cache-fixture-v1          6
resource-paper-bootstrap-batch-v1        6
resource-publication-envelope-v1         3
resource-resume-base-panel-v1            3
resource-resume-cell-panel-v1            3
resource-resume-bootstrap-weights-v1     3
resource-resume-paper-bootstrap-weights-v1 3
resource-resume-candidate-focals-v1      9
```

Thus `count=51`; each trace owns exactly seventeen rows. The values are exact
nonnegative `u64` counts, not examples.

The root rows are the globally path-sorted concatenation of the three trace
receipts' exact `artifact_inventory.rows`; payload deletion does not remove
those durable commitments. Its `sha256` is:

```text
SHA256(CJSON([
  "xid-g2-resource-artifact-inventory-v1",
  rows,
]))
```

For every rehearsal trace `i`, ownership was validated against the manifest
immediately before timed deletion: each new-kind row had
`creation.trace_index=i`; an inherited `base-panel` or `cell-panel` row had
the unchanged manifest address `panel_index=10000+i`, equal to the trace and
attempt panel. The root validator now joins rows to the durable kernel records
and trace object byte-for-byte and requires every corresponding `TC` final to
be absent. A missing commitment, duplicate path, ownership mismatch,
kind-count mismatch, subset-digest mismatch, or surviving artifact makes root
`all_passed=false`.
The root `_SUCCESS` schema is Section 17's success schema with the result hash.
`TR/terminal/failure/failure.json` has exactly:

```text
schema_version status authority_stage attempt_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
failure_stage failure_type message worker_return_code failure_intent_sha256
cutoff_boot_identity_sha256 cutoff_perf_counter_ns cutoff_wall_time_ns
calendar_to_cutoff_ns excluded_poweroff_ns cumulative_active_to_cutoff_ns
terminal_close_method terminal_close_accounting_charge_ns
terminal_accounted_interval_ns resource_accounted_charge_ns
preterminal_git_checks
receipt_inventories ordinary_prefix partial_artifact_inventory artifact_inventory
rng_address_inventory_sha256 logs rss disk failure_cleanup retry_permitted
```

`status` is `"failed"`, stage is `"test-rehearsal"`, and
`retry_permitted=false`. `worker_return_code` is null or a signed 32-bit
integer and `failure_intent_sha256` hashes Section 10.2's exact rehearsal
intent. `preterminal_git_checks` is Section 4.3's exact two-check terminal
object; a failed or incomplete terminal pre-JSON child set leaves the selected
failure forensically incomplete rather than publishing this JSON.
`receipt_inventories` has exactly `worker_launches`, `worker_births`,
`workers`, `reservations`, `boundaries`, `cleanups`, `traces`,
`failure_intents`, and `failure_resumes`; each value has exactly `count` and
`sha256` under
Section 10's receipt-inventory formula. Failure-intent count is exactly one;
resume count is in `1..641` and its indices are contiguous from zero.
Let `F` be the cleanup-complete final failure-resume receipt. The top-level
failure cutoff is on `F.boot_identity_sha256` and the same live boot:

```text
cutoff_boot_identity_sha256 = F.boot_identity_sha256
terminal_work_ns =
    cutoff_perf_counter_ns - F.cutoff_perf_counter_ns
cumulative_active_to_cutoff_ns =
    F.cumulative_active_ns + terminal_work_ns
calendar_to_cutoff_ns =
    cutoff_wall_time_ns - attempt.time_origin.wall_time_ns
excluded_poweroff_ns = 0
terminal_close_method = "fixed-terminal-accounting-charge-v1"
terminal_close_accounting_charge_ns = 60000000000
terminal_accounted_interval_ns =
    terminal_work_ns + terminal_close_accounting_charge_ns
resource_accounted_charge_ns =
    cumulative_active_to_cutoff_ns + terminal_close_accounting_charge_ns
```

The two cutoff samples are consecutive final-telemetry samples after cleanup;
`terminal_work_ns` is nonnegative and at most `480000000000`; the fixed
terminal charge is exactly `60000000000`; and their accounted sum is at most
`540000000000`. These are resource-accounting predicates, not an observation
or latency bound for the later marker/final-seal/rename/parent-fsync suffix.

Let the ordinary counts be `Lb`, `Nb`, `Wb`, `Qb`, `Bb`, `Cb`, and `Tb` for
worker launches, worker births, worker claims, reservations, boundaries,
cleanups, and traces. Every category path is an exact rehearsal-index prefix.
One trace's
durable-marker word is:

```text
E = [B0,B1,B2,B3,B4,B5,B6,B7,B8,C0,
     B9,B10,B11,C1,B12,C2,B13,C3,B14]
```

where `B` is a boundary leaf and `C` a cleanup-intent leaf. Let `m` be the
current incomplete trace's prefix length in `0..19`, or zero without a current
reservation. Then:

```text
0 <= Tb <= Qb <= Wb <= Nb <= Lb <= min(3, Tb + 1)
if Qb == Tb:     m == 0
if Qb == Tb + 1: Wb == Nb == Lb == Tb + 1

Bb = 15 * Tb + count(B in E[:m])
Cb =  4 * Tb + count(C in E[:m])
```

The nested inequalities permit exactly the three additional pre-reservation
cuts: launch-only, launch-plus-birth, and launch-plus-birth-plus-claim. A birth
cannot exist without its launch and a claim cannot exist without both.
Boundary paths map global index `d` to rehearsal `d//15` and local position
`d%15`; cleanup paths map `u//4,u%4`. Every listed pair, precursor,
predecessor, worker, and immediate-marker join must validate, and no path
outside the event prefix may exist.

Rehearsal `ordinary_prefix` has exactly
`schema_version,event_count,event_inventory_sha256,tip_kind,tip_sha256`, with
`schema_version=1`. Its deterministic scheduler emits, for each rehearsal
`i=0..2`, the exact sequence:

```text
worker-launch(i), worker-birth(i), worker(i), reservation(i),
E_i[0], ..., E_i[18], trace(i)
```

and stops at the durable prefix described by `Lb,Nb,Wb,Qb,Bb,Cb,Tb,m`. Each
emitted row is:

```text
[event_ordinal, event_kind, category_index,
 relative_receipt_path, receipt_sha256]
```

`event_ordinal` is globally contiguous from zero. Kinds and global category
indices are `"worker-launch"/i`, `"worker-birth"/i`, `"worker"/i`,
`"reservation"/i`,
`"boundary"/(15*i+p)`, `"cleanup-intent"/(4*i+c)`, and `"trace"/i`.
Paths are exactly `worker-launches/rehearsal-i`,
`worker-births/rehearsal-i`, `workers/rehearsal-i`,
`reservations/rehearsal-i`,
`boundaries/rehearsal-i/boundary-<two-digit p>`,
`cleanups/rehearsal-i/cleanup-<two-digit c>`, and
`traces/rehearsal-i`. The boundary/cleanup local index is the one named by
`E_i`; every SHA256 hashes that leaf's exact claim/receipt bytes. Then:

```text
event_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-ordinary-event-prefix-v1",
  rows,
]))
```

`event_count=len(rows)`. The two tip fields are null for an empty prefix and
otherwise equal the final row's kind and receipt SHA256. No other row order,
path spelling, or category index is admitted.

`partial_artifact_inventory` has exactly `count`, `rows`, and `sha256`.
`rows` is the path-sorted unique union of every current incomplete trace
kernel-record artifact row in its latest boundary plus any additional current
cleanup-intent `record_prefix.artifact_inventory_rows`. It is empty without a
durable current record. It is a durable commitment even when terminal cleanup
has removed the final. Its digest uses the artifact-inventory domain.
`artifact_inventory` has exactly `count`, `sha256`, and the thirteen-key
`kind_counts`; it is the path-sorted union of complete trace inventories and
partial rows. Counts are nonnegative `u64` values rather than the success
totals.

The failure `rng_address_inventory_sha256` covers only the `Tb` complete-trace
prefix under the exact success-domain row grammar above. RNG evidence for a
durable partial current trace remains transitively committed by the
`ordinary_prefix` boundary/cleanup receipt hashes and is not separately
claimed by this aggregate. Neither commitment says anything about an
uncommitted physical call prefix. `logs` has exactly `stdout` and `stderr`;
each has `count,rows,sha256`. Rows are worker-index ordered:

```text
[worker_index, TS-relative_log_path, byte_count, exact_file_sha256]
```

and the digest is
`SHA256(CJSON(["xid-g2-resource-log-inventory-v1",stream,rows]))`.
No-worker values are the exact empty rows/digest. `rss` and `disk` use the
Section 17 failure-telemetry schemas, including explicit pre-sampler/
pre-baseline states rather than fabricated success values.

A marked failure is permitted only through Section 10.2. After every currently
waitable worker is reaped and every other issued worker identity has an exact
non-wait death proof, while every issued Git child has its mandatory wait row,
capability descriptors and registries are closed,
stdout/stderr are finalized, any complete cleanup intent finishes only its
exact suffix, and every durable prefix/evidence object revalidates, the
supervisor publishes the immutable failure intent before deleting any terminal
artifact. A proved missing wait remains a failing telemetry fact; an unproved
identity prevents intent publication. The cleanup inventory covers every
remaining valid artifact final and every uniquely implied stage beneath `TC`
and `TS`. Cleanup then follows only the journaled prefix/resume protocol.
`failure_cleanup` is the exact Section 10.2 object and proves both roots absent
before `failure.json`.

If invalid final bytes, publication uncertainty, a non-prefix receipt, or
unremovable debris prevents intent publication, the attempt remains consumed
and forensically incomplete. After an intent exists, the selected failure
remains irrevocable even if cleanup or terminal publication becomes
forensically incomplete; ordinary work and success remain forbidden.
The root `_FAILURE` is Section 17's exact failure marker: it is written and
fsynced inside the hidden failure stage before that stage-directory fsync. The
no-overwrite outcome-directory rename and terminal-parent fsync are the final
mutations to any rehearsal root, with no later mutation. A marked failure
requires an append-only amendment before any new measurability evidence.

On success, the supervisor validates the complete rows and retains `TC` and
`TS` as immutable evidence roots. It performs no post-result cleanup. The
final durable rehearsal boundary is the predecessor of one root terminal
accounting row: waits, scans, aggregation, and pre-JSON work take at most
`480000000000` ns. The later atomic `TR/terminal/success/` publication
sequence receives the fixed `60000000000`-ns accounting charge, so the
accounted sum is at most `540000000000` ns. That charge is not an observed or
enforced upper on hidden-stage creation, JSON/marker fsync, the post-JSON Git
certificate, final in-process seal, sampler shutdown, no-overwrite rename, or
terminal-parent fsync. The complete directory becomes visible in one rename
and durably attests that the final seal passed; visibility irrevocably selects
success. No JSON-without-marker suffix exists. The later quantitative
prediction seal binds the exact visible `result.json` and `_SUCCESS` bytes
inside that directory.

### 10.2 Immutable terminal-failure selection and cleanup

Rehearsal and registered terminal failure share one marker-last atomic receipt
journal before any destructive terminal cleanup. This journal is distinct
from the later atomic terminal-outcome directory. Let `X` be `TR` for
rehearsal and `R` for registered execution. The exact paths are:

```text
X/terminal/failure-intent/
X/terminal/failure-resumes/resume-<10-digit j>/
```

Each is an atomic receipt directory under Section 10. The failure-intent
`receipt.json` has exactly:

```text
schema_version receipt_kind authority_stage attempt_sha256
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
failure_stage failure_type message worker_return_code failure_selection_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
boot_identity_sha256 process_deaths worker_waits
preterminal_git_rusage_highwater_bytes predecessor_checkpoint_kind
predecessor_checkpoint_sha256 precleanup_cutoff_wall_time_ns
precleanup_cutoff_perf_counter_ns precleanup_cumulative_active_ns
chunk_work_elapsed_ns publication_accounting_charge_ns
publication_accounting_method accounted_interval_ns
receipt_evidence_sha256 ordinary_event_prefix_sha256 artifact_evidence_sha256
rng_evidence_sha256 logs_evidence_sha256 cleanup_inventory complete
```

Fixed values are `schema_version=1`,
`receipt_kind="resource-terminal-failure-intent-v1"`, `complete=true`, and
`authority_stage` equal to `"test-rehearsal"` or `"registered-resource"`.
`worker_return_code` is null or a signed 32-bit integer. The bounded
failure-stage/type/message triple is frozen here and:

```text
failure_selection_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-failure-selection-v1",
  authority_stage,
  failure_stage,
  failure_type,
  message,
  worker_return_code,
]))
```

The publisher identity is checked immediately before the intent marker.
`process_deaths` is Section 16's exact object. Together with every earlier
durable interruption process-death set, it proves every superseded
worker/supervisor identity not equal to the publisher; its local rows contain
only newly proved identities absent from all earlier durable sets. It may have
empty rows only when those earlier sets already prove every superseded
identity and the same live supervisor selects the failure.
`predecessor_checkpoint_kind` is `"attempt"`, `"boundary"`,
`"cleanup-intent"`, or `"interruption"` and identifies the latest durable
checkpoint/work receipt. The precleanup cutoff values use the
unique cumulative clock. Define `predecessor_anchor_ns` as zero for
`"attempt"`, `boundary.cumulative_active_to_cutoff_ns` for `"boundary"`,
`cleanup_intent.intent_cutoff_cumulative_active_ns` for `"cleanup-intent"`, or
`interruption.cumulative_active_ns` for `"interruption"`. Then:

```text
chunk_work_elapsed_ns =
    precleanup_cumulative_active_ns - predecessor_anchor_ns
publication_accounting_charge_ns = 60000000000
publication_accounting_method =
    "fixed-failure-receipt-accounting-charge-v1"
accounted_interval_ns =
    chunk_work_elapsed_ns + publication_accounting_charge_ns
```

The difference is nonnegative, work is at most `480000000000`, the fixed
charge is exactly `60000000000`, and the accounted sum is at most
`540000000000`. The charge is a failure-lane accounting convention, not an
observed or enforced upper on intent-stage construction, marker write, rename,
or parent fsync. For an attempt predecessor before boundary zero, the clock
starts at `attempt.time_origin`; same-boot monotonic or cross-boot wall
arithmetic charges the entire interval.

Before encoding the intent, every currently waitable direct child is reaped
and contributes its exact Section 4.6 row to cumulative `worker_waits`; every
issued worker identity lacking a wait row
must instead have one exact Section 16 process-death proof. An unresolved live
or unproved identity is forensically incomplete, while a proved historical
missing wait selects terminal failure and remains false in failure RSS.
Every reaped row in the intent's `process_deaths` matches the corresponding
`worker_waits` projection; the cumulative object exactly extends its immediate
predecessor's durable inventory. When the predecessor is `attempt.json`, that
predecessor inventory is Section 4.6's canonical empty `worker_waits` object.
`preterminal_git_rusage_highwater_bytes` equals the bootstrap Git-child maximum
bound by the attempt; failure intent precedes the terminal pre-JSON check, so no
second preterminal child set exists yet. Git children are wait-only under
Section 4.6. The bootstrap check may license ordinary continuation only after
all of its Git children are reaped. The later terminal-pre-JSON check occurs
only after non-resumable terminal entry, so it can either validate completely
or leave the selected attempt forensically incomplete. Missing Git wait/rusage
evidence is never replaceable by a death proof.
Capability descriptors and registries are closed, logs are finalized, any
already committed cleanup-intent suffix is completed, and the complete durable
prefix is validated. No terminal artifact is deleted yet. The four evidence
digests bind the exact structured objects that the later failure JSON must
reproduce:

```text
receipt_evidence_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-failure-receipt-evidence-v1",
  [[category, count, inventory_sha256], ...],
]))

artifact_evidence_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-failure-artifact-evidence-v1",
  artifact_failure_evidence,
]))

rng_evidence_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-failure-rng-evidence-v1",
  rng_failure_evidence,
]))

logs_evidence_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-failure-log-evidence-v1",
  logs,
]))
```

Receipt evidence uses exactly the ordered category list
`worker_launches,worker_births,workers,reservations,boundaries,cleanups,traces`
for rehearsal and the ordered category list
`worker_launches,worker_births,workers,reservations,boundaries,interruptions,cleanups,traces,measurements`
for registered execution. It excludes the not-yet-published intent/resume
categories.
`ordinary_event_prefix_sha256` equals the final
`ordinary_prefix.event_inventory_sha256`. Registered execution and rehearsal
both use Section 17's domain; rehearsal constructs its exact scheduler rows in
Section 10.1. It prevents independently prefix-shaped categories from being
combined in an impossible scheduler order.
For rehearsal, `artifact_failure_evidence` has exactly
`partial_artifact_inventory,artifact_inventory`; for registered execution it
is the exact failure artifact object with `all_final_artifacts_deleted`
omitted. `rng_failure_evidence` is the rehearsal failure RNG digest or the
registered partial-prefix RNG object.

`cleanup_inventory` is Section 16.2's exact common deletion plan:
`schema_version,target_count,target_rows,entry_count,entry_rows,plan_sha256`,
with `schema_version=2`. Here target action is
`"delete-committed-final"`, `"delete-hidden-artifact-stage"`,
`"delete-uncommitted-artifact-final"`,
`"delete-uncommitted-receipt-publication"`, or
`"delete-terminal-root"`. Object kind is the exact artifact kind,
`"resource-terminal-close-probe-v1"`, `"checkpoint-root"`, or
`"scratch-root"`; the receipt-publication action is admitted only for that
scratch-resident terminal-close probe.
Every action/object/path state and its nonnull target evidence obeys Section
16.2's exhaustive table. The entry rows use stable
file/directory validation digests, child-before-parent order, and null
directory byte/hash fields. They cover every remaining checkpoint/scratch
entry and every currently present configured root exactly once. No symlink,
hard-linked regular file,
device, FIFO, socket, unknown stage family, or unaccounted path is admissible.
Invalid/conflicting bytes leave the attempt forensically incomplete before
intent.

Terminal `target_rows` are exactly the union of (a) one target for every
currently present admitted artifact final/stage or terminal-close-probe
final/stage, with its unique action, object kind, and evidence fixed by Section
16.2's exhaustive table, and (b) exactly one fallback target for each
configured checkpoint or scratch root that currently exists as an admitted
directory, using respectively `object_kind="checkpoint-root"` or
`object_kind="scratch-root"` and
`action="delete-terminal-root"`. An absent configured root contributes neither
a target nor an entry; a present one contributes exactly one positive slice.
There is no intermediate ordinary-tree target. Rows are sorted by descending
repository-relative UTF-8 target path before contiguous indices and entry
slices are assigned; otherwise ordinary checkpoint/scratch entries belong to
their unique deepest matching root fallback.

Finite liveness is byte-authoritative. Registered execution admits at most
`64` worker-launch intents, `64` worker births, `64` worker claims, `63`
interruptions, `4096` traces, and `641` failure-resume receipts. A terminal
cleanup inventory has at most `512` entry rows. Across the whole attempt, the
deduplicated union of process-death rows
in interruptions, the failure intent, and failure resumes has at most `128`
rows; every receipt contains only identities not proved in an earlier durable
receipt. Every canonical path is ASCII and at most `240` bytes.

Each cleanup entry row encodes in at most `1024` canonical bytes, each
process-death row in at most `512`, and each of the at most `64` cumulative
worker-wait rows in at most `512`, where the per-row CJSON length includes its
terminal LF. For exact non-row accounting, let `I0` be the complete canonical
failure-intent object with `cleanup_inventory.entry_rows`,
`process_deaths.rows`, and `worker_waits.rows` replaced by `[]`, leaving every
scalar, target row, digest, key, delimiter, array enclosure, and the top-level
LF unchanged.
`maximum_failure_intent_nonrow_bytes=131072` bounds `len(CJSON(I0))`. Replacing
a nonempty `[]` with its rows adds exactly the sum of the individual row CJSON
lengths minus one; an empty array adds zero. Therefore the following is a
strictly conservative complete-intent envelope:

```text
512 * 1024 + 128 * 512 + 64 * 512 + 131072 = 753664 < 1048576
```

The implementation checks every component bound before appending a row and
checks the complete canonical intent before publication. Section 16.2's
prospective plan check makes the 512-row limit true before any filesystem
entry exists. Before failure selection, reaching a worker, interruption,
trace, cleanup-row, death-row, path, row-byte, non-row-byte, or envelope bound
selects the corresponding bounded terminal failure without creating the
one-past item. After failure selection, reaching the resume/death/byte cap
stops before publication and leaves the selected attempt forensically
incomplete; it cannot truncate evidence, reopen work, choose another reason,
or grow an unbounded tail. Every failure-resume receipt also obeys the
1,048,576-byte root-receipt cap, so the 641-receipt lane is finite. The
deterministic maximal-envelope test uses the exact configured maxima and must
produce a canonical intent of at most `753664` bytes.

That intent equation is necessary but not sufficient terminal-size evidence.
Before implementation, the frozen fixture generator bound by
`fixture_schema_sha256` must also construct maximum-width exact CJSON,
including terminal LF, for all of:

```text
failure intent
failure resume index zero
failure resume with maximum strict cleanup progress
failure resume with a maximum-width new death proof
cleanup-complete final failure resume
result.json
failure.json
_SUCCESS
_FAILURE
```

The applicable fixture for each shape uses every reachable maximum rather than
an average case: 64 worker waits, 128 factorized process-death rows, 512
cleanup rows, 641 failure resumes, 240-byte paths, maximum integer and bounded
string widths, all source/control rows, 24 preterminal Git rows, 12 post-JSON
Git rows, and 1,201 terminal-publication RSS samples. Each exact file must be
at most `1048576` bytes. For every bounded vector, row, string, or path
dimension, a deterministic one-past mutation must be rejected before file or
stage creation; passing one shape cannot substitute for any other. The final
success boundary and cleanup-complete final failure resume persist the
applicable runtime preflight, so the pre-code maximum fixture and the concrete
attempt agree on one schema digest and cap.

Publication of the complete failure-intent marker irrevocably selects terminal
failure. From that point, no worker, reservation, capability, RNG, kernel,
ordinary interruption, result, alternate failure reason, or opposite marker
is legal. The only mutations are deletion of an exact prefix of
`cleanup_inventory.entry_rows`, parent fsyncs, failure-resume receipts, the final
byte-consistent `failure.json`, and `_FAILURE`.

A hidden failure-intent stage is not selected until normalized, but it is not
ordinary debris. The same live publisher may finish it. A successor first
proves the encoded publisher dead and may complete only exact canonical
payload-only or payload-plus-marker bytes without changing the selected
failure; the mandatory first failure-resume binds that death before deletion.
Marker-only, corrupt, extra, or conflicting state is forensically incomplete:
no ordinary work, success, alternate failure, or stage deletion is permitted.
A valid complete final discovered after rename is reused.

Before deleting the first row, after a crash, and after a positive cleanup
prefix advance before a 480-second cleanup segment can expire, the supervisor
publishes the next contiguous failure-resume receipt. At least one receipt is
mandatory, at most `641` may exist, and the last is published only after all
rows are absent and all required parent fsyncs complete. It has exactly:

```text
schema_version receipt_kind authority_stage attempt_sha256
failure_intent_sha256 resume_index predecessor_checkpoint_kind
predecessor_checkpoint_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
boot_identity_sha256 process_deaths completed_cleanup_entry_prefix_count
worker_waits preterminal_git_rusage_highwater_bytes
remaining_cleanup_sha256 prior_durable_wall_time_ns
prior_durable_perf_counter_ns prior_durable_cumulative_active_ns
resume_wall_time_ns resume_perf_counter_ns cutoff_wall_time_ns
cutoff_perf_counter_ns charged_gap_ns current_active_work_ns
cumulative_active_ns chunk_work_elapsed_ns
publication_accounting_charge_ns publication_accounting_method
accounted_interval_ns
terminal_size_preflight cleanup_complete complete
```

Fixed values are `schema_version=1`,
`receipt_kind="resource-terminal-failure-resume-v1"`, and `complete=true`.
`worker_waits` equals the failure intent's cumulative object byte-for-byte;
`preterminal_git_rusage_highwater_bytes` equals the intent's scalar
byte-for-byte; terminal cleanup launches no worker or Git child.
At index zero, `predecessor_checkpoint_kind="failure-intent"` and the digest
equals the exact intent; later the kind is `"failure-resume"` and the digest
equals index `j-1`. `resume_index` is less than
`maximum_failure_resume_count=641`. `process_deaths` is Section 16's exact
object and contains only newly proved identities from the attempt-wide
128-row union. It may be empty at index zero under the same continuously live
supervisor, or later only when the completed cleanup prefix has strictly
advanced. For every index `j>0`, either the completed prefix is strictly
greater than receipt `j-1` or `process_deaths.rows` is nonempty; a no-progress,
no-death receipt is invalid. The cleanup filesystem must equal one exact
absent entry-row prefix plus the byte-valid remaining suffix, with no extra
path.
`completed_cleanup_entry_prefix_count` is that prefix length and:

```text
remaining_cleanup_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-failure-cleanup-remaining-v1",
  cleanup_inventory.entry_rows[completed_cleanup_entry_prefix_count:],
]))
```

At `resume_index=0`,
`completed_cleanup_entry_prefix_count=0`; its `cleanup_complete` is true iff
`cleanup_inventory.entry_count=0`. Every later receipt obeys the strict
progress/death rule above.

The predecessor's durable wall/perf/cumulative values populate the three
`prior_durable_*` fields. After predecessor publication or adoption and
predecessor validation, the supervisor takes the resume wall/perf samples
consecutively before that segment's first cleanup deletion or parent fsync.
The charged gap is calculated from those samples before cleanup begins. On the
same boot:

```text
charged_gap_ns = resume_perf_counter_ns - prior_durable_perf_counter_ns
```

and across boots:

```text
charged_gap_ns = resume_wall_time_ns - prior_durable_wall_time_ns
```

The resume and cutoff samples share the current boot and
`current_active_work_ns=cutoff_perf_counter_ns-resume_perf_counter_ns`.
Every cleanup-prefix advance and required parent fsync performed by this
segment lies after the resume samples and before the cutoff samples; at index
zero both samples therefore precede any terminal deletion.
Then
`cumulative_active_ns=prior_durable_cumulative_active_ns+charged_gap_ns+
current_active_work_ns`. All differences are nonnegative. The encoded interval
fields are exactly:

```text
chunk_work_elapsed_ns = current_active_work_ns
publication_accounting_charge_ns = 60000000000
publication_accounting_method =
    "fixed-failure-receipt-accounting-charge-v1"
accounted_interval_ns =
    chunk_work_elapsed_ns + publication_accounting_charge_ns
```

Work must be at most `480000000000`, the charge is exactly `60000000000`, and
the accounted sum must be at most `540000000000`. The fixed charge is not an
observation or latency bound for publication of this resume receipt. A resumed
supervisor may delete only the next bound remaining entry rows in order. A
second loss publishes the next receipt and cannot alter terminal selection.
`cleanup_complete=true` iff the completed count equals
`cleanup_inventory.entry_count`, every required parent fsync is complete, and the
checkpoint/scratch roots are absent; otherwise it is false. Exactly the final
resume receipt has true. The count bound follows directly: one mandatory
index-zero anchor plus at most 512 strict cleanup-prefix advances and at most
128 newly proved publisher deaths gives at most `1+512+128=641` receipts.
Before publishing a one-past receipt, the selected attempt stops
forensically incomplete.

`terminal_size_preflight` is null on every nonfinal resume. Before publishing
the one cleanup-complete final resume, the supervisor runs the exact Section
16.1 fixture generator with `terminal_kind="rehearsal-failure"` when
`authority_stage="test-rehearsal"` or
`terminal_kind="registered-failure"` when
`authority_stage="registered-resource"`, and persists:

```text
[["terminal/failure/failure.json", failure_upper_bytes],
 ["terminal/failure/_FAILURE", failure_marker_upper_bytes]]
```

as `file_upper_rows`; every other field has the Section 16.1 schema and
fixture digest unchanged. Both uppers must be at most `1048576` and
`passed=true`. If the digest or either bound cannot be proved after failure
selection, the supervisor stops before publishing the final resume or any
terminal-stage mutation. The selected attempt remains forensically incomplete;
it may not emit a smaller/truncated file or create a one-past resume.

A hidden failure-resume stage follows Section 10's normalization rule. The
identical still-live publisher may finish it. If `cleanup_complete=false`, a
successor first proves the encoded publisher dead, may complete only an exact
payload-only or payload-plus-marker stage without changing receipt bytes, and
binds that newly proved death in the next contiguous resume receipt. Before
normalization it proves both `resume_index+1<641` and capacity for that newly
deduplicated death row; a dead-publisher nonfinal stage at index 640 or at the
death cap is forensically incomplete without mutation. If
`cleanup_complete=true` and the encoded publisher is dead, successor adoption
is forbidden and the selected attempt is forensically incomplete; otherwise
two cleanup-complete receipts would be required. Marker-only, corrupt, extra,
or conflicting bytes likewise leave the selected failure forensically
incomplete and authorize no deletion.

After the mandatory final cleanup-complete resume, the supervisor samples
final failure telemetry and publishes the atomic
`X/terminal/failure/{failure.json,_FAILURE}` directory. Its
`failure_stage`, `failure_type`, `message`, and `worker_return_code` reproduce
the intent. The validator reconstructs `receipt_evidence_sha256` from exactly
the final receipt inventory's pre-intent categories in the Section 10.2 order,
excluding only `failure_intents` and `failure_resumes`; reconstructs
`ordinary_event_prefix_sha256` from the final `ordinary_prefix`;
reconstructs
`artifact_evidence_sha256` from the final artifact object with only the
post-cleanup Boolean omitted where specified; and reconstructs
`rng_evidence_sha256` and `logs_evidence_sha256` from the exact final RNG and
log objects. All five values must equal the intent byte-for-byte. It also has
exactly:

```text
failure_cleanup =
  {intent_sha256, resume_receipt_count, resume_receipt_inventory_sha256,
   final_resume_sha256, cleanup_plan_sha256,
   completed_cleanup_entry_prefix_count,
   maximum_chunk_work_elapsed_ns, maximum_publication_accounting_ns,
   maximum_accounted_interval_ns, complete}
```

The completed prefix equals `cleanup_inventory.entry_count`,
`final_resume_sha256` hashes the mandatory cleanup-complete final resume, the
three accounting maxima are at most `480000000000`, `60000000000`, and
`540000000000`, and `complete=true`.
`intent_sha256` equals the top-level `failure_intent_sha256`;
`resume_receipt_count` is positive and
`resume_receipt_inventory_sha256` equals the final
`failure_resumes` receipt inventory;
and `cleanup_plan_sha256` equals the intent's exact cleanup plan digest. The
three maxima reconstruct the intent's and every failure-resume receipt's
`chunk_work_elapsed_ns`, fixed `publication_accounting_charge_ns`, and
`accounted_interval_ns`, plus the root failure-outcome accounting row. Final
cutoff time continues the same unique cumulative clock from the latest receipt;
final telemetry and JSON preparation are at most `480000000000` ns, terminal
outcome publication is assigned the fixed `60000000000`-ns accounting charge,
and their accounted sum is at most `540000000000` ns. Neither failure-receipt
nor terminal-outcome charge is evidence that its publication suffix finished
in 60 seconds. Cleanup, parent fsyncs, resume setup, and final telemetry are
therefore charged exactly once.
Failure-intent/resume/outcome publication
uncertainty, a non-prefix cleanup state, or inability to revalidate the
selected evidence is forensically incomplete; it never reopens ordinary work.

### 10.3 Successor-rebuildable terminal nonpass

Terminal nonpass is a forensic close, not a third scientific or engineering
outcome. It is available only when an exact terminal-entry object has already
selected success or failure but that selected outcome can no longer receive
its continuously-live publisher certificate. The selecting object is either a
complete visible `terminal_entry=true` final success boundary, an exact
payload-only or payload-plus-marker hidden stage for that boundary, a complete
visible cleanup-complete final failure resume, or its exact payload-only or
payload-plus-marker hidden stage. An absent entry stage is pre-entry and follows
the existing replay/failure transition. Marker-only, noncanonical, truncated,
extra-entry, or conflicting entry bytes do not license nonpass or any other
outcome.

Let `selected_outcome_kind` be exactly `"success"` for the final boundary and
`"failure"` for the final resume. The original publisher must either be proved
dead by Section 16's exact evidence or remain live and provide one exact
post-entry failure object. That object has fields
`failure_stage,failure_type,message,worker_return_code`; its canonical digest
uses the existing terminal-failure-selection domain, but it cannot relabel the
selected outcome as ordinary failure. No terminal-pre-JSON or post-JSON Git
check is retried, and no random, timing, kernel, cleanup, or source-admission
work is performed.

Before a nonpass outcome stage can exist, the recovery publisher creates and
locks the exact `publication.lock` inside the atomic
`X/terminal/nonpass-intent/` receipt stage. The intent's `receipt.json` has
exactly:

```text
schema_version receipt_kind status authority_stage attempt_sha256
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
selected_outcome_kind selected_entry_receipt_kind selected_entry_location
selected_entry_sha256 original_publisher_supervisor_pid
original_publisher_supervisor_start_identity boot_identity_sha256
closure_reason original_publisher_death post_entry_failure
selected_hidden_stage_kind selected_hidden_stage_inventory_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
publication_lock_kind publication_lock_filename publication_lock_mode
publication_lock_size publication_lock_sha256 publication_lock_device
publication_lock_inode publication_lock_nlink
publication_accounting_method publication_accounting_charge_ns
maximum_intent_bytes admission_pass retry_permitted complete
```

Fixed values are `schema_version=1`,
`receipt_kind="resource-terminal-nonpass-intent-v1"`,
`status="consumed-nonpass"`,
`closure_reason` equal to `"terminal-publisher-dead"` or
`"terminal-publication-failed"`,
`publication_lock_kind="darwin-fileglob-flock-exclusive-lease-v1"`,
`publication_lock_filename="publication.lock"`, mode `384`, size `45`, SHA256
`c15704b0bf11881a954c8b11d6d10b0317f66448ef0551f0be760ef7968c5cc8`,
and exact bytes
`xid-g2-terminal-nonpass-publication-lease-v1\n`.
`publication_accounting_method="fixed-terminal-accounting-charge-v1"`, the
charge is `60000000000`, `maximum_intent_bytes=131072`,
`admission_pass=false`, `retry_permitted=false`, and `complete=true`.

Exactly one of `original_publisher_death` and `post_entry_failure` is nonnull.
The death form is Section 16's exact proof for the entry publisher. The live
failure form is the exact four-field object above. `selected_entry_location`
is `"visible-final"`, `"stage-payload"`, or `"stage-complete"`.
`selected_hidden_stage_kind` is null when no selected success/failure outcome
stage exists and otherwise equals that selected kind; its inventory digest
binds the exact absent, JSON-only, or complete JSON/marker hidden-stage state.
The opposite visible outcome, opposite hidden stage, any existing nonpass
final, or a second nonpass intent is forbidden before intent creation.

The intent directory contains exactly `receipt.json`, `_SUCCESS`, and
`publication.lock`. The lock file is regular, single-link, no-follow opened,
and bound by the same device/inode/type/mode/size/content checks as the launch
lease. It is opened exactly once by the initial publisher, never explicitly
unlocked, duplicated, passed, leaked, unlinked, or replaced, and is held until
the visible nonpass directory and terminal-parent fsync complete. A successor
may normalize an exact intent stage or rebuild an incomplete nonpass stage only
after independently opening the same inode, acquiring `LOCK_EX|LOCK_NB`, and
revalidating it. `EWOULDBLOCK` authorizes no mutation.

Given the exact visible intent bytes `I`, define `i=SHA256(I)`. The canonical
`nonpass.json` has exactly:

```text
schema_version outcome authority_stage attempt_sha256
resource_config_sha256 selected_outcome_kind selected_entry_receipt_kind
selected_entry_location selected_entry_sha256 closure_reason
nonpass_intent_sha256 admission_pass retry_permitted
publication_accounting_method publication_accounting_charge_ns complete
```

It copies the named intent fields byte-for-byte, uses `outcome="nonpass"`,
`nonpass_intent_sha256=i`, `admission_pass=false`,
`retry_permitted=false`, and `complete=true`. `_NONPASS` has exactly:

```text
schema_version marker_kind nonpass_sha256 admission_pass
retry_permitted complete
```

with `schema_version=1`,
`marker_kind="xid-g2-resource-terminal-nonpass-v1"`, the exact
`nonpass.json` SHA256, both policy Booleans false, and `complete=true`.
Neither file contains successor-local time or identity. Their bytes are pure
functions of the immutable visible intent.

The locked publisher creates the unique hidden nonpass stage, fsyncs
`terminal/`, writes/fsyncs the exact JSON then marker, fsyncs the stage,
no-overwrite renames the complete directory, and fsyncs `terminal/`. Under a
successor-acquired intent lock, an exact incomplete prefix of that hidden stage
may be removed and rebuilt byte-for-byte; a complete hidden stage is renamed;
and an uncertain rename is resolved by validating the exact visible pair and
fsyncing the parent. Invalid bytes fail closed. A visible nonpass is immutable,
mutually exclusive with visible success/failure, consumes the attempt without
admission, and cannot license another seed use. Its sole accounting row uses
the already frozen fixed 60-second terminal charge, so successful-rehearsal
counts remain unchanged.

## 11. Attempt and one-use worker authority

`R/attempt.json` is create-exclusive and is the irreversible consumption
record. It has exactly:

```text
schema_version status seed streams contract source_snapshots git_executable
bootstrap_git_check runtime module_inventory_sha256 resource_config_sha256
roots outside_baseline filesystem clock hard_stops schedule terminal process
capability time_origin
```

Exact fixed values:

```text
schema_version             1
status                     "started"
seed                       2026071529
streams                    ["resource_smooth","resource_paper"]
resource_config_sha256     SHA256(exact configs/g2_resource.toml bytes)
```

`contract`, `git_executable`, `bootstrap_git_check`, and `runtime` are the exact
objects defined above. `bootstrap_git_check` is Section 4.3's complete
`"bootstrap"` object, was issued by `time_origin`'s supervisor before any
worker, and reconstructs all three `source_snapshots`. `git_executable` is
immutable attempt authority: every resumed
supervisor, source check, terminal control row, and Git-child `argv[0]`
revalidates and equals its path/mode/count/SHA before use. No successor may
re-resolve `PATH`.
`source_snapshots` has exactly `panel`, `executable`, and `authority`; each is
its exact four-key Section 4 source object. `roots` has exactly `result`,
`checkpoint`, and `scratch`, with the three literal repository-relative paths
in Section 3.

`outside_baseline` has exactly:

```text
logical_bytes allocated_bytes accounting_bytes entry_count inventory_sha256
```

It is the immutable Section 18 no-follow inventory sampled while all three
roots are absent. `accounting_bytes=max(logical_bytes,allocated_bytes)`.
`entry_count` is the row count and:

```text
inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-outside-baseline-v1",
  [[relative_path, entry_type, mode, logical_bytes, allocated_bytes,
    content_sha256_or_null], ...],
]))
```

Rows are sorted by relative-path UTF-8 bytes. Directories have null content
hashes; regular files have exact content hashes; no other path type is valid.
Every resume and final outside-workspace comparison recomputes the exact
Section 18 rows and requires their aggregates, count, and digest to equal the
immutable values in `attempt.json`; an in-memory or freshly substituted
baseline is invalid.

`filesystem` is the exact initial Section 18 filesystem snapshot sampled while
all roots are absent. It persists the nearest-parent device and allocation
unit for all three future roots and the initial maximum `g`.

`clock` has exactly:

```text
name resolution_ns
```

`name` is `"perf_counter_ns"` and `resolution_ns` is the positive integer
ceiling of the reported monotonic clock resolution in nanoseconds.

`time_origin` has exactly:

```text
wall_time_ns perf_counter_ns boot_identity_sha256
supervisor_pid supervisor_start_identity
```

The two time values are sampled consecutively with `time.time_ns()` and
`time.perf_counter_ns()` as the first two operations of the Make-launched
resource-supervisor bootstrap, before project-module import,
source/runtime/config preflight, baseline measurement, root creation, or any
other attempt mutation; both are positive `u64` values. The bootstrap then
samples Section 4.5's boot digest and its own PID/start identity before doing
any of those operations. The five values remain in memory until the later
`attempt.json` encoding. The
measured scope therefore includes the complete Python-owned supervisor path
from its bootstrap entry but explicitly excludes external `make`, shell,
`uv`, and Python-interpreter launch latency before that entry.
The minimal bootstrap supervisor arms a literal
`480000000000`-ns watchdog before project import; after the sealed config is
loaded, equality with `hard_stops.attempt_bootstrap_ns` is mandatory.
`attempt_sha256` is `SHA256(exact attempt.json bytes)`.

`hard_stops` has exactly:

```text
resource_expected_ns resource_hard_ns validation_expected_ns
validation_hard_ns research_expected_ns research_hard_ns
combined_expected_ns combined_hard_ns task_ns peak_rss_bytes
checkpoint_tree_bytes checkpoint_margin_tree_bytes
created_transient_bytes steady_total_bytes
absolute_transient_bytes sampler_period_ns maximum_sampler_gap_ns
payload_bytes checkpoint_work_ns boundary_publication_ns
durable_marker_interval_ns attempt_bootstrap_ns maximum_worker_count
maximum_interruption_count maximum_trace_count
maximum_terminal_cleanup_rows maximum_failure_resume_count
maximum_process_death_rows
maximum_canonical_path_bytes maximum_cleanup_row_bytes
maximum_process_death_row_bytes maximum_worker_wait_row_bytes
maximum_failure_intent_nonrow_bytes
maximum_failure_intent_envelope_bytes maximum_terminal_nonpass_intent_bytes
unknown_loss_rss_upper_bytes
unknown_loss_checkpoint_tree_upper_bytes
unknown_loss_created_roots_upper_bytes
unknown_loss_absolute_workspace_upper_bytes
```

The values are:

```text
3,600,000,000,000    7,200,000,000,000
43,200,000,000,000   86,400,000,000,000
10,800,000,000,000   21,600,000,000,000
57,600,000,000,000  115,200,000,000,000
480,000,000,000
3,500,000,000
2,000,000,000
1,600,000,000
6,000,000,000
25,000,000,000
30,000,000,000
50,000,000
1,000,000,000
5,242,880
480,000,000,000
60,000,000,000
540,000,000,000
480,000,000,000
64
63
4,096
512
641
128
240
1,024
512
512
131,072
753,664
131,072
3,500,000,001
2,000,000,001
6,000,000,001
30,000,000,001
```

`schedule` has exactly:

```text
cold_trace_count thermal_minimum_ns thermal_phase_order warm_block_count
warm_block_minimum_ns warm_block_minimum_pairs measurement_pair_order
boundary_rule recovery_thermal_rule rate_trace_interruption_rule
rehearsal_success_rule reservation_resume_rule telemetry_continuity_rule
```

with values:

```text
1
600,000,000,000
["validation","research","research","validation"]
3
200,000,000,000
4
[["validation","research"],["research","validation"]]
"canonical-worker-ready-post-k1-k2-post-remaining-record-trace-measurement-plus-resume-worker-ready-copy-prefix-v1"
"between-rate-traces-reset-600s-before-next-warm-trace-recovery-cycle-restarts-v2"
"inside-any-rate-bearing-trace-select-terminal-failure-exclude-all-trace-rate-evidence-v1"
"retain-evidence-roots-no-post-result-cleanup-v1"
"immutable-original-claim-contiguous-predecessor-ancestry-v1"
"closed-segments-only-unknown-loss-limit-plus-one-v1"
```

`terminal` has exactly:

```text
success_path failure_path success_stage failure_stage nonpass_path
nonpass_stage nonpass_publication_rule publication_rule
```

with values:

```text
"terminal/success"
"terminal/failure"
"terminal/.success.xid-g2-terminal-stage-v1"
"terminal/.failure.xid-g2-terminal-stage-v1"
"terminal/nonpass"
"terminal/.nonpass.xid-g2-terminal-stage-v1"
"immutable-terminal-entry-selection-successor-rebuildable-forensic-close-v1"
"write-fsync-children-stage-no-overwrite-directory-rename-parent-fsync-v1"
```

`process` has exactly:

```text
initial_supervisor_identity death_methods launch_quiescence_kind
launch_quiescence_rule launch_quiescence_successor_rule
launch_quiescence_filename launch_quiescence_mode
```

with values:

```text
"pid-start-boot-v1"
["wait4-reaped","double-process-identity-absence","boot-identity-changed"]
"darwin-fileglob-flock-exclusive-lease-v1"
"atomic-intent-directory-stable-inode-no-unlock-no-dup-no-pass-no-descendant-last-close-v1"
"fresh-open-nofollow-fstat-same-inode-flock-ex-nb-plus-supervisor-death-v1"
"quiescence.lock"
384
```

`capability` has exactly:

```text
kind pipe_attestation one_use
```

with kind `"resource-rng-worker-v1"`,
`pipe_attestation="darwin-fifo-dev0-nlink0-v1"`, and exact Boolean `true`.
Hosted Linux test attempts instead carry
`"linux-proc-fd-pipe-v1"` and cannot satisfy public authority. The pipe is
created only with `os.pipe()`. The child admits its read descriptor only under
the inherited exact predicate:

```text
Darwin: S_ISFIFO(mode) and st_dev == 0 and st_nlink == 0
Linux test-only: S_ISFIFO(mode) and
                 readlink("/proc/self/fd/d") == "pipe:[digits]"
other: reject
```

Attempt publication is exact: write and fsync a mode-`0600` same-parent stage,
expose `attempt.json` with a create-exclusive no-overwrite hard link, fsync
`R`, unlink and fsync the stage name, then fsync `R` again. The first visible
complete `attempt.json` irreversibly consumes the attempt. A partial stage
without `attempt.json` is pre-attempt debris and cannot authorize RNG; an
invalid visible `attempt.json` is consumed terminal failure and cannot be
replaced.

For worker index `w`, the supervisor executes this exact order:

1. create distinct anonymous capability and parent-liveness pipes, draw exactly
   32 capability bytes with `os.urandom(32)`, derive their nonce commitment,
   create the launch-intent stage's exact `quiescence.lock`, open it exactly
   once, and acquire `LOCK_EX|LOCK_NB` before any child exists;
2. derive the initial `watchdog_arm` below and durably publish and revalidate
   the three-entry `resource-worker-launch-intent-v1` directory before a child
   exists;
3. spawn the bootstrap-only child with only the two pipe read descriptors and
   one duplicate reference to the locked launch-quiescence open-file object
   inherited;
   before a complete capability is released it may use only the standard
   library and the frozen birth publisher, may not import NumPy, call a resource
   factory, or construct an RNG, and must exit with the fixed pre-authority
   failure code on parent-liveness EOF;
4. as its first persistent action, the child queries its PID/start/boot and the
   encoded parent identity, brackets publication with non-EOF liveness and
   unchanged-parent checks, and atomically publishes
   `resource-worker-birth-v1`;
5. under the process-census lock, the supervisor requires the returned spawn
   PID/start/boot to equal the complete birth record and requires birth
   publication not later than the launch intent's registration deadline;
6. derive the exact capability payload below, durably publish and revalidate
   the worker `claim.json` plus marker, including the launch-intent digest,
   birth digest, capability SHA256, byte-equal initial `watchdog_arm`, and
   launch-quiescence identity;
7. publish and revalidate the applicable reservation and worker-ready boundary,
   or revalidate the existing reservation before a resume worker-ready
   boundary; and only then
8. make the capability readable by writing the exact payload once and closing
   the capability write descriptor.

The supervisor keeps the liveness write descriptor and its launch-quiescence
reference open through capability release and closes them on every orderly
worker close. The bootstrap child keeps its inherited quiescence reference
through complete visible birth and claim, then closes it without calling
`LOCK_UN`; before release it polls both pipe descriptors, and liveness EOF/HUP
or capability EOF before a complete payload causes immediate pre-authority
exit. Launch-only code may not call `LOCK_UN`, reopen, `dup`, pass, unlink, or
replace the lease, or spawn a descendant. A same-boot launch intent without a
complete visible birth after supervisor death is recovery-pending. A successor
may select pre-RNG terminal failure only after the existing exact supervisor-
death proof and the fresh-open lease-quiescence proof below both pass. A
changed boot may close the launch-only state as pre-capability because no child,
pipe, or inherited descriptor survives. A complete visible birth makes the
worker identity durable and must join an eventual exact wait/death proof even
if no worker claim followed.

`R/worker-launches/launch-<10-digit w>/claim.json` has exactly:

```text
schema_version receipt_kind status attempt_sha256 worker_index
publisher_supervisor_pid publisher_supervisor_start_identity
boot_identity_sha256 predecessor_worker_claim_sha256 resume_reason
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
capability_nonce_sha256 launch_wall_time_ns launch_perf_counter_ns
registration_deadline_perf_counter_ns parent_liveness_kind watchdog_arm
launch_quiescence_kind launch_quiescence_filename launch_quiescence_mode
launch_quiescence_size launch_quiescence_sha256 launch_quiescence_device
launch_quiescence_inode launch_quiescence_nlink
```

`receipt_kind="resource-worker-launch-intent-v1"`, `status="launch-intent"`,
`parent_liveness_kind="anonymous-pipe-eof-before-capability-v1"`, and:

```text
registration_deadline_perf_counter_ns =
    launch_perf_counter_ns + 60000000000
```

The visible launch-intent directory contains exactly `claim.json`, its exact
marker, and `quiescence.lock`; the ordinary two-entry receipt rule is
superseded for this kind only. `launch_quiescence_kind` is
`"darwin-fileglob-flock-exclusive-lease-v1"`; filename is
`"quiescence.lock"`; mode is decimal `384`; size is `34`; SHA256 is
`ebc63059762c893ce8829c9f495615854f58e8624a8bb68f496bf9764bacf807`;
and the exact bytes are `xid-g2-launch-quiescence-lease-v1\n`. Device, inode,
and link count are positive `u64`, with link count exactly one. The stage is
created exclusively on the same local filesystem as its final, the file is
regular and no-follow opened, and every pre/post-lock, pre/post-rename, and
recovery `fstat` must reproduce the bound type, permission, device, inode,
link, size, and bytes.

After proving the launch-intent publisher dead, a same-boot successor opens
the exact staged or visible lease independently with no-follow semantics,
revalidates its identity, and attempts `flock(fd, LOCK_EX|LOCK_NB)` on the fresh
open-file object. `EWOULDBLOCK` authorizes no mutation. Success, followed by a
second identity validation, proves no incompatible `flock` remains on the
inherited open-file object. Combined with the frozen rule that the parent and
bootstrap child are its only references and neither can unlock, duplicate,
pass, or leak it, that proof authorizes normalization of a valid launch-intent
stage if needed and selection of ordinary terminal failure before capability
release or `SeedSequence`. The lock alone is never encoded as PID death.

`capability_nonce_sha256` hashes the exact 32 nonce bytes; those bytes are not
persisted separately. `watchdog_arm` has exactly:

```text
armed_perf_counter_ns work_limit_ns work_deadline_perf_counter_ns
reap_grace_ns reap_deadline_perf_counter_ns
```

with:

```text
work_limit_ns = 480000000000
work_deadline_perf_counter_ns =
    armed_perf_counter_ns + work_limit_ns
reap_grace_ns = 60000000000
reap_deadline_perf_counter_ns =
    work_deadline_perf_counter_ns + reap_grace_ns
```

The arm is derived before intent publication. Work gated by an arm begins only
after the arm-bearing receipt is durable. Every later boundary, cleanup intent,
or interruption that can precede more worker work carries a newly derived
`next_watchdog_arm` with the same exact schema and arithmetic. It becomes the
only active arm after that receipt is durable; later clocks may not recompute
or extend it.

`R/worker-births/birth-<10-digit w>/claim.json` has exactly:

```text
schema_version receipt_kind status attempt_sha256 worker_index
launch_intent_sha256 pid process_start_identity boot_identity_sha256
publisher_worker_pid publisher_worker_start_identity
supervisor_pid supervisor_start_identity
birth_wall_time_ns birth_perf_counter_ns
```

`receipt_kind="resource-worker-birth-v1"`, status is `"born-no-capability"`,
the publisher fields equal the worker fields, and the supervisor fields equal
the launch intent. A birth hidden stage is not successor-adoptable. Failure
before its complete visible pair leaves no durable worker identity and cannot
be guessed from a later census. It remains launch-only and may close only
through amendment A026's exact supervisor-death plus lease-quiescence proof;
the hidden birth stage then belongs to the marked-failure cleanup inventory.

The payload is:

```text
CJSON([
  "xid-g2-resource-worker-capability-v1",
  attempt_sha256,
  w,
  supervisor_pid,
  supervisor_start_identity,
  worker_pid,
  worker_start_identity,
  panel_source_snapshot_sha256,
  executable_source_snapshot_sha256,
  authority_source_snapshot_sha256,
  runtime_sha256,
  resource_config_sha256,
  capability_nonce_64_lower_hex,
])
```

through one supervisor-created anonymous pipe. Only the in-worker
`ResourceRngNamespace` factory may consume that pipe. Until the worker-ready
marker is complete, the child remains blocked on that descriptor and therefore
cannot import NumPy, call the factory, construct `SeedSequence`, or execute a
kernel. After the bounded complete read and mandatory EOF, the child hashes the
payload, opens and validates its already-complete claim/marker, reservation,
and worker-ready boundary, requires the payload, current worker claim, and
worker-ready identities to agree, validates the immutable
reservation-creator ancestry below, and only then calls the internal factory.
The payload binds the immediate
parent and target PID/start identities. The nonce is exact lowercase hex for
the 32 bytes, is never accepted from a caller or persisted separately, and the
worker claim publishes only `SHA256(exact capability bytes)`. The supervisor
closes the write descriptor immediately after the bounded complete write.
Direct construction, copied bytes, a named FIFO, a replayed descriptor, a
second read, short write/read, wrong parent, a missing/incomplete claim,
reservation, or worker-ready boundary, or any mismatch fails before
`SeedSequence`.

A process or boot loss after durable `attempt.json` but before the first
worker-ready boundary is terminal, not resumable: no registered capability has
been released and no scientific RNG exists, but no durable trace checkpoint
exists from which to continue. The supervisor selects the exact terminal
failure under Section 17's failure-intent protocol. A loss after worker-ready
is handled only by Section 16 and receives its conservative replay charge even
if the child had not yet completed its bounded capability read.
The one nonce per worker is operating-system capability entropy, not a G2 DGP
or bootstrap draw; it is counted separately and never enters the scientific
RNG address inventory.

`R/workers/worker-<10-digit w>/claim.json` has exactly:

```text
schema_version receipt_kind status attempt_sha256 worker_index pid
process_start_identity supervisor_pid supervisor_start_identity
launch_intent_sha256 worker_birth_sha256 capability_sha256
panel_source_snapshot_sha256
executable_source_snapshot_sha256 authority_source_snapshot_sha256
runtime_sha256 resource_config_sha256 boot_identity_sha256
claimed_wall_time_ns claimed_perf_counter_ns resume_reason
predecessor_worker_claim_sha256 initial_watchdog_arm
```

`receipt_kind` is `"resource-worker-claim-v1"`, status is `"claimed"`,
`worker_index` is contiguous from zero, and `resume_reason` is exactly
`"initial"`, `"supervisor-signal"`, `"boot-changed"`, `"worker-lost"`, or
`"supervisor-lost"`.
The predecessor is null only for the initial worker and otherwise identifies
the immediately preceding valid worker claim. `"worker-lost"` is permitted
only with Section 16's exact same-boot dead-worker evidence. Claim times are
consecutive positive `u64` samples from `time.time_ns()` and
`time.perf_counter_ns()` under the claim's boot identity.
`launch_intent_sha256` and `worker_birth_sha256` hash the exact complete
visible receipts for the same index, and `initial_watchdog_arm` equals the
launch intent's object byte-for-byte. No worker claim may be derived from a
hidden birth stage, an intent without birth, a birth with a different
PID/start/boot identity, or a later clock. The first worker work is charged to
this persisted arm.
The first claim's supervisor PID/start identity equals
`attempt.time_origin`; every later claim's supervisor identity equals the
publisher of the exact interruption authorizing it.

## 12. Contiguous panel reservations

Before the first draw at panel `b`, the supervisor publishes:

```text
R/reservations/panel-<10-digit b>/claim.json
R/reservations/panel-<10-digit b>/_SUCCESS
```

`claim.json` has exactly:

```text
schema_version receipt_kind status attempt_sha256 panel_index trace_index
epoch_index role phase measurement_block pair_index
reservation_creator_worker_claim_sha256
recovery_trigger_interruption_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
licensed_address_domains
```

Fixed values and domains:

```text
receipt_kind       "resource-panel-reservation-v1"
status             "reserved"
panel_index        b
trace_index        exact trace consuming b
epoch_index        u32
role               "cold-equal" | "thermal-phase" |
                   "measurement-equal" | "measurement-phase" |
                   "recovery-thermal-phase"
phase              "equal" | "validation" | "research"
measurement_block  0 outside measurement, otherwise 1..3
pair_index         0 outside a phase pair, otherwise positive u32
```

`recovery_trigger_interruption_sha256` is nonnull exactly for
`"recovery-thermal-phase"` and hashes the interruption that reset thermal
qualification; it is null otherwise.

`licensed_address_domains` has exactly `smooth` and `paper`. Each has exactly
`stream`, `phase_id`, `scenario_id`, `n_dates`, `date_range`,
`component_ids`, and `bootstrap_replicate_range`. The fixed full reservation
domains are smooth `resource_smooth`, `10/0`, dates `[0,252)`, components
`[1,2,3,4,5]`, replicates `[0,25)` and paper `resource_paper`, `10/1`, dates
`[0,2)`, components `[1,2,3,4,5]`, replicates `[0,25)`. A trace may use a
proper subset, but no address outside the reservation.

Reservations are globally contiguous: `b=0,1,2,...`, with no gap. Publishing
claim `b` requires every `0..b-1` claim and marker to validate and every
`b`-or-greater claim to be absent. Panel zero is the sole cold equal-context
trace. A claimed panel is permanently assigned to exactly one trace and can
never be reassigned. If that trace is partial at a durable boundary, resume
continues its exact next canonical position under the same claim; deterministic
re-execution of a lost current position is recorded as replay rather than
misrepresented as a new panel. Only after the trace receipt is complete may
the next trace claim the next integer.

`reservation_creator_worker_claim_sha256` never changes. For an initial
worker it equals the current claim. For any later current claim `h_0`, define
`h_(m+1)` by loading the exact claim hashed by
`h_m.predecessor_worker_claim_sha256` until null. The chain must be finite,
gap-free in descending worker index, and free of repeated digests. There is
exactly one smallest `a>=0` with `SHA256(exact h_a bytes)` equal to
`reservation_creator_worker_claim_sha256`; `h_a` is the claim that published
the reservation. Every link in the reservation-specific suffix
`h_0,...,h_a` is authorized by the unique contiguous interruption between its
predecessor and successor. Older claims may exist only after `h_a` in the
backward walk and are outside this reservation-specific suffix. If an
interruption retains the same live worker, no new claim link is invented. The
current capability and worker-ready boundary bind `h_0`; neither rewrites nor
falsely equates the immutable reservation creator.

Thermal phase traces repeat the exact phase order:

```text
validation, research, research, validation
```

Measurement block `1`, `2`, and `3` each begins with exactly one
measurement-equal trace. Its phase pairs then reset to:

```text
(validation,research), (research,validation), repeat
```

until the block has at least four complete pairs and at least 200 seconds.
The reservation ledger, not an in-memory counter, decides the next panel.

## 13. Trace receipts

The trace-record vector has 15 fixed positions:

```text
0  (k1 default)
1  (k2 default)
2  (k3 default)
3  (k4 default)
4  (k5 default)
5  (k6 default)
6  (k7 default)
7  (k9 default)
8  (k10 default)
9  (k8 default)
10 (k11 default)
11 (k12 default)
12 (k13 recovery)
13 (k13 research)
14 (k14 default)
```

The exact units vector is derived only from the receipt role/phase:

```text
cold-equal or measurement-equal:
[252,252,25,225,225,225,4096,1,1,1,1,1,6048000,53298000,1]

thermal-phase or measurement-phase, validation:
[252,252,25,225,225,225,1,1,1,1,0,1,6048000,0,1]

thermal-phase or measurement-phase, research:
[252,252,25,25,25,25,1,1,1,1,1,0,0,53298000,1]
```

The three test-rehearsal traces use the equal vector. The validator derives
this vector internally; the worker cannot select or omit a unit.
The three values at positions `7..9` remain `[1,1,1]`; their semantic kernel
IDs are now k9, k10, and k8 in that order. No validator may recover the old
k8/k9/k10 order from the unchanged numeric triple.

The successful RNG call sequence is also role-derived, not inferred from unit
counts. For seed `S` (`1729` in rehearsal and `2026071529` in registered
execution), panel `b`, and phase bit `q` (`0` smooth, `1` paper), define the
exact 13-word addresses:

```text
D_q(d,c) = [S,3,2,10,q,0,0,252,b,0,d,c,0]
B_q(r)   = [S,3,2,40,0,10,q,252,b,0,0,6,r]
```

The complete position-order sequences are:

```text
position 0:  D_0(d,c), d=0..251 outer and c=1..5 inner
position 2:  B_0(r), r=0..24 ascending
position 10: D_1(0,c), c=1..5, iff the role has positive units
position 11: D_1(1,c), c=1..5, iff the role has positive units
position 12: B_1(r), r=0..24, for equal/validation; empty for research
position 13: B_1(r), r=0..24, for research; empty for equal/validation
all other positions: empty
```

Thus the exact `len(L)` vectors are:

```text
cold_equal = [1260,0,25,0,0,0,0,0,0,0,5,5,25,0,0]
validation = [1260,0,25,0,0,0,0,0,0,0,0,5,25,0,0]
research   = [1260,0,25,0,0,0,0,0,0,0,5,0,0,25,0]
```

The successful totals are `1320`, `1315`, and `1315`, respectively; the three
fixed rehearsals total `3960`. Every zero is exact. Successful inventory and
replay-copy order is the written order without sorting or deduplication.

Every kernel record has exactly:

```text
kernel_position kernel_id variant units worker_claim_sha256
boot_identity_sha256 successful_started_perf_counter_ns
successful_ended_perf_counter_ns successful_work_ns
accounting_started_cumulative_ns accounting_ended_cumulative_ns duration_ns
clock_resolution_ns duration_plus_ns replay_count replay_penalty_ns
admission_duration_ns admission_duration_plus_ns
prelude_ns kernel_ns epilogue_ns substage_ns artifact_sha256s
artifact_inventory_rows
cleanup_intent_sha256 cleanup_completion_boot_identity_sha256
terminal_close_probe_evidence_sha256 rng_call_count rng_call_upper_count
rng_address_inventory_sha256 rng_address_upper_inventory_sha256
finite converged
```

`kernel_position` is the zero-based position in the fixed 15-position vector.
`worker_claim_sha256` and `boot_identity_sha256` identify the successful
execution. Its two successful perf-counter samples share that boot,
`successful_work_ns` is their nonnegative difference, and a positive-unit
record requires it to be positive.

Every boundary carries
`next_record_accounting_anchor_cumulative_ns`. At the first attempt's initial
worker-ready boundary it equals that boundary's cumulative cutoff, so one-off
attempt/bootstrap setup remains in lifecycle resource elapsed but is not
normalized as a repeated kernel rate. At a kernel boundary it advances to that
boundary's cumulative cutoff. Trace and measurement boundaries carry it
unchanged. An ordinary later new-trace worker-ready boundary also carries that
unchanged anchor, so trace/measurement publication, cleanup, the next
reservation and worker claim, capability setup, and worker-ready publication
enter the following k1 record exactly once. A worker-ready boundary after an
interruption instead resets it to that new boundary's cumulative cutoff; lost
execution and interruption administration are represented by the fixed replay
penalty and lifecycle clock rather than selected from a partially observable
timer.
For every record except positions `0` and `1`:

```text
accounting_started_cumulative_ns =
    predecessor_boundary.next_record_accounting_anchor_cumulative_ns

accounting_ended_cumulative_ns =
    current_kernel_boundary.cumulative_active_to_cutoff_ns

duration_ns =
    accounting_ended_cumulative_ns - accounting_started_cumulative_ns
```

Positions `0` and `1` are one indivisible first-operand epoch and share the
single post-k2 boundary. That boundary's
`trace_progress.first_operand_epoch` is nonnull and has exactly:

```text
record_positions internal_cutoff_cumulative_ns
internal_cutoff_perf_counter_ns registry replay
```

`record_positions=[0,1]`. After all k1 numerical work and durable resume-base
publication, but before any k2 work, the worker takes one same-boot monotonic
sample. It becomes both the k1 accounting end and k2 accounting start:

```text
k1.accounting_started_cumulative_ns =
    predecessor_boundary.next_record_accounting_anchor_cumulative_ns
k1.accounting_ended_cumulative_ns =
    first_operand_epoch.internal_cutoff_cumulative_ns
k1.duration_ns =
    k1.accounting_ended_cumulative_ns
    - k1.accounting_started_cumulative_ns

k2.accounting_started_cumulative_ns =
    first_operand_epoch.internal_cutoff_cumulative_ns
k2.accounting_ended_cumulative_ns =
    current_composite_boundary.cumulative_active_to_cutoff_ns
k2.duration_ns =
    k2.accounting_ended_cumulative_ns
    - k2.accounting_started_cumulative_ns
```

The cutoff is diagnostic state inside the composite boundary, not a durable
resume point. The two durations sum exactly to the epoch interval from the
predecessor accounting anchor through the post-k2 cutoff, with no overlap or
unassigned gap. A crash before that boundary commits neither record and
replays the whole epoch.

`first_operand_epoch.replay` is null when no epoch loss occurred. Otherwise it
is byte-equal to the consumed Section 16.1 pending-replay object with
`scope="first-operand-epoch"` and `record_positions=[0,1]`. The post-k2
boundary copies that object into this field and both record replay fields
before clearing top-level `trace_progress.pending_replay`.

`first_operand_epoch.registry` has exactly:

```text
names before_k1 after_k1_retained maximum_through_k1
after_k2_release after_k2_gc maximum_through_k2
```

`names` is the fixed nine-name vector and every count field is a nine-`u64`
vector. `before_k1` equals the predecessor boundary registry baseline.
`after_k1_retained` may exceed it only for the exact raw/date/design/base-date
authority required by k2; `maximum_through_k1` encloses both. After k2 has
issued the resume cell state, all live raw/design/panel objects are released
and collected; `after_k2_gc == before_k1` elementwise, and
`maximum_through_k2` encloses every epoch sample. Position 0 is the sole
exception to per-record baseline restoration. The composite epoch and every
later record restore baseline before their boundary.

The difference must be nonnegative and at least `successful_work_ns`.
`prelude_ns + kernel_ns + epilogue_ns = duration_ns`; the successful numerical
or I/O operation is inside `kernel_ns`, while source checks, reservation and
receipt carry, registry work, waits, scans, and cleanup are assigned to the
prelude or epilogue exactly once. Initial attempt/worker setup and interruption
administration remain in cumulative resource elapsed but, because they are
one-off or lost-execution work, are not falsely normalized as a successfully
completed production kernel. The fixed replay penalty below is the admission
charge for the latter. Final terminal publication receives the separately
reported fixed `terminal_close_accounting_charge_ns`; it is never misreported
as a duration or latency upper observed after its own encoding.

`variant` is `"default"` except the two kernel-13 positions. Offsets are
not used because one trace may span workers or boots. For every record:

```text
duration_plus_ns = duration_ns + 2 * clock_resolution_ns
replay_penalty_ns = 480000000000 * replay_count
admission_duration_ns = duration_ns + replay_penalty_ns
admission_duration_plus_ns =
    admission_duration_ns + 2 * clock_resolution_ns
```

Use the exact aliases:

```text
Rplus = duration_plus_ns
Aplus = admission_duration_plus_ns
```

All arithmetic is exact nonnegative integer arithmetic. `replay_count` is the
number of lost executions of this exact position recorded by Section 16.
For a lost first-operand epoch, one epoch ordinal increments both position-0
and position-1 `replay_count`; each record receives the full
`480000000000*r` admission penalty. The resulting doubled trace admission
charge is deliberate: neither k1 nor k2 can obtain a better per-kernel rate
through kill selection. Cumulative/lifecycle elapsed still counts each
physical epoch once, and each RNG upper contains only that record's own
licensed call sequence.
Relative rate gates are one-sided. Predictor/reference operands use `Rplus`;
held/current operands use `Aplus`. Every cold, conservative/projected task,
block, phase, combined, and final absolute projection or budget uses `Aplus`.
Raw successful timings remain diagnostics and successful-work stop clocks.
Increasing a replay count therefore cannot enlarge a reference prediction or
improve acceptance.
A zero-unit record has `successful_work_ns=0`, `kernel_ns=0`, no artifacts,
and no RNG calls, but its prelude/epilogue and boundary work remain charged in
`duration_ns`; for an I/O kernel its substage vector is exactly five zeros.

For artifact-producing kernels `1`, `2`, `3`, `4`, `5`, `6`, `8`, `9`,
`10`, `11`, `12`, `13`, and `14`, `substage_ns` is an exact five-element
`u64` array in this order:

```text
construction_and_serialization
hash_and_prepublication_validation
fsync_and_atomic_publication
reload_hash_validation_and_permitted_issuance
durable_receipt_and_cleanup
```

For a positive-unit listed kernel it is an alternate exhaustive partition of
the full `duration_ns`, including applicable prelude/epilogue work, and sums
exactly to `duration_ns`; the separate
`prelude_ns + kernel_ns + epilogue_ns` partition must agree on the same total.
For a zero-unit listed position it is exactly five zeros while its separately
reported prelude/epilogue orchestration remains charged in `duration_ns`. For
other kernels it is null.
Kernels 1--6 own the resume artifact created at their corresponding record
position: resume base, resume cell, bootstrap weights, then oracle,
homogeneous, and observable focals. The first four substages include its
construction through reload/issuance; the fifth includes any receipt,
release, registry collection, and cleanup work assigned below. K1's fifth
substage finishes before the internal epoch cutoff.
`artifact_inventory_rows` is the UTF-8-path-sorted array of exact
`[C-or-TC-relative artifact leaf, artifact_kind, artifact_sha256]` rows
created or first durably adopted by this kernel execution; it is empty for a
zero-unit or non-artifact kernel. `artifact_sha256s` is the sorted unique
third column and no other hash may appear there. These rows remain in the
later kernel boundary even after the timed cleanup deletes the final
artifacts. `finite` and `converged` are exact Booleans; a required false value
is terminal.
`cleanup_intent_sha256` is nonnull exactly for a positive-unit record at
position `9`, `12`, `13`, or `14` and hashes Section 16's exact cleanup-intent
receipt bytes. It is null otherwise. `cleanup_completion_boot_identity_sha256`
is null with a null intent; otherwise it identifies the boot on which the
frozen deletion suffix and parent fsync completed. It equals the successful
record boot absent interruption and may differ only under the exact
cleanup-intent continuation. Numerical work, successful perf-counter fields,
RNG evidence, and artifact rows always retain the original successful
worker/boot identity.
`terminal_close_probe_evidence_sha256` is null for kernels 1--13 and is
Section 10's exact probe-evidence digest for kernel 14. Kernel 14's
`artifact_sha256s` contains only the publication-envelope artifact SHA256;
the two separate fields prove that its timed unit exercised both publisher
state machines without relabeling receipt evidence as an artifact hash.

`rng_call_count` and `rng_address_inventory_sha256` describe only the
successful execution's exact licensed calls. For a zero-call record the
inventory is the canonical empty inventory. Let `L` be the frozen complete
licensed call sequence for this position and let `r=replay_count`. Then
`rng_call_upper_count = rng_call_count + r*len(L)`, and
`rng_address_upper_inventory_sha256` is exactly:

```text
SHA256(CJSON([
  "xid-g2-resource-record-address-upper-inventory-v1",
  kernel_position,
  [[replay_ordinal_or_zero, entropy_13_words], ...],
]))
```

Rows contain the successful call sequence in actual call order tagged with
ordinal zero, followed by `r` complete copies of `L` in replay-ordinal
`1..r` outer order and licensed-call inner order. The row count equals
`rng_call_upper_count`; a zero-call, zero-replay record has the canonical empty
row array. This is a deterministic upper inventory, not a claim that every
lost process reached its last call.

`R/traces/trace-<10-digit t>/receipt.json` has exactly:

```text
schema_version receipt_kind attempt_sha256 trace_index panel_index
reservation_sha256 epoch_index role phase measurement_block pair_index
recovery_trigger_interruption_sha256
worker_claim_sha256s panel_source_snapshot_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
executable_source_snapshot_sha256 authority_source_snapshot_sha256
runtime_sha256 resource_config_sha256 boot_identity_sha256s
panel_evidence started_wall_time_ns ended_wall_time_ns
trace_started_cumulative_active_ns cumulative_active_to_trace_end_ns
successful_duration_ns admission_duration_ns lifecycle_active_ns
clock_resolution_ns kernel_records rng_address_inventory_sha256
rng_address_upper_inventory_sha256 rng_call_count rng_call_upper_count
artifact_inventory_rows artifact_inventory_sha256 artifact_sha256s
cleanup_intent_sha256s resume_state registry_counts rss disk complete
```

`receipt_kind` is `"resource-trace-receipt-v1"`, `complete` is true, and the
role/phase/block/pair/recovery-trigger fields exactly equal the reservation.
`worker_claim_sha256s` and `boot_identity_sha256s` are the sorted unique sets
from the successful kernel records. The wall values are positive `u64` samples
bracketing the trace's first reservation and final record and must be
nondecreasing; they never derive a kernel rate. A backward wall clock is
terminal.
`trace_started_cumulative_active_ns` is the cumulative cutoff immediately
before reservation publication.
`cumulative_active_to_trace_end_ns` is the final kernel boundary's exact
cumulative cutoff. Define:

```text
successful_duration_ns =
    sum(record.duration_ns for record in kernel_records)

admission_duration_ns =
    sum(record.admission_duration_ns for record in kernel_records)

lifecycle_active_ns =
    cumulative_active_to_trace_end_ns
    - trace_started_cumulative_active_ns
```

All differences are nonnegative. `successful_duration_ns` is the only trace
time used for the 600-/200-second minimum-work stops;
`admission_duration_ns` and the per-record admission-plus fields govern every
admission comparison. `lifecycle_active_ns` is reported separately and enters
the cumulative resource budget. Trace indices and reservations are contiguous.
A partial trace is resumable only from Section 16's exact durable prefix; an
unreceipted non-prefix state is terminal.

`panel_evidence` has exactly:

```text
base_artifact_sha256 base_panel_token cell_artifact_sha256 cell_panel_token
panel_source_snapshot_sha256
```

Every value is a SHA256. The source digest repeats the trace's panel source
digest and must equal both inherited panel manifests. Both artifact hashes and
tokens equal the issued inherited evidence used by the trace.

`artifact_inventory_rows` is the UTF-8-path-sorted array:

```text
[[C-relative artifact leaf, artifact_kind, artifact_sha256], ...]
```

It contains every inherited or new artifact owned by this trace, including
artifacts deleted inside its combined kernel. A new artifact belongs
to trace `t` only when its manifest has `creation.trace_index=t`; an inherited
`base-panel` or `cell-panel` belongs only when its unchanged manifest address
has the trace's exact reserved `panel_index`. The path, kind, and digest must
have revalidated immediately before timed deletion and must equal the
corresponding durable kernel-record row byte-for-byte. At trace receipt
publication every listed final artifact must be absent; an extant, unlisted,
or mismatched artifact is terminal.
`artifact_inventory_sha256` is:

```text
SHA256(CJSON([
  "xid-g2-resource-artifact-inventory-v1",
  artifact_inventory_rows,
]))
```

`artifact_sha256s` is the sorted unique array of the third column. Thus the
durable trace receipt preserves the exact path/kind/hash join even after an
eligible fixture is deleted; a digest alone or an unordered kernel-level hash
set is insufficient.

`resume_state` is the final Section 16 object and every boundary prefix carries
its current value. It has exactly:

```text
schema_version rows aggregate_token_inventory_sha256
paper_weight_inventory_sha256
production_panel_evidence sha256
```

`schema_version=2`. `rows` has exactly seven UTF-8-path-sorted rows:

```text
[relative_leaf, artifact_kind, variant,
 artifact_sha256_or_null, payload_inventory_sha256_or_null, parents,
 producer_position, last_consumer_position, cleanup_position, state]
```

The fixed semantic coordinates are:

| Resume row | Producer | Last consumer | Cleanup |
| --- | ---: | ---: | ---: |
| base panel | 0 | 8 | 9 |
| cell panel | 1 | 8 | 9 |
| bootstrap weights | 2 | 5 | 9 |
| oracle focals | 3 | 9 | 9 |
| homogeneous focals | 4 | 9 | 9 |
| observable focals | 5 | 9 | 9 |
| paper bootstrap weights, equal | 12 | 13 | 13 |
| paper bootstrap weights, validation | 12 | 12 | 12 |
| paper bootstrap weights, research | 13 | 13 | 13 |

Exactly one of the final three role alternatives is present, so the concrete
state always has six smooth rows plus one paper-weight row.

`relative_leaf` is the exact `C`- or `TC`-relative Section 7 path for this
panel, without a trailing slash. `artifact_kind`, `variant`, and `parents`
equal the validated manifest; the focal variants are exactly `"oracle"`,
`"homogeneous"`, and `"observable"`, while the other variants are
`"default"`. Once published, neither digest becomes null again.
`payload_inventory_sha256_or_null` is:

```text
SHA256(CJSON([
  "xid-g2-resource-resume-payload-inventory-v1",
  [[payload.name, payload.sha256] for payload in manifest.payloads],
]))
```

in manifest order. State is exactly `"not-yet-published"` before the producer,
`"required-present"` from publication through the boundary before its last
consumer, `"retained-present"` after that consumer's numerical work but before
its cleanup-intent marker, and `"deleted"` after the cleanup suffix. The
retained state therefore appears inside the exact cleanup intent even when it
never appears at a kernel boundary. A present state requires a byte-valid
final; deleted requires absence while retaining all hashes and parents.

`aggregate_token_inventory_sha256` is null before position 2 and thereafter
equals Section 7.9. `paper_weight_inventory_sha256` is null before the
role-resolved producer, equals Section 7.9a from that publication onward, and
remains committed after deletion. The paper row's `variant` is exactly
`"paper-bootstrap-weights"`; its role-resolved producer, consumer, and cleanup
coordinates are selected from the table above and may not be caller supplied.
`production_panel_evidence` has exactly the five
`panel_evidence` keys; the base pair is null before position 7, the cell pair
is null before position 8, and every nonnull value is retained after deletion.
The state digest is:

```text
SHA256(CJSON([
  "xid-g2-resource-resume-state-v2",
  2,
  rows,
  aggregate_token_inventory_sha256,
  paper_weight_inventory_sha256,
  production_panel_evidence,
]))
```

The trace receipt requires all seven resume rows in state `"deleted"` and full
production panel evidence. `cleanup_intent_sha256s` is the cleanup-receipt
hashes owned by this trace in increasing global cleanup index.

Every post-epoch operand consumer has one path on uninterrupted and resumed
workers:

1. Position 2/k3 loads the resume base/cell panels, draws the 25 licensed
   bootstrap-weight rows, constructs and validates all 25 aggregates, publishes
   the weight artifact plus aggregate-token inventory, then releases panels,
   weights, and aggregates before its boundary.
2. Positions 3, 4, and 5/k4--k6 each load the resume panels and saved weights,
   recompute all 25 aggregates in replicate order, require the aggregate-token
   inventory, execute only its named candidate fit, publish that focal
   artifact, and release all issued objects.
3. Position 6/k7 loads the observable focal artifact and derives the fixed
   499-value in-memory fixture; it does not refer to the not-yet-published null
   artifact.
4. Position 7/k9 loads the resume base panel, writes/reloads the inherited
   production base artifact, releases the issued wrapper, and retains the
   immutable final for k10.
5. Position 8/k10 loads the resume cell panel, validates the retained
   production base parent, writes/reloads the inherited production cell
   artifact, releases wrappers, and retains both production finals for k8.
6. Position 9/k8 loads all three focal artifacts, validates both retained
   production panels and their parent tokens, publishes/reloads the null
   artifact, then follows its nine-row cleanup intent.
7. The first positive kernel-13 position draws and publishes the paper
   bootstrap-weight row. The last positive kernel-13 position loads exactly
   those bytes and removes them through its cleanup intent. Equal traces
   therefore draw at position 12 and reload at 13; validation draws and
   consumes at 12; research draws and consumes at 13. A zero-unit variant
   constructs no RNG and never reconstructs the weights.

Every load, recomputation, parent validation, and release is charged to that
record's prelude/epilogue and five-substage partition where applicable. The
nine registry counts equal baseline at every durable work boundary. No
aggregate object crosses a boundary and no bootstrap RNG is reconstructed
after k3.

Artifact cleanup occurs inside the originating combined-kernel timing and
before that kernel's boundary, but only after Section 16's immutable cleanup
intent has committed. Validated manifest/marker bytes and the intent's exact
row inventory are the pre-deletion authority; an in-memory list alone cannot
license deletion.

The last-use assignment is exact:

```text
k8:  null-batch artifact; production base-panel and cell-panel artifacts;
     resume base panel, resume cell panel, bootstrap weights, and all three
     candidate-focal artifacts (nine targets total)
k13 recovery:
      recovery cache, recovery bootstrap batch, recovery paper-date parent;
      validation also deletes its paper bootstrap weights
k13 research:
      research cache, research bootstrap batch, full paper-date parent;
      equal and research also delete their paper bootstrap weights
k14: publication envelope and terminal-close probe
```

K9 retains its production base artifact for k10. K10 retains both production
panels for k8, whose null manifest binds their hashes and whose cleanup intent
then removes the complete smooth tree. Any unexpected still-accounted
artifact at k14 is terminal; it is not silently added to the intent.
Kernels 11 and 12 retain their paper-date parents only until the named k13
variant consumes them. The shared paper-weight final remains through the
role-resolved last positive k13 variant and both paper-bootstrap manifests
bind it as parent role `"resume-paper-bootstrap-weights"`. Kernel 14's probe
is a receipt rather than an artifact
row, but its deletion remains in the same fifth substage. Rehearsal and
registered paths use the same last-use rule. Thus every final binary artifact
is absent by the position-14 boundary; only durable result-tree receipts and
their row commitments remain.

Within a position, cleanup targets are ordered by descending repository-
relative UTF-8 path bytes; each tree is removed children-first and its parent
is fsynced. Before a complete intent, no deletion is permitted. After it, the
only valid cleanup states are an exact missing prefix and byte-valid remaining
suffix of that order. A loss after the intent resumes only deletion of that
suffix and boundary publication: it adds no replay count, reconstructs
nothing, and performs no RNG or numerical work. A loss before a complete
intent removes any uniquely derivable uncommitted finals and replays the
current record or first epoch with the fixed penalty.
The completed record's fifth `substage_ns`, `kernel_ns`, `duration_ns`, disk
high water, and RSS high water include validation, durable pre-deletion
intent publication, deletion, and parent fsync. The trace receipt then sets
`artifact_inventory_rows` to the globally path-sorted concatenation of its 15
kernel-record row arrays and requires global path uniqueness. It performs no
post-boundary artifact cleanup.

The RNG address inventory is:

```text
SHA256(CJSON([
  "xid-g2-resource-address-inventory-v1",
  [[entropy_word_0, ..., entropy_word_12], ...],
]))
```

in actual call order. It contains only licensed resource addresses and its row
count equals `rng_call_count`.

The trace upper inventory concatenates each record's tagged upper rows in
kernel-position order and hashes:

```text
SHA256(CJSON([
  "xid-g2-resource-address-upper-inventory-v1",
  [[kernel_position, replay_ordinal_or_zero,
    [entropy_word_0, ..., entropy_word_12]], ...],
]))
```

Ordinal zero is the successful sequence; positive ordinals are complete
licensed replay-upper sequences. Its row count equals
`rng_call_upper_count`. No unknown partial physical prefix is presented as an
observed call.

`registry_counts` has exactly:

```text
names before retained_high_water after_release after_gc
```

`names` is exactly:

```text
["_RAW_BASE_REGISTRY",
 "_G2_DATE_REGISTRY",
 "_CONTRACT_DESIGN_REGISTRY",
 "_CONTRACT_BASE_DATE_REGISTRY",
 "_CONTRACT_CELL_DATE_REGISTRY",
 "_CONTRACT_BASE_PANEL_REGISTRY",
 "_CONTRACT_CELL_PANEL_REGISTRY",
 "_CONTRACT_AGGREGATE_REGISTRY",
 "_RESOURCE_ARTIFACT_REGISTRY"]
```

Each count vector has nine `u64` values. `after_gc` must equal `before`
elementwise.

`rss` has exactly:

```text
sample_period_ns maximum_sample_gap_ns sampled_tree_peak_bytes
rusage_highwater_envelope_bytes supervisor_rusage_highwater_bytes
worker_waits preterminal_git_rusage_highwater_bytes rss_envelope_bytes sample_count
all_wait_statuses_collected
```

The sample period is `50,000,000`; the observed maximum gap is at most
`1,000,000,000`; `rss_envelope_bytes` is the maximum of the sampled tree peak and
`rusage_highwater_envelope_bytes`. `worker_waits` is the exact cumulative
Section 4.6 object at the trace cutoff, and
`supervisor_rusage_highwater_bytes` is the same-cutoff zeroed-`getrusage`
sample. `preterminal_git_rusage_highwater_bytes` is Section 4.6's exact
bootstrap-check maximum at every nonterminal trace cutoff. Because all children
are serial:

```text
rusage_highwater_envelope_bytes =
    supervisor_rusage_highwater_bytes
    + max(
        max([row[7] for row in worker_waits.rows], default=0),
        preterminal_git_rusage_highwater_bytes
    )
```

Column seven is the frozen worker `ru_maxrss_bytes` value. Every PID is keyed by
`(pid, process_start_identity)`. Every reaped child has
one exact wait row. `all_wait_statuses_collected=true` iff every issued worker
that has exited by this cutoff is represented and the bootstrap check has all
twelve exact Git wait/rusage rows; a terminal success later requires one row
for every issued worker plus both complete preterminal Git checks. A sampler
failure or gap over one second is terminal, not resumable.

`disk` has exactly:

```text
result_start result_end result_high_water checkpoint_start checkpoint_end
checkpoint_high_water scratch_start scratch_end scratch_high_water
checkpoint_active_tree_high_water outside_baseline_bytes
created_roots_high_water_bytes absolute_workspace_high_water_bytes
filesystem_start filesystem_end
```

Each root snapshot has exactly `logical_bytes` and `allocated_bytes`; each
reported scalar uses the larger of the applicable summed logical and allocated
values. `filesystem_start` and `filesystem_end` are Section 18 snapshots
bracketing the trace and must preserve the attempt devices/units exactly.
Section 18 defines the inequalities.

## 14. Measurement-block receipts

`R/measurements/block-<j>/receipt.json`, for `j=1..3`, has exactly:

```text
schema_version receipt_kind attempt_sha256 block_index epoch_indices
publisher_supervisor_pid publisher_supervisor_start_identity
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
equal_trace_index pair_trace_indices trace_inventory_sha256
successful_duration_ns admission_duration_ns pair_count
phase_summaries stationarity complete
```

`receipt_kind` is `"resource-measurement-block-v1"`, `complete` is true,
`pair_count >= 4`, and `successful_duration_ns >= 200,000,000,000`.
`epoch_indices` is the ordered unique list encountered by the block's
measurement-role traces; it has length one without interruption and may grow
only after Section 16's exact fresh recovery thermalization.
`pair_trace_indices` is an ordered array of two-element trace-index arrays
following `(V,R),(R,V),...`. Define the unique ordered trace sequence:

```text
block_trace_indices =
    [equal_trace_index] + flatten(pair_trace_indices)
```

These indices are strictly increasing and are consecutive within the
measurement-role subsequence. On an uninterrupted attempt they are globally
consecutive. After an admitted resume, only the exact fresh recovery-
thermalization traces in Section 16 may intervene in global trace order; they
cannot enter `block_trace_indices`, a pair count, or a phase summary. All
referenced trace receipts and every intervening thermal receipt must validate
before block publication. Let `trace_sha256[t]` hash the exact corresponding
trace receipt bytes. Then:

```text
trace_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-measurement-trace-inventory-v1",
  [[t, trace_sha256[t]] for t in block_trace_indices],
]))

successful_duration_ns =
    sum(trace_receipt[t].successful_duration_ns for t in block_trace_indices)

admission_duration_ns =
    sum(trace_receipt[t].admission_duration_ns for t in block_trace_indices)

pair_count = len(pair_trace_indices)
```

The successful sum is the precommitted 200-second completed-work stop clock.
It includes the equal trace and all phase traces; replay penalties cannot make
a block stop early. The admission sum retains every replay penalty. Receipt,
boundary, reservation, and cleanup work assigned through Section 13's
cumulative record anchors is included exactly once; the terminal tail after
the last record remains in cumulative resource time and the separately
bounded close.

`phase_summaries` has exactly `validation` and `research`. Each has exactly:

```text
trace_indices pair_count units_by_kernel duration_by_kernel
reference_duration_plus_by_kernel admission_duration_plus_by_kernel
successful_total_ns reference_total_plus_ns admission_total_plus_ns
```

The three kernel vectors use the fixed 15-position order in Section 13 and are
exact sums over that phase's traces. `duration_by_kernel` sums raw record
durations; `reference_duration_plus_by_kernel` sums `duration_plus_ns`;
`admission_duration_plus_by_kernel` sums `admission_duration_plus_ns`. The
three total fields are their corresponding vector sums.

`stationarity` has exactly `overall`, `validation`, and `research`. Each is
null for block 1. For blocks 2 and 3 it has exactly:

```text
method previous_count current_count previous_reference_total_plus_ns
current_admission_total_plus_ns lhs rhs passed
```

with:

```text
method = "one-sided-replay-monotone-stationarity-v1"
lhs = 20 * current_count * previous_reference_total_plus_ns
rhs = 19 * previous_count * current_admission_total_plus_ns
passed = (lhs >= rhs)
```

For `overall`, count is the complete balanced-pair count; the previous
reference total is the sum of `duration_plus_ns`, and the current admission
total is the sum of `admission_duration_plus_ns`, over the flattened phase
traces excluding the equal trace. Phase entries use the same pair count and
the corresponding totals over the named phase's exact `trace_indices`. All
three must pass. Raw successful-duration ratios are diagnostics and cannot
override the one-sided comparison.

## 15. Temporal and core cross-context rate robustness

For block `j`, phase `p`, and kernel position `k`, let:

```text
U[j,p,k]     = summed units
Rplus[j,p,k] = summed duration_plus_ns
Aplus[j,p,k] = summed admission_duration_plus_ns
Oplus[j,p]   = admission_total_plus_ns
```

For the two other blocks `a` and `b`, define the same-phase temporal
prediction:

```text
H[j,p,k] = max(
  ceil_div(U[j,p,k] * Rplus[a,p,k], U[a,p,k]),
  ceil_div(U[j,p,k] * Rplus[b,p,k], U[b,p,k]),
)
H[j,p] = sum_k H[j,p,k]
```

A zero held-out unit contributes zero. Every positive held-out unit requires
positive comparison-block units and admission duration. The check is:

```text
Oplus[j,p] <= ceil_div(5 * H[j,p], 4).
```

Let `q` be the phase other than `p`, and let the common kernel positions be:

```text
C = {k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k14}.
```

For each `k in C`, define the cross-phase prediction:

```text
X[j,p,k] = max(
  ceil_div(U[j,p,k] * Rplus[a,q,k], U[a,q,k]),
  ceil_div(U[j,p,k] * Rplus[b,q,k], U[b,q,k]),
)
```

Every denominator and prediction is positive. Require both:

```text
Aplus[j,p,k] <= ceil_div(5 * X[j,p,k], 4)  for every k in C

sum_{k in C} Aplus[j,p,k]
    <= ceil_div(5 * sum_{k in C} X[j,p,k], 4).
```

Kernels 11, 12, and both kernel-13 variants are outside the cross-phase set.
They retain cold, equal, and own-phase slowest-context projection. The
temporal and cross-phase checks do not establish linear scaling to the frozen
full-work matrix.

The terminal `rate_robustness` object has exactly:

```text
method temporal_checks cross_context_checks
all_temporal_passed all_cross_context_passed all_passed
maximum_temporal_ratio_numerator maximum_temporal_ratio_denominator
maximum_cross_context_ratio_numerator maximum_cross_context_ratio_denominator
```

`method` is
`"blocked-temporal-and-cross-phase-core-replay-monotone-v1"`.
`temporal_checks` is an ordered six-element array by block `1..3`, then phase
validation/research. Each check has exactly:

```text
block_index phase held_admission_plus_ns reference_predicted_plus_ns
upper_ns passed
```

`cross_context_checks` is an ordered 72-element array by block `1..3`, phase
validation/research, then kernels `1..10,14`, then the aggregate. Each check
has exactly:

```text
block_index phase scope kernel_id held_admission_plus_ns
reference_predicted_plus_ns upper_ns passed
```

`scope` is `"kernel"` with `kernel_id` equal to the named integer, or
`"aggregate"` with `kernel_id` JSON null. The two maximum ratios are the exact
unreduced held-`Aplus` numerator and `Rplus`-derived reference denominator from
the applicable check with maximum cross-multiplied ratio; ties use the array
order above. The three pass Booleans are the exact conjunctions of their
arrays.

## 16. Interruption and resume receipts

Completed reservations, worker claims, kernel records, traces, measurements,
artifacts, cleanup intents, and terminal evidence are irrevocable. Resume may
not delete, replace, or ignore an unfavorable completed receipt.

The ten-minute lost-work invariant is enforced between durable checkpoint/work
markers. The canonical no-interruption trace, and every rehearsal trace, has
the exact boundary schedule:

```text
local boundary 0: worker ready, next position 0
local boundary 1: positions 0 and 1 complete, next position 2
local boundary p for p=2..14:
    positions 0..p complete, next position p+1
```

Thus a canonical trace has one worker-ready plus fourteen work boundaries,
fifteen boundary leaves total. The first work boundary commits both k1 and k2;
no boundary exists between them. A registered partial-trace resume adds one
worker-ready boundary after each permitted interruption and before ordinary
continuation or replay. Those additional leaves copy the durable prefix and do
not alter the canonical next-position vector, the fifteen-leaf rehearsal
schedule, or any fixed rehearsal count. Registered execution additionally
publishes a boundary after each complete trace receipt and each measurement
receipt. Cleanup intents at positive-unit positions 9, 12, 13, and 14 are
intermediate durable markers, not boundary leaves.

For every boundary or cleanup intent reached by ordinary work or a
supervisor-only continuation, elapsed work from completion of the immediate
predecessor durable checkpoint/work marker through the current pre-encoding
cutoff is at most `480000000000` ns. Here and below that predecessor is exactly
`attempt.json`, a boundary, a cleanup intent, or an interruption receipt.
Intervening reservation, worker-claim, trace, or measurement receipts are
governance/evidence leaves and do not reset the watchdog or accounting anchor;
their following boundary does. Atomic marker publication accounting is at most
`60000000000` ns, so:

```text
marker_interval_ns =
    chunk_work_elapsed_ns + publication_accounting_ns
marker_interval_ns <= 540000000000 < 600 seconds.
```

The supervisor owns both watchdogs. The first worker-ready boundary uses the
durable `attempt.json` publication as predecessor. A work timeout is terminal;
the fixed k1+k2 epoch or record is never resized. Interruption publication
itself may follow a conservatively charged shutdown/downtime gap and therefore
is not relabeled a normal 480-second work interval, but its own publication
still has the 60-second cap. The next work interval starts at that interruption
marker.

### 16.1 Boundary receipt and exact trace progress

The registered boundary path is:

```text
R/boundaries/boundary-<10-digit d>/receipt.json
```

plus its Section 10 marker. The receipt has exactly:

```text
schema_version receipt_kind attempt_sha256 boundary_index boundary_kind
predecessor_boundary_sha256 predecessor_durable_marker_kind
predecessor_durable_marker_sha256 worker_claim_sha256 boot_identity_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
last_complete_trace_index completed_measurement_block
active_measurement_block next_panel_index next_trace_index trace_progress
pending_signal_number terminal_entry next_watchdog_arm
terminal_size_preflight cumulative_active_to_cutoff_ns
cutoff_wall_time_ns cutoff_perf_counter_ns
chunk_work_elapsed_ns boundary_publication_upper_ns chunk_upper_ns
attempt_bootstrap_elapsed_ns
predecessor_durable_marker_publication_accounting_ns
predecessor_durable_marker_publication_method
next_record_accounting_anchor_cumulative_ns
rss_sample_count_to_cutoff rss_maximum_sample_gap_ns_to_cutoff
rss_sampled_tree_peak_to_cutoff_bytes
rss_supervisor_rusage_highwater_to_cutoff_bytes
rss_worker_waits_to_cutoff
rss_preterminal_git_rusage_highwater_to_cutoff_bytes
rss_rusage_highwater_envelope_to_cutoff_bytes
rss_observed_to_cutoff_bytes rss_admission_upper_bytes
rss_observation_complete_to_cutoff
created_roots_high_water_observed_bytes created_roots_at_cutoff_bytes
created_roots_resume_upper_bytes checkpoint_tree_high_water_bytes
checkpoint_tree_admission_upper_bytes disk_observation_complete_to_cutoff
absolute_workspace_resume_upper_bytes filesystem registries
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
complete
```

`receipt_kind="resource-resume-boundary-v1"`, `complete=true`, and indices are
contiguous from zero. `boundary_kind` is `"worker-ready"`,
`"kernel-record"`, `"trace"`, or `"measurement-block"`.
`predecessor_boundary_sha256` is null only at boundary zero and otherwise
hashes boundary `d-1`; it is the logical boundary chain even when another
durable marker intervenes. `predecessor_durable_marker_kind` is exactly
`"attempt"`, `"boundary"`, `"cleanup-intent"`, or `"interruption"`, and its
SHA256 hashes the exact immediate predecessor receipt bytes. At boundary zero
the kind is `"attempt"` and the digest is `attempt_sha256`.

`terminal_entry` is false at every boundary except a final block-3
`"measurement-block"` boundary that has no remaining numerical work and whose
terminal-size preflight passes. It may be true only at that one boundary.
When true, `next_watchdog_arm` is null and `terminal_size_preflight` is the
exact nonnull success object below. When the final block-3 preflight fails, the
boundary remains an ordinary `terminal_entry=false` boundary, persists the
failed preflight, publishes no successor worker or capability, and selects the
ordinary terminal-failure lane. At every other boundary,
`terminal_size_preflight` is null. `next_watchdog_arm` is the exact Section 11
arm whenever later worker work remains and is otherwise null; work governed by
it cannot start before this boundary is durable.

`terminal_size_preflight` has exactly:

```text
schema_version terminal_kind cap_bytes fixture_schema_sha256
file_upper_rows passed
```

`schema_version=1`, `terminal_kind` is `"registered-success"` here, and
`cap_bytes=1048576`. `file_upper_rows` is exactly:

```text
[["terminal/success/result.json", result_upper_bytes],
 ["terminal/success/_SUCCESS", success_marker_upper_bytes]]
```

in that order. Each upper is the exact output of the frozen deterministic
maximum-width canonical fixture generator for the selected schema after
substituting the current attempt's already bounded category counts and every
still-unknown terminal child/output field with its admitted maximum.
`fixture_schema_sha256` is:

```text
SHA256(CJSON([
  "xid-g2-resource-terminal-size-fixture-schema-v1",
  ["failure-intent",
   "failure-resume-index-zero",
   "failure-resume-progress",
   "failure-resume-death",
   "failure-resume-cleanup-complete",
   "rehearsal-success-result",
   "rehearsal-failure-result",
   "registered-success-result",
   "registered-failure-result",
   "success-marker",
   "failure-marker"],
  [64,128,512,641,240,24,12,1201],
  1048576,
]))
```

The numeric vector binds respectively maximum worker waits, process deaths,
cleanup rows, failure resumes, path bytes, preterminal Git rows, post-JSON Git
rows, and publication-RSS samples. The following scalar binds the per-file
cap. `passed` is true iff every row upper is at most the cap and the
implementation reproduced this fixture-schema digest. A malformed, missing,
or failing object cannot be `terminal_entry=true`.

Ordinarily `worker_claim_sha256` and `boot_identity_sha256` identify the
worker/boot that completed the boundary's work. For a supervisor-only
cross-boot cleanup continuation, the worker hash remains the original
successful record and cleanup-intent claim, while the boundary boot identifies
the supervisor boot that completed deletion and publication; it must equal
the record's `cleanup_completion_boot_identity_sha256`. This is the sole
permitted worker-claim/boot divergence.

`completed_measurement_block` is the greatest complete block in `0..3`;
`active_measurement_block` is null outside a block. `pending_signal_number`
is null or the first latched `SIGTERM`, `SIGINT`, or `SIGHUP` number `15`,
`2`, or `1`. Only the first worker-ready boundary after its interruption may
clear it.

At boundary zero, `attempt_bootstrap_elapsed_ns` is the exact cumulative
elapsed from `attempt.time_origin.perf_counter_ns` through durable
`attempt.json` parent fsync and is at most `480000000000`; it is null later.
A crash before visible `attempt.json` may discard only its bounded stage. A
visible attempt remains consumed.

`trace_progress` is null at complete-trace and measurement boundaries.
Otherwise it has exactly:

```text
trace_index panel_index reservation_sha256 epoch_index role phase
measurement_block pair_index trace_started_cumulative_active_ns
started_wall_time_ns completed_kernel_positions next_kernel_position
kernel_records first_operand_epoch resume_state pending_replay
```

At an initial new-trace worker-ready boundary, positions and records are empty,
`next_kernel_position=0`, `first_operand_epoch=null`, `pending_replay=null`,
and `resume_state` is Section 13's seven-row initial object. A resumed
partial-trace worker-ready boundary instead copies every `trace_progress` field
byte-for-byte from the latest complete boundary—including trace/reservation
identity, role/phase/block/pair coordinates, trace-start cumulative and wall
times, completed positions, next position, kernel records, first-epoch object,
and resume state—except that `pending_replay` is set by the exact interruption
transition below. It never advances the position or resets trace-start
evidence. After the composite epoch boundary, positions are `[0,1]`, next is
`2`, and `first_operand_epoch` is Section 13's exact nonnull object. Thereafter,
after record position `p=2..14`, positions are `[0,...,p]` and next is `p+1`.
At next `15`, the trace receipt reproduces all records and the final resume
state before a trace boundary clears progress. A partial measurement block is
reconstructed only from its durable trace prefix.

`pending_replay` is null or has exactly:

```text
scope record_positions lost_execution_count record_rows sha256
```

`scope` is `"record"` with `record_positions=[p]`, or
`"first-operand-epoch"` with `[0,1]`. `lost_execution_count=r` is a positive
`u32`. `record_rows` is ascending by position and each row is:

```text
[kernel_position, replay_penalty_ns, rng_call_upper_increment,
 rng_replay_increment_inventory_sha256]
```

For every row:

```text
replay_penalty_ns = 480000000000 * r
rng_call_upper_increment = r * len(L_kernel_position)
```

The fourth element hashes only that replay increment:

```text
SHA256(CJSON([
  "xid-g2-resource-replay-increment-v1",
  kernel_position,
  [[replay_ordinal, entropy_13_words], ...],
]))
```

The rows use replay ordinal `1..r` as the outer order and, within each ordinal,
the frozen complete licensed sequence `L_kernel_position` in call order. The
row count is therefore exactly `r*len(L_kernel_position)`; k2's canonical empty
sequence produces the canonical empty row array. This is not the eventual
record upper inventory: Section 13 separately hashes successful ordinal zero
followed by these positive-ordinal rows. The pending object digest is:

```text
SHA256(CJSON([
  "xid-g2-resource-pending-replay-v1",
  scope,
  record_positions,
  lost_execution_count,
  record_rows,
]))
```

The epoch object has two rows and one loss ordinal; both eventual records
receive the full penalty, while each increment digest contains only its own
licensed sequence. K2 may have the canonical empty licensed sequence.
Repeated losses add to `r` without changing scope or positions. A completed
record/epoch consumes the object into its record fields and clears
`pending_replay`. Cleanup-intent continuation never creates replay evidence.

The cutoff samples are consecutive positive `u64` values taken after required
waits, registry restoration, RSS reconciliation, and disk scans but before
encoding. `chunk_work_elapsed_ns` runs from the supervisor's post-publication
sample for the immediate predecessor durable checkpoint/work marker defined
above through this cutoff.
`boundary_publication_upper_ns=60000000000` and
`chunk_upper_ns=chunk_work_elapsed_ns+boundary_publication_upper_ns`; both
fixed limits must pass.

Only durably closed process segments contribute favorable observations.
`rss_sample_count_to_cutoff` counts exact 50-ms samples from complete segments;
`rss_maximum_sample_gap_ns_to_cutoff` is their maximum adjacent within-segment
gap and is at most `1000000000`.
`rss_sampled_tree_peak_to_cutoff_bytes` is the cumulative actual sampled
maximum over those segments. `rss_worker_waits_to_cutoff` is the exact
cumulative Section 4.6 object and must extend the immediate predecessor's
inventory. `rss_supervisor_rusage_highwater_to_cutoff_bytes` is the current
zeroed-`getrusage` high-water sample.
`rss_preterminal_git_rusage_highwater_to_cutoff_bytes` is the exact Section
4.6 bootstrap-check maximum at every ordinary boundary/cleanup cutoff. Because
all children are serial:

```text
rss_rusage_highwater_envelope_to_cutoff_bytes =
    rss_supervisor_rusage_highwater_to_cutoff_bytes
    + max(
        max(
            [row[7] for row in rss_worker_waits_to_cutoff.rows],
            default=0
        ),
        rss_preterminal_git_rusage_highwater_to_cutoff_bytes
    )
```

The row index is the frozen `ru_maxrss_bytes` column. A live supervisor sets
`rss_observation_complete_to_cutoff=true` only after continuous sampling,
one wait/rusage row for every issued worker that has exited, and its final
cutoff sample. A still-live current worker is permitted at a nonterminal
boundary; its eventual wait row is mandatory before success, while loss before
that row can close only as a failing Section 16 non-wait death proof.
Similarly, `disk_observation_complete_to_cutoff=true` requires a final
no-follow disk scan on the same live segment. Define:

```text
rss_observed_to_cutoff_bytes =
    max(
        rss_sampled_tree_peak_to_cutoff_bytes,
        rss_rusage_highwater_envelope_to_cutoff_bytes
    )

rss_admission_upper_bytes =
    max(
        prior_durable_rss_admission_upper_bytes_or_zero,
        ceil_div(5 * rss_observed_to_cutoff_bytes, 4),
        3500000001 if not rss_observation_complete_to_cutoff else 0
    )

checkpoint_tree_admission_upper_bytes =
    max(
        prior_durable_checkpoint_tree_admission_upper_bytes_or_zero,
        ceil_div(5 * checkpoint_tree_high_water_bytes, 4),
        2000000001 if not disk_observation_complete_to_cutoff else 0
    )
```

The observed checkpoint tree must also be at most `1600000000` bytes before
any mutation, the largest value compatible with its 25% margin and the
`2000000000`-byte cap. No conservative upper is relabeled observed or
multiplied twice. Define disk carry:

```text
created_roots_resume_upper_bytes =
    max(
        prior_durable_created_roots_resume_upper_bytes_or_zero,
        created_roots_high_water_observed_bytes,
        created_roots_at_cutoff_bytes + F_close,
        6000000001 if not disk_observation_complete_to_cutoff else 0
    )

absolute_workspace_resume_upper_bytes =
    max(
        outside_baseline_bytes + created_roots_resume_upper_bytes,
        30000000001 if not disk_observation_complete_to_cutoff else 0
    )
```

where `F_close` is Section 18. `filesystem` matches the attempt device/unit
invariants. Any false completeness value selects
`"select-terminal-failure-telemetry-gap"` and forbids another worker,
capability, RNG call, or thermal trace. `registries` has exactly:

```text
names baseline final maximum all_baselines_restored
```

The three vectors contain nine `u64` values. Baseline is the first worker
pre-record vector and every later worker reproduces it. Final is the latest
durable epoch/record post-GC vector; maximum is the elementwise high water.
`all_baselines_restored` requires the k1+k2 epoch and every later record to
restore baseline. K1's internal retained vector is evaluated only through the
epoch object and is not a false per-position failure.

The predecessor-publication fields are null only at boundary zero. Otherwise
method is `"measured"` with the exact publication duration of the immediate
predecessor marker, or `"fixed-upper-after-loss"` with accounting value
`60000000000`. The next boundary, interruption, or terminal clock always
closes the current marker's publication accounting. A measured value is never
replaced by the upper.

At a kernel boundary, `next_record_accounting_anchor_cumulative_ns` becomes
that boundary cutoff. At trace/measurement boundaries it is unchanged. The
first attempt's initial worker-ready and every post-interruption worker-ready
set it to their own cutoff; an ordinary later new-trace worker-ready carries
the preceding trace/measurement anchor unchanged. A supervisor-only cleanup
continuation publishes its originating kernel boundary first and does not
invent a new numerical anchor.

### 16.2 Cleanup-intent receipt and idempotent suffix

The registered path is:

```text
R/cleanups/cleanup-<10-digit u32>/receipt.json
```

plus its marker; indices are contiguous. The receipt has exactly:

```text
schema_version receipt_kind attempt_sha256 cleanup_index trace_index
panel_index kernel_position kernel_id kernel_variant
predecessor_boundary_sha256 worker_claim_sha256 boot_identity_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
record_prefix resume_state_sha256 deletion_plan next_watchdog_arm
intent_cutoff_cumulative_active_ns intent_cutoff_wall_time_ns
intent_cutoff_perf_counter_ns chunk_work_elapsed_ns
publication_upper_ns chunk_upper_ns
rss_sample_count_to_cutoff rss_maximum_sample_gap_ns_to_cutoff
rss_sampled_tree_peak_to_cutoff_bytes
rss_supervisor_rusage_highwater_to_cutoff_bytes
rss_worker_waits_to_cutoff
rss_preterminal_git_rusage_highwater_to_cutoff_bytes
rss_rusage_highwater_envelope_to_cutoff_bytes
rss_observed_to_cutoff_bytes rss_admission_upper_bytes
rss_observation_complete_to_cutoff
created_roots_high_water_observed_bytes created_roots_at_cutoff_bytes
created_roots_resume_upper_bytes checkpoint_tree_high_water_bytes
checkpoint_tree_admission_upper_bytes disk_observation_complete_to_cutoff
absolute_workspace_resume_upper_bytes filesystem registries
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
complete
```

`schema_version=1`, `receipt_kind="resource-cleanup-intent-v1"`, and
`complete=true`. It is permitted exactly for a positive-unit record at
position `9`, `12`, `13`, or `14`. `predecessor_boundary_sha256` is the latest
logical boundary and identifies the immediate predecessor durable
checkpoint/work marker.
`publication_upper_ns=60000000000`,
`chunk_upper_ns=chunk_work_elapsed_ns+publication_upper_ns`, and the same
480/60/540-second checks apply. The RSS/disk/registry fields use the boundary
formulas through the intent cutoff; the post-intent boundary carries them
forward.
`next_watchdog_arm` is the exact Section 11 object derived before encoding
this intent. It becomes active only after the complete intent is durable and
governs every later worker-work byte until the following boundary replaces it.
It may not be recomputed after cleanup, copied from a later clock, or extended
because deletion or fsync consumed part of its interval.

`record_prefix` has exactly:

```text
kernel_position kernel_id variant units worker_claim_sha256
boot_identity_sha256 successful_started_perf_counter_ns
successful_ended_perf_counter_ns successful_work_ns
accounting_started_cumulative_ns clock_resolution_ns
replay_count replay_penalty_ns prelude_ns kernel_ns
precleanup_epilogue_ns substage_prefix_ns artifact_sha256s
artifact_inventory_rows terminal_close_probe_evidence_sha256
rng_call_count rng_call_upper_count rng_address_inventory_sha256
rng_address_upper_inventory_sha256 finite converged
```

`substage_prefix_ns` is the first four Section 13 values. Every field is
already knowable and immutable before deletion. The later kernel record
reproduces it byte-for-byte and adds its accounting end/duration,
duration/admission enclosures, full epilogue and fifth substage,
`cleanup_intent_sha256`, and cleanup-completion boot identity.

`resume_state_sha256` hashes the Section 13 state with every target whose last
consumer just completed in `"retained-present"` state. `deletion_plan` has
exactly:

```text
schema_version target_count target_rows entry_count entry_rows plan_sha256
```

`schema_version=2`, `target_count=len(target_rows)`, and
`entry_count=len(entry_rows)`.

Each target row is:

```text
[target_index, root_kind, target_relative_path, object_kind, action,
 target_evidence_sha256_or_null, first_entry_index, entry_count]
```

`root_kind` is `"checkpoint"` or `"scratch"`. `action` is
`"delete-committed-final"` here. `object_kind` is the exact artifact kind or
`"resource-terminal-close-probe-v1"`. Artifact targets bind their artifact
SHA256; the probe binds the Section 10 receipt-final digest. Target rows are in
descending repository-relative UTF-8 path order and target indices are
contiguous from zero.

Each entry row is:

```text
[entry_index, target_index, repository_relative_path, entry_type, mode,
 evidence_logical_bytes_or_null, evidence_allocated_bytes_or_null,
content_sha256_or_null, validation_sha256]
```

Target membership is algorithmic. Target paths are unique. An entry matches a
target exactly when its repository-relative path equals the target path or has
that path plus `/` as a component-boundary prefix. Assign each enumerated entry
to the matching target with greatest component depth. In a terminal plan, one
exact checkpoint-root or scratch-root target is emitted iff that configured
root currently exists as an admitted directory; those are the only fallbacks,
so every still-unassigned ancestor or ordinary tree entry is assigned to its
matching present root. An absent configured root emits no target or entry. An
ordinary cleanup plan enumerates only the frozen target subtrees. Equal-depth
multiple matches, an unmatched entry row, or a target with no entry is
invalid.
For target `i`, `first_entry_index` is zero for the first target and otherwise
the prior target's first index plus count; `entry_count` is positive; and the
corresponding global slice contains only rows whose `target_index=i`.
Consequently target slices are positive, contiguous, exhaustive, and
nonoverlapping, including shared ancestor directories.

Define the exact target-slice digest:

```text
target_entry_slice_sha256 =
SHA256(CJSON([
  "xid-g2-resource-deletion-target-entry-slice-v1",
  target_index,
  root_kind,
  target_relative_path,
  entry_rows[first_entry_index:first_entry_index+entry_count],
]))
```

`target_evidence_sha256_or_null` is exhaustive despite its inherited field
name; every admitted A025 target has a nonnull value:

| Action | Object/path state | Exact target evidence |
| --- | --- | --- |
| `delete-committed-final` | complete artifact final | artifact SHA256 |
| `delete-committed-final` | complete terminal-close-probe receipt final | Section 10 receipt-final SHA256 |
| `delete-hidden-artifact-stage` | unique admitted hidden artifact stage | `target_entry_slice_sha256` |
| `delete-uncommitted-artifact-final` | valid complete uncommitted artifact final | artifact SHA256 |
| `delete-uncommitted-receipt-publication` | valid payload-only or payload-plus-marker hidden terminal-close-probe receipt stage | `target_entry_slice_sha256` |
| `delete-uncommitted-receipt-publication` | valid complete visible uncommitted terminal-close-probe receipt final | Section 10 receipt-final SHA256 |
| `delete-terminal-root` | currently present exact configured `checkpoint-root` or `scratch-root` fallback | `target_entry_slice_sha256` |

The path grammar distinguishes hidden stage from visible final. A partial
artifact final, marker-only receipt, invalid bytes, unknown stage family, null
target evidence, or any action/object/path-state combination absent from this
table is invalid before deletion. No target digest can be substituted for
another target class. Ordinary result-root receipt stages/finals never enter a
deletion plan: they obey Section 10's separate adoption or fail-closed
transition.

Within a target, greater depth comes first and equal depth is descending UTF-8
path order; global `entry_index` is the resulting contiguous order.
`entry_type` is `"regular-file"` or `"directory"`. Regular files bind exact
six-digit mode, logical/allocated bytes, and content SHA256. Directories bind
only path/type/mode and have null byte/hash fields, so a prior child unlink
cannot invalidate a surviving parent row. Stable validation hashes are:

```text
regular file:
SHA256(CJSON([
  "xid-g2-resource-deletion-entry-regular-v1",
  repository_relative_path, mode, evidence_logical_bytes,
  evidence_allocated_bytes, content_sha256,
]))

directory:
SHA256(CJSON([
  "xid-g2-resource-deletion-entry-directory-v1",
  repository_relative_path, mode,
]))
```

and:

```text
plan_sha256 =
SHA256(CJSON([
  "xid-g2-resource-deletion-plan-v1",
  target_rows,
  entry_rows,
]))
```

Before every mutation that could create a file or directory below the
checkpoint or scratch root, the supervisor computes the exact no-follow
post-mutation inventory and its prospective terminal deletion plan, including
the maximum simultaneous atomic-stage/final state. The mutation is forbidden
unless that plan has at most `maximum_terminal_cleanup_rows=512` entries,
every target/slice/path/row byte bound passes, and every currently present root
remains fully representable. Hitting a bound selects terminal failure from the
still representable pre-mutation state. Worker logs, temporary trees, bytecode
caches, receipt/artifact stages, owner directories, and root directories have
no exemption; ungoverned writers and implicit cache creation are disabled.

Exact target order is:

```text
k8:
  resume/focals/oracle
  resume/focals/observable
  resume/focals/homogeneous
  resume/cell-panel
  resume/bootstrap-weights
  resume/base-panel
  null-batch
  inherited cell-panel
  inherited base-panel

k13-recovery:
  resume/paper-bootstrap-weights  [validation only]
  paper/recovery-date
  paper/cache/recovery
  paper/bootstrap/recovery

k13-research:
  resume/paper-bootstrap-weights  [equal and research only]
  paper/full-date
  paper/cache/research
  paper/bootstrap/research

k14:
  scratch terminal-close-probe
  checkpoint publication/envelope
```

Therefore target counts are exactly nine for k8; three for equal
k13-recovery, four for validation k13-recovery; four for equal/research
k13-research; and two for k14. Zero-unit k13 variants have no intent.

Before the marker is complete, no target deletion is authorized. If the
intent is absent, uniquely implied hidden stages and valid-but-uncommitted
artifact finals are inventoried and removed, then the record/epoch is replayed
with its penalty. Once the marker is complete, numerical work and RNG evidence
are irrevocable. The filesystem may contain only an exact absent entry prefix
and byte-valid remaining suffix of `entry_rows`, with no extra path. Before
recording an entry as absent, fsync every distinct nearest existing ancestor,
deepest first and then descending UTF-8. Progress has exactly:

```text
deletion_plan_sha256 completed_entry_prefix_count remaining_entry_sha256
```

`deletion_plan_sha256=deletion_plan.plan_sha256`, and
`completed_entry_prefix_count` is the unique current absent-prefix length.

where:

```text
remaining_entry_sha256 =
SHA256(CJSON([
  "xid-g2-resource-deletion-remaining-v1",
  deletion_plan.plan_sha256,
  deletion_plan.entry_rows[completed_entry_prefix_count:],
]))
```

The supervisor removes the next suffix entries in order, fsyncs as specified,
then publishes the record boundary with full completion. A missing non-prefix
member, hash mismatch, extra target/stage, changed order, or reconstruction
attempt is terminal. A chained interruption retains identical target/entry
rows and plan digest but advances the prefix count and remaining digest from
the actual filesystem; it never copies stale progress.

Loss after the intent performs no numerical replay and no RNG construction.
The final record retains the original successful worker/boot and sets
`cleanup_completion_boot_identity_sha256` to the boot that completed deletion.
Its fifth substage and full duration include intent publication, deletion,
fsync, interruption charge, and final cleanup suffix exactly once.
After an interruption marker, the resumed deletion/boundary suffix has its own
480-second work watchdog and 60-second boundary-publication upper; its
checkpoint interval must therefore also be at most 540 seconds. A timeout is
terminal and cannot reopen the numerical record.

### 16.3 Interruption evidence, debris, and replay transition

A nonterminal attempt resumes only after every prior PID/start identity is
absent and one of: a latched clean signal at a boundary; a changed boot whose
old segment already has a durable clean-exit interruption; or exact same-boot
dead-worker proof under one continuously observing live supervisor. Direct
boot/supervisor loss instead selects the telemetry-gap failure. The path:

```text
R/interruptions/interruption-<10-digit i>/receipt.json
```

has exactly:

```text
schema_version receipt_kind attempt_sha256 interruption_index
predecessor_worker_claim_sha256 boundary_sha256 cleanup_intent_sha256
last_durable_marker_kind last_durable_marker_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
reason signal_number old_boot_identity_sha256 new_boot_identity_sha256
last_complete_trace_index next_panel_index next_trace_index
resume_position replay recovery_action pending_receipt_completion
receipt_stage_normalization cleanup_progress debris process_deaths
thermal_recovery next_watchdog_arm
cumulative_active_ns worker_waits rss_supervisor_rusage_highwater_bytes
preterminal_git_rusage_highwater_bytes
rss_rusage_highwater_envelope_bytes rss_admission_upper_bytes
checkpoint_tree_admission_upper_bytes created_roots_resume_upper_bytes
absolute_workspace_resume_upper_bytes filesystem
rss_observation_complete_to_cutoff disk_observation_complete_to_cutoff
predecessor_segment_close_method
last_durable_wall_time_ns last_durable_perf_counter_ns
last_durable_marker_publication_accounting_ns
last_durable_marker_publication_method
resume_wall_time_ns resume_perf_counter_ns charged_gap_ns excluded_poweroff_ns
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 resource_config_sha256
complete
```

`receipt_kind="resource-interruption-receipt-v1"`, `complete=true`, and indices
are contiguous. `publisher_supervisor_pid` and
`publisher_supervisor_start_identity` identify the process publishing this
receipt and are validated again before its marker. Reason is
`"supervisor-signal"`, `"boot-changed"`, `"worker-lost"`, or
`"supervisor-lost"`; `signal_number` is `1`, `2`, or `15` only for the first.
`predecessor_segment_close_method` is exactly `"same-live-supervisor"`,
`"durable-clean-exit"`, or `"unknown-loss"`. The first requires the current
live supervisor to have continuously sampled, reaped every worker, collected
rusage, appended each row to the cumulative Section 4.6 `worker_waits`
object, and completed the final disk scan. Its
`preterminal_git_rusage_highwater_bytes` equals the bootstrap-check maximum and
its supervisor/rusage fields use the boundary formula over that exact
inventory. The second is available across a
boot change only when an already durable predecessor interruption closed the
old segment with those same facts. Abrupt supervisor loss or direct boot loss
is `"unknown-loss"`; it sets both observation-complete Booleans false, assigns
the four limit-plus-one uppers, and requires
`recovery_action="select-terminal-failure-telemetry-gap"`.
Every interruption, including unknown loss, preserves the nonzero bootstrap
Git scalar derived from immutable `attempt.json`; no resume may replace it with
zero or omit it.
`predecessor_worker_claim_sha256` identifies the latest valid worker claim.
`boundary_sha256` hashes the latest boundary. `cleanup_intent_sha256` is
nonnull only when that boundary is followed by a complete cleanup intent.
`last_durable_marker_kind` is `"boundary"`, `"cleanup-intent"`, or
`"interruption"` and the digest/times/cumulative fields equal that exact
checkpoint/work marker.
`next_watchdog_arm` is null exactly when
`recovery_action="select-terminal-failure-telemetry-gap"` or no later worker
work remains. Otherwise it is a freshly derived Section 11 arm, durable before
any successor worker work, and the next worker claim/wait/death evidence must
join its exact digest and deadlines unless a later arm-bearing boundary or
cleanup intent supersedes it before work begins.

An interruption predecessor is permitted only when its recovery action has not
yet reached a later worker-ready or cleanup-completion boundary. The new receipt
copies that predecessor's boundary, cleanup intent, resume position, replay,
recovery action, pending receipt completion, immutable debris plan, referenced
cleanup-plan identity, and thermal trigger byte-for-byte. It advances only the
applicable debris or committed-cleanup prefix from current filesystem bytes
and changes the contiguous interruption index, last-marker chain,
receipt-stage normalization, newly proved process deaths, publisher/boot/times,
charged gap, closed-segment telemetry uppers, and the resulting cumulative
active clock. No second replay ordinal is created because no new worker-ready
boundary released another execution.

The last-marker publication method is `"measured"` or
`"fixed-upper-after-loss"` under the 60-second rule. Resume wall/perf samples
are consecutive and precede interruption publication. `filesystem` must
retain the attempt device/allocation-unit identity.

`resume_position` is null without a partial trace; otherwise it has exactly:

```text
active_measurement_block trace_index panel_index next_kernel_position
```

`replay` is null for cleanup-intent continuation. For a supervisor-signal
continuation from a boundary, it copies the latest
`trace_progress.pending_replay` unchanged; a clean signal adds zero but cannot
erase a carried loss count. For an abrupt loss after a worker-ready boundary,
it is the exact Section 16.1 pending-replay object for the in-flight ordinary
position or `[0,1]` epoch, with one added to any carried count. For an
interruption predecessor it is copied unchanged as specified above. After
worker-ready, there is no post hoc “not started” exception.

`recovery_action` is exactly `"continue-prefix"`, `"replay-record"`,
`"replay-first-operand-epoch"`, `"complete-cleanup-suffix"`,
`"complete-receipt-boundary"`, `"reconstruct-receipt-and-boundary"`, or
`"select-terminal-failure-telemetry-gap"`. Cleanup suffix requires nonnull
`cleanup_intent_sha256`, null replay, and supervisor-only cleanup before any new
RNG capability.

`cleanup_progress` is null unless
`recovery_action="complete-cleanup-suffix"`. In that branch it has exactly:

```text
deletion_plan_sha256 completed_entry_prefix_count remaining_entry_sha256
```

`deletion_plan_sha256` equals the referenced cleanup intent's
`deletion_plan.plan_sha256`. The prefix count is the unique current absent
prefix of that frozen plan, and `remaining_entry_sha256` is the Section 16.2
digest over its exact remaining suffix. A chained cleanup interruption retains
the same intent and plan digest and advances only that filesystem-derived
prefix/digest. In every other recovery action `cleanup_progress` is null.

`pending_receipt_completion` is null except when an exact already-marked trace
or measurement receipt exists after the latest boundary, or its bytes are
uniquely reconstructible from the complete durable prefix, and its required
following boundary is absent. Otherwise it has exactly:

```text
receipt_kind receipt_sha256 marker_sha256 required_boundary_kind origin
prerequisite_inventory_sha256
```

The kinds are `"resource-trace-receipt-v1"`/`"trace"` or
`"resource-measurement-block-v1"`/`"measurement-block"`. All bytes and
the complete durable prefix must revalidate. `origin` is `"visible-final"`,
`"adopted-stage"`, or `"reconstructed-from-prefix"`; the prerequisite digest
binds the exact prefix used. The first two require
`recovery_action="complete-receipt-boundary"`; the last requires
`"reconstruct-receipt-and-boundary"`. All require null cleanup intent, null
cleanup progress, null replay, and empty debris. Recovery publishes/reuses only
the exact receipt and its uniquely derived following boundary before any new
reservation, worker, capability, or RNG.

`receipt_stage_normalization` is null or has exactly:

```text
final_relative_receipt_path hidden_stage_relative_path receipt_kind
payload_name prior_stage_state payload_sha256 marker_sha256
receipt_final_sha256
```

`payload_name` is `"claim.json"` or `"receipt.json"` and
`prior_stage_state` is `"payload-only"` or `"payload-and-marker"`. It records
the one exact Section 10 stage normalized before this interruption. The
process-death set proves its encoded publisher dead. If the normalized leaf is
the immediately preceding interruption, this receipt is the mandatory chained
interruption that binds that death before any work. No receipt may bind more
than one normalized stage.

`thermal_recovery` has exactly `required,start_after_trace_index`. Every
admitted interruption sets `required=true` iff a later warm measurement trace
remains. A partial trace is completed first and does not count toward the new
thermal epoch; otherwise recovery starts immediately after the last complete
trace. `start_after_trace_index` identifies that trace, or is null before any
trace.

`debris` has exactly:

```text
schema_version target_count target_rows entry_count entry_rows plan_sha256
completed_entry_prefix_count remaining_entry_sha256
```

`schema_version=2`. Target and entry rows use Section 16.2's exact common
deletion-plan grammar. Here `action` is exactly
`"delete-hidden-artifact-stage"`,
`"delete-uncommitted-artifact-final"`, or
`"delete-uncommitted-receipt-publication"`; object kind is the exact artifact
kind or `"resource-terminal-close-probe-v1"`. Evidence follows Section 16.2's
exhaustive table without exception: a hidden stage binds its target-entry-slice
digest, an uncommitted artifact final binds its artifact SHA256, and a valid
visible probe final binds its Section 10 receipt-final digest. Null target
evidence is invalid.
Receipt-stage normalization is the separate Section 10 transition and never
appears as generic debris.

The canonical empty debris object has
`target_count=entry_count=completed_entry_prefix_count=0`,
`target_rows=entry_rows=[]`,
`plan_sha256=SHA256(CJSON([
"xid-g2-resource-deletion-plan-v1",[],[]]))`, and
`remaining_entry_sha256=SHA256(CJSON([
"xid-g2-resource-deletion-remaining-v1",plan_sha256,[]]))`. It is mandatory
whenever no pre-intent uncommitted artifact/probe debris exists, including
`recovery_action="complete-cleanup-suffix"`; committed cleanup progress appears
only in `cleanup_progress`.

The exact maximum target families are: two for the first-operand epoch
(resume base and cell); one for each of k3--k6 and k8--k12; three for either
k13 variant (paper weights, cache, and bootstrap batch); and two for k14
(publication envelope and terminal-close probe). A zero-unit position permits
zero. Target rows are descending by path and entry rows are child-before-parent
under Section 16.2. An extra path, duplicate, or state outside that position's
frozen family is terminal.

Progress is:

```text
remaining_entry_sha256 =
SHA256(CJSON([
  "xid-g2-resource-deletion-remaining-v1",
  plan_sha256,
  entry_rows[completed_entry_prefix_count:],
]))
```

The current filesystem must equal one exact absent prefix plus a valid suffix.
Every delete removes only the next entry, fsyncs the required nearest existing
ancestors, and advances the prefix monotonically. Chained interruptions copy
the immutable plan bytes but derive the later prefix count and remaining
digest from current bytes. An artifact final is never reused to evade a
missing timing record.

For an atomic receipt final:

```text
valid_final_sha256 = SHA256(CJSON([
  "xid-g2-resource-receipt-final-v1",
  receipt_kind,
  receipt_sha256,
  marker_sha256,
]))
```

`process_deaths` has exactly:

```text
schema_version rows sha256
```

`schema_version=1`. Rows are ordered by role `"supervisor"` before `"worker"`
and then by ascending PID/start identity; each newly superseded process appears
exactly once:

```text
[role, pid, process_start_identity, old_boot_identity_sha256, method,
 first_check_perf_counter_ns, second_check_perf_counter_ns,
 wait_status, ru_maxrss_bytes, watchdog_arm_kind, watchdog_arm_sha256,
 work_deadline_perf_counter_ns, reap_deadline_perf_counter_ns,
 absence_observations]
```

The deduplicated union of these rows across every interruption, the terminal
failure intent, and every failure-resume receipt in one attempt has at most
`maximum_process_death_rows=128` rows. A later receipt contains only identities
absent from every earlier durable process-death set; duplicate identity/method
rows and a 129th distinct identity are forbidden before publication.

Method is exactly `"wait4-reaped"`,
`"double-process-identity-absence"`, or `"boot-identity-changed"`. Nullable
fields are JSON null under this byte-authoritative table:

| Method | Role | First check | Second check | Wait/status/rusage | Arm/deadlines | Absence observations |
| --- | --- | --- | --- | --- | --- | --- |
| `wait4-reaped` | worker only | nonnull, immediately post-`wait4` | null | exact signed status and nonnull byte-normalized `ru_maxrss` | exact nonnull persisted arm kind/digest/work/reap values | null |
| `double-process-identity-absence` | supervisor or worker | nonnull | nonnull | both null | all four null | exact compact two-sample factorization |
| `boot-identity-changed` | supervisor or worker | null | null | both null | all four null | null |

Every row joins `(role,pid,process_start_identity)` to the unique authoritative
attempt, worker birth, worker claim, interruption, failure-intent, or
failure-resume record that last encoded that process identity, and
`old_boot_identity_sha256` equals that record's boot digest. Define the
enclosing current boot as an interruption's `new_boot_identity_sha256` or a
failure-intent/resume's `boot_identity_sha256`. For `wait4-reaped` and
`double-process-identity-absence`, old boot equals current boot. For
`boot-identity-changed`, old boot differs from current boot. No caller-supplied
or merely well-formed boot digest can satisfy this join.

For `wait4-reaped`, `wait4` returns the exact PID, timeout termination was
requested not later than the persisted work deadline when applicable, the
post-wait sample is not later than the persisted reap deadline, and
`ru_maxrss_bytes` is the exact Section 4.6 byte-normalized value. For a claimed
worker, the arm kind/digest and both deadlines equal the authoritative arm
selected by the worker-wait row, and that row must equal the matching
`worker_waits` row projection. For the exact fourteen-field worker-wait row
`W`, the death row is literally:

```text
["worker", W[2], W[3], W[4], "wait4-reaped",
 W[5], null, W[6], W[7], W[8], W[9], W[10], W[11], null]
```

No alternate field order, copied timestamp, or recomputed deadline is valid. A
clean zero exit uses the same method and is distinguished by its raw status.
The sole exception is a complete visible worker birth whose worker claim was
never published. Its exact `wait4-reaped` death row joins the birth identity,
uses the launch intent's persisted arm kind/digest/deadlines, and carries the
actual post-wait/status/rusage fields in the same positions, but it has no
invented cumulative worker-wait row or worker-claim digest. This exception can
close only terminal failure; `all_wait_statuses_collected` remains false
because no claimed-worker wait inventory row exists. A birth-only child not
closed by this exact row or another admissible death method blocks failure
publication.
For double absence, `absence_observations` is the compact, lossless
factorization:

```text
[verdict, observed_pid_or_null, observed_start_identity_or_null,
 [[first_perf_counter_ns, first_return_bytes, first_errno_value],
  [second_perf_counter_ns, second_return_bytes, second_errno_value]]]
```

The verdict and optional decoded replacement identity are common to both raw
samples. This factorization is required because duplicating the 64-hex
replacement identity in two observation rows can exceed the frozen
`maximum_process_death_row_bytes=512` cap. Expanding the common values into
either sample reconstructs the two raw syscall observations exactly; no
information used by the truth table is omitted.

Before each `proc_pidinfo(pid,PROC_PIDTBSDINFO,0,...)` call the complete
`proc_bsdinfo` buffer is zeroed and `errno=0`. Its executable truth table is:

| Return and errno | Valid decoded identity | Verdict | Effect |
| --- | --- | --- | --- |
| exact `sizeof(proc_bsdinfo)`, zero | expected PID/start | `"present-target"` | reject death proof |
| exact size, zero | same PID, different valid start | `"absent-pid-reused"` | admissible absence class |
| zero, `ESRCH` | both identity fields null and buffer still zero | `"absent-esrch"` | admissible absence class |
| zero with any other errno, including zero, `EPERM`, or `EACCES` | any | `"query-error"` | terminal |
| short positive, oversize, negative, malformed struct, or PID mismatch | any | `"query-error"` | terminal |

Both checks use the current unchanged boot and satisfy
`first+50000000 <= second <= first+1000000000`. Both verdicts must be the same
admissible absence class. Two reused-PID observations must name the same
replacement PID/start identity; mixed ESRCH/reuse, a changing replacement, a
present target, permission failure, ABI/short-read failure, or ambiguous
zero/zero return cannot prove death. `first_check_perf_counter_ns` and
`second_check_perf_counter_ns` equal the two observation timestamps exactly.
For `"absent-esrch"`, both common identity fields are null, both return values
are zero, and both errno values are `ESRCH`. For
`"absent-pid-reused"`, the common PID equals the queried PID, the common
start identity is a valid 64-hex digest different from the expected start
identity, both return values equal `sizeof(proc_bsdinfo)`, and both errno
values are zero. The deterministic maximum-width row fixture exercises this
factorized reused-PID form, the maximum-width `wait4` form, and the changed-
boot form independently and requires every exact CJSON row including terminal
LF to remain at most `512` bytes; the duplicated-identity two-row form is a
required rejection fixture.
For boot change,
the joined old boot differs from the enclosing current boot as above. The first transition
binds each superseded worker and, when different from the publisher, its
supervisor from the worker claim. A chained transition binds the prior
interruption's publisher supervisor; it does not duplicate already durable
death rows. The digest is:

```text
SHA256(CJSON([
  "xid-g2-resource-process-death-set-v1",
  rows,
]))
```

Every prior process identity not equal to the current publisher must be either
newly proved in these rows or already proved by the exact predecessor
interruption chain. PID reuse grants no authority.

On the same boot:

```text
charged_gap_ns =
    resume_perf_counter_ns - last_durable_perf_counter_ns
```

Across boots:

```text
charged_gap_ns =
    resume_wall_time_ns - last_durable_wall_time_ns
```

The difference is nonnegative,
`cumulative_active_ns=last_durable_cumulative_ns+charged_gap_ns`, and
`excluded_poweroff_ns=0`. This charges publication, shutdown, downtime, and
resume setup. RSS/disk conservative uppers equal or exceed the latest durable
marker values and are never called observed.

On ordinary replay, validate the full durable prefix, publish/reuse the
interruption receipt, perform only its debris action, create the next
contiguous worker claim, publish worker-ready, release the capability, and
continue the same reservation/address schedule with the pending replay object.
On cleanup continuation, validate the intent, publish/reuse the interruption
receipt, finish only its deletion suffix, publish the originating record
boundary, and only then create a new worker if more numerical work remains. On
receipt-boundary completion, publish/reuse the interruption receipt, revalidate
the frozen receipt/marker, publish only its required following boundary, and
then resume the canonical scheduler. If another supervisor is lost before any
of those transitions reaches its next boundary, publish the chained
interruption receipt above and continue the same frozen action.

After every admitted interruption, including one exactly at a trace or
measurement boundary, all prior thermal qualification expires. A suspended
trace first completes but contributes zero to the reset epoch. If a later warm
measurement trace remains, consume new contiguous panels with
`role="recovery-thermal-phase"` in complete
`validation,research,research,validation` cycles until the sum of successful
trace durations through a cycle end is at least `600000000000` ns. Those
traces enter lifecycle time, RSS, disk, and receipt inventories but never
measurement pairs, the 200-second block minimum, stationarity, temporal
checks, or projection contexts. A second interruption discards only recovery
qualification accumulated since the prior interruption after its suspended
trace completes. No thermal work is required when no later warm trace exists.
Completed cold traces, partial-block traces, and measurement blocks remain in
admission. `next_panel_index` is always the next unclaimed panel;
`next_trace_index` equals the partial trace when present and otherwise one
plus the complete maximum.

### 16.4 Unique cumulative clock

At initial bootstrap:

```text
active_anchor_cumulative_ns = 0
active_anchor_perf_counter_ns = attempt.time_origin.perf_counter_ns
```

After interruption publication:

```text
active_anchor_cumulative_ns = interruption.cumulative_active_ns
active_anchor_perf_counter_ns = interruption.resume_perf_counter_ns
```

For every later cutoff on that boot:

```text
cumulative_active_ns =
    active_anchor_cumulative_ns
    + current_perf_counter_ns
    - active_anchor_perf_counter_ns
```

No timer resets without carrying the interruption value. Supervisor setup,
source checks, fixture work, fsync, cleanup, receipt publication, same-boot
gaps, and cross-boot gaps through the accounting cutoff are active work. No
calendar interval is subtracted as powered-off time. Terminal outcome
publication receives the fixed 60-second accounting charge because a receipt
cannot observe the suffix after its own encoding; that charge is a
preregistered projection convention, not an observed or kernel-enforced
marker/final-seal/rename/parent-fsync latency bound. A sampler gap,
stationarity/rate failure, budget breach, numerical/provenance failure, or
ordinary exception is terminal and cannot be relabeled interruption.

## 17. Terminal result and failure schemas

`R/terminal/success/result.json` has exactly:

```text
schema_version status attempt_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
panel_source_snapshot_sha256
executable_source_snapshot_sha256 authority_source_snapshot_sha256
runtime_sha256 resource_config_sha256 receipt_inventories artifact_inventory
preterminal_git_checks rng clock thermal_recovery stationarity rate_robustness projections
rss disk registries acceptance
strongest_residual
```

Fixed values are `schema_version=1` and `status="passed"`.
`preterminal_git_checks` is Section 4.3's exact two-check terminal object. Its
terminal-pre-JSON check is complete before the `clock` and `rss` cutoff values
are encoded; any child/output/wait/rusage or bootstrap crosslink failure
prevents success JSON publication.

`receipt_inventories` has exactly:

```text
reservations worker_launches worker_births workers boundaries interruptions
cleanups traces measurements
```

Each value has exactly `count` and `sha256`, using Section 10's inventory
formula.

`artifact_inventory` has exactly:

```text
count sha256 kind_counts all_final_artifacts_deleted
```

Its digest is:

```text
SHA256(CJSON([
  "xid-g2-resource-artifact-inventory-v1",
  [[relative_artifact_path, artifact_kind, artifact_sha256], ...],
]))
```

The rows are the UTF-8-path-sorted concatenation of every validated trace
receipt's `artifact_inventory_rows`. Paths are globally unique; a duplicate,
gap, row/hash mismatch, artifact hash absent from its trace kernel records, or
terminal count/digest mismatch is terminal. This durable per-trace row
authority makes the terminal inventory independently reproducible even after
receipt-bound fixture deletion.

`kind_counts` has exactly the thirteen Section 10.1 names: the inherited
`base-panel`/`cell-panel` plus all eleven resource kinds. Registered values are
nonnegative `u64` counts derived from trace rows; the fixed rehearsal totals
are not copied into this variable-length run.

`all_final_artifacts_deleted` is exact `true`. At terminal cutoff every
artifact leaf represented by those durable rows is absent from `C`; the rows
are audit commitments, not claims that deleted payload bytes remain
independently re-readable. Any remaining final artifact, hidden stage, owner
marker, or unaccounted checkpoint/scratch entry prevents success.

`rng` has exactly:

```text
seed streams address_count address_inventory_sha256
address_upper_count address_upper_inventory_sha256
replay_count replay_penalty_ns
validation_address_count research_address_count
```

Order complete trace receipts by `trace_index`. Define:

```text
address_count =
    sum(trace.rng_call_count for trace in traces)

address_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-address-inventory-v1",
  [[trace_index, trace.rng_call_count,
    trace.rng_address_inventory_sha256], ...],
]))

address_upper_count =
    sum(trace.rng_call_upper_count for trace in traces)

address_upper_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-terminal-address-upper-inventory-v1",
  [[trace_index, trace.rng_call_upper_count,
    trace.rng_address_upper_inventory_sha256], ...],
]))
```

Terminal `replay_count` is an admission record-charge sum: it is the sum of all
kernel-record `replay_count` values in that same trace/kernel order, and
`replay_penalty_ns=480000000000*replay_count`. One physical lost k1+k2 epoch
therefore contributes two record charges while its single physical loss ordinal
and event remain derivable from the interruption receipts. The field is not a
physical loss-event count. These terminal digests are inventories of durable
per-trace digests, not a second ambiguous concatenation of physical address
rows. `seed=2026071529`,
`streams=["resource_smooth","resource_paper"]`, and validation/research counts
are both zero. No terminal draw-count field exists because scalar draw sizes
are not persisted by trace receipts and are unnecessary for admission.

`clock` has exactly:

```text
name resolution_ns cutoff_boot_identity_sha256 cutoff_perf_counter_ns
cutoff_wall_time_ns calendar_to_cutoff_ns excluded_poweroff_ns
cumulative_active_to_cutoff_ns terminal_close_method
terminal_close_accounting_charge_ns
terminal_predecessor_marker_kind terminal_predecessor_marker_sha256
terminal_chunk_work_elapsed_ns terminal_publication_accounting_charge_ns
terminal_accounted_interval_ns
resource_accounted_charge_ns resource_expected_ns resource_hard_ns
attempt_bootstrap_elapsed_ns
maximum_chunk_work_elapsed_ns
maximum_publication_accounting_ns maximum_accounted_interval_ns
durable_marker_publication_upper_ns durable_marker_interval_upper_ns
all_checkpoint_intervals_passed terminal_accounting_row_passed
```

`excluded_poweroff_ns` is exactly zero. The cutoff samples are taken after all
preterminal validation, cleanup, waits, resource sampling, and disk scans but
immediately before terminal JSON encoding. `calendar_to_cutoff_ns` is the
nonnegative difference between the cutoff and attempt wall-time samples;
`cumulative_active_to_cutoff_ns` is the same-boot monotonic accumulation plus
every conservatively charged cross-boot wall gap through that cutoff.
`terminal_predecessor_marker_kind` and its digest identify the exact last
durable boundary. `terminal_chunk_work_elapsed_ns` spans that marker through
the pre-JSON cutoff and is at most `480000000000`.
`terminal_publication_accounting_charge_ns=
terminal_close_accounting_charge_ns=60000000000`,
`terminal_accounted_interval_ns=terminal_chunk_work_elapsed_ns+
terminal_publication_accounting_charge_ns`,
`terminal_accounted_interval_ns<=540000000000`, and
`terminal_close_method="fixed-terminal-accounting-charge-v1"`. Therefore
`resource_accounted_charge_ns = cumulative_active_to_cutoff_ns +
terminal_close_accounting_charge_ns`. The charge is a projection convention;
no value claims to observe or upper-bound marker encoding, final seal,
directory rename, or parent-fsync latency.

The three maximum fields join every ordinary-work boundary and cleanup-intent
interval with its forward-reported exact publication duration or, after a loss
before that duration became durable, the ordinary fixed 60-second accounting
upper, plus the separate terminal accounting row above. Interruption downtime
is charged to cumulative resource elapsed but is not mislabeled an ordinary
480-second work interval. The terminal JSON encoding closes the pre-JSON work
value. The maxima must be at most `480000000000`, `60000000000`, and
`540000000000`, respectively.
`durable_marker_publication_upper_ns=60000000000` and
`durable_marker_interval_upper_ns=540000000000`;
`attempt_bootstrap_elapsed_ns` repeats boundary zero and must be at most
`480000000000`. `all_checkpoint_intervals_passed` is the conjunction for the
ordinary nonterminal checkpoint intervals, including that initial lost-work
interval. `terminal_accounting_row_passed` separately requires the exact charge,
pre-JSON work cap, and accounted-sum cap; it is not an end-to-end close-time
verdict.

`thermal_recovery` has exactly `count,rows,sha256`. Rows are:

```text
[interruption_index, start_after_trace_index,
 first_recovery_trace_index, last_recovery_trace_index,
 successful_duration_ns]
```

ordered by interruption index and hashed under
`"xid-g2-resource-recovery-thermal-inventory-v1"`. A row exists exactly when
the interruption's `thermal_recovery.required` is true; its final duration is
at least `600000000000` and ends only at a complete four-phase cycle.

`stationarity` has exactly:

```text
check_count all_passed measurement_receipt_sha256s
```

`check_count=6`: overall, validation, and research for blocks 2 and 3.
`measurement_receipt_sha256s` has exactly three elements, the exact
measurement receipt hashes for blocks `1`, `2`, and `3` in that order. Those
three receipts uniquely derive all six comparisons; no check-level or
duplicated hash is permitted. `rate_robustness` is the exact object in
Section 15.

`projections` has exactly:

```text
validation research combined tasks
```

Validation and research each have exactly:

```text
startup_ns block_projections raw_ns upper_ns
expected_limit_ns hard_limit_ns passed
```

`block_projections` is the ordered three-row array for measurement blocks
`1..3`. Every row has exactly `block_index`, `raw_ns`, and `upper_ns` and uses
`GATE_G2_RESOURCE_ADMISSION.md` Section 11's
cold-plus-paired-equal-plus-paired-phase formula. The final
`raw_ns` and `upper_ns` use the seven-context slowest formula and cannot be
replaced by a favorable block row. Both formulas use the common cross-variant
slower normalized kernel-13 rate for each phase, and every duration input is a
Section 13 replay-penalized admission duration. Variant-specific rates remain
separate only in task rows and diagnostics.

Combined has exactly:

```text
resource_accounted_charge_ns validation_upper_ns research_upper_ns total_ns
expected_limit_ns hard_limit_ns passed
```

Tasks has exactly:

```text
by_task maximum_observed_ns maximum_projected_ns limit_ns all_passed
```

`by_task` is an ordered ten-row array in
`GATE_G2_RESOURCE_ADMISSION.md` Section 10's task order. Every row
has exactly:

```text
task_name kernel_vector contexts observed_max_ns
observed_max_context projected_upper_ns passed
```

`contexts` contains every admissible context in fixed order `cold`,
`equal-1..3`, `validation-1..3`, `research-1..3`, omitting only a phase
context with a zero unit in a required task position. Each context row has
exactly:

```text
context_id observed_ns conservative_ns
```

For cold, `conservative_ns` is the 60%-rate
`task_cold_plus`; otherwise it is `task_plus`. Both use
`admission_duration_plus_ns`; `observed_ns` uses the successful raw durations
only.
`projected_upper_ns` is the 1.25-multiplied maximum conservative value. The
`kernel_vector` is the exact 15-position nonnegative-u64 vector in Section
10's kernel/variant order. `observed_max_context` is the first maximum in the
fixed context order above, so a tie has one byte representation. The two
public maxima are exact maxima over the ten rows, and every row must pass.

`rss` has exactly:

```text
sample_period_ns sample_count maximum_sample_gap_ns
sampled_tree_peak_bytes supervisor_rusage_highwater_bytes
worker_waits preterminal_git_rusage_highwater_bytes
rusage_highwater_envelope_bytes
observed_envelope_to_cutoff_bytes carried_durable_marker_upper_bytes
current_margin_upper_bytes rss_admission_upper_bytes
observation_complete_to_cutoff terminal_publication_accounting_method limit_bytes
all_wait_statuses_collected passed
```

`sample_period_ns=50000000`. `sample_count`,
`maximum_sample_gap_ns`, and both actual peaks equal the terminal accounting
cutoff's cumulative sampler values, whose latest durable prefix was carried by
the prior boundary or cleanup intent. There is no second cutoff/sample-count
field.
`worker_waits` is the final cumulative Section 4.6 object and has exactly one
row for every issued worker. `supervisor_rusage_highwater_bytes` is the
same-cutoff zeroed-`getrusage` sample.
`preterminal_git_rusage_highwater_bytes` is the maximum over all 24 child rows
in `preterminal_git_checks`, and:

```text
rusage_highwater_envelope_bytes =
    supervisor_rusage_highwater_bytes
    + max(
        max([row[7] for row in worker_waits.rows], default=0),
        preterminal_git_rusage_highwater_bytes
    )
```

The row index is the frozen `ru_maxrss_bytes` column. This equality, every row
join, complete issued-worker coverage, and all 24 preterminal Git waits are
required before success.
`observed_envelope_to_cutoff_bytes` is the maximum actual sampled/rusage
envelope recoverable from all complete epochs plus the current epoch through
the accounting cutoff. `carried_durable_marker_upper_bytes` is zero without a
work marker and otherwise the latest complete boundary or cleanup intent's
`rss_admission_upper_bytes`; it is conservative, not observed. Define:

```text
current_margin_upper_bytes =
    ceil_div(5 * observed_envelope_to_cutoff_bytes, 4)

rss_admission_upper_bytes =
    max(carried_durable_marker_upper_bytes, current_margin_upper_bytes)
```

`observation_complete_to_cutoff=true`; an unknown segment cannot produce
success. `terminal_publication_accounting_method` is the exact string
`"fixed-terminal-accounting-charge-v1"` and is not a cumulative-RSS
observation of the post-JSON suffix.
`passed` requires both the observed envelope and the admission upper to be at
most `limit_bytes=3,500,000,000`, positive sampling, every descendant wait
status, and `maximum_sample_gap_ns<=1000000000`. The carried upper is never
multiplied again. The terminal marker's separate
`terminal_guard.publication_rss` proves the current post-JSON publication
segment and Git children fit the close-safety threshold; it does not rewrite
this cumulative run-level object. The final in-process seal repeats the
publication predicate, while success validity still requires this cumulative
object to pass. Visible final-directory existence attests the final seal rather
than relabeling it as a pre-JSON observation.

`disk` has exactly:

```text
outside_baseline_bytes created_roots_high_water_observed_bytes
carried_durable_marker_created_roots_upper_bytes
created_roots_admission_upper_bytes
checkpoint_active_tree_high_water_bytes checkpoint_margin_upper_bytes
checkpoint_tree_admission_upper_bytes observation_complete_to_cutoff
absolute_workspace_high_water_observed_bytes
absolute_workspace_admission_upper_bytes
filesystem cutoff_created_roots_bytes cutoff_workspace_bytes
terminal_close_reserved_bytes terminal_created_roots_upper_bytes
terminal_workspace_upper_bytes
created_transient_limit_bytes checkpoint_limit_bytes
absolute_transient_limit_bytes steady_limit_bytes all_passed
```

Let `B` be `outside_baseline_bytes`, `H` be
`created_roots_high_water_observed_bytes`, `C` be zero without a work marker and
otherwise the latest boundary or cleanup intent's
`created_roots_resume_upper_bytes`, `F` be
`terminal_close_reserved_bytes`, and `R` be
`cutoff_created_roots_bytes`. `filesystem` is the current Section 18 snapshot;
its `maximum_allocation_unit_bytes` is `g` and all three root records must
equal the attempt's device/allocation-unit invariants. Exact derived fields are:

```text
carried_durable_marker_created_roots_upper_bytes = C
terminal_created_roots_upper_bytes = R + F
created_roots_admission_upper_bytes =
    max(C, H, terminal_created_roots_upper_bytes)
checkpoint_margin_upper_bytes =
    ceil_div(5 * checkpoint_active_tree_high_water_bytes, 4)
absolute_workspace_high_water_observed_bytes = B + H
absolute_workspace_admission_upper_bytes =
    B + created_roots_admission_upper_bytes
cutoff_workspace_bytes = B + R
terminal_workspace_upper_bytes =
    B + terminal_created_roots_upper_bytes
```

`all_passed` is Section 18's exact conjunction. Carried marker values are
never labeled observed. `observation_complete_to_cutoff=true`; the checkpoint
admission upper is the maximum carried/current value and is at most
`2000000000`, while the observed checkpoint tree is at most `1600000000`.

`registries` has exactly:

```text
names baseline final maximum all_baselines_restored
```

using the fixed nine-name order. On success it equals the latest complete
measurement-block boundary's `registries` object byte-for-byte; that boundary
therefore commits all traces across all worker epochs.

`acceptance` has exactly these Boolean keys:

```text
all_kernels_complete all_identities_match all_artifacts_valid
all_addresses_licensed no_scientific_output all_stationarity_passed
all_rate_robustness_passed all_time_budgets_passed all_task_budgets_passed
all_checkpoint_intervals_passed terminal_accounting_row_passed
rss_passed disk_passed registries_passed
```

Every value must be true. `terminal_accounting_row_passed` has the exact
charge-based meaning in `clock`; it does not certify end-to-end terminal
latency. `strongest_residual` is the exact single-line UTF-8
string `"non-W-proportional traces and tiled caches do not validate full-mixture linear scaling, heterogeneous 252-date lifetime, or a future 12-hour thermal trajectory"`.

Both terminal markers carry one exact `terminal_guard` object:

```text
schema_version method outcome_status
panel_source_snapshot_sha256 executable_source_snapshot_sha256
authority_source_snapshot_sha256 runtime_sha256 module_inventory_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
boot_identity_sha256 publication_started_perf_counter_ns
guard_cutoff_perf_counter_ns guard_elapsed_ns
terminal_close_accounting_charge_ns
source_seal git_control_inputs git_children publication_rss
no_live_descendants all_terminal_child_waits_collected passed
```

Fixed values are `schema_version=1`,
`method="post-json-git-process-publication-certificate-v1"`, and
`terminal_close_accounting_charge_ns=60000000000`. `outcome_status` equals
the containing marker's `"passed"` or `"failed"` status; it is not a second
resource-admission verdict.

The three source digests equal both the terminal JSON fields and the three
`attempt.source_snapshots.*.snapshot_sha256` values. `runtime_sha256` equals
the terminal JSON and `attempt.runtime.runtime_sha256`.
`module_inventory_sha256` equals the attempt field and the current recomputed
loaded-module inventory; terminal JSON has no duplicate module field.
Publisher identity equals the terminal JSON and the final durable boundary
publisher on success or final cleanup-complete failure-resume publisher on
failure. It need not equal the initial `attempt.time_origin` supervisor.
`boot_identity_sha256` equals the terminal cutoff boot
(`result.clock.cutoff_boot_identity_sha256` on success or the top-level failure
field), the named final predecessor's boot, and the current boot; it need not
equal the attempt's initial boot after an admitted changed-boot resume.

`publication_started_perf_counter_ns` is sampled immediately
before exclusive terminal-stage creation; `guard_cutoff_perf_counter_ns` is
sampled on that same boot after the twelve Git children are reaped and the
source/control/runtime/module/publisher checks and current sampler reconciliation
are complete, but before marker encoding. Exactly:

```text
guard_elapsed_ns =
    guard_cutoff_perf_counter_ns
    - publication_started_perf_counter_ns
```

It is nonnegative and at most `60000000000`. This proves the subprocess-bearing
prefix reached its guard cutoff within the 60-second guard-prefix limit; it does not
mislabel the marker write, final seal, rename, or parent fsync as observed.

`source_seal`, `git_control_inputs`, and `git_children` each have exactly
`count,rows,sha256`. Their rows and domains are Section 4.3's exact terminal
source-seal, Git-decision-input, and Git-child rows. Counts equal `len(rows)`;
the source and control counts are positive, Git-child count is exactly `12`,
and each digest is reconstructed from its rows. The post-JSON `source_seal` and
`git_control_inputs` equal both
`terminal_json.preterminal_git_checks.terminal_pre_json_check` objects and the
attempt bootstrap objects byte-for-byte; only the new post-JSON child rows
differ. Persisting the rows—not only
an opaque digest—makes every stdout result and wait/rusage claim independently
auditable and hash-binds every admitted Git-control input to the trusted
publisher's runtime validation. The certificate does not claim that mutable
pre-run Git-control bytes remain independently recoverable after the evidence
commit changes repository metadata.

The marker's `publication_rss` is deliberately distinct from the cumulative
run-level `rss` in terminal JSON. A dedicated 50-ms terminal-publication
sampling segment starts at `publication_started_perf_counter_ns`, before stage
creation, even when earlier telemetry selected failure. The twelve Git
children run strictly sequentially, so at most one is live at a time.
`publication_rss` has exactly:

```text
sample_period_ns samples maximum_sample_gap_ns
start_to_first_sample_gap_ns last_sample_to_guard_gap_ns
publication_start_self_resident_bytes sampled_publication_tree_peak_bytes
git_child_rusage_highwater_envelope_bytes
observed_publication_envelope_bytes current_margin_upper_bytes
rss_admission_upper_bytes limit_bytes observation_complete_to_guard passed
```

The values cover only this publication segment through
`guard_cutoff_perf_counter_ns`; historical failure telemetry is neither erased
nor required to pass here. Immediately after sampling
`publication_started_perf_counter_ns`, while holding `process_census_lock` and
before stage creation or any terminal Git child, the supervisor takes the
Section 4.6 stable task-info/start-identity bracket for itself.
`publication_start_self_resident_bytes` is that bracket's
`pti_resident_size`; any identity, ABI, or task-info failure prevents terminal
publication. `samples` has exactly `count,rows,sha256`. Rows are
`[sample_ordinal,perf_counter_ns,tree_resident_bytes]`, ordinals are contiguous
from zero, `count=len(rows)` is in `1..1201`, timestamps are strictly
increasing on the marker's boot, and the
digest is:

```text
SHA256(CJSON([
  "xid-g2-terminal-publication-rss-samples-v1",
  rows,
]))
```

The first sample is taken after
`publication_started_perf_counter_ns`; the final sample is taken no later than
`guard_cutoff_perf_counter_ns`. After the first, the sampler never intentionally
schedules a sample before `sample_period_ns` has elapsed. Every adjacent
timestamp gap, the start-to-first gap, and the last-to-guard gap enter the
completeness test, so identical truncated endpoint summaries cannot pass.
Define:

```text
sample_period_ns = 50000000
start_to_first_sample_gap_ns =
    samples.rows[0][1]
    - publication_started_perf_counter_ns
last_sample_to_guard_gap_ns =
    guard_cutoff_perf_counter_ns
    - samples.rows[-1][1]
maximum_sample_gap_ns =
    max(
        start_to_first_sample_gap_ns,
        every adjacent sample timestamp difference,
        last_sample_to_guard_gap_ns
    )
sampled_publication_tree_peak_bytes =
    max(row[2] for row in samples.rows)
git_child_rusage_highwater_envelope_bytes =
    publication_start_self_resident_bytes
    + max(child.ru_maxrss_bytes for the twelve Git children)
observed_publication_envelope_bytes =
    max(
        sampled_publication_tree_peak_bytes,
        git_child_rusage_highwater_envelope_bytes
    )
current_margin_upper_bytes =
    ceil_div(5 * observed_publication_envelope_bytes, 4)
rss_admission_upper_bytes = current_margin_upper_bytes
limit_bytes = 3500000000
```

Sampling has a positive row count, every derived gap is nonnegative,
`maximum_sample_gap_ns<=1000000000`,
`observation_complete_to_guard=true`, the observed publication envelope is at
most `2800000000`, the admission upper is at most the limit, and
`publication_rss.passed=true`. `no_live_descendants=true` and
`all_terminal_child_waits_collected=true` require the exact twelve expected
Git children to be absent/reaped and no other descendant to exist. They do not
rewrite missing historical waits in a failure JSON. Top-level `passed=true` is
the conjunction of every publication-certificate identity, command output,
child, terminal wait, source/control seal, clock, process, sampler, gap, and
publication-RSS predicate. On success, pair validity additionally requires the
terminal JSON's cumulative run-level RSS and every acceptance Boolean to pass.
On failure, the marker proves only that the failed run was closed under a
currently safe publication suffix; it never converts its failing run telemetry
into acceptance. The complete marker must remain within Section 2's
`1048576`-byte canonical JSON cap.

`R/terminal/success/_SUCCESS` is written and fsynced after `result.json`
inside the hidden success stage and has exactly:

```text
schema_version status result_sha256 terminal_guard complete
```

with `schema_version=1`, `status="passed"`, and `complete=true`.
`result_sha256=SHA256(exact result.json bytes)`.

On terminal failure, `R/terminal/failure/failure.json` has exactly:

```text
schema_version status attempt_sha256
publisher_supervisor_pid publisher_supervisor_start_identity
panel_source_snapshot_sha256
executable_source_snapshot_sha256 authority_source_snapshot_sha256
runtime_sha256 resource_config_sha256 failure_stage failure_type message
worker_return_code failure_intent_sha256 cutoff_boot_identity_sha256
cutoff_perf_counter_ns
cutoff_wall_time_ns calendar_to_cutoff_ns excluded_poweroff_ns
cumulative_active_to_cutoff_ns
terminal_close_method terminal_close_accounting_charge_ns
terminal_accounted_interval_ns resource_accounted_charge_ns
preterminal_git_checks rss disk receipt_inventories ordinary_prefix artifact_inventory rng logs
failure_cleanup retry_permitted
```

`status` is `"failed"`, `worker_return_code` is null or an exact signed
32-bit integer, the bounded `message` is UTF-8, and `retry_permitted` is exact
false. `failure_intent_sha256` hashes the one exact Section 10.2 registered
intent, and the selected failure fields equal it byte-for-byte.
`preterminal_git_checks` is Section 4.3's exact two-check terminal object; a
failed or incomplete terminal-pre-JSON child set leaves the selected failure
forensically incomplete and publishes no terminal JSON. A marked
failure is permitted only after one valid immutable
`attempt.json`; a failure before or during uncertain attempt publication leaves
the roots absent or the attempt consumed/forensically incomplete and publishes
no terminal JSON. Thus the attempt's baseline, source, runtime, config, and
time origin always exist for a marked failure.

On every marked failure,
`terminal_close_method="fixed-terminal-accounting-charge-v1"` and
`terminal_close_accounting_charge_ns=60000000000`; kernel 14 supplies no
end-to-end publication bound.
Let `F` be the mandatory cleanup-complete final failure-resume receipt. The
failure publisher remains on `F.boot_identity_sha256`, and the top-level clock
fields are exactly:

```text
cutoff_boot_identity_sha256 = F.boot_identity_sha256
terminal_work_ns =
    cutoff_perf_counter_ns - F.cutoff_perf_counter_ns
cumulative_active_to_cutoff_ns =
    F.cumulative_active_ns + terminal_work_ns
calendar_to_cutoff_ns =
    cutoff_wall_time_ns - attempt.time_origin.wall_time_ns
excluded_poweroff_ns = 0
terminal_accounted_interval_ns =
    terminal_work_ns + terminal_close_accounting_charge_ns
resource_accounted_charge_ns =
    cumulative_active_to_cutoff_ns + terminal_close_accounting_charge_ns
```

The final-resume cutoff and terminal cutoff are same-boot monotonic samples.
`terminal_work_ns` is nonnegative and at most `480000000000`; terminal
publication is assigned the fixed `60000000000` accounting charge; and the
root failure accounted sum is at most `540000000000`. Those three values
participate in
`failure_cleanup.maximum_chunk_work_elapsed_ns`,
`maximum_publication_accounting_ns`, and
`maximum_accounted_interval_ns`, respectively, together with the intent and all
failure-resume intervals. They do not claim the later marker/final-seal/rename/
parent-fsync suffix completed within 60 seconds.

Failure `receipt_inventories` has exactly:

```text
reservations worker_launches worker_births workers boundaries interruptions
cleanups traces measurements failure_intents failure_resumes
```

It contains only category-contiguous prefixes admitted by the deterministic
scheduler. Failure-intent count is exactly one; failure-resume indices are
contiguous from zero and their count is in `1..641`. The final resume alone is
cleanup-complete, every later index satisfies the progress/death rule, and the
attempt-wide process-death union is at most 128. Ordinary paths are exact:

```text
reservations:  panel-0000000000 through panel-(Q-1)
worker_launches: launch-0000000000 through launch-(L-1)
worker_births: birth-0000000000 through birth-(N-1)
workers:       worker-0000000000 through worker-(W-1)
boundaries:    boundary-0000000000 through boundary-(B-1)
interruptions: interruption-0000000000 through interruption-(I-1)
cleanups:      cleanup-0000000000 through cleanup-(C-1)
traces:        trace-0000000000 through trace-(T-1)
measurements:  empty, block-1, block-1..2, or block-1..3
```

Here `0 <= W <= N <= L <= 64`, `L-W <= 1`, and each birth/claim at index
`w` requires the launch/birth precursor at that same index. The two legal
strict cuts are one durable launch without birth and one complete birth
without claim. A same-boot launch-only cut is forensically incomplete; a
changed boot may close it only as the pre-capability failure defined in
Section 11. A birth-only cut must join the durable worker identity to an exact
wait/death proof before failure intent.

`ordinary_prefix` has exactly
`schema_version,event_count,event_inventory_sha256,tip_kind,tip_sha256`.
The validator reconstructs logical rows by running the frozen scheduler from
`attempt.json`:

```text
[event_ordinal, event_kind, category_index,
 relative_receipt_path, receipt_sha256]
```

`event_kind` is `"worker-launch"`, `"worker-birth"`, `"worker"`,
`"reservation"`, `"boundary"`, `"interruption"`, `"cleanup-intent"`,
`"trace"`, or `"measurement-block"`, and:

```text
event_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-ordinary-event-prefix-v1",
  rows,
]))
```

At each automaton state exactly one extant next leaf is legal. It admits the
worker-launch/worker-birth/worker-claim/reservation/worker-ready prelude, the
canonical trace word and role-dependent cleanup intents, trace/measurement
receipt followed by its boundary, and only the exact interruption branches in
Section 16. Zero or multiple legal next leaves fail. `event_count` and tip
identify the final row, or are zero/null for an empty prefix.

`artifact_inventory` has exactly:

```text
count sha256 kind_counts complete_trace_count
partial_trace_rows_sha256 all_final_artifacts_deleted
```

Its rows are the reproducible path-sorted union of complete trace rows and the
latest durable boundary/cleanup-intent partial rows. `kind_counts` is the
thirteen-key object. `partial_trace_rows_sha256` uses the normal artifact
inventory domain over only partial rows. `all_final_artifacts_deleted=true`
is required before the failure cutoff; a surviving final or hidden stage
prevents the marker. `complete_trace_count` equals both the exact
`receipt_inventories.traces.count` and the number of complete trace receipts
whose artifact rows enter the union.

Failure `rng` has exactly:

```text
seed streams durable_record_count durable_record_inventory_sha256
address_count address_inventory_sha256
address_upper_count address_upper_inventory_sha256
replay_record_charge_count replay_penalty_ns
```

Order every complete-trace kernel record and then the latest durable
boundary/cleanup-intent partial prefix by `(trace_index,kernel_position)`,
without duplication. Each durable row is:

```text
[trace_index, kernel_position, rng_call_count,
 rng_address_inventory_sha256, rng_call_upper_count,
 rng_address_upper_inventory_sha256, replay_count, replay_penalty_ns]
```

`durable_record_inventory_sha256` is:

```text
SHA256(CJSON([
  "xid-g2-resource-failure-durable-rng-records-v1",
  rows,
]))
```

The aggregate fields are exactly:

```text
durable_record_count = len(rows)
address_count = sum(row[2] for row in rows)
address_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-failure-address-inventory-v1",
  [[row[0],row[1],row[2],row[3]] for row in rows],
]))
address_upper_count = sum(row[4] for row in rows)
address_upper_inventory_sha256 =
SHA256(CJSON([
  "xid-g2-resource-failure-address-upper-inventory-v1",
  [[row[0],row[1],row[4],row[5]] for row in rows],
]))
replay_record_charge_count = sum(row[6] for row in rows)
replay_penalty_ns = 480000000000 * replay_record_charge_count
```

Each durable row also requires `row[7]=480000000000*row[6]`. Thus one physical
lost first epoch contributes two record charges. No uncommitted physical call
prefix appears. `seed=2026071529` and streams are the exact two resource
streams.

`logs` has exactly `stdout` and `stderr`; each is the Section 10.1
`count,rows,sha256` domain-separated inventory. Empty/no-worker values are
canonical, never an invented digest of an absent file.

Failure `rss` has exactly:

```text
sampling_started sample_period_ns sample_count maximum_sample_gap_ns
sampled_tree_peak_bytes supervisor_rusage_highwater_bytes
worker_waits preterminal_git_rusage_highwater_bytes
rusage_highwater_envelope_bytes
observed_envelope_to_cutoff_bytes carried_durable_marker_upper_bytes
current_margin_upper_bytes rss_admission_upper_bytes limit_bytes
observation_complete_to_cutoff predecessor_segment_close_method
sampler_complete all_wait_statuses_collected passed
```

`preterminal_git_rusage_highwater_bytes` is the maximum over the bootstrap and
terminal-pre-JSON child rows and must reconstruct from
`preterminal_git_checks`. If sampling never started,
`sampling_started=false`, counts, sampled peak, gap, and
`supervisor_rusage_highwater_bytes` are zero, `worker_waits` is the canonical
empty object, `rusage_highwater_envelope_bytes` and
`observed_envelope_to_cutoff_bytes` equal the preterminal Git scalar,
`current_margin_upper_bytes=ceil_div(5*observed_envelope_to_cutoff_bytes,4)`,
`sampler_complete=false`, and `passed=false`; the carried upper may still come
from a durable marker. Otherwise every value is the exact available cumulative
observation and `passed` uses the success cap/gap rules. The
rusage-envelope equality is the success formula over the persisted supervisor
sample, `worker_waits`, and preterminal Git scalar; worker rows must extend the
last durable inventory exactly. `all_wait_statuses_collected=true` iff every
issued worker child has its exact wait/rusage row and both preterminal Git
checks have all 24 exact rows. An identity closed only by
double absence or changed boot makes that Boolean false even though the
process-death proof is sufficient to close a marked failure; an identity with
neither wait nor death proof prevents publication. A missing wait or sampler
suffix is false, not null. Unknown loss sets
`observation_complete_to_cutoff=false`,
`predecessor_segment_close_method="unknown-loss"`, and the RSS admission
upper to at least `3500000001`. This cumulative object remains failing when it
selected `sampler-gap`, `rss-limit`, unknown-loss, or missing-wait failure.
The marker's distinct `terminal_guard.publication_rss` starts a fresh bounded
publication segment after cleanup and may pass when current resident memory
has returned below its close-safety threshold. That permits an honest marked
failure without erasing the reason it failed. If the dedicated publication
segment or final in-process publication predicate fails, the selected attempt
remains forensically incomplete and is not renamed.

Failure `disk` has exactly:

```text
baseline_complete outside_baseline_bytes
created_roots_high_water_observed_bytes
carried_durable_marker_created_roots_upper_bytes
created_roots_admission_upper_bytes
checkpoint_active_tree_high_water_bytes checkpoint_margin_upper_bytes
checkpoint_tree_admission_upper_bytes observation_complete_to_cutoff
predecessor_segment_close_method
absolute_workspace_high_water_observed_bytes
absolute_workspace_admission_upper_bytes filesystem
cutoff_created_roots_bytes cutoff_workspace_bytes
terminal_close_reserved_bytes terminal_created_roots_upper_bytes
terminal_workspace_upper_bytes
created_transient_limit_bytes checkpoint_limit_bytes
absolute_transient_limit_bytes steady_limit_bytes
cleanup_complete all_passed
```

`baseline_complete=true` because a marked failure requires a valid attempt.
Values use the success formulas over every available durable/current scan.
Unknown loss sets the completeness Boolean false and the checkpoint, created
roots, and absolute workspace uppers to at least `2000000001`,
`6000000001`, and `30000000001`, respectively.
`cleanup_complete` requires all artifact/stage/owner paths removed and every
parent fsynced. Any missing scan, device/unit mismatch, cleanup gap, or cap
breach sets `all_passed=false`; it does not omit or synthesize a field.

Before selecting failure, the supervisor reaps every currently waitable worker
and appends its wait/rusage row, proves every other issued worker identity dead
by an exact Section 16 method, requires every issued Git child to have its
mandatory wait/rusage row, closes capabilities/registries, finalizes logs,
completes only a committed cleanup-intent suffix, and inventories every durable
receipt, artifact, RNG, and log commitment. A proved missing wait remains the
selected failing fact; an unresolved identity prevents a marked failure. The
supervisor then follows Section 10.2: publish the immutable failure intent
before terminal deletion, remove only its exact journaled cleanup prefix across
any resume receipts, fsync parents, and take the final cutoff telemetry.
`failure_cleanup` is the exact common object. If a
forward receipt/final is invalid, non-prefix, or publication-uncertain before
intent, the attempt remains consumed and forensically incomplete. If cleanup
cannot finish within a current segment, failure remains selected and only the
next bounded contiguous failure-resume may continue. The mandatory final
cleanup-complete resume precedes terminal outcome publication. Reaching a
count/path/byte cap selects failure before creating another row and never
licenses an unbounded tail; ordinary work and success remain forbidden.

`R/terminal/failure/_FAILURE` has exactly:

```text
schema_version status failure_sha256 terminal_guard complete
```

with `schema_version=1`, `status="failed"`, and `complete=true`. Success and
failure evidence are mutually exclusive.
`failure_sha256=SHA256(exact failure.json bytes)`.
If terminal publication becomes uncertain, the consumed `attempt.json` and
failure intent remain authoritative; the same continuously live publisher may
finish only the exact staged outcome and any successor may reuse only an exact
visible final. A dead-publisher hidden outcome is forensically incomplete, and
no opposite outcome may be published.
Result, failure, and marker JSON files retain Section 2's
1,048,576-byte canonical-receipt cap and
use Section 10's exact atomic outcome-directory state machine. Their cutoff and
terminal-close fields are non-self-referential. Pair validity requires the
terminal JSON's preterminal predicate, the marker's post-JSON guard predicate,
and visible final-directory existence, which attests the later in-process seal.
No field claims to observe its own marker write, directory rename, or later
parent fsync.

The terminal result and failure receipts contain no coefficient, truth,
standard error, PCA loading, loss, bootstrap estimate, interval endpoint, or
sign/error comparison.

## 18. Three-root disk accounting

Before `attempt.json`, compute a no-follow recursive snapshot of the repository
workspace while all three canonical roots are absent. Let:

```text
B_L = logical bytes in the immutable outside inventory
B_A = allocated bytes in the immutable outside inventory
B   = max(B_L, B_A)
```

Every disk-inventory row, including Section 16 debris, is exactly:

```text
[repository_relative_path, entry_type, mode, logical_bytes,
 allocated_bytes, content_sha256_or_null]
```

`repository_relative_path` is NFC UTF-8 and rows are sorted by its UTF-8
bytes. The repository root itself is omitted. `entry_type` is exactly
`"directory"` or `"regular-file"`. With no-follow `lstat` result `st`, define:

```text
mode = format(
    stat.S_IFMT(st.st_mode) | stat.S_IMODE(st.st_mode),
    "06o",
)
logical_bytes = st.st_size
allocated_bytes = st.st_blocks * 512
```

`mode` is exactly six lowercase octal digits: directories are in
`040000..047777`, regular files in `100000..107777`. Regular-file content
SHA256 hashes exact bytes; directory digest is JSON null. A symlink, FIFO,
socket, character device, block device, unknown type, negative field,
overflow beyond `u64`, or identity change during inspection is terminal.

Let `M` be the exact set of proper-ancestor directory rows below the repository
root for `R`, `C`, and `S`; the repository root itself is already omitted.
For the registered roots:

```text
M = {"results", "data", "data/g2_resource_benchmark"}
```

and the rehearsal mechanically substitutes
`"data/g2_resource_rehearsal"` for the last entry. A named row in `M` is
included only when that directory currently exists. Omitting an `M` directory
row never prunes traversal: every sibling and every descendant outside the
three roots is still inventoried.

The outside baseline includes every descendant below the repository,
including ignored paths and `.git`, except the three roots and descendants
and only the directory rows in `M`. Those mutable ancestor rows are instead
included in created-root accounting below, because root creation/deletion
necessarily changes their metadata. `attempt.json` persists the outside
rows' logical/allocated aggregates, row count, and digest rather than the
potentially unbounded row array. After every trace and at the final
complete-hidden-outcome/pre-rename check, recomputation under the same
traversal/exclusion rule must match all four values exactly. Any new, removed,
or changed outside entry is an undeclared-write terminal failure.

Consequently both one-shot commands require a symlink-free execution worktree.
An ignored in-repository `.venv` is not exempt: its interpreter symlinks make
preflight fail before root creation or RNG authority. The registered/rehearsal
interpreter environment must already exist outside the repository, remain
read-only for the attempt, and match the frozen runtime/source launch
contract. This is an eligibility condition, not permission to delete or
rewrite a developer environment.

At every filesystem mutation under `R`, `C`, or `S`, scan all three roots and
the currently existing directory rows in `M` without following symlinks.
Include final files, hidden stages, temporary files, crash markers,
directories, sparse-file logical sizes, and the `M` rows themselves, but not
non-root descendants reached through `M`, using the same row grammar. Thus
every workspace row is charged exactly once: immutable descendants in the
outside baseline, or mutable root/ancestor rows here. Before any root exists,
record `statvfs` and `st_dev` for its nearest existing parent. After creation,
and at every mutation and preterminal cutoff, record them for each root. For
root `X`, define:

```text
a_X = f_frsize if f_frsize > 0 else f_bsize
```

Each `a_X` must be a positive `u64`, each root must remain on its pre-attempt
device, and no recorded device or allocation unit may change during the
attempt. Every persisted `filesystem` snapshot has exactly:

```text
result checkpoint scratch maximum_allocation_unit_bytes
```

Each named root record has exactly:

```text
root_exists probe_relative_path device_id allocation_unit_bytes
```

`root_exists` is a Boolean. Before creation, `probe_relative_path` names the
nearest existing repository-relative parent; after creation it is the exact
root path. The repository root is encoded by the exact string `"."`.
`device_id` is no-follow `st_dev` encoded as `u64`, and
`allocation_unit_bytes` is the corresponding `a_X`. The maximum field is the
maximum over the three records and all prior snapshots in the attempt; it is
therefore the current persisted value of `g`. Define `g` as the maximum over
every recorded `a_R`, `a_C`, and `a_S`. Then:

```text
L(t) = sum logical bytes across R,C,S and current M rows
A(t) = sum allocated bytes across R,C,S and current M rows
U(t) = max(L(t), A(t))

Q(t) = max(logical bytes below active checkpoint tree,
           allocated bytes below active checkpoint tree)
```

The exact inequalities are:

```text
F_close = 2 * 1,048,576 + 16 * g
C_resume = latest complete boundary created_roots_resume_upper_bytes, or zero
U_terminal_upper = U(cutoff) + F_close
U_admission_upper = max(C_resume, max_t U(t), U_terminal_upper)

U_admission_upper             <=  6,000,000,000
max_t Q(t)                    <=  2,000,000,000
B + U_admission_upper
                              <= 30,000,000,000
B + U_terminal_upper          <= 25,000,000,000
ceil_div(5 * max_t Q(t), 4)  <=  2,000,000,000
```

Capacity for the selected two-child terminal outcome, its same-parent hidden
stage, directory metadata, allocation rounding, and rename slack is reserved
before mutation. The selected terminal JSON and marker are each conservatively
capped at 1,048,576 bytes for this reservation calculation, which is also each
file's schema cap. The separate 16,384-byte binary-artifact `_SUCCESS` cap does
not apply to these terminal JSON markers. Exactly one hidden outcome directory
is renamed without overwrite to exactly one final outcome directory, so no
hard-link or JSON-only visible state is part of the protocol. The sixteen
allocation units cover both directories' metadata and rounding. A root scan
failure is terminal. Deletion and its parent fsync are charged before a
transient fixture may leave the active tree. `C_resume`, `max_t U(t)`,
`U(cutoff)`, `F_close`, `U_terminal_upper`, and `U_admission_upper` are
separately reported; the carried upper is not an observed scan and no
post-outcome scan is claimed. No external download occurs.

## 19. Deterministic pre-code falsification suite

Before registered authority can exist, exact test-seed tests must show:

1. the inherited base/cell artifact bytes and digests remain unchanged;
2. every new kind round-trips its exact payload bytes and only its exact
   stage-specific resource authority;
3. every listed missing, extra, symlink, hard-link, kind, path, JSON, NPY,
   shape, dtype, order, offset, length, nonfinite, parent, completion, address,
   source, runtime, attempt, manifest, payload, and marker mutation fails;
4. every payload total equals Section 7 and stays below 5 MiB;
5. the four research cache shards jointly contain exactly 252 rows and
   17,055,360 numeric bytes;
6. the publication envelope contains exactly 50 shards and 238,000,000
   numeric bytes, and kernel 14's close probe is exactly 1,048,576 canonical
   JSON bytes and exercises the ordinary atomic receipt-directory publisher;
7. cache/publication fixtures cannot mint scientific authority or enter a
   validation/research loader;
8. resource panels cannot be loaded through test, validation, or research
   authority;
9. a copied/reconstructed array cannot be registered;
10. reservation zero is cold, all reservation numbers are contiguous, partial
    reservations are not reused, and every thermal/measurement phase order is
    exact;
11. a sampler gap over one second, missing wait/rusage, PID reuse, source
    drift, outside-root write, cap breach, stationarity failure, or rate-robustness
    failure is terminal;
12. every worker-ready, zero-unit, positive-unit, complete-trace, measurement,
    cleanup-continuation, failure-intent, and failure-resume checkpoint has a
    contiguous predecessor chain; every work interval is at most 480 seconds,
    every ordinary publication upper is at most 60 seconds, every ordinary
    durable-marker interval upper is at most 540 seconds, every failure-intent
    and failure-resume receipt carries exactly the fixed 60-second
    `"fixed-failure-receipt-accounting-charge-v1"` charge and an accounted
    interval at most 540 seconds without representing that charge as observed
    publication latency, and bootstrap through durable `attempt.json` is at
    most 480 seconds;
13. capability bytes remain unreadable before worker-ready, pre-boundary loss
    selects terminal failure before `SeedSequence`, and only a complete signal,
    changed boot, or exact same-boot process-death set can resume later work; a
    partial trace continues only its exact next position under the same
    reservation, a partial measurement block continues its exact
    measurement-role subsequence after fresh thermalization, and neither
    completed prefix nor unfavorable duration can disappear;
14. same-boot, cross-boot, and chained interruption receipts reproduce the
    exact charged gap, retain cumulative active time, trace-start identity,
    actual observed pre-boundary highs, conservative RSS/disk resume uppers,
    completed unfavorable blocks, replay count/penalty/RNG uppers, and the
    exact next panel/trace/position without relabeling an upper observed; a
    clean signal preserves carried replay and a pre-worker-ready chained loss
    adds no ordinal;
15. every uncommitted artifact final or uniquely implied hidden stage is bound
    in the exact position-specific zero-to-three-target debris plan, with
    entry rows derived by Section 16.2, deleted and parent-fsynced before
    numerical replay; only an exact already-marked trace
    or measurement receipt may authorize its uniquely derived missing following
    boundary through `pending_receipt_completion`, and every other forward
    state fails;
16. atomic receipt-directory publication exposes no torn receipt/marker pair;
    each terminal result/failure JSON and its marker become visible together
    through a mutually exclusive, immutable, no-overwrite directory rename,
    and recovery never completes a JSON-only terminal state in place;
17. the k1+k2 internal cutoff partitions one physical epoch without becoming a
    resume point, its registry state restores only after k2, and each record
    receives the full fixed admission penalty for every lost epoch ordinal
    while cumulative physical elapsed is counted once;
18. initial and resumed worker-ready boundaries reproduce their distinct exact
    empty or copied-prefix states, every resume-state producer/consumer and
    last-use cleanup transition is exact, and no aggregate object crosses a
    boundary;
19. the three rehearsals produce exactly 45 canonical boundary leaves, 12
    cleanup-intent leaves, 57 capped checkpoint intervals plus one root
    terminal accounting row, 58 resource-accounting rows in total, 13
    artifact-kind keys, and 51 artifact rows, while registered
    interruptions may add only the
    specified prefix-copying worker-ready leaves;
20. every completed record's address-upper digest and every pending replay
    increment reproduce their distinct exact CJSON domains, row orders, counts,
    and epoch semantics;
21. ordinary later new-trace worker-ready publication preserves the prior
    accounting anchor so inter-trace orchestration enters k1 exactly once,
    while first-attempt and post-interruption anchors follow their explicit
    exceptions;
22. failure intent is durable before any terminal deletion; every subsequent
    filesystem state is one exact cleanup prefix, every resume is contiguous,
    and a crash cannot reopen work, change failure identity, or select success;
23. the exact resource-config byte length, byte SHA256, parsed type
    tree, and type-tree SHA256 reproduce the frozen Section 4.2 values, and
    registered seed construction fails before `SeedSequence` until the exact
    public command has a clean, hosted-green, explicitly authorized source
    and every A022--A026 deterministic prerequisite has passed;
24. the equal, validation, and research traces reproduce their exact
    15-position RNG-call count vectors, exact address order, and totals
    `1320`, `1315`, and `1315`, respectively, with no call in a zero-count
    position;
25. the shared paper-bootstrap weight artifact is drawn only at the first
    positive k13 position, reloads byte-identically at every later consumer,
    and is deleted only after the role-specific last positive k13 position;
26. every enumerated payload-only, payload-plus-marker, complete-final,
    marker-only, corrupt, extra-entry, and stage-plus-final receipt state
    either normalizes through the exact dead-publisher transition or fails
    closed; ordinary receipts, failure intent, and eligible nonfinal failure
    resumes exercise adoption, while a dead-publisher nonfinal resume in the
    last slot, a cleanup-complete resume, or either hidden terminal outcome
    always fails closed and a visible terminal final is reused; death of the
    visible final-resume publisher before failure cutover also fails closed
    without successor publication;
27. each process-death method reproduces its exact nullable-field table,
    every `wait4-reaped` row carries and joins the byte-normalized
    `ru_maxrss_bytes` value in the cumulative worker-wait inventory, initial
    supervisor identity is bound in `attempt.json`, and PID reuse or an
    unproved predecessor supervisor cannot authorize recovery;
28. every reservation after interruption binds the immutable original claim
    and a gap-free predecessor ancestry, and no successor can relabel or
    replace the original reservation;
29. every admitted interruption completes only its exact pending prefix and
    then performs a fresh 600-second thermal reset before any next warm trace;
30. every closed telemetry segment preserves only durably closed
    observations, while abrupt supervisor or direct boot loss selects the
    exact four limit-plus-one uppers and terminal failure before new work; and
31. the maximal failure-intent fixture exercises `64/63/4096`,
    `512/641/128/240`, the cleanup/death/wait/nonrow
    `1024/512/512/131072` component bounds, the exact
    empty-row-substitution byte equation, and a complete canonical envelope
    no larger than `753664` bytes, with every one-past mutation rejected
    before it is created;
32. every checkpoint/scratch mutation passes the prospective terminal-plan
    check, each entry is assigned to the unique deepest target, root fallbacks
    own all otherwise unassigned terminal entries, an early failure with either
    configured root absent emits no target for that root, every emitted target
    slice is positive and contiguous, and each tree/root target digest
    recomputes from its exact slice; and
33. every adoptable receipt schema encodes and revalidates its unique
    publisher, the attempt-wide process-death union is deduplicated and capped
    at 128, failure-resume zero plus every strict progress/death successor is
    capped at 641, and cap exhaustion after failure selection stops
    forensically incomplete without another mutation;
34. the post-JSON Git certificate launches exactly the twelve ordered children
    with the fixed absolute executable, prefix, environment, snapshot tuple,
    PID/start identity, signed `wait4` status, and byte-normalized
    `ru_maxrss`; any missing, additional, reordered, differently configured,
    wrong-returned-PID, signaled, nonzero, unreaped, or
    row/digest-inconsistent child prevents marker publication, and mutation of
    a child stdout count/hash/parsed projection or a zero-exit dirty `clean`
    result is rejected;
35. after marker and stage-directory fsync, mutation of any declared or
    Git-ignored `src/xid` source, literal authority file, Git executable,
    index, repository config/exclude, HEAD/loose-ref/packed-ref, applicable
    `.gitignore`, applicable `.gitattributes`, `.git/info/attributes`,
    runtime/module/boot identity, or publisher identity makes the final
    in-process seal fail before rename and leaves the selected hidden outcome
    forensically incomplete; removal or mutation of `GIT_ATTR_NOSYSTEM` or any
    other fixed child environment/prefix row is rejected before child launch;
36. an unexpected descendant, missing final wait/rusage evidence, sampler
    incompleteness, a final sample gap over one second, observed RSS above
    `2800000000` bytes, or recomputed 25%-margin RSS admission above
    `3500000000` bytes prevents terminal visibility;
37. crash injection immediately before stage creation, between exclusive
    creation and terminal-parent fsync, after that fsync, after JSON fsync,
    after marker fsync, after stage fsync, after rename, and after final parent
    fsync reproduces the exact pre-cutover, conservatively kind-locked hidden,
    forensically incomplete, or reusable visible-final state prescribed by
    Section 10, and never licenses the opposite outcome; and
38. the marker proves only that the subprocess-bearing prefix reached its
    guard cutoff within `60000000000` ns; no test or receipt relabels marker
    write, final seal, rename, or parent-fsync latency as observed, while the
    syscall-only suffix remains represented only by the conservative fixed
    accounting charge; and
39. wait/rusage truth-table fixtures prove that a currently waitable worker is
    reaped into one exact cumulative inventory row, a non-wait death proof
    permits only marked failure with `all_wait_statuses_collected=false` and
    `passed=false`, absence of both a wait row and a valid death proof blocks
    failure-intent publication,
    an omitted/duplicate/wrong-identity/wrong-status/wrong-`ru_maxrss` worker
    row or non-prefix cumulative inventory is rejected, and every missing Git
    wait/rusage row is forensically incomplete rather than converted to a
    worker death proof; and
40. `attempt.json` persists exactly one complete twelve-child bootstrap Git
    check, each visible terminal JSON persists exactly one complete
    twelve-child terminal-pre-JSON check and their two-check inventory, no Git
    subprocess is launched between them or while a worker is alive, and the
    terminal cumulative rusage envelope adds the supervisor high water to the
    maximum of all worker and all 24 preterminal Git-child high waters.
    Rehearsal success additionally requires exactly three worker-wait rows and
    all 24 Git rows. Mutation/omission of either check, any child row or digest,
    or the rusage maximum fails; terminal-pre-JSON failure or death of the
    final-boundary/final-resume publisher before visibility is forensically
    incomplete and never authorizes a retry or third preterminal check; and
41. for fixed raw `D`, units, and enclosure `h`, incrementing any one record's
    replay count by one leaves every `Rplus` reference operand and derived
    `H`/`X` prediction byte-for-byte unchanged; among timing comparator and
    projection operands it weakly increases only the affected held/current
    `Aplus` and its dependent absolute projections, leaves successful-work
    stop clocks unchanged, and cannot change any
    stationarity, temporal, cross-context, task, phase, total, or overall
    acceptance Boolean from false to true. Required rejection fixtures include
    equal-count blocks `(600 s,640 s)` where adding one prior-block replay
    cannot repair stationarity, and leave-one-out raw durations
    `[1000,1000,1300]` with replay counts `[1,0,0]` where the third block
    remains a temporal failure; and
42. crash injection before launch-intent publication, after intent/before
    spawn, after spawn/before birth, at birth payload-only and
    payload-plus-marker stages, after complete birth/before claim, after
    claim/before worker-ready, and after worker-ready/before capability proves
    that no unregistered live child or incomplete precursor can receive
    capability bytes or reach `SeedSequence`, while every complete birth joins
    exactly one eventual wait/death proof; and
43. Darwin process-identity fixtures exercise same-target presence,
    `ESRCH/ESRCH`, stable PID reuse, mixed `ESRCH`/reuse, changing reused
    identity, `EPERM`, ambiguous zero/zero, short and oversize returns, ABI
    mismatch, and boot change between samples. Only the two exact stable
    absence classes pass, their compact factorization round-trips both raw
    observations, and every maximum-width process-death row stays within 512
    bytes while the duplicated-identity form is rejected; and
44. final-success boundary crash injection at absent, payload-only,
    payload-plus-marker, post-rename, and post-parent-fsync states distinguishes
    the same live publisher from a dead one: no dead-publisher case may adopt
    the stage, launch a terminal Git child, publish another receipt, create a
    terminal outcome, or choose the opposite outcome; and
45. every launch intent and every boundary, cleanup intent, or interruption
    that can precede worker work persists the governing watchdog arm before
    that work. Missing/wrong arm digests, first appearance in a wait row,
    recomputation from a later clock, timeout request after the work deadline,
    `wait4` after the reap deadline, and work/reap-deadline substitution are
    deterministic failures; and
46. the fixture-schema digest reproduces maximum canonical failure-intent,
    every failure-resume shape, success/failure terminal JSON, and both
    terminal markers with all applicable `64/128/512/641/240/24/12/1201`
    maxima. Every file is at most 1 MiB, every one-past mutation fails before
    publication, the final success boundary and final failure resume bind the
    applicable passing preflight, and a missing/failing preflight can never
    enter terminal publication.

## 20. Strongest unresolved objection

The artifact contract closes byte ambiguity, schema substitution, false
scientific issuance, torn publication, cap accounting, and resume
cherry-picking inside the trusted local boundary. It does not make the fixed
phase traces proportional to `W`, validate per-kernel linear extrapolation, or
make tiled paper caches representative of 252 heterogeneous paper dates.
Those fixtures reproduce exact shape, byte volume, weighted accumulation,
hashing, fsync, reload, validation, and cleanup, but they repeat one actual
resource summary.

RSS authority remains measurement-based rather than a continuous mathematical
bound. The 50-ms sampler, one-second hard gap rule, child `wait4` high-water
values, and 25% margin make a missed material excursion less plausible and
falsifiable under rehearsal, but a sub-sample parent-process spike during
terminal publication can escape observation. In particular,
`publication_start_self_resident_bytes + max(child.ru_maxrss_bytes)` bounds the
measured child envelope, not arbitrary unsampled parent growth; the 25% factor
is policy headroom, not a proof of impossibility.

These are the strongest residuals. The resource admission derivation must keep
them prominent, and later validation/research runners must retain live
reforecast and hard-stop rules. No artifact or receipt defined here turns
either limitation into a continuous RSS guarantee or a measured full-mixture
guarantee.

## 21. Historical A025 closure and precedence

A025 is a specification amendment, not evidence that the implementation or
resource rehearsal exists. It preserves the previously frozen seeds, address
domains, scientific estimands, kernel set, and resource ceilings while
superseding every conflicting A022--A024 sentence about RNG-call counts,
resume-state cardinality, paper-weight lifetime, receipt recovery, terminal
publication, process death, reservation continuation, interruption
thermalization, telemetry continuity, cleanup granularity, failure-prefix
shape, evidence-envelope finiteness, replay-comparator operand roles, durable
worker birth, Darwin double-absence encoding, watchdog-arm provenance,
final-boundary adoption, or all-terminal size preflight.

The deterministic tuple frozen by A025 was:

```text
config bytes/hash/type rows/type hash:
9061
1a196dc09b9fdee9b9df6389d44b43bf24f10cd07cfef0140a6696ebcb1ec9fe
184
838f74d41bd4f553bd5c01dceebe279de0ed7fa998d88ba0cff510e470a40df6

successful rehearsal:
3 traces
45 canonical boundaries
12 cleanup intents
57 capped checkpoint intervals
1 terminal accounting row
58 resource-accounting rows
13 artifact kinds
51 artifact rows
7 resume-state rows per trace
```

Amendment A026 supersedes A025 only for interruption admission, launch-only
recovery, terminal-entry recovery, and the active config seal. All other A025
clauses remain controlling.

## 22. A026 closure and precedence

A026 is a specification amendment, not execution evidence. It leaves every
scientific address, kernel, estimator, threshold, budget, successful artifact
shape, and successful-rehearsal count unchanged. It supersedes every earlier
sentence that would (i) admit any suffix of an interrupted rate-bearing trace,
(ii) classify an exact same-boot launch-only state as permanently
unpublishable after supervisor death despite proved descriptor quiescence, or
(iii) leave an exact success/failure terminal-entry state without a definitive
nonpass close after its publisher dies or publication fails.

The active deterministic tuple is:

```text
config bytes/hash/type rows/type hash:
9799
3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29
194
e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3

successful rehearsal:
3 traces
45 canonical boundaries
12 cleanup intents
57 capped checkpoint intervals
1 terminal accounting row
58 resource-accounting rows
13 artifact kinds
51 artifact rows
7 resume-state rows per trace
```

The launch-quiescence mechanism relies on the Darwin contract that `flock`
locks are associated with the shared open-file object: `dup`/`fork`
references share it, a separately opened descriptor receives
`EWOULDBLOCK` while the incompatible lock remains, and final close releases
the lock. The controlling primary references are Apple's `flock(2)`,
`close(2)`, `execve(2)`, and `fcntl(2)` man pages and the Apple XNU
`sys_flock`, `finishdup`, `fg_drop`, and `vn_closefile` implementations,
retrieved 2026-08-06. This is not generalized to network filesystems or other
operating systems. `EOPNOTSUPP`, a changed inode, unexpected descriptor,
explicit unlock, duplicate/pass capability, or any unproved bootstrap
descendant is terminal non-admission.

Primary references:

- Apple, [`flock(2)`](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/flock.2.html),
  [`close(2)`](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/close.2.html),
  [`execve(2)`](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/execve.2.html), and
  [`fcntl(2)`](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fcntl.2.html);
- Apple XNU,
  [`kern_descrip.c`](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/kern_descrip.c)
  (`sys_flock`, `finishdup`, `fg_drop`) and
  [`vfs_vnops.c`](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/vfs/vfs_vnops.c)
  (`vn_closefile`).

Before implementation can pass review, deterministic fixtures must prove all
of the following without constructing a registered namespace:

1. interruption at every boundary-adjacent point and inside every cold/equal/
   validation/research rate-bearing trace selects terminal failure, contributes
   no timing operand, and cannot be replaced; between-trace interruption
   requires a complete fresh thermal cycle, and interrupted thermal cycles
   restart from zero;
2. launch-intent crash injection covers pre-lock, locked hidden stage,
   payload-only, marker-complete, post-rename/pre-parent-fsync, pre-spawn,
   post-spawn/pre-birth, and hidden-birth states. A live inherited holder yields
   `EWOULDBLOCK`; only exact supervisor death plus fresh-open acquisition of the
   same inode selects pre-RNG failure. Wrong path/inode/mode/link/content,
   `LOCK_UN`, descriptor duplication/passing, descendant creation, and
   unsupported locking all fail closed;
3. terminal-entry and terminal-outcome crash injection covers absent,
   payload-only, marker-complete, hidden selected outcome, nonpass-intent, every
   nonpass-stage prefix, uncertain rename, and visible nonpass. Repeated
   successor deaths rebuild identical `nonpass.json/_NONPASS` bytes, never
   rerun Git or RNG, never publish the opposite selected outcome, and never
   change `admission_pass=false` or `retry_permitted=false`;
4. maximum-width nonpass intent remains at most 131,072 bytes, both nonpass
   files remain at most 1 MiB, and every one-past mutation fails before stage
   creation; and
5. the exact 9,799-byte config, full typed value, 194-row type tree, and both
   SHA256 values above reproduce from a fresh process.

No implementation may begin until fresh independent methods, systems, and
schema hostile reviews all pass this A022--A026 document set. No rehearsal may
run until the resulting implementation passes its deterministic local suite
and hosted CI, and no registered seed may be constructed until the separately
authorized public command satisfies every gate condition.
