from GetFromIsOrienteering import Mod_get
from PostToIsOrienteering import Mod_post
from database_sandberg_handler import SandbergDatabaseHandler
from config_file_reader import ConfigFileReader
from export_data_to_file import TXTConverter, CSVConverter, HTMLConverter
import ErrorHandler as error
from  DateConverter import DateConverter
from datetime import datetime
from GoogleCalendarService import GoogleCalendarService



class Procesor:
    def __init__(self):
        self.config = ConfigFileReader()
        self.mod_get = Mod_get(self.config.IS_API_ENDPOINT,
                               self.config.IS_API_KEY)  # here we need url endpoit and  api acces key from config file
        self.mod_post = Mod_post(self.config.IS_API_ENDPOINT, self.config.IS_API_KEY)  # same here
        self.sandberg_handler = SandbergDatabaseHandler(self.config.SANDBERG_API_ENDPOINT)
        self.categories = {}  # dict of category_id : name
        self.dc = DateConverter()
        try:
            for category in self.mod_get.get_categories_details(): self.categories[category["id"]] = category["name"]
        except error.IsOrieteeringApiError as e:
            raise e

        self.races = {}  # dict filled with dicts of races, see function fil_out_cache
        self.club_id = self.config.CLUB_ID  # ulozene v configu
        self.runners = []
        self.google_calendar_service = GoogleCalendarService()


    def get_races_from_IsOrienteering_in_month(self, month: str):
        try:
            races = self.mod_get.get_races_in_month(month)
        except error.IsOrieteeringApiError as e:
            raise e
        output = [{"id": None, "dátum": None, "názov": None, "deadline": None,
                   "miesto": None, "kategorie": None}
                  for _ in range(len(races))]
        for i in range(len(races)):
            id = races[i]["id"]
            try:
                race = self.mod_get.get_race_details(id)
            except error.IsOrieteeringApiError as e:
                raise e
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

            for category in input_race["categories"]:
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
            raise e
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
                raise e
            try:
                deadline_date = self.dc.get_date_object_from_string(race["date_to"] if race["entry_dates"] == [] else  race["entry_dates"][0]["entries_to"])
            except error.HandlerError as e:
                raise e
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

    def fill_runners(self, race_id: int):
        try:
            self.sandberg_handler.export_registered_runners(race_id)
        except error.SandbergDatabaseError as e:
            raise e
        data = self.sandberg_handler.get_last_exported_data()

        for runner in data:
            registration_form = {
                "registration_id": "0",  # ID registrácie, alebo 0, ak prihlasujeme bez prepojenia na registráciu
                "first_name": runner["MENO"],
                "surname": runner["PRIEZVISKO"],
                "reg_number": runner["OS.ČÍSLO"],  # registration number, temporlaly OS.Cislo
                "sportident": runner["ČIP"],  # sportident, temporarly cislo cipu
                "comment": runner["POZNÁMKA"],
                "categories": [
                    {
                        "competition_event_id": self.races[race_id]["events"][0]["id"] if isinstance(
                            self.races[race_id]["events"], list) else self.races[race_id]["events"]["id"],
                        # ID etapy pretekov
                        "competition_category_id": runner["ID_KATÉGORIE"],  # ID kategórie pretekov
                    }
                ],
                "services": []
            }
            self.runners.append(registration_form)

    def sign_runners_to_IsOrienteering(self, race_id: int):
        self.fill_runners(race_id)
        for runner in self.runners:
            try:
                self.mod_post.register_runner(race_id, runner)
            except error.IsOrieteeringApiError as e:
                raise e
        return self.runners

    def convert_data(self, converter_class, race_id=None):
        self.fill_runners(race_id)
        convert_class = converter_class(self.runners)
        convert_class.save_to_file()
        return converter_class(self.runners)

    def convert_html(self, race_id=None):
        return self.convert_data(HTMLConverter, race_id)

    def convert_csv(self, race_id=None):
        return self.convert_data(CSVConverter, race_id)

    def convert_txt(self, race_id=None):
        return self.convert_data(TXTConverter, race_id)

    def add_to_google_calendar(self, race_id):
        race = self.races[race_id]
        try:
            event_id = self.google_calendar_service.add_to_google_calendar(
                summary=race["title_sk"],
                location=race.get("place", "Nešpecifikované"),
                description=f"Pretek: {race['title_sk']} | ID: {race['id']}",
                start_date=race["date_from"],
                end_date=race["date_to"]
            )
            print(f"Udalosť pre pretek {race['title_sk']} bola pridaná do Google Kalendára.")

            if self.dc.get_date_object_from_string(race["deadline"]) != self.dc.get_date_object_from_string(race["date_to"]):
                self.google_calendar_service.add_deadline_event(
                    summary=f"Deadline: {race['title_sk']}",
                    location=race.get("place", "Nešpecifikované"),
                    description=f"Deadline pre registráciu na pretek: {race['title_sk']} | ID: {race['id']}",
                    deadline_date=race["deadline"]
                )
                print(f"Deadline pre pretek {race['title_sk']} bol pridaný do Google Kalendára.")

            return event_id

        except Exception as e:
            print(f"Chyba pri pridávaní udalosti do Google Kalendára: {str(e)}")
            raise error.HandlerError("Nepodarilo sa pridať udalosť do kalendára")

    def update_google_event(self, event_id: str, new_data: str):
        pass

    def delete_from_google_calendar(self, event_id: str):
        pass

    def get_runners_from_club(self):
        output = []
        try:
            runners = self.mod_get.get_club_registrations(self.club_id)
        except error.IsOrieteeringApiError as e:
            raise e
        for runner in runners:
            output.append({"ID": runner["runner"]["id"], "MENO": runner["runner"]["first_name"], "PRIEZVISKO": runner["runner"]["surname"]})
        return output

    def get_runner_results(self, runner_id, date_from, date_to):
        "date format YYYY-MM-DD"
        "ziska vysledky bezca v zadanom intervaly"
        try:
            runner_results = self.mod_get.get_runner_results(runner_id, date_from, date_to)
        except error.IsOrieteeringApiError as e:
            raise e
        try:
            races = self.mod_get.get_races_from_to(date_from, date_to)
        except error.IsOrieteeringApiError as e:
            raise e
        
        atendence = {}
        times_after_first = {}
        date_placement = {}
        for result in runner_results:
            for race in races:
                if race["events"] != [] and race["events"][0]["id"] == result["event_id"]:
                    date = self.dc.get_date_object_from_string(race['date_to'])
                    
                    first_runner_time, number_of_competitors = self.get_race_results(race['id'], race["events"][0]["id"])
                    hours = int(result["time_min"]) // 60
                    minutes = int(result["time_min"]) % 60
                    runner_time = self.dc.get_time_object_from_string(f'{hours}-{minutes}-{result["time_sec"]}')
                    atendence[date.month, date.year] = True
                    times_after_first[race["title_sk"]] = runner_time - first_runner_time
                    date_placement[race["title_sk"]] = (date, result["place"], number_of_competitors)

        runner_name = f'{runner_results[0]['first_name']} {runner_results[0]['surname']}'
        output = [atendence, times_after_first, date_placement, runner_name, "SKS krúžky OB",date_from, date_to]
        return output

    def get_race_results(self, race_id, event_id):
        try:
            results = self.mod_get.get_race_results(race_id, event_id)
        except error.IsOrieteeringApiError as e:
            raise e
        hours = int(results[0]["time_min"]) // 60
        minutes = int(results[0]["time_min"]) % 60
        time_of_first_runner = self.dc.get_time_object_from_string(f'{hours}-{minutes}-{results[0]["time_sec"]}')
        return time_of_first_runner, len(results)


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

# processor = Procesor()
# # processor.get_races_from_IsOrienteering_in_month("December")
# processor.races[1887] = race_data_json
# # result = processor.import_race_to_Sandberg_Databaze(1888)
# # print(result)
# # result1 = processor.sign_racers_to_IsOrienteering(1888)
# # print(result1)
# result2 = processor.convert_html(1887)
# print(result2)
# # result3 = processor.convert_csv(1888)
# # result4 = processor.convert_txt(1888)
