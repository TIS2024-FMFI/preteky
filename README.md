# preteky

Projekt na Tvorbu informačných systémov 2024 - aplikácia pre prácu so systémom SZOS a webovou aplikáciou ŠK Sandberg.

# Inštalácia
Pre správne fungovanie aplikácie je potrebné mať nainštalovaný operačný systém Linux alebo WSL. Iné operačné systémy nie sú podporované.
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

## Voliteľé kroky od 2 až po 4: Nahranie súborov na server a inicializácia databázy

## Krok 2: Nahranie súborov na server

1. Prejdite do priečinka s súbormi, ktoré chcete nahrať na server:

   ```bash
   cd API/sandberg_api
   ```

2. Použite príkaz scp na nahranie súborov na server:

   ```bash
   scp api.php export_import.php database_initialization.php username@senzor.robotika.sk:/var/www/sks/
   ```

Za username napíšte svoje prihlasovacie meno.
Po zadaní tohto príkazu budete požiadaní o heslo. Zadajte ho a počkajte na dokončenie nahrávania.
## Správny výpis pre nahratie súborov

Po pripojení na server a vykonaní prenosu súborov očakávame nasledovný výpis:

```
username@senzor.robotika.sk's password:
api.php 100% 1745 1.7KB/s 00:00 
export_import.php 100% 7631 465.8KB/s 00:00 
database_initialization.php 100% 1438 87.8KB/s 00:00
``` 

Tento výpis znamená, že súbory boli úspešne nahrané na server. Ak sa objaví podobný výstup, inštalácia môže pokračovať ďalšími krokmi.

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
Očakáva sa, že tam bude viac súborov ako naše tri nahraté, ale to nie je predmetom tohto projektu.

## Krok 4: Inicializácia databázy

1. Prejdite do adresára /var/www/sks/:

   ```bash
   cd /var/www/sks/
   ```

2. Spustite skript database_initialization.php:

   ```bash
   php database_initialization.php
   ```
Očakávame takýto výstup:
```
Stĺpec 'api_comp_cat_id' bol úspešne odstránený.
Tabuľky boli úspešne vyčistené.
Inicializácia databázy bola dokončená.
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
Takýto výpis by ste mali dostať, že sa všetko nainštalovalo:
 ```
Collecting pip~=24.3.1 (from -r requirements.txt (line 1))
  Using cached pip-24.3.1-py3-none-any.whl.metadata (3.7 kB)
Collecting wheel~=0.44.0 (from -r requirements.txt (line 2))
  Using cached wheel-0.44.0-py3-none-any.whl.metadata (2.3 kB)
Collecting setuptools~=70.0.0 (from -r requirements.txt (line 3))
  Using cached setuptools-70.0.0-py3-none-any.whl.metadata (5.9 kB)
Collecting toml~=0.10.2 (from -r requirements.txt (line 4))
  Using cached toml-0.10.2-py2.py3-none-any.whl.metadata (7.1 kB)
Collecting requests~=2.32.3 (from -r requirements.txt (line 5))
  Using cached requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
Collecting matplotlib~=3.7.5 (from -r requirements.txt (line 6))
  Using cached matplotlib-3.7.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.7 kB)
Collecting google-auth~=2.20.0 (from -r requirements.txt (line 7))
  Using cached google_auth-2.20.0-py2.py3-none-any.whl.metadata (4.2 kB)
Collecting google-auth-httplib2~=0.1.0 (from -r requirements.txt (line 8))
  Using cached google_auth_httplib2-0.1.1-py2.py3-none-any.whl.metadata (2.1 kB)
Collecting google-api-python-client~=2.92.0 (from -r requirements.txt (line 9))
  Using cached google_api_python_client-2.92.0-py2.py3-none-any.whl.metadata (6.6 kB)
Collecting charset-normalizer<4,>=2 (from requests~=2.32.3->-r requirements.txt (line 5))
  Using cached charset_normalizer-3.4.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (35 kB)
Collecting idna<4,>=2.5 (from requests~=2.32.3->-r requirements.txt (line 5))
  Using cached idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting urllib3<3,>=1.21.1 (from requests~=2.32.3->-r requirements.txt (line 5))
  Using cached urllib3-2.3.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests~=2.32.3->-r requirements.txt (line 5))
  Downloading certifi-2025.1.31-py3-none-any.whl.metadata (2.5 kB)
