#!/usr/bin/env bash

set -x -e

docker build -t data-manipulation-coursera .
# Start interactive container with all code mounted
docker run -it --rm -v `pwd`:/opt/code --workdir=/opt/code data-manipulation-coursera
