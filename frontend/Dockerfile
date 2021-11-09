# Base image (last LTS)
FROM node:16.13-bullseye

# Update the system
RUN apt-get update && apt-get upgrade -y

# TODO: run as much as possible as non-root

# Make a working dir
WORKDIR /node

# Install dependencies
COPY package*.json .

# Handle requirements
RUN npm install --silent

# Copy project files
COPY . .

# Make files executable
RUN chmod +x entrypoint.dev.sh

# Expose the ports
EXPOSE 3000
