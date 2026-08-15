from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.multi_proxy import identify_with_two_proxies

N = 12
K = 3


def _population(seed: int = 1729):  # type: ignore[no-untyped-def]
    """Exact population moments for a general, non-diagonal structural matrix."""
    rng = np.random.default_rng(seed)

    def psd(n: int, scale: float = 1.0) -> NDArray[np.float64]:
        a = rng.normal(size=(n, n))
        return np.ascontiguousarray(scale * (a @ a.T / n + np.eye(n) * 0.6))

    impact = np.diag(rng.uniform(0.2, 0.4, N)) + rng.normal(scale=0.03, size=(N, N))
    gamma = rng.normal(size=(N, K))
    loading = rng.normal(size=(N, K))
    factor = psd(K)
    _ = psd(N)
    idiosyncratic = psd(N)
    flow = loading @ factor @ loading.T + idiosyncratic
    return_flow = impact @ flow + gamma @ factor @ loading.T
    return_proxy = (impact @ loading + gamma) @ factor
    flow_proxy = loading @ factor
    return (
        np.ascontiguousarray(impact),
        np.ascontiguousarray(loading),
        factor,
        np.ascontiguousarray(idiosyncratic),
        np.ascontiguousarray(flow),
        np.ascontiguousarray(return_flow),
        np.ascontiguousarray(return_proxy),
        np.ascontiguousarray(flow_proxy),
    )


def _solve(proxy_cross: NDArray[np.float64]):  # type: ignore[no-untyped-def]
    impact, loading, factor, idio, flow, rq, rh, qh = _population()
    return impact, loading, idio, identify_with_two_proxies(flow, rq, rh, qh, proxy_cross)


def test_prediction_1_proxy_cross_covariance_is_the_factor_covariance() -> None:
    _, _, factor, *_ = _population()
    _, _, _, out = _solve(factor)
    assert np.abs(out.factor_covariance - factor).max() < 1e-12


def test_prediction_2_loading_is_recovered() -> None:
    _, _, factor, *_ = _population()
    _, loading, _, out = _solve(factor)
    assert np.abs(out.flow_loading - loading).max() < 1e-12


def test_prediction_3_general_impact_matrix_is_point_identified() -> None:
    """The headline: a non-diagonal Lambda recovered exactly."""
    _, _, factor, *_ = _population()
    impact, _, _, out = _solve(factor)
    assert np.abs(out.impact - impact).max() < 1e-12
    off = impact - np.diag(np.diag(impact))
    assert np.abs(off).max() > 1e-3, "fixture must be genuinely non-diagonal"


def test_prediction_4_inverted_bracket_is_the_idiosyncratic_flow_covariance() -> None:
    _, _, factor, *_ = _population()
    _, _, idio, out = _solve(factor)
    assert np.abs(out.idiosyncratic_flow_covariance - idio).max() < 1e-12


def test_prediction_5_one_proxy_and_naive_regression_both_fail() -> None:
    impact, loading, factor, idio, flow, rq, rh, qh = _population()
    rng = np.random.default_rng(4242)
    a = rng.normal(size=(K, K))
    proxy_noise = a @ a.T / K + np.eye(K) * 0.3
    single = identify_with_two_proxies(flow, rq, rh, qh, factor + proxy_noise)
    naive = rq @ np.linalg.inv(flow)
    assert np.abs(single.impact - impact).max() > 0.1
    assert np.abs(naive - impact).max() > 0.1


def test_prediction_6_small_error_correlation_destroys_identification() -> None:
    """The cliff: 0.1 correlation already costs most of the benefit."""
    impact, loading, factor, idio, flow, rq, rh, qh = _population()
    rng = np.random.default_rng(4242)
    a = rng.normal(size=(K, K))
    noise = a @ a.T / K + np.eye(K) * 0.3
    scale = np.sqrt(np.diag(noise))
    errors = {}
    for rho in (0.1, 1.0):
        contaminated = factor + rho * np.outer(scale, scale)
        out = identify_with_two_proxies(flow, rq, rh, qh, contaminated)
        errors[rho] = float(np.abs(out.impact - impact).max())
    assert errors[0.1] > 0.1
    assert errors[0.1] > 0.5 * errors[1.0], errors


def test_singular_idiosyncratic_flow_is_refused() -> None:
    """Flow driven purely by common factors leaves the impact unidentified."""
    impact, loading, factor, idio, flow, rq, rh, qh = _population()
    degenerate = np.ascontiguousarray(loading @ factor @ loading.T)
    with pytest.raises(ValueError, match="purely by"):
        identify_with_two_proxies(degenerate, rq, rh, qh, factor)


def test_singular_factor_covariance_is_refused() -> None:
    impact, loading, factor, idio, flow, rq, rh, qh = _population()
    with pytest.raises(ValueError, match="singular factor covariance"):
        identify_with_two_proxies(flow, rq, rh, qh, np.zeros((K, K)))


def test_rejects_non_float64() -> None:
    impact, loading, factor, idio, flow, rq, rh, qh = _population()
    with pytest.raises(ValueError, match="float64"):
        identify_with_two_proxies(flow.astype(np.float32), rq, rh, qh, factor)


def test_rejects_shape_mismatch() -> None:
    impact, loading, factor, idio, flow, rq, rh, qh = _population()
    with pytest.raises(ValueError, match="shape"):
        identify_with_two_proxies(flow, rq, rh[:-1], qh, factor)
