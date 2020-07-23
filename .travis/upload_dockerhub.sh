#!/bin/bash

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

if [[ "${TRAVIS_BRANCH}" = "master" ]]; then
    TAG="latest"
    TARGET="production_heroku"
elif [[ "${TRAVIS_BRANCH}" = "dev" ]]; then
    TAG="latest-dev"
    TARGET="dev"
else
    TAG="latest-feature"
    TARGET="dev"
fi

docker build -f Dockerfile -t $DOCKER_USER/$DOCKER_REPO:$TAG --target $TARGET .
docker push $DOCKER_USER/$DOCKER_REPO:$TAG