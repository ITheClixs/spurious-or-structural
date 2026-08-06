# G2 resource-admission derivation

Written on 2026-07-28 before any registered G2 resource, validation, or
research RNG access and before any resource-run implementation; amended on
2026-07-29 and 2026-08-06 by append-only preregistration amendments A023--A026
before code. This document derives the A022 admission experiment under A023's
narrower claim, A024's restartable operand order, A025's closed receipt and
evidence state machine, and A026's interruption, launch-quiescence, and
terminal-nonpass closure. It changes no G2 DGP, estimator, scientific
threshold, work total, validation family, or research address.

## 1. Claim and scope

The claim tested here is deliberately narrow:

> On the exact final M4 runtime, source snapshot, thread environment, and
> registered resource address law, complete production kernels can be measured
> in operand-complete cold/equal contexts and two fixed, non-`W`-proportional
> phase-labelled stress contexts. Conditional on per-kernel linear
> extrapolation beyond those timed unit counts, the frozen G2
> work matrix—including provenance validation, hashing, checkpoint I/O,
> interval finalization, and success-last publication—projects inside every
> expected wall-clock, task, RSS, and disk bound.

This is an engineering admission claim. It is not evidence about structural
truth, finite-sample bias, power, or the premise of G2. No coefficient, PCA
loading, loss, bootstrap estimate, or comparison with truth may enter the
public resource result.

The frozen fourteen kernels, phase work matrix `W`, statistical design,
registered resource seed `2026071529`, phase/scenario assignments, and
one-/12-/three-/16-hour expected bounds remain unchanged. A022 narrowly
supersedes only:

1. the non-executable “one unit of each kernel” benchmark bundle;
2. the last-three equal-context warm rate as the sole admission statistic;
3. the undefined “larger validation payload”; and
4. the ambiguity between combined I/O kernel rates and their required
   serialize/publish/load/hash/validate/issue diagnostics.

The sealed `configs/g2.toml` is not edited.
`configs/g2_resource.toml` is the separate preregistered executable contract;
the artifact authority binds its exact byte length, SHA256, key/type schema,
fixed block counts, paths, order, shapes, and boundary schedule before code or
the three measurability rehearsals. It contains no observed duration or
self-referential source digest.

## 2. Diagnosis before method selection

The naive benchmark fails before stochastic execution for distinct reasons.

### 2.1 It would time surrogates

The repository currently has no six-specification paper estimator, `CI_I`
recovery runner, paper bootstrap cache, interval-finalization pipeline, phase
publisher, compute-contract parser, or registered resource capability. Timing
private ridge kernels and extrapolating them to the frozen fourteen-kernel
matrix would omit the dominant published-protocol work.

### 2.2 Its operand graph is impossible

One `base_panel_io_hash` or `cell_io_hash` unit is a complete 252-date
artifact. A “one base date plus one full panel I/O” bundle must either generate
251 dates outside the clock or serialize a false panel. Likewise, one paper
date cannot honestly mint a 252-date paper cache. The old bundle therefore
left necessary operand construction unassigned.

### 2.3 Its timing resolution is inadequate

Several cheap kernels may complete in less than one meaningful clock or
scheduler interval. One call per bundle can make the normalized rate depend
more on timer quantization than on the operation being projected.

### 2.4 Its temporal and cross-context rate assumptions are untested

The frozen phase projection is additive:

```text
sum_k W[p,k] / v_k.
```

An equal-weight, fixed-order bundle does not establish temporal stability or
that rates survive validation and research contexts. Thermal state, allocator
and cache lifetime, checkpoint-tree state, and input-dependent LASSO iteration
counts can interact with the context.

Nor can a nontrivial exact proportional trace be constructed under the frozen
task grammar. For a reduced fraction `alpha=a/b`, integrality of
`alpha*W[p,k]` at kernel 14, whose work is one in both phases, forces `b=1`;
even after dropping kernel 14, each phase's nonzero work counts have greatest
common divisor one. A trace small enough for the 480-second lost-work bound
therefore cannot validate the realized full-workload mixture. A022 must test
bounded temporal and cross-phase rate robustness and state linear
per-kernel extrapolation as an explicit residual assumption.

### 2.5 Its lifecycle and limits are ambiguous

The old prose does not define registered resource capability construction,
address reservation, interruption versus terminal failure, thermal epochs,
fixture authority, artifact retention, process-tree RSS measurement, or the
conflict between the configured decimal `2,000,000,000`-byte tree cap and the
codec's larger generic `2 * 1024**3` ceiling.

These diagnoses preceded any method search. No literature method was selected
to repair them; the contract below follows directly from the measured objects
and frozen workload.

## 3. Prerequisites and authority boundary

The public command is fixed as:

```text
make g2-resource-benchmark
```

Its canonical roots are:

```text
results/g2_resource_benchmark/
data/g2_resource_benchmark/checkpoints/
data/g2_resource_benchmark/scratch/
```

The command is not executable merely because this derivation exists. Before a
registered resource address can be constructed, all of the following must
hold:

1. all fourteen production kernels and every artifact variant below exist;
2. every estimator has recovered known truth under authorized test seeds at
   the actual `N=30`, date count, and relevant regime contrast;
3. deterministic malformed-state, provenance, resume, cap, and source-drift
   tests pass;
4. the three exact test-seed measurability rehearsals in Section 7 pass and
   publish immutable success-last evidence outside the declared source paths;
5. fresh independent methods, systems, and schema hostile reviews all pass;
6. the worktree is clean and hosted CI is green on the exact source SHA;
7. all three canonical roots are absent for a new attempt; and
8. the exact irreversible command has explicit human authorization.

Semantic agreement with the TOML is insufficient. Implementation remains
forbidden until the post-A026 `configs/g2_resource.toml` byte length, SHA256,
and key/type seal are recomputed, every conflicting cross-document value is
removed or explicitly classified as historical, and the three fresh hostile
reviews run against that settled byte-authoritative package.

The implementation must add an exact `ResourceRngNamespace` type. It may not
add an `allow_registered` flag to `TestRngNamespace`. The only constructor is
an internal factory that consumes a supervisor-minted, one-use anonymous-pipe
capability. Every registered and rehearsal attempt binds the initial supervisor
PID, kernel-derived process-start identity, and boot-identity digest. The pipe
payload binds the attempt SHA256, worker index, supervisor and worker
PID/start identities, all three source-snapshot SHA256s, runtime/config
SHA256s, and the exact lowercase-hex 256-bit supervisor nonce. It is never
accepted through an environment variable, command-line argument, filesystem
token, caller boolean, or public Python constructor.

Worker launch is two-phase and durable before a worker claim can exist. For
worker index `w`, the supervisor executes this exact order:

1. create distinct anonymous capability and parent-liveness pipes, draw exactly
   32 capability bytes with `os.urandom(32)`, derive the nonce commitment,
   create/open exactly one launch `quiescence.lock`, and acquire its exclusive
   nonblocking Darwin `flock` before a child exists;
2. derive the initial `watchdog_arm` below and durably publish and revalidate
   the immutable three-entry `resource-worker-launch-intent-v1` directory
   before a child exists;
3. spawn the bootstrap-only child with the two read descriptors and one
   reference to the same locked open-file object inherited;
   before capability release it may use only the standard library and frozen
   birth publisher and exits with the fixed pre-authority code on
   parent-liveness EOF;
4. as its first persistent action, the child queries its PID/start/boot and the
   encoded parent identity, brackets birth publication with non-EOF liveness
   and unchanged-parent checks, and atomically publishes
   `resource-worker-birth-v1`;
5. under the process-census lock, require the returned spawn PID/start/boot to
   equal the complete birth record and require birth publication not later
   than the intent's registration deadline;
6. publish and revalidate the worker claim and marker, binding the exact launch
   and birth digests, capability SHA256, and byte-equal initial arm;
7. publish and revalidate the applicable reservation and worker-ready boundary,
   or revalidate the existing reservation before a resume worker-ready
   boundary; and only then
8. write the exact capability payload once and close the capability write
   descriptor.

The launch-intent payload has exactly:

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

with `receipt_kind="resource-worker-launch-intent-v1"`,
`status="launch-intent"`,
`parent_liveness_kind="anonymous-pipe-eof-before-capability-v1"`, and

```text
registration_deadline_perf_counter_ns =
    launch_perf_counter_ns + 60000000000
```

The intent directory's third entry is exactly mode-`0600`
`quiescence.lock`, 34 bytes
`xid-g2-launch-quiescence-lease-v1\n`, SHA256
`ebc63059762c893ce8829c9f495615854f58e8624a8bb68f496bf9764bacf807`.
The artifact authority freezes its inode/type/link checks and the only legal
stage-normalization transition.

The child-published birth payload has exactly:

```text
schema_version receipt_kind status attempt_sha256 worker_index
launch_intent_sha256 pid process_start_identity boot_identity_sha256
publisher_worker_pid publisher_worker_start_identity
supervisor_pid supervisor_start_identity
birth_wall_time_ns birth_perf_counter_ns
```

Its `receipt_kind` is `"resource-worker-birth-v1"`, status is
`"born-no-capability"`, the publisher fields equal the worker fields, and the
supervisor fields equal the launch intent. The worker claim binds these exact
receipts as `launch_intent_sha256` and `worker_birth_sha256`, and copies the
intent arm as `initial_watchdog_arm`.

The supervisor keeps the parent-liveness write descriptor and launch lease open
through capability release and closes them on every orderly worker close. The
child keeps its inherited lease reference through visible birth and claim and
closes without `LOCK_UN`; before release it polls both pipe descriptors.
Liveness EOF/HUP or capability EOF before a complete payload causes immediate
pre-authority exit. Launch-only code cannot unlock, reopen, duplicate, pass,
unlink, replace, or leak the lease or spawn a descendant. A same-boot launch
intent without complete visible birth after supervisor death is recovery-
pending. A successor proves the encoded supervisor dead, independently opens
and revalidates the same stable lease inode, and attempts `LOCK_EX|LOCK_NB`.
`EWOULDBLOCK` authorizes no mutation. Successful acquisition under the frozen
descriptor discipline proves launch quiescence and selects the ordinary pre-RNG
terminal-failure lane. A changed boot may close that launch-only state as
pre-capability because no child, pipe, or inherited descriptor survives. A
complete visible birth makes the child identity durable and requires an exact
wait/death proof even if no worker claim followed. A hidden birth stage is not
adopted as worker identity; after supervisor death it can close only through
the same lease-quiescence failure rule and then enters cleanup evidence.

- accepts only seed `2026071529`;
- issues only `RESOURCE_SMOOTH` and `RESOURCE_PAPER` DGP and bootstrap
  addresses;
- cannot construct a validation or research address;
- reruns the frozen A006 runtime known-answer preflight;
- binds the exact clean source, runtime, thread, config, target, ratio, both
  A022 derivations, prediction, preregistration, compute-plan, and
  resource-config digests;
- is constructed inside the Make-launched worker only after immutable
  `attempt.json`, its complete launch intent and self-published birth receipt,
  the worker's complete claim/marker, its reservation, and its worker-ready
  boundary exist; the launch-intent/birth/claim PID, start, boot, index, and
  ancestry joins must agree; on the first worker the pipe payload, current
  claim, reservation's immutable original-claim digest, and worker-ready
  boundary agree directly; on a resumed worker the pipe payload, current claim,
  and worker-ready boundary agree, while the reservation's original claim is
  reached by the exact finite, gap-free, repetition-free backward walk from
  the current claim, with each intervening link authorized by one contiguous
  interruption; the reservation is never rewritten to name the successor;
  the pipe payload is made readable only after all applicable objects validate,
  and the child revalidates them before the factory can construct authority; and
- is never serialized into a checkpoint.

Any relevant source, runtime, config, or thread change invalidates all measured
rates. The final resource result root contains immutable `attempt.json` and
exactly one terminal outcome directory:

```text
terminal/success/
    result.json
    _SUCCESS
```

or

```text
terminal/failure/
    failure.json
    _FAILURE
```

or, only after a selected success/failure terminal entry cannot be certified,

```text
terminal/nonpass/
    nonpass.json
    _NONPASS
```

