from dataclasses import dataclass
from os.path import join

from jinja2 import Template

from src.core.filters import (
    create_api_date,
    format_datetime,
    format_date_pretty
)


__all__ = [
    "generate",
    "render",
    "EmailTemplate"
]


@dataclass
class EmailTemplate:
    text: str
    html: str


def create_tweet_url(tweet: dict) -> str:
    return f"https://twitter.com/{tweet['handle']}/status/{tweet['id']}"


def render(tweet: dict) -> EmailTemplate:
    """Render a complete email template."""
    # Read the templates
    html_template_file = join("src", "templates", "email", "email.html")
    text_template_file = join("src", "templates", "email", "email.txt")
    with open(html_template_file) as f:
        html_template = f.read()
    with open(text_template_file) as f:
        text_template = f.read()

    # Render the thing already
    return EmailTemplate(
        Template(text_template).render(tweet=tweet),
        Template(html_template).render(tweet=tweet)
    )


def generate(tweet: dict) -> dict:
    # Format the tweet date for both displaying and URL usage
    tweet_date = create_api_date(tweet["date"])
    tweet["date"] = format_datetime(tweet_date)
    tweet["date_pretty"] = format_date_pretty(tweet_date)

    # Construct a URL to the tweet
    tweet["url"] = create_tweet_url(tweet)
    return tweet
