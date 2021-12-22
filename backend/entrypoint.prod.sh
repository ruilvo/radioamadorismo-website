#!/bin/bash
source wait_for_pg.sh
exec uwsgi --ini config_uwsgi.ini