The only hidden stages are respectively
`terminal/.success.xid-g2-terminal-stage-v1/` and
`terminal/.failure.xid-g2-terminal-stage-v1/`; terminal nonpass uses
`terminal/.nonpass.xid-g2-terminal-stage-v1/`. A success/failure publisher exclusively
creates the stage and fsyncs `terminal/`, writes and fsyncs the exact JSON,
writes and fsyncs the post-JSON Git/process/RSS certificate marker, fsyncs the
stage directory, runs the final in-process source/control/runtime/publisher
seal, stops and joins the sampler, no-overwrite renames the complete directory,
and fsyncs `terminal/`. A visible outcome therefore
always contains its complete pair.
Marker-only, invalid, conflicting, both-kind, or JSON-without-marker states are
forensically incomplete and cannot select the opposite outcome. Exclusive
creation of the unique hidden success or failure directory followed by
successful completion of its immediate parent fsync is the forward-execution
terminal cutover and locks that outcome kind. If a crash lands between those
operations, an absent stage after recovery is pre-cutover; an exact surviving
stage conservatively locks its kind and is treated as a dead-publisher hidden
stage, never as authority for the opposite outcome. The same continuously live
publisher may finish its stage. An exact visible
final after an uncertain rename is revalidated and reused only after the
current live supervisor fsyncs `terminal/`. A successor never adopts a hidden
success/failure outcome left by a dead publisher and never publishes the
opposite selected outcome. It may only publish the A026 forensic nonpass after
the exact terminal-entry and publisher-death prerequisites below validate.
Abrupt-supervisor-loss unknown telemetry selects failure only before
publication of the final success boundary. Publication of that boundary or the
cleanup-complete final failure resume is non-resumable terminal entry; later
loss can close only as terminal nonpass. Every
terminal JSON encodes its publisher: success matches the final-boundary
publisher and failure matches the cleanup-complete final-resume publisher.
Every boundary receipt carries exact Boolean `terminal_entry`; it is true only
for the final block-3 measurement boundary after every success precondition and
the pre-entry `terminal_size_preflight` below passes. When true,
`next_watchdog_arm` is null. If that final preflight fails, the boundary
persists the failed object as an ordinary `terminal_entry=false` boundary,
publishes no successor worker or capability, and selects the ordinary
terminal-failure lane. Every boundary that is not this final candidate carries
null `terminal_size_preflight`; it carries the exact nonnull
`next_watchdog_arm` below whenever later worker work remains and otherwise
carries null. A
`terminal_entry=true` payload-only or
payload-plus-marker hidden receipt stage may be finished only by that same
continuously live publisher. If the encoded publisher is dead, successor
normalization and rename are forbidden: the attempt is forensically incomplete
as success/failure because the otherwise-required next receipt would occur
after terminal entry. Its exact immutable payload can instead select terminal
nonpass after publisher death. An already visible final boundary remains
immutable evidence but licenses no successor success/failure publication.

Terminal nonpass is a definitive consumed-attempt non-admission, not a retry or
an outcome switch. An ordinary successor-adoptable
`resource-terminal-nonpass-intent-v1` first binds the selected outcome kind,
exact terminal-entry bytes/location, original publisher death or live
post-entry failure, any selected hidden-stage inventory, and one locked
`publication.lock`. `nonpass.json` and `_NONPASS` are canonical pure functions
of that visible intent; they contain `admission_pass=false` and
`retry_permitted=false`, launch no Git child, construct no RNG, and report no
new timing measurement. A publisher or successor must hold the exact stable
Darwin lease inode while creating, rebuilding, or adopting the hidden nonpass
stage. After holder death, fresh-open `LOCK_EX|LOCK_NB` acquisition permits an
exact incomplete stage suffix to be rebuilt byte-for-byte. Visible nonpass is
mutually exclusive with visible success/failure and receives the same fixed
60-second terminal accounting charge without claiming a close-latency bound.
The complete schemas and crash transitions are frozen in the artifact
authority.

There is one logical resource attempt and no seed retry. After the first
worker-ready checkpoint, a lost worker under a continuously observing live
supervisor, or a successor carrying an already durable clean-exit interruption
receipt, may resume that same attempt under identical bytes and runtime.
Abrupt supervisor or power/boot loss cannot preserve favorable telemetry and
therefore selects the A025 unknown-loss terminal-failure branch. Loss after
`attempt.json` but before boundary zero selects terminal failure before
capability release or `SeedSequence`; there is no invented pre-boundary resume
state. A stationarity, rate-robustness, numerical, provenance, budget, or
specification failure is terminal and cannot be relabeled as an interruption.

The source-snapshot path tuple is exactly:

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

Snapshot version 1 reuses the A020 stable-file enumeration algorithm exactly:
validate the Git top level; enumerate tracked plus untracked, non-ignored
regular files below the tuple; reject absent paths, aliases, symlinks,
non-regular files, unstable identity, duplicate or non-normalized paths; sort
by UTF-8 path bytes; and encode
`[relative_path, mode, byte_count, SHA256(file_bytes)]` as canonical JSON. The
panel identity retains namespace `xid-g2-source-snapshot-v1\n`; the executable
and authority identities use
`xid-g2-resource-executable-source-snapshot-v1\n` and
`xid-g2-resource-authority-source-snapshot-v1\n`, respectively.

Before the first worker, one twelve-child bootstrap full Git check is reaped
and persisted in `attempt.json`. Subprocess-free in-process source/control
seals reconstructed from the bootstrap source/control rows and enumeration
arrays run before and after sealed contract/resource-config loading,
immediately before and after every nonterminal resource-root mutation, before
every worker capability, and after every measurement block. After every issued
worker identity is closed, no worker is alive, and every currently waitable
direct child has been reaped, the only second full preterminal check launches
and reaps twelve children. The selected terminal JSON persists that complete
check, all of its output/wait/rusage rows, and the count-two inventory that also
binds the bootstrap check. No other preterminal Git subprocess is legal.

After the exact terminal JSON is written/fsynced inside the hidden stage, one
final full three-snapshot check launches exactly twelve sampler-observed Git
children: top-level, enumeration, commit, and clean roles for panel,
executable, and authority in that order. The marker is a post-JSON resource
certificate. Its exact `terminal_guard` persists all twelve PID/start/argv/
wait4/rusage/stdout/stderr/parsed-result rows, the complete source and
Git-control-input row inventories, the pinned Git-executable identity, the
three source plus runtime/module/boot/publisher identities, a dedicated
publication-local sampler row inventory, no-descendant/all-waits flags, and the
recomputed 25% RSS upper. System/global/external Git config and attributes are
disabled; repository index, config/exclude/attributes, HEAD/ref/packed-ref
inputs and applicable `.gitignore`/`.gitattributes` files are hash-bound.
Marker publication requires every child result to reconstruct the root,
enumeration, commit, and clean decision, every child to be reaped, no
unexpected descendant, every sampler endpoint/adjacent gap at most one second,
the publication-local observed envelope at or below 2.8 GB, and its admission
upper at or below 3.5 GB. Only then is the marker written/fsynced and the stage
directory fsynced.

Immediately before rename, an in-process seal—with no subprocess, import, new
thread, or worktree mutation—recomputes the complete source/control/runtime/
module/boot/publisher identities and proves no descendants. It stops/joins the
sampler, requires the publisher to be the only live thread, and takes the exact
final synchronous self-resident/RUSAGE_SELF sample. Every sampler/final-sample
gap is at most one second, the final observed envelope is at most
2,800,000,000 bytes, and the recomputed 25%-margin admission upper is at most
3,500,000,000 bytes. Only the pre-bound no-overwrite rename and terminal-parent
fsync syscalls may follow. Visible final-directory existence is the durable
one-bit attestation that this final seal passed. The JSON reports observations
only through the pre-JSON cutoff; the marker durably extends evidence through
its guard cutoff; neither falsely claims to observe its own later write/rename/
parent fsync. The full close receives a fixed 60-second accounting charge, a
projection convention that is not mislabeled an observed or enforced
post-fsync latency upper.

An intermediate in-process mismatch before publication of the final success
boundary selects the ordinary failure lane. Publication of that final success
boundary or of the cleanup-complete final failure-resume receipt is
non-resumable terminal entry. Any later terminal-pre-JSON or post-JSON Git
failure, seal mismatch, publisher death, sampler/process/wait/RSS failure, or
publication error forbids the selected success/failure, opposite outcome,
Git-check retry, and third preterminal check, but licenses the exact forensic
nonpass close. Because all source paths are disjoint from the three
resource roots, no receipt claims a self-referential post-outcome check. The
declared paths must be clean in the bootstrap, terminal-pre-JSON, and post-JSON
certificate checks. An external write after the final stable read remains
outside the trusted local-process boundary absent an immutable filesystem
snapshot or enforced writer lease.
The generic nonterminal receipt-stage adoption rule does not apply to a
`terminal_entry=true` boundary, just as it does not apply to a dead-publisher
cleanup-complete failure-resume or hidden terminal outcome.

Three nested identities use the same exact snapshot algorithm:

1. the C0015 panel identity is the original seven-path snapshot
   (`src/xid`, the two sealed G2 config/target files, `pyproject.toml`,
   `uv.lock`, `.python-version`, and `Makefile`);
2. the resource executable identity is those seven paths plus
   `configs/g2_resource.toml`; and
3. the resource authority identity is the complete 13-path tuple above.

The fixed seed-1729 rehearsal evidence binds the executable identity. Appending
its measured evidence and quantitative prediction can change only authority
documents, not that executable identity. The registered attempt must match the
rehearsal executable digest exactly and bind the final authority digest. Each
panel manifest retains the original seven-path digest; each outer trace binds
both resource digests plus the exact panel artifact hashes and panel tokens.
All applicable snapshots must be independently clean and stable. No config
contains its own digest.

## 4. Exact address and reservation schedule

The registered address ledger is the unique contiguous sequence
`b = 0, 1, 2, ...`. Before the first draw at `b`, the supervisor durably
publishes:

```text
results/g2_resource_benchmark/reservations/panel-<10-digit b>/
    claim.json
    _SUCCESS
```

using the exact schema in
`GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md`. A claim is valid only when every
lower panel index already has a valid claim. A gap, duplicate, caller-supplied
index, or missing success marker is terminal. Used, partially used, or merely
claimed indices are never reused. Reservation publication is charged to the
following trace and enters the cumulative active clock.

The first claim, `b=0`, belongs to the cold equal-context trace. Thereafter
trace roles consume one claim each in this exact order:

1. thermalization repeats `V, R, R, V`;
2. each of warm blocks 1, 2, and 3 first consumes one `EQUAL` claim;
3. that block then repeats the balanced phase pair order `V, R`, followed by
   `R, V`, until its fixed stop boundary; and
4. the next role takes the next contiguous claim.

One role never spans panels, and one panel never supplies two roles. The
complete ordered reservation inventory and its hash are public evidence. Each
reservation permanently retains the SHA256 of the worker claim that created it.
An interruption may transfer execution authority only through the current
claim's complete contiguous predecessor chain back to that immutable creator
claim. It never rewrites the reservation, equates the dead creator with the
current worker, or permits a claim outside that ancestry to consume the panel.

For one operand-complete block `b`:

### Smooth path

- master seed: `2026071529`;
- stream: `RESOURCE_SMOOTH`;
- phase/scenario: `10/0`;
- `n_dates = 252`;
- `panel_index = b`;
- `date_index = 0..251`;
- DGP components `1..5`, each drawn by the already frozen one-call law;
- target index `16`;
- `paper_recovery = false`;
- `phi = 0.60`;
- reliability `0.95`; and
- DGP `cell_key = 0`, parent slots zero, and replicate index zero.

The block draws bootstrap replicates `0..24` at phase/scenario `40/0`, parent
`10/0`, the same `n_dates` and panel index, `cell_key = date_index = 0`, and
component `6`.

### Paper path

- master seed: `2026071529`;
- stream: `RESOURCE_PAPER`;
- parent phase/scenario: `10/1`;
- `n_dates = 252`;
- `panel_index = b`;
- full-paper date: `date_index = 0`, target 16,
  `paper_recovery = false`;
- recovery date: `date_index = 1`, target 16,
  `paper_recovery = true`;
- both use `phi = 0.60`, reliability `0.95`, and DGP components `1..5`.

Paper bootstrap replicates `0..24` use phase/scenario `40/0`, parent `10/1`,
and the same fixed bootstrap fields. The recovery and research-width cache
fixtures share these weights.

Let `D(s,d,c)` denote the frozen 13-word DGP address for stream `s`, date `d`,
and component `c`, and let `B(s,r)` denote the frozen 13-word bootstrap address
for stream `s` and replicate `r`, always at the current reserved panel. In
15-position record order, every successful trace uses exactly:

```text
position 0:  [D(resource_smooth,d,c)
              for d in 0..251, then c in 1..5]
position 2:  [B(resource_smooth,r) for r in 0..24]
position 10: [D(resource_paper,0,c) for c in 1..5] if units > 0, else []
position 11: [D(resource_paper,1,c) for c in 1..5] if units > 0, else []
position 12: [B(resource_paper,r) for r in 0..24]
             for equal or validation roles, else []
position 13: [B(resource_paper,r) for r in 0..24]
             for research roles, else []
every other position: []
```

The exact successful call-count vectors are:

```text
equal/rehearsal [1260,0,25,0,0,0,0,0,0,0,5,5,25,0,0]
validation      [1260,0,25,0,0,0,0,0,0,0,0,5,25,0,0]
research        [1260,0,25,0,0,0,0,0,0,0,5,0,0,25,0]
```

Call order, successful inventories, and replay copies preserve those sequences
without sorting or deduplication. A zero-unit position instantiates no
generator. There is no data-dependent address choice and no validation or
research coordinate is ever constructed.

## 5. Operand-complete kernel block

The old one-unit bundle is replaced by a fixed block that constructs its own
honest smooth operands and gives the cheap finalizer a clock-resolvable fixed
denominator:

