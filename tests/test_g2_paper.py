from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from xid.models.g2_paper import (
    LassoCoordinateDescentResult,
    LassoRatioSelection,
    PaperCrossSectionProjection,
    PaperLassoProblem,
    PaperLinearCoefficients,
    PaperOlsResult,
    PaperPcaFit,
    apply_cross_sectional_pca,
    apply_integrated_level_pca,
    fit_full_rank_ols,
    fit_paper_pca,
    prepare_lasso_problem,
    reconstruct_lasso_coefficients,
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


def _factor_preprocessing_fixture() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    y = np.asarray([1.0, 3.0, 5.0, 7.0], dtype=np.float64)
    factor = np.asarray([-1.0, -1.0, 1.0, 1.0], dtype=np.float64)
    penalized = np.asarray(
        [[0.0, 1.0], [2.0, 3.0], [4.0, 1.0], [6.0, 3.0]],
        dtype=np.float64,
    )
    return y, penalized, factor


def test_prepare_lasso_problem_scales_before_factor_fwl() -> None:
    contract = load_g2_contract(_root())
    y, penalized, factor = _factor_preprocessing_fixture()
    y_before = y.copy()
    penalized_before = penalized.copy()
    factor_before = factor.copy()

    problem = prepare_lasso_problem(
        y,
        penalized,
        factor=factor,
        contract=contract,
    )

    root_five = np.sqrt(np.float64(5.0))
    expected_x_res = np.asarray(
        [
            [-1.0 / root_five, -1.0],
            [1.0 / root_five, 1.0],
            [-1.0 / root_five, -1.0],
            [1.0 / root_five, 1.0],
        ],
        dtype=np.float64,
    )
    assert type(problem) is PaperLassoProblem
    assert problem.y_mean == 4.0
    assert problem.factor_mean == 0.0
    assert problem.factor_sum_squares == 4.0
    assert problem.lambda_max == 1.0
    np.testing.assert_array_equal(problem.x_means, np.asarray([3.0, 2.0]))
    np.testing.assert_array_equal(problem.pre_fwl_rms, np.asarray([root_five, 1.0]))
    np.testing.assert_array_equal(problem.active_columns, np.asarray([True, True]))
    np.testing.assert_array_equal(problem.y_res, np.asarray([-1.0, 1.0, -1.0, 1.0]))
    np.testing.assert_allclose(problem.x_res, expected_x_res, rtol=0.0, atol=1e-15)
    for values in (
        problem.x_means,
        problem.pre_fwl_rms,
        problem.active_columns,
        problem.y_centered,
        problem.x_centered,
        problem.factor_centered,
        problem.y_res,
        problem.x_res,
    ):
        assert values is not None
        assert values.flags.c_contiguous
        assert not values.flags.writeable
    np.testing.assert_array_equal(y, y_before)
    np.testing.assert_array_equal(penalized, penalized_before)
    np.testing.assert_array_equal(factor, factor_before)


def test_reconstruct_lasso_coefficients_returns_original_units() -> None:
    contract = load_g2_contract(_root())
    y, penalized, factor = _factor_preprocessing_fixture()
    problem = prepare_lasso_problem(
        y,
        penalized,
        factor=factor,
        contract=contract,
    )

    coefficients = reconstruct_lasso_coefficients(
        problem,
        np.asarray([np.sqrt(np.float64(5.0)), 2.0], dtype=np.float64),
        contract=contract,
    )

    assert type(coefficients) is PaperLinearCoefficients
    assert coefficients.intercept == -3.0
    assert coefficients.factor_coefficient == 0.0
    np.testing.assert_array_equal(
        coefficients.penalized_coefficients,
        np.asarray([1.0, 2.0]),
    )
    assert coefficients.penalized_coefficients.flags.c_contiguous
    assert not coefficients.penalized_coefficients.flags.writeable


def test_prepare_lasso_problem_drops_only_after_the_declared_stage() -> None:
    contract = load_g2_contract(_root())
    y = np.asarray([-1.0, 1.0, -1.0, 1.0], dtype=np.float64)
    factor = np.asarray([-1.0, -1.0, 1.0, 1.0], dtype=np.float64)
    penalized = np.asarray(
        [[-1.0, -1.0], [-1.0, 1.0], [1.0, -1.0], [1.0, 1.0]],
        dtype=np.float64,
    )

    problem = prepare_lasso_problem(
        y,
        penalized,
        factor=factor,
        contract=contract,
    )

    np.testing.assert_array_equal(problem.pre_fwl_rms, np.asarray([1.0, 1.0]))
    np.testing.assert_array_equal(problem.active_columns, np.asarray([False, True]))
    np.testing.assert_array_equal(problem.x_res, penalized[:, 1:])
    assert problem.lambda_max == 1.0


def test_post_fwl_cutoff_compares_the_squared_norm_to_100_eps() -> None:
    contract = load_g2_contract(_root())
    factor = np.asarray([-1.0, -1.0, 1.0, 1.0], dtype=np.float64)
    orthogonal = np.asarray([-1.0, 1.0, -1.0, 1.0], dtype=np.float64)
    cutoff = np.float64(
        contract.paper_reconstruction.post_fwl_zero_norm_multiplier * np.finfo(np.float64).eps
    )
    below = np.sqrt(np.float64((cutoff / 2.0) / (1.0 - cutoff / 2.0)))
    above = np.sqrt(np.float64((2.0 * cutoff) / (1.0 - 2.0 * cutoff)))
    penalized = np.column_stack((factor + below * orthogonal, factor + above * orthogonal)).astype(
        np.float64
    )

    problem = prepare_lasso_problem(
        orthogonal,
        penalized,
        factor=factor,
        contract=contract,
    )

    assert np.all(problem.pre_fwl_rms > 0.0)
    np.testing.assert_array_equal(problem.active_columns, np.asarray([False, True]))
    assert problem.x_res.shape == (4, 1)


def test_reconstruct_lasso_coefficients_without_a_factor() -> None:
    contract = load_g2_contract(_root())
    y = np.asarray([1.0, 3.0, 5.0, 7.0], dtype=np.float64)
    penalized = np.asarray([[0.0], [2.0], [4.0], [6.0]], dtype=np.float64)
    problem = prepare_lasso_problem(y, penalized, factor=None, contract=contract)

    coefficients = reconstruct_lasso_coefficients(
        problem,
        np.asarray([np.sqrt(np.float64(5.0))], dtype=np.float64),
        contract=contract,
    )

    assert coefficients.intercept == 1.0
    assert coefficients.factor_coefficient is None
    np.testing.assert_array_equal(coefficients.penalized_coefficients, np.asarray([1.0]))


def test_prepare_lasso_problem_fails_closed_and_allows_the_zero_path() -> None:
    contract = load_g2_contract(_root())
    y = np.asarray([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    constants = np.asarray(
        [[2.0, -3.0], [2.0, -3.0], [2.0, -3.0], [2.0, -3.0]],
        dtype=np.float64,
    )

    zero_problem = prepare_lasso_problem(y, constants, factor=None, contract=contract)
    np.testing.assert_array_equal(zero_problem.pre_fwl_rms, np.asarray([0.0, 0.0]))
    np.testing.assert_array_equal(zero_problem.active_columns, np.asarray([False, False]))
    assert zero_problem.x_res.shape == (4, 0)
    assert zero_problem.lambda_max == 0.0
    zero_coefficients = reconstruct_lasso_coefficients(
        zero_problem,
        np.empty(0, dtype=np.float64),
        contract=contract,
    )
    np.testing.assert_array_equal(
        zero_coefficients.penalized_coefficients,
        np.asarray([0.0, 0.0]),
    )

    with pytest.raises(ValueError, match="factor|variance|sum"):
        prepare_lasso_problem(
            y,
            constants,
            factor=np.ones(4, dtype=np.float64),
            contract=contract,
        )

    nonfinite = constants.copy()
    nonfinite[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        prepare_lasso_problem(y, nonfinite, factor=None, contract=contract)

    with pytest.raises(TypeError, match="float64"):
        prepare_lasso_problem(
            y,
            constants.astype(np.float32),
            factor=None,
            contract=contract,
        )

    altered = replace(
        contract,
        paper_reconstruction=replace(
            contract.paper_reconstruction,
            post_fwl_zero_norm_multiplier=10.0,
        ),
    )
    with pytest.raises(ValueError, match="sealed G2 contract"):
        prepare_lasso_problem(y, constants, factor=None, contract=altered)


def _rank_one_pca_fixture() -> np.ndarray:
    axis = np.asarray([-3.0, -1.0, 1.0, 3.0], dtype=np.float64)
    return np.column_stack((-axis, 2.0 * axis))


def test_paper_pca_fits_training_means_sign_and_l1_mapping() -> None:
    contract = load_g2_contract(_root())
    training = _rank_one_pca_fixture()
    training_before = training.copy()

    fit = fit_paper_pca(training, contract=contract)
    training_scores = apply_integrated_level_pca(fit, training, contract=contract)
    test_features = training[:2] + np.asarray([100.0, -7.0], dtype=np.float64)
    test_scores = apply_integrated_level_pca(fit, test_features, contract=contract)

    root_five = np.sqrt(np.float64(5.0))
    assert type(fit) is PaperPcaFit
    np.testing.assert_array_equal(fit.training_means, np.asarray([0.0, 0.0]))
    np.testing.assert_allclose(
        fit.loading,
        np.asarray([-1.0, 2.0], dtype=np.float64) / root_five,
        rtol=0.0,
        atol=3e-16,
    )
    np.testing.assert_allclose(
        training_scores,
        (5.0 / 3.0) * np.asarray([-3.0, -1.0, 1.0, 3.0]),
        rtol=0.0,
        atol=2e-15,
    )
    np.testing.assert_allclose(
        test_scores,
        np.asarray([-43.0, -119.0 / 3.0]),
        rtol=0.0,
        atol=2e-14,
    )
    assert fit.covariance_trace == pytest.approx(25.0, rel=0.0, abs=1e-15)
    assert fit.leading_eigenvalue == pytest.approx(25.0, rel=0.0, abs=1e-15)
    assert fit.eigengap == pytest.approx(25.0, rel=0.0, abs=1e-15)
    assert fit.loading_l1_norm == pytest.approx(3.0 / root_five, rel=0.0, abs=1e-15)
    for values in (
        fit.training_means,
        fit.loading,
        fit.orthogonal_projector,
        training_scores,
        test_scores,
    ):
        assert values.flags.c_contiguous
        assert not values.flags.writeable
    np.testing.assert_array_equal(training, training_before)


def test_paper_pca_sign_tie_and_cross_sectional_projection() -> None:
    contract = load_g2_contract(_root())
    axis = np.asarray([3.0, 1.0, -1.0, -3.0], dtype=np.float64)
    training = np.column_stack((axis, -axis))

    fit = fit_paper_pca(training, contract=contract)
    projection = apply_cross_sectional_pca(fit, training, contract=contract)

    root_two = np.sqrt(np.float64(2.0))
    assert type(projection) is PaperCrossSectionProjection
    np.testing.assert_allclose(
        fit.loading,
        np.asarray([1.0, -1.0], dtype=np.float64) / root_two,
        rtol=0.0,
        atol=3e-16,
    )
    np.testing.assert_allclose(
        fit.orthogonal_projector,
        np.asarray([[0.5, 0.5], [0.5, 0.5]], dtype=np.float64),
        rtol=0.0,
        atol=3e-16,
    )
    np.testing.assert_allclose(projection.scores, axis * root_two, rtol=0.0, atol=2e-15)
    np.testing.assert_allclose(projection.residuals, np.zeros_like(training), rtol=0.0, atol=2e-15)
    assert projection.scores.flags.c_contiguous
    assert projection.residuals.flags.c_contiguous
    assert not projection.scores.flags.writeable
    assert not projection.residuals.flags.writeable


def test_paper_pca_fails_weak_or_invalid_training_problems() -> None:
    contract = load_g2_contract(_root())
    isotropic = np.asarray([[1, 0], [-1, 0], [0, 1], [0, -1]], dtype=np.float64)
    with pytest.raises(ValueError, match="eigengap"):
        fit_paper_pca(isotropic, contract=contract)
    with pytest.raises(ValueError, match="trace"):
        fit_paper_pca(np.zeros((4, 2), dtype=np.float64), contract=contract)
    with pytest.raises(ValueError, match="columns|features|dimensions|eigen"):
        fit_paper_pca(
            np.asarray([[-1.0], [0.0], [1.0], [2.0]], dtype=np.float64),
            contract=contract,
        )

    nonfinite = _rank_one_pca_fixture()
    nonfinite[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        fit_paper_pca(nonfinite, contract=contract)
    with pytest.raises(TypeError, match="float64"):
        fit_paper_pca(_rank_one_pca_fixture().astype(np.float32), contract=contract)

    altered = replace(
        contract,
        paper_reconstruction=replace(
            contract.paper_reconstruction,
            pca_top_eigengap_min_trace_ratio=1e-9,
        ),
    )
    with pytest.raises(ValueError, match="sealed G2 contract"):
        fit_paper_pca(_rank_one_pca_fixture(), contract=altered)


def test_full_rank_ols_uses_the_frozen_rcond(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = load_g2_contract(_root())
    design = np.asarray(
        [[1.0, 0.0], [1.0, 1.0], [1.0, 2.0], [1.0, 3.0]],
        dtype=np.float64,
    )
    response = np.asarray([2.0, 5.0, 8.0, 11.0], dtype=np.float64)
    original_lstsq = np.linalg.lstsq
    seen_rcond: list[float] = []

    def recording_lstsq(
        a: np.ndarray,
        b: np.ndarray,
        rcond: float,
    ) -> tuple[np.ndarray, np.ndarray, np.int64, np.ndarray]:
        seen_rcond.append(rcond)
        return original_lstsq(a, b, rcond=rcond)

    monkeypatch.setattr(np.linalg, "lstsq", recording_lstsq)
    result = fit_full_rank_ols(design, response, contract=contract)

    expected_rcond = float(np.finfo(np.float64).eps * max(design.shape))
    assert type(result) is PaperOlsResult
    assert seen_rcond == [expected_rcond]
    assert result.rank == 2
    assert result.rcond == expected_rcond
    np.testing.assert_allclose(
        result.coefficients,
        np.asarray([2.0, 3.0]),
        rtol=0.0,
        atol=3e-15,
    )
    assert result.coefficients.flags.c_contiguous
    assert not result.coefficients.flags.writeable


def test_full_rank_ols_rejects_rank_loss_and_bad_inputs() -> None:
    contract = load_g2_contract(_root())
    rank_deficient = np.ones((3, 2), dtype=np.float64)
    response = np.asarray([1.0, 2.0, 3.0], dtype=np.float64)
    with pytest.raises(ValueError, match="rank"):
        fit_full_rank_ols(rank_deficient, response, contract=contract)
    with pytest.raises(ValueError, match="shape|rows"):
        fit_full_rank_ols(rank_deficient, response[:2], contract=contract)
    with pytest.raises(TypeError, match="float64"):
        fit_full_rank_ols(rank_deficient.astype(np.float32), response, contract=contract)
