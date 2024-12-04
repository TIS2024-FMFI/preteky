### Scenár 1: Import pretekov do lokálnej SQLite databázy

1. Používateľ vykoná kroky z README.md na inštaláciu a konfiguráciu aplikácie.
2. Používateľ spustí aplikáciu a vyberie možnosť `Import pretekov`.
3. Používateľ si zvolí mesiac, na základe ktorého sa mu zobrazia všetky preteky v danom mesiaci.
    - **Vedľajšia možnosť:** Ak sa v zvolenom mesiaci nekonajú žiadne preteky, aplikácia zobrazí správu: "V zvolenom mesiaci sa nekonajú žiadne preteky."
4. Používateľ si vyberie jedny preteky zo zoznamu a dá pokyn na ich import.
    - Aplikácia stiahne údaje o vybraných pretekoch a vloží ich do lokálnej SQLite databázy.
        - **Úspešná správa:** "Preteky boli úspešne importované do databázy."
        - **Vedľajšia možnosť:** Ak sa preteky už v databáze nachádzajú, aplikácia upozorní používateľa správou: "Tieto preteky už existujú v databáze."

**Požiadavky pokryté:**
- **3.1 Import pretekov do lokálnej SQLite databázy**

### Scenár 2: Prihlásenie bežcov na preteky

1. Používateľ vykoná kroky z README.md na inštaláciu a konfiguráciu aplikácie.
2. Používateľ spustí aplikáciu a vyberie možnosť `Prihlásenie pretekárov`.
    - Aplikácia zobrazí preteky pridané do lokálnej databázy, ktorým ešte neuplynul deadline na prihlasovanie.
        - **Vedľajšia možnosť:** Ak neexistujú žiadne preteky s neuplynutým deadline, aplikácia zobrazí správu: "Nenašli sa žiadne preteky s neuplynutým deadline."
4. Používateľ si vyberie preteky a aplikácia prihlási všetkých bežcov, ktorí sa prihlásili cez web stránku Sandbergu.
    - **Úspešná správa:** "Všetci bežci boli úspešne prihlásení na vybrané preteky."
    - **Vedľajšia možnosť:** Ak sa žiadni bežci neprihlásili, aplikácia zobrazí správu: "Nenašli sa žiadni prihlásení bežci."
5. Alternatívne sa bežci vyexportujú do CSV súboru.
    - **Úspešná správa:** "Bežci boli úspešne exportovaní do CSV súboru."

**Požiadavky pokryté:**
- **3.2 Prihlásenie bežcov na preteky**

### Scenár 3: Vloženie prihlásených bežcov do súboru

1. Používateľ vykoná kroky z README.md na inštaláciu a konfiguráciu aplikácie.
2. Používateľ spustí aplikáciu a vyberie možnosť `Export do súboru`.
3. Používateľ si vyberie preteky z lokálnej databázy.
    - **Vedľajšia možnosť:** Ak neexistujú žiadne preteky v databáze, aplikácia zobrazí správu: "Nenašli sa žiadne preteky v databáze."
4. Používateľ vygeneruje súbor vo formáte .txt alebo .csv z prihlásených bežcov.
    - **Úspešná správa:** "Súbor bol úspešne vygenerovaný."
    - **Vedľajšia možnosť:** Ak sú bežci už pridaní v súbore, aplikácia zobrazí správu: "Bežec už existuje v súbore."
5. Súbor sa uloží na zvolenej ceste.
    - **Úspešná správa:** "Súbor bol úspešne uložený na zvolenú cestu."

**Požiadavky pokryté:**
- **3.3 Vloženie prihlásených bežcov do súboru**

### Scenár 4: Zobrazenie štatistík bežcov

1. Používateľ vykoná kroky z README.md na inštaláciu a konfiguráciu aplikácie.
2. Používateľ spustí aplikáciu a vyberie možnosť `Štatistiky pretekára`.
3. Používateľ vyhľadá bežca podľa mena alebo ID.
    - **Vedľajšia možnosť:** Ak sa bežec nenájde, aplikácia zobrazí správu: "Bežec sa nenašiel."
4. Používateľ si vyberie údaje, ktoré chce zobraziť za zadaný časový interval.
5. Štatistiky sa zobrazia a môžu sa exportovať vo formáte .html, .json, alebo .csv.
    - **Úspešná správa:** "Štatistiky boli úspešne exportované."
6. Štatistika umiestnení sa dá zobraziť v grafe.
    - **Úspešná správa:** "Graf štatistík bol úspešne vygenerovaný."
    - **Vedľajšia možnosť** Používateľ si vie graf exportovať do pdf súboru

**Požiadavky pokryté:**
- **3.4 Používateľ môže zobraziť štatistiky bežcov**

### Scenár 5: Export pretekov ako udalosti pre Google Calendar

#### Prípad 5.1: Úspešné vytvorenie udalostí pre Google Calendar
1. Admin naimportuje preteky cez aplikáciu.
2. Aplikácia automaticky vytvorí dve udalosti v Google Kalendári:
   - **Prvá udalosť**: dátum pretekov (celodenná udalosť, červená farba).
   - **Druhá udalosť**: deadline prihlasovania na preteky (celodenná udalosť, červená farba).
3. Google Calendar API vráti úspešnú odpoveď obsahujúcu ID oboch udalostí.
4. Aplikácia zobrazí správu: „Udalosti boli úspešne pridané do Google Kalendára.“

#### Vedľajšie možnosti:
- Ak Google Calendar API nie je dostupné, zobrazí sa správa: „Synchronizácia s Google Kalendárom zlyhala. Skontrolujte pripojenie a skúste znova.“

---

#### Prípad 5.3: Zrušenie udalostí z Google Calendar
1. Admin odstráni preteky z aplikácie alebo zruší ich prihlásenie.
2. Aplikácia odošle požiadavku na odstránenie oboch udalostí v Google Kalendári pomocou uloženého ID udalostí.
3. API vráti úspešnú odpoveď potvrdzujúcu odstránenie udalostí.
4. Aplikácia zobrazí správu: „Udalosti boli úspešne zrušené v Google Kalendári.“

#### Vedľajšie možnosti:
- Ak API zlyhá, zobrazí sa správa: „Nepodarilo sa zrušiť udalosti. Skontrolujte pripojenie alebo údaje.“