| Kernel | Units per complete block |
| --- | ---: |
| `base_date` | 252 |
| `cell_date` | 252 |
| `bootstrap_moment_aggregation` | 25 |
| `oracle_ridge_fit` | 225 |
| `homogeneous_fit` | 225 |
| `observable_ridge_fit` | 225 |
| `interval_finalize` | 4,096 |
| `null_batch_io_hash` | 1 |
| `base_panel_io_hash` | 1 |
| `cell_io_hash` | 1 |
| `paper_full_date` | 1 |
| `paper_ci_i_recovery_date` | 1 |
| recovery `paper_bootstrap_io` | `25 * 960 * 252 = 6,048,000` |
| research `paper_bootstrap_io` | `25 * 8,460 * 252 = 53,298,000` |
| `success_last_publish` | 1 |

The A024 receipt/execution order is exactly:

```text
k1, k2, k3, k4, k5, k6, k7, k9, k10, k8,
k11, k12, k13-recovery, k13-research, k14
```

Kernels 1 and 2 form one indivisible operand epoch with separate timers and no
intermediate durable boundary. The order of k9, k10, and k8 makes the base
artifact precede the cell artifact and both precede the null-batch manifest
that binds their hashes. Those three kernels have one unit in every role, so
the numeric 15-position unit vectors are unchanged. Kernel identities, not
legacy ordinal positions, control every task, projection, and cross-context
formula.

The 252 smooth dates produce one real issued base panel and one real target-16
cell panel. The 25 actual smooth bootstrap vectors produce 25 issued
aggregates. For each of the three candidates, the block fits every one of the
nine frozen target-16 null-grid reliability nodes, giving
`25 * 9 = 225` fits. Their focal scalar estimates form the actual
`(25, 3, 9)` float64 null-batch payload.

The interval fixture has exactly 499 values:

```text
c = 8 if observable_focals.shape[1] == 9 else 0
x[i] = observable_focals[i % 25, c],
i = 0, ..., 498.
```

`observable_focals` is the loaded read-only k6 resume artifact (or the
byte-identical in-memory value before a boundary), not the k8 null artifact,
which does not yet exist. The fixed fixture is finalized 4,096 times from the
same immutable input.
Every output must be byte-identical. This exercises the complete production
interval/finalization function at clock-resolvable duration but is explicitly
a benchmark fixture, not an inferential output. The frozen phase/task workload
remains one finalization; 4,096 is only the equal-context and cold measurement
denominator.

The first post-worker boundary also publishes the A024 resume-only base/cell
sufficient-statistic state. Later boundaries bind the saved smooth bootstrap
weights and candidate focal arrays required to continue without stochastic
redraw. The first positive kernel-13 position also draws and publishes one
immutable `resource-resume-paper-bootstrap-weights-v1` artifact of shape
`(25,252)`. The last positive kernel-13 position is its sole last consumer and
deletes it through that position's cleanup intent. Producer/last-consumer
positions are `12/13` for equal/rehearsal, `12/12` for validation, and `13/13`
for research; both positive equal variants load the same bytes. The seven
resume-state rows are the base panel, cell panel, smooth bootstrap weights,
oracle/homogeneous/observable focal arrays, and paper bootstrap weights. These
benchmark-only resume leaves are not k9/k10 timing artifacts and are rejected
by every scientific loader.

## 6. Shape fixtures without false provenance

Creating 252 full paper dates per benchmark block would collapse the
one-hour admission experiment into the validation and research workload it is
supposed to project. Faking 252 scientific receipts would be worse. A022
therefore separates computational shape from scientific authority.

Kernel 11 creates one actual issued 8,460-field full-paper date summary.
Kernel 12 creates one actual issued 960-field recovery summary at its distinct
address. Kernel 13 then constructs benchmark-only, finite, little-endian
float64, C-order cache fixtures:

```text
recovery: one payload with shape (252, 960)
research: four payloads with shape (63, 8460)
```

Every row is an exact byte copy of the corresponding loaded one-date summary.
The fixtures carry artifact kind `resource-paper-cache-fixture-v1` and
benchmark coordinates, never `G2DateReceipt`. Validation and research loaders
must reject them before issuance. No fixture uses RNG or can enter an
estimator-result path.

The paper-bootstrap unit includes, inside its timer:

1. fixture expansion and validation;
2. canonical metadata and payload hashing;
3. staged write, file and directory fsync, and success-last publication;
4. reload, rehash, and schema validation;
5. the exact 25-weight matrix multiplication;
6. batch serialization, reload, and hash; and
7. benchmark-fixture cleanup after an immutable receipt.

Charging fixture preparation to every projected batch is conservative because
the real phase constructs its 252-date cache once.

The formerly undefined larger publication is fixed as a
`resource-publication-envelope-v1` with exactly `238,000,000` numeric payload
bytes:

```text
50 shards * 595,000 float64 values * 8 bytes.
```

Each 4,760,000-byte shard remains below the existing 5 MiB per-payload codec
limit. Values are the exact finite float64 global element indices. The
production publisher is constrained to no more payload bytes or payload files
than this envelope. Construction, canonical metadata, hashing, staging,
fsyncs, atomic rename, reload, validation, success-last write, and cleanup are
all inside kernel 14's elapsed time. Kernel 14 additionally publishes,
validates, and deletes one exact 1,048,576-byte
`resource-terminal-close-probe-v1` receipt plus marker through the same
ordinary atomic receipt-directory publisher used for nonterminal receipts. Its
deterministic padding carries no scientific value or authority. It is not a
surrogate for either atomic terminal-outcome directory and supplies no
terminal-publication bound. This separate probe remains necessary because the
envelope artifact uses a different segmented directory publisher.

The publication and paper fixtures bound byte volume and shared code-path cost.
They do not claim to reproduce 252-date scientific heterogeneity. That
limitation remains explicit in Section 15.

## 7. Fixed test-seed measurability falsifier

There is no adaptive microbatch selection. The Section 5 equal/cold counts are
fixed before code:

```text
k3=25
k4=225
k5=225
k6=225
k7=4096
```

After the complete production path exists and before registered access, run
exactly three test-authority rehearsal panels at seed `1729`, panel indices
`10000`, `10001`, and `10002`, in that order. Each panel uses the complete
Section 5 operand construction. For each of `k3..k7`, the contiguous fixed
subblock duration must be at least `100,000,000` nanoseconds in all three
rehearsals. The fixed counts and addresses are already committed in
`configs/g2_resource.toml` before rehearsal. Integer durations, clock identity
and resolution, executable-source/runtime/config digests, and the pass/fail
decision publish success-last under `results/g2_resource_rehearsal/`; they are
never written back into the config. The later append-only quantitative
prediction seal binds that evidence hash.

Every rehearsal also runs the complete one-unit k14
envelope-plus-terminal-close-probe. For its conservative `D_plus`, require:

```text
ceil_div(25 * D_plus, 12) <= 480,000,000,000.
```

The factor `25/12 = (5/3)*(5/4)` applies both the frozen cold-rate derating and
25% margin. All three panels must pass. This falsifies the k14 task projection
only; it supplies no terminal-close latency bound. The separate terminal
accounting charge is fixed independently at 60 seconds.

Each rehearsal panel uses the atomic receipt publisher for one worker-ready
boundary, fourteen work boundaries (k1+k2 share the first), and four
cleanup-intent markers. Across the three panels, the 45 canonical boundary rows
and 12 cleanup-intent rows must satisfy:

```text
chunk_work_elapsed_ns             <= 480,000,000,000
publication_accounting_ns         <=  60,000,000,000
their sum                         <= 540,000,000,000.
```

The boundary leaves remain exactly 45; the 12 cleanup-intent leaves are
additional checkpoints whose post-marker suffix is separately bounded. These
are the 57 capped ordinary checkpoint intervals: measured work is at most
`480,000,000,000` ns, publication accounting is at most `60,000,000,000` ns,
and each interval is at most `540,000,000,000` ns. The complete three-panel
command adds one root terminal accounting row. Its measured pre-JSON work is
at most `480,000,000,000` ns and its fixed accounting charge is exactly
`60,000,000,000` ns, giving an accounted sum at most `540,000,000,000` ns.
The charge is not an observed or enforced upper bound on marker encoding,
final seal, rename, or terminal-parent fsync. Thus the rehearsal has 58
resource-accounting rows—57 capped checkpoint intervals plus one accounting
row—not a 58th work boundary or a 58th observed close interval. These rows
cannot be retried or used to change a kernel count. The rehearsal
also requires bootstrap from the first supervisor instruction through durable
`attempt.json` to finish within `480,000,000,000` ns.

Successful rehearsal evidence retains exactly 13 artifact-kind counts and 51
artifact rows. After the atomic success outcome becomes visible, the rehearsal
checkpoint and scratch roots remain immutable evidence roots; there is no
post-outcome cleanup suffix.

The exact command is `make g2-resource-rehearsal`, submitted once with no
timing retry after its three disjoint roots are proved absent:

```text
results/g2_resource_rehearsal/
data/g2_resource_rehearsal/checkpoints/
data/g2_resource_rehearsal/scratch/
```

Its separately named test-stage entry points require exact
`TestRngNamespace`, seed `1729`, and only panels `10000..10002`; registered
entry points reject its artifacts. Both stages share private production
serialization/validation functions, but no public function accepts a stage,
seed, root, namespace-union, or path override. The registered resource roots
remain absent throughout rehearsal.

Failure is a deterministic design failure. It requires a new append-only
preregistration amendment and hostile review; it cannot select a larger count,
repeat a rehearsal, discard a non-monotone timing, or tune against registered
data. Exact full-task date, artifact, paper, publication, and phase/task
vectors remain the single complete unit or exact vector in Sections 5 and 10.
A registered run may not adapt a count, add a block, change a fixture, or
substitute a private kernel.

## 8. Clock and exact arithmetic

Every timed boundary uses `time.perf_counter_ns()`. Let the reported monotonic
clock resolution, rounded upward to integer nanoseconds, be `h`. For observed
positive integer completed duration `D` and replay count `r`, define

```text
replay_penalty = 480,000,000,000 * r
D_plus = D + 2 h
D_admission = D + replay_penalty
D_admission_plus = D_admission + 2 h.
```

Use the exact aliases

```text
Rplus = D_plus
Aplus = D_admission_plus.
```

`Rplus` is the clock-enclosed successful duration and is legal only on the
predictor/reference side of a relative rate comparison. `Aplus` is the
clock-enclosed replay-penalized duration and is mandatory on the held/current
side of a relative comparison and in every cold, conservative/projected task,
block, phase, combined, and final absolute projection or budget.

The named clock-resolution enclosure is

```text
[max(1, D - 2 h), D + 2 h].
```

For positive integer units `U` and planned work `W`, define

```text
ceil_div(a, b) = (a + b - 1) // b
time_ns(W; U, D_admission_plus) =
    ceil_div(W * D_admission_plus, U)
cold_ns(W; U, D_admission_plus) =
    ceil_div(5 * W * D_admission_plus, 3 * U).
```

`cold_ns` is exactly the time implied by 60% of the measured cold rate.
Python integers and cross multiplication decide every comparison; binary64
rates never decide admission. Raw `D` remains a diagnostic and successful-work
stop clock. Relative rate gates are deliberately one-sided: their
predictor/reference operands use `Rplus`, while their held/current operands use
`Aplus`. Every conservative/projected task, phase, total-budget, and final
admission formula uses `Aplus`; `Rplus` can never relax an absolute
projection. Raw observed successful-work task stops continue to use `D`. The
seed-1729 measurability rehearsal has `r=0`, so its persisted
`duration_plus_ns` is byte-for-byte equal to `admission_duration_plus_ns`;
that zero-replay alias does not license `Rplus` in any registered absolute
projection.

For paper bootstrap, calculate every timing bound separately for the
960-field and 8,460-field variants and use the slower normalized result.

I/O kernels additionally report the following contiguous substages:

1. construction/serialization;
2. hash and prepublication validation;
3. file/directory fsync and atomic publication;
4. reload, hash, schema validation, and any permitted benchmark issuance; and
5. durable receipt plus cleanup.

The combined kernel duration is the exact sum of these substages. Separate
diagnostics therefore cannot omit work from the frozen combined kernel rate.
All inter-kernel orchestration time is charged to the following kernel; final
bundle cleanup is charged to kernel 14. No worker time between startup and the
last receipt is unassigned.

## 9. Thermal and phase-context experiment

The registered run has the following fixed schedule.

### 9.1 Startup

Four fresh zero-work validation subprocesses and four fresh zero-work research
subprocesses run the exact config, seal, source, runtime, and complete
checkpoint-inventory path. They instantiate no validation or research RNG.
For phase `p`,

```text
startup_p = max(startup_p_0, ..., startup_p_3).
```

The final scheduler must generate a deterministic complete phase-coordinate
inventory, and these probes parse and validate that exact inventory rather
than an empty-tree surrogate.

### 9.2 Cold context

One complete Section 5 block in a fresh worker supplies the operational cold
trace. “Cold” means first production-kernel use in that worker with an empty
bytecode-cache prefix; it is not a claim about OS page-cache or ambient
temperature state. It consumes registered panel `b=0`.

### 9.3 Thermalization

After the cold block, consume exact phase roles in the repeating order:

```text
V, R, R, V, V, R, R, V, ...
```

