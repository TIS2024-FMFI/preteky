import unittest
from unittest.mock import patch

from preteky.modules.config_file_reader import ConfigFileReader
from preteky.modules.export_data_to_file import TXTConverter, CSVConverter, HTMLConverter


class TestExportDataToFile(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
            {"first_name": "Ján", "surname": "Novák", "reg_number": "123", "sportident": "9876",
             "categories": [{"competition_category_id": "A1"}], "comment": "Poznámka1"},
            {"first_name": "Anna", "surname": "Horáková", "reg_number": "124", "sportident": "9877",
             "categories": [{"competition_category_id": "B2"}], "comment": "Poznámka2"}
        ]
        self.config = ConfigFileReader()

    @patch('preteky.modules.config_file_reader.ConfigFileReader')
    def test_html_converter(self, MockConfigFileReader):
        MockConfigFileReader.return_value.HOME_DIR = "/mock_dir"

        converter = HTMLConverter(self.sample_data)
        content = converter.generate_content()

        self.assertIn("<html>", content)
        self.assertIn("<th onclick=\"filterTable(0)\">MENO</th>", content)
        self.assertIn("<td>Ján</td>", content)
        self.assertIn("<td>Novák</td>", content)
        self.assertIn(converter.get_file_extension(), ".html")

    @patch('preteky.modules.config_file_reader.ConfigFileReader')
    def test_csv_converter(self, MockConfigFileReader):
        MockConfigFileReader.return_value.HOME_DIR = "/mock_dir"

        converter = CSVConverter(self.sample_data)
        content = converter.generate_content()

        self.assertIn("MENO;PRIEZVISKO;OS.ČÍSLO;ČIP;ID_KATÉGORIE;POZNÁMKA", content)
        self.assertIn("Ján;Novák;123;9876;A1;Poznámka1", content)
        self.assertIn(converter.get_file_extension(), ".csv")

    @patch('preteky.modules.config_file_reader.ConfigFileReader')
    def test_txt_converter(self, MockConfigFileReader):
        MockConfigFileReader.return_value.HOME_DIR = "/mock_dir"

        converter = TXTConverter(self.sample_data)
        content = converter.generate_content()

        self.assertIn("Ján Novák (OS.ČÍSLO: 123, ČIP: 9876, I)", content)
        self.assertIn("Anna Horáková (OS.ČÍSLO: 124, ČIP: 9877, I)", content)
        self.assertIn(converter.get_file_extension(), ".txt")

    @patch('preteky.modules.config_file_reader.ConfigFileReader')
    def test_save_to_file(self, MockConfigFileReader):
        MockConfigFileReader = self.config
        converters = [HTMLConverter(self.sample_data), CSVConverter(self.sample_data),
                      TXTConverter(self.sample_data)]
        for converter in converters:
            converter.save_to_file()
            expected_file_path = f"{MockConfigFileReader.HOME_DIR}/exported_runners{converter.get_file_extension()}"
            self.assertTrue(expected_file_path, f"File {expected_file_path} does not exist")
            with open(expected_file_path, "r", encoding="utf-8-sig") as file:
                content = file.read()
                self.assertIn(converter.generate_content(), content)


if __name__ == "__main__":
    unittest.main()
