#!/bin/bash

if [[ -z "${DEVELOPMENT}" ]]
then
    ./run_migration_chores.sh --noinput
    echo "Starting server..."
    exec gunicorn -c gunicorn_config.py config.wsgi:application
else
    echo "Keeping alive..."
    exec tail -f /dev/null
fi
