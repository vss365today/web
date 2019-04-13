import re
from os.path import abspath

from dotenv import dotenv_values, find_dotenv
from sqlalchemy import create_engine


__all__ = [
    "create_db_connection",
    "find_prompt_tweet",
    "find_prompt_word",
    "get_all_hashtags",
    "load_env_vals",
    "make_hashtags",
    "make_urls",
    "validate_email"
]


def create_db_connection(config):
    connect_str = f"sqlite:///{abspath(config['DB_PATH'])}"
    return connect_str, create_engine(connect_str)


def find_prompt_tweet(text: str) -> bool:
    return all(
        hashtag in text.upper()
        for hashtag in ("#VSS365", "#PROMPT")
    )


def get_all_hashtags(text: str) -> list:
    regex = re.compile(r"(#\w+)", re.MULTILINE)
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
        lambda hashtag: hashtag.upper() not in ("#VSS365", "#PROMPT"),
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

    # Go through each url and wrap it in an HTML a tag
    for ht in hashtags:
        url = f'<a href="https://twitter.com/hashtag/{ht[1:]}">{ht}</a>'
        text = text.replace(ht, url)
    return text


def make_urls(text: str) -> str:
    """Convert all text links in a tweet into an HTML link."""
    # Start by finding all possible t.co text links
    matches = re.findall(r"(https://t\.co/[a-z0-9]+)", text, re.I)
    if matches is None:
        return text

    # Go through each url and wrap it in an HTML a tag
    for match in matches:
        url = f'<a href="{match}">{match}</a>'
        text = text.replace(match, url)
    return text


def validate_email(addr: str) -> bool:
    regex = r"[a-z0-9.-_]+@[a-z0-9.-_]+\.[a-z0-9.-_]+"
    return re.fullmatch(regex, addr) is not None
