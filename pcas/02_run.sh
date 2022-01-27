#!/bin/bash
source settings

docker run --name=$PCAS_NAME \
       --platform=linux/amd64 \
       -itd \
       -w /work \
       --network=host \
       --env-file=.env \
       $PCAS_NAME:$VERSION
