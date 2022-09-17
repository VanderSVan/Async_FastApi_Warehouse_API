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
  docker rmi warehouse_dev_flower
  docker rmi warehouse_dev_celery_worker
  docker rmi warehouse_dev_backend
  docker volume rm warehouse_dev_warehouse-db
  ;;
*)
  export COMPOSE_PROJECT_NAME=warehouse
  echo "The production containers data are removing ..."
  docker rmi warehouse_flower
  docker rmi warehouse_celery_worker
  docker rmi warehouse_backend
  docker volume rm warehouse_warehouse-backend warehouse_warehouse-db
  ;;
esac