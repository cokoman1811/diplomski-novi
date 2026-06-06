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
        print("Učitane temperature za Split:")
        print(series.head())

        output_path = Path("data/processed/split_temperature.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        series.to_frame().to_csv(output_path, index_label="timestamp")

        print()
        print(f"CSV za Split spremljen je ovdje: {output_path}")
        print(f"Broj zapisa: {len(series)}")
    else:
        print("Projekt je spreman.")
        print("Pokreni brzi test naredbom:")
        print("python .\\main.py --quick")


if __name__ == "__main__":
    main()