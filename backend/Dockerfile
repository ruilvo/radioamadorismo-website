# Base image
FROM python:latest

# Env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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