Collecting contourpy>=1.0.1 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached contourpy-1.3.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.4 kB)
Collecting cycler>=0.10 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached cycler-0.12.1-py3-none-any.whl.metadata (3.8 kB)
Collecting fonttools>=4.22.0 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Downloading fonttools-4.56.0-cp312-cp312-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (101 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 101.9/101.9 kB 3.9 MB/s eta 0:00:00
Collecting kiwisolver>=1.0.1 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached kiwisolver-1.4.8-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.2 kB)
Collecting numpy<2,>=1.20 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
Collecting packaging>=20.0 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached packaging-24.2-py3-none-any.whl.metadata (3.2 kB)
Collecting pillow>=6.2.0 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached pillow-11.1.0-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (9.1 kB)
Collecting pyparsing>=2.3.1 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached pyparsing-3.2.1-py3-none-any.whl.metadata (5.0 kB)
Collecting python-dateutil>=2.7 (from matplotlib~=3.7.5->-r requirements.txt (line 6))
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting cachetools<6.0,>=2.0.0 (from google-auth~=2.20.0->-r requirements.txt (line 7))
  Using cached cachetools-5.5.1-py3-none-any.whl.metadata (5.4 kB)
Collecting pyasn1-modules>=0.2.1 (from google-auth~=2.20.0->-r requirements.txt (line 7))
  Using cached pyasn1_modules-0.4.1-py3-none-any.whl.metadata (3.5 kB)
Collecting rsa<5,>=3.1.4 (from google-auth~=2.20.0->-r requirements.txt (line 7))
  Using cached rsa-4.9-py3-none-any.whl.metadata (4.2 kB)
Collecting six>=1.9.0 (from google-auth~=2.20.0->-r requirements.txt (line 7))
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting urllib3<3,>=1.21.1 (from requests~=2.32.3->-r requirements.txt (line 5))
  Using cached urllib3-1.26.20-py2.py3-none-any.whl.metadata (50 kB)
Collecting httplib2>=0.19.0 (from google-auth-httplib2~=0.1.0->-r requirements.txt (line 8))
  Using cached httplib2-0.22.0-py3-none-any.whl.metadata (2.6 kB)
Collecting google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5 (from google-api-python-client~=2.92.0->-r requirements.txt (line 9))
  Downloading google_api_core-2.24.1-py3-none-any.whl.metadata (3.0 kB)
Collecting uritemplate<5,>=3.0.1 (from google-api-python-client~=2.92.0->-r requirements.txt (line 9))
  Using cached uritemplate-4.1.1-py2.py3-none-any.whl.metadata (2.9 kB)
Collecting googleapis-common-protos<2.0.dev0,>=1.56.2 (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client~=2.92.0->-r requirements.txt (line 9))
  Using cached googleapis_common_protos-1.66.0-py2.py3-none-any.whl.metadata (1.5 kB)
Collecting protobuf!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<6.0.0.dev0,>=3.19.5 (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client~=2.92.0->-r requirements.txt (line 9))
  Using cached protobuf-5.29.3-cp38-abi3-manylinux2014_x86_64.whl.metadata (592 bytes)
Collecting proto-plus<2.0.0dev,>=1.22.3 (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client~=2.92.0->-r requirements.txt (line 9))
  Downloading proto_plus-1.26.0-py3-none-any.whl.metadata (2.2 kB)
Collecting pyasn1<0.7.0,>=0.4.6 (from pyasn1-modules>=0.2.1->google-auth~=2.20.0->-r requirements.txt (line 7))
  Using cached pyasn1-0.6.1-py3-none-any.whl.metadata (8.4 kB)
