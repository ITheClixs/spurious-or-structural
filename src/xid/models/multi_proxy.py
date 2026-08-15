"""Restoring identification of the structural impact matrix with two proxies.

One noisy factor proxy does not identify the structural matrix, because
``Cov(h,h)`` confounds the factor covariance with the measurement-error
covariance. Two proxies whose errors are uncorrelated with each other break
that confound: ``Cov(h1,h2)`` equals the factor covariance alone, which unlocks
the loading matrix and then the structural matrix itself.

The result identifies a **general** structural matrix, not merely a diagonal
one, and so is stronger than the cross-block restriction, which assumes the
diagonal null it is designed to falsify.

The independence assumption is brittle rather than approximate: see
``docs/derivations/MULTI_PROXY_IDENTIFICATION.md`` Section 4, where a
proxy-error correlation of ``0.1`` already produces 86% of the error at perfect
correlation.

Population moments only. No sampling theory, no random-number generator, no
registered stream, no market data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

__all__ = ("ProxyIdentification", "identify_with_two_proxies")

Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class ProxyIdentification:
    """Structural matrix and the intermediates identified along the way."""

    impact: Matrix
    factor_covariance: Matrix
    flow_loading: Matrix
    idiosyncratic_flow_covariance: Matrix


def _check(name: str, m: Matrix, shape: tuple[int, int]) -> None:
    if not isinstance(m, np.ndarray) or type(m) is not np.ndarray:
        raise ValueError(f"{name}: expected exactly numpy.ndarray")
    if m.dtype != np.float64:
        raise ValueError(f"{name}: expected float64, got {m.dtype}")
    if m.shape != shape:
        raise ValueError(f"{name}: expected shape {shape}, got {m.shape}")
    if not np.isfinite(m).all():
        raise ValueError(f"{name}: expected finite entries")


def identify_with_two_proxies(
    flow_covariance: Matrix,
    return_flow_covariance: Matrix,
    return_proxy_covariance: Matrix,
    flow_proxy_covariance: Matrix,
    proxy_cross_covariance: Matrix,
) -> ProxyIdentification:
    """Point identify the structural impact matrix from two proxies.

    Arguments are population second moments with ``Cov(x, y) = E[x y']``:
    ``Sigma_qq``, ``Sigma_rq``, ``Cov(r, h1)``, ``Cov(q, h1)``, and
    ``Cov(h1, h2)``.

    Identification requires idiosyncratic flow variation. The matrix inverted at
    the last step is ``Sigma_v``, so flow driven purely by common factors leaves
    the structural matrix unidentified no matter how many proxies are supplied.
    """
    n = flow_covariance.shape[0]
    k = proxy_cross_covariance.shape[0]
    _check("flow_covariance", flow_covariance, (n, n))
    _check("return_flow_covariance", return_flow_covariance, (n, n))
    _check("return_proxy_covariance", return_proxy_covariance, (n, k))
    _check("flow_proxy_covariance", flow_proxy_covariance, (n, k))
    _check("proxy_cross_covariance", proxy_cross_covariance, (k, k))

    factor_covariance = np.ascontiguousarray(
        (proxy_cross_covariance + proxy_cross_covariance.T) / 2.0
    )
    factor_scale = float(np.linalg.svd(factor_covariance, compute_uv=False)[0])
    if factor_scale == 0.0 or np.linalg.matrix_rank(factor_covariance) < k:
        raise ValueError(
            "proxy_cross_covariance: singular factor covariance leaves the "
            "loading matrix unidentified"
        )
    loading: Matrix = flow_proxy_covariance @ np.linalg.inv(factor_covariance)
    idiosyncratic: Matrix = flow_covariance - loading @ factor_covariance @ loading.T
    # Rank must be judged against the scale of the flow covariance, not against
    # the residual's own scale: a numerically zero residual has full rank
    # relative to itself, which would let a degenerate input through.
    flow_scale = float(np.linalg.svd(flow_covariance, compute_uv=False)[0])
    smallest = float(np.linalg.svd(idiosyncratic, compute_uv=False)[-1])
    if smallest <= flow_scale * 1e-10:
        raise ValueError(
            "idiosyncratic flow covariance is singular: flow driven purely by "
            "common factors leaves the impact matrix unidentified"
        )
    impact: Matrix = (return_flow_covariance - return_proxy_covariance @ loading.T) @ np.linalg.inv(
        idiosyncratic
    )
    return ProxyIdentification(
        impact=np.ascontiguousarray(impact),
        factor_covariance=factor_covariance,
        flow_loading=np.ascontiguousarray(loading),
        idiosyncratic_flow_covariance=np.ascontiguousarray(idiosyncratic),
    )
