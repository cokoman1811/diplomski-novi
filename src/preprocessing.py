"""Utilities for artificially removing values from temperature time series."""

import numpy as np
import pandas as pd


def create_missing_values(
    series: pd.Series,
    missing_rate: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.Series, pd.Series]:
    """
    Randomly remove interior values from a temperature series for evaluation.

    The first and last values are always kept so interpolation methods have
    boundary anchors.

    Parameters
    ----------
    series :
        Temperature time series with a DatetimeIndex.
    missing_rate :
        Fraction of values to remove, between 0 and 1 (inclusive).
    random_state :
        Seed for reproducible random selection.

    Returns
    -------
    damaged_series :
        Copy of ``series`` with selected values replaced by NaN.
    missing_mask :
        Boolean series aligned with ``series``; True where a value was removed.
    """
    if not isinstance(series, pd.Series):
        raise ValueError("series must be a pandas Series.")

    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("series index must be a DatetimeIndex.")

    if len(series) < 2:
        raise ValueError("series must contain at least 2 values.")

    if not 0 <= missing_rate <= 1:
        raise ValueError("missing_rate must be between 0 and 1.")

    damaged_series = series.copy()
    missing_mask = pd.Series(False, index=series.index, name="missing_mask")

    eligible_positions = list(range(1, len(series) - 1))
    if not eligible_positions:
        return damaged_series, missing_mask

    n_to_remove = min(round(missing_rate * len(series)), len(eligible_positions))
    if n_to_remove == 0:
        return damaged_series, missing_mask

    rng = np.random.default_rng(random_state)
    removed_positions = rng.choice(eligible_positions, size=n_to_remove, replace=False)

    for position in removed_positions:
        index_label = series.index[position]
        damaged_series.iloc[position] = np.nan
        missing_mask.iloc[position] = True

    return damaged_series, missing_mask
