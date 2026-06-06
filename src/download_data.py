"""Download and prepare the Jena Climate dataset."""

import zipfile
from pathlib import Path
from urllib.request import urlretrieve

from src.config import JENA_DATA_URL, JENA_RAW_FILENAME, JENA_ZIP_FILENAME, TEMPERATURE_COLUMN
from src.paths import RAW_DIR, ensure_data_dirs


def download_jena_climate(raw_dir: Path | None = None, force: bool = False) -> Path:
    """Download and extract the Jena Climate CSV into data/raw/."""
    ensure_data_dirs()
    raw_dir = raw_dir or RAW_DIR
    csv_path = raw_dir / JENA_RAW_FILENAME

    if csv_path.exists() and not force:
        return csv_path

    zip_path = raw_dir / JENA_ZIP_FILENAME
    print(f"Preuzimam Jena Climate dataset...")
    print(f"URL: {JENA_DATA_URL}")
    urlretrieve(JENA_DATA_URL, zip_path)

    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(raw_dir)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV nije pronađen nakon raspakiravanja: {csv_path}")

    print(f"Spremno: {csv_path}")
    return csv_path


def validate_jena_csv(csv_path: Path) -> None:
    """Basic validation of the downloaded Jena CSV."""
    import pandas as pd

    sample = pd.read_csv(csv_path, nrows=5)
    if TEMPERATURE_COLUMN not in sample.columns:
        raise ValueError(f"Nedostaje stupac temperature: {TEMPERATURE_COLUMN}")


def ensure_jena_data(raw_dir: Path | None = None, force: bool = False) -> Path:
    """Download Jena data if missing and validate it."""
    raw_dir = raw_dir or RAW_DIR
    csv_path = raw_dir / JENA_RAW_FILENAME

    if not csv_path.exists() or force:
        csv_path = download_jena_climate(raw_dir, force=force)

    validate_jena_csv(csv_path)
    return csv_path
