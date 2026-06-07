"""Utilities for loading temperature time-series data."""

from pathlib import Path

import pandas as pd

from src.config import (
    DATETIME_COLUMN,
    JENA_INTERVAL_MINUTES,
    JENA_RAW_FILENAME,
    QUICK_SAMPLE_HOURS,
    TEMPERATURE_COLUMN,
)
from src.paths import PROCESSED_DIR, RAW_DIR

JENA_QUICK_PROCESSED_CSV = PROCESSED_DIR / "jena_temperature_48h.csv"

REQUIRED_DEMO_COLUMNS = {"timestamp", "city", "temperature"}


def list_available_cities(csv_path: str | Path) -> list[str]:
    """Return sorted city names found in a demo temperature CSV file."""
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV datoteka ne postoji: {csv_path}")

    data = pd.read_csv(csv_path, usecols=["city"])
    return sorted(data["city"].dropna().unique().tolist())


def load_temperature_series(csv_path: str | Path, city: str | None = None) -> pd.Series:
    """
    Load temperature data from a demo CSV (timestamp, city, temperature).

    Used for the small multi-city demo file in data/raw/.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV datoteka ne postoji: {csv_path}")

    data = pd.read_csv(csv_path)

    if data.empty:
        raise ValueError(f"CSV datoteka je prazna: {csv_path}")

    missing_columns = REQUIRED_DEMO_COLUMNS - set(data.columns)
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


def load_jena_raw(raw_dir: Path | None = None) -> pd.DataFrame:
    """Load the full Jena Climate CSV with datetime index."""
    raw_dir = raw_dir or RAW_DIR
    csv_path = raw_dir / JENA_RAW_FILENAME

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Jena Climate datoteka ne postoji: {csv_path}. "
            "Pokreni: python main.py --download"
        )

    df = pd.read_csv(csv_path)
    df.index = pd.to_datetime(df[DATETIME_COLUMN], dayfirst=True)
    df = df.drop(columns=[DATETIME_COLUMN])
    return df.sort_index()


def load_jena_temperature(raw_dir: Path | None = None) -> pd.Series:
    """
    Load temperature from the Jena weather station (2009–2016, 10-minute resolution).
    """
    df = load_jena_raw(raw_dir)
    temperature = pd.to_numeric(df[TEMPERATURE_COLUMN], errors="coerce")
    temperature.name = "temperature"
    temperature.index.name = "timestamp"
    return temperature.sort_index()


def load_processed_series(csv_path: str | Path | None = None) -> pd.Series:
    """
    Load a processed temperature CSV saved by the project (timestamp, temperature).

    Defaults to the 48 h Jena quick-mode file in data/processed/.
    """
    csv_path = Path(csv_path) if csv_path is not None else JENA_QUICK_PROCESSED_CSV

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Obrađena CSV datoteka ne postoji: {csv_path}. "
            "Pokreni: python main.py --quick"
        )

    data = pd.read_csv(csv_path, index_col="timestamp", parse_dates=True)

    if data.empty:
        raise ValueError(f"CSV datoteka je prazna: {csv_path}")

    if "temperature" not in data.columns:
        raise ValueError(f"Nedostaje stupac 'temperature' u CSV datoteci: {csv_path}")

    temperature = pd.to_numeric(data["temperature"], errors="coerce")
    if temperature.isna().any():
        raise ValueError("Neki temperature zapisi nisu valjani brojevi.")

    series = pd.Series(
        data=temperature.values,
        index=pd.DatetimeIndex(data.index),
        name="temperature",
    )
    series.index.name = "timestamp"

    if series.index.has_duplicates:
        series = series[~series.index.duplicated(keep="last")]

    return series.sort_index()


def load_jena_temperature_slice(
    hours: int = QUICK_SAMPLE_HOURS,
    raw_dir: Path | None = None,
) -> pd.Series:
    """Load the first N hours of Jena temperature data (for quick tests)."""
    series = load_jena_temperature(raw_dir)
    samples = int(hours * 60 / JENA_INTERVAL_MINUTES)
    return series.iloc[:samples]
