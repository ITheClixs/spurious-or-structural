from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from xid.models.g2_paper import (
    LassoCoordinateDescentResult,
    LassoRatioSelection,
    select_lasso_ratio,
    solve_lasso_coordinate_descent,
)
from xid.sim.g2 import load_g2_contract


def _root() -> Path:
    return Path(__file__).parents[1]


def _fold_order_pooled_mse(fold_sse: np.ndarray) -> np.ndarray:
    pooled = np.empty(fold_sse.shape[1], dtype=np.float64)
    for ratio_index in range(fold_sse.shape[1]):
        total = np.float64(0.0)
        for fold_index in range(fold_sse.shape[0]):
            total = np.float64(total + fold_sse[fold_index, ratio_index])
        pooled[ratio_index] = np.float64(total / np.float64(30.0))
    return pooled


def test_lasso_ratio_selection_uses_fold_order_and_the_inclusive_tie_rule() -> None:
    contract = load_g2_contract(_root())
    fold_sse = np.full((5, 40), 3.0, dtype=np.float64)
    fold_sse[:, 4:] = 4.0
    fold_sse[4, 0] += 1.5e-11
    fold_sse[4, 2] += 1.8e-11
    fold_sse[4, 3] += 6.0e-11

    selection = select_lasso_ratio(fold_sse, contract=contract)
    expected_mse = _fold_order_pooled_mse(fold_sse)

    assert type(selection) is LassoRatioSelection
    assert selection.selected_index == 0
    assert selection.selected_ratio == contract.lasso_ratio_grid[0]
    np.testing.assert_array_equal(selection.pooled_mse, expected_mse)
    assert expected_mse[0] > expected_mse[1]
    assert (
        expected_mse[0] <= expected_mse[1] + contract.paper_reconstruction.selected_ratio_tolerance
    )
    assert (
        expected_mse[3] > expected_mse[1] + contract.paper_reconstruction.selected_ratio_tolerance
    )
    assert selection.pooled_mse.flags.c_contiguous
    assert not selection.pooled_mse.flags.writeable


def test_lasso_ratio_selection_rejects_invalid_sse_before_selecting() -> None:
    contract = load_g2_contract(_root())
    valid = np.ones((5, 40), dtype=np.float64)

    with pytest.raises(ValueError, match="five|shape|fold"):
        select_lasso_ratio(valid[:4], contract=contract)
    with pytest.raises(TypeError, match="float64"):
        select_lasso_ratio(valid.astype(np.float32), contract=contract)

    nonfinite = valid.copy()
    nonfinite[2, 7] = np.nan
    with pytest.raises(ValueError, match="finite"):
        select_lasso_ratio(nonfinite, contract=contract)

    negative = valid.copy()
    negative[0, 0] = -1.0
    with pytest.raises(ValueError, match="nonnegative"):
        select_lasso_ratio(negative, contract=contract)

    overflowing = np.full((5, 40), np.finfo(np.float64).max, dtype=np.float64)
    with pytest.raises(FloatingPointError, match="nonfinite|overflow"):
        select_lasso_ratio(overflowing, contract=contract)


def test_lasso_ratio_selection_revalidates_the_contract() -> None:
    contract = load_g2_contract(_root())
    altered = replace(
        contract,
        paper_reconstruction=replace(
            contract.paper_reconstruction,
            selected_ratio_tolerance=1e-9,
        ),
    )

    with pytest.raises(ValueError, match="sealed G2 contract"):
        select_lasso_ratio(np.ones((5, 40), dtype=np.float64), contract=altered)


def test_coordinate_descent_matches_orthogonal_known_answers() -> None:
    contract = load_g2_contract(_root())
    x_res = np.asarray(
        [[1.0, 0.0], [0.0, 2.0], [-1.0, 0.0], [0.0, -2.0]],
        dtype=np.float64,
    )
    y_res = np.asarray([3.0, 4.0, -3.0, -4.0], dtype=np.float64)

    result = solve_lasso_coordinate_descent(
        x_res,
        y_res,
        lambda_value=0.5,
        contract=contract,
    )
    threshold_zero = solve_lasso_coordinate_descent(
        x_res,
        y_res,
        lambda_value=1.5,
        contract=contract,
    )

    assert type(result) is LassoCoordinateDescentResult
    np.testing.assert_array_equal(result.coefficients, np.asarray([2.0, 1.75]))
    assert result.sweeps == 2
    assert result.maximum_update == 0.0
    assert result.maximum_kkt_violation == 0.0
    assert result.coefficients.flags.c_contiguous
    assert not result.coefficients.flags.writeable
    np.testing.assert_array_equal(threshold_zero.coefficients, np.asarray([0.0, 1.25]))
    assert not np.signbit(threshold_zero.coefficients[0])


def test_coordinate_descent_rejects_invalid_inputs_and_contract_drift() -> None:
    contract = load_g2_contract(_root())
    x_res = np.eye(4, 2, dtype=np.float64)
    y_res = np.ones(4, dtype=np.float64)

    with pytest.raises(TypeError, match="float64"):
        solve_lasso_coordinate_descent(
            x_res.astype(np.float32),
            y_res,
            lambda_value=0.5,
            contract=contract,
        )
    with pytest.raises(ValueError, match="shape|rows"):
        solve_lasso_coordinate_descent(
            x_res,
            y_res[:3],
            lambda_value=0.5,
            contract=contract,
        )

    nonfinite = x_res.copy()
    nonfinite[0, 0] = np.inf
    with pytest.raises(ValueError, match="finite"):
        solve_lasso_coordinate_descent(
            nonfinite,
            y_res,
            lambda_value=0.5,
            contract=contract,
        )
    with pytest.raises(ValueError, match="nonnegative"):
        solve_lasso_coordinate_descent(
            x_res,
            y_res,
            lambda_value=-0.5,
            contract=contract,
        )

    zero_column = x_res.copy()
    zero_column[:, 1] = 0.0
    with pytest.raises(ValueError, match="column|norm"):
        solve_lasso_coordinate_descent(
            zero_column,
            y_res,
            lambda_value=0.5,
            contract=contract,
        )

    altered = replace(
        contract,
        paper_reconstruction=replace(
            contract.paper_reconstruction,
            kkt_tolerance=1e-8,
        ),
    )
    with pytest.raises(ValueError, match="sealed G2 contract"):
        solve_lasso_coordinate_descent(
            x_res,
            y_res,
            lambda_value=0.5,
            contract=altered,
        )
