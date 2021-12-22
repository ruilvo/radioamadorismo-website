#!/bin/bash
source wait_for_pg.sh
exec python manage.py runserver 0.0.0.0:8000
