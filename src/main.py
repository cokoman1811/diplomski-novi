"""Command-line entry point for thesis experiments."""

import argparse
from pathlib import Path

from src.data_loader import list_available_cities, load_temperature_series

DEFAULT_CSV = Path("data/raw/temperature_demo_cities.csv")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Eksperimenti za imputaciju nedostajućih vrijednosti u vremenskim nizovima."
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Brzi test na manjem uzorku podataka.",
    )
    parser.add_argument(
        "--city",
        type=str,
        help="Grad za učitavanje (npr. Split). Ako nije zadan, program pita interaktivno.",
    )
    return parser


def prompt_city(csv_path: Path) -> str:
    """Ask the user to choose a city from the CSV."""
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


def run_quick_mode(city: str, csv_path: Path = DEFAULT_CSV) -> None:
    series = load_temperature_series(csv_path, city=city)

    city_slug = city.lower().replace(" ", "_")
    output_path = Path(f"data/processed/{city_slug}_temperature.csv")

    print()
    print("Quick mode pokrenut.")
    print()
    print(f"ULAZ:  {csv_path}")
    print(f"IZLAZ: {output_path}")
    print()
    print(f"Učitane temperature za {city} ({len(series)} zapisa):")
    print(f"  Od:  {series.index.min()}")
    print(f"  Do:  {series.index.max()}")
    print()
    print("Prvih 5 zapisa:")
    print(series.head())
    print()
    print("Zadnjih 5 zapisa:")
    print(series.tail())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    series.to_frame().to_csv(output_path, index_label="timestamp")

    print()
    print(f"Spremanje: samo {city}, stupci timestamp + temperature")
    print(f"Datoteka:  {output_path}")


def main() -> None:
    args = build_parser().parse_args()

    if args.quick:
        city = resolve_city(DEFAULT_CSV, args.city)
        print(f"Odabran grad: {city}")
        run_quick_mode(city)
    else:
        print("Projekt je spreman.")
        print("Pokreni brzi test naredbom:")
        print("python .\\main.py --quick")


if __name__ == "__main__":
    main()
