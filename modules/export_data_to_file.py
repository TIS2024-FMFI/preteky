from abc import ABC, abstractmethod
import os
from config_file_reader import ConfigFileReader


class ExportDataToFile(ABC):
    def __init__(self, race_data: list):
        self.race_data = race_data
        self.base_name = "exported_runners"
        self.config = ConfigFileReader()
        self.output_dir = self.config.HOME_DIR

    @abstractmethod
    def generate_content(self) -> str:
        """
        Implement this method to generate specific format content
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Returns the file extension specific to the format
        """
        pass

    def save_to_file(self):
        """
        Save the content to a file with the appropriate name and extension
        """
        self.output_dir = self.config.HOME_DIR

        if not self.output_dir:
            raise ValueError("Output directory is not set")

        os.makedirs(self.output_dir, exist_ok=True)

        file_name = f"{self.base_name}{self.get_file_extension()}"
        file_path = os.path.join(self.output_dir, file_name)

        content = self.generate_content()
        with open(file_path, "w", encoding="utf-8-sig") as file:
            file.write(content)
        print(f"Content saved to {file_path}")


class HTMLConverter(ExportDataToFile):
    def generate_content(self) -> str:
        html_content = """
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>ÚDAJE O PRETEKOCH</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 20px;
                            background-color: #f5f5dc; /* Beige background */
                        }
                        h1 {
                            color: #4CAF50;
                            text-align: center;
                            text-transform: uppercase;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                        }
                        th, td {
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #4CAF50;
                            color: white;
                            cursor: pointer;
                        }
                        tr:nth-child(odd) {
                            background-color: #bbf4bd; /* Light green background for odd rows */
                        }
                        tr:hover {
                            background-color: #9ae89d;
                        }
                        td:first-child, nth-child(2) {
                            font-weight: bold; /* Bold names */
                        }
                    </style>
                    <script>
                        function filterTable(n) {
                            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
                            table = document.getElementById("raceTable");
                            switching = true;
                            dir = "asc";
                            while (switching) {
                                switching = false;
                                rows = table.rows;
                                for (i = 1; i < (rows.length - 1); i++) {
                                    shouldSwitch = false;
                                    x = rows[i].getElementsByTagName("TD")[n];
                                    y = rows[i + 1].getElementsByTagName("TD")[n];
                                    if (dir == "asc") {
                                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                                            shouldSwitch = true;
                                            break;
                                        }
                                    } else if (dir == "desc") {
                                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                            shouldSwitch = true;
                                            break;
                                        }
                                    }
                                }
                                if (shouldSwitch) {
                                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                                    switching = true;
                                    switchcount ++;
                                } else {
                                    if (switchcount == 0 && dir == "asc") {
                                        dir = "desc";
                                        switching = true;
                                    }
                                }
                            }
                        }
                    </script>
                </head>
                <body>
                    <h1>ÚDAJE O PRIHLÁSENÝCH PRETEKÁROCH</h1>
                    <table id="raceTable">
                        <tr>
                            <th onclick="filterTable(0)">MENO</th>
                            <th onclick="filterTable(1)">PRIEZVISKO</th>
                            <th onclick="filterTable(2)">OS.ČÍSLO</th>
                            <th onclick="filterTable(3)">ČIP</th>
                            <th onclick="filterTable(4)">ID_KATÉGORIE</th>
                            <th onclick="filterTable(5)">POZNÁMKA</th>
                        </tr>
                """
        for item in self.race_data:
            html_content += f"""
                <tr>
                    <td>{item['first_name']}</td>
                    <td>{item['surname']}</td>
                    <td>{item['reg_number']}</td>
                    <td>{item['sportident']}</td>
                    <td>{item['categories'][0]['competition_category_id']}</td>
                    <td>{item['comment']}</td>
                </tr>
            """
        html_content += """
            </table>
        </body>
        </html>
        """
        return html_content

    def get_file_extension(self) -> str:
        return ".html"


class CSVConverter(ExportDataToFile):
    def generate_content(self) -> str:
        csv_content = "OS.ČÍSLO;ID_KATÉGORIE;ČIP;PRIEZVISKO;MENO;POZNÁMKA\n"
        for item in self.race_data:
            csv_content += f"{item['reg_number']};{item['categories'][0]['competition_category_id']};{item['sportident']};{item['surname']};{item['first_name']};{item['comment']}\n"
        return csv_content

    def get_file_extension(self) -> str:
        return ".csv"


class TXTConverter(ExportDataToFile):
    def generate_content(self) -> str:
        txt_content = ""
        for item in self.race_data:
            txt_content += f"{item['first_name']} {item['surname']} (OS.ČÍSLO: {item['reg_number']}, ČIP: {item['sportident']}, I)\n"
        return txt_content

    def get_file_extension(self) -> str:
        return ".txt"
