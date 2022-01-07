#!/bin/bash

DEVLOPMENT_ENV=${DEVELOPMENT:-0}

if [ !DEVLOPMENT_ENV ] then
    ./run_migration_chores.sh --noinput
    echo "Starting server..."
    exec uwsgi --ini config_uwsgi.ini

else
    # Keep container alive
    exec tail -f /dev/null
fi
