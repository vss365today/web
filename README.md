# vss365

> VSS 365 Today website

## Install

1. Python 3.6+
1. [Poetry](https://poetry.eustace.io/)
1. Throw MySQL/MariaDB instance at it
1. Run sql scheme files to create tables
1. `$ mv oss.env .env` and add missing auth/config values
1. `poetry install`
1. `poetry shell`
1. `flask run`

## Build/Deploy

1. `docker build -f "Dockerfile" -t vss365today:latest .`
1. `docker run -d --name vss365today -p 5001:5001 -t vss365today:latest`

## License

2019 Caleb Ely

[MIT](LICENSE)
