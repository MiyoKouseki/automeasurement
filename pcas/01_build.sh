#!/bin/bash
source settings
docker build -t $PCAS_NAME:$VERSION .
