#!/bin/sh
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Checking if initial data seeding is needed..."
python manage.py shell -c "
from property_app.models import PropertySetting, CondoUnit
from django.core.management import call_command
if not CondoUnit.objects.exists() or not PropertySetting.objects.exists():
    print('Empty database detected. Running seed_data...')
    call_command('seed_data')
else:
    print('Database is already seeded with suites and settings.')
"

# Optional automatic superuser creation if environment variables are provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "==> Checking/creating admin superuser ($DJANGO_SUPERUSER_USERNAME)..."
    python manage.py createsuperuser --noinput || true
fi

PORT="${PORT:-8000}"
WORKERS="${GUNICORN_WORKERS:-3}"

echo "==> Starting production Gunicorn server on 0.0.0.0:$PORT with $WORKERS workers..."
exec gunicorn dlyns_condo.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
