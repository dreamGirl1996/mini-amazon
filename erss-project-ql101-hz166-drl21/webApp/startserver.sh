#!/bin/bash
python3 amazon_web/manage.py makemigrations
python3 amazon_web/manage.py migrate

python3 amazon_web/manage.py runserver 0.0.0.0:8000

