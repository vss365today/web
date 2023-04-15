import re
from html import unescape

from flask import current_app, url_for

import markupsafe


__all__ = [
    "format_content",
    "get_all_hashtags",
    "get_static_url",
    "make_hashtags",
    "make_mentions",
    "make_urls",
]


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


def get_all_hashtags(text: str) -> tuple:
    return tuple(re.findall(r"(#\w+)", text, re.I))


def get_static_url(filename: str) -> str:
    """Generate a URL to static assets based on dev/prod status."""
    # If this config key is present, we are running in prod,
    # which means we should pull the files from a URL
    if (static_url := current_app.config.get("STATIC_FILES_URL")) is not None:
        return f"{static_url}/{filename}"

    # Otherwise, we're running locally, so we pull the files
    # from the local filesystem
    return url_for("static", filename=filename)


def make_hashtags(text: str) -> str:
    # Go through each hashtag and make it a clickable link
    for ht in get_all_hashtags(text):
        html = f'<a href="https://twitter.com/hashtag/{ht[1:]}">{ht}</a>'
        text = re.sub(rf"({ht})\b", html, text)
    return markupsafe.soft_str(markupsafe.Markup(text))


def make_mentions(text: str) -> str:
    # Start by finding all possible @mentions
    mentions = re.findall(r"(@\w+)", text, re.I)
    if not mentions:
        return text

    # Go through each mention and make it a clickable link
    for mention in mentions:
        html = markupsafe.Markup(
            f'<a href="https://twitter.com/{mention[1:]}">{mention}</a>'
        )
        text = text.replace(mention, html)
    return markupsafe.soft_str(text)


def make_urls(text: str) -> str:
    """Convert all text links in a tweet into an HTML link."""
    # Start by finding all possible t.co text links
    links = re.findall(r"(https://t\.co/[a-z0-9]+)", text, re.I)
    if not links:
        return text

    # Go through each url and make it a clickable link
    for link in links:
        html = markupsafe.Markup(f'<a href="{link}">{link}</a>')
        text = text.replace(link, html)
    return markupsafe.soft_str(text)
