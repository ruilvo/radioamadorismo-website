# Base image
FROM python:3.9-bullseye

# Env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update the system, install postgres adapter
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y libpq-dev python3-dev gcc

# Update pip
RUN pip install --upgrade pip

# Make a working dir
WORKDIR /backend

# Creates a non-root user and adds permission to access the working dir
RUN adduser --disabled-password --gecos "" appuser \
    && mkdir /static_root \
    && mkdir /media_root \
    && chown -R appuser /static_root \
    && chown -R appuser /media_root \
    && chown -R appuser /backend
USER appuser

# Handle requirements
COPY --chown=appuser:appuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/worker/.local/bin:${PATH}"

# Copy project files
COPY --chown=appuser:appuser . .

# Make files executable
RUN chmod +x entrypoint.dev.sh

# Expose the ports
EXPOSE 8000
