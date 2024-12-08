import requests
import modules.utilities.ErrorHandler as ErrorHandler

class Mod_post():
    def __init__(self, api_endpoint, api_key):
        self._api_endpoint = api_endpoint
        self._api_key = api_key
    
    def _get_header(self):
        return   {
        'x-szos-api-key': {self._api_key},
        'Content-Type': 'application/json'
        }  
    
    def _handle_response_code(response : requests.Response):
        if response.status_code < 200 or response.status_code >= 300:
            raise ErrorHandler.IsOrieteeringApiError(response.text, response.status_code)
        return


    def register_runner(self, race_id, registration_form):
        url = f'{self._api_endpoint}/competitions/{race_id}/entries/save'
        response = requests.get(url, json= registration_form, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
            
    
    def remove_runner(self, race_id, deregistration_form):
        url = f'{self._api_endpoint}/competitions/{race_id}/entries/delete'
        response = requests.get(url, json= deregistration_form, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
            