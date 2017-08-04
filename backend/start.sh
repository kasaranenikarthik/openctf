#!/bin/bash

# stop if any command fails
set -e

COMMAND=$1
DATABASE_URL=mysql://${DB_USER}:${MYSQL_ROOT_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
ENVIRONMENT=${ENV:-"development"}
PORT=${PORT:-80}
WORKERS=${WORKERS:-4}

# make sure db is available
>&2 echo "waiting for mysql..."
until mysqladmin ping -h"${DB_HOST}" -P"${DB_PORT}" --silent; do
    sleep 1
done
mysql -u"${DB_USER}" -p"${MYSQL_ROOT_PASSWORD}" -h"${DB_HOST}" -P"${DB_PORT}" -e"create database if not exists ${DB_NAME};"
>&2 echo "ready."

# start main application
case ${COMMAND} in
    runserver )
        if [ "${ENV}" == "production" ]; then
            bash -c "python manage.py db upgrade; gunicorn --bind 0.0.0.0:${PORT} -w ${WORKERS} openctf:create_app()"
        else
            bash -c "python manage.py db upgrade; python manage.py runserver"
        fi
        ;;
    worker )
        bash -c "python manage.py db upgrade; python manage.py worker"
        ;;
esac
