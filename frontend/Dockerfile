# Base image (last LTS)
FROM node:16.13-bullseye

# Update the system
RUN apt-get update && apt-get upgrade -y

# Update node
RUN npm install -g npm@latest
RUN npm install -g @quasar/cli

# Make a working dir
WORKDIR /workspace

# Creates a non-root user and adds permission to access the working dir
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /workspace
USER appuser

# Copy project files
COPY --chown=appuser:appuser . frontend

# Make files executable
RUN chmod +x frontend/entrypoint.sh

# Expose the ports
EXPOSE 8080

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./frontend/entrypoint.sh"]
