# xid

[![CI](https://github.com/ITheClixs/spurious-or-structural/actions/workflows/ci.yml/badge.svg)](https://github.com/ITheClixs/spurious-or-structural/actions/workflows/ci.yml)

`xid` asks whether apparent cross-asset price impact is structural, or whether
latent common factors and same-bin feedback make ordinary return-on-flow
regressions look structural when they are not.

**Current claim: none.** G0, the engineering and compute-plan gate, has passed;
G1, the symbolic derivation gate, is open but not started. No external market
data has been accessed, no estimator has been validated, and the holdout does
not yet exist. The eventual money figure is therefore deliberately locked.

## Reproduce the G0 smoke path

```bash
make demo
```

The command reads a versioned configuration and streams a deterministic
synthetic record set. It stages the data and row-count-and-hash manifest,
publishes them under a file lock, then writes `results/demo/_SUCCESS` last. An
artifact set is valid only when that marker exists and its data and summary
hashes match. The demo performs no regression and supports no market claim. Its
purpose is to prove that the package, configuration, output, and reproducibility
surfaces work before research code is allowed to exist.

Run the complete local parity suite with:

```bash
make check
```

## Gate status

| Gate | Status | Evidence |
| --- | --- | --- |
| G0 environment and compute plan | Passed | `docs/COMPUTE_PLAN.md`, deterministic demo, CI run `29416847411` |
| G1 derivation | Open | Algebra and pre-run predictions precede simulation code |
| G2 premise kill switch | Locked | Requires G1 pass |
| G3-G8 | Locked | Sequential gate discipline |

The exact research state and next action live in `STATE.md`. Failed approaches
remain visible in `SPECIFICATION_LOG.md`; assumptions and decision rationales
live in their corresponding ledgers.

## Limitations at G0

- The data-size and throughput envelope is a conditional projection until G3
  measures real archives byte by byte.
- The smoke sample is deliberately synthetic and does not resemble or validate
  a market-generating process.
- A green local run is not a substitute for a green hosted CI run on the same
  commit.
- No statement about the existence, sign, magnitude, identifiability, or
  economic value of cross-impact is warranted.
