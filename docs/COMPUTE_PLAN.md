# Compute and data plan

Status: G0 projection, version 0.1, 2026-07-15. No external market archive has
been inspected. All archive-size and compression figures below are explicit
assumptions with G3 stop/go tests; hard byte counters prevent an assumption
failure from violating the machine limits.

## Operating point and safety rules

- Planning dimensions: `N = 30` assets, `K = 3` latent factors, `S = 4`
  variance regimes.
- One thermally heavy driver at a time. No process may exceed 3.7 GB RSS; the
  target is 3.5 GB and the hard project limit is 4 GB.
- Work units are one symbol-date for ETL, one parameter-cell/seed for Monte
  Carlo, and one multistart or bootstrap shard for estimation.
- Checkpoints occur at most every eight minutes. A crash must lose less than ten
  minutes of completed work.
- Overnight jobs use `caffeinate -i`, but resumability never depends on it.
- At 80% of a phase's hard wall budget, the driver recomputes projected
  completion time and stops if the cap would be crossed.

## Provisional sample envelope

This is a capacity envelope, not permission to download. Exact sources, dates,
event definitions, and inclusion probabilities must be frozen in a
preregistration amendment before their first request.

| Use | Dates | Symbols | Retained window |
| --- | ---: | ---: | ---: |
| Schema/calibration pilots, excluded from inference | 4 | 30 | full day |
| Training, 12 dates per regime | 48 | 30 | 6 hours |
| Sealed holdout, 4 dates per regime | 16 | 30 | 6 hours |

The sampling frame uses externally timestamped event strata plus calendar-block
matched controls. For sampled unit `i` in stratum `s`, the estimator records
`pi_i = n_s / N_s` and uses `w_i = 1 / pi_i`. Resampling preserves event/date
clusters and those design weights. Pilot, train, and holdout dates are mutually
disjoint.

## Lifetime download arithmetic

Assumption A001 caps the combined compressed input at 150 MB per symbol-day.
There are `30 * (4 + 48 + 16) = 2,040` planned symbol-days. Including a 10%
retry/checksum allowance:

```text
market archives = 2,040 * 0.150 GB * 1.10 = 336.6 GB
schema probes beyond retained pilots             =   8.0 GB
environment and reference reserve                =   4.0 GB
planned lifetime total                           = 348.6 GB
hard limit                                       = 400.0 GB
headroom                                          = 51.4 GB
```

The downloader maintains an append-only byte ledger and refuses to start a
request whose declared or conservative maximum would push lifetime downloads
above 360 GB. The final 40 GB is failure-recovery reserve, not sample capacity.
If G3 measures a universe-weighted mean above 150 MB per symbol-day, the sample
must be redesigned and preregistered before any bulk request.

## Retained-row and steady-disk arithmetic

At the finest planned retained clock of 250 ms:

```text
pilot rows   = 4 * 30 * 24 * 3,600 * 4 =  41.472 million
train rows   = 48 * 30 * 6 * 3,600 * 4 = 124.416 million
holdout rows = 16 * 30 * 6 * 3,600 * 4 =  41.472 million
total rows                                  207.360 million
```

At the A002 ceiling of 50 compressed bytes per symbol-bin, the feature lake is
`207.36e6 * 50 = 10.368 GB`.

| Persistent allocation | Cap |
| --- | ---: |
| Environment, source, and local caches | 2.0 GB |
| Partitioned feature Parquet | 10.4 GB |
| Monte Carlo outputs and resumable checkpoints | 4.0 GB |
| Estimation/bootstrap sufficient-statistic shards | 3.0 GB |
| Results, figures, demo, and paper | 2.0 GB |
| Unallocated safety margin | 3.6 GB |
| **Steady-state hard maximum** | **25.0 GB** |

Raw is transient. The ETL state transition is:

```text
pending -> downloaded -> parsed -> validated -> committed -> raw_deleted
```

