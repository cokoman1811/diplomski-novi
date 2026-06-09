"""Ručni test za create_missing_values — pokreni: python tests/test_preprocessing.py"""

import bootstrap  # noqa: F401

import pandas as pd

from output_format import (
    ROWS,
    configure_display,
    format_gap,
    format_nan,
    format_temperature,
    print_legend,
    print_section,
    print_summary,
)
from src.data_loader import load_jena_temperature_slice
from src.preprocessing import create_missing_values

configure_display()

# 1. Učitaj originalni Jena niz (prvih 48 sati)
series = load_jena_temperature_slice(hours=48)

# 2. Umjetno ukloni 20% vrijednosti i zapamti masku
damaged, mask = create_missing_values(
    series,
    missing_rate=0.4,
    random_state=42,
)

# 3. Sažetak brojeva
print_summary(series, damaged, mask)

# 4. Zasebne tablice (prvih 20 redova)
print_section(f"ORIGINAL — prvih {ROWS} redova")
print(series.head(ROWS).to_frame(name="temperature"))

print_section(f"DAMAGED — prvih {ROWS} redova")
print(damaged.head(ROWS).to_frame(name="temperature"))

print_section(f"MASK — prvih {ROWS} redova")
print(mask.head(ROWS).to_frame(name="missing_mask"))

# 5. Usporedna tablica: original | damaged | maska | razlika | status
comparison = pd.DataFrame(
    {
        "original_temperature": series,
        "damaged_temperature": damaged,
        "missing_mask": mask,
    }
)
comparison["razlika"] = comparison["original_temperature"] - comparison["damaged_temperature"]
comparison["status"] = comparison["missing_mask"].map({True: "OBRISANO", False: "OK"})

print_section(f"USPOREDBA (side by side) — prvih {ROWS} redova")
print(
    comparison.head(ROWS).to_string(
        formatters={
            "original_temperature": format_temperature,
            "damaged_temperature": format_temperature,
            "razlika": lambda x: format_temperature(x) if pd.notna(x) else format_gap(x),
        },
    )
)

# 6. Samo obrisane vrijednosti — najjasniji prikaz razlike
removed = comparison[comparison["missing_mask"]]

print_section(f"SAMO OBRISANE VRIJEDNOSTI — prvih {ROWS} od {len(removed)}")
print(
    removed.head(ROWS).to_string(
        formatters={
            "original_temperature": format_temperature,
            "damaged_temperature": format_nan,
            "razlika": format_gap,
        },
    )
)

print_legend(
    "OK       = vrijednost nije dirana (original == damaged)",
    "OBRISANO = vrijednost zamijenjena s NaN",
    "razlika  = original - damaged (0.00 kad nije dirano, --- kad je obrisano)",
)
