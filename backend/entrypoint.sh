#!/bin/bash

# The script starts from /workspace
cd backend

if [[ -z "${DEVELOPMENT}" ]]
then
    ./run_migration_chores.sh --noinput
    echo "Starting server..."
    exec uwsgi --ini config_uwsgi.ini
else
    echo "Keeping alive..."
    exec tail -f /dev/null
fi
