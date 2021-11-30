# Base image (last LTS)
FROM node:16.13-bullseye

# Update the system
RUN apt-get update && apt-get upgrade -y

# Make a working dir
WORKDIR /frontend

# Creates a non-root user and adds permission to access the working dir
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /frontend
USER appuser

# Handle requirements
COPY --chown=appuser:appuser package.json .
RUN npm install

# Copy project files
COPY --chown=appuser:appuser . .

# Make files executable
RUN chmod +x entrypoint.dev.sh
RUN chmod +x entrypoint.sh

# Expose the ports
EXPOSE 8080
