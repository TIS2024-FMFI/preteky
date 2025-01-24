from modules.ErrorHandler import SandbergDatabaseError


class ResponseHandler:
    @staticmethod
    def handle_response(response):
        if not response or response.text.strip() == "":
            raise SandbergDatabaseError("Server returned empty response.", response.status_code)

        try:
            json_data = response.json()
            if isinstance(json_data, dict):
                if json_data.get('status') == "success" and "data" in json_data:
                    if not json_data['data']:
                        raise SandbergDatabaseError("No active races found.", response.status_code)
                else:
                    raise SandbergDatabaseError(f"Unexpected response structure in object: {json_data}",
                                                response.status_code)

            elif isinstance(json_data, list):
                if not json_data:
                    raise SandbergDatabaseError("No active races found.", response.status_code)

            else:
                raise SandbergDatabaseError(f"Unexpected response type: {type(json_data)}", response.status_code)

        except ValueError:
            raise SandbergDatabaseError(f"Invalid JSON response: {response.text}", response.status_code)

        return json_data
