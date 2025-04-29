FROM python:3.12.3-alpine


LABEL maintainer="danielmombeyni"

ENV PYTHONUNBUFFERED=1

COPY ./backend/requirements.txt /tmp/requirements.txt
COPY ./backend/requirements.dev.txt /tmp/requirements.dev.txt

COPY ./backend /app

WORKDIR /app

EXPOSE 8000

ARG DEV=false


RUN apk update && apk add --no-cache \
    postgresql15-client \
    jpeg-dev \
    zlib-dev \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev\
    postgresql-dev



RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    apk del gcc musl-dev libffi-dev

RUN adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol


ENV PATH="/py/bin/:$PATH"

USER django-user