Using cached pip-24.3.1-py3-none-any.whl (1.8 MB)
Using cached wheel-0.44.0-py3-none-any.whl (67 kB)
Using cached setuptools-70.0.0-py3-none-any.whl (863 kB)
Using cached toml-0.10.2-py2.py3-none-any.whl (16 kB)
Using cached requests-2.32.3-py3-none-any.whl (64 kB)
Using cached matplotlib-3.7.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.6 MB)
Using cached google_auth-2.20.0-py2.py3-none-any.whl (181 kB)
Using cached google_auth_httplib2-0.1.1-py2.py3-none-any.whl (9.3 kB)
Using cached google_api_python_client-2.92.0-py2.py3-none-any.whl (11.4 MB)
Using cached cachetools-5.5.1-py3-none-any.whl (9.5 kB)
Downloading certifi-2025.1.31-py3-none-any.whl (166 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 166.4/166.4 kB 6.7 MB/s eta 0:00:00
Using cached charset_normalizer-3.4.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (145 kB)
Using cached contourpy-1.3.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
Using cached cycler-0.12.1-py3-none-any.whl (8.3 kB)
Downloading fonttools-4.56.0-cp312-cp312-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.9/4.9 MB 18.4 MB/s eta 0:00:00
Downloading google_api_core-2.24.1-py3-none-any.whl (160 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 160.1/160.1 kB 11.9 MB/s eta 0:00:00
Using cached httplib2-0.22.0-py3-none-any.whl (96 kB)
Using cached idna-3.10-py3-none-any.whl (70 kB)
Using cached kiwisolver-1.4.8-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.5 MB)
Using cached numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (18.0 MB)
Using cached packaging-24.2-py3-none-any.whl (65 kB)
Using cached pillow-11.1.0-cp312-cp312-manylinux_2_28_x86_64.whl (4.5 MB)
Using cached pyasn1_modules-0.4.1-py3-none-any.whl (181 kB)
Using cached pyparsing-3.2.1-py3-none-any.whl (107 kB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached rsa-4.9-py3-none-any.whl (34 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Using cached uritemplate-4.1.1-py2.py3-none-any.whl (10 kB)
Using cached urllib3-1.26.20-py2.py3-none-any.whl (144 kB)
Using cached googleapis_common_protos-1.66.0-py2.py3-none-any.whl (221 kB)
Downloading proto_plus-1.26.0-py3-none-any.whl (50 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50.2/50.2 kB 3.3 MB/s eta 0:00:00
Using cached protobuf-5.29.3-cp38-abi3-manylinux2014_x86_64.whl (319 kB)
Using cached pyasn1-0.6.1-py3-none-any.whl (83 kB)
Installing collected packages: wheel, urllib3, uritemplate, toml, six, setuptools, pyparsing, pyasn1, protobuf, pip, pillow, packaging, numpy, kiwisolver, idna, fonttools, cycler, charset-normalizer, certifi, cachetools, rsa, requests, python-dateutil, pyasn1-modules, proto-plus, httplib2, googleapis-common-protos, contourpy, matplotlib, google-auth, google-auth-httplib2, google-api-core, google-api-python-client
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed cachetools-5.5.1 certifi-2025.1.31 charset-normalizer-3.4.1 contourpy-1.3.1 cycler-0.12.1 fonttools-4.56.0 google-api-core-2.24.1 google-api-python-client-2.92.0 google-auth-2.20.0 google-auth-httplib2-0.1.1 googleapis-common-protos-1.66.0 httplib2-0.22.0 idna-3.10 kiwisolver-1.4.8 matplotlib-3.7.5 numpy-1.26.4 packaging-24.2 pillow-11.1.0 pip-24.3.1 proto-plus-1.26.0 protobuf-5.29.3 pyasn1-0.6.1 pyasn1-modules-0.4.1 pyparsing-3.2.1 python-dateutil-2.9.0.post0 requests-2.32.3 rsa-4.9 setuptools-70.0.0 six-1.17.0 toml-0.10.2 uritemplate-4.1.1 urllib3-1.26.20 wheel-0.44.0
 ```
Skript automaticky vytvorí virtuálne prostredie, nainštaluje potrebné knižnice a spustí konzolovú aplikáciu.
 ```
(press 'q' to quit, UP and DOWN to navigate, ENTER to select option, 'b' for back)
--- MENU ---
> Import preteku
  Prihlásenie pretekárov
  Export do súboru
  Štatistiky pretekara
________________________________________
 ```

