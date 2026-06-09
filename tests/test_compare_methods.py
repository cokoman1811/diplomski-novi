"""Usporedba klasičnih interpolacijskih metoda — pokreni: python tests/test_compare_methods.py"""

import bootstrap  # noqa: F401

import pandas as pd

from output_format import configure_display, print_section, print_summary
from src.data_loader import load_jena_temperature_slice
from src.evaluation import evaluate_reconstruction
from src.interpolation_methods import (
    forward_fill,
    linear_interpolation,
    time_interpolation,
)
from src.preprocessing import create_missing_values

configure_display()

METHODS = {
    "forward_fill": forward_fill,
    "linear_interpolation": linear_interpolation,
    "time_interpolation": time_interpolation,
}

# 1. Učitaj originalni Jena niz (prvih 48 sati)
series = load_jena_temperature_slice(hours=48)

# 2. Umjetno ukloni vrijednosti i zapamti masku
damaged, mask = create_missing_values(
    series,
    missing_rate=0.4,
    random_state=42,
)

print_summary(series, damaged, mask)

# 3. Pokreni svaku metodu i izračunaj metrike samo na obrisanim mjestima
rows = []

for method_name, method in METHODS.items():
    reconstructed = method(damaged)

    metrics = evaluate_reconstruction(
        original=series,
        reconstructed=reconstructed,
        missing_mask=mask,
    )

    rows.append(
        {
            "method": method_name,
            "mae": metrics["mae"],
            "rmse": metrics["rmse"],
            "r2": metrics["r2"],
        }
    )

# 4. Ispiši usporednu tablicu metrika
results = pd.DataFrame(rows)

print_section("USPOREDBA METODA (metrike samo na obrisanim mjestima)")
print(
    results.to_string(
        index=False,
        formatters={
            "mae": "{:8.4f}".format,
            "rmse": "{:8.4f}".format,
            "r2": "{:8.4f}".format,
        },
    )
)
print()
