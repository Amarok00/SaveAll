# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Wait for the database to be ready
RUN until python Save_all/manage.py migrate; do \
    >&2 echo "Database is unavailable - sleeping"; \
    sleep 1; \
  done

# Output message once database is up
RUN >&2 echo "Database is up - continuing with prestart tasks"

# Collect static files
RUN cd Save_all/
RUN python Save_all/manage.py makemigrations
RUN python Save_all/manage.py migrate

# Start Daphne in the background
RUN cd Save_all/
CMD daphne -p 8001 Save_all.asgi:application & \
    python Save_all/manage.py runserver 0.0.0.0:8000
