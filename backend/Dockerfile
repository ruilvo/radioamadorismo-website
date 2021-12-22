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

# Creates a non-root user and adds permission to access the working dir
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /workspace \
    && mkdir -p /home/appuser/.vscode-server \
    && chown -R appuser /home/appuser/.vscode-server
USER appuser

# Handle requirements
COPY --chown=appuser:appuser requirements.txt backend/requirements.txt
RUN pip install --user -r backend/requirements.txt

# Now, we have to update the PATH env. variable
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy project files
COPY --chown=appuser:appuser . backend

# Make files executable
RUN chmod +x backend/entrypoint.sh

# Expose the ports
EXPOSE 8000

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./backend/entrypoint.sh"]
