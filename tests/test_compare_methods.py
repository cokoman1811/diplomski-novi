"""Usporedba klasičnih interpolacijskih metoda — pokreni: python tests/test_compare_methods.py"""

import bootstrap  # noqa: F401

import pandas as pd

from src.data_loader import load_jena_temperature_slice
from src.evaluation import evaluate_reconstruction
from src.interpolation_methods import (
    forward_fill,
    linear_interpolation,
    time_interpolation,
)
from src.preprocessing import create_missing_values

pd.set_option("display.float_format", lambda x: f"{x:.4f}")

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
    missing_rate=0.2,
    random_state=42,
)

# 3. Sažetak ulaznih podataka
print()
print("=" * 50)
print("SAŽETAK")
print("=" * 50)
print(f"Broj originalnih zapisa:            {len(series)}")
print(f"Broj oštećenih zapisa:              {len(damaged)}")
print(f"Broj umjetno obrisanih vrijednosti: {int(mask.sum())}")
print(f"Broj NaN u damaged:                 {int(damaged.isna().sum())}")

# 4. Pokreni svaku metodu i izračunaj metrike samo na obrisanim mjestima
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

# 5. Ispiši usporednu tablicu metrika
results = pd.DataFrame(rows)

print()
print("=" * 50)
print("USPOREDBA METODA (metrike samo na obrisanim mjestima)")
print("=" * 50)
print(results.to_string(index=False))
print()
