# VSS 365 Today

> VSS 365 Today website


## Required Keys

* Flask secret key
* Twitter Consumer API keys
* Twitter access token & access token secret
* MailJet public and private keys

## Install

1. Install Python 3.6+ and [Poetry](https://poetry.eustace.io/)
1. Rename `oss.env` to `.env`
1. Set missing environment variables
1. `poetry install`
1. `poetry shell`
1. `flask run`

## Build/Deploy

1. `docker build -f "docker/Dockerfile" -t vss365today:latest .`
1. `docker-compose up -d`

## Known Issues

Firefox's built-in content blocker prevents the Twitter-hosted images from loading,
as it blocks the `https://pbs.twimg.com` domain by default.
To see images in a tweet, consider disabling the content blocker just for this site.

## License

2019 Caleb Ely

[MIT](LICENSE)
