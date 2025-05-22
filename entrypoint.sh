#!/bin/bash
echo "🚀 Django server ishga tushdi!"

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info