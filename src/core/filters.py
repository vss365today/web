from datetime import date, timedelta

from src.core.helpers import make_urls


__all__ = [
    "create_date",
    "format_content",
    "format_date",
    "previous",
    "next"
]


def create_date(date_str: str) -> date:
    return date(*[int(d) for d in date_str.split("-")])


def create_tweet_url(tweet: dict) -> str:
    return f"https://twitter.com/{tweet.giver.handle}/status/{tweet.tweet_id}"


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
    new_text = make_urls(new_text)
    return new_text


def format_date(date: date) -> str:
    """Nicely format the date as MM DD, YYYY."""
    return date.strftime("%B %d, %Y")


def previous(date: date) -> str:
    """Get the date prior to the given date."""
    return (date - timedelta(1)).isoformat()


def next(date: date) -> str:
    """Get the date after to the given date."""
    return (date + timedelta(1)).isoformat()
