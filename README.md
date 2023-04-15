# #vss365 today Web

> Get the latest #vss365 prompt

## Required Secrets

- Flask secret key (`SECRET_KEY_WEB`)
- Mailgun abuse email address (`ABUSE_EMAIL_ADDR`)
- Running instance of [#vss365 today API v2](https://github.com/le717/vss365today-api)
  - Operating domain (`API_DOMAIN`)
  - API key with `has_archive`, `has_notification`, `has_hosts`, `has_prompts`, and `has_emails` permissions (`API_AUTH_TOKEN`)
- Static files hosting URL (prod only) (`STATIC_FILES_URL`)

## Development

1. Install [Python](https://www.python.org/) 3.10+, [Poetry](https://poetry.eustace.io/) 1.3.0+, and VS Code
1. Create required secret keys in appropriate place (default: `/app/../secrets`)
1. Adjust configuration values in appropriate `configuration/*.json` files as necessary
1. Run `poetry install`
1. Launch the app using the provided VS Code launch configuration

SVG icons sourced from [Heroicons](https://heroicons.com/).

## Build

Creating a Docker image will install all required components.
Creating an image is a one-line command:

1. `docker build -t vss365today-web:latest .`

## License

2019-2023 Caleb

[MIT](LICENSE)
