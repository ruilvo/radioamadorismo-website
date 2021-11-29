#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
exec gunicorn config.wsgi -b 0.0.0.0:8000
