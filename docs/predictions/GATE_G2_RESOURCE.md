# G2 resource-admission pre-implementation prediction

Written on 2026-07-28 before resource-run code and before any registered G2
resource, validation, or research RNG access.

## Claim at risk

The complete final G2 production path can be measured on the target M4 Air in
a way that includes provenance hashing, checkpoint I/O, paper reconstruction,
thermal drift, workload-mixture transfer, and publication without opening a
validation or research realization.

This prediction is about whether that admission experiment is implementable.
It is not yet a prediction that the final G2 workload will fit.

## Predicted current result

The current repository will fail closed before RNG construction for at least
these independent reasons:

1. no registered resource namespace or Make-only resource supervisor exists;
2. the typed contract does not parse the frozen `[compute]` tables;
3. the paper reconstruction, paper recovery, interval-finalization,
   paper-bootstrap, phase-publication, and resource-runner paths do not exist;
4. null-batch, paper-summary, paper-cache, paper-bootstrap, publication, trace,
   and measurement-block artifact schemas do not exist;
5. the current 5 MiB payload ceiling cannot hold the 17,055,360-byte research
   cache without the preregistered four-shard layout;
6. the codec's generic 2 GiB tree ceiling is larger than the binding decimal
   2,000,000,000-byte limit; and
7. the old one-unit/last-three bundle cannot test thermal stationarity or
   phase-mixture transfer.

These are seven deterministic failure classes, not seven scientific trials.

## Predicted repaired software result

After test-seed implementation:

- every malformed authority, address, source/runtime, artifact, cap, resume,
  registry, timing, stationarity, and held-out-transfer case will fail before
  a registered address;
- the exact operand block will report units
  `252, 252, 25, 225, 225, 225, 4096, 1, 1, 1, 1, 1,
  6,048,000/53,298,000, 1`;
- registered panels will be claimed contiguously from zero, with `b=0` cold
  and every later `EQUAL`/`V`/`R` role fixed by the preregistered schedule;
- the three fixed test-seed measurability rehearsals will use seed `1729`,
  panels `10000..10002`, and the unrevised
  `k3=25,k4=225,k5=225,k6=225,k7=4096` counts; any subblock below 100 ms will
  fail rather than tune;
- every rehearsal k14 envelope-plus-terminal-close-probe will satisfy
  `ceil_div(25*D_plus,12) <= 480,000,000,000` ns or fail, licensing the fixed
  early-failure close fallback without registered timing; rehearsal
  `replay_count=0`, so this persisted `D_plus` is exactly equal to `Aplus` and
  does not license `Rplus` in a registered absolute projection;
- the rehearsals' 45 canonical boundary leaves plus 12 cleanup-intent leaves
  will produce exactly 57 ordinary checkpoint intervals, each satisfying the
  fixed 480/60/540-second work/publication/marker limits or failing without
  retiming;
  supervisor bootstrap through durable `attempt.json` will satisfy its fixed
  480-second limit;
- their exact one-shot command is `make g2-resource-rehearsal`; it uses
  disjoint test-only roots and artifacts that every registered loader rejects;
- the paper fixtures will have exact shapes `(252,960)` and four
  `(63,8460)` shards, will pass only their benchmark loader, and will fail
  every scientific loader;
- the publication envelope will contain exactly 50 payload shards and
  238,000,000 numeric bytes;
- integer-nanosecond arithmetic will reproduce every projected bound without a
  float-rate comparison;
- all eight weak registries will return to their exact pre-block counts after
  charged release and GC; and
- every durable work/publication/marker interval will be at most
  480/60/540 seconds, respectively; partial traces and partial blocks will
  preserve their exact prefixes, and pre-attempt bootstrap will be at most
  480 seconds; and
- interruption will preserve cumulative elapsed, actual pre-boundary
  observations, nondecreasing conservative RSS/disk resume uppers, the same
  partial-trace reservation, every completed measurement-role trace, and
  fixed replay/RNG uppers without relabeling an upper observed. A suspended
  trace completes its exact next position, then a fresh 600-second
  successful-work thermalization precedes any later warm trace.