with one new contiguous resource panel per role. Stop only after a complete
four-role cycle and at least `600,000,000,000` nanoseconds of successful
complete post-cold phase-trace time; replay penalties cannot shorten warmup.
Thermalization rates are reported but excluded
from admission. A missing live RSS/process sample, a sampler gap greater than
one second, or an unaccounted descendant while its telemetry owner remains
live is a terminal attempt failure; it cannot be reclassified as an
interrupted thermal epoch. Abrupt supervisor loss or direct boot loss instead
uses A025's `"unknown-loss"` close method, assigns limit-plus-one admission
uppers, and selects terminal failure before another worker, capability, RNG
call, or thermal trace.

Every cold, equal-context, validation-context, and research-context trace that
can supply a rate or comparison operand is rate-bearing from worker-ready
through its complete trace boundary. Any interruption inside that interval
selects ordinary terminal failure. The unfinished trace contributes no
`N/U/Rplus/Aplus/H/X`, minimum, stationarity, temporal, cross-context, or
projection operand; it cannot finish, resume, or receive a replacement panel,
and no later measurement work is legal. Its exact durable prefix survives only
for failure evidence and bounded cleanup. Hence every admission-bearing rate
record has `replay_count=0` and `Rplus=Aplus`; a nonzero replay count on such a
record is terminal failure. Replay-monotonicity fixtures remain mandatory
negative tests, not authority for replayed rate evidence.

An interruption strictly after one complete rate-bearing trace boundary and
before the next rate-bearing worker-ready boundary preserves the completed
evidence but resets thermal qualification. New contiguous panels then follow a
fresh `V,R,R,V` cycle until complete uninterrupted recovery-thermal traces
total at least `600,000,000,000` ns. Those traces do not count toward a
measurement pair or its 200-second minimum. An interruption inside initial or
recovery thermalization discards the entire partial thermal trace, consumes its
address without reuse, and restarts the four-role cycle and 600-second total
from zero after recovery. It contributes no rate evidence. No recovery thermal
work is required when no later warm rate-bearing trace exists.

### 9.4 Three measurement blocks

Exactly three consecutive warm measurement blocks follow. No fourth block may
be added after seeing them. Each block:

1. consumes one `EQUAL` panel and runs one complete fixed Section 5 block;
2. consumes new panels in exact repeated order `V,R,R,V`, which is two
   balanced phase pairs with reversed within-pair order;
3. completes at least two four-role cycles, hence at least four balanced
   validation/research pairs;
4. continues to a complete four-role cycle until successful completed block
   time is at least `200,000,000,000` nanoseconds; replay penalties cannot
   shorten the block; and
5. records per-kernel, per-phase, per-trace, and total integer timings.

The stop decision is evaluated only after a complete four-role cycle. For
measurement block `j`, let `N_j` be its number of complete balanced
validation/research pairs. For scope `s` in `overall`, `validation`, or
`research`, let `Rplus_(j,s)` be the summed `Rplus` duration and
`Aplus_(j,s)` the summed `Aplus` duration of that scope's phase traces,
excluding the `EQUAL` trace. Thermal stationarity requires for blocks 2 and 3:

```text
20 * N_j * Rplus_(j-1,s)
    >= 19 * N_(j-1) * Aplus_(j,s)
for s in {overall, validation, research}.
```

Thus balanced-pair throughput may not degrade by more than 5% sequentially
after the 600-second thermalization. The previous block is a fixed
clock-enclosed reference; replay loss in it cannot enlarge the allowed current
duration. The current block remains replay-penalized. Failure is terminal and
irrevocable; it does not license more warmup, an interruption label, or a
cherry-picked block.

### 9.5 Temporal and core cross-context rate falsifiers

For block `j`, phase `p`, and kernel `k`, define:

```text
U[j,p,k]      = total completed kernel units across phase-p traces in block j
Rplus[j,p,k]  = sum of clock-enclosed successful kernel durations
Aplus[j,p,k]  = sum of replay-penalized clock-enclosed kernel durations
Oplus[j,p]    = sum_k Aplus[j,p,k]
```

Every `U[j,p,k]` required by phase `p` is positive. For held-out block `j`,
let `a,b` be the other two blocks and define the slower same-phase temporal
prediction for the exact held-out unit count:

```text
H[j,p,k] = max(
    ceil_div(U[j,p,k] * Rplus[a,p,k], U[a,p,k]),
    ceil_div(U[j,p,k] * Rplus[b,p,k], U[b,p,k])
)
H[j,p] = sum_{k: U[j,p,k] > 0} H[j,p,k].
```

Zero-unit positions contribute exactly zero and are never used as
denominators.

The same-context temporal-rate check passes only if, for both phases and all
three held-out blocks:

```text
Oplus[j,p] <= ceil_div(5 * H[j,p], 4).
```

The equal-context trace is excluded. This exact normalization remains valid
when blocks contain different pair counts.

This is blocked leave-one-warm-block-out temporal prediction, not an in-sample
refit. Failure rejects the conditional additive projection and terminates
A022.

The common cross-context positions are:

```text
C = {1,2,3,4,5,6,7,8,9,10,14}.
```

For a held-out phase `p`, let `q` be the other phase. For every `k in C`,
define the cross-phase prediction from the other two blocks:

```text
X[j,p,k] = max(
    ceil_div(U[j,p,k] * Rplus[a,q,k], U[a,q,k]),
    ceil_div(U[j,p,k] * Rplus[b,q,k], U[b,q,k])
).
```

Every denominator is positive by construction. Both the per-kernel and
core-aggregate checks must pass:

```text
Aplus[j,p,k] <= ceil_div(5 * X[j,p,k], 4)       for every k in C
sum_{k in C} Aplus[j,p,k]
    <= ceil_div(5 * sum_{k in C} X[j,p,k], 4).
```

This is a genuine cross-context rate stress between two distinct phase
mixtures. Kernels 11, 12, and both variants of kernel 13 remain outside it and
are governed by cold, equal, and own-phase slowest-context rates. Neither
falsifier proves linear scaling to `W` or equivalence to the realized full
phase mixture.

The stationarity, temporal, and cross-context checks are replay-monotone. With
raw durations, units, and clock resolutions fixed, increasing any replay count
leaves every `Rplus` reference, `H`, and `X` unchanged; it can only weakly
increase affected held/current `Aplus` operands and absolute projections. No
acceptance Boolean may change from false to true.

The original last-three complete equal-context aggregate is still reported as
a diagnostic. It cannot override any cold, stationarity, temporal,
cross-context, or slowest-block failure.

## 10. Exact phase traces and task vectors

One validation phase-context trace is:

| Kernel | Units |
| --- | ---: |
| base date | 252 |
| cell date | 252 |
| bootstrap aggregation | 25 |
| oracle fit | 225 |
| homogeneous fit | 225 |
| observable fit | 225 |
| interval finalization | 1 |
| null-batch I/O | 1 |
| base-panel I/O | 1 |
| cell-panel I/O | 1 |
| full paper date | 0 |
| `CI_I` recovery date | 1 |
| paper-bootstrap terms | 6,048,000 |
| publication | 1 |

One research phase-context trace is:

| Kernel | Units |
| --- | ---: |
| base date | 252 |
| cell date | 252 |
| bootstrap aggregation | 25 |
| oracle fit | 25 |
| homogeneous fit | 25 |
| observable fit | 25 |
| interval finalization | 1 |
| null-batch I/O | 1 |
| base-panel I/O | 1 |
| cell-panel I/O | 1 |
| full paper date | 1 |
| `CI_I` recovery date | 0 |
| paper-bootstrap terms | 53,298,000 |
| publication | 1 |

Both traces use the 238,000,000-byte publication envelope. These are bounded
cross-context resource probes, not `W`-proportional traces or replacements for
the frozen full phase work totals. Their fixed fit counts also preserve the
null-batch artifact atoms: validation emits `25 * 3 * 9 = 675` focal values,
while research emits `25 * 3 * 1 = 75` before its explicitly benchmark-only
nine-node fill.

The 480-second task matrix is:

| Task | Exact kernel vector |
| --- | --- |
| Base panel | `k1=252, k9=1` |
| Cell panel | `k2=252, k10=1` |
| Largest null smooth batch | `k3=25, k4=225, k5=225, k6=225, k8=1` |
| Research smooth batch | `k3=25, k4=25, k5=25, k6=25, k8=1` |
| Full paper date | `k11=1` |
| `CI_I` recovery date | `k12=1` |
| Recovery paper batch | `k13=6,048,000` |
| Research paper batch | `k13=53,298,000` |
| Scalar finalization | `k7=1` |
| Larger success publication | `k14=1` |

Both the largest observed task duration and its conservative projected duration
after the 1.25 multiplier must be at most `480,000,000,000` nanoseconds.

## 11. Admission rates and projections

For phase `p`, kernel `k != 13`, and full frozen phase work `W[p,k]`, every
context supplies a positive integer unit count and replay-penalized
conservative summed duration. Let `U[c,k],Aplus[c,k]` denote cold or
equal-context units/admission duration, and retain
`U[j,p,k],Aplus[j,p,k]` from Section 9 for
phase-context block `j`. Compute:

```text
E[p,k] = max(
    ceil_div(5 * W[p,k] * Aplus[cold,k], 3 * U[cold,k]),
    ceil_div(W[p,k] * Aplus[equal_1,k], U[equal_1,k]),
    ceil_div(W[p,k] * Aplus[equal_2,k], U[equal_2,k]),
    ceil_div(W[p,k] * Aplus[equal_3,k], U[equal_3,k]),
    ceil_div(W[p,k] * Aplus[1,p,k], U[1,p,k]),
    ceil_div(W[p,k] * Aplus[2,p,k], U[2,p,k]),
    ceil_div(W[p,k] * Aplus[3,p,k], U[3,p,k])
).
```

Terms with `W[p,k] = 0` are exactly zero. Every other term must have positive
units and elapsed time in every context required by its phase.

Kernel 13 retains the frozen common slower-variant rule rather than choosing
the phase's favorable width. Let variants `v` be `recovery` and `research`.
The eligible contexts are cold, all three equal blocks, all three validation
blocks for the recovery variant, and all three research blocks for the
research variant. For either phase:

```text
E[p,13] = max over both variants and their eligible contexts of
    ceil_div(W[p,13] * Aplus[context,variant],
             U[context,variant])
```

with `5/3` applied inside `ceil_div` for each cold-variant term. Thus the
slower normalized 960-/8,460-field rate governs both phase projections.

The phase projection is:

```text
raw_p = startup_p + sum_{k=1..14} E[p,k]
T_hat_p = ceil_div(5 * raw_p, 4).
```

This is more conservative than taking one aggregate last-three rate: it uses
the slowest observed admissible context for every phase/kernel pair and then
adds the frozen 25% time margin.

The multiplication from each measured `U` to `W` is a conditional per-kernel
linear extrapolation. Section 9's temporal and cross-context checks can
falsify observed rate instability, but cannot prove that scaling or reproduce
the realized full-workload mixture. Passage therefore leaves the corresponding
assumption open rather than relabeling it measured.

The required block-specific diagnostic is also exact. For block `j` and
`k != 13`, replace the seven-way maximum in `E[p,k]` by the maximum of only
the cold term, `equal_j`, and phase context `(j,p)`:

```text
E_block[j,p,k] = max(
    ceil_div(5 * W[p,k] * Aplus[cold,k], 3 * U[cold,k]),
    ceil_div(W[p,k] * Aplus[equal_j,k], U[equal_j,k]),
    ceil_div(W[p,k] * Aplus[j,p,k], U[j,p,k])
)

raw_block[j,p] = startup_p + sum_{k=1..14} E_block[j,p,k]
upper_block[j,p] = ceil_div(5 * raw_block[j,p], 4).
```

For kernel 13, `E_block[j,p,13]` is the maximum of six normalized terms:
cold recovery and research with `5/3` derating, equal-block `j` recovery and
research, validation-block `j` recovery, and research-block `j` research,
each scaled to `W[p,13]`. Terms with zero frozen work remain zero. The three
diagnostics cannot replace the final seven-context slowest projection.

Task admission uses the same 15-position kernel/variant order and is not an
unreported maximum. Let `A[a,l]` be task `a`'s exact vector from Section 10
and let context `c` be admissible for that task only when
`U[c,l] > 0` for every `A[a,l] > 0`. Let `D[c,l]` be the corresponding raw
completed duration and `Aplus[c,l]` its replay-penalized conservative
duration. For every cold, equal-block, and applicable phase-block context,
compute:

```text
task_observed[c,a] =
    sum_{l:A[a,l]>0} ceil_div(A[a,l] * D[c,l], U[c,l])

task_plus[c,a] =
    sum_{l:A[a,l]>0} ceil_div(A[a,l] * Aplus[c,l], U[c,l])

task_cold_plus[a] =
    sum_{l:A[a,l]>0}
        ceil_div(5 * A[a,l] * Aplus[cold,l], 3 * U[cold,l])

task_observed_max[a] =
    max_c task_observed[c,a]

task_projected_upper[a] =
    ceil_div(5 * max(
        task_cold_plus[a],
        max_{c != cold} task_plus[c,a]
    ), 4).
```

The 960-field and 8,460-field kernel-13 positions are distinct throughout.
The registered result reports every context contribution and both maxima for
all ten named tasks. For each task, both `task_observed_max` and
`task_projected_upper` must be at most `480,000,000,000` ns; the two public
global maxima are derived from those ten auditable rows.

