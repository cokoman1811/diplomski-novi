"""Machine learning imputation methods for temperature time series."""

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor


def _build_time_features(index: pd.Index) -> np.ndarray:
    """Build simple time-based features for KNN training and prediction."""
    # Redni broj mjerenja (0, 1, 2, ...).
    features = [np.arange(len(index), dtype=float)]

    if isinstance(index, pd.DatetimeIndex):
        # Sat u danu (0–23) i dan u godini (1–366).
        features.append(index.hour.astype(float).to_numpy())
        features.append(index.dayofyear.astype(float).to_numpy())

    return np.column_stack(features)


def knn_imputation(series: pd.Series, n_neighbors: int = 5) -> pd.Series:
    """
    Fill missing temperature values using K-Nearest Neighbors regression.

    The model trains only on known (non-NaN) values and predicts only at
    missing positions. Any remaining gaps are filled with forward/backward fill.
    """
    if not isinstance(series, pd.Series):
        raise ValueError("series must be a pandas Series.")

    if n_neighbors < 1:
        raise ValueError("n_neighbors must be at least 1.")

    result = series.copy()
    missing_mask = series.isna()

    # Nothing to impute — return a copy unchanged.
    if not missing_mask.any():
        result.name = "temperature"
        return result

    known_mask = ~missing_mask
    known_count = int(known_mask.sum())

    if known_count == 0:
        raise ValueError("Cannot impute: series has no known values.")

    features = _build_time_features(series.index)
    effective_neighbors = min(n_neighbors, known_count)

    model = KNeighborsRegressor(n_neighbors=effective_neighbors)
    model.fit(features[known_mask], series.loc[known_mask].to_numpy())

    # Predict only where temperature is missing.
    predicted = model.predict(features[missing_mask])
    result.loc[missing_mask] = predicted

    # Safety net for edge cases that still leave NaN.
    result = result.ffill().bfill()
    result.name = "temperature"
    return result
