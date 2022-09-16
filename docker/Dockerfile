# Set args
ARG PYTHON_VERSION=3.10
ARG PYTHON_VERSION_SUFFIX=slim-buster

# Creating a python base with shared environment variables
FROM python:${PYTHON_VERSION}-${PYTHON_VERSION_SUFFIX} AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DEPENDS="/usr/src/dependencies" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# -----------------------------------------------------------
# 'PIP-POETRY-BASE' stage is used to install pip and poetry only
FROM python-base as pip-poetry-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION>=1.1.0
RUN curl -sSL https://install.python-poetry.org | python3 -


# We copy our Poetry requirements here to cache them
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

# And create requirements.txt file for production mode
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt


# -----------------------------------------------------------
# 'POETRY-BASE' stage is used to build dependencies for development mode
FROM python-base as poetry-base

WORKDIR $PYSETUP_PATH
# Copying poetry and venv into image
COPY --from=pip-poetry-base $POETRY_HOME $POETRY_HOME
COPY --from=pip-poetry-base $PYSETUP_PATH $PYSETUP_PATH

# Install all deps using poetry
RUN poetry install


# -----------------------------------------------------------
# 'DEVELOPMENT' stage installs all dev deps and can be used to develop code.
FROM python-base as development
ENV FASTAPI_ENV=development

# Copying poetry and venv into image
COPY --from=poetry-base $POETRY_HOME $POETRY_HOME
COPY --from=poetry-base $PYSETUP_PATH $PYSETUP_PATH

# Copying our entrypoint
COPY ./docker/docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /app
COPY . .


# -----------------------------------------------------------
# 'PIP-BASE' stage is used to build dependencies for production mode
FROM python-base as pip-base

COPY --from=pip-poetry-base $PYSETUP_PATH $PYSETUP_PATH

#Install dependencies and uvicorn globally. Uvicorn need for support WebSocket Nginx
RUN pip install --upgrade pip &&  \
    pip install --no-cache-dir -r $PYSETUP_PATH/requirements.txt


# -----------------------------------------------------------
# 'PRODUCTION' stage installs all dev deps and can be used to develop code.
FROM python-base as production
ENV FASTAPI_ENV=production

COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY --from=pip-base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=pip-base /usr/local/bin/ /usr/local/bin/

WORKDIR /app
COPY . .

RUN rm -d -r tests/ \
    && rm -d -r docker/ \
    && rm -d -r nginx/ \
    && rm poetry.lock \
    && rm pyproject.toml