class ResponseHandler:
    @staticmethod
    def handle_response(response):
        if response:
            try:
                if isinstance(response, list):
                    return response

                json_data = ResponseHandler._parse_json(response)
                if json_data:
                    return json_data
                else:
                    print("Error: No JSON data to return.")
                    return None
            except ValueError as e:
                print(f"ValueError while handling response: {e}")
                return None
            except TypeError as e:
                print(f"TypeError while handling response: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error while handling response: {e}")
                return None
        else:
            print("Error: Response is empty or None.")
            return None

    @staticmethod
    def _parse_json(response):
        try:
            if isinstance(response, dict):
                return response
            else:
                print("Error: Expected a dictionary or list, got:", type(response))
                return None
        except ValueError as e:
            print("JSON parsing error: Response is not valid JSON.")
            print(f"Error details: {e}")
            return None
