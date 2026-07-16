# G2 smooth panel completeness and fit authority

Written after the second C0003 hostile lane and before its repair. It narrows
software authority only; no stochastic law, estimator, threshold, target, or
inference rule changes.

## 1. Diagnosed failures

An ascending tuple is not necessarily a complete panel. If a failed date is
omitted, the old stack inferred a smaller `D`, accepted weights summing to that
smaller value, and produced an estimate. That violates the registered rule
that a required-date numerical failure invalidates the cell rather than being
dropped.

The old high-level fit functions also accepted self-consistent `N=2` or `N=3`
analytic aggregates while receiving the sealed `N=30` contract. Generic
linear algebra is useful for deterministic tests, but it must not be the same
call surface that licenses a G2 result.

## 2. Complete contract panel

Each contract-built date carries its full validated source coordinates:

```text
(stream, phase_id, scenario_id, n_dates, panel_index, date_index,
 filtered_base_identity)
```

For a contract panel, stacking requires:

1. one exact stream/phase/scenario/declared-`n_dates`/panel-index prefix;
2. `date_index` and record index agree for every date;
3. the tuple is exactly `range(n_dates)`, not merely ascending;
4. every source-base identity and design digest is retained in that order; and
5. base and cell panels have exactly equal source-coordinate and design-digest
   tuples before aggregation.

There is no option to shorten, sort, impute, or silently skip a contract panel.
A frontier panel remains valid because its minted provenance declares 48 or 96
dates; a 96-date prefix of a date-252 panel does not.

Analytic panels are a separate origin. They may use small dimensions and a
caller-declared finite date sequence for deterministic algebra tests, but they
are never accepted by a contract fit.

## 3. Split algebra from licensed fitting

The public pure-math path consists of:

```text
aggregate -> extract centered/proxy-partialled moments -> generic solver
```

Extraction does not receive a `G2Contract` and makes no claim that the input is
licensed. Generic solvers receive only the already validated numerical
threshold projection needed for their boundary tests.

The high-level G2 fit path first requires a contract-origin aggregate with:

```text
N == contract.n_assets == 30
T == contract.bins_per_date == 330
L == contract.n_levels == 10
complete minted panel provenance
row_mass == n_dates * T
```

Only then may it call the same extraction and solver kernels. The pooled fit has
the identical authority check. A dimension-generic aggregate, incomplete
contract panel, forged origin flag, or mismatched source tuple fails before a
coefficient is returned.

## 4. Pre-run predictions

Deterministic tests must show that:

1. dropping any middle or terminal date from a contract provenance tuple fails;
2. a 48/96 frontier declared at issuance is distinguishable from a truncated
   252-date panel;
3. base and cell panels from different streams, panel indices, or design
   digests fail before weighted multiplication;
4. high-level ridge and pooled fits reject analytic `N=2/3` aggregates and any
   contract-origin aggregate whose `N,T,L` differ from the sealed contract; and
5. the pure extraction-plus-solver path retains every existing deterministic
   coefficient and numerical-boundary result.

No 252-date stochastic estimator run is authorized by this document. Exact
test-seed recovery remains a later separately registered slice.
