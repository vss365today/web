# vss365

> View the latest VSS 365 prompt

## Install

1. Python 3.6+
1. [Poetry](https://poetry.eustace.io/)
1. `poetry install`
1. Throw MySQL/MariaDB instance at it
1. Run sql scheme files to create tables
1. `$ mv oss.env .env` and add missing auth/config values
1. `poetry run python ./wsgi.py`