No microbatch count will be selected from timings. The fixed counts above are
falsified, not tuned, by three predeclared test-seed rehearsals and are frozen
in `configs/g2_resource.toml` before registered access.

## Registered-run prediction remains sealed

A quantitative prediction for registered benchmark elapsed, RSS, checkpoint
high water, and validation/research projections would currently be invented.
A019 supplies only a partial observation: one 252-date smooth checkpoint
recovery took 18.907810209 seconds, observed 178,864,128 bytes peak RSS, and
allocated 9,183,232 checkpoint bytes. It contains no paper/LASSO, thermal,
mixture, or phase-publication rate.

Therefore the registered-run prediction is deferred, not omitted. After all
fourteen paths pass at actual shape under test seeds, but before seed
`2026071529` is accessible, this file must receive an append-only execution
seal containing:

- exact resource-config hash;
- the exact eight-path executable digest shared by rehearsal and registered
  execution and the immutable rehearsal evidence hash;
- all frozen fixed block counts and three test-seed measurability durations;
- test-seed observed timing, RSS, and disk ranges with named measurement
  methods;
- predicted registered elapsed, RSS, disk, validation, research, and combined
  ranges; and
- the exact authorized command and no-retry/resume boundary.

The execution seal cannot contain the digest of the 13-path authority tuple
because this prediction file is itself one of those 13 paths. After the seal
is committed, preflight computes the final authority digest over the resulting
bytes; the clean hosted commit, `attempt.json`, every registered receipt, and
the human authorization bind that digest. No file inside the authority tuple
contains its own authority digest.

Until that append-only seal exists and passes two hostile reviews plus hosted
CI, `make g2-resource-benchmark` must fail before constructing any RNG
capability.

## Falsification

The software claim is falsified if any required production path cannot be
timed without a surrogate that can mint scientific authority, any time remains
unassigned, any fixture reaches a scientific loader, any registry grows across
charged cleanup, any resource limit can reset on resume, or any test-seed
malformed case obtains a registered address.

The eventual resource claim is falsified by any stationarity, temporal, or
cross-context rate failure, expected or hard budget breach, task over 480
seconds, checkpoint work/publication/marker interval over 480/60/540 seconds,
resource high-water breach, missing/nonfinite/nonconverged kernel, source or
runtime drift, incomplete rate region, discarded prefix, replay penalty present
on a predictor/reference operand, replay penalty absent from a held/current or
absolute-projection operand, or fixed-input replay-count increment that changes
an acceptance Boolean from false to true. A failure leaves every validation and
research seed sealed.

## A023 correction before implementation

Appended on 2026-07-29 before resource-run code or any rehearsal. This section
supersedes the earlier “workload-mixture transfer”, “phase-mixture transfer”,
“held-out mixture failure”, and “all eight weak registries” predictions
without changing their historical text. The active failure condition is a
temporal or cross-context rate-robustness failure.

The fixed validation and research phase traces are not proportional to `W`,
and no nontrivial exact proportional trace exists under the frozen integer
work grammar. The repaired software is therefore predicted to:

- report the existing six same-phase held-out rows only as temporal checks;
- report 72 separately gating, individually falsifiable cross-context rows
  over kernels `1..10,14`, comprising every block, phase, per-kernel
  comparison, and shared-kernel aggregate;
- reject when any held `Aplus` duration exceeds 1.25 times its
  `Rplus`-derived slower opposite-phase reference upper from the other two
  blocks; raw observed timings remain diagnostic;
- describe every final `W` projection as conditional on per-kernel linear
  extrapolation, never as a measured full-mixture transfer guarantee;
- account for the four new issuable wrapper classes in one ninth weak
  `_RESOURCE_ARTIFACT_REGISTRY`, with all nine baselines restored after
  charged cleanup;
- bind panel, executable, and historical authority snapshots in every
  rehearsal terminal path while requiring only executable equality across
  rehearsal and registered stages; and
