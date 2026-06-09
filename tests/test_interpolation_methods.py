"""Pytest testovi za klasične interpolacijske metode."""

import numpy as np
import pandas as pd
import pytest

from src.interpolation_methods import (
    CLASSICAL_METHOD_NAMES,
    cubic_interpolation,
    forward_fill_interpolation,
    linear_interpolation,
    run_classical_interpolations,
    spline_interpolation,
    time_interpolation,
)

SIMPLE_INDEX = pd.date_range("2024-01-01", periods=6, freq="h")
# 4 poznate vrijednosti — dovoljno za cubic i spline; 2 rupe u sredini.
SIMPLE_SERIES = pd.Series(
    [1.0, 2.0, np.nan, 4.0, np.nan, 6.0],
    index=SIMPLE_INDEX,
    name="temperature",
)

ALL_METHODS = [
    forward_fill_interpolation,
    linear_interpolation,
    time_interpolation,
    cubic_interpolation,
    spline_interpolation,
]


@pytest.mark.parametrize("method", ALL_METHODS)
def test_method_returns_series_without_changing_original(method):
    original = SIMPLE_SERIES.copy()
    result = method(original)

    assert isinstance(result, pd.Series)
    assert original.equals(SIMPLE_SERIES)
    assert not result.isna().any()


def test_linear_interpolation_fills_middle_gap():
    result = linear_interpolation(SIMPLE_SERIES)

    assert result.iloc[2] == pytest.approx(3.0)
    assert result.iloc[4] == pytest.approx(5.0)


def test_time_interpolation_with_datetime_index():
    result = time_interpolation(SIMPLE_SERIES)

    assert isinstance(result.index, pd.DatetimeIndex)
    assert not result.isna().any()
    assert result.iloc[2] == pytest.approx(3.0)


def test_time_interpolation_requires_datetime_index():
    numeric_index = pd.Series([1.0, np.nan, 3.0], index=[0, 1, 2])

    with pytest.raises(ValueError, match="DatetimeIndex"):
        time_interpolation(numeric_index)


def test_run_classical_interpolations_returns_expected_keys():
    results = run_classical_interpolations(SIMPLE_SERIES, quiet=True)

    assert set(results.keys()) == set(CLASSICAL_METHOD_NAMES)
    for name in CLASSICAL_METHOD_NAMES:
        assert isinstance(results[name], pd.Series)
        assert not results[name].isna().any()
