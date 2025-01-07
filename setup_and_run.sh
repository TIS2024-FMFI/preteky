#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python modules/console_app_implementacia.py