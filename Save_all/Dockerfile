FROM python:3.10
WORKDIR /code/Save_all

COPY requirements.txt /code/Save_all/requirements.txt 
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /code/Save_all


EXPOSE 8000

RUN until python manage.py migrate; do \
    >&2 echo "Database is unavailable - sleeping"; \
    sleep 1; \
  done

# Output message once database is up
RUN >&2 echo "Database is up - continuing with prestart tasks"

# Collect static files

# Start Daphne in the background
CMD daphne -b 0.0.0.0 -p 8000  Save_all.asgi:application 
