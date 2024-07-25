#!/bin/sh
export PYTHONUNBUFFERED=1
POD_IP=$(hostname -i)
export DJANGO_ALLOWED_HOSTS="$POD_IP,localhost"
./manage.py migrate

./manage.py runserver 0.0.0.0:8000
