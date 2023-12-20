# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client net-tools telnet curl libpq-dev python-dev build-essential\
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
# Set the working directory to /app
WORKDIR /waste-management

# Copy the current directory contents into the container at /app
COPY . /waste-management

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install PostgreSQL client library

# Expose port 80 for web server
EXPOSE 8000

# Set environment variables for PostgreSQL connection
# Run migrations and start web server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:80"]