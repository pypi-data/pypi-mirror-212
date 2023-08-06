#!/usr/bin/env sh
set -e

for PYTHON_VERSION in 3.7 3.8 3.9 3.10 3.11; do
    TARGET=registry.gitlab.com/gorilladev/pytest-django-ifactory/python:$PYTHON_VERSION
    docker build --pull --build-arg PYTHON_VERSION=$PYTHON_VERSION -t $TARGET \
	   $(dirname $0)
    docker push $TARGET
done
