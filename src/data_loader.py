"""Utilities for loading temperature time-series data."""

from pathlib import Path
from typing import Literal

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
DEMO_CSV = RAW_DIR / "temperature_demo_cities.csv"
DEFAULT_DEMO_CITY = "Split"

REQUIRED_DEMO_COLUMNS = {"timestamp", "city", "temperature"}
ExperimentSource = Literal["demo", "jena_quick", "jena_full", "processed"]


def _validate_temperature_series(series: pd.Series) -> pd.Series:
    """Check that a loaded temperature series is ready for experiments."""
    if series.empty:
        raise ValueError("Temperaturni niz je prazan.")

    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("Indeks mora biti DatetimeIndex.")

    if not series.index.is_monotonic_increasing:
        raise ValueError("Indeks mora biti sortiran.")

    if series.index.has_duplicates:
        raise ValueError("Indeks ne smije imati duplikate.")

    if not pd.api.types.is_numeric_dtype(series):
        raise ValueError("Temperatura mora biti numerička.")

    if series.isna().any():
        raise ValueError("Temperatura ne smije sadržavati nedostajuće vrijednosti.")

    return series


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

    return _validate_temperature_series(series.sort_index())


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
    temperature = temperature.sort_index()
    if temperature.index.has_duplicates:
        temperature = temperature[~temperature.index.duplicated(keep="last")]
    return _validate_temperature_series(temperature)


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

    return _validate_temperature_series(series.sort_index())


def load_jena_temperature_slice(
    hours: int = QUICK_SAMPLE_HOURS,
    raw_dir: Path | None = None,
) -> pd.Series:
    """Load the first N hours of Jena temperature data (for quick tests)."""
    series = load_jena_temperature(raw_dir)
    samples = int(hours * 60 / JENA_INTERVAL_MINUTES)
    return _validate_temperature_series(series.iloc[:samples])


def load_experiment_series(
    source: ExperimentSource = "jena_quick",
    *,
    city: str | None = None,
) -> pd.Series:
    """Load a temperature series for experiments from a named project source."""
    if source == "demo":
        return load_temperature_series(DEMO_CSV, city=city or DEFAULT_DEMO_CITY)
    if source == "jena_quick":
        return load_jena_temperature_slice()
    if source == "jena_full":
        return load_jena_temperature()
    if source == "processed":
        return load_processed_series()
    raise ValueError(f"Nepoznat izvor podataka: {source}")
