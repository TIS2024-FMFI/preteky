import utilities.date_converter as date_converter
import requests
import utilities.ErrorHandler as ErrorHandler

class Mod_get():
    def __init__(self, api_endpoint : str, api_key : str):
        self._api_endpoint = api_endpoint
        self._api_key = api_key
    def _get_header(self):
        return   {
        'x-szos-api-key': self._api_key,
        'Content-Type': 'application/json'
        }  
    def _handle_response_code(self, response : requests.Response):
        if response.status_code < 200 or response.status_code >= 300:
            raise ErrorHandler.IsOrieteeringApiError(response.reason+" "+response.url, response.status_code)
        return
    
    
    def get_races_in_month(self, month):
        url = f'{self._api_endpoint}/competitions'
        param = {"date_from" :{date_converter.return_date_with_first_day_of_month(month)} , "date_to" :{date_converter.return_date_with_last_day_of_month(month)}}
        response = requests.get(url, headers=self._get_header(), params=param)
        self._handle_response_code(response)
        return response.json()
    
    def get_races_from_date(self, date):
        url = f'{self._api_endpoint}/competitions'
        param = {"date_from" : {}}
        response = requests.get(url, headers=self._get_header(), params=param)
        self._handle_response_code(response)
        return response.json()
        
    def get_club_registrations(self, club_id):
        url = f'{self._api_endpoint}/clubs/{club_id}/registrations'
        response = requests.get(url, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
           
    
    def get_runner(self, runner_id):
        url = f'{self._api_endpoint}/runners/{runner_id}'
        response = requests.get(url, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
            
    
    def get_race_details(self, race_id):
        url = f'{self._api_endpoint}/competitions/{race_id}'
        response = requests.get(url, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
        
        
    def get_runner_results(self, runner_id, date_from, date_to): ### date_from a date_to musia byt vo formate YYYY-MM-DD
        url = f'{self._api_endpoint}/runners/{runner_id}/results'
        param = {"date_from" : {date_from}, "date_to" : {date_to}}
        response = requests.get(url, headers=self._get_header(), params=param)
        self._handle_response_code(response)
        return response.json()
    
    def get_race_results(self, race_id, event_id):
        url = f'{self._api_endpoint}/competitions/{race_id}/results/{event_id}'
        response = requests.get(url, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
            
        
    def get_race_registration(self, race_id, club_id):
        url = f'{self._api_endpoint}/competitions/{race_id}/entries'
        param = club_id
        response = requests.get(url, headers=self._get_header(), params=param)
        self._handle_response_code(response)
        return response.json()
            
        
    def get_runner_kategories(self, racer_registration_id, event_id):
        url = f'{self._api_endpoint}/registrations/{racer_registration_id}/categories/{event_id}'
        response = requests.get(url, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
        
    def get_categories_details(self):
        url = f'{self._api_endpoint}/lists/category'
        response = requests.get(url, headers=self._get_header())
        self._handle_response_code(response)
        return response.json()
    


