# Base image
FROM python:3.9-bullseye

# Env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update the system, install postgres adapter
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y libpq-dev python3-dev gcc netcat

# Update pip
RUN pip install --upgrade pip

# Make a working dir
WORKDIR /workspace

# Handle requirements
COPY requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt

# Creates a non-root user and adds permission to access the working dir
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /workspace
USER appuser

# Copy project files
COPY --chown=appuser:appuser . backend

RUN mkdir static_root
RUN mkdir media_root

# Make files executable
RUN chmod +x backend/entrypoint.sh

# Expose the ports
EXPOSE 8000

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./backend/entrypoint.sh"]
