"""Zajednički format ispisa za sve test skripte."""

import pandas as pd

SECTION_WIDTH = 70
ROWS = 20
NA_DISPLAY = "   NaN"
GAP_DISPLAY = "   ---"


def configure_display(width: int = 120, max_columns: int = 12) -> None:
    """Postavi pandas prikaz tablica u terminalu."""
    pd.set_option("display.width", width)
    pd.set_option("display.max_columns", max_columns)
    pd.set_option("display.float_format", lambda x: f"{x:8.2f}")


def print_section(title: str) -> None:
    """Ispiši naslov sekcije."""
    print()
    print("=" * SECTION_WIDTH)
    print(title)
    print("=" * SECTION_WIDTH)


def print_stat(label: str, value) -> None:
    """Ispiši jedan red sažetka (poravnata oznaka i vrijednost)."""
    print(f"  {label:<40} {value}")


def print_summary(series, damaged, mask) -> None:
    """Ispiši standardni sažetak za preprocessing/interpolaciju."""
    print_section("SAŽETAK")
    print_stat("Broj originalnih zapisa", len(series))
    print_stat("Broj oštećenih zapisa", len(damaged))
    print_stat("Broj umjetno obrisanih vrijednosti", int(mask.sum()))
    print_stat("Broj NaN u damaged", int(damaged.isna().sum()))
    print_stat("Broj vrijednosti koje nisu dirane", int((~mask).sum()))


def print_legend(*lines: str) -> None:
    """Ispiši legendu na kraju testa."""
    print()
    print("Legenda:")
    for line in lines:
        print(f"  {line}")


def format_temperature(value) -> str:
    """Formatiraj temperaturu ili NaN placeholder."""
    return f"{value:8.2f}" if pd.notna(value) else NA_DISPLAY


def format_nan(_value) -> str:
    """Uvijek prikaži NaN placeholder."""
    return NA_DISPLAY


def format_gap(_value) -> str:
    """Placeholder kad razlika nema smisla (obrisana vrijednost)."""
    return GAP_DISPLAY
