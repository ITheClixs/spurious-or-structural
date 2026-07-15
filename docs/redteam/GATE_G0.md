# Red-team memo — G0 environment and compute plan

Review date: 2026-07-15

## Verdict before hosted CI

**G0 remains in progress.** The candidate is locally reproducible and ready to
commit, but the gate cannot pass until the reviewed commit reproduces on hosted
CI. No G1 work is permitted while that evidence is missing.

The claim under attack is deliberately narrow: the repository has a real,
deterministic, resource-bounded software skeleton and a conditional plan that
cannot exceed the stated laptop budgets if its guards are implemented. This is
not a claim that the data exist, the identification design works, or cross-impact
is structural.

## Evidence available locally

- `uv lock --check` resolves the pinned 12-package environment without changing
  the lock.
- The locked parity suite runs Ruff, formatting, strict mypy, pytest, the demo,
  and a scoped diff check for committed demo artifacts.
- Two clean post-review demos each completed in 0.04 seconds. Maximum RSS was
  28,180,480 and 28,229,632 bytes, far below 4 GB.
- Both runs emitted exactly 64 records. JSONL, summary, and `_SUCCESS` were
  byte-identical with SHA256 values recorded in `SPECIFICATION_LOG.md`.
- Fault injection interrupts the second publish replacement, proves `_SUCCESS`
  is absent for the mixed pair, then proves the next run recovers with matching
  data and summary hashes.
- `data/manifest.json` records no external datasets and zero external bytes.
- The projected ledger is 348.6 GB lifetime download, 25.0 GB steady disk, and
  29 GB guarded transient peak. The dense-phase RAM design is 3.345 GB with an
  abort at 3.7 GB.

## Attacks

### 1. The budget could be spreadsheet theater

The 150 MB/symbol-day and 50 bytes/retained-bin inputs have not been measured.
Averages could hide BTC event-day tails, delisted-contract oddities,
decompression spill, or atomic-write duplication. If either estimate is wrong,
the nominal 51.4 GB lifetime-download headroom can disappear quickly.

**Response:** the plan labels both figures untested, reserves retries, caps a
single archive, checks disk before each work unit, stops lifetime requests at
360 GB, and forbids bulk acquisition until G3 measures the distribution. This
prevents a hardware-limit violation but does not prove scientific feasibility.

### 2. The RAM proof may hide simultaneous copies

Dense GMM code often creates undocumented factorization and BLAS temporaries.
Adding the base matrix and three additional copies would cross the internal
3.7 GB guard.

**Response:** the written design permits three dense weight/factorization
matrices total—the base plus two copies—two 64 MB columnar buffers, and 302 MB of
general array scratch. Together with a separate 1.5 GB overhead allowance, the
projection is 3.345 GB. A fourth dense copy is a design failure, not a reason to
raise the limit. Actual RSS remains a mandatory phase benchmark.

### 3. The demo could be scaffold theater

A deterministic integer generator does not exercise Parquet, matrix algebra,
inference, checkpoint resumption, or the eventual money figure.

**Response:** exercising those paths now would invent schemas before G3 and
implement estimators before G1. The G0 demo instead proves config parsing,
streaming, deterministic serialization, hashing, locked failure-safe
publication, CLI packaging, and clean regeneration. It is a skeleton, not the
final demo, and README says so prominently.

### 4. Seed determinism could still fail across platforms

Same-machine double runs do not prove a clean Linux runner will reproduce the
committed bytes. Tool or interpreter drift could silently update results.

**Response:** the generator uses explicit unsigned 64-bit integer operations,
JSON keys are sorted, timestamps and absolute paths are excluded, Python and uv
are pinned, and CI runs the demo then fails if `results/demo` differs. This
response is incomplete until hosted CI is green.

### 5. Atomic files are not an atomic artifact set

The first implementation replaced data before summary. Interruption could leave
a new data file beside a stale summary that appeared usable.

**Response:** hostile review killed that implementation. The replacement stages
files on the same filesystem, serializes publication with `flock`, removes the
old validity marker, replaces data and summary, and writes a hash-bearing
`_SUCCESS` last. The injected-failure regression validates the invalidation and
recovery contract.

### 6. Preregistration could be cosmetic

The method, exact dates, venue, and final event definitions remain unresolved.
Calling this a frozen preregistration could disguise later discretion.

**Response:** the frozen core fixes hypotheses, numeric kill criteria, universe
formation logic, discovery cap/date rule, headline bin sweep, holdout policy,
and the diagnosis-before-method selection rule. Exact choices that cannot be
made before schema discovery require dated append-only amendments before their
data are requested. The full specification trial count remains public.

### 7. Resumability is only prose

No long research job currently proves eight-minute checkpoint recovery.

**Response:** G0 defines the work units, transition state machine, atomic commit
ordering, checkpoint interval, and stop guards. There is no long job yet to
resume. The first G1 job longer than ten minutes must supply an interruption and
resume regression before its result is admissible.

### 8. CI may be unavailable

The local GitHub CLI reports an invalid token. A workflow file and local green
run are not hosted evidence.

**Response:** the configured Git remote may use a separate credential helper,
so the candidate will be committed and a normal push attempted. If push or CI
cannot run, G0 stays open. Authentication is not silently waived.

## Strongest objection not yet answered

The data-capacity plan is conditional on archive and compression distributions
that have never been observed. Hard counters make the design safe for the
laptop, but they cannot guarantee that a scientifically adequate sample fits.
Only G3 byte-level evidence can answer that. If it fails, the project must
redesign and preregister the sample or report the budget infeasibility; it may
not quietly degrade features or omit difficult instruments.

## Gate decision

- Local engineering and compute-plan candidate: **ready for commit** after the
  final parity run.
- Hosted reproduction: **pending**.
- G0 overall: **not passed**.
- G1: **locked**.
