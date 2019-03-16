FROM python:3.7.2-alpine

ADD ./src /usr/src/app

WORKDIR /usr/src/app

ENV PACKAGES="gcc \
    binutils \
    gmp \
    isl \
    libgomp \
    libatomic \
    libgcc \
    mpfr3 \
    mpc1 \
    libc-dev \
    libstdc++ \
    linux-headers \
    libc-dev \
    musl-dev \
    pkgconf \
    python3 \
    python3-dev"

RUN apk add --no-cache $PACKAGES && \
    pip install pipenv uwsgi && \
    pip install -r requirements.txt && \
    apk del --no-cache --purge $PACKAGES

ENV PORT=8000

EXPOSE $PORT

ENTRYPOINT './entrypoint.sh'
