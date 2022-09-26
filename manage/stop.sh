#!/usr/bin/env bash

set -e

cd ..

set -a
source $PWD/.env
set +a

case "$1" in
--dev)
  export COMPOSE_PROJECT_NAME=warehouse-dev
  echo "The development containers are stopping ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml stop
  echo "The development containers are removing ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml down
  ;;
*)
  export COMPOSE_PROJECT_NAME=warehouse
  echo "The production containers are stopping ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.prod.yml stop
  echo "The production containers are removing ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.prod.yml down
esac