- fail deterministic byte tests for any nonliteral NPY header, alternate stage
  name, incomplete debris/final digest, opaque rehearsal artifact inventory,
  ambiguous mode/allocation unit, or incomplete outside-workspace row.

The registered quantitative timing/RSS/disk ranges remain deferred until the
one-shot test-seed rehearsal exists. Passage of these stronger software checks
still would not establish full-workload rate linearity, heterogeneous
252-date cache lifetime, scientific validity, or any validation/research
result.

## A024 correction before implementation

Appended on 2026-07-29 before resource-run code, any rehearsal, or any
registered resource access. This section supersedes the earlier 48-boundary,
eight-registry, per-record replay, and implicit operand-lifetime predictions
without changing their historical text.

The repaired software is now predicted to:

- execute the exact 15-position record order
  `k1,k2,k3,k4,k5,k6,k7,k9,k10,k8,k11,k12,k13-recovery,k13-research,k14`,
  with k1+k2 forming one indivisible first-operand epoch;
- persist only the exact base/cell panels, bootstrap weights, and three
  candidate-focal arrays needed by later operands; deterministically reconstruct
  aggregates rather than persisting them; and fail any alternate
  producer/consumer/cleanup path;
- expose 15 canonical boundary leaves and four cleanup-intent leaves per
  rehearsal, hence exactly 45 boundaries, 12 cleanup intents, and 57 capped
  checkpoint intervals across the three frozen panels;
- preserve a registered partial trace by publishing an additional worker-ready
  boundary that copies its completed positions, records, first-epoch object,
  resume state, next position, and pending replay without advancing the
  canonical sequence;
- inventory and delete every position-permitted uncommitted artifact final or
  hidden stage before replay, with an exact zero-to-three-target debris plan
  and derived entry rows; permit only an exact
  already-marked trace or measurement receipt to complete its uniquely derived
  missing following boundary;
- assign one replay ordinal to a lost k1+k2 epoch while deliberately charging
  the full 480-second admission penalty to both eventual records and counting
  physical cumulative elapsed once;
- select terminal failure in an immutable pre-deletion intent, then permit only
  its journaled cleanup/resume suffix and byte-consistent `_FAILURE` closure;
  no crash during terminal cleanup may reopen work or select success;
- restore all nine weak registries after the composite epoch and every later
  record; and
- retain exactly 12 artifact-kind counts and 48 artifact rows across a
  successful three-panel rehearsal.

These are falsifiable software predictions, not observed outcomes. No A024
rehearsal has run, no registered resource seed has been constructed, and the
quantitative registered timing/RSS/disk prediction remains deferred.

## A025 correction before implementation

Appended on 2026-07-29 before resource-run code, any rehearsal, or any
registered resource access. A022--A025 were the active authority at that
freeze; A026 below supersedes three failed branches.
A025 supersedes every conflicting receipt, cleanup, interruption,
RNG-lifecycle, telemetry, terminal-close, replay-comparator, durable-child,
process-absence, watchdog, terminal-adoption, and terminal-size prediction
above without changing the older text, which is explicitly historical. In
particular, the earlier 48- and 57-interval, eight-registry, 12-kind/48-row,
whole-leaf-cleanup, implicit failure-resume, post-interruption-thermal, and
predictor-side replay-penalty statements are not implementation authority.

The repaired software is now predicted to satisfy all of the following
falsifiers:

- In the frozen 15-position record order, successful RNG call-count vectors
  are exactly
  `[1260,0,25,0,0,0,0,0,0,0,5,5,25,0,0]` for equal/rehearsal,
  `[1260,0,25,0,0,0,0,0,0,0,0,5,25,0,0]` for validation, and
  `[1260,0,25,0,0,0,0,0,0,0,5,0,0,25,0]` for research. Position 0 is
  date-major/component-ascending smooth DGP calls, position 2 is
  replicate-ascending smooth bootstrap calls, positions 10 and 11 contain
  their positive five-call paper-date inventories, and the first positive
  kernel-13 position contains the 25 replicate-ascending paper-bootstrap
  calls. Every other inventory is empty; replay copies cannot sort or
  deduplicate them.
