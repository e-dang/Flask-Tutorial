#!/bin/bash

# wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
# heroku plugins:install @heroku-cli/plugin-container-registry

# echo "$HEROKU_PASS" | docker login --username=_ --password-stdin registry.heroku.com
# heroku container:push web --app $HEROKU_APP_NAME --arg TARGET=production_heroku
# heroku container:release web --app $HEROKU_APP_NAME
docker ls -a
echo $DOCKER_USER/$DOCKER_REPO:$TAG

if [[ "${TRAVIS_BRANCH}" = "master" ]]; then
    export TAG="latest"
    export TARGET="production_heroku"
elif [[ "${TRAVIS_BRANCH}" = "dev" ]]; then
    export TAG="latest-dev"
    export TARGET="dev"
else
    export TAG="latest-feature"
    export TARGET="dev"
fi

docker tag $DOCKER_USER/$DOCKER_REPO:$TAG registry.heroku.com/edang-flaskblog/web
docker push registry.heroku.com/edang-flaskblog/web