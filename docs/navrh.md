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
Táto podkapitola predstavuje návrh komunikácie medzi konzolovou aplikáciou a lokálnou databázou Sandberg.Keďže naša aplikácia bude bežať na rovnakom serveri ako lokálna databáza Sandberg, ale bude implementovaná v inom jazyku (naša bude bežať v pythone a aplikácia Sandberg v php), je potrebný prepis a sú rôzne prístupy:

# 1. Použitie RESTful API
RESTful API umožňuje aplikáciám komunikovať cez HTTP protokol. Aplikácia Sandberg môže poskytovať API endpointy, ktoré naša aplikácia volá na získanie alebo odoslanie údajov.
- Implementácia v Sandberg aplikácii: Vytvoria sa endpointy pre každú funkciu, ktorú chceme použiť. Tieto endpointy budú spracovávať HTTP požiadavky a vracať odpovede vo formáte JSON.
- Implementácia v našej aplikácii: Aplikácia používa knižnice ako requests na volanie API endpointov a spracovanie odpovedí.

# 2. Použitie súborov
Sandberg aplikácia a naša aplikácia môžu komunikovať prostredníctvom súborov. Sandberg aplikácia môže zapisovať údaje do súborov, ktoré potom naša číta a naopak.
- Implementácia v Sandberg aplikácii: Vytvoríme nové php skripty, ako komunikačné mosty. PHP skript zapisuje údaje do textového súboru alebo prijíma súbor na import.
- Implementácia v našej aplikácii: Python skript číta údaje zo súboru a spracováva ich alebo zapisuje údaje do textového súboru.
  
# 3. Použitie databázy
Obidve aplikácie môžu pristupovať k rovnakej databáze, čo umožňuje zdieľanie údajov. Databáza slúži ako spoločný úložný priestor, kde môžu obe aplikácie ukladať a načítavať údaje.
- Implementácia v Sandberg aplikácii: Sandberg aplikácia vytvára databázu a tabuľky, zapisuje a číta údaje o bežcoch a pretekoch.
- Implementácia v našej aplikácii:  Naša aplikácia zapisuje a číta údaje o bežcoch a pretekoch z tej istej databázy.

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
