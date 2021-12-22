#!/bin/bash
source wait_for_pg.sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --clear --noinput
