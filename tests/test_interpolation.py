"""Ručni test za interpolacijske metode — pokreni: python tests/test_interpolation.py"""

import bootstrap  # noqa: F401

import pandas as pd

from output_format import (
    ROWS,
    configure_display,
    format_nan,
    format_temperature,
    print_legend,
    print_section,
    print_stat,
    print_summary,
)
from src.data_loader import load_jena_temperature_slice
from src.evaluation import evaluate_reconstruction
from src.interpolation_methods import (
    forward_fill,
    linear_interpolation,
    time_interpolation,
)
from src.preprocessing import create_missing_values

configure_display(width=140)

METHODS = {
    "forward_fill": forward_fill,
    "linear_interpolation": linear_interpolation,
    "time_interpolation": time_interpolation,
}

# 1. Učitaj original i napravi oštećeni niz s maskom
series = load_jena_temperature_slice(hours=48)
series_before = series.copy()

damaged, mask = create_missing_values(
    series,
    missing_rate=0.4,
    random_state=42,
)
damaged_before = damaged.copy()

print_summary(series, damaged, mask)

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

    print()
    print(f"  --- {name} ---")
    print_stat("NaN nakon interpolacije", int(result.isna().sum()))
    print_stat("Isti index kao original", result.index.equals(series.index))
    print_stat("Isto ime kao original", result.name == series.name)
    print_stat("Original nije promijenjen", series.equals(series_before))
    print_stat("Damaged nije promijenjen", damaged.equals(damaged_before))
    print_stat("MAE (samo obrisana mjesta)", f"{metrics['mae']:.4f}")
    print_stat("RMSE (samo obrisana mjesta)", f"{metrics['rmse']:.4f}")
    print_stat("R2 (samo obrisana mjesta)", f"{metrics['r2']:.4f}")

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
        formatters={
            "original": format_temperature,
            "damaged": format_nan,
            "forward_fill": format_temperature,
            "linear": format_temperature,
            "time": format_temperature,
        },
    )
)

print_legend(
    "damaged      = NaN (rupe koje metode popunjavaju)",
    "forward_fill = zadnja poznata temperatura",
    "linear       = ravna linija između susjeda",
    "time         = interpolacija uz obzir vremena između mjerenja",
)
