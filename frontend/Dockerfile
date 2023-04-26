# Base image (last LTS)
FROM node:latest

# Update the system
RUN apt-get update && apt-get upgrade -y

# Update node
RUN npm install -g npm@latest
RUN npm install -g @quasar/cli

# Make a working dir
WORKDIR /frontend

# Handle requirements
COPY package.json package-lock.jso[n] /frontend/
RUN npm install

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x frontend/entrypoint.sh

# Expose the ports
EXPOSE 8080

# Give it a (replaceable) entrypoint
ENTRYPOINT ["./entrypoint.sh"]
