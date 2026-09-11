#!/bin/sh

set -e

cd /app

gunicorn config.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 1 \
    --access-logfile - \
    --error-logfile - &

exec nginx -g "daemon off;"