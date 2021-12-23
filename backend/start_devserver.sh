#!/bin/bash
./wait_for_pg.sh
echo "Making migrations"
python manage.py makemigrations
./run_migration_chores.sh
echo "Starting the development server"
exec python manage.py runserver 0.0.0.0:8000