Only one symbol-day may be raw. Before a download, persistent usage must be at
most 23 GB. The largest permitted compressed archive is 4 GB and temporary
output/spill is capped at 2 GB; the driver checks that the projected peak is at
most 29 GB before starting. Output is atomically renamed only after schema,
SHA256, and row-count validation, then raw is deleted.

## RAM arithmetic

A 100,000-observation simulation chunk with `2N + K = 63` float64 entries per
row occupies `100,000 * 63 * 8 = 50.4 MB` per full workspace. Six such
workspaces occupy 302.4 MB. Simulation and dense GMM phases do not run
concurrently; the same 302.4 MB is retained below as a conservative dense-phase
scratch allowance rather than counted twice.

At the brief's approximate G5 dimensions:

```text
Jacobian: 7,320 * 2,200 * 8 bytes                = 128.8 MB
weight matrix plus two factorization copies     =   1.286 GB
two 64 MB Arrow/Polars buffers                   =   0.128 GB
general dense-phase array scratch                =   0.302 GB
```

The factorization line is three simultaneously live dense matrices **total**,
including the base weight matrix. The named dense-phase allocations total about
1.845 GB. A separate 1.5 GB interpreter, library, allocator, and unlisted
overhead allowance gives 3.345 GB, leaving about 155 MB below the 3.5 GB target
and 355 MB below the 3.7 GB abort guard. Bootstrap jobs operate on block
sufficient statistics; multiprocessing that duplicates the feature lake or
dense matrices is forbidden. If measured factorization requires a fourth dense
copy, the job fails this design and must use an in-place or structured method.

## Machine wall-clock budgets

Budgets exclude reading, derivation, and writing time. They use thermally
sustained throughput. Before a phase with more than one hour of compute, use:

```text
budgeted time = 1.25 * planned work /
                min(measured warm throughput, 0.60 * cold throughput)
```

| Gate | Expected | Hard stop | Peak RSS | New download | Peak transient disk |
| --- | ---: | ---: | ---: | ---: | ---: |
| G0 scaffold, checks, demo | 4 h | 8 h | 1.5 GB | 2.0 GB | 4 GB |
| G1 streamed `10^7` verification | 3 h | 8 h | 1.5 GB | 0 | 4 GB |
| G2 calibrated premise frontier | 16 h | 32 h | 3.0 GB | 0 (uses reserved references) | 6 GB |
| G3 byte probes and ETL benchmarks | 8 h | 16 h | 2.5 GB | 27.8 GB | 12 GB |
| G4 Jacobian/recovery frontier | 36 h | 72 h | 3.5 GB | 0 | 14 GB |
| G5 failure diagnosis and scalable fits | 72 h | 120 h | 3.5 GB | 0 | 18 GB |
| G6 train acquisition and inference | 60 h | 96 h | 3.5 GB | 237.6 GB | 27 GB |
| G7 one holdout open and economics | 60 h | 96 h | 3.5 GB | 79.2 GB | 29 GB |
| G8 deterministic regeneration/write-up | 12 h | 24 h | 3.0 GB | 2.0 GB | 29 GB |

For G5, the 120-hour cap supports about 8,000 checkpointed fits only if the
thermally sustained median fit remains below 45 seconds. A slower candidate has
failed the laptop-scale requirement and must be structurally simplified rather
than brute-forced.

## Mandatory stop/go measurements

G3 must measure, rather than assume:

1. Mean, maximum, and tail compressed bytes per symbol-day for every required
   stream, including high-volume and delisted contracts.
2. Maximum raw archive size and whether range/stream decompression is possible.
3. Compressed bytes per retained 250 ms row after lossless column pruning and
   dictionary encoding.
4. Timestamp semantics, schema history, sequence gaps, symbol mappings,
   redenominations, and contract multipliers.
5. Thermally sustained parse, simulation, linear-algebra, and write throughput.
6. Availability of genuine forced-liquidation events with known size, side, and
   timestamp.

Any failed ceiling is recorded in `DECISIONS.md`. The response order is lossless
schema/encoding repair, then a preregistered sample redesign. Silent feature or
sample degradation is forbidden.