- Resume state contains exactly seven rows: base panel, cell panel, smooth
  bootstrap weights, three candidate-focal artifacts, and one role-resolved
  paper-bootstrap-weight artifact. The immutable
  `resource-resume-paper-bootstrap-weights-v1` payload has shape `(25,252)`,
  is produced at the first positive kernel-13 position, and is deleted by the
  last positive kernel-13 position's cleanup. Its
  producer/last-consumer/cleanup positions are `12/13/13` for
  equal/rehearsal, `12/12/12` for validation, and `13/13/13` for research.
  Both positive equal variants consume identical bytes; a zero-unit variant
  draws nothing.
- A successful three-panel rehearsal retains exactly 13 artifact-kind counts
  and 51 path/kind/hash rows. It exposes 45 canonical boundaries, 12 cleanup
  intents, 57 capped ordinary checkpoint intervals, one terminal accounting
  row, and therefore 58 resource-accounting rows.
- Ordinary receipt stages are normalized before a transition: a valid
  receipt-only stage is completed, a valid complete staged pair is
  no-overwrite renamed and parent-fsynced, and a valid final is reused. A
  successor may adopt a valid stage only after proving the encoded publisher
  dead, and every adoptable payload encodes/revalidates that publisher.
  Worker-birth stages, the registered `terminal_entry=true` final block-3
  boundary, the final rehearsal boundary, and cleanup-complete final
  failure-resume stages are never successor-adoptable after publisher death.
  Their same live publisher may finish exact bytes; a dead publisher
  authorizes no next receipt, Git check, or terminal outcome.
  Marker-only, partial, corrupt, extra-entry, mismatched, or conflicting
  states remain forensically incomplete.
- Cleanup and debris freeze exact child-before-parent filesystem-entry rows,
  not whole leaves. File rows bind mode, logical/allocated bytes, and content
  SHA256; directory rows bind type/mode with null byte/hash fields. Only an
  exact absent prefix plus byte-valid remaining suffix and no extra path is
  legal. Chained interruptions preserve immutable target/row bytes while
  advancing the completed-prefix count and remaining-suffix digest from the
  filesystem. Unique deepest-target membership, positive contiguous target
  slices, terminal root fallbacks, and a prospective pre-mutation 512-row
  check make the terminal plan deterministic and representable.
- Terminal failure publishes between one and 641 contiguous failure-resume
  receipts, including an exact final cleanup-complete receipt after every row
  is absent and all required parent fsyncs complete. Resume zero binds the
  failure intent; each later receipt binds its immediate predecessor and the
  exact prior/current wall, perf, gap, active-work, and cumulative clocks.
  Each resume sample precedes that segment's first deletion/fsync and its cutoff
  follows every charged prefix advance/fsync. Resume zero has prefix count zero
  and has `cleanup_complete=true` iff the intent is empty. Each failure-intent
  or failure-resume receipt records at most 480 seconds of work, a fixed
  60-second publication-accounting charge, and an accounted interval of at
  most 540 seconds. The charge is not an observed or enforced bound on
  failure-receipt publication latency. Every later
  nonfinal receipt advances the prefix or binds a newly dead publisher. A
  dead-publisher
  nonfinal stage is adoptable only with another slot/death row; a last-slot or
  cleanup-complete stage fails closed rather than producing a second final.
