#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app
