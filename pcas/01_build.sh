#!/bin/bash
source settings
docker build -t $PCAS_NAME:$VERSION ./build/pcas
docker build -t epics-base:v0.0.1 ./build/epics-base