- Terminal outcomes are atomic directories
  `terminal/success/{result.json,_SUCCESS}` and
  `terminal/failure/{failure.json,_FAILURE}`. Exactly three non-overlapping
  twelve-child Git checks are legal: bootstrap before the first worker;
  terminal-pre-JSON after every issued worker identity is closed, no worker is
  alive, and every currently waitable direct child has been reaped; and the
  distinct post-JSON check bound by the marker. `attempt.json` persists the
  complete twelve-child bootstrap full check. Terminal JSON persists that
  check's digest, the complete twelve-child terminal-pre-JSON full check, and
  their count-two inventory/hash; the 24 Git-child rows are jointly
  reconstructible from `attempt.json` plus terminal JSON. The marker persists
  the final 12 rows. Intermediate
  source/control seals reconstruct stable bytes in-process before and after
  sealed contract/resource-config loading, immediately before and after every
  nonterminal resource-root mutation, before every worker capability, and
  after every measurement block; they launch no Git subprocess. At
  each cutoff, the rusage high-water envelope is supervisor high-water plus the
  larger of the cumulative worker high-water and the available preterminal
  Git-child high-water. Observed RSS is the maximum of the sampled tree peak
  and that envelope; admission then applies the 25% current margin and carried
  durable-upper maximum. Bootstrap Git high-water is present at every durable
  cutoff, terminal-pre-JSON joins only at the terminal cutoff, and post-JSON
  remains in the marker's separate publication-RSS envelope.

  Publication of the final success boundary or cleanup-complete final
  failure-resume receipt is the non-resumable terminal-entry point. The same
  publisher must execute the terminal-pre-JSON check, write and fsync the
  hidden JSON stage, execute the post-JSON check under the sampler, write and
  fsync the marker, pass the no-subprocess final seal, rename the outcome, and
  fsync the terminal parent. A failed or incomplete check, publisher death, or
  later publication failure makes the attempt forensically incomplete; no
  successor may retry a Git check, publish the selected outcome, or select its
  opposite.

  Each terminal-entry receipt also carries a schema-bound size preflight.
  Maximum canonical fixtures cover failure intent, every failure-resume
  shape, rehearsal and registered success/failure JSON, and both markers with
  every applicable 64-wait, 128-death, 512-cleanup, 641-resume, 240-byte-path,
  24-preterminal-Git, 12-post-JSON-Git, and 1,201-publication-sample maximum.
  Every file must remain at or below 1 MiB and every one-past mutation fails
  before publication. A failing success preflight selects ordinary failure;
  after failure selection, a failing final preflight stops before the final
  resume or terminal-stage mutation.

  The marker persists every post-JSON
  wait/rusage/stdout/stderr/parsed-result row, complete source and Git-control
  rows, runtime/module/boot/publisher identities, publication-local sampler
  rows, and recomputed RSS upper. After marker/stage fsync, a no-subprocess
  final seal repeats those identities, proves no descendants, waits for a
  post-guard sample, stops/joins the sampler, requires only the publisher
  thread to remain, and takes the final self-resident/RUSAGE_SELF sample.
  Every final gap is at most one second, observed RSS is at most 2.8 GB, and
  the recomputed 25%-margin admission upper is at most 3.5 GB; only then does
  it license rename plus parent fsync. That RSS claim is a sampled empirical
  envelope, not a continuous bound; a sub-sample publisher spike remains
  possible despite the child high-water evidence and 25% policy headroom.
  Success measures at most 480 seconds of final pre-JSON work and assigns the
  later suffix a fixed 60-second accounting charge; failure uses the same
  charge after its mandatory final resume. The accounted sum is at most 540
  seconds, but the charge is not an observed or enforced upper on end-to-end
  close latency. No JSON-only or post-terminal mutation branch is legal, and
  rehearsal success retains `TC` and `TS`. Forward cutover requires exclusive
  hidden-stage creation plus successful parent fsync; an absent post-crash
  stage from the intervening window is pre-cutover, while an exact surviving
  stage conservatively locks its kind. An exact visible final is reusable
  only after a current-live terminal-parent fsync. The fixed 60 seconds are an
  accounting charge, while visible-directory existence attests the final seal.
