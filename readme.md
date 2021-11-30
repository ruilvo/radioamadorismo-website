# Radioamadorismo: website

A basic django-rest-framework (+ Vue.js) website.

## How to deploy

Deployment needs Docker and `docker-compose`. To deploy the **development**
server (not suitable for production) you can run the following command:

```sh
docker-compose -f "docker-compose.dev.yaml" up -d --build
```

To clear/clean all Docker images, run:

```sh
docker system prune -a -f
docker volume prune -f
```

To access a backend shell:

```sh
docker exec -it radioamadorismo-website-backend-1 /bin/bash
```

To pull up the **deployment** server:

```sh
docker-compose -f "docker-compose.yaml" up -d --build
```
