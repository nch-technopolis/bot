#!/usr/bin/env sh

uwsgi --socket 0.0.0.0:${PORT} --wsgi-file app.py