- Every attempt binds the initial supervisor PID, kernel start identity, and
  boot digest. Every claimed-worker `wait4` appends one cumulative hash-bound
  claim/identity/status/byte-normalized-`ru_maxrss`/sample/deadline row. Each
  superseded identity is proved dead exactly once using only `wait4-reaped`,
  `double-process-identity-absence`, or `boot-identity-changed` with their
  frozen samples, statuses, rusage, deadlines, boot comparisons, and
  nullability. Kernel 14's receipt probe is not a child role. Git execution is
  limited to the three sequential twelve-child sets above: the first 24 rows
  live in `attempt.json` plus terminal JSON, and the last 12 live in the
  marker. Intermediate seals launch no process, no Git child overlaps a
  worker, and every Git child is wait-only, so a missing Git wait/rusage row is
  unclosable rather than a worker death proof. The deduplicated attempt-wide
  death union has at most 128 rows.
- Before spawn, the supervisor durably publishes a launch intent containing a
  nonce commitment and arithmetically derived 480-second work and distinct
  60-second reap deadlines. The bootstrap-only child inherits parent-liveness
  and publishes PID/start/boot birth as its first durable action. Only a
  validated launch/birth pair may enter claim, reservation, worker-ready, and
  capability release; every complete birth later joins exact wait/death
  evidence. Every arm-bearing boundary, cleanup intent, or interruption is
  durable before the work it governs, and no wait/death row may invent,
  extend, or recompute its deadlines.
- Darwin double absence admits only two zeroed-buffer `proc_pidinfo` samples
  50 ms to 1 s apart that are both zero/`ESRCH` or both full reads naming the
  same stable replacement PID/start identity. Target presence, mixed classes,
  changing replacement identity, permission or ABI failure, ambiguous
  zero/zero, malformed/short/oversize return, PID mismatch, or boot change
  fails. A compact common verdict/replacement plus two raw
  `[time,return_bytes,errno]` samples round-trips the evidence while preserving
  the 512-byte process-death-row cap.
- A reservation retains its creator-claim digest forever. Initial capability
  equality is direct; a resumed current claim must match the payload and
  worker-ready boundary and reach the unique reservation creator through a
  finite gap-free backward suffix whose links are interruption-authorized. No resume rewrites the reservation or
  equates the old claimant with its child.
- Every admitted interruption, including one at a trace or measurement
  boundary, resets thermal qualification. The suspended trace finishes but
  contributes no new-epoch thermal time; before a later warm trace, new
  contiguous panels in the reset
  `validation,research,research,validation` cycle must contribute at least 600
  successful seconds. A further interruption resets only that recovery epoch.
- At record `i`, replay timing has two fixed operands:
  `Rplus_i=duration_plus_ns_i=D_i+2*h_i` and
  `Aplus_i=admission_duration_plus_ns_i=Rplus_i+480000000000*r_i`.
  Predictor/reference operands use only `Rplus`; held/current operands and
  every cold, conservative/projected task, block, phase, combined, or final
  absolute projection or budget use `Aplus`. Raw `D` remains diagnostic
  timing and the successful-work stop clock. For measurement block `j`, `N_j`
  is its complete balanced-pair count. For
  `s in {overall,validation,research}`, `Rplus[j,s]` and `Aplus[j,s]` sum the
  corresponding fields over the named phase traces, excluding the `EQUAL`
  trace; `overall` combines validation and research. Stationarity is exactly
  `20*N_j*Rplus[j-1,s] >= 19*N_(j-1)*Aplus[j,s]`. For held-out block `j`,
  phase `p`, kernel `k`, and other blocks `a,b`, temporal reference is
  `H[j,p,k]=max(ceil_div(U[j,p,k]*Rplus[a,p,k],U[a,p,k]),`
  `ceil_div(U[j,p,k]*Rplus[b,p,k],U[b,p,k]))`, with
  `H[j,p]=sum_{k:U[j,p,k]>0} H[j,p,k]` and
  `Aplus[j,p] <= ceil_div(5*H[j,p],4)`. For other phase `q` and
  `C={1,2,3,4,5,6,7,8,9,10,14}`, cross-context reference is
  `X[j,p,k]=max(ceil_div(U[j,p,k]*Rplus[a,q,k],U[a,q,k]),`
  `ceil_div(U[j,p,k]*Rplus[b,q,k],U[b,q,k]))`; require both
  `Aplus[j,p,k] <= ceil_div(5*X[j,p,k],4)` for every `k in C` and
  `sum_C Aplus[j,p,k] <= ceil_div(5*sum_C X[j,p,k],4)`.
  With raw `D`, units `U`, and resolution `h` fixed, incrementing each replay
  count separately must leave all reference `Rplus`, `H`, and `X` operands
  unchanged, weakly increase every affected held/current `Aplus` and dependent
  absolute projection, leave successful-work stop clocks unchanged, and never
  change a stationarity, temporal, cross-context, task, phase, total, or
  overall acceptance Boolean from false to true.
