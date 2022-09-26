#!/usr/bin/env bash

set -e

cd ..

set -a
source $PWD/.env
set +a

case "$1" in
--dev)
  export COMPOSE_PROJECT_NAME=warehouse_dev
  echo "The development containers data are removing ..."
  docker rmi warehouse-dev-flower
  docker rmi warehouse-dev-celery-worker
  docker rmi warehouse-dev-backend
  docker volume rm warehouse-dev-warehouse-db
  ;;
*)
  export COMPOSE_PROJECT_NAME=warehouse
  echo "The production containers data are removing ..."
  docker rmi warehouse-flower
  docker rmi warehouse-celery-worker
  docker rmi warehouse-backend
  docker volume rm warehouse-warehouse-backend warehouse_warehouse-db
  ;;
esac