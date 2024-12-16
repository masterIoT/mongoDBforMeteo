# MongoDB Docker Setup

## Pull the Docker Image
Download the MongoDB image from GitHub Container Registry.

```bash
docker pull ghcr.io/masteriot/mongdbformeteo:latest
```

## Run the Docker Container

### For Windows
Run the following command to start the Docker container on Windows:

```powershell
docker run ^
  -p 127.0.0.1:27017:27017 ^
  --name mongodbformeteo-container ^
  -e MONGO_INITDB_ROOT_USERNAME=admin ^
  -e MONGO_INITDB_ROOT_PASSWORD=YOURPASSWORD ^
  --restart always ^
  -d ^
  ghcr.io/masteriot/mongdbformeteo:latest ^
  --auth
```

### For Linux/Mac
Run the following command to start the Docker container on Linux or Mac:

```bash
docker run \
  -p 127.0.0.1:27017:27017 \
  --name mongodbformeteo-container \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=YOURPASSWORD \
  --restart always \
  -d \
  ghcr.io/masteriot/mongdbformeteo:latest \
  --auth
```

## Access the Container's Bash Shell
To access the container's shell and execute commands inside it:

```bash
docker exec -it mongodbformeteo-container bash
```

## Restore the Database
To restore your database from an archive:

```bash
mongorestore --archive=/data/mongodb.archive -u admin -p 'YOURPASSWORD' --authenticationDatabase admin
```

## Connect to MongoDB using Mongo Shell
To connect to the database using the MongoDB shell:

```bash
mongosh -u admin -p 'YOURPASSWORD' --authenticationDatabase admin
```