This rule is intentionally severe: one abrupt lost execution in a positive-
unit task normally makes its replay-penalized projected upper fail. Resume
still preserves and closes the one logical attempt, but it cannot turn an
unobserved partial execution into a favorable positive admission. A clean
signal honored at a completed kernel boundary has zero replay penalty.

Terminal close is non-self-referential and independent of kernel 14. From the
last durable boundary through process waits, resource scans, aggregation, and
the cutoff immediately before terminal JSON encoding, active work is at most
`480,000,000,000` ns. The complete success or failure outcome publication
includes hidden-stage creation and parent fsync, JSON write/fsync, the
post-JSON Git certificate and child/rusage/output inventory, marker
write/fsync, stage-directory fsync, final in-process seal, sampler shutdown,
no-overwrite rename, and terminal-parent fsync. Because no local receipt can
self-attest that complete suffix's latency, it receives one fixed accounting
charge:

```text
terminal_close_method = "fixed-terminal-accounting-charge-v1"
terminal_close_accounting_charge_ns = 60,000,000,000
terminal_accounted_interval_ns =
    terminal_chunk_work_elapsed_ns
    + terminal_close_accounting_charge_ns
resource_accounted_charge_ns =
    cumulative_active_to_cutoff_ns
    + terminal_close_accounting_charge_ns.
```

The success publisher uses only
`terminal/.success.xid-g2-terminal-stage-v1/` and the final
`terminal/success/{result.json,_SUCCESS}` directory; the failure publisher uses
the corresponding `.failure` stage and
`terminal/failure/{failure.json,_FAILURE}` final. Both child files and the
stage directory are fsynced before the final in-process seal and no-overwrite
directory rename, and the terminal parent is fsynced afterward. The terminal
JSON reports the preterminal cutoff and fixed charge; the marker separately
reports the post-JSON Git/process/RSS certificate. Visible-directory existence
attests the later final seal. None claims an observation after its own write or
the final parent fsync, and the charge is not an end-to-end close-time bound.

Kernel 14 continues to measure its 50-shard, 238,000,000-byte publication
envelope and ordinary maximum-size receipt-directory probe, but it supplies no
terminal-close bound. On failure, cleanup is first closed by the mandatory
final failure-resume receipt; deterministic failure-JSON encoding and atomic
outcome-directory publication then receive the same fixed 60-second accounting
charge and cannot reopen work.

The registered result must report:

- the clock-resolution rate enclosure for every timing;
- the non-probabilistic min--max range across the three warm blocks;
- the three block-specific phase-projection values;
- the three held-out predictive ratios for each phase; and
- the final conservative upper projection.

Three serial thermal blocks do not justify a probabilistic confidence
interval. Calling their range a confidence interval is forbidden.

## 12. RSS, disk, registries, and process rules

Only one thermally heavy worker may exist. Timed numerical kernels may not
spawn descendants or use hidden numerical threads. All six frozen numerical
thread variables equal `1` before NumPy import, and process/thread counts enter
runtime evidence.

Process-tree RSS is sampled every 50 ms. Process identity is the pair of PID
and kernel-reported start time from Darwin
`proc_pidinfo(PROC_PIDTBSDINFO)`; PID alone is never an identity. The attempt
also binds the initial supervisor's PID/start identity and boot-identity
digest. The supervisor inventories every descendant at every sample, records
its start identity and instantaneous resident bytes, and reaps every direct
child with `wait4` so exit status and child `ru_maxrss` cannot disappear with a
short-lived or killed process. On registered Darwin, `ru_maxrss` is
interpreted as bytes without multiplication. Workers are serial; kernel 14's
receipt probe is work inside its ordinary worker, not a distinct child role.
Every claimed-worker `wait4` result enters this exact cumulative hash-bound
row:

```text
[worker_index, worker_claim_sha256, pid, process_start_identity,
 boot_identity_sha256, post_wait_perf_counter_ns,
 wait_status, ru_maxrss_bytes, watchdog_arm_kind, watchdog_arm_sha256,
 work_deadline_perf_counter_ns, reap_deadline_perf_counter_ns,
 termination_reason, termination_requested_perf_counter_ns]
```

`watchdog_arm_kind` is `"worker-launch-intent"`, `"boundary"`,
`"cleanup-intent"`, or `"interruption"` and the digest hashes the exact durable
receipt that armed those two deadlines before further worker work. A normal
exit uses `termination_reason="worker-exit"` and a null termination-request
time. A timeout uses `termination_reason="work-timeout"`, requires a nonnull
request time not later than the precommitted work deadline, and is reaped no
later than the distinct precommitted reap deadline. The post-wait sample is
taken immediately after the exact-PID `wait4` return and is not later than that
reap deadline. Raw `wait_status` is a signed 32-bit integer and
`ru_maxrss_bytes` is nonnegative. Rows are strictly ordered by worker index,
with no omitted or duplicate reaped worker, and each exact CJSON row including
terminal LF is at most 512 bytes. No deadline first observed in this wait row,
copied from a later clock, or recomputed from the wait time is valid.

Every cumulative `worker_waits` object has exactly:

```text
count rows sha256
```

Here `count=len(rows)` and:

```text
sha256 =
SHA256(CJSON([
  "xid-g2-resource-worker-wait-inventory-v1",
  rows,
]))
```

Each later inventory preserves every earlier durable row as an exact prefix and
appends only newly reaped workers. A worker closed only by double absence or
boot change has no invented wait row.

Every preterminal Git child also has
an exact output/wait/rusage row. The bootstrap rows are available at every
cutoff; the terminal-pre-JSON rows join only at the terminal cutoff. Define
`preterminal_git_rusage_highwater_bytes` as the maximum byte-normalized
`ru_maxrss` over the complete Git rows available at that cutoff. The observed
resource RSS envelope `O_R` is the maximum of:

1. every sampled simultaneous process-tree total; and
2. the supervisor high water plus the larger of the maximum `ru_maxrss` over
   the serial worker-wait inventory, or zero for an empty inventory, and
   `preterminal_git_rusage_highwater_bytes`.

The scalar and its exact child rows reconstruct from
`attempt.bootstrap_git_check` at ordinary cutoffs and from that object plus
`terminal_json.preterminal_git_checks.terminal_pre_json_check` at the terminal
cutoff. The post-JSON Git-child high-water belongs only to the marker's
publication envelope and is not inserted retroactively into terminal JSON.

For an exact Darwin identity query, the caller zeroes the complete
`proc_bsdinfo` buffer, clears `errno`, calls
`proc_pidinfo(pid,PROC_PIDTBSDINFO,0,...)`, and samples
`perf_counter_ns` immediately afterward. A double-absence proof stores the
compact, lossless factorization:

```text
[verdict, observed_pid_or_null, observed_start_identity_or_null,
 [[first_perf_counter_ns, first_return_bytes, first_errno_value],
  [second_perf_counter_ns, second_return_bytes, second_errno_value]]]
```

The verdict and optional decoded replacement identity are common to both raw
samples; expanding them into either sample reconstructs the two raw syscall
observations exactly. This factorization is mandatory because duplicating a
maximum-width replacement identity can exceed the 512-byte death-row cap. The
byte-authoritative Darwin truth table is:

| Return and errno | Valid decoded identity | Verdict | Effect |
| --- | --- | --- | --- |
| exact `sizeof(proc_bsdinfo)`, zero | expected PID/start | `"present-target"` | reject death proof |
| exact size, zero | same PID, different valid start | `"absent-pid-reused"` | admissible absence class |
| zero, `ESRCH` | both identity fields null and buffer still zero | `"absent-esrch"` | admissible absence class |
| zero with any other errno, including zero, `EPERM`, or `EACCES` | any | `"query-error"` | terminal |
| short positive, oversize, negative, malformed struct, or PID mismatch | any | `"query-error"` | terminal |

Both observations use the unchanged current boot and satisfy
`first+50000000 <= second <= first+1000000000`. They must have the same
admissible verdict. For `"absent-esrch"`, both common identity fields are null,
both returns are zero, and both errno values are `ESRCH`. For
`"absent-pid-reused"`, the common PID equals the queried PID, the common start
identity is valid and differs from the target, both returns equal
`sizeof(proc_bsdinfo)`, and both errno values are zero. Mixed ESRCH/reuse,
changing replacement identity, a present target, permission failure,
ABI/short-read failure, or ambiguous zero/zero return fails closed.

Every process-death row has exact order:

```text
[role, pid, process_start_identity, old_boot_identity_sha256, method,
 first_check_perf_counter_ns, second_check_perf_counter_ns,
 wait_status, ru_maxrss_bytes, watchdog_arm_kind, watchdog_arm_sha256,
 work_deadline_perf_counter_ns, reap_deadline_perf_counter_ns,
 absence_observations]
```

and uses only `wait4-reaped`, `double-process-identity-absence`, or
`boot-identity-changed`. Nullable fields are exact:

| Method | Role | First check | Second check | Wait/status/rusage | Arm/deadlines | Absence observations |
| --- | --- | --- | --- | --- | --- | --- |
| `wait4-reaped` | worker only | nonnull, immediately post-`wait4` | null | exact signed status and nonnull byte-normalized `ru_maxrss` | exact nonnull persisted arm kind/digest/work/reap values | null |
| `double-process-identity-absence` | supervisor or worker | nonnull | nonnull | both null | all four null | exact factorized two-sample array |
| `boot-identity-changed` | supervisor or worker | null | null | both null | all four null | null |

For an exact worker-wait row `W`, the
`wait4-reaped` death row is:

```text
["worker", W[2], W[3], W[4], "wait4-reaped",
 W[5], null, W[6], W[7], W[8], W[9], W[10], W[11], null]
```

Thus it binds the same post-wait sample, signed status, byte-normalized
`ru_maxrss`, arm receipt, work deadline, and reap deadline. Double absence has
nonnull first and second check times equal to the factorized observation
timestamps, null wait/rusage/arm/deadline fields, and the exact nonnull
four-field observation array. Boot change requires unequal boot digests and
has every field after `method` null. Per-method nullability and ordering are
byte-authoritative.

The sole wait4 exception is a complete visible worker birth whose worker claim
was never published. Its exact `wait4-reaped` death row joins the birth
identity, uses the launch intent's persisted arm kind/digest/deadlines, and
carries the actual post-wait/status/rusage values in the same positions, but
there is no invented worker-wait row or worker-claim digest. This exception can
close only terminal failure; `all_wait_statuses_collected` remains false. A
birth-only child not closed by this row or another admissible death method
blocks failure publication.

Every `process_deaths` object has exactly:

```text
schema_version rows sha256
```

Here `schema_version=1`, rows are ordered by role `"supervisor"` before
`"worker"` and then ascending PID/start identity, and:

```text
sha256 =
SHA256(CJSON([
  "xid-g2-resource-process-death-set-v1",
  rows,
]))
```

Every row joins its `(role,pid,process_start_identity)` to the unique
authoritative attempt, worker birth, worker claim, interruption,
failure-intent, or failure-resume record that last encoded the identity, and
its old-boot digest equals that record. Same-boot wait4/double-absence rows
require old boot equal to the enclosing current boot; boot-change rows require
inequality. No caller-supplied or merely well-formed boot digest can satisfy
the join.

Interruption, failure-intent, and failure-resume chains prove each superseded
supervisor or worker exactly once. A complete visible birth makes the child
identity durable and requires an eventual exact wait/death proof even when no
worker claim followed. Git check children are wait-only; a missing Git
wait/rusage row is forensically incomplete and cannot be replaced by one of
these worker death proofs.

The second RSS term protects the gate against a sub-50-ms worker spike. Only a
durably closed process segment can preserve favorable telemetry: a live
supervisor closes a worker-loss segment only after continuous sampling,
`wait4`/rusage collection, and a final disk scan; a cross-boot successor may
carry that segment only through its already durable clean-exit interruption
receipt. On a fresh attempt let `C_R=0`; on a closed-segment resume let `C_R`
be the latest complete boundary receipt's `rss_admission_upper_bytes`. Define:

```text
M_R = ceil_div(5 * O_R, 4)
A_R = max(C_R, M_R).
```

Admission requires `O_R <= 3,500,000,000` and
`A_R <= 3,500,000,000` bytes. The current 25% margin is applied only to
actual observed telemetry; a carried conservative upper is never multiplied
again or relabeled observed. `O_R` covers durable observed telemetry from all
completed epochs plus the current epoch through the preterminal accounting
cutoff. No field is described as an RSS sample taken after its own outcome
directory became visible.

Abrupt supervisor loss or direct boot loss has predecessor-close method
`"unknown-loss"` rather than a closed segment. It increments the lost-telemetry
epoch count and assigns admission uppers strictly above every affected limit:

```text
rss_admission_upper_bytes                  = 3,500,000,001
checkpoint_tree_admission_upper_bytes      = 2,000,000,001
created_roots_admission_upper_bytes        = 6,000,000,001
absolute_workspace_admission_upper_bytes  = 30,000,000,001.
```

Those values are bounds, never samples, and select terminal failure
`"select-terminal-failure-telemetry-gap"` before another worker, capability,
RNG call, or thermal trace.

