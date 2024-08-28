FROM python:3.9.19-alpine3.20

LABEL maintainer=shiva.r.160899@gmail.com
LABEL created_at="26-AUG-24"

# seting ENV variable for py
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV COLUMNS=80

# container's port to serve http
EXPOSE 8000

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app

ARG DEV=false

# creating virtual env; installing dependencies and creating user to limit privileges
RUN python -m venv /pyenv && \
    /pyenv/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /pyenv/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /pyenv/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        rest-api

# the container will look in /py/bin first before looking in the other directories for executables.
ENV PATH="/pyenv/bin:$PATH" 

# switching to the latest user
USER rest-api
