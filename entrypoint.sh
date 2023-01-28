#!/bin/bash

# This script is used to start the container for django development

APP_PORT=${PORT:-8000}

## make migrations and migrate for postgres
python3 manage.py makemigrations members buildings userlog
python3 manage.py migrate

# create superuser
# python3 manage.py createsuperuser --noinput || true

# collect static files
python3 manage.py collectstatic --noinput 

# start server
# python3 manage.py runserver 0.0.0.0:8000 using django server
# daphne -b 0.0.0.0 -p 8000 ims.asgi:application using daphne

# using gunicorn server
gunicorn  ims.wsgi:application --bind "0.0.0.0:${APP_PORT}"