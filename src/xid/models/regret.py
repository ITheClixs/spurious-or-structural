"""What a trader loses by optimising against a confounded impact matrix.

The partial-identification results say the impact matrix cannot be pinned down.
They do not say what that costs. For a trader minimising quadratic cost subject
to one linear constraint, the loss from acting on ``A_s = Lambda_s + G_s``
instead of the truth obeys an exact identity,

```
Regret = delta' Lambda_s delta,    delta = x(A_s) - x(Lambda_s),
```

so it is the true cost of the *error in the trade* rather than of the error in
the matrix. Expanding in the size of the gap makes the practical point: a
first-order error in the matrix produces only a second-order loss in execution.

See ``docs/derivations/EXECUTION_REGRET.md``. Deterministic linear algebra
only. No random-number generator, no registered stream, no market data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

__all__ = (
    "RegretDecomposition",
    "execution_regret",
    "optimal_trade",
    "regret_leading_constant",
)

Matrix = NDArray[np.float64]
Vector = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class RegretDecomposition:
    """The cost of acting on a confounded matrix, and where it comes from."""

    regret: float
    """``x_A' Lambda_s x_A - x_L' Lambda_s x_L``, never negative."""

    optimal_cost: float
    """``x_L' Lambda_s x_L``, the cost under the true matrix."""

    trade_error: Vector
    """``delta = x_A - x_L``. Satisfies ``c' delta = 0``."""

    @property
    def relative_regret(self) -> float:
        """Regret as a fraction of the cost a fully informed trader would pay."""
        return self.regret / self.optimal_cost


def _symmetric_positive_definite(name: str, value: object, n: int | None = None) -> Matrix:
    if not isinstance(value, np.ndarray) or type(value) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray")
    if value.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {value.dtype}")
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise ValueError(f"{name}: expected a square matrix, got shape {value.shape}")
    if n is not None and value.shape[0] != n:
        raise ValueError(f"{name}: expected {n} rows to match the constraint, got {value.shape[0]}")
    if not np.isfinite(value).all():
        raise ValueError(f"{name}: expected finite entries")
    symmetric = np.ascontiguousarray((value + value.T) / 2.0)
    smallest = float(np.linalg.eigvalsh(symmetric).min())
    if smallest <= max(1.0, float(np.abs(symmetric).max())) * 1e-12:
        raise ValueError(
            f"{name}: expected a positive definite symmetric part; the smallest "
            f"eigenvalue is {smallest:.3e}. Cost minimisation is unbounded otherwise"
        )
    return symmetric


def _constraint(value: object) -> Vector:
    if not isinstance(value, np.ndarray) or type(value) is not np.ndarray:
        raise ValueError("constraint: expected exactly numpy.ndarray")
    if value.dtype != np.float64:
        raise ValueError(f"constraint: expected float64, got {value.dtype}")
    if value.ndim != 1:
        raise ValueError(f"constraint: expected one dimension, got {value.ndim}")
    if not np.isfinite(value).all():
        raise ValueError("constraint: expected finite entries")
    if float(np.linalg.norm(value)) == 0.0:
        raise ValueError("constraint: expected a nonzero vector; c' x = 1 is infeasible at zero")
    return value


def optimal_trade(cost_matrix: Matrix, constraint: Vector) -> Vector:
    """Return ``argmin x' M x`` subject to ``c' x = 1``.

    Only the symmetric part of ``cost_matrix`` enters, since
    ``x' M x = x' sym(M) x``.
    """
    c = _constraint(constraint)
    m = _symmetric_positive_definite("cost_matrix", cost_matrix, c.shape[0])
    solved = np.linalg.solve(m, c)
    trade: Vector = np.ascontiguousarray(solved / float(c @ solved))
    return trade


def execution_regret(
    true_cost: Matrix,
    believed_cost: Matrix,
    constraint: Vector,
) -> RegretDecomposition:
    """Cost of executing the trade that is optimal under ``believed_cost``.

    Non-negative by construction: the informed trade minimises the true cost
    over the same constraint set.
    """
    c = _constraint(constraint)
    truth = _symmetric_positive_definite("true_cost", true_cost, c.shape[0])
    belief = _symmetric_positive_definite("believed_cost", believed_cost, c.shape[0])
    informed = optimal_trade(truth, c)
    acted = optimal_trade(belief, c)
    error = np.ascontiguousarray(acted - informed)
    return RegretDecomposition(
        regret=float(error @ truth @ error),
        optimal_cost=float(informed @ truth @ informed),
        trade_error=error,
    )


def regret_leading_constant(
    true_cost: Matrix,
    gap: Matrix,
    constraint: Vector,
) -> float:
    """The coefficient of ``eps^2`` in the regret from a gap ``eps * gap``.

    Equals ``(Pi G_s x_L)' Lambda_s^{-1} (Pi G_s x_L)`` with
    ``Pi = I - c c' Lambda_s^{-1} / (c' Lambda_s^{-1} c)``. Zero exactly when
    the gap moves the optimal trade only along the constraint direction, in
    which case the trader's action — and so the trader's cost — is unchanged.
    """
    c = _constraint(constraint)
    truth = _symmetric_positive_definite("true_cost", true_cost, c.shape[0])
    if not isinstance(gap, np.ndarray) or gap.shape != truth.shape:
        raise ValueError(f"gap: expected a numpy.ndarray of shape {truth.shape}")
    if gap.dtype != np.float64 or not np.isfinite(gap).all():
        raise ValueError("gap: expected finite float64 entries")
    symmetric_gap = (gap + gap.T) / 2.0
    informed = optimal_trade(truth, c)
    weighted = np.linalg.solve(truth, c)
    projected = symmetric_gap @ informed
    projected = projected - c * float(weighted @ projected) / float(c @ weighted)
    return float(projected @ np.linalg.solve(truth, projected))