The authoritative checkpoint-tree cap is the configured decimal
`2,000,000,000` bytes. The generic codec ceiling cannot widen it. At every
mutation, measure logical `st_size` and allocated `st_blocks * 512`, reserve
staging/metadata/directory/rename slack first, and reject before mutation
unless the complete reserved active tree is at most `1,600,000,000` bytes.
Admission additionally requires the same 25% headroom:

```text
ceil_div(5 * active_tree_high_water, 4) <= 2,000,000,000.
```

Before `attempt.json`, all three resource roots must be absent and the
supervisor measures the worktree baseline `B0`, excluding those absent roots,
as the larger of recursively summed logical `st_size` and allocated
`st_blocks * 512`. Every resource mutation boundary—including staging writes,
temporary files, fsync/rename, receipts, retained exemplars, cleanup, Python
bytecode, and the preterminal accounting cutoff—rescans all three resource
roots. Let `R_t` be the larger of their combined logical and allocated totals
at boundary `t`. All `TMPDIR`, Python bytecode, cache, and result staging
paths are predeclared descendants of the scratch or result root. Any
G2-created write outside the three roots is terminal.

Terminal result/failure publication cannot report a scan taken after its own
outcome directory. Let `g` be the maximum recorded `statvfs` allocation unit
across the three roots. The exact JSON and binding marker are each capped at
1,048,576 bytes. The atomic publisher reserves the unique hidden outcome stage,
its two children, the final directory entry, and terminal-parent growth before
encoding. The no-overwrite directory rename moves the same complete entries
and never duplicates their file payload. Define the precommitted close
reservation:

```text
R_close = 2 * 1,048,576 + 16 * g.
R_close_upper = R_cutoff + R_close.
C_D = latest complete boundary created_roots_resume_upper_bytes, or zero.
R_admission_upper = max(C_D, max_t R_t, R_close_upper).
```

The 16 allocation units conservatively cover the hidden stage, terminal and
final-directory entries, both child entries, parent growth, and allocation
rounding. The publisher must fail before encoding if its exact
path/file/byte grammar exceeds this reservation. The result reports `C_D`,
`max_t R_t`, `R_cutoff`, `R_close`, `R_close_upper`, and
`R_admission_upper`; it never labels a carried conservative upper or
prepublication scan as observed terminal telemetry.

File-space reservation does not substitute for canonical-schema fit. Before
implementation, the frozen deterministic maximum-fixture generator constructs
maximum-width exact CJSON, including terminal LF, for all nine artifact
families below. Because `result.json` and `failure.json` each have distinct
rehearsal and registered schemas, the digest binds eleven schema fixtures:

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

Each applicable fixture uses every reachable maximum rather than an average
case: 64 worker waits, 128 factorized process-death rows, 512 cleanup rows, 641
failure resumes, 240-byte paths, maximum integer and bounded-string widths,
all source/control rows, 24 preterminal Git rows, 12 post-JSON Git rows, and
1,201 terminal-publication RSS samples. Every exact file must fit the
1,048,576-byte per-file cap, and a deterministic one-past mutation of every
bounded vector, row, string, or path dimension must fail before file or stage
creation. Passing one shape cannot substitute for another.

The frozen fixture-schema digest is exactly:

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

The vector binds, in order, maximum worker waits, process deaths, cleanup rows,
failure resumes, path bytes, preterminal Git rows, post-JSON Git rows, and
publication-RSS samples. The final success boundary and cleanup-complete final
failure resume persist the applicable runtime `terminal_size_preflight`, which
has exactly:

```text
schema_version terminal_kind cap_bytes fixture_schema_sha256
file_upper_rows passed
```

For success, `terminal_kind="rehearsal-success"` when
`authority_stage="test-rehearsal"` and `"registered-success"` when
`authority_stage="registered-resource"`; `file_upper_rows` is exactly:

```text
[["terminal/success/result.json", result_upper_bytes],
 ["terminal/success/_SUCCESS", success_marker_upper_bytes]]
```

For failure, `terminal_kind="rehearsal-failure"` or
`"registered-failure"` under the same authority-stage mapping, and
`file_upper_rows` is exactly:

```text
[["terminal/failure/failure.json", failure_upper_bytes],
 ["terminal/failure/_FAILURE", failure_marker_upper_bytes]]
```

`schema_version=1`, `cap_bytes=1048576`, and each upper is the exact selected
schema's production-CJSON maximum after substituting the current attempt's
already bounded category counts and admitted maxima for every still-unknown
field. `passed` is true iff every row upper is at most the cap and the
implementation reproduced the frozen fixture digest. The publisher also checks
the exact selected bytes before each write. A malformed, missing, stale, or
failing success preflight cannot produce `terminal_entry=true`; it leaves the
boundary ordinary, launches no successor work, and selects terminal failure.
After failure selection, an unprovable failure preflight stops before the final
resume or terminal-stage mutation as forensically incomplete. No terminal
entry may rely on truncation, compression, field omission, or a later size
check.

The exact decimal constraints are:

```text
R_admission_upper <= 6,000,000,000
B0 + R_admission_upper <= 30,000,000,000
B0 + R_close_upper <= 25,000,000,000.
```

The first is the G2-created transient allowance, the second is absolute
transient project disk, and the third is steady-state project disk. Crash
restart carries only the latest durably closed conservative boundary upper;
deletion cannot reset it, and that carried value is not called an observed
scan. Unknown-loss uses the limit-plus-one values above and therefore cannot
preserve admission.
Resource artifacts contain no external download.

A missing live sample, sampler death, PID/start mismatch, un-reaped child,
unaccounted descendant, or filesystem-accounting gap while the attempt is
active under a live telemetry owner is terminal. It cannot be repaired by
discarding the epoch. Loss of the telemetry owner or boot follows the distinct
fail-closed unknown-loss branch above.

The following nine live weak-registry counts are recorded before each block,
at their retained-object high water, after explicit object release, and after
charged forced GC:

```text
_RAW_BASE_REGISTRY
_G2_DATE_REGISTRY
_CONTRACT_DESIGN_REGISTRY
_CONTRACT_BASE_DATE_REGISTRY
_CONTRACT_CELL_DATE_REGISTRY
_CONTRACT_BASE_PANEL_REGISTRY
_CONTRACT_CELL_PANEL_REGISTRY
_CONTRACT_AGGREGATE_REGISTRY
_RESOURCE_ARTIFACT_REGISTRY
```

After release and charged GC, every count must equal its exact pre-block
baseline. Cleanup that passes only under an untimed diagnostic GC fails.

## 13. Artifact schemas and lifecycle

`docs/derivations/GATE_G2_RESOURCE_ARTIFACT_AUTHORITY.md` is the sole
byte-level authority for every new file. It freezes canonical JSON key sets and
types, path derivation, payload order, dtypes, shapes, byte counts, digest
namespaces, address/completion domains, loader permissions, and success-last
lifecycle before implementation. This document freezes only their scientific
roles and required inventory.

The already licensed checkpoint kinds remain exactly `base-panel` and
`cell-panel`; their byte schema, kind strings, final paths, digest formulas,
and weak-issuance semantics are reused unchanged. A022 does not rename or wrap
them as resource artifacts. The C0015 test-authority entry points remain
unchanged and continue to accept only exact `TestRngNamespace` test authority.
Separately derived resource-stage writer/loader entry points accept only exact
`ResourceRngNamespace` authority, preserve the same panel bytes, and bind the
outer attempt through the containing trace receipt. No subclass, boolean
bypass, or generic registrar is permitted. The new artifact kinds are:

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

The separate canonical-JSON receipt kinds are:

```text
resource-panel-reservation-v1
resource-worker-launch-intent-v1
resource-worker-birth-v1
resource-worker-claim-v1
resource-resume-boundary-v1
resource-interruption-receipt-v1
resource-cleanup-intent-v1
resource-trace-receipt-v1
resource-measurement-block-v1
resource-terminal-close-probe-v1
resource-terminal-failure-intent-v1
resource-terminal-failure-resume-v1
```

Every payload artifact has canonical metadata, exact
source/runtime/config/attempt hashes, an exact address or benchmark-coordinate
domain, payload descriptors, SHA256 values, and logical/allocated sizes.
Every receipt has its separately frozen exact JSON keys, provenance and
applicable telemetry. Both classes use their own exclusive success-last
state machine. The existing 5 MiB per-payload ceiling remains; canonical JSON
receipts retain their 1,048,576-byte cap. Larger payload objects are segmented
as specified in Section 6. The complete active tree always uses the stricter
decimal cap.

Every trace retains exact path/kind/hash inventory rows in its immutable
kernel boundaries and trace receipt, including the complete cold block and
every warm block. Payload bytes are deliberately ephemeral. Immediately
before a timed last-use deletion, an immutable cleanup-intent receipt binds
the completed successful-work evidence, immutable logical targets, and the
complete child-before-parent filesystem-entry sequence. Each entry row is

```text
[entry_index, target_index, repository_relative_path, entry_type, mode,
 evidence_logical_bytes_or_null, evidence_allocated_bytes_or_null,
 content_sha256_or_null, validation_sha256]
```

Entry indices are contiguous in deletion order. Regular-file rows bind exact
mode, logical/allocated bytes, content SHA256, and the authority's stable
validation digest. Directory rows bind exact type, mode, and directory
validation digest and use null byte/hash fields, so deleting one child cannot
invalidate its surviving parent row. A cleanup filesystem is legal only when
one exact row prefix is absent, the complete suffix validates, and no extra
path exists. Deletion and parent-fsync time remain inside the originating
combined kernel; an interruption can finish only the journaled suffix. Debris
uses the same immutable targets and entry rows plus a monotone completed-prefix
count and remaining-suffix digest.
Chained interruptions copy the target/row bytes but advance those progress
fields from the actual filesystem rather than copying stale progress.
Artifact finals bind their exact artifact SHA256 and receipt finals bind the
receipt-final domain digest. The terminal inventory is independently
reproducible from durable row commitments, but deleted payloads are not
claimed to remain re-readable. Scientific validation/research checkpoints are
not covered by this ephemeral-fixture rule.

The resource supervisor holds exclusive ownership across each panel mutation
and pre-reserves the complete staged mutation against both the
`1,600,000,000`-byte pre-margin admission ceiling and decimal
`2,000,000,000`-byte tree cap before entering the shared panel serializer.
The generic `2 * 1024**3` codec ceiling is only an additional check and cannot
widen this outer bound. A valid immutable panel may be loaded and reused on a
permitted resume; an invalid, partial, or conflicting final path is terminal
and is never regenerated in place.

Ordinary-work resume is allowed only when neither final terminal outcome
directory exists, neither hidden terminal stage is present, and the prior
process left a complete Section 16 boundary or a cleanup intent whose
predecessor is that boundary. A valid hidden outcome stage is handled only by
the terminal-cutover rule: the same live publisher may finish it, an exact
visible final is reusable, and a dead-publisher hidden stage is forensically
incomplete. It never authorizes ordinary work. A canonical no-interruption trace, including every rehearsal, publishes
a boundary after initial worker readiness, after the indivisible k1+k2 epoch,
and after each of the remaining 13 positions (including zero-unit positions).
Its exact next-position sequence is
`[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15]`. Registered execution also publishes a
prefix-copying worker-ready boundary after each permitted partial-trace
interruption, plus a boundary after every trace receipt and measurement
receipt. Extra resume leaves do not alter the canonical sequence or rehearsal
counts. A trace may therefore have one exact durable kernel prefix and a
measurement block may contain an exact completed measurement-role subsequence.
Neither state is discarded.

Every launch intent that can license worker work carries `watchdog_arm`; every
later boundary, cleanup-intent, or interruption that can precede more worker
work carries a newly derived `next_watchdog_arm`. Both names carry exactly:

```text
armed_perf_counter_ns work_limit_ns work_deadline_perf_counter_ns
reap_grace_ns reap_deadline_perf_counter_ns
```

`work_limit_ns=480000000000`, `reap_grace_ns=60000000000`,
`work_deadline_perf_counter_ns=armed_perf_counter_ns+work_limit_ns`, and
`reap_deadline_perf_counter_ns=work_deadline_perf_counter_ns+reap_grace_ns`.
The arm is derived before encoding its receipt, and worker work gated by it may
begin only after the arm-bearing receipt and marker are durable. It becomes the
only active arm at that point; a later clock cannot recompute or extend it.
Counting publication against the precommitted deadline is deliberately
conservative. A `terminal_entry=true` boundary has
`next_watchdog_arm=null`; the cleanup-complete final failure resume licenses no
later worker work. The worker claim copies its launch intent's object
byte-for-byte as `initial_watchdog_arm`, and every worker wait/death projection
names the latest durable arm that governed that child when it exited or was
terminated.

The hard checkpoint clock starts when the predecessor boundary marker is
complete. Work through the next cutoff must be at most 480 seconds, including
the combined k1+k2 epoch, and atomic boundary publication has a separate
60-second upper, so every active interval between durable markers is at most
540 seconds, strictly below the repository's ten-minute lost-work ceiling. A
480-second work timeout is terminal; an indivisible epoch or position is not
retried forever. Receipt-stage normalization below determines whether loss
during publication returns to the predecessor or completes the unique receipt.
Loss after a cleanup intent continues only its exact deletion and
boundary-publication suffix.
Bootstrap from the first supervisor instruction through durable
`attempt.json` has its own 480-second watchdog, so work before boundary zero
cannot become an unbounded loss interval.

