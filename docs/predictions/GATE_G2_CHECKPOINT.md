# G2 checkpoint and 252-date test-seed recovery predictions

Recorded before checkpoint implementation and before the stochastic call
described below. No registered G2 seed, empirical data, or holdout informed
these predictions.

## Deterministic checkpoint predictions

The existing code has no serialized manifest loader and cannot mint fresh
base-panel or cell-panel authority after process-local weak receipts die. The
first red tests therefore fail at import/API collection.

The repaired path must satisfy all eight outcomes in
`docs/derivations/GATE_G2_CHECKPOINT_AUTHORITY.md`, including exact round-trip
bytes, fresh-process fit authority without a draw or upstream replay,
fail-closed hostile schemas, immutable success-last publication,
cumulative-resource recovery, and refusal of every registered or otherwise
unlicensed seed. The checkpoint regression suite uses only seed `1729`; the
preregistration-amendment-A019 `VALIDATION_RECOVERY`, 252-date checkpoint
address at seed `9191` does not appear in a pytest-collected test.

These are software-contract tests. They evaluate no scientific coefficient and
have no statistical interval or multiple-testing count.

## One 252-date test-seed recovery

After the deterministic checkpoint suite is green, exactly one stochastic
software-recovery run is licensed through a dedicated one-shot supervisor, not
through ordinary pytest. Before the first draw, the supervisor atomically
publishes an immutable `attempt.json`; its existence blocks every retry,
including after a crash:

```text
master seed:       9191
stream:            VALIDATION_RECOVERY
phase/scenario:    contract-derived 23/0
n_dates:           252
panel_index:       0
target_index:      16
paper_recovery:    false
phi:               0.60
stored reliability:0.95
date order:        0..251
weights:           252 float64 ones
```

The public attempt/result receipts are rooted at
`results/g2_checkpoint_recovery/`; the checkpoint and scratch roots are
`data/g2_checkpoint_recovery/checkpoints/` and
`data/g2_checkpoint_recovery/scratch/`. The sole public interface is
`make g2-checkpoint-recovery`; it starts the supervisor with the exact empty
`data/g2_checkpoint_recovery/scratch/bootstrap-pycache/` prefix before Python
imports the module, and direct module invocation fails before constructing the
A019 address. The worker and fresh process use separate unique, initially empty
bytecode-cache prefixes below the same exact scratch root, so no pre-existing
timestamp `.pyc` can select their executable code. Each private child also
requires a one-shot inherited pipe capability bound to its role, immediate
parent, attempt digest, exact internal-specification bytes, and canonical
scratch path.

The run constructs one complete issued base panel and one complete issued cell
panel, computes the three smooth point fits, writes the two checkpoints,
deletes every live date/design/moment/panel/aggregate object, forces garbage
collection, reloads both artifacts, reaggregates, and recomputes the three
fits. It does not compare any coefficient with truth and cannot pass or fail
the G2 premise.

Prediction and tolerance:

- every loaded panel array has the same exact little-endian C-order bytes and
  SHA256 as its pre-checkpoint array;
- every retained receipt tuple and design digest tuple is exactly equal;
- oracle-ridge, observable-ridge, and pooled-homogeneous coefficients are
  exactly equal on the same runtime; no positive numerical tolerance is
  permitted;
- all outputs are finite with shapes `(30,30)`, `(30,30)`, and `(3,)`;
- the two artifact directories together remain below 12 MiB;
- wall clock is expected below 30 seconds, hard-stopped at 120 seconds;
- peak RSS is expected below 1 GiB and hard-stopped at 1.5 GiB; and
- a fresh subprocess obtains the same three coefficient SHA256 values by
  loading only the checkpoints; all namespace draw methods are patched to
  raise, proving that recovery performs no draw or upstream replay.

Any mismatch is a checkpoint/recovery implementation failure. The seed is not
retried and the tolerance is not widened. The parent CLI enforces the 120-second
hard timeout and 1.5-GiB RSS hard stop, records actual method-normalized peak
RSS and wall time, and writes one immutable committed result containing:

```text
schema_version status seed stream phase_id scenario_id n_dates panel_index
source_snapshot_sha256 runtime_sha256 base_artifact_sha256
cell_artifact_sha256 array_sha256_before array_sha256_after
receipt_sha256_before receipt_sha256_after design_digest_sha256_before
design_digest_sha256_after
coefficient_sha256_before coefficient_sha256_after
coefficient_shapes coefficient_finite fresh_process_coefficient_sha256
fresh_process_rng_draw_count artifact_logical_bytes artifact_allocated_bytes
elapsed_seconds timeout_method peak_rss_bytes rss_normalization_method
hard_stops
```

The result is written as canonical `result.json` plus a canonical `_SUCCESS`
containing the result SHA256 and `complete=true`; both are immutable and are
not silently regenerated if they already exist. A failed or interrupted
one-shot writes an immutable failure receipt when the supervisor can do so and
still remains non-rerunnable. Because wall-clock and RSS are execution-specific,
this receipt is an immutable audit record with an explicit exemption from
byte-identical regeneration; its scientific inputs and content hashes remain
fully reproducible.

The public runner has no address overrides and may consume A019 only from a
clean declared execution-source snapshot after deterministic local and hosted
verification. It requires all six numerical thread variables to equal `"1"`.
Before the first DGP draw, the primary worker also publishes an exclusive
ignored worker claim, after independently rechecking the live source/runtime
identity against `attempt.json`. The supervisor samples the complete
worker-process-tree RSS every 0.05 seconds using `ps` KiB values normalized to
bytes and rejects surviving process-group descendants after the leader exits.
This proves termination at the first observed breach; it does not claim that no
shorter unsampled peak occurred. Exact receipt schemas and failure-state
semantics are frozen in Section 9 of
`docs/derivations/GATE_G2_CHECKPOINT_AUTHORITY.md`.

