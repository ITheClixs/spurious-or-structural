"""Which functionals of the impact matrix survive non-identification.

Every member of the identified set has the form ``Lambda = A - Gamma W'`` with
``W = Sigma_qq^{-1} Delta_f``, so a functional is point identified exactly when
the ``Gamma W'`` term cannot move it. For both linear and quadratic functionals
the condition falls on the **flow argument** alone: ``a' Lambda b`` is
identified if and only if ``W' b = 0``, and ``x' Lambda x`` if and only if
``W' x = 0``.

The published dollar-neutral cost corollary is the one-spike instance of that
second statement and holds for no other reason: there ``col(W) = span(m)``, so
``W' x = 0`` reduces to ``m' x = 0``.

See ``docs/derivations/IDENTIFIED_FUNCTIONALS.md``. Deterministic linear
algebra only. No random-number generator, no registered stream, no market data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

__all__ = (
    "FunctionalVerdict",
    "confounding_directions",
    "identified_width",
    "is_point_identified",
    "width_attaining_loading",
)

Matrix = NDArray[np.float64]
Vector = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class FunctionalVerdict:
    """Whether one functional survives, and how wide its interval is."""

    exposure: float
    """``||W' x||``, the flow argument's reach into the confounding subspace."""

    point_identified: bool
    width: float
    """``2 R ||x|| ||W' x||`` for quadratic functionals; zero when identified."""


def _validate_array(value: object, name: str, ndim: int) -> Matrix:
    if not isinstance(value, np.ndarray) or type(value) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray")
    if value.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {value.dtype}")
    if value.ndim != ndim:
        raise ValueError(f"{name}: expected {ndim} dimensions, got {value.ndim}")
    if not np.isfinite(value).all():
        raise ValueError(f"{name}: expected finite entries")
    return value


def confounding_directions(
    flow_covariance: Matrix,
    flow_factor_loading: Matrix,
) -> Matrix:
    """Return ``W = Sigma_qq^{-1} Delta_f``, whose columns span the lost space.

    A functional's flow argument is identified precisely when it is orthogonal
    to ``col(W)``.
    """
    sigma = _validate_array(flow_covariance, "flow_covariance", 2)
    delta = _validate_array(flow_factor_loading, "flow_factor_loading", 2)
    n = sigma.shape[0]
    if sigma.shape[1] != n:
        raise ValueError(f"flow_covariance: expected a square matrix, got {sigma.shape}")
    if delta.shape[0] != n:
        raise ValueError(
            f"flow_factor_loading: expected {n} rows to match the flow covariance, "
            f"got {delta.shape[0]}"
        )
    symmetric = (sigma + sigma.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(symmetric)
    scale = max(1.0, float(np.abs(symmetric).max()))
    if float(eigenvalues.min()) <= scale * 1e-12:
        raise ValueError(
            "flow_covariance: expected a positive definite matrix; the smallest "
            f"eigenvalue is {float(eigenvalues.min()):.3e}"
        )
    return np.ascontiguousarray(np.linalg.solve(symmetric, delta))


def _exposure(w: Matrix, flow_argument: Vector) -> tuple[float, float]:
    directions = _validate_array(w, "w", 2)
    argument = _validate_array(flow_argument, "flow_argument", 1)
    if argument.shape[0] != directions.shape[0]:
        raise ValueError(
            f"flow_argument: expected length {directions.shape[0]} to match w, "
            f"got {argument.shape[0]}"
        )
    norm = float(np.linalg.norm(argument))
    if norm == 0.0:
        raise ValueError("flow_argument: expected a nonzero vector")
    return float(np.linalg.norm(directions.T @ argument)), norm


def is_point_identified(w: Matrix, flow_argument: Vector, rtol: float = 1e-10) -> bool:
    """Whether a functional with this flow argument is point identified.

    True exactly when ``W' b = 0`` up to ``rtol`` relative to ``||b||`` scaled
    by the largest singular value of ``W``. The response argument of a linear
    functional plays no role, which is the content of Theorem A's asymmetry.
    """
    if rtol <= 0.0:
        raise ValueError("rtol: expected a positive relative tolerance")
    exposure, norm = _exposure(w, flow_argument)
    scale = float(np.linalg.svd(w, compute_uv=False)[0]) * norm
    if scale == 0.0:
        return True
    return exposure <= scale * rtol


def identified_width(w: Matrix, trade: Vector, radius: float) -> FunctionalVerdict:
    """Width of the identified interval for the execution cost ``x' Lambda x``.

    Equals ``2 R ||x|| ||W' x||`` when the admissible loadings satisfy
    ``||Gamma||_F <= radius``. Zero exactly when the trade is confounding
    orthogonal.
    """
    if not np.isfinite(radius) or radius < 0.0:
        raise ValueError("radius: expected a finite nonnegative loading bound")
    exposure, norm = _exposure(w, trade)
    return FunctionalVerdict(
        exposure=exposure,
        point_identified=is_point_identified(w, trade),
        width=2.0 * radius * norm * exposure,
    )


def width_attaining_loading(w: Matrix, trade: Vector, radius: float) -> Matrix:
    """The loading ``Gamma*`` at which the upper endpoint of the width is met.

    ``Gamma* = R (x w') / ||x w'||_F`` with ``w = W' x``. Refuses a
    confounding-orthogonal trade, where the interval is a point and no
    maximiser is defined.
    """
    if not np.isfinite(radius) or radius < 0.0:
        raise ValueError("radius: expected a finite nonnegative loading bound")
    exposure, _ = _exposure(w, trade)
    if is_point_identified(w, trade):
        raise ValueError(
            "trade: the cost is point identified for this trade, so the identified "
            "interval is a single point and no attaining loading exists"
        )
    outer = np.outer(trade, w.T @ trade)
    return np.ascontiguousarray(radius * outer / np.linalg.norm(outer))
