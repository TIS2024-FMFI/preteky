from GetFromIsOrienteering import Mod_get
from PostToIsOrienteering import Mod_post
import utilities.ErrorHandler as error


class Procesor():
    def __init__(self):
        self.mod_get = Mod_get() # here we need url endpoit and  api acces key from config file 
        self.mod_post = Mod_post() # same here
        self.categories = {} # dict of category_id : name
        try:
            for category in self.mod_get.get_categories_details(): self.categories[category["id"]]=category["name"]
        except error.IsOrieteeringApiError as e:
            raise e
        
    def get_races_from_IsOrienteering_in_month(self, month : str):
        '''
        
        input:     January
        output:    datum, nazov preteku, deadline prihlasenia, miesto, kategorie 

        '''
        try:
            races = self.mod_get.get_races_in_month(month)
        except error.IsOrieteeringApiError as e:
            return e
        output = [{"id": None, "datum": None, "nazov": None, "deadline": None,
            "miesto": None, "kategorie": None}
            for _ in range(len(races))]
        for i in  range(len(races)):
            id = races[i]["id"]
            try:
                race = self.mod_get.get_race_details(id)
            except error.IsOrieteeringApiError as e:
                return e
            ids_of_categories = [category["category_id"] for category in race["categories"]]
            names_of_categories = [ self.categories[category_id] for category_id in ids_of_categories]
            
            output[i]["id"] = id
            output[i]["datum"] = races[i]["events"][0]["date"]
            output[i]["nazov"] = races[i]["title_sk"]
            output[i]["deadline"] = race["entry_dates"][0]["entries_to"]
            output[i]["miesto"] = races[i]["place"]
            output[i]["kategorie"] = ",".join(names_of_categories)

        
        return output
    
    def import_race_to_Sandberg_Databaze(race_id : int):
        '''
            input: nejake unikatne id preteku
            input do sandbergu: vid race_data_json 
            output: success, error, uz bol v klubovej databaze
        '''
        return "success"

    def get_active_races():
        '''
            ziskaj aktivne preteky z isorienteering
            Implementovat,
            input:     None
            output:    udaje o preteku (datum, nazov preteku, deadline prihlasenia, miesto, kategorie)
            
        '''
        
        
        return [
            {"id": 1,"datum": f"2023-{i**i%12+1}-0{i+1}", "nazov": f"Race {i + 1}", "deadline": f"2023-{i*i%12+1}-1{i+1}",
             "miesto": f"Location {i + 1}", "kategorie": f"Category {i % 3 + 1}"}
            for i in range(5)
        ]

    def sign_racers_to_IsOrienteering(race_id : int):
        '''
            input: potrebne parametre preteku
            output: success, error + API response
        '''
        return "success"
        
   
    def convert_html(race_id : int):
        '''
            Implementovat,
            input: nejake unikatne id preteku
            output: success, error, uz bol v klubovej databaze
        '''
        return "success"
    def convert_csv(race_id : int):
        ...
    def convert_txt(race_id : int):
        ...

    def add_to_google_calendar(race: dict):
        ...
        "po pridani preteku do databazy sa rovno prida aj do kalendara, bude mozne vybrat ze pouzivatel nechce pouzit tuto funkcinalitu"


    def update_google_event(event_id: str, new_data: str): pass

    def delete_from_google_calendar(event_id: str): pass

    def get_runners_from_club():
        "ziska mena bezcov v klube pre uceli zobrazenia statistik"        
        return []
    
    def get_runner_results(runner_id, date_from, date_to):
        "date format YYYY-MM-DD"
        "ziska vysledky bezca v zadanom intervaly"
        pass





race_data_json = """
{
    "id": "1887",
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
            "id": "97531",
            "category_id": "160",
            "category_name": "A - muži"
        },
        {
            "id": "97541",
            "category_id": "161",
            "category_name": "A - ženy"
        },
        {
            "id": "97551",
            "category_id": "162",
            "category_name": "B - muži"
        },
        {
            "id": "98321",
            "category_id": "163",
            "category_name": "B - ženy"
        },
        {
            "id": "98331",
            "category_id": "164",
            "category_name": "C - muži"
        },
        {
            "id": "98341",
            "category_id": "165",
            "category_name": "C - ženy"
        }
    ]
}
"""