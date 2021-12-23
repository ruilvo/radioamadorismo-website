#!/bin/bash

# This file runs from its parent dir
cd backend
./run_migration_chores.sh --noinput
echo "Starting server..."
exec uwsgi --ini config_uwsgi.ini