An admitted ordinary-work interruption is exactly one of:

1. a supervisor-recorded `SIGTERM`, `SIGINT`, or `SIGHUP` latched at a kernel
   boundary after the live supervisor durably closes telemetry;
2. exact same-boot proof by the live supervisor that the prior worker
   PID/start identity is dead through collected `wait4` status or two ordered
   kernel-identity absences while telemetry is continuously closed; or
3. a cross-boot successor carrying an already durable clean-exit interruption
   receipt that closed the predecessor segment before boot change.

A changed boot digest remains a valid process-death proof, but abrupt
supervisor or boot loss without that already durable close is `"unknown-loss"`
and selects terminal failure through the limit-plus-one telemetry branch. It
cannot resume ordinary work merely because the old PID is absent.

Every process-death row joins its role/PID/start identity and old-boot digest
to the exact authoritative attempt, worker-birth receipt, worker claim, or
predecessor receipt that last encoded that process. Same-boot `wait4` and
double-absence proofs require that joined old boot to equal the enclosing
current boot; boot-change proof requires inequality. A free-standing
well-formed boot digest has no authority.

Before deriving any transition, the atomic nonterminal receipt-directory
publisher admits only four states: absent stage/final; one valid canonical
receipt file in the unique stage, from which the exact marker is derived; one
valid complete staged receipt/marker pair; or one valid visible final pair. A
valid receipt-only stage is completed, and a valid complete stage is
no-overwrite renamed and parent-fsynced without changing its bytes. A successor
may perform that idempotent adoption only after proving the encoded publisher
dead, and its next durable receipt binds that death. Marker-only,
partial/corrupt, extra-entry, mismatched, or conflicting states are
forensically incomplete. An absent work-boundary stage means the current record
was not committed and must replay. An absent trace or measurement receipt is
reconstructed only from its complete durable prefix and followed by its
uniquely derived boundary. The measurement receipt literal is exactly
`"resource-measurement-block-v1"`.

This adoption rule has four explicit exceptions. A dead publisher's
worker-birth stage, `terminal_entry=true` final-success-boundary stage,
cleanup-complete failure-resume stage, or hidden terminal-outcome stage is
never normalized by a successor. Payload-only and payload-plus-marker forms
are never promoted to birth, success, or failure by a successor. For the three
terminal cases, A026 permits only a terminal-nonpass intent that binds the exact
stage bytes and publisher death; for worker birth, the identity may not be
guessed, but the launch may select pre-RNG failure after exact supervisor death
plus lease quiescence. The same continuously live publisher may finish its
exact stage, and an exact visible final may be revalidated only under its
branch-specific rules.

Every adoptable claim/receipt encodes and revalidates the publishing
process PID/start identity. A worker-birth payload uses the child identity it
self-published; worker claims use their existing supervisor fields;
reservations, traces, measurements, boundaries, cleanup intents, interruptions,
failure intents, and failure resumes use the exact fields frozen in the
artifact authority. A hidden worker-birth stage, the temporary kernel-14
probe, a dead-publisher `terminal_entry=true` boundary, a dead-publisher
cleanup-complete resume, and hidden terminal outcomes are not
successor-adoptable checkpoints. The latter three can only be bound as selected
evidence by the terminal-nonpass intent; they cannot be adopted as the selected
success/failure outcome.

A position-dependent debris set permits only the exact zero, one, two, or three
uniquely implied artifact-stage/final families in the authority derivation.
Its no-follow entry inventory enters an immutable interruption receipt before
idempotent prefix deletion and parent fsync. An uncommitted artifact final is
deleted before replay, never reused as a substitute for missing timing
evidence. Only an exact already-marked trace or measurement receipt may
authorize its uniquely derived missing following boundary. Chained supervisors
retain the immutable debris targets/rows and advance only the completed-prefix
and remaining-suffix fields from the filesystem. An extra stage/final,
conflicting final, forward reservation, non-prefix record, or other path is
terminal or forensically incomplete as frozen by the artifact authority.

Ordinary exceptions, sampler/accounting gaps, cap failures, stationarity
failures, rate-robustness failures, chunk-work timeouts, and numerical/provenance
failures are terminal, not interruptions. On a permitted resume:

1. the same attempt/config/source/runtime identity and outside-workspace
   baseline reload;
2. cumulative active elapsed, actual observed pre-boundary RSS/disk highs, and
   conservative boundary RSS/disk resume uppers reload only from durably closed
   process segments; reservation inventory, exact kernel prefix, and every
   completed receipt reload without deletion or replacement; conservative
   uppers are never relabeled observed, while unknown-loss selects failure;
3. an admitted lost worker execution adds a fixed 480-second replay penalty
   and its complete licensed RNG-call upper to the exact current position; a
   lost k1+k2 epoch has one replay ordinal but deliberately charges that full
   penalty to both eventual records, while physical cumulative elapsed counts
   the epoch only once; every eventual record carries both `Rplus` and
   `Aplus`, every relative predictor/reference operand reads only `Rplus`,
   every relative held/current operand reads only `Aplus`, and every
   conservative absolute projection reads only `Aplus`;
4. every completed stationarity, rate-robustness, cap, or failure verdict is
   irrevocable;
5. no interrupted rate-bearing trace resumes. If the interruption occurred
   inside one, ordinary work is already terminal failure. A partial initial or
   recovery-thermal trace is discarded without address reuse or rate evidence;
6. an interruption between completed rate-bearing traces resets thermal
   qualification immediately, and a later warm rate trace requires 600
   seconds of new uninterrupted recovery-thermal traces; interruption inside
   that recovery discards the partial cycle and restarts qualification from
   zero;
7. every completed rate-bearing trace and measurement block remains in
   admission, but there is no partial-block rate trace eligible for admission
   or replacement; and
8. only a new trace claims the next unused contiguous panel; a partial trace
   never receives a replacement panel; and every resumed capability proves the
   reservation creator at the unique endpoint of its current-to-creator
   predecessor suffix, with each link interruption-authorized.

Cumulative active elapsed starts at the first executable instruction of the
Make-launched resource supervisor, before source/runtime/config preflight,
baseline measurement, any root creation, or any other attempt mutation. The
origin samples are carried in memory and later sealed in immutable
`attempt.json`. The measured scope excludes only external `make`, shell,
`uv`, and Python-interpreter launch latency before that instruction; no
artifact calls that excluded launcher latency resource elapsed. Accounting
ends at the cutoff sampled immediately before terminal result/failure
encoding. It charges all in-scope supervisor startup, probes, capability
handoff, reservations, fixture preparation, workers, waits, hashing, fsyncs,
cleanup, resume validation, and every same-boot gap through that cutoff. The
later atomic terminal-outcome publication cannot measure its own fsync;
acceptance therefore adds Section 11's fixed
`terminal_close_accounting_charge_ns=60,000,000,000` as a projection
convention, not a terminal-close latency bound. An admitted cross-boot continuation
with an already durable clean-exit receipt charges the entire wall-clock gap
and reports `excluded_poweroff_ns=0`; abrupt boot loss instead selects
unknown-telemetry failure. Thermalization traces remain diagnostics only; no
completed cold, partial-block, or measurement-block evidence can be excluded
after an interruption. A claimed panel is never reassigned; deterministic
re-execution of a lost current position is separately counted as replay.

Terminal failure uses a different, irreversible continuation lane. Before any
destructive terminal cleanup, one immutable failure-intent receipt binds the
exact failure identity, durable receipt/artifact/RNG/log evidence, and complete
entry-level checkpoint/scratch deletion order. Its marker forbids every later
kernel, RNG, success result, or alternate failure. Terminal target rows are
exactly the currently present admitted artifact and terminal-close-probe
final/stage targets plus one exact fallback for each configured
checkpoint/scratch root that currently exists as an admitted directory. An
absent root emits no target or entry, and there is no intermediate
ordinary-tree target. Ordinary result-root receipts use only their separate
adoption or fail-closed state machine and never enter deletion plans. At least
one contiguous
failure-resume receipt is mandatory and no more than 641 may exist. Resume
zero names predecessor kind `"failure-intent"` and its digest; every later
resume names `"failure-resume"` and the immediately prior digest. Each segment
stores prior durable wall/perf/cumulative anchors, current resume and cutoff
samples, the same-boot monotonic or cross-boot wall charged gap, active work,
and exact cumulative sum. After predecessor publication/adoption, the resume
samples precede the segment's first deletion or parent fsync; the cutoff
samples follow every prefix advance and fsync charged to that segment. Resume
zero has completed prefix zero and is cleanup-complete iff the intent has no
entries. Each failure-intent or failure-resume receipt records at most 480
seconds of work, a fixed 60-second publication-accounting charge, and an
accounted interval of at most 540 seconds. The charge is a conservative
accounting convention, not evidence that failure-receipt publication completed
within 60 seconds. The
final resume is published only after every cleanup row is absent and every
required parent fsync is complete. Only then may deterministic
`terminal/failure/failure.json` and `_FAILURE` be atomically published with the
fixed 60-second terminal accounting charge. No post-intent interruption,
cleanup error, or cap can reopen work or change the selected outcome.

The final-resume publisher must remain continuously alive through failure
outcome-directory rename and therefore visibility. Death while outcome
stage/final are absent is forensically incomplete and authorizes no successor
creation or rename; death with a hidden stage is also fail-closed. An exact
visible final may only be revalidated and followed by an idempotent
terminal-parent fsync.

Resume zero is the mandatory pre-deletion anchor. Every later nonfinal receipt
either strictly advances the cleanup prefix or binds at least one newly proved
dead publisher. Process-death identities are deduplicated attempt-wide across
interruptions, failure intent, and failure resumes. A nonfinal staged resume
may be adopted after its publisher death and that death is bound in the next
receipt; a dead-publisher cleanup-complete stage is forensically incomplete
rather than duplicated. The bound is conservative:
`1 + 512 cleanup advances + 128 new deaths = 641`. Reaching a post-selection
resume/death cap stops before mutation as forensically incomplete.

Finite liveness is part of failure selection, not an implementation choice.
Registered execution admits at most 64 launch intents, 64 worker births, 64
worker claims, 63 interruptions, 4,096 traces, and 641 failure resumes. A
terminal cleanup inventory has at most 512 rows, the attempt-wide process-death
union has at most 128 rows, the cumulative worker-wait inventory has at most 64
rows, and every canonical path at most 240 ASCII bytes. Before every
checkpoint/scratch
mutation, the exact prospective terminal plan must remain within the row,
partition, path, and byte bounds. Each cleanup row encodes in at most 1,024
canonical bytes and each death or worker-wait row in at most 512. The
131,072-byte non-row term is the complete failure intent with all three row
arrays replaced by empty
arrays, so it includes every key, delimiter, array enclosure, digest, and
terminal LF. Therefore the maximum intent envelope is
`512*1024 + 128*512 + 64*512 + 131072 = 753,664` bytes, below the
1,048,576-byte receipt
cap. Before failure selection, reaching a count, path, or encoding bound
selects terminal failure before the one-past object is created. After failure
selection, exhausting a resume, death, path, row-byte, or receipt-envelope cap
stops the consumed failure as forensically incomplete before mutation; it
cannot become an unmarked or unbounded cleanup tail. The all-terminal fixtures
independently prove the result/failure/marker/failure-resume maxima; the
`753,664` failure-intent equation alone is not evidence that those other
schemas fit.

Marked failure admits only category-contiguous receipt prefixes, with at most
one active incomplete trace and every cross-category count derived by the
canonical scheduler. Generic parent arrays are sorted by UTF-8 role bytes. The
null-batch parent order is exactly `base-panel`, `cell-panel`,
`resume-homogeneous-focals`, `resume-observable-focals`, then
`resume-oracle-focals`. Cleanup object-kind literals, target order, and
entry-row order are the frozen sequences in the artifact authority; neither a
failure publisher nor a recovery supervisor may normalize or reorder them.

## 14. Acceptance and terminal failures

Every condition below must pass:

1. all fourteen exact kernels and all required contexts are complete;
2. each role reproduces its exact 15-position successful RNG-call sequence and
   equal/validation/research count vector, with no call at a zero-unit
   position;
3. all seals, initial supervisor/process identities, cumulative worker-wait
   inventories, both complete preterminal Git checks, all 24 preterminal Git
   child/output/wait/rusage rows, the count-two check inventory and digests,
   process-death rows, reservation ancestry, source/runtime identity,
   addresses, hashes, schemas, receipt-stage transitions, and registry
   transitions validate; no intermediate Git subprocess or worker/Git overlap
   occurs, and every cumulative rusage envelope reconstructs the frozen
   supervisor plus maximum worker-or-preterminal-Git high-water formula;
4. all seven resume-state rows obey their producer/consumer/cleanup lifecycle,
   including one shared immutable paper-weight artifact with no redraw;
5. the completed rehearsal evidence contains exactly 45 canonical boundaries,
   12 cleanup intents, 57 capped ordinary checkpoint intervals, one terminal
   accounting row, 58 resource-accounting rows in total, 13 artifact-kind
   counts, and 51 artifact rows;
6. the 600-second thermalization, three warm blocks, stationarity tests, all
   six temporal held-out predictions, and all 72 core cross-context checks
   pass;
