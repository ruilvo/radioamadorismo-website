# Portal do Radioamadorismo

## How to deploy

Deployment needs Docker and `docker-compose`. To deploy the **development**
server (not suitable for production) you can run the following command:

```sh
docker-compose -f "docker-compose.dev.yaml" up -d --build
```

To pull up the **production** server:

```sh
docker-compose -f "docker-compose.yaml" up -d --build
```

### Development

Development is best with VSCode. Pull up the **development** server, and then
open the `backend` or `frontend` folders with VSCode and it'll ask you open
the directory inside the container.

### Access the backend terminal

You'll need to make a first superuser for Django. You can access a terminal for
the backend with:

```sh
docker exec -it radioamadorismo-website_backend_1 /bin/bash
```

### Turning down the server

```sh
docker-compose -f "docker-compose.yaml" down
```

To clear/clean all Docker images, run:

```sh
docker system prune -a -f
docker volume prune -f # **This _can_ lead to data loss**
```
