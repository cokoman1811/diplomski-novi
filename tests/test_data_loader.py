"""Minimal tests for temperature data loading."""

import pytest

from src.config import JENA_INTERVAL_MINUTES, QUICK_SAMPLE_HOURS
from src.data_loader import load_experiment_series


def test_load_experiment_series_demo():
    series = load_experiment_series("demo", city="Split")

    assert series.name == "temperature"
    assert len(series) == 12
    assert not series.isna().any()
    assert series.index.is_monotonic_increasing


def test_load_experiment_series_jena_quick():
    try:
        series = load_experiment_series("jena_quick")
    except FileNotFoundError:
        pytest.skip("Jena dataset nije preuzet. Pokreni: python main.py --download")

    expected = int(QUICK_SAMPLE_HOURS * 60 / JENA_INTERVAL_MINUTES)
    assert len(series) == expected
    assert series.name == "temperature"
    assert not series.isna().any()
    assert series.index.is_monotonic_increasing
