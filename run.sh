#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

if [ ! -d .venv ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install django
else
    source .venv/bin/activate
fi

if [ ! -f db.sqlite3 ]; then
    python manage.py migrate
    python seed.py
fi

echo "Starting WebVuln Lab on http://0.0.0.0:9000"
python manage.py runserver 0.0.0.0:9000
