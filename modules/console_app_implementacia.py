import os
import time
import tty
import termios
import sys
from datetime import datetime
from difflib import SequenceMatcher
from HandlerOfInputsFromUi import HandlerOfInputsFromUi
import config_file_reader as config
from DateConverter import DateConverter


####vrati bud zoznam ak to ma zobrazit alebo vrati none ak je finalny
###komunikacia s ostanymi


class Cache:
    def __init__(self):
        self.config = config.ConfigFileReader()
        self.data = {"isOrienteering": {}, "sandberg": {}, "save_path": ""}

    def add_races_orienteering(self, races, date):
        self.data["isOrienteering"][date] = races

    def get_races_orienteering(self, date):
        return self.data["isOrienteering"].get(date)

    def add_races_sandberg(self, races):
        self.data["sandberg"] = races

    def get_races_sandberg(self):
        return self.data.get("sandberg")

    def import_path(self):  ### stiahne z databazy nejakej / konfiguracneho suboru
        self.data["save_path"] = self.config.HOME_DIR

    def save_path(self, path):  ### nastavi novu path v ulozisku
        self.data["save_path"] = path

    def get_path(self):
        if self.data["save_path"] == "":
            self.import_path()
        return self.data["save_path"]

    def set_path(self, path):
        ### nastavit novu path na miesto kde je stara ulozena
        self.save_path(path)
        self.save_path_to_config()

    def save_path_to_config(self):
        self.config.set_home_dir(self.data["save_path"])


class Log:
    def __init__(self):
        self.log_records = []

    def add_record(self, record):
        self.log_records.insert(0, record)

    def display(self):
        print("_" * 40)
        for entry in self.log_records:
            print(entry)


