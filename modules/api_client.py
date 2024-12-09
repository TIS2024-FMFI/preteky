import requests

SUCCESS_CODE = 200

"""Base class providing common methods for API communication."""


class BaseAPI:
    def __init__(self, base_urli):
        self.base_url = base_urli

    def _build_url(self, endpoint):
        return f"{self.base_url}{endpoint}"

    @staticmethod
    def _send_get_request(url):
        try:
            response = requests.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    @staticmethod
    def _send_post_request(url, data):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None


class APIClient(BaseAPI):
    def process_race(self, race_data):
        url = self._build_url("/competitions/competition")
        response = self._send_post_request(url, race_data)

        if response.status_code == SUCCESS_CODE:
            if response.text.strip():
                try:
                    json_response = response.json()
                    if json_response.get('status') == "success":
                        print(json_response.get('message'))
                    else:
                        print(f"Failed to add race: {json_response.get('message')}")
                    return json_response
                except ValueError:
                    return {"status": "error", "message": "Invalid JSON response"}
            else:
                return {"status": "error", "message": "Empty response from API"}
        else:
            self._log_error(response)
            return {"status": "error", "message": f"Failed to process race. {response.text}"}

    def export_registered_runners(self, id_pret):
        url = self._build_url(f"/competitions/{id_pret}/export")
        response = self._send_get_request(url)

        if response.status_code == SUCCESS_CODE:
            try:
                json_response = response.json()

                if isinstance(json_response, dict):
                    if json_response.get('status') == "success":
                        return json_response
                    else:
                        print(f"Error: {json_response.get('message')}")
                        return None
                elif isinstance(json_response, list):
                    return json_response
                else:
                    print("Unexpected response type.")
                    return None
            except ValueError:
                print("Error: Invalid JSON response")
                return None
        else:
            self._log_error(response)
            return None



    @staticmethod
    def _log_error(response):
        print(f"Error: {response.status_code} - {response.text}")
