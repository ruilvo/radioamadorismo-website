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
RUN pip install --user -r backend/requirements.txt

# Now, we have to update the PATH env. variable
ENV PATH="/root/.local/bin:${PATH}"

# Copy project files
COPY . backend

# Make files executable
RUN chmod +x backend/entrypoint.sh &&  \
    chmod +x backend/run_migration_chores.sh && \
    chmod +x backend/start_devserver.sh && \
    chmod +x backend/wait_for_pg.sh

# Expose the ports
EXPOSE 8000

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./backend/entrypoint.sh"]
