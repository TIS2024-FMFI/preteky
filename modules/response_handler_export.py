from preteky.modules.ErrorHandler import SandbergDatabaseError


class ResponseHandler:
    @staticmethod
    def handle_response(response):
        if not response:
            raise SandbergDatabaseError("Response is empty or None.", 400)
        try:
            json_data = response.json()
            if isinstance(json_data, dict):
                if json_data.get('status') != 'success':
                    raise SandbergDatabaseError(f"Request failed with message {json_data.get('message')}.", response.status_code)
            elif isinstance(json_data, list):
                if not json_data:
                    raise SandbergDatabaseError("Response contains an empty list.", response.status_code)
            else:
                raise SandbergDatabaseError(f"Unexpected response type: {type(json_data)}", response.status_code)
        except ValueError:
            raise SandbergDatabaseError(f"Invalid JSON response.", response.status_code)
        return json_data
