#!/bin/bash
echo "Waiting for postgres..."
while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
done
echo "PostgreSQL started"
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
exec python manage.py runserver 0.0.0.0:8000
