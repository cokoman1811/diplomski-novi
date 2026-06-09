"""Metrics for comparing reconstructed temperature values to the original series."""

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_reconstruction(
    original: pd.Series,
    reconstructed: pd.Series,
    missing_mask: pd.Series | None = None,
) -> dict[str, float]:
    """
    Compare reconstructed values to the original series.

    If ``missing_mask`` is provided, metrics are computed only at positions
    where the mask is True (artificially removed values).
    """
    if missing_mask is not None:
        y_true = original[missing_mask]
        y_pred = reconstructed[missing_mask]
    else:
        y_true = original
        y_pred = reconstructed

    if len(y_true) == 0:
        raise ValueError("Nema točaka za evaluaciju.")

    return {
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": mean_squared_error(y_true, y_pred) ** 0.5,
        "r2": r2_score(y_true, y_pred),
    }
