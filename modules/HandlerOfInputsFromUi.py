from GetFromIsOrienteering import Mod_get
from PostToIsOrienteering import Mod_post
from database_sandberg_handler import SandbergDatabaseHandler
from config_file_reader import ConfigFileReader
from export_data_to_file import TXTConverter, CSVConverter, HTMLConverter
import ErrorHandler as error
from  DateConverter import DateConverter
from datetime import datetime


class Procesor:
    def __init__(self):
        self.config = ConfigFileReader()
        self.mod_get = Mod_get(self.config.IS_API_ENDPOINT,
                               self.config.IS_API_KEY)  # here we need url endpoit and  api acces key from config file
        self.mod_post = Mod_post(self.config.IS_API_ENDPOINT, self.config.IS_API_KEY)  # same here
        self.sandberg_handler = SandbergDatabaseHandler(self.config.SANDBERG_API_ENDPOINT)
        self
        self.categories = {}  # dict of category_id : name
        self.dc = DateConverter()
        try:
            for category in self.mod_get.get_categories_details(): self.categories[category["id"]] = category["name"]
        except error.IsOrieteeringApiError as e:
            raise e

        self.races = {}  # dict filled with dicts of races, see function fil_out_cache
        self.club_id = self.config.CLUB_ID  # ulozene v configu
        self.runners = []

    def get_races_from_IsOrienteering_in_month(self, month: str):
        try:
            races = self.mod_get.get_races_in_month(month)
        except error.IsOrieteeringApiError as e:
            return f'{str(e)}'
        output = [{"id": None, "dátum": None, "názov": None, "deadline": None,
                   "miesto": None, "kategorie": None}
                  for _ in range(len(races))]
        for i in range(len(races)):
            id = races[i]["id"]
            try:
                race = self.mod_get.get_race_details(id)
            except error.IsOrieteeringApiError as e:
                return f'{str(e)}'
            try:
                self.fill_out_cache(race)
            except error.HandlerError:
                pass
            ids_of_categories = [category["category_id"] for category in race["categories"]]
            names_of_categories = [self.categories[category_id] for category_id in ids_of_categories]
            output[i]["id"] = id
            output[i]["dátum"] = races[i]["date_to"]
            output[i]["názov"] = races[i]["title_sk"]
            output[i]["deadline"] = race["date_to"] if race["entry_dates"] == [] else race["entry_dates"][0]["entries_to"]
            output[i]["miesto"] = races[i]["place"]
            output[i]["kategorie"] = ",".join(names_of_categories)

        return output

    def fill_out_cache(self, input_race: dict):
        if input_race["id"] not in self.races.keys():
            race = {
                "id": input_race["id"],
                "title_sk": input_race["title_sk"],
                "date_from": input_race["date_from"],
                "date_to": input_race["date_to"],
                "cancelled": input_race["cancelled"],
                "deadline": input_race["date_to"] if input_race["entry_dates"] == [] else input_race["entry_dates"][0]["entries_to"],
                "events": {"id": None if input_race["events"] == [] else input_race["events"][0]["id"]},
                "categories": []
            }

            for category in race["categories"]:
                tmp_category = {"id": category["id"], "category_id": category["category_id"],
                                "category_name": self.categories[category["category_id"]]}
                race["categories"].append(tmp_category)

            self.races[race["id"]] = race
        else:
            raise error.HandlerError("Race already in cache")

    # def import_race_to_Sandberg_Databaze(race_id : int):

    #         output[i]["kategorie"] = names_of_categories

    #     return output

    def import_race_to_Sandberg_Database(self, race_id: int):

        if race_id in self.races.keys():
            race_data = self.races[race_id]
            try:
                self.sandberg_handler.process_race_data(race_data)
                return "The race has been successfully added."
            except error.SandbergDatabaseError as e:
                return f"{str(e)}"
        else:
            raise error.HandlerError("race_id not found in cache")

    def get_active_races(self):
        try:
            active_races = self.mod_get.get_races_from_date()
        except error.IsOrieteeringApiError as e:
            return f'{str(e)}'
        output = []
        output_dict = {"id": None, "datum": None, "nazov": None, "deadline": None,
                       "miesto": None, "kategorie": None}
        for i in range(len(active_races)):
            output_dict = {"id": None, "datum": None, "nazov": None, "deadline": None,
                           "miesto": None, "kategorie": None}
            id = active_races[i]["id"]
            try:
                race = self.mod_get.get_race_details(id)
            except error.IsOrieteeringApiError as e:
                return f'{str(e)}'
            try:
                deadline_date = self.dc.get_date_object_from_string(race["date_to"] if race["entry_dates"] == [] else  race["entry_dates"][0]["entries_to"])
            except error.HandlerError as e:
                return f'{str(e)}'
            try:
                self.fill_out_cache(race)
            except error.HandlerError:
                pass

            if deadline_date > datetime.now():
                ids_of_categories = [category["category_id"] for category in race["categories"]]
                names_of_categories = [self.categories[category_id] for category_id in ids_of_categories]
                output_dict["id"] = id
                output_dict["dátum"] = race["events"][0]["date"]
                output_dict["názov"] = race["title_sk"]
                output_dict["deadline"] = race["date_to"] if race["entry_dates"] == [] else  race["entry_dates"][0]["entries_to"]
                output_dict["miesto"] = race["place"]
                output_dict["kategorie"] = ",".join(names_of_categories)
                output.append(output_dict)

        return output

    def sign_racers_to_IsOrienteering(self, race_id: int):
        """
            input: potrebne parametre preteku
            output: success, error + API response
        """
        try:
            self.sandberg_handler.export_registered_runners(race_id)
        except error.SandbergDatabaseError as e:  # test this
            return f'{str(e)}'
        data = self.sandberg_handler.get_last_exported_data()

        for runner in data:
            registration_form = {
                "registration_id": "0",  ##ID registrácie, alebo 0, ak prihlasujeme bez prepojenia na registráciu
                "first_name": runner["MENO"],
                "surname": runner["PRIEZVISKO"],
                "reg_number": runner["OS.ČÍSLO"],  ##registration number, temporlaly OS.Cislo
                "sportident": runner["ČIP"],  ##sportident, temporarly cislo cipu
                "comment": runner["POZNÁMKA"],
                "categories": [
                    {
                        "competition_event_id": self.races[race_id]["events"][0]["id"] if isinstance(
                            self.races[race_id]["events"], list) else self.races[race_id]["events"]["id"],
                        # //ID etapy pretekov
                        "competition_category_id": runner["ID_KATÉGORIE"],  # //ID kategórie pretekov
                    }
                ],
                "services": []
            }
            self.runners.append(registration_form)
            # try:
            #     self.mod_post.register_runner(race_id, registration_form)
            # except error.IsOrieteeringApiError as e:
            #     return f'{str(e)}'
        return self.runners

    def convert_data(self, converter_class, output_dir=None):
        if self.runners:
            runners = self.runners
            convert_class = converter_class(runners)
            convert_class.save_to_file(output_dir)
            return converter_class(runners)
        else:
            raise error.HandlerError("race_id not found in cache")

    def convert_html(self, output_dir=None):
        return self.convert_data(HTMLConverter, output_dir)

    def convert_csv(self, output_dir=None):
        return self.convert_data(CSVConverter, output_dir)

    def convert_txt(self, output_dir=None):
        return self.convert_data(TXTConverter, output_dir)

    def add_to_google_calendar(self, race: dict):
        ...
        "po pridani preteku do databazy sa rovno prida aj do kalendara, bude mozne vybrat ze pouzivatel nechce pouzit tuto funkcinalitu"

    def update_google_event(self, event_id: str, new_data: str):
        pass

    def delete_from_google_calendar(self, event_id: str):
        pass

    def get_runners_from_club(self):
        output = []
        try:
            runners = self.mod_get.get_club_registrations(self.club_id)
        except error.IsOrieteeringApiError as e:
            return f'{str(e)}'
        for runner in runners:
            output.append({"ID": runner["runner"]["id"], "MENO": runner["runner"]["first_name"], "PRIEZVISKO": runner["runner"]["surname"]})
        return output

    def get_runner_results(self, runner_id, date_from, date_to):
        "date format YYYY-MM-DD"
        "ziska vysledky bezca v zadanom intervaly"
        try:
            results = self.mod_get.get_runner_results(runner_id, date_from, date_to)
        except error.IsOrieteeringApiError as e:
            return f'{str(e)}'
        return results


# kedze toto je ako dict a nie ako json string (co bolo povodne), tak sa pomenil database_sandberg_handler.py
race_data_json = {
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

processor = Procesor()
processor.get_races_from_IsOrienteering_in_month("December")
# processor.races[1888] = race_data_json
# result = processor.import_race_to_Sandberg_Databaze(1888)
# print(result)
# result1 = processor.sign_racers_to_IsOrienteering(1888)
# print(result1)
# result2 = processor.convert_html("C:\\Users\\miria")
# print(result2)
# result3 = processor.convert_csv(1888)
# result4 = processor.convert_txt(1888)
