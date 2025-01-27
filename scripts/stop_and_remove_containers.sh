# Stop and remove only the dst app container

#docker rm -f bdc-dashboard-app


#!/bin/bash

CONTAINER_NAME="bdc-dashboard-app"

# Check if the container exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Stopping and removing container: ${CONTAINER_NAME}"
  docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}
else
  echo "Container ${CONTAINER_NAME} does not exist."
fi

# Check if the associated image exists and remove it
IMAGE_ID=$(docker inspect ${CONTAINER_NAME} --format '{{.Image}}' 2>/dev/null)
if [ -n "${IMAGE_ID}" ]; then
  echo "Removing image: ${IMAGE_ID}"
  docker rmi -f ${IMAGE_ID}
else
  echo "No image found for container: ${CONTAINER_NAME}"
fi


