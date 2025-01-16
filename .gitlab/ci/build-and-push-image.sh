#!/bin/sh

docker login registry.gitlab.isc.org

# Backup first.
docker pull registry.gitlab.isc.org/isc-projects/forge:latest
docker tag registry.gitlab.isc.org/isc-projects/forge:latest registry.gitlab.isc.org/isc-projects/forge:backup
docker push registry.gitlab.isc.org/isc-projects/forge:backup

# Rebuild and push.
cp ../../requirements.txt .
docker build --no-cache -t registry.gitlab.isc.org/isc-projects/forge ./
docker push registry.gitlab.isc.org/isc-projects/forge
rm requirements.txt
