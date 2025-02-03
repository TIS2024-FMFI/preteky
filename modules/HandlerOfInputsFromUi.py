import ErrorHandler as error

from DateConverter import DateConverter
from datetime import datetime

from GetFromIsOrienteering import Mod_get
from PostToIsOrienteering import Mod_post
from database_sandberg_handler import SandbergDatabaseHandler
from config_file_reader import ConfigFileReader
from export_data_to_file import TXTConverter, CSVConverter, HTMLConverter
import ErrorHandler as error
from DateConverter import DateConverter
from datetime import datetime
from GoogleCalendarService import GoogleCalendarService


class HandlerOfInputsFromUi:
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
            output[i]["deadline"] = race["date_to"] if race["entry_dates"] == [] else race["entry_dates"][0][
                "entries_to"]
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
                "deadline": input_race["date_to"] if input_race["entry_dates"] == [] else input_race["entry_dates"][0][
                    "entries_to"],
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

    def import_race_to_Sandberg_Database(self, race_id: int):

        if race_id in self.races.keys():
            race_data = self.races[race_id]
            try:
                self.sandberg_handler.process_race_data(race_data)
                return "The race has been successfully added."
            except error.SandbergDatabaseError as e:
                raise e
        else:
            raise error.HandlerError("race_id not found in cache")

    def get_active_races(self):
        active_races = self.sandberg_handler.get_active_competitions()
        output = []
        output_dict = {"id": None, "datum": None, "nazov": None, "deadline": None,
                       "miesto": None, "kategorie": None}
        for id in active_races:
            output_dict = {"id": None, "datum": None, "nazov": None, "deadline": None,
                           "miesto": None, "kategorie": None}
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
            output_dict["id"] = id
            output_dict["dátum"] = race["events"][0]["date"]
            output_dict["názov"] = race["title_sk"]
            output_dict["deadline"] = race["date_to"] if race["entry_dates"] == [] else race["entry_dates"][0][
                    "entries_to"]
            output_dict["miesto"] = race["place"]
            output_dict["kategorie"] = ",".join(names_of_categories)
            output.append(output_dict)

        return output

    def fill_runners(self, race_id: int):
        self.runners = []
        if race_id not in self.races.keys():
            self.fill_out_cache(self.mod_get.get_race_details(race_id))
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

    def fill_runners_with_category_names(self, race_id: int):
        self.runners = []
        if race_id not in self.races.keys():
            self.fill_out_cache(self.mod_get.get_race_details(race_id))
        try:
            self.sandberg_handler.export_registered_runners(race_id)
        except error.SandbergDatabaseError as e:
            raise e
        data = self.sandberg_handler.get_last_exported_data()

        for runner in data:
            for category in self.races[race_id]["categories"]:
                if category["id"] == str(runner["ID_KATÉGORIE"]):
                    runner_category_name = category["category_name"]
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
                        "competition_category_id": runner_category_name,  # ID kategórie pretekov
                    }
                ],
                "services": []
            }
            self.runners.append(registration_form)


    def convert_data(self, converter_class, race_id=None):
        self.fill_runners_with_category_names(race_id)
        convert_class = converter_class(self.runners)
        convert_class.save_to_file()
        return converter_class(self.runners)

    def convert_html(self, race_id=None):
        return self.convert_data(HTMLConverter, race_id)

    def convert_csv(self, race_id=None):
        return self.convert_data(CSVConverter, race_id)

    def convert_txt(self, race_id=None):
        return self.convert_data(TXTConverter, race_id)

    def add_to_google_calendar(self, race_id: str):
        """
        Add race event to Google Calendar. If a deadline exists, it adds both the main event and the deadline.
        :param race_id: ID of the race
        :param calendar_id: ID of the calendar
        :return: Event ID of the main race event
        """
        calendar_id=self.config.GOOGLE_EMAIL
        try:
            race = self.races[race_id]

            if "deadline" in race and race["deadline"] and \
                    self.dc.get_date_object_from_string(race["deadline"]) != self.dc.get_date_object_from_string(
                race["date_to"]):
                # Add main event with deadline
                event_id = self.google_calendar_service.add_event_with_deadline(
                    main_event_summary=race["title_sk"],
                    location=race.get("place", "Nešpecifikované"),
                    description=f"Pretek: {race['title_sk']} | ID: {race['id']}",
                    start_date=race["date_from"],
                    end_date=race["date_to"],
                    deadline_date=race["deadline"],
                    calendar_id=calendar_id
                )
            else:
                # Add only main event
                event_id = self.google_calendar_service.add_main_event(
                    summary=race["title_sk"],
                    location=race.get("place", "Nešpecifikované"),
                    description=f"Pretek: {race['title_sk']} | ID: {race['id']}",
                    start_date=race["date_from"],
                    end_date=race["date_to"],
                    calendar_id=calendar_id
                )

            print(f"Udalosť pre pretek {race['title_sk']} bola pridaná do Google Kalendára.")
            return event_id

        except Exception as e:
            print(f"Chyba pri pridávaní udalosti do Google Kalendára: {str(e)}")
            raise error.HandlerError("Nepodarilo sa pridať udalosť do kalendára")

    def update_google_event(self, event_id: str, calendar_id: str, new_data: dict):
        """
        Update an event in Google Calendar.
        :param event_id: ID of the event
        :param calendar_id: ID of the calendar
        :param new_data: Updated data for the event
        """
        try:
            self.google_calendar_service.update_event(event_id, calendar_id, new_data)
            print(f"Udalosť s ID {event_id} bola aktualizovaná v Google Kalendári.")
        except Exception as e:
            print(f"Chyba pri aktualizovaní udalosti v Google Kalendári: {str(e)}")
            raise error.HandlerError("Nepodarilo sa aktualizovať udalosť v kalendári")

    def delete_from_google_calendar(self, event_id: str, calendar_id: str):
        """
        Delete an event from Google Calendar.
        :param event_id: ID of the event
        :param calendar_id: ID of the calendar
        """
        try:
            self.google_calendar_service.delete_event_with_deadline(event_id, calendar_id)
            print(
                f"Udalosť s ID {event_id} bola zmazaná z Google Kalendára spolu s deadline udalosťou (ak existovala).")
        except Exception as e:
            print(f"Chyba pri mazaní udalosti z Google Kalendára: {str(e)}")
            raise error.HandlerError("Nepodarilo sa zmazať udalosť z kalendára")

    def get_runners_from_club(self):
        output = []
        try:
            runners = self.mod_get.get_club_registrations(self.club_id)
        except error.IsOrieteeringApiError as e:
            raise e
        for runner in runners:
            output.append({"ID": runner["runner"]["id"], "MENO": runner["runner"]["first_name"],
                           "PRIEZVISKO": runner["runner"]["surname"]})
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
                    first_runner_time, number_of_competitors = self.get_race_results(race['id'],
                            race["events"][0]["id"], result['competition_category_id'])
                    hours = int(result["time_min"]) // 60
                    minutes = int(result["time_min"]) % 60
                    runner_time = self.dc.get_time_object_from_string(f'{hours}-{minutes}-{result["time_sec"]}')
                    if f"{date.year}-{date.month}" in atendence:
                        atendence[f"{date.year}-{date.month}"] += 1
                    else:
                        atendence[f"{date.year}-{date.month}"] = 1
                    delta =  runner_time - first_runner_time
                    times_after_first[race["title_sk"]] = delta

                    date_placement[race["title_sk"]] = (date, result["place"], number_of_competitors)
        runner =  self.mod_get.get_club_registrations(self.club_id)[runner_id]
        runner_name = f'{runner["runner"]["first_name"]} {runner["runner"]["surname"]}'
        output = [atendence, times_after_first, date_placement, runner_name, "SKS krúžky OB", date_from, date_to]
        return output

    def get_race_results(self, race_id, event_id, competition_category_id):
        try:
            tmp  = self.mod_get.get_race_results(race_id, event_id)
        except error.IsOrieteeringApiError as e:
            raise e
        results = []
        for item in tmp:
            if item['competition_category_id'] == competition_category_id :
                results.append(item)

        hours = int(results[0]["time_min"]) // 60
        minutes = int(results[0]["time_min"]) % 60
        time_of_first_runner = self.dc.get_time_object_from_string(f'{hours}-{minutes}-{results[0]["time_sec"]}')
        return time_of_first_runner, len(results), 


