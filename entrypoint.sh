#!/bin/bash

# This script is used to start the container for django development

## make migrations and migrate for sqlite
# python3 manage.py makemigrations
# python3 manage.py migrate --run-syncdb

## make migrations and migrate for postgres
python3 manage.py makemigrations members buildings userlog
python3 manage.py migrate

# start cron
service cron start

# start the django-crontab
python3 manage.py crontab add

# start server
python3 manage.py runserver 0.0.0.0:8000
