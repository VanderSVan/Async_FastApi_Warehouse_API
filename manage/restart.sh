#!/usr/bin/env bash

set -e

cd ..

set -a
source $PWD/.env
set +a

case "$1" in
--dev)
  export COMPOSE_PROJECT_NAME=warehouse-dev
  echo "The development containers are restarting ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml restart
  ;;
*)
  export COMPOSE_PROJECT_NAME=warehouse
  echo "The production containers are restarting ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.prod.yml restart
  ;;
esac