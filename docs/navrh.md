# Návrh
## 1 Úvod
## 1.1 Účel návrhu
Tento dokument slúži ako detailný návrh informačného systému pre projekt “Aplikácia pre import a export údajov z databázy termínov pretekov”. Systém je vyvíjaný pre Športový klub Sandberg a je súčasťou predmetu Tvorba informačných systémov na FMFI UK v akademickom roku 2024/2025. Dokument obsahuje všetky potrebné informácie týkajúce sa implementácie, fungovania a dizajnu systému. Je určený predovšetkým pre vývojárov, ktorí budú systém realizovať a zahŕňa všetky požiadavky uvedené v katalógu požiadaviek.

## 1.2 Rozsah využitia systém
Tento dokument je úzko prepojený s katalógom požiadaviek a špecifikuje všetky požiadavky, ktoré sú v ňom uvedené. Okrem toho definuje vonkajšie rozhrania, formáty súborov a potrebné API pre správnu funkčnosť systému. Dokument tiež obsahuje návrh používateľského rozhrania konzolovej aplikácie vrátane vizualizácií a diagramov, ktoré detailne popisujú implementáciu systému.

## 1.3 Referencie
- Github repozitár projektu zameraného na tvorbu systému Športového klubu Sandberg z roku 2017: 
    [https://github.com/TIS2017/SportovyKlub](https://github.com/TIS2017/SportovyKlub)
- Github repozitár projektu z roku 2023, ktorí menili časť databázy:
    [https://github.com/TIS2023-FMFI/sportovy-pretek-web](https://github.com/TIS2023-FMFI/sportovy-pretek-web)
- [API roznhranie is.orientering.sk](https://github.com/TIS2024-FMFI/preteky/tree/main/API/is.orienteering.sk)
## 2 Špecifikácia vonkajších interfacov
## 2.1 Návrh komunikácie medzi konzolovou aplikáciou a stránkou is.orienteering.sk 
V tejto kapitole sa venujeme komunikácí so stránkou [is.orieteering.sk](is.orienteering.sk) pomoco restfull API. Všetku komunikáciu vieme rozdeliť na dva módy: Get a Post 

Mód Get
- používame keď sa snažíme získať dáta z is.orienteering.sk
- dáta ktoré získavame:
    - preteky v mesiaci, ktorý zadáme
    - kategórie pretekárov na daných pretekoch (hľadáme podľa ID pretekov)
    - všetky informácie o pretekárovi, ktorého sme si vybrali (na základe ID pretekára)
        - počítajú sa tu aj výsledky na pretekoch
    - informácie o registrácii jednotlivých pretekárov, ale aj celého klubu (na zaklade ID klubu/pretekára)
    - informácie o registrácii na dané preteky (podľa ID pretekov)
        - kto je na nich prihlásený
    - detailnejšie informácie o kategóriach na daných pretekoch (može sa daný pretekár prihlásiť s touto kategóriou?)

Mód Post
- používame keď vkladáme dáta na is.orienteering.sk
- dáta, ktoré vkladáme:
    - registrácia pretekára na dané preteky (podľa ID pretekov)
    - zrušenie registrácie pretekára na dané preteky (podľa ID pretekov)
 
----------- 
- na používanie API je potrebný bezpečnostný klúč
    - bude uložený v konfig súbore 
- na každý request z modu Get budeme mať samostatnú funkciu, ktorá vráti JSON string
- pri mode Post vkladáme JSON string ako parameter a vraciame boolovskú hodnotu, či sa vloženie podarilo
- pomocné triedy
    -  parser a creator JSON stringov
    -  úprava dátumov do správneho tvaru
    -  čítanie konfig súboru

## 2.2 Návrh komunikácie medzi konzolovou aplikáciou a lokálnou databázou Sandberg
Táto podkapitola predstavuje návrh komunikácie medzi konzolovou aplikáciou a lokálnou databázou Sandberg. Keďže naša aplikácia bude bežať na rovnakom serveri ako lokálna databáza Sandberg, ale bude implementovaná v inom jazyku (naša bude bežať v pythone a aplikácia Sandberg v php), je potrebný prepis a sú rôzne prístupy:

### 1. Použitie RESTful API
RESTful API umožňuje aplikáciám komunikovať cez HTTP protokol. Aplikácia Sandberg môže poskytovať API endpointy, ktoré naša aplikácia volá na získanie alebo odoslanie údajov.
- Implementácia v Sandberg aplikácii: Vytvoria sa endpointy pre každú funkciu, ktorú chceme použiť. Tieto endpointy budú spracovávať HTTP požiadavky a vracať odpovede vo formáte JSON.
- Implementácia v našej aplikácii: Aplikácia používa knižnice ako requests na volanie API endpointov a spracovanie odpovedí.

### 2. Použitie súborov
Sandberg aplikácia a naša aplikácia môžu komunikovať prostredníctvom súborov. Sandberg aplikácia môže zapisovať údaje do súborov, ktoré potom naša číta a naopak.
- Implementácia v Sandberg aplikácii: Vytvoríme nové php skripty, ako komunikačné mosty. PHP skript zapisuje údaje do textového súboru alebo prijíma súbor na import.
- Implementácia v našej aplikácii: Python skript číta údaje zo súboru a spracováva ich alebo zapisuje údaje do textového súboru.
  
Všetky funkcie, ktoré budeme potrebovať z PHP aplikácie, sú implementované v súbore https://github.com/TIS2017/SportovyKlub/blob/master/source/preteky.php.
1. Import pretekov do našej aplikácie
- Tabuľky, ktoré sa budú používať:
  	- Preteky
  	- Kategorie
  	- Kategorie_pre
- Funkcie:
	- pridaj_pretek($nazov, $datum, $deadline, $poznamka): Pridá nový pretek do databázy.
	- pridaj_kategoriu($nazov): Pridá novú kategóriu do databázy.
	- pridaj_kat_preteku($id_pret, $id_kat): Priradí kategóriu k preteku.
- Vstupný formát pre funkciu pridaj_pretek bude obsahovať nasledovné parametre:
 - NAZOV (String): Názov preteku.
 - DATUM (String): Dátum preteku vo formáte YYYY-MM-DD.
 - DEADLINE (String): Deadline pre registráciu vo formáte YYYY-MM-DD.
 - POZNAMKA (String): Poznámka k preteku, ktorá môže obsahovať aj URL odkazy.
   
2. Export prihlásených bežcov
- Tabuľky, ktoré sa budú používať:
	- Exporty
    - Prihlaseni
    - Pouzivatelia
    - Kategorie
- Funkcie:
	- exportuj($id_pret)
 - Výstupný súbor je vo formáte CSV. Podrobnosti o formáte a parametre výstupu:
	- Hlavičky vo výstupe: Hlavičky v CSV súbore sú mapované z poľa prepis a budú preložené do výrazov ako "MENO", "PRIEZVISKO", "OS.ČÍSLO", "ČIP", "KATEGÓRIA", a "POZNÁMKA".
	- Parametre:
		- meno (string): Meno prihláseného bežca 
   		- priezvisko (string): Priezvisko prihláseného bežca 
		- os_i_c (string): Osobné číslo prihláseného bežca 
  		- cip (string): Číslo čipu prihláseného bežca 
		- nazov (string): Kategória
		- poznamka (string): Poznámka
- Funkcia zapisuje tieto hodnoty do CSV súboru a pripraví ho na stiahnutie.

- ## 2.3 Návrh komunikácie medzi konzolovou aplikáciou a Google Kalendárom

V tejto časti popisujeme komunikáciu s Google Kalendárom, ktorá umožní automatické pridanie udalostí do kalendára admina pri prihlásení bežcov na preteky. Implementácia bude prebiehať prostredníctvom Google Calendar API, čo zabezpečí synchronizáciu medzi našou aplikáciou a kalendárom.

### Implementácia funkčnosti
1. **Autorizácia a autentifikácia:**
   - Na komunikáciu s Google Calendar API je potrebný OAuth 2.0 prístupový token. Pri prvej synchronizácii sa admin prihlási do svojho Google účtu a autorizuje aplikáciu na správu jeho kalendára. Token sa následne uloží v konfiguračnom súbore alebo zabezpečenej databáze, aby sa zamedzilo opakovanému prihlasovaniu.

2. **Automatické vytvorenie udalosti:**
   - Po registrácii bežcov na preteky aplikácia zavolá API endpoint na vytvorenie udalosti v kalendári. Parametre udalosti, ktoré sa odosielajú cez API, zahŕňajú:
     - **Názov udalosti:** Obsahuje názov pretekov.
     - **Dátum a čas:** Definované podľa rozpisu pretekov.
     - **Umiestnenie:** Miesto konania pretekov, ak je dostupné.
     - **Poznámka:** Ďalšie informácie alebo URL odkaz na detaily o pretekoch.

3. **Zrušenie alebo úprava udalosti:**
   - Pri zrušení registrácie bežca alebo pri zmene údajov pretekov aplikácia automaticky aktualizuje alebo odstráni príslušnú udalosť z Google Kalendára prostredníctvom PUT (update) alebo DELETE (delete) požiadavky na daný event ID.

4. **Formátovanie dátumu a času:**
   - Dátumy a časy budú formátované podľa štandardu ISO 8601, ktorý vyžaduje Google Calendar API.

5. **Výstup a potvrdenie:**
   - Po úspešnom pridelení udalosti v kalendári API vráti ID udalosti, ktoré sa uloží pre budúce operácie (napr. zrušenie alebo úprava). Funkcia vracia bool hodnotu úspešnosti.

---

Táto časť zabezpečí, že admin bude mať vždy aktuálne informácie o pretekoch vo svojom Google Kalendári, čo mu umožní lepšiu organizáciu a prehľad.

## 3 Návrh dátového modelu
Dátový model je reprezentovaný entitno-relačným diagramom, ktorý ilustruje vzťahy medzi jednotlivými entitami. Entita predstavuje objekt, ktorý existuje samostatne a nezávisle od iných objektov. Vzťahy medzi entitami opisujú prepojenia a interakcie medzi týmito objektmi
Dátovy model je prevzatý z existujúcej aplikácie.

![datovy_model](https://github.com/user-attachments/assets/fa6856e0-0aec-4070-9817-27235892dd93)


## 4 Analýza použitých technológií
- PHP 5.6, SQLite - prevzaté z pôvodnej aplikácie
## 5 Návrh konzolového rozhrania
Úvodné okno ktoré sa zobrazí
![Uvodne okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Vyber_akcie.png)
Po zvolení Import sa zobrazí výber mesiaca
![Mesiace okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Vyber_mesiaca.png)
Zoznam pretekov, vyobrazí sa po zvolení mesiaca v Importe, po zvolení prihlásenia na preteky a po zvolení exportu do súboru
![Preteky okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Vyber_preteku.png)

Voľba formátu na export
![Formaty okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Volba_formatu.png)
Path uloženia vyexportovaného súboru (pri exporte a štatistikách)
![Path okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Volba_path.png)
![Path input](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Input_window_path.png)

Vyhľadávanie pretekára v štatistike
![Filter okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Volba_filtru_vyhladanie_hraca.png)
![Pretekar okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Volba_pretekara.png)
Zadávanie parametrov štatistiky
![Interval okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Nastavenie_intervalu_merania_statistiky.png)
![Statistika okno](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/Volba_statistiky.png)
Po stlačení q, ukončuje konzolovú aplikáciu
![quit](https://github.com/TIS2024-FMFI/preteky/blob/main/docs/obrazky/quit.png)



## 6 Návrh zobrazenia štatistík
## 7 Diagramy
## 8 Harmonogram implementácie
