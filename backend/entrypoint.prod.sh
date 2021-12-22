#!/bin/bash

# This file runs from its parent dir
cd backend
source wait_for_pg.sh
exec uwsgi --ini config_uwsgi.ini
