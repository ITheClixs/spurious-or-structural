from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.models.g2_assembly import (
    PAPER_ASSEMBLY_SPEC_ORDER,
    PaperDatePanel,
    assemble_paper_date,
)
from xid.models.g2_paper_cache import (
    PAPER_CACHE_RESEARCH_FIELD_COUNT,
    pack_research_paper_cache,
)
from xid.models.g2_resource import ResourceConfig, load_resource_config
from xid.sim.g2 import G2Contract, load_g2_contract

ROOT = Path(__file__).parents[1]

# A full date costs about 4.2 hours with the sealed solver numerics; see
# docs/redteam/PAPER_ASSEMBLY_COST.md. The composition tests that need a
# complete assembly are therefore opt-in rather than part of the default gate.
slow = pytest.mark.skipif(
    not __import__("os").environ.get("XID_RUN_SLOW_ASSEMBLY"),
    reason="full-date assembly is ~4.2h at sealed numerics; set XID_RUN_SLOW_ASSEMBLY=1",
)


def _contract() -> G2Contract:
    return load_g2_contract(ROOT)


def _resource() -> ResourceConfig:
    return load_resource_config(ROOT)


def _panel(seed: int = 1729) -> PaperDatePanel:
    """Synthetic issued panel: a software fixture, not a scientific trial."""
    contract = _contract()
    n = contract.n_assets
    levels = contract.n_levels
    bins = contract.bins_per_date
    rng = np.random.default_rng(seed)
    common = rng.normal(size=(bins, 1))
    level_flows = 0.6 * common[:, :, None] + rng.normal(size=(bins, n, levels)) * 0.4
    best = level_flows[:, :, contract.paper_reconstruction.best_level_index]
    returns = 0.3 * best + 0.5 * common + rng.normal(size=(bins, n)) * 0.2
    return PaperDatePanel(
        level_flows=np.ascontiguousarray(level_flows, dtype=np.float64),
        returns=np.ascontiguousarray(returns, dtype=np.float64),
    )


def test_spec_order_matches_the_sealed_loss_order() -> None:
    assert PAPER_ASSEMBLY_SPEC_ORDER == (
        "PI_1",
        "PI_I",
        "CI_1",
        "CI_I",
        "PI_CC",
        "CI_CC",
    )


@slow
def test_prediction_1_shapes_finiteness_and_packing() -> None:
    contract = _contract()
    cache = assemble_paper_date(_panel(), contract=contract)
    n = contract.n_assets
    for name in (
        "pi_1_direct",
        "pi_i_direct",
        "ci_1_direct",
        "ci_i_direct",
        "pi_cc_purged",
        "ci_cc_purged",
        "pi_cc_full_response",
        "ci_cc_full_response",
        "cc_mean_projection_p_perp",
    ):
        matrix = getattr(cache, name)
        assert matrix.shape == (n, n), name
        assert matrix.dtype == np.float64, name
        assert np.isfinite(matrix).all(), name
    assert cache.losses.shape == (6, n, 2)
    assert np.isfinite(cache.losses).all()
    packed = pack_research_paper_cache(cache, contract=_resource())
    assert packed.shape == (PAPER_CACHE_RESEARCH_FIELD_COUNT,)


@slow
def test_prediction_2_own_flow_specs_have_exact_zero_offdiagonals() -> None:
    cache = assemble_paper_date(_panel(), contract=_contract())
    for name in ("pi_1_direct", "pi_i_direct"):
        matrix = getattr(cache, name)
        off = matrix - np.diag(np.diag(matrix))
        assert np.abs(off).max() == 0.0, name
        assert np.abs(np.diag(matrix)).max() > 0.0, name


@slow
def test_prediction_3_projection_is_a_rank_deficient_projector() -> None:
    cache = assemble_paper_date(_panel(), contract=_contract())
    p_perp = cache.cc_mean_projection_p_perp
    assert np.abs(p_perp - p_perp.T).max() < 1e-12
    assert np.abs(p_perp @ p_perp - p_perp).max() < 1e-10
    assert abs(float(np.trace(p_perp)) - (_contract().n_assets - 1)) < 1e-9


