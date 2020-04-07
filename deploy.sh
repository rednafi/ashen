#!/bin/bash

# bring down the containers
docker-compose down

# remove the containers and orphan volumes
docker-compose rm -f -v

# remove all dangling volumes
docker volume rm $(docker volume ls -qf dangling=true)

# remove the image of the base app
# this app will be rebuild
# ignore the containers that do not need to be rebuilt
docker rmi $(docker images |grep 'area-search-engine_app')

# bring up the containers again
docker-compose up -d
