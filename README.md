  # #vss365 today

> Get the latest #vss365 prompt


## Required Configuration

* Running instance of [#vss365 today API](https://github.com/le717/vss365-today-api/) (domain configurable)
* Flask secret key
* JWT secret key
* Twitter Consumer API keys
* Twitter access token & access token secret
* Mailgun API key & verified domain (_to be removed_)
* Mailjet public & private keys (_to be removed_)
* SMTP server address (default port 587, configurable)

## Install

1. Install Python 3.8+ and [Poetry](https://poetry.eustace.io/) 1.0.0b6+
1. `mv oss.env .env`
1. Set missing configuration keys
1. `poetry install`
1. `poetry run flask run`

## Build/Deploy

1. `docker build -f "docker/Dockerfile" -t vss365-today:latest .`
1. `docker-compose -f "docker/docker-compose.yml" up -d`

## Known Issues

- Firefox's built-in content blocker prevents the Twitter-hosted media from loading,
as it blocks the `https://pbs.twimg.com` domain by default.
To see tweet media, consider disabling the content blocker just for this site.

## License

2019-2020 Caleb Ely

[MIT](LICENSE)
