"""A cross-block rank test that does not pretend high-frequency bins are independent.

Theorem 9 fixes ``sigma_{K+1}(A_{I,J})`` at zero in population. Estimated, it is
positive almost surely, so testing needs a null distribution. Two choices make
this procedure what it is.

The bootstrap is recentred on the rank-``K`` truncation of the observed block,
because the null constrains a singular value rather than a parameter; without
recentring the resampled statistic has no reason to behave like a null draw.

Resampling is over whole dates. Order flow and returns are serially correlated
within a trading day, and a scheme that resamples bins independently asserts an
independence the data does not have — in simulation it rejects a true null in
every replication.

See ``docs/derivations/CROSS_BLOCK_INFERENCE.md``. Randomness enters only
through an explicitly supplied generator; no registered stream and no market
data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

__all__ = (
    "CrossBlockTest",
    "DateStatistics",
    "accumulate_dates",
    "cross_block_pvalue",
    "weighted_coefficients",
)

Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class DateStatistics:
    """Per-date sufficient statistics for the coefficient matrix."""

    return_flow: Matrix
    """``S_rq[d] = sum_t r_t q_t'`` stacked over dates, shape ``(D, N, N)``."""

    flow: Matrix
    """``S_qq[d] = sum_t q_t q_t'`` stacked over dates, shape ``(D, N, N)``."""

    @property
    def date_count(self) -> int:
        return int(self.return_flow.shape[0])


@dataclass(frozen=True, slots=True)
class CrossBlockTest:
    """Outcome of one cross-block rank test."""

    statistic: float
    """``sigma_{K+1}`` of the observed disjoint block."""

    p_value: float
    date_count: int
    """Reported alongside the p-value: a short panel has little power."""

    draws: int


def _validate_panel(returns: Matrix, flow: Matrix) -> tuple[int, int, int]:
    for name, value in (("returns", returns), ("flow", flow)):
        if not isinstance(value, np.ndarray) or type(value) is not np.ndarray:
            raise ValueError(f"{name}: expected exactly numpy.ndarray")
        if value.dtype != np.float64:
            raise ValueError(f"{name}: expected float64, got {value.dtype}")
        if value.ndim != 3:
            raise ValueError(f"{name}: expected (dates, bins, assets), got {value.ndim} dimensions")
        if not np.isfinite(value).all():
            raise ValueError(f"{name}: expected finite entries")
    if returns.shape != flow.shape:
        raise ValueError(
            f"returns and flow must agree in shape, got {returns.shape} and {flow.shape}"
        )
    dates, bins, assets = (int(x) for x in returns.shape)
    if dates < 2:
        raise ValueError(f"expected at least two dates to resample, got {dates}")
    if bins < 1 or assets < 1:
        raise ValueError(f"expected a nonempty panel, got {bins} bins and {assets} assets")
    return dates, bins, assets


def accumulate_dates(returns: Matrix, flow: Matrix) -> DateStatistics:
    """Reduce a ``(dates, bins, assets)`` panel to per-date sufficient statistics.

    Resampling then costs a weighted sum of small matrices rather than a pass
    over the panel, and the reduction is exact: no information the coefficient
    matrix uses is discarded.
    """
    _validate_panel(returns, flow)
    return DateStatistics(
        return_flow=np.ascontiguousarray(np.einsum("dta,dtb->dab", returns, flow)),
        flow=np.ascontiguousarray(np.einsum("dta,dtb->dab", flow, flow)),
    )


def weighted_coefficients(statistics: DateStatistics, weights: Matrix | None = None) -> Matrix:
    """Return ``A(w) = [sum_d w_d S_rq^d][sum_d w_d S_qq^d]^{-1}``."""
    if weights is None:
        numerator, denominator = statistics.return_flow.sum(0), statistics.flow.sum(0)
    else:
        if weights.shape != (statistics.date_count,):
            raise ValueError(
                f"weights: expected shape {(statistics.date_count,)}, got {weights.shape}"
            )
        if not np.isfinite(weights).all() or float(weights.min()) < 0.0:
            raise ValueError("weights: expected finite nonnegative date weights")
        numerator = np.tensordot(weights, statistics.return_flow, axes=1)
        denominator = np.tensordot(weights, statistics.flow, axes=1)
    symmetric = (denominator + denominator.T) / 2.0
    scale = max(1.0, float(np.abs(symmetric).max()))
    if float(np.linalg.eigvalsh(symmetric).min()) <= scale * 1e-12:
        raise ValueError(
            "resampled flow covariance is singular; the draw carries too few "
            "distinct dates to identify the coefficient matrix"
        )
    coefficients: Matrix = np.linalg.solve(symmetric.T, numerator.T).T
    return np.ascontiguousarray(coefficients)


def _block(coefficients: Matrix, rows: tuple[int, ...], columns: tuple[int, ...]) -> Matrix:
    overlap = set(rows) & set(columns)
    if overlap:
        raise ValueError(
            "rows and columns must be disjoint; the diagonal enters the block "
            f"otherwise, and indices {sorted(overlap)} appear in both"
        )
    return np.ascontiguousarray(coefficients[np.ix_(list(rows), list(columns))])


def cross_block_pvalue(
    statistics: DateStatistics,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    k: int,
    generator: np.random.Generator,
    draws: int = 299,
) -> CrossBlockTest:
    """Date-cluster bootstrap p-value for ``rank(A_{I,J}) <= k``.

    Whole dates are resampled with replacement, so within-day dependence of any
    form is preserved without being modelled. The bootstrap is recentred on the
    rank-``k`` truncation of the observed block, which is what turns the
    resampled distribution into a null distribution.
    """
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError("k: expected a nonnegative int factor count")
    if not isinstance(draws, int) or isinstance(draws, bool) or draws < 1:
        raise ValueError("draws: expected a positive int replicate count")
    if not isinstance(generator, np.random.Generator):
        raise ValueError("generator: expected a numpy.random.Generator")

    observed_block = _block(weighted_coefficients(statistics), rows, columns)
    if min(observed_block.shape) <= k:
        raise ValueError(
            f"block of shape {observed_block.shape} has no singular value of index {k}; "
            f"the restriction is vacuous and cannot be tested at k = {k}"
        )
    left, singular, right = np.linalg.svd(observed_block)
    observed = float(singular[k])
    truncated = singular.copy()
    truncated[k:] = 0.0
    null_block = (left[:, : truncated.size] * truncated) @ right

    dates = statistics.date_count
    exceedances = 0
    for _ in range(draws):
        weights = np.bincount(generator.integers(0, dates, dates), minlength=dates).astype(
            np.float64
        )
        perturbation = (
            _block(weighted_coefficients(statistics, weights), rows, columns) - observed_block
        )
        resampled = float(np.linalg.svd(null_block + perturbation, compute_uv=False)[k])
        if resampled >= observed:
            exceedances += 1
    return CrossBlockTest(
        statistic=observed,
        p_value=exceedances / draws,
        date_count=dates,
        draws=draws,
    )
