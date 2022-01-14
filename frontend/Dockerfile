# Base image (last LTS)
FROM node:16.13-bullseye

# Update the system
RUN apt-get update && apt-get upgrade -y

# Update node
RUN npm install -g npm@latest
RUN npm install -g @quasar/cli

# Make a working dir
WORKDIR /workspace

# Handle requirements
COPY package.json package-lock.jso[n] frontend/
RUN cd frontend && npm install

# Copy project files
COPY . frontend

# Make entrypoint executable
RUN chmod +x frontend/entrypoint.sh

# Expose the ports
EXPOSE 8080

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./frontend/entrypoint.sh"]
