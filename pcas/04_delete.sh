#!/bin/bash
source settings
docker-compose stop 
docker stop $PCAS_NAME epics-base
docker rm $PCAS_NAME epics-base
docker network rm isolated
docker network rm isolated2
