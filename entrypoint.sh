#!/bin/bash


python manage.py waitfordb
python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn eureka.wsgi:application -w 3 --bind 0.0.0.0:8000