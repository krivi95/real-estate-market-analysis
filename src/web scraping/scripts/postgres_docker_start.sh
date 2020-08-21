docker volume create postgres-psz
docker run --name postgres-psz -e POSTGRES_PASSWORD=intas -v postgres-psz:/var/lib/postgresql/data  -d -p 4321:5432 postgres:alpine