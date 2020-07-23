#!/bin/bash

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

if [[ "${TRAVIS_BRANCH}" = "master" ]]; then
    TAG="latest"
elif [[ "${TRAVIS_BRANCH}" = "dev" ]]; then
    TAG="latest-dev"
else
    TAG="latest-feature"
fi

docker build -f Dockerfile -t $DOCKER_REPO:$TAG --target production_heroku .
docker push "$DOCKER_USER"/"$DOCKER_REPO"