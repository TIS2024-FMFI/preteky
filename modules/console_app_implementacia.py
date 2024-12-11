import os
import time
import tty
import termios
import sys
#import msvcrt  # Windows-only library for capturing keypresses
from datetime import datetime




            
        ####vrati bud zoznam ak to ma zobrazit alebo vrati none ak je finalny
         #komunikacia s ostanymi 

class Cache:
    def __init__(self):
        self.data = {"isOrienteering": {}, "sandberg": {}, "save_path": ""}

    def add_races_orienteering(self, races, date):
        self.data["isOrienteering"][date] = races

    def get_races_orienteering(self, date):
        return self.data["isOrienteering"].get(date)

    def add_races_sandberg(self, races):
        self.data["sandberg"] = races

    def get_races_sandberg(self):
        return self.data.get("sandberg")
    
    def import_path(self):   ### stiahne z databazy nejakej / konfiguracneho suboru
        self.data["save_path"] = "C:\\Nie\\kde\\v\\pici"

    def save_path(self):     ### nastavi novu path v ulozisku
        pass

    def get_path(self):
        if self.data["save_path"] == "":
            self.import_path()
        return self.data["save_path"]

    def set_path(self, path):
        ### nastavit novu path na miesto kde je stara ulozena
        self.save_path()
        self.data["save_path"] = path


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
        self.log = Log()
        self.cache = Cache()
        self.window_general(["Import preteku", "Prihlásenie pretekarov", "Export do súboru", "Štatistiky pretekara"], "MENU", "MENU")

    def run_interface(self, interface_name, *param):
        if interface_name == "races_from_orienteering":
            #mena pretekov na dany mesiac
            cache_contains = self.cache.get_races_orienteering(param[0])
            if not cache_contains:
                races = [
                        {"DÁTUM": f"2023-a-0{i+1}", "NÁZOV": f"Race {i + 1}", "DEADLINE": f"2023-b-1{i+1}",
                        "MIESTO": f"Location {i + 1}", "KATEGÓRIA": f"Category {i % 3 + 1}"}
                        for i in range(5)
                    ]
                self.cache.add_races_orienteering(races, param[0])
            else:
                races = cache_contains
            return races

        elif interface_name == "races_from_sandberg":
            cache_contains = self.cache.get_races_sandberg()
            if not cache_contains:
                races = [
                        {"DÁTUM": f"2023-a-0{i+1}", "NÁZOV": f"Race {i + 1}", "DEADLINE": f"2023-b-1{i+1}",
                        "MIESTO": f"Location {i + 1}", "KATEGÓRIA": f"Category {i % 3 + 1}"}
                        for i in range(5)
                    ]
                self.cache.add_races_sandberg(races)
            else:
                races = cache_contains
            return races

        

        elif interface_name == "html":
            return "Dojebalo sa to"

        elif interface_name == "csv":
            return "Dojebalo sa to"

        elif interface_name == "txt":
            return "Dojebalo sa to"
            ### import pretekov
        elif interface_name == "racers":
            if param[0] == "Bez filtra":
                return [{'MENO': f"meno{i}", 'DÁTUM NARODENIA': f"1-1-200{i}",'KLUB': "abcdef"} for i in range(5)]
            if param[0] == "Meno":
                return [{'MENO': f"meno{i}", 'DÁTUM NARODENIA': f"1-1-200{i}",'KLUB': "abcdef"} for i in range(5)]
            if param[0] == "ID":
                return [{'MENO': f"meno{i}", 'DÁTUM NARODENIA': f"1-1-200{i}",'KLUB': "abcdef"} for i in range(5)]
        elif interface_name == "import_stat":
            return "SUCCESS"


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
            print("(press 'q' to quit, UP and DOWN to navigate, ENTER to select option, 'b' for back, 's' to sort items)")
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
            if key == '\033': # Arrow keys
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0: # Up
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(main_options) - 1: # Down
                    current_idx += 1
            elif key == '\r':  # Enter
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
            races = sorted(races, key=lambda x: x[sort_key])
            races_display = [f"{p['DÁTUM']} | {p['NÁZOV']} | {p['DEADLINE']} | {p['MIESTO']} | {p['KATEGÓRIA']}" for p in races]
            
            self.display_menu(races_display, current_idx, f"ZVOĽTE PRETEK (zoradené podľa {sort_key})")
            key = self.get_key()
            if key == '\033': # Arrow keys
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0: # Up
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(races) - 1: # Down
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':  # Enter
                if path[1] == "Prihlásenie pretekárov":
                    result = self.run_interface(aaa)
                elif path[1] == "Export do súboru":
                    self.log.add_record(f"Zvolený pretek {races[current_idx]}")
                    self.window_general(["html", "csv", "txt"], "ZVOĽTE FORMÁT", *path, races[current_idx])
                    
            elif key.lower() == 'q':  # Quit
                self.quit()

            elif key == 's':
                sort_keys = ["DÁTUM", "NÁZOV", "DEADLINE", "MIESTO", "KATEGÓRIA"]
                sort_key = sort_keys[(sort_keys.index(sort_key) + 1) % len(sort_keys)]
        
       
    
    def months_menu(self, *path):
        # Get the current month and year
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        year_offset = 0  # To keep track of the year offset for navigation
        current_idx = 0
        
        while True:
            # Create a list of months for the current year plus the offset
            months = []
            for i in range(12):  # Loop through 12 months
                month_index = (current_month - 1 + i) % 12  # Calculate month index
                year = current_year + year_offset + (current_month - 1 + i) // 12  # Increment year if needed
                month_name = datetime(1900, month_index + 1, 1).strftime("%B")
                months.append(f"{month_name}, {year}")

            # Add navigation options
            if year_offset > 0:
                months.insert(0, "Previous")  # Add previous option at the top
            months.append("Next")

            self.display_menu(months, current_idx, "ZVOĽTE MESIAC")
            key = self.get_key()
            if key == '\033': # Arrow keys
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0: # Up
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(months) - 1: # Down
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':  # Enter
                if months[current_idx] == "Previous":
                    year_offset -= 1  # Go to the previous year
                    current_idx = 0  # Reset selection to the top
                elif months[current_idx] == "Next":
                    year_offset += 1  # Go to the next year
                    current_idx = 0  # Reset selection to the top
                else:
                    m,y = months[current_idx].split(', ')
                    self.log.add_record(f"Zvolený mesiac {months[current_idx]}")
                    self.race_window(*path, months[current_idx])
    ##                print(f"Selected {months[current_idx]} from {called_from}")
