#!/bin/bash
./wait_for_pg.sh
echo "Running migration chores"
echo "Migrating"
python manage.py migrate $1 # --noinput
echo "Collecting static files"
python manage.py collectstatic --clear $1 # --noinput
echo "Done migrating!"
