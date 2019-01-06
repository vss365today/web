from datetime import datetime
from datetime import timedelta
import re


def find_image(content: str) -> str:
    regex = re.compile(r"https://.+\.(?:jpg|png|gif)", re.MULTILINE)
    match = re.search(regex, content)
    if match:
        url = match.group(0)
        content = content.replace(url, f'<img width="500" src="{url}">')
    return content


def format_content(content) -> str:
    return "\n".join([
        f"<p>{find_image(para)}</p>"
        for para in content.split("\r\n")
        if para
    ])

def format_date(date) -> str:
    return date.strftime("%d %B, %Y")


def yesterday(date) -> str:
    return datetime.strftime(date - timedelta(1), "%Y-%m-%d")


def tomorrow(date) -> str:
    return datetime.strftime(date + timedelta(1), "%Y-%m-%d")
