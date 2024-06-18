#!/bin/sh
cp ../../requirements.txt .
docker login registry.gitlab.isc.org
docker build --no-cache -t registry.gitlab.isc.org/isc-projects/forge ./
docker push registry.gitlab.isc.org/isc-projects/forge
