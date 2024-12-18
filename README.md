# preteky
Projekt na Tvorbu informačných systémov 2024 - aplikácia pre prácu so systémom SZOS a webovou aplikáciou ŠK Sandberg
# Inštalácia
## Inštalačný návod pre nahranie súborov

Tento návod popisuje, ako nahrávať súbory na server z GitHubu pomocou príkazového riadku.

## Krok 1: Klonovanie repozitára

1. Otvorte príkazový riadok alebo terminál.
2. Použite tento príkaz na stiahnutie repozitára do vášho počítača:

   ```bash
   git clone https://github.com/TIS2024-FMFI/preteky.git
   ```
3. Prejdite do priečinka vášho repozitára:
   ```bash
   cd preteky/API/sandberg_api
   ```
## Krok 2: Nahranie súborov na server
1. Použite príkaz scp na nahranie súborov na server:
   ```bash
   scp api.php export_import.php username@senzor.robotika.sk:/var/www/sks/
   ```
   Za username napíšte svoje prihlasovacie meno.
   
2. Po zadaní tohto príkazu budete požiadaní o heslo. Zadajte ho a počkajte na dokončenie nahrávania.
## Krok 3: Overenie
1. Pre pripojenie na server použite príkaz:
   ```bash
   ssh username@senzor.robotika.sk
   ```
2. Prejdite do priečinka s nahranými súbormi:
   ```bash
   cd /var/www/sks/
   ls
   ```
