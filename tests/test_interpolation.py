"""Ručni test za interpolacijske metode — pokreni: python tests/test_interpolation.py"""

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

pd.set_option("display.width", 140)
pd.set_option("display.max_columns", 12)
pd.set_option("display.float_format", lambda x: f"{x:7.2f}")

ROWS = 20

METHODS = {
    "forward_fill": forward_fill,
    "linear_interpolation": linear_interpolation,
    "time_interpolation": time_interpolation,
}


def print_section(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# 1. Učitaj original i napravi oštećeni niz s maskom
series = load_jena_temperature_slice(hours=48)
series_before = series.copy()

damaged, mask = create_missing_values(
    series,
    missing_rate=0.2,
    random_state=42,
)
damaged_before = damaged.copy()

print_section("ULAZNI PODACI")
print(f"Broj zapisa:                 {len(series)}")
print(f"NaN u damaged:               {int(damaged.isna().sum())}")
print(f"Umjetno obrisano (mask):     {int(mask.sum())}")

# 2. Primijeni svaku metodu i provjeri osnovne uvjete
reconstructed = {}

print_section("REZULTAT PO METODI")
for name, method in METHODS.items():
    result = method(damaged)
    reconstructed[name] = result

    metrics = evaluate_reconstruction(
        original=series,
        reconstructed=result,
        missing_mask=mask,
    )

    print(f"\n--- {name} ---")
    print(f"NaN nakon interpolacije:     {int(result.isna().sum())}")
    print(f"Isti index kao original:     {result.index.equals(series.index)}")
    print(f"Isto ime kao original:       {result.name == series.name}")
    print(f"Original nije promijenjen:   {series.equals(series_before)}")
    print(f"Damaged nije promijenjen:    {damaged.equals(damaged_before)}")
    print("Metrike (samo obrisana mjesta):")
    print(f"  MAE:  {metrics['mae']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  R2:   {metrics['r2']:.4f}")

# 3. Usporedna tablica — samo obrisana mjesta, sve metode jedna pored druge
comparison = pd.DataFrame(
    {
        "original": series,
        "damaged": damaged,
        "forward_fill": reconstructed["forward_fill"],
        "linear": reconstructed["linear_interpolation"],
        "time": reconstructed["time_interpolation"],
        "missing_mask": mask,
    }
)
removed = comparison[comparison["missing_mask"]]

print_section(f"USPOREDBA METODA — prvih {ROWS} obrisanih vrijednosti")
print(
    removed.head(ROWS).to_string(
        na_rep="  NaN  ",
        formatters={
            "original": "{:7.2f}".format,
            "damaged": lambda _: "  NaN  ",
            "forward_fill": "{:7.2f}".format,
            "linear": "{:7.2f}".format,
            "time": "{:7.2f}".format,
        },
    )
)

print()
print("Legenda:")
print("  damaged = NaN (rupe koje metode popunjavaju)")
print("  forward_fill = zadnja poznata temperatura")
print("  linear = ravna linija između susjeda")
print("  time = interpolacija uz obzir vremena između mjerenja")
