from api_client import APIClient
from competition_formatter import CompetitionFormatter


class SandbergDatabaseHandler:
    def __init__(self, base_urli):
        self.last_exported_data = None
        self.api_client = APIClient(base_urli)

    def get_last_exported_data(self):
        return self.last_exported_data

    def export_registered_runners(self, competition_id):
        self.last_exported_data = self.api_client.export_registered_runners(competition_id)

    def process_race_data(self, json_dict):
        formatter = CompetitionFormatter(json_dict)
        formatted_dict = formatter.format()
        self.last_exported_data = self.api_client.process_race(formatted_dict)

    def get_active_competitions(self):
        return self.api_client.get_active_competitions()
