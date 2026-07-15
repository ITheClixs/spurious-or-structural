# Methodology status

No identification estimator has been chosen.

That absence is deliberate: the operating brief makes method discovery the
research contribution and requires diagnosis before search. G1 must first
derive the probability limits of naive and noisy-control OLS and verify them in
simulation. G4 then proves or rejects an identification strategy by its
true-parameter Jacobian, recovery, and failure frontier. G5 may replace a naive
estimator only after at least two failure modes are demonstrated numerically.

The G0 implementation therefore contains only a deterministic configuration,
streaming, hashing, atomic-write, and CLI smoke path. It contains no structural
simulation, OLS, GMM, bootstrap, or empirical-data logic.
