#!/bin/sh

DOCKER_TAG=${1:-test-python-pip-flask}
DOCKER_DEFAULT_PLATFORM=linux/amd64

docker build -t $DOCKER_TAG .