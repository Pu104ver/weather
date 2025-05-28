#!/bin/sh

echo "⏳ Waiting for database..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "✅ Database is up. Running migrations..."
python manage.py migrate

echo "🚀 Starting server..."

exec "$@"