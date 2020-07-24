#!/bin/bash

wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
echo "$HEROKU_API_KEY" | docker login --username=$HEROKU_USER --password-stdin registry.heroku.com
docker build -f Dockerfile -t master-flaskblog:latest --target production_heroku .
docker tag master-flaskblog:latest registry.heroku.com/$HEROKU_APP_NAME/web
docker push registry.heroku.com/$HEROKU_APP_NAME/web
heroku container:release web --app $HEROKU_APP_NAME