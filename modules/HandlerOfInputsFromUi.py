class Procesor():
    def __init__(self):
      
       ... 
    

    def get_races_from_IsOrienteering_in_month(month : str):
        '''
        
        input:     January
        output:    datum, nazov preteku, deadline prihlasenia, miesto, kategorie 

        '''
        return [
            {"id": 1, "datum": f"2023-{month}-0{i+1}", "nazov": f"Race {i + 1}", "deadline": f"2023-{month}-1{i+1}",
            "miesto": f"Location {i + 1}", "kategorie": f"Category {i % 3 + 1}"}
            for i in range(5)
        ]
    
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