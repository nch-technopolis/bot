FROM python:3.8.1-slim-buster

ARG version=local
ENV VERSION=$version
ENV PYTHONUNBUFFERED=1

ENV PORT=8000

EXPOSE $PORT

ADD ./src /usr/src/app

WORKDIR /usr/src/app

RUN set -x \
    && buildDeps='gcc libc-dev' \
    && apt-get update && apt-get install -y --no-install-recommends \
        $buildDeps \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uwsgi \
    && pip install --no-cache-dir -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && find /usr/src/app -type d -name __pycache__ -exec rm -rf '{}' + \
    && apt-get purge -y --auto-remove $buildDeps

