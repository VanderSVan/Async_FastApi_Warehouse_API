#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Activate our virtual environment for `poetry` here.
if [[ $FASTAPI_ENV == 'development' ]]; then
  . /opt/pysetup/.venv/bin/activate
fi

# Create a new database if it doesn't exists.
python -m src.db --create_db

# And run alembic migrations
cd src/db/ && alembic upgrade head && cd ../..

# Populate the database with prepared data
if [[ $INSERT_PREPARED_DATA == 'TRUE' ]]; then
  python -m src.utils.db_populating --populate_db
fi

# `exec "$@"` is typically used to make the entrypoint
# a pass through that then runs the docker command.
# `"$@"` list of arguments passed to script as string / delimited list
exec "$@"
