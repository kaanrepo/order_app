#!/bin/bash

DJANGO_SUPERUSER_NAME=${DJANGO_SUPERUSER_NAME:-admin}

# Run Django migrations
/usr/local/bin/python manage.py makemigrations
/usr/local/bin/python manage.py migrate
/usr/local/bin/python manage.py createsuperuser --noinput --username ${DJANGO_SUPERUSER_NAME} || true