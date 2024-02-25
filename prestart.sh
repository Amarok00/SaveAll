# Wait for the database to be ready
until python /code/Save_all/manage.py migrate; do
  >&2 echo "Database is unavailable - sleeping"
  sleep 1
done

>&2 echo "Database is up - continuing with prestart tasks"

# Collect static files
python /code/Save_all/manage.py collectstatic --noinput

# Start Daphne in the background
daphne -p 8001 Save_all.asgi:application &

# Start the main application
exec "$@"