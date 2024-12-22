from GetFromIsOrienteering import Mod_get
from PostToIsOrienteering import Mod_post
from database_sandberg_handler import SandbergDatabaseHandler
from config_file_reader import ConfigFileReader
from export_data_to_file import TXTConverter, CSVConverter, HTMLConverter

ERROR_RACE_ID_NOT_FOUND = "error: race_id not found in cache"


class Procesor:
    def __init__(self):
        self.config = ConfigFileReader()
        self.mod_get = Mod_get(self.config.IS_API_ENDPOINT,
                               self.config.IS_API_KEY)  # here we need url endpoit and  api acces key from config file
        self.mod_post = Mod_post(self.config.IS_API_ENDPOINT, self.config.IS_API_KEY)  # same here
        self.sandberg_handler = SandbergDatabaseHandler(self.config.SANDBERG_API_ENDPOINT)
        self.categories = {}  # dict of category_id : name
        self.cache = {
            "competitions": {
                1888: """
                {
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
            }
        }
        # for category in self.mod_get.get_categories_details():
        #     self.categories[category["id"]] = category["name"]

    def get_races_from_IsOrienteering_in_month(self, month: str):
        '''
        
        input:     January
        output:    datum, nazov preteku, deadline prihlasenia, miesto, kategorie 

        '''
        races = self.mod_get.get_races_in_month(month)
        output = [{"id": None, "datum": None, "nazov": None, "deadline": None,
                   "miesto": None, "kategorie": None}
                  for _ in range(len(races))]
        for i in range(len(races)):
            id = races[i]["id"]
            race = self.mod_get.get_race_details(id)
            ids_of_categories = [category["category_id"] for category in race["categories"]]
            names_of_categories = [self.categories[category_id] for category_id in ids_of_categories]

            output[i]["id"] = id
            output[i]["datum"] = races[i]["events"][0]["date"]
            output[i]["nazov"] = races[i]["title_sk"]
            output[i]["deadline"] = race["entry_dates"][0]["entries_to"]
            output[i]["miesto"] = races[i]["place"]
            output[i]["kategorie"] = names_of_categories

        return output

    def import_race_to_Sandberg_Databaze(self, race_id: int):
        """
            input: nejake unikatne id preteku
            input do sandbergu: vid race_data_json
            output: success, error, uz bol v klubovej databaze
        """
        if race_id in self.cache["competitions"]:
            race_data = self.cache["competitions"][race_id]
            try:
                self.sandberg_handler.process_race_data(race_data)
                return "The race has been successfully added."
            except Exception as e:
                return f"{str(e)}"
        else:
            return ERROR_RACE_ID_NOT_FOUND

    def get_active_races(self):
        """
            ziskaj aktivne preteky z isorienteering
            Implementovat,
            input:     None
            output:    udaje o preteku (datum, nazov preteku, deadline prihlasenia, miesto, kategorie)

        """
        return [
            {"id": 1, "datum": f"2023-{i ** i % 12 + 1}-0{i + 1}", "nazov": f"Race {i + 1}",
             "deadline": f"2023-{i * i % 12 + 1}-1{i + 1}",
             "miesto": f"Location {i + 1}", "kategorie": f"Category {i % 3 + 1}"}
            for i in range(5)
        ]

    def add_registered_runners_to_cache(self, race_id: int):
        self.cache.setdefault("registered_runners", {})
        if race_id not in self.cache["registered_runners"]:
            self.cache["registered_runners"][race_id] = self.sandberg_handler.get_last_exported_data()

    def sign_racers_to_IsOrienteering(self, race_id: int):
        """
            input: potrebne parametre preteku
            output: success, error + API response
        """
        try:
            self.sandberg_handler.export_registered_runners(race_id)
        except Exception as e:
            return f"error: {str(e)}"
        self.add_registered_runners_to_cache(race_id)
        return "success"

    def convert_data(self, race_id: int, converter_class):
        if race_id in self.cache["registered_runners"]:
            runners = self.cache["registered_runners"][race_id]
            return converter_class(runners)
        return ERROR_RACE_ID_NOT_FOUND

    def convert_html(self, race_id: int):
        return self.convert_data(race_id, HTMLConverter)

    def convert_csv(self, race_id: int):
        return self.convert_data(race_id, CSVConverter)

    def convert_txt(self, race_id: int):
        return self.convert_data(race_id, TXTConverter)

    def add_to_google_calendar(self, race: dict):
        ...
        "po pridani preteku do databazy sa rovno prida aj do kalendara, bude mozne vybrat ze pouzivatel nechce pouzit tuto funkcinalitu"

    def update_google_event(self, event_id: str, new_data: str):
        pass

    def delete_from_google_calendar(self, event_id: str):
        pass

    def get_runners_from_club(self):
        "ziska mena bezcov v klube pre uceli zobrazenia statistik"
        return []

    def get_runner_results(self, runner_id, date_from, date_to):
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

processor = Procesor()
result = processor.import_race_to_Sandberg_Databaze(1888)
print(result)
result1 = processor.sign_racers_to_IsOrienteering(1888)
result2 = processor.convert_html(1888)
result3 = processor.convert_csv(1888)
result4 = processor.convert_txt(1888)

# toto bude treba ked bude moznost ukladat niekam a ako
exported_data = result3.save_to_file()


