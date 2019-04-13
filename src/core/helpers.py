import re
from os.path import abspath

from dotenv import dotenv_values, find_dotenv
from sqlalchemy import create_engine


__all__ = [
    "IDENTIFYING_HASHTAGS",
    "create_db_connection",
    "find_prompt_tweet",
    "find_prompt_word",
    "get_all_hashtags",
    "load_env_vals",
    "make_hashtags",
    "make_mentions",
    "make_urls",
    "validate_email"
]


# The hashtags that identify a prompt tweet
IDENTIFYING_HASHTAGS = ("#VSS365", "#PROMPT")


def create_db_connection(config):
    connect_str = f"sqlite:///{abspath(config['DB_PATH'])}"
    return connect_str, create_engine(connect_str)


def find_prompt_tweet(text: str) -> bool:
    return all(
        hashtag in text.upper()
        for hashtag in IDENTIFYING_HASHTAGS
    )


def get_all_hashtags(text: str) -> list:
    regex = re.compile(r"(#\w+)", re.I)
    matches = re.findall(regex, text)
    return matches if matches else None


def find_prompt_word(text: str) -> str:
    prompt_word = ""

    # Find all hashtags in the tweet
    hashtags = get_all_hashtags(text)
    if hashtags is None:
        return prompt_word

    # Remove all identifying hashtags
    remaining = list(filter(
        lambda ht: ht.upper() not in IDENTIFYING_HASHTAGS,
        hashtags
    ))

    # If there are any hashtags left, get the second one
    # and remove the prefixed pound sign
    if remaining:
        prompt_word = remaining[1][1:]
    return prompt_word


def load_env_vals():
    # Load the variables from the .env file
    vals = {}
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        vals[key] = (value if value != "" else None)
    return vals


def make_hashtags(text: str) -> str:
    # Start by finding all hashtags
    hashtags = get_all_hashtags(text)
    if hashtags is None:
        return text

    # Go through each hashtag and make it a clickable link
    for ht in hashtags:
        html = f'<a href="https://twitter.com/hashtag/{ht[1:]}">{ht}</a>'
        text = text.replace(ht, html)
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


def validate_email(addr: str) -> bool:
    regex = r"[a-z0-9.-_]+@[a-z0-9.-_]+\.[a-z0-9.-_]+"
    return re.fullmatch(regex, addr) is not None
