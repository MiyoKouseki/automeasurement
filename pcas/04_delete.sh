#!/bin/bash
source settings
docker-compose stop 
docker stop $PCAS_NAME epics-base
docker rm $PCAS_NAME epics-base
docker network prune -y 
docker container prune -y 
docker image prune -y