7. interruption inside any rate-bearing trace selects terminal failure and
   contributes no rate operand; interruption between completed rate traces
   preserves prior evidence but requires a fresh uninterrupted 600-second
   thermal cycle, and interruption inside that cycle restarts it from zero;
8. `resource_accounted_charge_ns`, including the fixed 60-second terminal
   accounting charge, is
   at most `3,600,000,000,000` ns;
9. `7,200,000,000,000` ns is an unconditional hard kill, not admission slack;
10. validation projection is at most `43,200,000,000,000` ns;
11. research projection is at most `10,800,000,000,000` ns;
12. resource accounted charge plus both projections is at most
   `57,600,000,000,000` ns;
13. every task in Section 10 is at most 480 seconds observed and projected;
14. every completed ordinary checkpoint work interval is at most 480 seconds, every
    boundary-publication upper is at most 60 seconds, and every durable-marker
    interval upper is at most 540 seconds; pre-attempt bootstrap is at most 480
    seconds; every failure-intent/resume receipt has at most 480 seconds of
    work, exactly the fixed 60-second publication-accounting charge, and an
    accounted interval at most 540 seconds without claiming observed receipt
    publication latency; terminal pre-JSON work is at most 480 seconds, its
    separate fixed accounting charge is exactly 60 seconds, and their accounted
    sum is at most 540 seconds, without claiming an end-to-end bound on the
    later terminal suffix;
15. RSS, checkpoint, transient-disk, steady-state-disk, closed-segment
    telemetry, prospective cleanup-plan partitioning, and finite
    worker/interruption/trace/failure-resume/death/path/encoding rules pass;
    any unknown-loss limit-plus-one upper has already selected failure;
16. every ordinary and terminal cleanup filesystem is an exact absent
    entry-row prefix plus valid suffix; terminal failure has a contiguous
    1-to-641 failure-resume chain, strict progress/death transitions, and
    exactly one final all-absent/fsynced receipt;
17. no nonfinite value, PCA/rank/conditioning failure, LASSO nonconvergence,
    incomplete bootstrap vector, missing unit, process leak, sampler failure,
    or unassigned worker time occurs; and
18. `attempt.json` proves the complete twelve-child bootstrap check. Terminal
    JSON proves its digest, the complete twelve-child terminal-pre-JSON check,
    and their count-two inventory/hash; all 24 preterminal
    child/output/wait/rusage rows are jointly reconstructible from
    `attempt.json` plus terminal JSON. The post-JSON marker certificate proves
    the distinct final twelve-child Git/source/runtime/publisher/process/RSS
    guard. Rehearsal success has exactly three worker waits plus those jointly
    bound 24 preterminal Git rows. Visible-directory existence attests the later
    in-process seal. Successful admission publishes
    exactly the complete atomic `terminal/success/{result.json,_SUCCESS}`
    directory, while any fully closed marked terminal failure publishes exactly
    `terminal/failure/{failure.json,_FAILURE}` and cannot pass acceptance. A
    selected pre-entry failure that cannot reach its cleanup-complete receipt
    remains consumed and publishes no success or alternative outcome. After
    terminal entry, any uncertifiable selected success/failure closes only as
    `terminal/nonpass/{nonpass.json,_NONPASS}` with both policy Booleans false.
    Publication of
    the final success boundary or cleanup-complete final failure-resume receipt
    is the non-resumable terminal-entry point: publisher death, a missing or
    failed Git row/check, or any later terminal failure permits no retry, third
    preterminal check, success/failure rename or adoption, or opposite outcome;
19. the terminal-certificate test suite reconstructs every source, Git-control,
    and child row/count/digest for all three sequential twelve-child checks from
    `attempt.json`, terminal JSON, and marker bytes. It rejects any missing,
    additional, reordered, differently configured, nonzero, unreaped, or
    wait/rusage-inconsistent Git child; any mutated check digest or
    `preterminal_git_rusage_highwater_bytes`; any intermediate Git subprocess;
    and any worker/Git or Git/Git overlap before visibility;
20. mutation injection after marker fsync but before final seal covers every
    declared or Git-ignored `src/xid` source, literal authority file, Git
    executable/control input, runtime/module/boot identity, publisher identity,
    unexpected descendant/thread, sampler gap, and both final RSS thresholds;
    every case forbids success/failure rename and licenses only exact terminal
    nonpass after the publisher-death/failure evidence is frozen; and
21. crash injection at every terminal transition reproduces the exact
    pre-entry recoverable, non-resumable terminal-entry, conservatively
    kind-locked hidden, successor-rebuildable nonpass, or reusable visible-final
    state; after terminal entry it proves there is no successor success/failure
    publication, Git-check retry, third preterminal check, adoption, or opposite
    outcome, while exact nonpass remains available. The
    marker's 60-second guard clock never claims to observe marker write, final
    seal, rename, or terminal-parent fsync latency; and
22. worker-wait truth-table and mutation fixtures distinguish waitable reaping,
    non-wait death proof with false wait/pass flags, and neither-evidence
    blockage; reject omitted, duplicate, wrong-identity, wrong-status,
    wrong-`ru_maxrss`, and non-prefix cumulative rows; and prove that missing
    Git wait/rusage evidence cannot be converted to a worker death proof;
23. for fixed raw `D`, units, and enclosure `h`, incrementing any one record's
    replay count by one leaves every `Rplus` reference and derived `H`/`X`
    prediction unchanged, weakly increases the affected held/current `Aplus`
    and conservative absolute projections, leaves successful-work stop clocks
    unchanged, and cannot change any stationarity, temporal, cross-context,
    task, phase, total, or overall acceptance Boolean from false to true.
    Required rejection fixtures include equal-count blocks `(600 s,640 s)`
    where adding one prior-block replay cannot repair stationarity, and
    leave-one-out raw durations `[1000,1000,1300]` with replay counts
    `[1,0,0]` where the third block remains a temporal failure;
24. launch crash injection before intent, after durable intent/before spawn,
    after spawn/before birth, at birth payload-only and payload-plus-marker
    stages, after birth/before claim, after claim/before worker-ready, and after
    worker-ready/before capability release proves the intent is durable before
    spawn, the parent-liveness and registration-deadline checks fail closed, no
    unregistered child can acquire authority, hidden birth stages are never
    successor-adopted, every complete visible birth identity is closed exactly
    once, a live inherited lease makes fresh-open `flock` return
    `EWOULDBLOCK`, exact supervisor death plus acquisition of the same stable
    lease inode selects pre-RNG failure, and a changed-boot launch-only close
    releases no scientific capability;
25. Darwin absence fixtures exercise present-target, stable ESRCH, stable PID
    reuse, mixed ESRCH/reuse, changing replacement identity, permission error,
    zero return with zero/wrong errno, short/oversize return, PID mismatch, ABI
    mismatch, and boot change between samples; they reconstruct both raw
    samples from the factorized row, and only the two stable admissible
    same-boot classes can satisfy double absence;
26. every final-success-boundary state—absent, payload-only,
    payload-plus-marker, complete visible final, marker-only, corrupt,
    extra-entry, and stage-plus-final—is exercised with live and dead
    publishers; a dead publisher can never normalize or rename a
    `terminal_entry=true` stage or authorize a terminal Git check/outcome, but
    its exact stage bytes can select the immutable terminal-nonpass intent;
27. watchdog fixtures reject an arm first appearing in a wait row, wrong or
    missing arm kind/digest, wrong `worker-exit`/`work-timeout` request-time
    nullability, arithmetic mismatch, deadline recomputation from a later
    clock, timeout request after the work deadline, and `wait4` completion after
    the reap deadline; every wait4 death row must equal the exact fourteen-field
    worker-wait projection; and
28. the frozen schema fixtures across every terminal artifact family,
    including nonpass intent, lock, JSON, and marker, reproduce their exact
    CJSON or fixed-file lengths at all configured maxima,
    remain at most 1,048,576 bytes, reproduce the exact fixture-schema digest
    and authority-stage-specific two-row success/failure preflight, and reject
    every one-past row, path, sample, integer-width, message, or envelope
    mutation before publication; and
29. a fresh process reproduces exactly 9,799 config bytes, SHA256
    `3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
    194 leaf-type rows, and type-tree SHA256
    `e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.

At 80% of a hard phase runtime, the later validation/research runner must stop
when its measured completion projection exceeds that hard cap. This runtime
rule cannot rescue an A022 expected-projection failure.

The public result contains only seals and hashes, address-inventory hashes and
RNG call counts, integer timing/unit/rational-rate records, named empirical
enclosures, projections, RSS/disk/registry telemetry, convergence/finiteness
booleans, and the exact admission decision or failure reason. Scientific
numeric outputs are forbidden.

## 15. Strongest unresolved objection

The paper-cache fixtures reproduce exact shape, byte count, hashing,
serialization, weighted accumulation, and cleanup work, but they repeat one
actual date summary. They cannot reproduce cache heterogeneity or the
concurrent lifetime of 252 independently computed paper summaries. Generating
252 full-paper and 252 recovery dates per block would turn the admission
experiment into the very workload being projected and can violate its
one-hour budget.

The phase traces are not proportional to `W`; kernels 11, 12, and 13 cannot
enter the cross-phase core check; and per-kernel extrapolation from each timed
count to full work remains unvalidated. The production paper-date kernels,
three sustained mixed blocks, slowest-context projection, 60%-cold bound, 25%
margin, temporal prediction, and cross-phase core checks reduce these threats;
they do not eliminate them. A022 therefore supports only a conditional
machine/runtime admission claim, not a measured full-mixture guarantee or
statistical coverage for a future 12-hour thermal trajectory. Validation and
research must retain their runtime reforecast and hard-stop rules.

Terminal-publication RSS is likewise a sampled empirical envelope, not a
continuous upper bound. Child `wait4` high-water evidence protects against a
short child spike, but a sub-sample parent-process spike can escape the 50-ms
tree sampler; the 25% factor is policy headroom rather than a mathematical
proof. Rehearsal must report this limitation and may falsify the selected
margin, but cannot erase it.

## 16. Pre-implementation falsification prediction

The current repository must fail deterministically before any registered RNG:

- the exact `configs/g2_resource.toml` contract now exists, but no typed parser
  or resource Make target exists;
- `G2Contract` does not mechanically expose the compute contract;
- `TestRngNamespace` correctly refuses the resource seed and no separate
  resource capability exists;
- paper, interval, paper-bootstrap, phase-publication, and resource-runner
  production paths are absent;
- only the pre-A024 base/cell checkpoint variants are implemented; no
  seven-row resume state, shared paper-weight, entry-level cleanup/debris,
  interruption, failure-intent/failure-resume, launch-quiescence lease,
  terminal-nonpass intent, or atomic three-kind terminal-outcome codec exists;
- no implementation enforces the exact three RNG-call vectors, initial
  supervisor/death-proof schema, durable launch-intent/birth lifecycle,
  precommitted watchdog arms, immutable reservation ancestry,
  rate-trace failure/between-trace thermal reset, closed-segment telemetry, or finite
  `64/64/64/63/4096/641`, `512/128/64/240`, and `753,664`-byte evidence
  bounds;
- no implementation enforces one-sided `Rplus` reference versus `Aplus`
  held/current operands, absolute-`Aplus` projections, or the deterministic
  replay-increment monotonicity fixtures;
- no implementation validates the category-contiguous marked-failure prefix
  or its exact generic-parent, null-batch-parent, cleanup-target, and entry-row
  byte order;
- no implementation proves the exact Darwin absence-result table, inherited
  open-file-object `flock` quiescence, dead-publisher final-boundary
  nonadoption-to-nonpass transition, successor-rebuildable nonpass stage, or
  all-terminal maximum-size preflight;
- no implementation can publish the required
  13-kind/51-artifact-row/58-resource-accounting-row rehearsal evidence;
- the paper cache exceeds the current single-payload ceiling; and
- the old equal-context statistic has no stationarity, temporal held-out, or
  cross-context rate falsifier.

Implementation may begin only under test seeds. The registered resource
outcome prediction—including expected elapsed, RSS, disk, and phase-projection
ranges—must be appended and sealed after the complete test-seed rehearsal and
before the registered command is authorized. No registered resource,
validation, or research seed is licensed by this derivation alone.

## 17. A026 precedence and present stop condition

Amendment A026 supersedes the A025 branches that allowed a resumed suffix of
an interrupted rate-bearing trace to enter admission, stranded a same-boot
launch-only attempt after supervisor death, or stranded an exact terminal-entry
selection after publisher death. All other A022--A025 numerical and byte
authority remains unchanged.

The active resource config is exactly 9,799 bytes with SHA256
`3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
194 leaf-type rows, and type-tree SHA256
`e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.
The successful-rehearsal tuple remains `3/45/12/57+1/58/13/51/7` for traces,
boundaries, cleanup intents, ordinary plus terminal accounting, total resource
rows, artifact kinds, artifact rows, and resume-state rows per trace.

The design remains deterministically red. No resource implementation,
test-seed rehearsal, registered resource command, or registered G2 namespace is
authorized until fresh independent methods, systems, and schema reviews pass
the settled A022--A026 package. Even a document pass licenses only test-seed
implementation followed by deterministic tests and hosted CI; it does not
license a registered seed.
