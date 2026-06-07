"""Ručni test za create_missing_values — pokreni iz korijena: python test_preprocessing.py"""

import sys

import pandas as pd

from src.data_loader import load_jena_temperature_slice
from src.preprocessing import create_missing_values

# Čitljiviji ispis u terminalu (hrvatski znakovi + poravnati stupci)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)
pd.set_option("display.float_format", lambda x: f"{x:7.2f}")

ROWS = 20


def print_section(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# 1. Učitaj originalni Jena niz (prvih 48 sati)
series = load_jena_temperature_slice(hours=48)

# 2. Umjetno ukloni 20% vrijednosti i zapamti masku
damaged, mask = create_missing_values(
    series,
    missing_rate=0.2,
    random_state=42,
)

# 3. Sažetak brojeva
unchanged_count = int((~mask).sum())

print_section("SAŽETAK")
print(f"Broj originalnih zapisa:              {len(series)}")
print(f"Broj oštećenih zapisa:                {len(damaged)}")
print(f"Broj umjetno obrisanih vrijednosti:   {int(mask.sum())}")
print(f"Broj NaN vrijednosti u damaged:       {int(damaged.isna().sum())}")
print(f"Broj vrijednosti koje nisu dirane:    {unchanged_count}")

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
        na_rep="  NaN  ",
        formatters={
            "original_temperature": "{:7.2f}".format,
            "damaged_temperature": lambda x: f"{x:7.2f}" if pd.notna(x) else "  NaN  ",
            "razlika": lambda x: f"{x:7.2f}" if pd.notna(x) else "  ---  ",
        },
    )
)

# 6. Samo obrisane vrijednosti — najjasniji prikaz razlike
removed = comparison[comparison["missing_mask"]].copy()

print_section(f"SAMO OBRISANE VRIJEDNOSTI — prvih {ROWS} redova")
print(
    removed.head(ROWS).to_string(
        na_rep="  NaN  ",
        formatters={
            "original_temperature": "{:7.2f}".format,
            "damaged_temperature": lambda _: "  NaN  ",
            "razlika": lambda x: "  ---  ",
        },
    )
)
print()
print("Legenda:")
print("  OK        = vrijednost nije dirana (original == damaged)")
print("  OBRISANO  = vrijednost zamijenjena s NaN")
print("  razlika   = original - damaged (0.00 kad nije dirano, --- kad je obrisano)")
