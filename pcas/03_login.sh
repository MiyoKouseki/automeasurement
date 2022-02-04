#!/bin/bash

source settings
echo "docker exec -it $PCAS_NAME bash"
docker exec -it pcas bash
#echo "docker exec -it epics-base bash"
#docker exec -it epics-gateway bash
