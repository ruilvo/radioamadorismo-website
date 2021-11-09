# Base image
FROM python:3.9-bullseye

# Env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update the system, install postgres adapter
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y libpq-dev python3-dev gcc

# TODO: run as much as possible as non-root

# Update pip
RUN pip install --upgrade pip

# Make a working dir
WORKDIR /django

# Handle requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Make files executable
RUN chmod +x entrypoint.dev.sh

# Expose the ports
EXPOSE 8000
