#!/bin/bash

echo "Docker container before cleanup ..."
docker ps

if [ -z ${CONTAINER_NAME} ]; then
    echo "No docker cleanup, conntainer name is not passed"
else
    echo "Container name recieved from env : ${CONTAINER_NAME}, cleaning only that container ..."
    docker stop $(docker ps -aqf "name=^${CONTAINER_NAME}$")
    docker rm $(docker ps -aqf "name=^${CONTAINER_NAME}$")
    docker rmi $(docker images "${CONTAINER_NAME}" -q)
fi

echo "After Cleanup ..."
docker ps
echo "Done"

