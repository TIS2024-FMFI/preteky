import unittest
from unittest.mock import patch, MagicMock
from preteky.modules.api_client import BaseAPI, APIClient
import requests

from preteky.modules.ErrorHandler import SandbergDatabaseError
from preteky.modules.competition_formatter import CompetitionFormatter
from preteky.modules.database_sandberg_handler import SandbergDatabaseHandler
from preteky.modules.response_handler_export import ResponseHandler


class TestBaseAPI(unittest.TestCase):

    def setUp(self):
        self.api = BaseAPI("https://senzor.robotika.sk/sks/api.php/api")

    def test_build_url(self):
        endpoint = "/competitions/1/export"
        expected_url = "https://senzor.robotika.sk/sks/api.php/api/competitions/1/export"
        self.assertEqual(self.api._build_url(endpoint), expected_url)

    @patch('preteky.modules.api_client.requests.get')
    def test_send_get_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.api._send_get_request("https://senzor.robotika.sk/sks/api.php/api/competitions/1/export")
        self.assertEqual(response.status_code, 200)

    @patch('preteky.modules.api_client.requests.get')
    def test_send_get_request_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")

        with self.assertRaises(SandbergDatabaseError) as context:
            self.api._send_get_request("https://senzor.robotika.sk/sks/api.php/api/competitions/1/export")
        expected_message = "SandbergDatabaseError: 500 GET request failed for https://senzor.robotika.sk/sks/api.php/api/competitions/1/export"
        self.assertEqual(str(context.exception), expected_message)

    @patch('preteky.modules.api_client.requests.post')
    def test_send_post_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.api._send_post_request("https://senzor.robotika.sk/sks/api.php/api/competitions/competition",
                                               {"key": "value"})
        self.assertEqual(response.status_code, 200)

    @patch('preteky.modules.api_client.requests.post')
    def test_send_post_request_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Request failed")

        with self.assertRaises(SandbergDatabaseError) as context:
            self.api._send_post_request("https://senzor.robotika.sk/sks/api.php/api/competitions/competition",
                                        {"key": "value"})

        expected_message = "SandbergDatabaseError: 500 POST request failed for https://senzor.robotika.sk/sks/api.php/api/competitions/competition"
        self.assertEqual(str(context.exception), expected_message)


class TestAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = APIClient("https://senzor.robotika.sk/sks/api.php/api")

    @patch('preteky.modules.api_client.APIClient._send_post_request')
    def test_process_race_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "message": "Race added successfully"}
        mock_post.return_value = mock_response

        race_data = {"race": "data"}
        response = self.client.process_race(race_data)
        self.assertEqual(response, "Race added successfully")

    @patch('preteky.modules.api_client.APIClient._send_post_request')
    def test_process_race_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        race_data = {"race": "data"}
        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.process_race(race_data)
        self.assertEqual(str(context.exception),
                         "SandbergDatabaseError: 400 Unexpected response type: <class 'unittest.mock.MagicMock'>")

    @patch('preteky.modules.api_client.APIClient._send_post_request')
    def test_process_race_invalid_json(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Invalid JSON"
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        race_data = {"race": "data"}
        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.process_race(race_data)
        self.assertEqual(str(context.exception), "SandbergDatabaseError: 200 Invalid JSON response.")

    @patch('preteky.modules.api_client.APIClient._send_post_request')
    def test_process_race_non_success_status(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "failure", "message": "Failed to add race"}
        mock_post.return_value = mock_response

        race_data = {"race": "data"}
        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.process_race(race_data)
        self.assertEqual(str(context.exception),
                         "SandbergDatabaseError: 200 Request failed with message Failed to add race.")

    @patch('preteky.modules.api_client.APIClient._send_post_request')
    def test_process_race_empty_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_post.return_value = mock_response

        race_data = {"race": "data"}
        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.process_race(race_data)
        self.assertEqual(str(context.exception),
                         "SandbergDatabaseError: 200 Unexpected response type: <class 'unittest.mock.MagicMock'>")

    @patch('preteky.modules.api_client.APIClient._send_post_request')
    def test_process_race_internal_server_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        race_data = {"race": "data"}
        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.process_race(race_data)
        self.assertEqual(str(context.exception),
                         "SandbergDatabaseError: 500 Unexpected response type: <class 'unittest.mock.MagicMock'>")

    @patch('preteky.modules.api_client.APIClient._send_get_request')
    def test_export_registered_runners_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": []}
        mock_get.return_value = mock_response

        response = self.client.export_registered_runners(1)
        self.assertEqual(response['status'], "success")

    @patch('preteky.modules.api_client.APIClient._send_get_request')
    def test_export_registered_runners_invalid_json(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Invalid JSON"
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.export_registered_runners(1)
        self.assertEqual(str(context.exception), "SandbergDatabaseError: 200 Invalid JSON response.")

    @patch('preteky.modules.api_client.APIClient._send_get_request')
    def test_export_registered_runners_unexpected_response_type(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = "Unexpected response"
        mock_get.return_value = mock_response

        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.export_registered_runners(1)
        self.assertEqual(str(context.exception), "SandbergDatabaseError: 200 Unexpected response type: <class 'str'>")

    @patch('preteky.modules.api_client.APIClient._send_get_request')
    def test_export_registered_runners_error_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with self.assertRaises(SandbergDatabaseError) as context:
            self.client.export_registered_runners(1)

        self.assertEqual(str(context.exception),
                         "SandbergDatabaseError: 500 Unexpected response type: <class 'unittest.mock.MagicMock'>")
        self.assertEqual(context.exception.code, 500)


class TestCompetitionFormatter(unittest.TestCase):

    def setUp(self):
        self.data = {
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

        self.formatter = CompetitionFormatter(self.data)

    def test_validate_data(self):
        self.formatter.validate_data()

    def test_get_competition_info(self):
        info = self.formatter.get_competition_info()
        self.assertEqual(info['id'], '1888')
        self.assertEqual(info['nazov'], "STRED O LIGA  - 2. kolo")
        self.assertEqual(info['datum'], "2024-12-04 00:00")
        self.assertEqual(info['deadline'], "2024-12-01 00:00")

    def test_get_categories(self):
        categories = self.formatter.get_categories()
        self.assertEqual(len(categories), 6)
        self.assertEqual(categories[0]['name'], "A - muži")
        self.assertEqual(categories[1]['name'], "A - ženy")
        self.assertEqual(categories[2]['name'], "B - muži")
        self.assertEqual(categories[3]['name'], "B - ženy")
        self.assertEqual(categories[4]['name'], "C - muži")
        self.assertEqual(categories[5]['name'], "C - ženy")

    def test_missing_keys(self):
        data = self.data.copy()
        del data['categories']
        with self.assertRaises(ValueError):
            CompetitionFormatter(data)

    def test_empty_categories(self):
        data = self.data.copy()
        data['categories'] = []
        formatter = CompetitionFormatter(data)
        categories = formatter.get_categories()
        self.assertEqual(len(categories), 0)

    def test_invalid_data_types(self):
        data = self.data.copy()
        data['id'] = 1888
        with self.assertRaises(ValueError):
            CompetitionFormatter(data)


class TestResponseHandler(unittest.TestCase):
    def test_handle_response_success_dict(self):
        response = MagicMock()
        response.json.return_value = {"status": "success", "data": {"key": "value"}}
        response.status_code = 200

        result = ResponseHandler.handle_response(response)
        self.assertEqual(result, {"status": "success", "data": {"key": "value"}})

    def test_handle_response_failed_dict(self):
        response = MagicMock()
        response.json.return_value = {"status": "error", "message": "Something went wrong"}
        response.status_code = 400

        with self.assertRaises(SandbergDatabaseError) as context:
            ResponseHandler.handle_response(response)
        self.assertIn("Request failed with message", str(context.exception))

    def test_handle_response_empty_list(self):
        response = MagicMock()
        response.json.return_value = []
        response.status_code = 200

        with self.assertRaises(SandbergDatabaseError) as context:
            ResponseHandler.handle_response(response)
        self.assertIn("Response contains an empty list.", str(context.exception))

    def test_handle_response_unexpected_type(self):
        response = MagicMock()
        response.json.return_value = "unexpected_string"
        response.status_code = 500

        with self.assertRaises(SandbergDatabaseError) as context:
            ResponseHandler.handle_response(response)
        self.assertIn("Unexpected response type", str(context.exception))

    def test_handle_response_invalid_json(self):
        response = MagicMock()
        response.json.side_effect = ValueError("Invalid JSON")
        response.status_code = 502

        with self.assertRaises(SandbergDatabaseError) as context:
            ResponseHandler.handle_response(response)
        self.assertIn("Invalid JSON response.", str(context.exception))

    def test_handle_response_empty_or_none(self):
        response = MagicMock()
        response.json.return_value = None
        response.status_code = 204

        with self.assertRaises(SandbergDatabaseError) as context:
            ResponseHandler.handle_response(None)
        self.assertEqual(str(context.exception), "SandbergDatabaseError: 400 Response is empty or None.")


class TestSandbergDatabaseHandler(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://senzor.robotika.sk/sks/api.php/api"
        self.handler = SandbergDatabaseHandler(self.base_url)

    @patch('preteky.modules.api_client.APIClient.export_registered_runners')
    @patch('preteky.modules.response_handler_export.ResponseHandler.handle_response')
    def test_export_registered_runners_success(self, mock_handle_response, mock_export):
        mock_response = {
            "status": "success",
            "data": []
        }

        mock_export.return_value = mock_response
        mock_handle_response.return_value = mock_response
        self.handler.export_registered_runners(1888)

        last_data = self.handler.get_last_exported_data()

        self.assertIsNotNone(last_data)
        self.assertEqual(last_data, {"status": "success", "data": []})

    @patch('preteky.modules.api_client.APIClient.export_registered_runners')
    @patch('preteky.modules.response_handler_export.ResponseHandler.handle_response')
    def test_export_registered_runners_no_data(self, mock_handle_response, mock_export):
        mock_export.return_value = None
        mock_handle_response.return_value = None

        self.handler.export_registered_runners(1888)
        self.assertIsNone(self.handler.get_last_exported_data())

    @patch('preteky.modules.api_client.APIClient.export_registered_runners')
    def test_export_registered_runners_exception(self, mock_export):
        mock_export.side_effect = SandbergDatabaseError("API error")

        with self.assertRaises(SandbergDatabaseError):
            self.handler.export_registered_runners(1888)
        self.assertEqual(self.handler.get_last_exported_data(), None)

    @patch('preteky.modules.api_client.APIClient.process_race')
    def test_process_race_data_success(self, mock_process):
        race_data_json = {
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

        self.handler.process_race_data(race_data_json)
        mock_process.assert_called_once()


if __name__ == '__main__':
    unittest.main()
