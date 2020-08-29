### Setting up postgres database in docker container

This section explains how to set up persistent database in docker container. To find the more info about it, please visit [official postgres docker page](https://hub.docker.com/_/postgres).

#### 1. Step
After installing docker and starting it, we will have to download postgres docker container. We'll use alpine version: `docker pull postgres:alpine`.

#### 2. Step
Under `docker-postgres-scripts` you will find commands on how to:
- Start postgres container (`postgres_docker_start.sh`)
First, it creates new volume, called `postgres-psz` in order to have database data saved when you stop the container and then it creates new container `postgres-psz` running on `port 4321` and mounting previously created volume `postgres-psz` to `/var/lib/postgresql/data`.
- Stop the container (`postgres_docker_stop.sh`).
- Remove the container (`postgres_container_remove.sh`).
- Backup up the table `properties` containing scraped realestate data (`postgres_container_backup.sh`).