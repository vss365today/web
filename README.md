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

1. `docker build -f "Dockerfile" -t vss365today:latest .`
1. `docker run -d --name vss365today -p 5000:5000 -t vss365today:latest`

## License

2019 Caleb Ely

[MIT](LICENSE)