@slow
def test_prediction_4_full_response_differs_by_rank_one() -> None:
    cache = assemble_paper_date(_panel(), contract=_contract())
    difference = cache.pi_cc_full_response - cache.pi_cc_purged
    singular = np.linalg.svd(difference, compute_uv=False)
    rank = int((singular > singular[0] * 1e-10).sum())
    assert rank == 1, singular[:4]


@slow
def test_prediction_5_assembly_is_deterministic() -> None:
    contract = _contract()
    panel = _panel()
    resource = _resource()
    first = pack_research_paper_cache(
        assemble_paper_date(panel, contract=contract), contract=resource
    )
    second = pack_research_paper_cache(
        assemble_paper_date(panel, contract=contract), contract=resource
    )
    assert first.tobytes() == second.tobytes()


@slow
def test_prediction_6_placement_contract_is_load_bearing() -> None:
    """A permutation or a slot swap must change the packed vector."""
    contract = _contract()
    cache = assemble_paper_date(_panel(), contract=contract)
    baseline = pack_research_paper_cache(cache, contract=_resource()).tobytes()

    from dataclasses import replace

    permutation = np.arange(contract.n_assets)[::-1]
    permuted = replace(cache, pi_1_direct=np.ascontiguousarray(cache.pi_1_direct[permutation]))
    assert pack_research_paper_cache(permuted, contract=_resource()).tobytes() != baseline

    swapped = replace(
        cache,
        pi_cc_full_response=np.ascontiguousarray(cache.pi_cc_purged.copy()),
    )
    assert pack_research_paper_cache(swapped, contract=_resource()).tobytes() != baseline


@slow
def test_prediction_7_sst_uses_the_training_mean_not_the_scored_mean() -> None:
    contract = _contract()
    cache = assemble_paper_date(_panel(), contract=contract)
    alternative = assemble_paper_date(_panel(), contract=contract, _sst_from_scored_mean=True)
    contract_sst = cache.losses[:, :, 1]
    scored_sst = alternative.losses[:, :, 1]
    assert np.abs(contract_sst - scored_sst).max() > 1e-8


@slow
def test_prediction_8_product_before_averaging_differs() -> None:
    contract = _contract()
    cache = assemble_paper_date(_panel(), contract=contract)
    alternative = assemble_paper_date(_panel(), contract=contract, _average_before_product=True)
    difference = np.abs(cache.pi_cc_full_response - alternative.pi_cc_full_response).max()
    assert difference > 1e-10, difference


# --- fail-closed ---------------------------------------------------------------


def test_rejects_nonfinite_returns() -> None:
    contract = _contract()
    panel = _panel()
    corrupted = panel.returns.copy()
    corrupted[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        assemble_paper_date(
            PaperDatePanel(level_flows=panel.level_flows, returns=corrupted),
            contract=contract,
        )


def test_rejects_wrong_bin_count() -> None:
    contract = _contract()
    panel = _panel()
    with pytest.raises(ValueError, match="bins"):
        assemble_paper_date(
            PaperDatePanel(
                level_flows=np.ascontiguousarray(panel.level_flows[:-1]),
                returns=np.ascontiguousarray(panel.returns[:-1]),
            ),
            contract=contract,
        )


def test_rejects_non_float64_panel() -> None:
    contract = _contract()
    panel = _panel()
    with pytest.raises(ValueError, match="float64"):
        assemble_paper_date(
            PaperDatePanel(
                level_flows=panel.level_flows.astype(np.float32),
                returns=panel.returns,
            ),
            contract=contract,
        )


def _degenerate_returns(contract: G2Contract) -> NDArray[np.float64]:
    return np.zeros((contract.bins_per_date, contract.n_assets), dtype=np.float64)


@slow
def test_rejects_zero_benchmark_variance() -> None:
    """An exactly zero SST makes the loss ratio undefined; the date must fail."""
    contract = _contract()
    panel = _panel()
    with pytest.raises(ValueError, match="sst"):
        assemble_paper_date(
            PaperDatePanel(
                level_flows=panel.level_flows,
                returns=_degenerate_returns(contract),
            ),
            contract=contract,
        )
