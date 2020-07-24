#!/bin/bash

# wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
# heroku plugins:install @heroku-cli/plugin-container-registry

# echo "$HEROKU_PASS" | docker login --username=_ --password-stdin registry.heroku.com
# heroku container:push web --app $HEROKU_APP_NAME --arg TARGET=production_heroku
# heroku container:release web --app $HEROKU_APP_NAME
docker tag $DOCKER_USER/$DOCKER_REPO registry.heroku.com/edang-flaskblog/web
docker push registry.heroku.com/edang-flaskblog/web