class ConsoleApp:

    def __init__(self):
        self.handler = HandlerOfInputsFromUi()
        self.log = Log()
        self.cache = Cache()
        self.date_converter = DateConverter()
        self.window_general(["Import preteku", "Prihlásenie pretekárov", "Export do súboru", "Štatistiky pretekara"],
                            "MENU", "MENU")
        # pri implementacii cache treba z config file zobrat path

    def run_interface(self, interface_name, *param):
        try:
            if interface_name == "races_from_orienteering":
                cache_contains = self.cache.get_races_orienteering(param[0])
                if not cache_contains:
                    # # races = [
                    # #         {"DÁTUM": f"2023-a-0{i+1}", "NÁZOV": f"Race {i + 1}", "DEADLINE": f"2023-b-1{i+1}",
                    # #         "MIESTO": f"Location {i + 1}", "ID": f"Category {i % 3 + 1}"}
                    # #         for i in range(5)
                    # #     ]
                    month = param[0].split(",")[0]
                    races = self.handler.get_races_from_IsOrienteering_in_month(month)  ### ocheckovat format ci sedi

                    self.cache.add_races_orienteering(races, param[0])
                else:
                    races = cache_contains
                return races

            elif interface_name == "races_from_sandberg":
                cache_contains = self.cache.get_races_sandberg()
                if not cache_contains:
                    # races = [
                    #         {"DÁTUM": f"2023-a-0{i+1}", "NÁZOV": f"Race {i + 1}", "DEADLINE": f"2023-b-1{i+1}",
                    #         "MIESTO": f"Location {i + 1}", "ID": f"Category {i % 3 + 1}"}
                    #         for i in range(5)
                    #     ]
                    races = self.handler.get_active_races()
                    self.cache.add_races_sandberg(races)
                else:
                    races = cache_contains
                return races

            elif interface_name == "Register_racers":
                self.handler.sign_racers_to_IsOrienteering(param[0])

            elif interface_name == "html":
                self.handler.convert_html(param[0])

            elif interface_name == "csv":
                self.handler.convert_csv(param[0])

            elif interface_name == "txt":
                self.handler.convert_txt(param[0])

            elif interface_name == "racers":
                runners = self.handler.get_runners_from_club()
                if param[0] == "Bez filtra":
                    return runners
                if param[0] == "Meno":
                    def is_similar(a, b):
                        return SequenceMatcher(None, a, b).ratio() >= 0.75

                    results = []
                    name_parts = param[1].split()
                    if len(name_parts) == 2:
                        first, last = name_parts
                    else:
                        first, last = name_parts[0], ""
                    for runner in runners:
                        full_name = f"{runner['MENO']} {runner['PRIEZVISKO']}"
                        reversed_name = f"{runner['PRIEZVISKO']} {runner['MENO']}"

                        if (
                                is_similar(full_name.lower(), param[1].lower())
                                or is_similar(reversed_name.lower(), param[1].lower())
                                or is_similar(runner["MENO"].lower(), param[1].lower())
                                or is_similar(runner["PRIEZVISKO"].lower(), param[1].lower())
                        ):
                            if runner not in results:
                                results.append(runner)
                    if results == []:
                        self.log.add_record("Bežec nebol nájdený. Pre opakovanie vyhľadávania stlačte 'b'")
                    return results

                if param[0] == "ID":
                    for i in runners:
                        if i["ID"] == param[1]:
                            return [i]
                    self.log.add_record("Bežec nebol nájdený. Pre opakovanie vyhľadávania stlačte 'b'")
                    return []

            elif interface_name == "import_stat":
                self.handler.get_runner_results(param[2], param[0], param[1])
                return "SUCCESS"

            elif interface_name == "Import preteku":
                self.handler.import_race_to_Sandberg_Database(param[0])
                self.window_general(["Nie", "Áno"], "Chcete zaznačiť pretek do Google Calendar?", "GCal", param[0])

            elif interface_name == "GoogleCalendar":
                self.handler.add_to_google_calendar(param[0])

            self.log.add_record("Akcia zbehla úspešne")

        except Exception as e:
            self.log.add_record(f'{str(e)}')

    def get_key(self):
        """Reads a single keypress."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self, options, current_idx, title):
        self.clear_screen()
        if "ZVOĽTE PRETEK" in title:
            print(
                "(press 'q' to quit, UP and DOWN to navigate, ENTER to select option, 'b' for back, 's' to sort items)")
        else:
            print("(press 'q' to quit, UP and DOWN to navigate, ENTER to select option, 'b' for back)")
        print(f"--- {title} ---")
        for i, option in enumerate(options):
            if i == current_idx:
                print(f"> {option}")
            else:
                print(f"  {option}")

        self.log.display()

    def quit(self):
        main_options = ["Nie", "Áno"]
        current_idx = 0

        while True:
            self.display_menu(main_options, current_idx, "Chcete naozaj odísť?")
            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(main_options) - 1:
                    current_idx += 1
            elif key == '\r':
                if main_options[current_idx] == "Áno":
                    print("Konzola je ukončená")
                    exit()
                elif main_options[current_idx] == "Nie":
                    break

    def race_window(self, *path):
        current_idx = 0
        sort_key = "DÁTUM"
        if path[1] == "Import preteku":
            races = self.run_interface("races_from_orienteering", path[-1])
        else:
            races = self.run_interface("races_from_sandberg")
        while True:
            if sort_key == "DÁTUM" or sort_key == "DEADLINE":
                races = sorted(races,
                               key=lambda x: self.date_converter.get_date_object_from_string(x[sort_key.lower()]))
            else:
                races = sorted(races, key=lambda x: x[sort_key.lower()])
            races_display = [
                f"{p['DÁTUM'.lower()]} | {p['NÁZOV'.lower()]} | {p['DEADLINE'.lower()]} | {p['MIESTO'.lower()]} | {p['ID'.lower()]}"
                for p in races]

            self.display_menu(races_display, current_idx, f"ZVOĽTE PRETEK (zoradené podľa {sort_key})")
            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(races) - 1:
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':
                if path[1] == "Prihlásenie pretekárov":
                    self.double_check("Register_racers",
                                      f"Chcete prihlásiť pretekárov na {races[current_idx]['názov']}",
                                      races[current_idx][
                                          "id"])  ###lepsie bude ak sa jednotlivy racers na pretek zapamataju v nejakej cache pre handler
                elif path[1] == "Export do súboru":
                    self.log.add_record(f"Zvolený pretek {races[current_idx]['NÁZOV'.lower()]}")
                    self.window_general(["html", "csv", "txt"], "ZVOĽTE FORMÁT", *path, races[current_idx])
                elif path[1] == "Import preteku":
                    self.double_check("Import preteku", f"Chcete importovať pretek {races[current_idx]['názov']}",
                                      races[current_idx]["id"])  #### tu je chyba

            elif key.lower() == 'q':
                self.quit()

            elif key == 's':
                sort_keys = ["DÁTUM", "NÁZOV", "DEADLINE", "MIESTO", "ID"]
                sort_key = sort_keys[(sort_keys.index(sort_key) + 1) % len(sort_keys)]

    def months_menu(self, *path):
        now = datetime.now()
        current_month = now.month
        current_year = now.year

        year_offset = 0
        current_idx = 0

        while True:
            months = []
            for i in range(12):
                month_index = (current_month - 1 + i) % 12
                year = current_year + year_offset + (current_month - 1 + i) // 12
                month_name = datetime(1900, month_index + 1, 1).strftime("%B")
                months.append(f"{month_name}, {year}")

            if year_offset > 0:
                months.insert(0, "Previous")
            months.append("Next")

            self.display_menu(months, current_idx, "ZVOĽTE MESIAC")
            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(months) - 1:
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':
                if months[current_idx] == "Previous":
                    year_offset -= 1
                    current_idx = 0
                elif months[current_idx] == "Next":
                    year_offset += 1
                    current_idx = 0
                else:
                    m, y = months[current_idx].split(', ')
                    self.log.add_record(f"Zvolený mesiac {months[current_idx]}")
                    self.race_window(*path, months[current_idx])
            elif key.lower() == 'q':
                self.quit()

    def path_window(self, *path):
        default_path = self.cache.get_path()
        options = ["Pokračovať", "Zmeniť predvolenú path"]
        current_idx = 0

        while True:
            self.display_menu(options, current_idx, f"Prevolená path je: {default_path}. Chcete pokračovať?")
            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(options) - 1:
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':
                if options[current_idx] == "Zmeniť predvolenú path":
                    self.clear_screen()
                    print("Zadajte novú path: ")
                    new_path = input().strip()
                    if os.path.isdir(new_path):
                        default_path = new_path
                        self.log.add_record("Path zmenená úspešne")
                        self.cache.set_path(new_path)
                    else:
                        self.log.add_record("Zvolená path nie je valídna")


                else:
                    if path[-1] in ["html", "csv", "txt"]:
                        self.double_check(path[-1], f"Želáte si exportovať pretek {path[-2]['názov']} do {path[-1]}",
                                          path[-2]['id'])
                    else:
                        self.time_interval(*path)

            elif key.lower() == 'q':
                self.quit()

    def window_general(self, options, title, *path):
        current_idx = 0
        ### ziskat title, options, a ostatne z path
        while True:
            self.display_menu(options, current_idx, title)
            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(options) - 1:
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':
                if len(path) == 1:
                    self.log.add_record(f"Zvolená funkcia {options[current_idx]}")
                    if options[current_idx] == "Import preteku":
                        self.months_menu(*path, "Import preteku")
                    elif options[current_idx] == "Štatistiky pretekara":
                        self.window_general(["Meno", "ID", "Bez filtra"], "Chcete zvoliť filtre?", *path,
                                            options[current_idx])
                    else:
                        self.race_window(*path, options[current_idx])

                elif options[current_idx] in ["html", "csv", "txt"]:
                    self.path_window(*path, options[current_idx])

                elif path[-1] == "Štatistiky pretekara":
                    if options[current_idx] == "Bez filtra":
                        self.racers(*path, "Bez filtra", None)
                    else:
                        self.racers(*path, options[current_idx], self.input_window(options[current_idx]))

                elif path[0] == "GCal":
                    if options[current_idx] == 'Áno':
                        self.run_interface("GoogleCalendar", path[1])
                        break
                    elif options[current_idx] == 'Nie':
                        break


            elif key.lower() == 'q':
                self.quit()

    def input_window(self, title):
        self.clear_screen()
        print(f"Zadajte {title.lower()}: ")
        return input().strip()

    def racers(self, *path):
        current_idx = 0
        sort_key = "ID"
        racers = self.run_interface("racers", path[-2], path[-1])
        while True:
            racers = sorted(racers, key=lambda x: x[sort_key])
            racers_display = [f"{p['ID']} | {p['MENO']} | {p['PRIEZVISKO']}" for p in racers]

            self.display_menu(racers_display, current_idx, f"ZVOĽTE PRETEKÁRA (zoradené podľa {sort_key})")
            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(racers) - 1:
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':
                self.log.add_record(f"Zvolený pretekár {racers[current_idx]}")
                self.path_window(*path, racers[current_idx])


            elif key.lower() == 'q':
                self.quit()

            elif key == 's':
                sort_keys = ["ID", "MENO", "PRIEZVISKO"]
                sort_key = sort_keys[(sort_keys.index(sort_key) + 1) % len(sort_keys)]

    def double_check(self, interface, title, *param):
        options = ["Nie", "Áno"]
        current_idx = 0
        while True:
            self.clear_screen()
            print(title)
            for i, option in enumerate(options):
                if i == current_idx:
                    print(f"> {option}")
                else:
                    print(f"  {option}")

            self.log.display()
            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(options) - 1:
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':
                if options[current_idx] == "Nie":
                    break
                elif options[current_idx] == "Áno":
                    self.run_interface(interface, *param)
                    break
            elif key.lower() == 'q':
                self.quit()

    def time_interval(self, *path):
        options = ["Nastavte začiatok intervalu", "Nastavte koniec intervalu", "Import štatistiky"]
        current_idx = 0
        start_date = None
        end_date = None

        while True:
            self.clear_screen()
            print(f"--- ZVOĽTE INTERVAL ŠTATISTIKY ---")
            print(f"Začiatok intervalu (dátum): {start_date if start_date else 'Nenastavený'}")
            print(f"Koniec intervalu (dátum): {end_date if end_date else 'Nenastavený'}")

            for i, option in enumerate(options):
                if i == current_idx:
                    print(f"> {option}")
                else:
                    print(f"  {option}")
            self.log.display()

            key = self.get_key()
            if key == '\033':
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0:
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(options) - 1:
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':
                if options[current_idx] == "Nastavte začiatok intervalu":
                    self.clear_screen()
                    print("Zadajte dátum začiatku intervalu (YYYY-MM-DD): ")
                    try:
                        start_date = datetime.strptime(input().strip(), "%Y-%m-%d")
                        if end_date is not None and start_date >= end_date:
                            self.log.add_record("Začiatok intervalu musí byť menší ako dátum konca intervalu")
                            start_date = None
                        else:
                            self.log.add_record(f"Začiatok intervalu bol nastavený na {start_date.date()}")
                    except ValueError:
                        self.log.add_record("Formát dátumu nie je valídny")

                elif options[current_idx] == "Nastavte koniec intervalu":
                    self.clear_screen()
                    print("Zadajte dátum konca intervalu (YYYY-MM-DD): ")
                    try:
                        end_date = datetime.strptime(input().strip(), "%Y-%m-%d")
                        if start_date is not None and start_date >= end_date:
                            self.log.add_record("Koniec intervalu musí byť väčší ako dátum začiatku intervalu")
                            end_date = None
                        else:
                            self.log.add_record(f"Koniec intervalu bol nastavený na {end_date.date()}")
                    except ValueError:
                        self.log.add_record("Formát dátumu nie je valídny")

                elif options[current_idx] == "Import štatistiky":
                    if start_date and end_date:
                        self.double_check("import_stat",
                                          f"Chcete importovať štatistiku pretekára {path[-1]['MENO']} {path[-1]['PRIEZVISKO']}?",
                                          start_date, end_date, path[-1]['ID'])
                        # self.log.add_record(path)

                    else:
                        self.log.add_record("Pred pokračovaním správne nastavte začiatok aj koniec intervalu")


            elif key.lower() == 'q':
                self.quit()


a = ConsoleApp()
