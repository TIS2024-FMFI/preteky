# Návod na nastavenie Google Cloud API pre Google Calendar s použitím Service Account

Tento návod vás prevedie nastavením Google Cloud API pre triedu `GoogleCalendarService` s použitím **Service Account** (bez OAuth prihlásenia).

---

## 1. Vytvorenie Google Cloud projektu
1. **Navštívte Google Cloud Console:**  
   [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. **Prihláste sa svojím Google účtom.**
3. **Vytvorte nový projekt:**
   - Kliknite na "Select a project" v hornej časti obrazovky.
   - Kliknite na "New Project".
   - Zadajte názov projektu (napr. "Google Calendar Integration") a kliknite na "Create".

---

## 2. Povolenie Google Calendar API
1. **V projekte kliknite na "APIs & Services" > "Library".**
2. **Vyhľadajte "Google Calendar API".**
3. Kliknite na výsledok a potom kliknite na "Enable".

---

## 3. Vytvorenie Service Account
1. **Prejdite na "IAM & Admin" > "Service Accounts".**
2. Kliknite na "Create Service Account".
3. **Vyplňte informácie o účte:**
   - Service account name: (napr. `calendar-service-account`)
   - Kliknite na "Create and Continue".
4. **Priraďte rolu:**
   - Vyberte rolu **Editor** alebo **Owner** (prípadne prispôsobte podľa potreby).
   - Kliknite na "Continue".
5. **Kliknite na "Done" pre dokončenie.**

---

## 4. Stiahnutie kľúča Service Account
1. Nájdite svoj Service Account na stránke **"IAM & Admin" > "Service Accounts"**.
2. Kliknite na tri bodky (⋮) vedľa svojho Service Account a vyberte "Manage Keys".
3. Kliknite na "Add Key" > "Create New Key".
4. Vyberte možnosť **JSON** a kliknite na "Create".
5. **Uložte vygenerovaný súbor** (napr. `service_account.json`) do koreňového adresára projektu.

---

## 5. Nastavenie prístupu k Google Kalendáru
1. **Navštívte Google Kalendár:** [Google Calendar](https://calendar.google.com).
2. Prejdite do **nastavení kalendára**, ku ktorému chcete získať prístup:
   - Kliknite na trojbodkovú ponuku vedľa názvu kalendára a vyberte **Nastavenia a zdieľanie**.
3. **Zdieľajte kalendár so Service Accountom:**
   - Do sekcie **"Zdieľanie s konkrétnymi ľuďmi alebo skupinami"** pridajte e-mail Service Accountu (napr. `calendar-service-account@your-project.iam.gserviceaccount.com`).
   - Nastavte oprávnenie na **"Vykonať zmeny a spravovať zdieľanie"**.

---

## 6. Testovanie Google Calendar API
Po nastavení všetkých krokov otestujte základné funkcie pomocou nasledovného kódu:

### Príklad testovacieho kódu
```python
if __name__ == '__main__':
    calendar_service = GoogleCalendarService()
    calendar_service.add_main_event(
        summary="Test Event",
        location="Bratislava",
        description="Toto je testovacia udalosť.",
        start_date="2025-01-20",
        end_date="2025-01-21",
        calendar_id="your-calendar-id@gmail.com"  # Nahraďte ID vášho kalendára
    )
