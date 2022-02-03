#!/bin/bash
source settings
cat settings > .env
docker-compose up -d
