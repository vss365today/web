#!/usr/bin/env bash
python3 ./listener.py & gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app
