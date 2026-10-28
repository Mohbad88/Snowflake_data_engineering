"""Vérifie la structure des fichiers CSV utilisés par le projet."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

EXPECTED_COLUMNS: dict[str, tuple[str, ...]] = {
    "bookings.csv": (
        "booking_id",
        "listing_id",
        "booking_date",
        "nights_booked",
        "booking_amount",
        "cleaning_fee",
        "service_fee",
        "booking_status",
        "created_at",
    ),
    "hosts.csv": (
        "host_id",
        "host_name",
        "host_since",
        "is_superhost",
        "response_rate",
        "created_at",
    ),
    "listings.csv": (
        "listing_id",
        "host_id",
        "property_type",
        "room_type",
        "city",
        "country",
        "accommodates",
        "bedrooms",
        "bathrooms",
        "price_per_night",
        "created_at",
    ),
}


def validate_csv(path: Path, expected_columns: tuple[str, ...]) -> tuple[int, list[str]]:
    """Vérifie les colonnes et la largeur de chaque ligne d’un fichier CSV."""
    errors: list[str] = []
    row_count = 0

    try:
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.reader(csv_file, strict=True)
            try:
                header = next(reader)
            except StopIteration:
                return 0, ["fichier vide, en-tête manquant"]

            if header != list(expected_columns):
                errors.append(
                    f"colonnes incorrectes (attendu : {', '.join(expected_columns)})"
                )

            for row_count, row in enumerate(reader, start=1):
                if len(row) != len(expected_columns):
                    errors.append(
                        f"enregistrement {row_count} : "
                        f"{len(row)} colonnes au lieu de {len(expected_columns)}"
                    )
    except (OSError, UnicodeError, csv.Error) as error:
        errors.append(str(error))

    if not errors and row_count == 0:
        errors.append("aucune ligne de données")

    return row_count, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Vérifie les en-têtes et les lignes des CSV Airbnb."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "raw",
        help="dossier contenant bookings.csv, hosts.csv et listings.csv",
    )
    args = parser.parse_args()

    has_errors = False
    for filename, expected_columns in EXPECTED_COLUMNS.items():
        path = args.data_dir / filename
        row_count, errors = validate_csv(path, expected_columns)
        if errors:
            has_errors = True
            for error in errors:
                print(f"[ERREUR] {path}: {error}", file=sys.stderr)
        else:
            print(f"[OK] {filename}: {row_count} lignes de données")

    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
