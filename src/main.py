"""Command-line entry point for thesis experiments."""

import argparse
from pathlib import Path

from src.config import JENA_INTERVAL_MINUTES, QUICK_SAMPLE_HOURS
from src.data_loader import (
    list_available_cities,
    load_jena_temperature_slice,
    load_temperature_series,
)
from src.download_data import ensure_jena_data
from src.paths import PROCESSED_DIR, RAW_DIR

DEMO_CSV = RAW_DIR / "temperature_demo_cities.csv"
JENA_OUTPUT = PROCESSED_DIR / "jena_temperature.csv"
JENA_QUICK_OUTPUT = PROCESSED_DIR / "jena_temperature_48h.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Eksperimenti za imputaciju nedostajućih vrijednosti u vremenskim nizovima."
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Brzi test: učitaj prvih 48 h Jena temperature i spremi u processed/.",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Preuzmi Jena Climate dataset u data/raw/.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Koristi mali demo CSV s gradovima umjesto Jena dataseta.",
    )
    parser.add_argument(
        "--city",
        type=str,
        help="Grad za demo način (npr. Split). Ako nije zadan, program pita.",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Ponovno preuzmi Jena dataset čak i ako već postoji.",
    )
    return parser


def prompt_city(csv_path: Path) -> str:
    """Ask the user to choose a city from the demo CSV."""
    cities = list_available_cities(csv_path)

    print("Dostupni gradovi:", ", ".join(cities))
    print()

    while True:
        city_input = input("Unesi grad: ").strip()

        if not city_input:
            print("Moraš unijeti naziv grada.")
            continue

        for city in cities:
            if city.lower() == city_input.lower():
                return city

        print(f"Grad '{city_input}' nije u podacima. Pokušaj ponovo.")
        print()


def resolve_city(csv_path: Path, city_arg: str | None) -> str:
    if city_arg:
        cities = list_available_cities(csv_path)
        for city in cities:
            if city.lower() == city_arg.strip().lower():
                return city
        available = ", ".join(cities)
        raise ValueError(f"Grad '{city_arg}' nije u podacima. Dostupno: {available}")

    return prompt_city(csv_path)


def save_series(series, output_path: Path, label: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    series.to_frame().to_csv(output_path, index_label="timestamp")

    print()
    print(f"Izvor:    {label}")
    print(f"Zapisa:   {len(series)}")
    print(f"Od:       {series.index.min()}")
    print(f"Do:       {series.index.max()}")
    if "jena" in label.lower():
        print(f"Interval: {JENA_INTERVAL_MINUTES} min")
    print()
    print("Prvih 5 zapisa:")
    print(series.head())
    print()
    print("Zadnjih 5 zapisa:")
    print(series.tail())
    print()
    print(f"Spremno: {output_path}")


def run_jena_quick_mode() -> None:
    csv_path = ensure_jena_data()
    series = load_jena_temperature_slice(hours=QUICK_SAMPLE_HOURS)

    print()
    print("Quick mode — Jena Climate")
    print(f"ULAZ:  {csv_path}")
    print(f"IZLAZ: {JENA_QUICK_OUTPUT}")
    print(f"Uzorka: prvih {QUICK_SAMPLE_HOURS} h ({len(series)} mjerenja svakih {JENA_INTERVAL_MINUTES} min)")

    save_series(series, JENA_QUICK_OUTPUT, "Jena Climate, weather station Jena (Germany)")


def run_jena_full_mode() -> None:
    from src.data_loader import load_jena_temperature

    csv_path = ensure_jena_data()
    series = load_jena_temperature()

    print()
    print("Jena Climate — puni niz")
    print(f"ULAZ:  {csv_path}")
    print(f"IZLAZ: {JENA_OUTPUT}")

    save_series(series, JENA_OUTPUT, "Jena Climate, weather station Jena (Germany)")


def run_demo_mode(city: str) -> None:
    series = load_temperature_series(DEMO_CSV, city=city)
    city_slug = city.lower().replace(" ", "_")
    output_path = PROCESSED_DIR / f"{city_slug}_temperature.csv"

    print()
    print("Demo mode — više gradova")
    print(f"ULAZ:  {DEMO_CSV}")
    print(f"IZLAZ: {output_path}")

    save_series(series, output_path, f"Demo CSV, grad {city}")


def main() -> None:
    args = build_parser().parse_args()

    if args.download or args.force_download:
        path = ensure_jena_data(force=args.force_download)
        print(f"Jena dataset spreman: {path}")
        return

    if args.demo:
        city = resolve_city(DEMO_CSV, args.city)
        print(f"Odabran grad: {city}")
        run_demo_mode(city)
        return

    if args.quick:
        run_jena_quick_mode()
        return

    print("Diplomski projekt — Jena Climate")
    print()
    print("Glavne naredbe:")
    print("  python main.py --download        preuzmi Jena dataset")
    print("  python main.py --quick           brzi test (48 h Jena temperature)")
    print("  python main.py --demo            demo s gradovima Split/Zagreb")
    print("  python main.py --demo --city Split")


if __name__ == "__main__":
    main()
