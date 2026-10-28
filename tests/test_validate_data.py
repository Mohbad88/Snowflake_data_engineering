import tempfile
import unittest
from pathlib import Path

from scripts.validate_data import validate_csv


class ValidateCsvTests(unittest.TestCase):
    def test_accepts_header_and_rows_with_expected_columns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "sample.csv"
            csv_path.write_text("id,name\n1,Ada\n2,Lin\n", encoding="utf-8")

            row_count, errors = validate_csv(csv_path, ("id", "name"))

        self.assertEqual(row_count, 2)
        self.assertEqual(errors, [])

    def test_reports_incorrect_header_and_row_width(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "sample.csv"
            csv_path.write_text("id,label\n1\n", encoding="utf-8")

            row_count, errors = validate_csv(csv_path, ("id", "name"))

        self.assertEqual(row_count, 1)
        self.assertEqual(len(errors), 2)
        self.assertIn("colonnes incorrectes", errors[0])
        self.assertIn("enregistrement 1", errors[1])

    def test_reports_empty_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "empty.csv"
            csv_path.write_text("", encoding="utf-8")

            row_count, errors = validate_csv(csv_path, ("id",))

        self.assertEqual(row_count, 0)
        self.assertEqual(errors, ["fichier vide, en-tête manquant"])


if __name__ == "__main__":
    unittest.main()
