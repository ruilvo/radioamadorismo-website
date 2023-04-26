# Base image
FROM python:3

# Update the system, install postgres adapter
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y libpq-dev python3-dev gcc netcat

# Update pip
RUN pip install --upgrade pip

# Make a working dir
WORKDIR /backend

# Handle requirements
COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

# Now, we have to update the PATH env. variable
ENV PATH="/root/.local/bin:${PATH}"

# Copy project files
COPY . .

# Make files executable
RUN chmod +x entrypoint.sh &&  \
    chmod +x run_migration_chores.sh && \
    chmod +x start_devserver.sh && \
    chmod +x wait_for_pg.sh

# Expose the ports
EXPOSE 8000

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./entrypoint.sh"]
