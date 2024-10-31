import os
import time
import msvcrt  # Windows-only library for capturing keypresses
from datetime import datetime


###### vytvorit log vykonanych akcii,  moze skratit cas pri zistovani ci pretek uz nebol pridany v nedalekej minulosti
log = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(options, current_idx, title, logging=True):
    clear_screen()
    print(f"--- {title} ---")
    if "Choose Pretek" in title:
        print("(press 'q' to quit, UP and DOWN to navigate, ENTER to select option, 's' to sort items)")
    else:
        print("(press 'q' to quit, UP and DOWN to navigate, ENTER to select option)")
    for i, option in enumerate(options):
        if i == current_idx:
            print(f"> {option}")
        else:
            print(f"  {option}")
    if logging:
        print("_"*40)
        for i in min(log,log[:5]):
            print(i)

def months_menu(called_from):
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
        months.append("Next")  # Add next option at the bottom
        months.append("Back")  # Add back option

        display_menu(months, current_idx, "Choose month")
        key = msvcrt.getch()
        
        if key == b'H' and current_idx > 0:  # Up
            current_idx -= 1
        elif key == b'P' and current_idx < len(months) - 1:  # Down
            current_idx += 1
        elif key == b'\r':  # Enter
            if months[current_idx] == "Back":
                break
            elif months[current_idx] == "Previous":
                year_offset -= 1  # Go to the previous year
                current_idx = 0  # Reset selection to the top
            elif months[current_idx] == "Next":
                year_offset += 1  # Go to the next year
                current_idx = 0  # Reset selection to the top
            else:
##                print(f"Selected {months[current_idx]} from {called_from}")
                log.insert(0, f"Selected {months[current_idx]} from {called_from}")
                time.sleep(1)  # Simulate action
                if "Import preteku" == called_from:
                    zoznam_pretekov_isOr(called_from, months[current_idx])
        elif key.lower() == b'q':  # Quit
            quit()

def quit():
    main_options = ["Nie", "Ano"]
    current_idx = 0

    while True:
        display_menu(main_options, current_idx, "Chcete naozaj odist")
        key = msvcrt.getch()
        if key == b'H' and current_idx > 0:  # Up
            current_idx -= 1
        elif key == b'P' and current_idx < len(main_options) - 1:  # Down
            current_idx += 1
        elif key == b'\r':  # Enter
            if main_options[current_idx] == "Ano":
                print("Exiting the program.")
                exit()
            elif main_options[current_idx] == "Nie":
                break

def zoznam_pretekov_isOr_API(month):
    '''
        Implementovat,
        input:     mesiac, rok
        output:    datum, nazov preteku, deadline prihlasenia, miesto, kategorie 

    '''
    return [
        {"datum": f"2023-{month}-0{i+1}", "nazov": f"Race {i + 1}", "deadline": f"2023-{month}-1{i+1}",
         "miesto": f"Location {i + 1}", "kategorie": f"Category {i % 3 + 1}"}
        for i in range(5)
    ]
def preteky_z_SQLite():
    '''
        Implementovat,
        input:     None
        output:    udaje o preteku (datum, nazov preteku, deadline prihlasenia, miesto, kategorie)
        
    '''
    return [
        {"datum": f"2023-{i**i%12+1}-0{i+1}", "nazov": f"Race {i + 1}", "deadline": f"2023-{i*i%12+1}-1{i+1}",
         "miesto": f"Location {i + 1}", "kategorie": f"Category {i % 3 + 1}"}
        for i in range(5)
    ]

def prihlas_do_isOr(pretek_param):
    '''
        Implementovat,
        input: potrebne parametre preteku
        output: success, error + API response
    '''
    return "success"
    
def import_preteku_isOr_API_do_databazy(pretek):
    '''
        Implementovat,
        input: nejake unikatne id preteku
        output: success, error, uz bol v klubovej databaze
    '''
    return "success"
def convert_html(pretek):
    '''
        Implementovat,
        input: nejake unikatne id preteku
        output: success, error, uz bol v klubovej databaze
    '''
    return "success"
def convert_csv(pretek):
def convert_txt(pretek):

