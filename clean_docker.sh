#!/bin/bash

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -q)

# Remove all containers (including stopped ones)
echo "Removing all containers..."
docker rm $(docker ps -a -q)

# Remove all images
echo "Removing all images..."
docker rmi $(docker images -q)

# Remove all unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove all unused networks
echo "Removing unused networks..."
docker network prune -f

# Remove dangling images (images not associated with any containers)
echo "Removing dangling images..."
docker image prune -f

# Remove all build cache
echo "Removing build cache..."
docker builder prune -f

echo "Docker cleanup complete!"
