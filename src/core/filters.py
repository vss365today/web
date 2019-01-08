from datetime import datetime
from datetime import timedelta
import re


__all__ = [
    "create_proper_image_url",
    "format_content",
    "format_date",
    "format_image_url"
]


def create_proper_image_url(
    text: str,
    img_short_url: str,
    img_full_url: str
) -> str:
    """Replace a t.co image short link with a full image url."""
    return text.replace(img_short_url, img_full_url)


def format_image_url(text: str) -> str:
    # Find an URL, if one is present
    regex = re.compile(
        r"https://pbs\.twimg\.com/.+\.(?:jpg|png|gif)",
        re.MULTILINE
    )
    match = re.search(regex, text)

    # If we have one, put it in an HTML img tag
    if match:
        url = match.group(0)
        text = text.replace(url, f'<img width="500" src="{url}">')
    return text


def format_content(text: str) -> str:
    return "\n".join([
        f"<p>{format_image_url(para)}</p>"
        for para in text.split("\r\n")
        if para
    ])


def format_date(date) -> str:
    return date.strftime("%d %B, %Y")


def yesterday(date) -> str:
    return datetime.strftime(date - timedelta(1), "%Y-%m-%d")


def tomorrow(date) -> str:
    return datetime.strftime(date + timedelta(1), "%Y-%m-%d")