- Only durably closed process segments preserve telemetry pass authority.
  Abrupt supervisor or direct boot loss records `"unknown-loss"` and sets
  fail-closed uppers to RSS `3,500,000,001`, checkpoint tree
  `2,000,000,001`, created roots `6,000,000,001`, and absolute workspace
  `30,000,000,001` bytes, selecting
  `"select-terminal-failure-telemetry-gap"` before new work. A completed
  segment keeps the maximum durable upper/current observed margin, never
  relabels a bound as observed, and never applies the 25% margin twice.
- Evidence admits at most 64 launch intents, 64 worker births, 64 worker
  claims, 63 interruptions, 4,096 traces,
  641 failure resumes, 512 terminal-cleanup rows, 128 attempt-wide
  process-death rows, 64 cumulative worker-wait rows, and 240 ASCII bytes per
  canonical path. Cleanup, death, and worker-wait rows are capped at 1,024,
  512, and 512 canonical bytes; the 131,072-byte non-row term is the exact
  intent with all three row arrays replaced by `[]`, so
  `512*1024 + 128*512 + 64*512 + 131072 = 753,664` bytes remains below the
  1,048,576-byte root-receipt cap. Before failure selection, a bound hit
  selects terminal failure before the one-past object is created. After
  selection, resume/death/encoding-cap exhaustion stops the consumed failure
  as forensically incomplete before mutation.

These remain unobserved engineering predictions. A025 changes no estimator,
truth value, interval, threshold, scientific trial, or registered
validation/research address. Implementation remains forbidden until the
sealed configuration, deterministic replay-count-increment falsifier, and
cross-document parity checks pass fresh independent methods, systems, and
schema review, the locked local suite, and hosted CI.

## A026 correction before implementation

Appended on 2026-08-06 before resource-run code, any rehearsal, or any
registered resource access. A022--A026 are the active authority. A026 preserves
all successful RNG sequences, kernels, estimators, budgets, artifact shapes,
and the `3/45/12/57+1/58/13/51/7` successful-rehearsal tuple. It supersedes
only A025's interruption-tainted timing branch, same-boot launch-only dead end,
and post-terminal-entry consumed-no-outcome branch.

Before implementation, the following falsifiable predictions are frozen:

- Every cold/equal/validation/research rate-bearing trace is uninterrupted
  from worker-ready through its trace boundary. Interruption selects ordinary
  terminal failure, the trace supplies no `N/U/Rplus/Aplus/H/X` or projection
  operand, and neither its suffix nor a replacement trace can enter admission.
  Every admitted rate record therefore has `replay_count=0` and
  `Rplus=Aplus`; a nonzero replay count is terminal failure, not a replay
  license.
  Interruption between completed rate traces preserves the earlier evidence
  but requires an uninterrupted fresh 600-second recovery-thermal cycle before
  the next warm trace. Interruption inside that cycle discards the partial
  thermal trace, consumes its address without reuse, and restarts the cycle and
  clock from zero.
- Each launch-intent directory contains its JSON/marker plus exact mode-`0600`
  `quiescence.lock` bytes. The supervisor holds an exclusive Darwin `flock`
  before the intent becomes visible; the bootstrap child inherits the sole
  duplicate open-file-object reference and cannot unlock, reopen, duplicate,
  pass, leak, unlink, replace, or share it with a descendant. A live holder
  makes a fresh independent `LOCK_EX|LOCK_NB` attempt return `EWOULDBLOCK`.
  After exact supervisor death, successful fresh-open acquisition of the same
  validated inode selects ordinary failure before capability release or
  `SeedSequence`; it is recorded as quiescence plus the separate named death
  proof, never as PID-only child death.
