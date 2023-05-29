# Base image
FROM python:latest

# Update the system, install postgres adapter
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y libpq-dev python3-dev gcc netcat \
    graphviz libgraphviz-dev

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

# Copy project files
COPY . .

# Move to the backend dir
WORKDIR /workspace/backend

# Make files executable
RUN chmod +x entrypoint.sh &&  \
    chmod +x run_migration_chores.sh && \
    chmod +x start_devserver.sh && \
    chmod +x wait_for_pg.sh

# Expose the ports
EXPOSE 8000

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./entrypoint.sh"]
