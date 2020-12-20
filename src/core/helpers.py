from html import unescape
import re
from typing import List, Optional

from src.core.config import load_json_config
from src.core.filters.date import create_datetime


__all__ = [
    "format_content",
    "get_all_hashtags",
    "get_unique_year_months",
    "make_hashtags",
    "make_mentions",
    "make_urls",
    "split_hashtags_into_list",
]


JSON_CONFIG = load_json_config()


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


def get_all_hashtags(text: str) -> Optional[tuple]:
    matches = re.findall(r"(#\w+)", text, re.I)
    return tuple(matches) if matches else None


def get_unique_year_months(year_data: List[dict]) -> List[dict]:
    """Make all Host dates for a given year into a unique set.

    For some months in 2017, November 2020, and in 2021 and beyond,
    there are multiple Hosts per month giving out the prompts.
    While the individual dates are stored distinctly,
    we need a unique year/month list in order to correctly display the
    year browsing page. This function creates that unique list."""
    unique = []

    # Go through each host for this year
    for host in year_data:
        # Convert the date they are hosting into a month-year group
        date = create_datetime(host["date"])
        month_dict = {"year": str(date.year), "month": date.strftime("%m")}

        # If we've not already seen this combo, we record it
        if month_dict not in unique:
            unique.append(month_dict)
    return unique


def make_hashtags(text: str) -> str:
    # Start by finding all hashtags
    hashtags = get_all_hashtags(text)
    if hashtags is None:
        return text

    # Go through each hashtag and make it a clickable link
    for ht in hashtags:
        html = f'<a href="https://twitter.com/hashtag/{ht[1:]}">{ht}</a>'
        text = re.sub(fr"({ht})\b", html, text)
    return text


def make_mentions(text: str) -> str:
    # Start by finding all possible @mentions
    mentions = re.findall(r"(@\w+)", text, re.I)
    if mentions is None:
        return text

    # Go through each mention and make it a clickable link
    for mention in mentions:
        html = f'<a href="https://twitter.com/{mention[1:]}">{mention}</a>'
        text = text.replace(mention, html)
    return text


def make_urls(text: str) -> str:
    """Convert all text links in a tweet into an HTML link."""
    # Start by finding all possible t.co text links
    links = re.findall(r"(https://t\.co/[a-z0-9]+)", text, re.I)
    if links is None:
        return text

    # Go through each url and make it a clickable link
    for link in links:
        html = f'<a href="{link}">{link}</a>'
        text = text.replace(link, html)
    return text


def split_hashtags_into_list(hashtags: str) -> list:
    return [
        hashtag.strip().upper()
        for hashtag in hashtags.split("\r\n")
        if hashtag.startswith("#")
    ]