- Exact launch crash fixtures cover the locked hidden intent, payload-only and
  marker-complete intent, uncertain rename, pre-spawn, post-spawn/pre-birth,
  hidden birth, complete birth, claim, worker-ready, and capability-release
  cuts. Wrong inode/path/type/mode/link/content, unsupported locking,
  `LOCK_UN`, descriptor duplication/passing, or an unproved descendant fails
  closed without new work.
- After an exact success or failure terminal-entry object, publisher death or
  any post-entry Git/process/sampler/seal/publication failure can close only as
  `terminal/nonpass/{nonpass.json,_NONPASS}`. An ordinary
  `resource-terminal-nonpass-intent-v1` first freezes the selected kind, exact
  entry bytes/location, death/failure evidence, selected hidden-stage state,
  and locked `publication.lock`. The visible files are pure functions of that
  intent, contain `admission_pass=false` and `retry_permitted=false`, perform no
  Git retry or RNG/timing work, and cannot coexist with visible success or
  failure.
- Crash injection at every nonpass-intent/stage/rename/fsync cut produces the
  same final bytes after any number of successor deaths. A successor may
  rebuild only while holding a fresh lock on the same intent inode. A visible
  nonpass consumes the attempt, never licenses the same seed again, and uses
  the existing fixed 60-second terminal accounting charge without claiming an
  observed publication-latency bound.
- A fresh deterministic verifier reproduces exactly 9,799 ASCII config bytes,
  SHA256
  `3408b35d27dc0b8415f18120357b822cf283f67ad463a4db8ff7b15235442f29`,
  194 leaf-type rows, and type-tree SHA256
  `e922c59028670e70c9d45c37ef4a8101b984d30eff0bdea0ed32c514897ec6e3`.
  The maximum nonpass intent is 131,072 bytes; every terminal file remains at
  most 1 MiB, and every one-past mutation fails before stage creation.

These are unobserved engineering predictions. Amendment A026 changes no
estimator, truth value, interval, threshold, scientific trial, or registered
validation/research address. Implementation remains forbidden until fresh
independent methods, systems, and schema reviews pass this settled package,
followed by the locked local suite and hosted CI.

## A027 deterministic representation prediction

Before implementation, the repository has no paper-cache index or pack/unpack
API. A focused test that requests the first, boundary, transposition-sensitive,
loss-kind, and last fields of the 8,460-vector must therefore fail because the
API is absent. After the smallest licensed implementation:

- research indices follow `900*m + 30*i + j` for nine matrices and
  `8100 + 60*s + 2*i + ell` for six response-level loss tables;
- recovery indices follow `30*i + j` and `900 + 2*i + ell`, and recovery is
  rejected as a research prefix;
- asymmetric literal sentinels round-trip without row/column transpose or
  SSE/SST reversal;
- exact finite float64 shape/type checks fail closed, output vectors are
  owned, C-contiguous, and read-only, and source mutation cannot change them;
- the order manifest reproduces 1,057 canonical bytes and SHA256
  `8810471ce6c0747af7cdda48299989303cd85a9c7def7c681f2a57f93348a083`;
  and
- the A027 resource config reproduces 10,863 ASCII bytes, SHA256
  `1a14fd68012819d5f901a97ddd9e9a58dd35886bdcc5d47728467f6417fc3cd3`,
  209 leaf rows, 10,369 type-tree bytes, and type-tree SHA256
  `81eed87be58bf04a897fdcf3dd39cf142944647824a9f97938d46f341803a2ff`.

Any different matrix/spec/kind order, a transposed coefficient, inclusion of
an intercept or factor coefficient, a false 960-prefix assumption, or an NPY
writer/resource fixture in this slice falsifies A027. These are deterministic
engineering predictions, not resource-feasibility or scientific outcomes. No
random-number constructor or data access is licensed.
