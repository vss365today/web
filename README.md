  # #vss365 today

> Get the latest #vss365 prompt


## Required Configuration

* Running instance of [#vss365 today API](https://github.com/le717/vss365-today-api/) (domain configurable)
* Flask secret key
* JWT secret key
* Twitter Consumer API keys
* Twitter access token & access token secret

## Install

1. Install Python 3.8+ and [Poetry](https://python-poetry.org/) 1.0.0+
1. `mv oss.env .env`
1. Set missing configuration keys
1. `poetry install`
1. `poetry run flask run`

## Build

1. `docker build -f "docker/Dockerfile" -t vss365-today:latest .`

## License

2019-2020 Caleb Ely

[MIT](LICENSE)
