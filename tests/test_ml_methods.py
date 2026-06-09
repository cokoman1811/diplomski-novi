"""Pytest testovi za ML metode imputacije."""

import numpy as np
import pandas as pd
import pytest

from src.ml_methods import knn_imputation

DATETIME_INDEX = pd.date_range("2024-01-01", periods=8, freq="h")
SAMPLE_SERIES = pd.Series(
    [10.0, 11.0, np.nan, 13.0, np.nan, 15.0, 16.0, 17.0],
    index=DATETIME_INDEX,
    name="temperature",
)


def test_knn_imputation_returns_series():
    result = knn_imputation(SAMPLE_SERIES)

    assert isinstance(result, pd.Series)


def test_knn_imputation_does_not_change_original():
    original = SAMPLE_SERIES.copy()
    knn_imputation(original)

    assert original.equals(SAMPLE_SERIES)


def test_knn_imputation_keeps_same_index():
    result = knn_imputation(SAMPLE_SERIES)

    assert result.index.equals(SAMPLE_SERIES.index)
    assert isinstance(result.index, pd.DatetimeIndex)


def test_knn_imputation_has_no_nan_values():
    result = knn_imputation(SAMPLE_SERIES)

    assert not result.isna().any()


def test_knn_imputation_keeps_known_values_unchanged():
    result = knn_imputation(SAMPLE_SERIES)
    known_mask = SAMPLE_SERIES.notna()

    assert result.loc[known_mask].equals(SAMPLE_SERIES.loc[known_mask])


def test_knn_imputation_result_name_is_temperature():
    result = knn_imputation(SAMPLE_SERIES)

    assert result.name == "temperature"


def test_knn_imputation_works_on_small_datetime_example():
    result = knn_imputation(SAMPLE_SERIES, n_neighbors=3)

    assert len(result) == len(SAMPLE_SERIES)
    assert result.iloc[2] == pytest.approx(12.0, abs=2.0)
    assert result.iloc[4] == pytest.approx(14.0, abs=2.0)
