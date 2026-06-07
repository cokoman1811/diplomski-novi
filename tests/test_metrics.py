"""Ručni test za evaluate_reconstruction — pokreni: python tests/test_metrics.py"""

import bootstrap  # noqa: F401

import pandas as pd

from output_format import configure_display, print_section, print_stat, print_summary
from src.data_loader import load_jena_temperature_slice
from src.evaluation import evaluate_reconstruction
from src.interpolation_methods import time_interpolation
from src.preprocessing import create_missing_values

configure_display()

# 1. Učitaj podatke i napravi oštećeni niz
series = load_jena_temperature_slice(hours=48)

damaged, mask = create_missing_values(
    series,
    missing_rate=0.4,
    random_state=42,
)

print_summary(series, damaged, mask)

# 2. Rekonstruiraj i izračunaj metrike
reconstructed = time_interpolation(damaged)

metrics = evaluate_reconstruction(
    original=series,
    reconstructed=reconstructed,
    missing_mask=mask,
)

print_section("METRIKE (time_interpolation, samo obrisana mjesta)")
print_stat("MAE", f"{metrics['mae']:.4f}")
print_stat("RMSE", f"{metrics['rmse']:.4f}")
print_stat("R2", f"{metrics['r2']:.4f}")
print()
