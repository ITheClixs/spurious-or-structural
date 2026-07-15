# G0 pre-run prediction

Recorded: 2026-07-15, before the first configured `make demo` run.

Given `configs/demo.toml`, the smoke path should:

1. exit successfully in less than 300 seconds on the target M4 Air;
2. use far less than the 4 GB RSS ceiling;
3. emit exactly 64 deterministic records (`2 assets * 32 bins`);
4. write `results/demo/synthetic_bins.jsonl` and `summary.json` atomically;
5. reproduce both files byte for byte on a second clean run;
6. leave `data/manifest.json` at zero external bytes; and
7. report `research_claim = none` and
   `interval_status = not-applicable-no-statistical-claim`.

The prediction is falsified if any output differs between clean runs, any hash
does not match its artifact, the configured count is wrong, the command crosses
the resource/time limit, or the pipeline accesses external data. A mismatch is
diagnosed; the config is not tuned to make the output look more plausible.

## Post-run failure-safety refinement

Hostile review found that individually atomic files could still form a mixed
pair after an interrupted publish. The configured records, expected count, and
pre-run hashes were not changed. Publication now treats `_SUCCESS` as the commit
marker: it is removed before replacement and written last with hashes of the
data and summary. Without a valid marker, consumers must reject the artifact
set. A fault-injection test interrupts the second replacement and verifies both
invalidation and recovery on the next run.
