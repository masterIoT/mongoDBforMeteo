# MongoDB Docker Setup

## Pull the Docker Image
# Pull the MongoDB image from GitHub Container Registry.
docker pull ghcr.io/masteriot/mongdbformeteo:latest

## Run the Docker Container
# For Windows
docker run ^
  -p 127.0.0.1:27017:27017 ^
  --name mongodbformeteo-container ^
  -e MONGO_INITDB_ROOT_USERNAME=admin ^
  -e MONGO_INITDB_ROOT_PASSWORD=YOURPASSWORD ^
  --restart always ^
  -d ^
  ghcr.io/masteriot/mongdbformeteo:latest ^
  --auth

# For Linux/Mac
docker run \
  -p 127.0.0.1:27017:27017 \
  --name mongodbformeteo-container \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=YOURPASSWORD \
  --restart always \
  -d \
  ghcr.io/masteriot/mongdbformeteo:latest \
  --auth

## Access the Container's Bash Shell
# Access the shell to run commands inside the container.
docker exec -it mongodbformeteo-container bash

## Restore the Database
# Restore your database from an archive.
mongorestore --archive=/data/mongodb.archive -u admin -p 'YOURPASSWORD' --authenticationDatabase admin

## Connect to MongoDB using Mongo Shell
# Connect to the database using the Mongo shell.
mongosh -u admin -p 'YOURPASSWORD' --authenticationDatabase admin
