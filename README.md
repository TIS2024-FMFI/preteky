# preteky

Projekt na Tvorbu informačných systémov 2024 - aplikácia pre prácu so systémom SZOS a webovou aplikáciou ŠK Sandberg.

# Inštalácia

## Krok 1: Klonovanie repozitára

1. Otvorte príkazový riadok alebo terminál.
2. Použite tento príkaz na stiahnutie repozitára do vášho počítača:

   ```bash
   git clone https://github.com/TIS2024-FMFI/preteky.git
   ```
3. Prejdite do priečinka vášho repozitára:
   ```bash
   cd preteky
   ```

## Voliteľé kroky: Nahranie súborov na server a inicializícia databázy

## Krok 2: Nahranie súborov na server

1. Prejdite do priečinka s súbormi, ktoré chcete nahrať na server:

   ```bash
   cd /API/sandberg_api
   ```

2. Použite príkaz scp na nahranie súborov na server:

   ```bash
   scp api.php export_import.php database_initialization.php username@senzor.robotika.sk:/var/www/sks/
   ```

Za username napíšte svoje prihlasovacie meno.
Po zadaní tohto príkazu budete požiadaní o heslo. Zadajte ho a počkajte na dokončenie nahrávania.

## Krok 3: Overenie

1. Pre pripojenie na server použite príkaz:

   ```bash
   ssh username@senzor.robotika.sk
   ```
   Za username napíšte svoje prihlasovacie meno.
   Po zadaní tohto príkazu budete požiadaní o heslo.

2. Prejdite do adresára /var/www/sks/:

   ```bash
   cd /var/www/sks/
   ```

3. Skontrolujte, či sú tam nahrané súbory:
   
   ```bash
   ls
   ```

## Krok 4: Inicializácia databázy

1. Prejdite do adresára /var/www/sks/:

   ```bash
   cd /var/www/sks/
   ```

2. Spustite skript database_initialization.php:

   ```bash
   php database_initialization.php
   ```

## Krok 5: Spustenie skriptu

1. Uistite sa, že máte skript setup_and_run.sh v koreňovom adresári repozitára.
2. Urobte skript spustiteľným, ak ešte ste to neurobili:

   ```bash
   chmod +x setup_and_run.sh
   ```

3. Spustite skript:
   ```bash
    ./setup_and_run.sh
    ```

Skript automaticky vytvorí virtuálne prostredie, nainštaluje potrebné knižnice a spustí konzolovú aplikáciu.


