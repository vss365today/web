from html import unescape
from itertools import zip_longest
import re
from typing import Iterable, Optional

from src.core.config import load_json_config


__all__ = [
    "format_content",
    "get_all_hashtags",
    "group_month_list_of_hosts",
    "make_hashtags",
    "make_mentions",
    "make_urls",
    "split_hashtags_into_list",
]


JSON_CONFIG = load_json_config()


def __grouper(iterable: Iterable) -> tuple:
    """Collect data into 2-length chunks or blocks.
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * 2
    return tuple(zip_longest(*args, fillvalue={}))


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


def group_month_list_of_hosts(hosts: Iterable[dict]) -> list:
    """Group multiple Hosts for a single month.

    For some months in 2017, three-overlapping Hosts
    gave out the prompts. While these are stored distinctly
    in the database, we need to present these as the same month.
    While it adds some complexity to the app, it makes the
    user experience more smooth and easier to navigate."""
    # Group the months into chunks of two
    final = []
    hosts_grouped = __grouper(hosts)

    # If there are multiple hosts in a single month,
    # lump the two handles together.
    # Since this will only get hit in historical data where
    # there's only two hosts in a single month,
    # this doesn't have to be any more ~~complicated~~ extensible
    for this_mo, next_mo in hosts_grouped:
        if next_mo and this_mo["date"] == next_mo["date"]:
            this_mo["handle"] = f"{this_mo['handle']}, {next_mo['handle']}"
            # Mark the second host record for removal
            next_mo["delete"] = True

    # Trim the hosts list down to just the ones we need
    for one, two in hosts_grouped:
        final.append(one)
        if two and not two.get("delete"):
            final.append(two)
    return final


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
