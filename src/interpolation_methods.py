"""Classical interpolation methods for temperature time series with missing values."""

import pandas as pd


def _validate_series(series: pd.Series) -> None:
    if not isinstance(series, pd.Series):
        raise ValueError("series must be a pandas Series.")


def _fill_remaining_gaps(result: pd.Series) -> pd.Series:
    """Forward- and back-fill any NaN values left after interpolation."""
    return result.ffill().bfill()


def forward_fill(series: pd.Series) -> pd.Series:
    """
    Fill missing values with the last known temperature.

    Parameters
    ----------
    series :
        Temperature time series that may contain NaN values.

    Returns
    -------
    pd.Series
        Copy of ``series`` with missing values filled.
    """
    _validate_series(series)

    result = series.copy()
    result = result.ffill()
    return _fill_remaining_gaps(result)


def linear_interpolation(series: pd.Series) -> pd.Series:
    """
    Fill missing values using linear interpolation between neighbors.

    Parameters
    ----------
    series :
        Temperature time series that may contain NaN values.

    Returns
    -------
    pd.Series
        Copy of ``series`` with missing values interpolated.
    """
    _validate_series(series)

    result = series.copy()
    result = result.interpolate(method="linear")
    return _fill_remaining_gaps(result)


def time_interpolation(series: pd.Series) -> pd.Series:
    """
    Fill missing values using time-aware linear interpolation.

    The series index must be a DatetimeIndex so pandas can weight gaps
    by elapsed time.

    Parameters
    ----------
    series :
        Temperature time series that may contain NaN values.

    Returns
    -------
    pd.Series
        Copy of ``series`` with missing values interpolated.
    """
    _validate_series(series)

    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("series index must be a DatetimeIndex for time interpolation.")

    result = series.copy()
    result = result.interpolate(method="time")
    return _fill_remaining_gaps(result)
