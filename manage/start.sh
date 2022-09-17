#!/usr/bin/env bash

set -e

cd ..

set -a
source $PWD/.env
set +a

case "$1" in
--dev)
  export COMPOSE_PROJECT_NAME=warehouse_dev
  echo "The development containers are running ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml up --build
  ;;
*)
  export COMPOSE_PROJECT_NAME=warehouse
  echo "The production containers are running ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.prod.yml up -d --build
  ;;
esac