def zoznam_formatov(pretek):
    current_idx = 0
    while True:
        # Create a list of months for the current year plus the offset
        
        display_menu(["csv", "txt", "html"], current_idx, "Choose format")
        key = msvcrt.getch()
        
        if key == b'H' and current_idx > 0:  # Up
            current_idx -= 1
        elif key == b'P' and current_idx < 2:  # Down
            current_idx += 1
        elif key == b'\r':  # Enter
            if ["csv", "txt", "html"][current_idx] == "Back":
                break
            elif ["csv", "txt", "html"][current_idx] == "html":
                convert_html(pretek)
            elif ["csv", "txt", "html"][current_idx] == "csv":
                convert_csv(pretek)
            elif ["csv", "txt", "html"][current_idx] == "txt":
                convert_txt(pretek)            
            else:
                log.insert(0, f"Selected {months[current_idx]} from {called_from}")
                time.sleep(1)  # Simulate action
                if "Import preteku" == called_from:
                    zoznam_pretekov_isOr(called_from, months[current_idx])
        elif key.lower() == b'q':  # Quit
            quit()

def zoznam_pretekov_isOr(called_from, mesiac=None):
    year_offset = 0
    current_idx = 0
    sort_key = "datum"  # Default sort by date
    
    while True:
        # Fetch and sort the list of races
        if mesiac:
            preteky = zoznam_pretekov_isOr_API(mesiac)
        else:
            preteky = preteky_z_SQLite()
        preteky = sorted(preteky, key=lambda x: x[sort_key])  # Sort by the selected attribute
        preteky_display = [f"{p['datum']} | {p['nazov']} | {p['deadline']} | {p['miesto']} | {p['kategorie']}" for p in preteky]
        
        preteky_display.append("Back")  # Add back option

        # Display the menu and handle navigation
        display_menu(preteky_display, current_idx, f"Choose Pretek (sorted by {sort_key})")
        key = msvcrt.getch()
        
        if key == b'H' and current_idx > 0:  # Up
            current_idx -= 1
        elif key == b'P' and current_idx < len(preteky_display) - 1:  # Down
            current_idx += 1
        
        elif key == b'\r':  # Enter
            if preteky_display[current_idx] == "Back":
                break
            elif called_from == "Import preteku":                
                log.insert(0, f"Selected {preteky_display[current_idx]} from {called_from}")
                log.insert(0, f"Response from isOrienteering -> SQLite was {import_preteku_isOr_API_do_databazy(preteky_display[current_idx])}")
                time.sleep(1)  # Simulate action or processing
            elif called_from == "Prihlasenie pretekarov":
                log.insert(0, f"Prihlasenie pretekarov bol {prihlas_do_isOr(preteky_display[current_idx])}")
            elif called_from == "Export do suboru":
                log.insert(0, f"Zvoleny {preteky_display[current_idx]}")
                zoznam_formatov(preteky_display[current_idx])
                
        elif key.lower() == b'q':  # Quit
            quit()
        elif key == b's':  # Sort key toggle
            # Cycle through available sorting keys
            sort_keys = ["datum", "nazov", "deadline", "miesto", "kategorie"]
            sort_key = sort_keys[(sort_keys.index(sort_key) + 1) % len(sort_keys)]

def main_menu():
    main_options = ["Import preteku", "Prihlasenie pretekarov", "Export do suboru", "Statistiky pretekara"]
    current_idx = 0

    while True:
        display_menu(main_options, current_idx, "Menu")
        key = msvcrt.getch()

        if key == b'H' and current_idx > 0:  # Up
            current_idx -= 1
        elif key == b'P' and current_idx < len(main_options) - 1:  # Down
            current_idx += 1
        elif key == b'\r':  # Enter
            log.insert(0, f"Zvolene {main_options[current_idx]}")
            if main_options[current_idx] == "Import preteku":
                months_menu("Import preteku")
            elif main_options[current_idx] == "Prihlasenie pretekarov":
                zoznam_pretekov_isOr("Prihlasenie pretekarov")
            elif main_options[current_idx] == "Export do suboru":
                zoznam_pretekov_isOr("Export do suboru")
            elif main_options[current_idx] == "Statistiky pretekara":
                option_2()
        elif key.lower() == b'q':  # Quit
            quit()

# Run the application
main_menu()



