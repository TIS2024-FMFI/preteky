# Návod na nastavenie Google Cloud API pre Google Calendar

Tento návod vás prevedie nastavením Google Cloud API pre triedu `GoogleCalendarService`.

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

## 3. Vytvorenie prihlasovacích údajov (Credentials)
1. **Prejdite na "APIs & Services" > "Credentials".**
2. Kliknite na "Create Credentials" > "OAuth 2.0 Client ID".
3. **Ak ste to ešte neurobili, nastavte "OAuth Consent Screen":**
   - Kliknite na "Configure Consent Screen".
   - Vyberte "External" a kliknite na "Create".
   - Vyplňte základné informácie (napr. názov aplikácie) a kliknite na "Save and Continue".
4. **Vytvorte OAuth 2.0 Client ID:**
   - Vyberte "Application type" > "Desktop app".
   - Zadajte názov (napr. "Desktop App") a kliknite na "Create".
   - Kliknite na "Download JSON" a uložte tento súbor ako `credentials.json` do koreňového adresára projektu.

---

## 4. Nastavenie OAuth tokenu
Keď používateľ prvýkrát spustí aplikáciu, vytvorí sa token `token.json`.

1. Uistite sa, že súbor `credentials.json` je v rovnakom priečinku ako váš kód.
2. Pri prvom spustení aplikácie vás Google požiada o povolenie. Pridajte adresy URL do zoznamu dôveryhodných (ak je to potrebné).
3. Po úspešnom prihlásení sa vytvorí súbor `token.json`, ktorý ukladá informácie o prihlásení.

---

## 5. Testovanie Google Calendar API
Po nastavení všetkých krokov otestujte základné funkcie. Tu je jednoduchý testovací kód:

```python
if __name__ == '__main__':
    calendar_service = GoogleCalendarService()
    calendar_service.list_events()
