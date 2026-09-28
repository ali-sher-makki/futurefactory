#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser --noinput || true
if [ -n "$VAPID_PRIVATE_KEY_B64" ]; then
  echo "$VAPID_PRIVATE_KEY_B64" | base64 -d > private_key.pem
fi