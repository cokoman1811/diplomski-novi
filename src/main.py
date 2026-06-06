"""Command-line entry point for thesis experiments."""

import argparse
from pathlib import Path

from src.data_loader import load_temperature_series


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Eksperimenti za imputaciju nedostajućih vrijednosti u vremenskim nizovima."
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Brzi test na manjem uzorku podataka.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.quick:
        series = load_temperature_series(
            "data/raw/temperature_demo_cities.csv",
            city="Split",
        )

        print("Quick mode pokrenut.")
        print()
        print("ULAZ:  data/raw/temperature_demo_cities.csv")
        print("IZLAZ: data/processed/split_temperature.csv")
        print()
        print(f"Učitane temperature za Split ({len(series)} zapisa):")
        print(f"  Od:  {series.index.min()}")
        print(f"  Do:  {series.index.max()}")
        print()
        print("Prvih 5 zapisa:")
        print(series.head())
        print()
        print("Zadnjih 5 zapisa:")
        print(series.tail())

        output_path = Path("data/processed/split_temperature.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        series.to_frame().to_csv(output_path, index_label="timestamp")

        print()
        print(f"Spremanje: samo Split, stupci timestamp + temperature")
        print(f"Datoteka:  {output_path}")
    else:
        print("Projekt je spreman.")
        print("Pokreni brzi test naredbom:")
        print("python .\\main.py --quick")


if __name__ == "__main__":
    main()