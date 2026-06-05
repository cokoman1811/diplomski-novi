"""Command-line entry point for thesis experiments."""

import argparse


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
        print("Quick mode — implementacija slijedi u sljedećim koracima.")
    else:
        print("Projekt je spreman. Dodaj module u src/ i pokreni eksperimente.")


if __name__ == "__main__":
    main()
