#!/bin/bash

docker login --username $DOCKER_USER --password $DOCKER_PASS

if [[ "${TRAVIS_BRANCH}" = "master" ]]; then
    TAG="latest"
elif [[ "${TRAVIS_BRANCH}" = "dev" ]]; then
    TAG="latest-dev"
else
    TAG="latest-feature"
fi

docker build -f Dockerfile -t $TRAVIS_REPO_SLUG:$TAG --target production .
docker tag $TRAVIS_REPO_SLUG $DOCKER_REPO
docker push $DOCKER_REPO