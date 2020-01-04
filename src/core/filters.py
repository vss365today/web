from datetime import datetime
from html import unescape

from src.core.helpers import (
    make_hashtags,
    make_mentions,
    make_urls
)


__all__ = [
    "create_datetime",
    "format_datetime",
    "create_api_date",
    "format_api_date",
    "format_content",
    "format_date_pretty",
    "format_month_year"
]


def create_datetime(date_str: str) -> datetime:
    """Create a datetime object from an ISO date string."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def format_datetime(date_obj: datetime) -> str:
    return date_obj.strftime("%Y-%m-%d")


def create_api_date(date_str: str) -> datetime:
    """Create a datetime object from an API response date string.

    E.g, Tue, 02 Jul 2019 00:00:00 GMT
    """
    return datetime.strptime(date_str, "%a, %d %b %Y 00:00:00 GMT")


def format_api_date(date_obj: datetime) -> str:
    """Create an API response date string from a datetime object.

    E.g, Tue, 02 Jul 2019 00:00:00 GMT
    """
    return date_obj.strftime("%a, %d %b %Y 00:00:00 GMT")


def format_date_pretty(date_obj: datetime) -> str:
    """Pretty format a date in MM DD, YYYY."""
    return date_obj.strftime("%B %d, %Y")


def format_month_year(date: str) -> str:
    """Format a date as MM YYYY."""
    # Add in a dummy day if needed
    if len(date.split("-")) == 2:
        date = f"{date}-01"
    return create_datetime(date).strftime("%B %Y")


def create_tweet_url(tweet: dict) -> str:
    return "https://twitter.com/{writer_handle}/status/{tweet_id}".format_map(
        tweet
    )


def format_content(text: str) -> str:
    # Wrap all non-blank lines in paragraphs
    split_text = text.split("\n")
    split_text = [
        f"<p>{para.strip()}</p>"
        for para in split_text
        if para  # false-y value means blank line
    ]

    # Rejoin the lines and make all links clickable
    new_text = "\n".join(split_text)
    new_text = unescape(new_text)
    new_text = make_hashtags(new_text)
    new_text = make_mentions(new_text)
    new_text = make_urls(new_text)
    return new_text
