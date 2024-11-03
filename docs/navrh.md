# Návrh
## 1 Úvod
## 1.1 Účel návrhu
Tento dokument slúži ako detailný návrh informačného systému pre projekt “Aplikácia pre import a export údajov z databázy termínov pretekov”. Systém je vyvíjaný pre Športový klub Sandberg a je súčasťou predmetu Tvorba informačných systémov na FMFI UK v akademickom roku 2024/2025. Dokument obsahuje všetky potrebné informácie týkajúce sa implementácie, fungovania a dizajnu systému. Je určený predovšetkým pre vývojárov, ktorí budú systém realizovať, a zahŕňa všetky požiadavky uvedené v katalógu požiadaviek.

## 1.2 Rozsah využitia systém
Tento dokument je úzko prepojený s katalógom požiadaviek a špecifikuje všetky požiadavky, ktoré sú v ňom uvedené. Okrem toho definuje vonkajšie rozhrania, formáty súborov a potrebné API pre správnu funkčnosť systému. Dokument tiež obsahuje návrh používateľského rozhrania konzolovej aplikácie vrátane vizualizácií a diagramov, ktoré detailne popisujú implementáciu systému.

## 1.3 Referencie
- Github repozitár projektu zameraného na tvorbu systému Športového klubu Sandberg z roku 2017: 
    [https://github.com/TIS2017/SportovyKlub](https://github.com/TIS2017/SportovyKlub)
- Github repozitár projektu z roku 2023, ktorí menili časť databázy:
    [https://github.com/TIS2023-FMFI/sportovy-pretek-web]({https://github.com/TIS2023-FMFI/sportovy-pretek-web)
## 2 Špecifikácia vonkajších interfacov
## 2.1 
## 2.2
## 2.3 Návrh komunikácie medzi konzolovou aplikáciou a lokálnou databázou Sandberg
Táto podkapitola predstavuje návrh komunikácie medzi konzolovou aplikáciou a lokálnou databázou Sandberg. Popisuje tri hlavné operácie: pripojenie k databáze, import vybraných pretekov a export prihlásených bežcov do CSV.
### 1. Pripojenie k databáze Sandberg
Pripojenie na databázu sa vykonáva pomocou SQLAlchemy na vytváranie SQL dotazov, ktoré sú potom odosielané ako HTTP POST požiadavky na URL servera Sandberg.
### 2. Import vybraných pretekov do SQLite databázy Sandberg
Pre každý vybraný pretek sa vykonajú nasledujúce kroky:
- Vytvorí sa jedinečné `id` kombináciou `id pretekov` a `id eventu`, aby sa predišlo kolíziam alebo duplicite.
- Vkontroluje sa, či už takéto `id` existuje:
    - Ak áno, vypíše sa správa, že preteky už existujú a nepridajú sa do databázy.
    - Ak nie, tak pomocou príkazu `insert` z SQLAlchemy sa vytvorí záznam s následujúcimi parametrami:
        - `id` (integer) -> id pretekov
        - `nazov` (string) -> názov udalosti, title_sk
        - `datum` (string, formát Y-m-d H:i:s) -> dátum udalosti
        - `deadline` (string, formát Y-m-d H:i:s) -> deadline udalosti
        - `aktiv` (integer) -> 1 znamená, že sa da prihlásiť na preteky a 0 znamená opak
        - `poznamka` (text)
        
- Pridanie kategórie pretekov:
    - Každý pretek má detaily obsahujúce categories, ktoré majú číselník. Na základe id kategórie sa nájde jej názov a ošetrí sa na alfa-numerický výraz.
    - Pri hľadaní zhody v kategóriách v lokálnej databáze, ktoré sú tiež ošetrené na alfa-numerický výraz, môžu nastať dve situácie:
        - Zhodu nájdeme: priradí sa kategória pretekom a vloží sa záznam obsahujúci:
            - `id` (integer)
            - `id_pret` (integer) ->id pretekov
            - `id_kat` (integer) -> id kategórie, ktorá má zhodu názvu s našou kategóriou pretekov
    
        - Zhodu nenájdeme: vytvorí sa nová kategória s novým jedinečným id, pridá sa do tabuľky `Kategórie` záznam obsahujúci:
            - `id_kat` (integer) -> id kategórie
            - `nazov` (text)
        Potom postup je rovnaký ako pri nájdení zhody.
-Všetky SQL výrazy sa pošlú ako POST požiadavka na URL servera vo formáte JSON, pričom sa dotaz skompiluje do SQL reťazca pomocou SQLite dialektu. Odpoveď určí úspešnosť operácie.

### 3. Export prihlásených bežcov do CSV
Pri exporte prihlásených bežcov sa použije `id pretekov`,  ktorého si na vyselectovanie všetkých bežcov v tabuľke `Prihlaseni`, ktorí majú rovnaké `id pretekov`. Zároveň sa vyžiadajú údaje o používateľovi z tabuľky `Pouzivatelia` a o kategórií z tabuľky `Kategorie`.
Exportované parametre sú:
- `meno` (string) -> meno používateľa
- `priezvisko` (string) -> priezvisko používateľa
- `os_i_c` (string)
- `cip` (string)
- `nazov` -> kategória, do ktorej je zaradený
- `poznamka` (string)

Tieto údaje sa pošlú ako POST požiadavka na URL servera vo formáte JSON, pričom sa dotaz skompiluje do SQL reťazca pomocou SQLite dialektu. Odpoveď určí úspešnosť operácie a následne sa údaje exportujú do CSV súboru.

  
## 3 Návrh dátového modelu
Dátový model je reprezentovaný entitno-relačným diagramom, ktorý ilustruje vzťahy medzi jednotlivými entitami. Entita predstavuje objekt, ktorý existuje samostatne a nezávisle od iných objektov. Vzťahy medzi entitami opisujú prepojenia a interakcie medzi týmito objektmi
Dátovy model je prevzatý z existujúcej aplikácie.

![datovy_model](https://github.com/user-attachments/assets/fa6856e0-0aec-4070-9817-27235892dd93)


## 4 Analýza použitých technológií
- PHP 5.6, SQLite - prevzaté z pôvodnej aplikácie
## 5 Návrh konzolového rozhrania
## 6 Návrh zobrazenia štatistík
## 7 Diagramy
## 8 Harmonogram implementácie