## Hostile closeout predictions recorded before the second recovery repair

The first hostile closeout found five fail-closed gaps after the ordinary
seed-1729 suite was green. Before changing the implementation, five focused
regressions were written and all five failed:

1. a symlinked ancestor was followed while creating an otherwise ordinary
   result/checkpoint/scratch leaf, reaching contract loading after mutation;
2. a process group reported alive after both `SIGTERM` and `SIGKILL`, but the
   teardown helper returned;
3. the private child accepted the same reopenable named FIFO twice as a
   purported one-shot capability;
4. an unexpected sampler exception escaped supervision without any worker
   process-group teardown; and
5. one injected directory-fsync fault after linking `_SUCCESS` left both
   `_SUCCESS` and `_FAILURE` visible.

The repair is predicted to make all five regressions pass without invoking
seed 9191. Specifically, every root must be an absolute normalized path whose
resolved identity is byte-for-byte the supplied path before any directory
mutation, and that equality must be rechecked after creation. A private child
must accept only an inherited anonymous pipe: Darwin requires an unlinked
kernel pipe identity, Linux requires a `/proc/self/fd` target of
`pipe:[inode]`, and an unsupported platform fails closed. Once `Popen`
succeeds, every exit from supervision—normal, handled, unexpected, or
`BaseException`—must either observe the process group absent or run the same
bounded TERM/KILL teardown. Teardown may return only after a post-`SIGKILL`
absence check; a group still present is a failed recovery.

An evidence hard link is not treated as a failed write merely because the
first parent-directory fsync raises. The writer retries that durability
barrier once. If the retry succeeds, the linked outcome is authoritative. If
it does not, the writer removes the link and durably confirms removal before
raising. If removal durability is itself unknowable, the outcome is marked
uncertain and the supervisor must not publish the opposite terminal marker.
Independent of that branch, failure publication refuses to coexist with a
visible success marker. The falsifying outcomes are any one of the five tests
remaining red, any two terminal markers coexisting, a teardown return while
the group-existence probe remains true, or any appearance of the exact A019
address in test execution.

## Second hostile-closeout predictions recorded before repair

The next read-only pass found two additional failures and three focused
regressions recorded them before code changed. First, the uncertainty branch
could be type-erased when its later stage unlink raised `OSError`; the
supervisor then saw an ordinary cleanup error and was permitted to publish
failure evidence. Second, a command-line Make variable redirected the
pre-import bootstrap `mkdir`, and a symlinked `data` ancestor was followed
before Python could reject it.

The evidence-stage cleanup prediction is that an ordinary cleanup `OSError`
never replaces a publication outcome. The fully written stage is
non-authoritative after link or rollback, so cleanup is best effort; the
original `_PublicationStateUncertain` must reach the supervisor unchanged.
Under three directory-fsync faults plus one stage-unlink fault, the attempt
must remain consumed and neither terminal marker nor `failure.json` may exist.

The public-launch prediction is that both the bootstrap path and six-thread
environment are Make `override` constants. A command-line assignment may not
appear in `make -n` output. Before the literal `mkdir`, the recipe checks every
existing component from `data` through `bootstrap-pycache` and stops if any is
a symlink. In a copied Make surface whose `data` is a symlink, the outside
target must remain byte-for-byte empty and the Python command must not run.
These checks cover accidental or ordinary redirection, not a coordinated
same-user process racing path components between shell operations.

A final variant recorded red before structured cleanup injects
`KeyboardInterrupt`, rather than `OSError`, while removing the success stage
after publication has become uncertain. The predicted result is identical:
the active uncertainty reaches the supervisor, no failure evidence is
published, and the attempt remains consumed. Broadly suppressing interrupts is
not permitted; cleanup suppresses a `BaseException` only while preserving an
already-active `_PublicationStateUncertain`. Without an active uncertainty,
the same interrupt must still propagate.

## Launcher-identity prediction recorded before source-contract repair

The current tracked-plus-untracked execution snapshot is predicted not to call
its stable file-identity routine for `Makefile`, even though the Make target is
now the sole public constructor of the A019 environment. A behavioral spy must
record that omission red. After repair, the snapshot must include exactly the
root `Makefile` alongside the previously frozen six paths, so a launcher byte
change alters `source_snapshot_sha256` and makes
`declared_paths_clean=false`. No stochastic address is involved in this test.

## Test-smoke receipt correction recorded before code

The existing seed-1729 smoke is predicted to expose two identities: its result
claims `VALIDATION_RECOVERY`/`23/0`, while its checkpoint source receipts carry
the actual `VALIDATION_DATE_FRONTIER`/`22/2` address selected by
`_execution_stream`. That mismatch is an evidence failure even though the
numeric recovery hashes are exact.

After repair there is one identity only. The test `RecoveryRunSpec`, attempt,
worker checkpoints, and result must all say
`VALIDATION_DATE_FRONTIER`/`22/2`; `_execution_stream` must not exist. The
seed-1729 procedure still writes, drops, reloads, and fresh-process refits the
checkpoints. Public A019 alone says `VALIDATION_RECOVERY`/`23/0`, and no pytest
case may instantiate its seed/date/stream tuple.
