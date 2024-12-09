import json
import logging

from response_handler_export import ResponseHandler
from competition_formatter import CompetitionFormatter
from api_client import APIClient

logging.basicConfig(level=logging.INFO)


class SandbergDatabaseHandler:
    def __init__(self, base_url):
        self.last_exported_data = None
        self.api_client = APIClient(base_url)

    def get_last_exported_data(self):
        return self.last_exported_data

    def export_registered_runners(self, competition_id):
        try:
            response = self.api_client.export_registered_runners(competition_id)
            json_data = ResponseHandler.handle_response(response)
            if json_data:
                self.last_exported_data = json_data
                print("Data successfully exported.")
            else:
                print("No data exported.")
        except Exception as e:
            logging.info(f"An unexpected error occurred during export: {e}")

    def process_race_data(self, json_string):
        try:
            raw_data = json.loads(json_string)
            formatter = CompetitionFormatter(raw_data)
            formatted_dict = formatter.format()
            self.api_client.process_race(formatted_dict)
        except json.JSONDecodeError as e:
            logging.info(f"Invalid JSON format: {e}")
        except ValueError as e:
            logging.info(f"Error while processing the race data: {e}")
        except Exception as e:
            logging.info(f"An unexpected error occurred during import: {e}")


# Example usage
if __name__ == "__main__":
    base_url = "https://senzor.robotika.sk/sks/api.php/api"
    manager = SandbergDatabaseHandler(base_url)
    competition_id = 1888
    manager.export_registered_runners(competition_id)
    if manager.get_last_exported_data():
        print(json.dumps(manager.get_last_exported_data(), indent=4, ensure_ascii=False))
    race_data_json = """
{
    "id": "1888",
    "title_sk": "STRED O LIGA  - 2. kolo",
    "date_from": "2024-12-04",
    "date_to": "2024-12-04",
    "cancelled": "0",
    "deadline": "2024-12-01",
    "events": {
        "id": "688"
    },
    "categories": [
        {
            "id": "9753",
            "category_id": "160",
            "category_name": "A - muži"
        },
        {
            "id": "9754",
            "category_id": "161",
            "category_name": "A - ženy"
        },
        {
            "id": "9755",
            "category_id": "162",
            "category_name": "B - muži"
        },
        {
            "id": "9832",
            "category_id": "163",
            "category_name": "B - ženy"
        },
        {
            "id": "9833",
            "category_id": "164",
            "category_name": "C - muži"
        },
        {
            "id": "9834",
            "category_id": "165",
            "category_name": "C - ženy"
        }
    ]
}
"""
    manager.process_race_data(race_data_json)
