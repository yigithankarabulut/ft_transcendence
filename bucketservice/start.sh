#!/bin/bash

# Veritabanı hizmetinin hazır olmasını bekleyin
until python manage.py migrate --noinput; do
  echo "Waiting for database to be ready..."
  sleep 3
done

# Veritabanı migrasyonlarını çalıştırın
python manage.py makemigrations
python manage.py migrate

# Sunucuyu başlatın
exec "$@"
