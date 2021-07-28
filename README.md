# #vss365 today

> Get the latest #vss365 prompt

## Required Configuration

- Flask secret key (`SECRET_KEY_WEB`)
- Mailgun abuse email address (`ABUSE_EMAIL_ADDR`)
- Running instance of [#vss365 today API](https://github.com/le717/vss365today-api)
  - Operating domain (`API_DOMAIN`)
  - API key with `has_archive`, `has_broadcast`, `has_host`, `has_prompt`, `has_settings`, and `has_subscription` permissions (`API_AUTH_TOKEN`)

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
