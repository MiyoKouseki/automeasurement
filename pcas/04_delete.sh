#!/bin/bash
source settings
docker stop $PCAS_NAME
docker rm $PCAS_NAME
