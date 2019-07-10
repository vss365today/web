from datetime import date, timedelta
from html import unescape

from src.core.helpers import (
    make_hashtags,
    make_mentions,
    make_urls
)


__all__ = [
    "create_date",
    "format_content",
    "format_date",
    "format_month_year",
    "tomorrow",
    "yesterday"
]


def create_date(date_str: str) -> date:
    """Create a date object from an ISO date string."""
    return date.fromisoformat(date_str)


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


def format_date(date: date) -> str:
    """Format a date as MM DD, YYYY."""
    return date.strftime("%B %d, %Y")


def format_month_year(date: str) -> str:
    """Format a date as MM YYYY."""
    # Add in a dummy day if needed
    if len(date.split("-")) == 2:
        date = f"{date}-01"
    return create_date(date).strftime("%B %Y")


def tomorrow(date: date) -> str:
    """Get the date after the given date."""
    return (date + timedelta(1)).isoformat()


def yesterday(date: date) -> str:
    """Get the date prior to the given date."""
    return (date - timedelta(1)).isoformat()
