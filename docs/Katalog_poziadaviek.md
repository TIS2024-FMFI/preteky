## 1 Úvod
### 1.1 Účel katalógu požiadaviek
Tento dokument definuje požiadavky a funkcionalitu projektu "Aplikácia pre import a export údajov z databázy termínov pretekov". Vyvíjaný informačný systém bude slúžiť správcovi klubovej aplikácie Športového klubu Sandberg a taktiež bude výstupom projektu v rámci predmetu Tvorba informačných systémov na FMFI UK v akademickom roku 2024/2025. Dokument je určený pre riešiteľov projektu, zadávateľa a vyučujúceho predmetu Tvorba Informačných Systémov. Zároveň slúži ako záväzná dohoda medzi zadávateľom a riešiteľmi, ktorá určuje finálnu podobu požiadaviek na výsledný produkt, ktoré sa spísali a upravili na základe požiadaviek zadávateľa projektu.

### 1.2 Rozsah využitia systému
Vyvíjaný informačný systém bude slúžiť na synchronizáciu a spracovanie údajov medzi lokálnou SQLite databázou a registračným prihláškovým systémom používaným na prihlasovanie na preteky v orientačnom behu. Aplikácia využije existujúce API prihláškového systému, ktoré umožňuje čítanie a zapisovanie údajov. Funkcionalita systému zahŕňa:

-	Export zoznamu pretekárov z lokálnej SQLite databázy do registračného prihláškového systému prostredníctvom API.
-	Synchronizácia údajov medzi lokálnou databázou, ktorá získava údaje z existujúcej webovej aplikácie a prihláškového systému.
-	Import údajov o blížiacich sa pretekoch z registračného systému a ich export do zdieľaného Google kalendára.

### 1.3 Slovník pojmov
- <b>FMFI</b> - Fakulta matematiky, fyziky a informatiky
- <b>SZOS</b> - Slovenský zväz orientačných športov

### 1.4 Referencie
<ol type="a">
 <li> Github repozitár pripravovaného systému: <p> https://github.com/TIS2024-FMFI/preteky.git </p></li>
 <li> Github predošlého projektu zameraného na túto tému: <p> https://github.com/TIS2023-FMFI/sportovy-pretek </p</li>
 <li> [Opis API]()</li>


</ol>

### 1.5 Prehlad nasledujúcich kapitol
 
V nasledujúcich kapitolách sa dokument podrobne zameriava na všeobecnú funkcionalitu systému a špecifické požiadavky, ktoré sú naň kladené. V kapitole 2 sa popisuje perspektíva systému, jeho hlavné funkcie, charakteristiky používateľov, všeobecné obmedzenia a na záver aj predpoklady a závislosti, ktoré ovplyvňujú jeho fungovanie. Kapitola 3 následne obsahuje detailnú špecifikáciu požiadaviek na vyvíjaný systém, pričom každá požiadavka je presne definovaná a štruktúrovaná tak, aby poskytovala úplný obraz o funkciách a vlastnostiach systému.

## 2. Všeobecný popis

### 2.1 Perspektíva systému:
Športový klub Sandberg umožňuje prihlasovanie ich členov na preteky na ich klubovej stránke, lenže tá nie je prepojená s oficiálnou SZOS. Kvôli tomu musí byť pretek na klubovej stránke vytvorený manuálne a následne účastníci prihlásení na pretek v tejto klubovej aplikácii prihlásení naspäť do oficiálneho systému SZOS. 

