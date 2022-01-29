#!/bin/bash
source settings

docker run --name=$PCAS_NAME \
       --platform=linux/amd64 \
       -itd \
       -w /work \
       --env-file=.env \
       $PCAS_NAME:$VERSION

docker run --name=epics-base \
       --platform=linux/amd64 \
       -itd \
       epics-base:v0.0.1
