#!/bin/sh

# Checking if connection with postgres is established, and then clears database and runs migration
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py loaddata account_tier/fixtures/account_tiers.json

exec "$@"