### 2.2 Funkcie produktu:
Výsledný produkt by mal poskytnúť používateľské rozhranie v podobe konzolovej aplikácie, ktorá mu umožní pracovať s údajmi o pretekoch v klubovom internom systéme. Počas práce by sa užívateľovi vypisovali možnosti všetkých dostupných akcii, z ktorých by si vybral žiadaný úkon.
Táto aplikácia by mala umožniť zvoliť mesiac a vyhľadať v ňom pretek a následne získať žiadané dáta z is.orienteering.sk, ktoré spracuje, ošetrí vstupy pre kategórie pretekov a vytvorí takýto pretek v SQLite databáze Sandbergu. Po tejto akcii majú pretekári možnosť prihlásiť sa na klubovej stránke pričom admin nemusí manuálne pridať každý jeden pretek. 
Aplikácia by mala byť schopná aj exportu žiadaného preteku z SQLite databázy Sandbergu do .csv súboru, ktorá následne môže slúžiť ako input pre SZOS API pri prihlasovaní pretekárov na oficiálnu stránku. Toto prihlásenie pretekárov môže byť automatizované za pomoci aplikácie.
Ďalším možným vylepšením je import jednotlivých pretekov do google calendar.

### 2.3 Používatelia:
Aplikácia je tvorená výhradne len pre administrátora Sandberg systému, takže nie je potrebné rozdelenie rolí ani prihlasovanie do aplikácie.

### 2.4 Všeobecné obmedzenia:
Aplikácia pracuje s SQLite databázou a funguje lokálne na Windowse

### 2.5 Predpoklady a závislosti:
Táto aplikácia pozostáva z troch hlavných rozhraní. Prvé je komunikácia medzi konzolovou aplikáciou a SQLite databázou Sandbergu, kde aplikácia importuje pretek do databázy alebo získava údaje o preteku vo formáte csv. Druhé rozhranie je medzi aplikáciu a is.orienteering.sk stránkou, ktoré bude poskytnuté už existujúcim API. Tretím rozhraním je komunikácia užívateľa a aplikácie v podobe výberu predvolených command-ov v konzole.


## 3. Špecifické požiadavky
###  3.1 Stiahnutie údajov o pretekoch z API is.orienteering.sk
#### 3.1.1 Používateľ vyberie možnosť stiahnuť údaje o pretekoch cez konzolovú aplikáciu
#### 3.1.2 Používateľ má možnosť zvoliť si filtre, napr. zobrazenie 3 najbližších pretekov
        
####  3.1.3 Údaje o pretekoch, ako je dátum, názov, kategórie, miesto a deadline sa získajú zo systému is.orienteering.sk pomocou API a zobrazia sa užívateľovi 
     
####     3.1.4 Vybrané preteky sa naimportujú do databázy SQLite v klubovej aplikácií ŠK Sandberg
     
#####        i. Ak sa pretek už v databáze nachádza, aplikácia upozorní používateľa a neimportuje ho znova
#####       ii. Aplikácia skontroluje, či sú kategórie v správnom formáte a ak je formát zlý tak používateľa upozorní
### 3.2 Prihlásenie bežcov na preteky
####  3.2.1 Používateľ si vyberie aktívne preteky z klubovej aplikácie ŠK Sandberg
####         3.2.2 Používateľ vyberie bežcov, ktorí budú prihlásení na preteky cez is.orienteering.sk
####         3.2.3 Ak je už náhodu niektorí bežec na preteky prihlásený, aplikácia na to upozorní používateľa a neprihlási bežca znovu
### 3.3 Export údajov do textového súboru
  #### 3.3.1 Používateľ si vyberie preteky na ktoré sú bežci prihlásení
  ####      3.3.2 Používateľ vygeneruje textový súbor, kde je:
  #####          i. 3.3.2.1 Registračne číslo bežca
  #####          ii. 3.3.2.2 Kategória bežca
  #####          iii. Meno bežca
  ####      3.3.3 Tento súbor sa následne naimportuje na stránku is.orienteering.sk
### 3.4 Štatistiky bežcov
####  3.4.1 Používateľ môže zobraziť Štatistiky bežcov ako napríklad celkový počet pretekov, počet víťazstiev a podobne
####        3.4.2 Tieto štatistiky sa vygenerujú v o forme CSV súboru
### 3.5 Export do Google calendar
####   3.5.1 Údaje o pretekoch môžu byť automaticky pridané do Google calendar
### 3.6 Obmedzenia podľa kategórie
####   3.6.1 Používateľ nebude môcť prihlásiť bežcov do kategórií, na ktoré nemajú nárok podľa veku alebo iných pravidiel pretekov
