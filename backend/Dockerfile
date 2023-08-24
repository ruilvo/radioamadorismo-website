# Base image
FROM python:latest

# Update the system, install postgres adapter
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc graphviz netcat-traditional
RUN apt-get install -y python3-dev libpq-dev libgraphviz-dev
RUN apt-get install -y python3-gdal

# Now, we have to update the PATH env. variable
ENV PATH="/root/.local/bin:${PATH}"

# Update pip
RUN pip install --upgrade pip

# Make a working dir
# We do not use /backend directly so that during development we can still use
# git.
WORKDIR /workspace

# Handle requirements
COPY requirements.txt backend/requirements.txt
RUN cd backend && pip install --user -r requirements.txt && cd ..

# Move to the backend dir
WORKDIR /workspace/backend

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
