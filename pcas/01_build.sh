#!/bin/bash
source settings

echo $PCAS_NAME:$VERSION
docker build -t $PCAS_NAME:$VERSION ./build/pcas
docker build -t epics-base:$VERSION ./build/epics-base
