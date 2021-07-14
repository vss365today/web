# #vss365 today

> Get the latest #vss365 prompt

## Required Configuration

- Flask secret key (`SECRET_KEY_WEB`)
- Running instance of [#vss365 today API](https://github.com/le717/vss365today-api/) (`API_DOMAIN`)
  - API key for protected endpoint access (`API_AUTH_TOKEN`)
- Mailgun abuse email address (`ABUSE_EMAIL_ADDR`)

## Install

1. Install Python 3.9+ and [Poetry](https://python-poetry.org/) 1.1.0+
1. Set missing configuration keys in appropriate `configuration/*.json` files
1. Create secret files in appropriate place (default: `/app/secrets`)
1. Run `poetry install`
1. Launch the app using the provided VS Code launch configuration

## Build

1. `docker build -t vss365today-web:latest .`

## License

2019-2021 Caleb

[MIT](LICENSE)
