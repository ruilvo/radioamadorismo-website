# Portal do Radioamadorismo

## How to deploy

Deployment needs Docker and `docker-compose`. To deploy the **development**
server (not suitable for production) you can run the following command:

```sh
docker compose -f "docker-compose.dev.yaml" up -d --build
```

To pull up the **production** server, first rename `sample.env` to `.env`, edit
the settings to your liking, and then run:

```sh
docker compose up -d --build
```

### Development

Development is best with VSCode. Pull up the **development** server, and then
open the `backend` or `frontend` folders with VSCode and it'll ask you open
the directory inside the container.

#### Docker + WSL2

WSL2 on Windows need to be configured with more file watchers.
This is a bit tricky, but you can follow the instructions (inspired from
[here](https://github.com/microsoft/WSL/issues/4293)).

First, create a script called `fs_watcher.sh` in your home directory:

```sh
nano fs_watcher.sh
```

Use the following contents

```sh
#!/bin/sh
sysctl fs.inotify.max_user_watches=524288
sysctl -p
```

Then, make it owned by root, executable, and delete-proof:

```sh
sudo chown root:root
sudo chmod 755
sudo chattr +i
```

Now, run the following command:

```sh
sudo EDITOR=nano visudo
```

Under the lines that say:

```sh
# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL
```

add:

```sh
%sudo ALL=(ALL:ALL) NOPASSWD:/home/<your_username_here>/fs_watcher.sh
```

replacing `<your_username_here>` with your username.

Now, edit your `.profile` file:

```sh
nano ~/.profile
```

and add this at the end of the file:

```sh
sudo /home/<your_username_here>/fs_watcher.sh
```

replacing `<your_username_here>` with your username.

Finally, reboot your computer.

### Access the backend terminal

You'll need to make a first superuser for Django. You can access a terminal for
the backend with:

```sh
docker compose exec backend /bin/bash
```

### Turning down the server

```sh
# For the development server
docker compose -f "docker-compose.dev.yaml" down

# For the production server
docker compose down
```

To clear/clean all Docker images, run:

```sh
docker system prune -af
docker builder prune -af

# To clean all volumes (including data) [VERY DANGEROUS]
docker volume prune -f # **This WILL lead to data loss**
```
