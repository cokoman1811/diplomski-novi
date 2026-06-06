"""Utilities for loading temperature time-series data."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"timestamp", "city", "temperature"}


def load_temperature_series(csv_path: str | Path, city: str | None = None) -> pd.Series:
    """
    Load temperature data from a CSV file and return it as a time-indexed Series.

    Expected columns: timestamp, city, temperature.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV datoteka ne postoji: {csv_path}")

    data = pd.read_csv(csv_path)

    if data.empty:
        raise ValueError(f"CSV datoteka je prazna: {csv_path}")

    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Nedostaju stupci u CSV datoteci: {missing_columns}")

    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    if data["timestamp"].isna().any():
        raise ValueError("Neki timestamp zapisi se ne mogu pretvoriti u datetime.")

    if city is not None:
        data = data[data["city"] == city]
        if data.empty:
            raise ValueError(f"Nema podataka za grad: {city}")

    data = data.sort_values("timestamp")

    temperature = pd.to_numeric(data["temperature"], errors="coerce")
    if temperature.isna().any():
        raise ValueError("Neki temperature zapisi nisu valjani brojevi.")

    series = pd.Series(
        data=temperature.values,
        index=pd.DatetimeIndex(data["timestamp"]),
        name="temperature",
    )

    if series.index.has_duplicates:
        series = series[~series.index.duplicated(keep="last")]

    return series.sort_index()