##                    self.log.add_record( f"Selected {months[current_idx]} from {called_from}")
##                    time.sleep(1)  # Simulate action
##                    if "Import preteku" == called_from:
##                        zoznam_pretekov_isOr(called_from, months[current_idx])
            elif key.lower() == 'q':  # Quit
                self.quit()


    def path_window(self, *path):
        default_path = self.cache.get_path()
        options = ["Pokračovať", "Zmeniť predvolenú path"]
        current_idx = 0
        
        while True:
            self.display_menu(options, current_idx, f"Prevolená path je: {default_path}. Chcete pokračovať?")
            key = self.get_key()
            if key == '\033': # Arrow keys
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0: # Up
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(options) - 1: # Down
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':  # Enter
                if options[current_idx] == "Zmeniť predvolenú path":
                    # Allow user to enter a new path
                    self.clear_screen()
                    print("Zadajte novú path: ")
                    new_path = input().strip()
                    if os.path.isdir(new_path):  # Check if the path is valid
                        default_path = new_path
                        self.log.add_record("Path zmenená úspešne")
                        self.cache.set_path(new_path)
                    else:
                        self.log.add_record("Zvolená path nie je valídna")

                        
                else:
                    if path[-1] in ["html", "csv", "txt"]:
                        result = self.run_interface(path[-1])
                    else:
                        self.time_interval(*path)

            elif key.lower() == 'q':  # Quit
                self.quit()


    def window_general(self, options, title, *path):
        current_idx = 0
        ### ziskat title, options, a ostatne z path
        while True:
            self.display_menu(options, current_idx, title)
            key = self.get_key()
            if key == '\033': # Arrow keys
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0: # Up
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(options) - 1: # Down
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':  # Enter
                if len(path) == 1:
                    self.log.add_record(f"Zvolená funkcia {options[current_idx]}")
                    if options[current_idx] == "Import preteku":
                        self.months_menu(*path, "Import preteku")
                    elif options[current_idx] == "Štatistiky pretekara":
                        self.window_general(["Meno", "ID", "Bez filtra"], "Chcete zvoliť filtre?", *path, options[current_idx])
                    else:
                        self.race_window(*path, options[current_idx])

                elif options[current_idx] in ["html", "csv", "txt"]:
                    self.path_window(*path, options[current_idx])

                elif path[-1] == "Štatistiky pretekara":
                    if options[current_idx] == "Bez filtra":
                        self.racers(*path, "Bez filtra", None)
                    else:
                        self.racers(*path, options[current_idx], self.input_window(options[current_idx]))

            elif key.lower() == 'q':  # Quit
                self.quit()

    def input_window(self, title):
        self.clear_screen()
        print(f"Zadajte {title.lower()}: ")
        return input().strip()

    def racers(self, *path):
        current_idx = 0
        sort_key = "MENO"
        racers = self.run_interface("racers", path[-2], path[-1])
        while True:
            racers = sorted(racers, key=lambda x: x[sort_key])
            racers_display = [f"{p['MENO']} | {p['DÁTUM NARODENIA']} | {p['KLUB']}" for p in racers]
            
            self.display_menu(racers_display, current_idx, f"ZVOĽTE PRETEKÁRA (zoradené podľa {sort_key})")
            key = self.get_key()
            if key == '\033': # Arrow keys
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0: # Up
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(racers) - 1: # Down
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':  # Enter
                self.log.add_record(f"Zvolený pretekár {racers[current_idx]}")
                self.path_window(*path, racers[current_idx])
                

            elif key.lower() == 'q':  # Quit
                self.quit()

            elif key == 's':
                sort_keys = ["MENO", "DÁTUM NARODENIA", "KLUB"]
                sort_key = sort_keys[(sort_keys.index(sort_key) + 1) % len(sort_keys)]
        

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
            
            # Display options and handle navigation
            for i, option in enumerate(options):
                if i == current_idx:
                    print(f"> {option}")
                else:
                    print(f"  {option}")
            self.log.display()

            key = self.get_key()
            if key == '\033': # Arrow keys
                next1, next2 = self.get_key(), self.get_key()
                if next2 == 'A' and current_idx > 0: # Up
                    current_idx -= 1
                elif next2 == 'B' and current_idx < len(options) - 1: # Down
                    current_idx += 1
            elif key == 'b':
                break
            elif key == '\r':  # Enter
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
                        self.run_interface("import_stat")
                    else:
                        self.log.add_record("Pred pokračovaním správne nastavte začiatok aj koniec intervalu")
                        
            
            elif key.lower() == 'q':  # Quit
                self.quit()











a = ConsoleApp()
