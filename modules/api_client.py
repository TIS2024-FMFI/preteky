import requests
from ErrorHandler import SandbergDatabaseError
from response_handler_export import ResponseHandler

SUCCESS_CODE = 200
GENERIC_ERROR_CODE = 500


class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def _build_url(self, endpoint):
        return f"{self.base_url}{endpoint}"

    @staticmethod
    def _send_get_request(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            raise SandbergDatabaseError(f"GET request failed for {url}", GENERIC_ERROR_CODE)

    @staticmethod
    def _send_post_request(url, data):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            raise SandbergDatabaseError(f"POST request failed for {url}", GENERIC_ERROR_CODE)


class APIClient(BaseAPI):
    def process_race(self, race_data):
        url = self._build_url("/competitions/competition")
        response = self._send_post_request(url, race_data)
        json_response = ResponseHandler.handle_response(response)

        if json_response.get('status') != "success":
            raise SandbergDatabaseError(f"Failed to add race: {json_response.get('message')}", response.status_code)

        return json_response.get('message')

    def export_registered_runners(self, competition_id):
        url = self._build_url(f"/competitions/{competition_id}/export")
        response = self._send_get_request(url)
        return ResponseHandler.handle_response(response)
