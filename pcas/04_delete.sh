#!/bin/bash
source settings
docker stop $PCAS_NAME epics-base
docker rm $PCAS_NAME epics-base
