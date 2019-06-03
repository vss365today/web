import re

import tweepy

from src.core.config import load_app_config
from src.core.database import get_words_for_month


__all__ = [
    "IDENTIFYING_HASHTAGS",
    "create_twitter_connection",
    "find_prompt_tweet",
    "find_prompt_word",
    "get_all_hashtags",
    "get_tweet_media",
    "get_tweet_text",
    "make_hashtags",
    "make_mentions",
    "make_urls",
    "validate_email"
]


# The hashtags that identify a prompt tweet
IDENTIFYING_HASHTAGS = ("#VSS365", "#PROMPT")


def create_twitter_connection() -> tweepy.API:
    # Connect to the Twitter API
    CONFIG = load_app_config()
    auth = tweepy.OAuthHandler(
        CONFIG["TWITTER_APP_KEY"],
        CONFIG["TWITTER_APP_SECRET"]
    )
    auth.set_access_token(
        CONFIG["TWITTER_KEY"],
        CONFIG["TWITTER_SECRET"]
    )
    api = tweepy.API(auth)
    print("Successfully connected to the Twitter API")
    return api


def find_prompt_tweet(text: str) -> bool:
    return all(
        hashtag in text.upper()
        for hashtag in IDENTIFYING_HASHTAGS
    )


def get_all_hashtags(text: str) -> list:
    matches = re.findall(r"(#\w+)", text, re.I)
    return matches if matches else None


def find_prompt_word(text: str) -> str or None:
    prompt_word = None

    # Find all hashtags in the tweet
    hashtags = get_all_hashtags(text)
    if hashtags is None:
        return prompt_word

    # Remove all identifying hashtags
    # For the month of June, we need to remove the
    # anthology hashtag too to simplify things
    anthology = ("#VSS365A",)
    remaining = list(filter(
        lambda ht: ht.upper() not in IDENTIFYING_HASHTAGS + anthology,
        hashtags
    ))

    # If there are any hashtags left, get the first one
    # and remove the prefixed pound sign
    if remaining:
        prompt_word = remaining[0].replace("#", "")
    return prompt_word


def get_tweet_media(tweet: tweepy.Status) -> tuple:
    """Get the tweet's media if it exists."""
    media_url = ""
    tweet_media = None

    # If we have media in our tweet
    media = tweet.extended_entities.get("media")
    if media:
        # We need just a static image, and it's the same route to get one
        # rgardless of the media's non-animated image or "animated GIF" status
        media_url = media[0]["url"]
        tweet_media = media[0]["media_url_https"]
    return (media_url, tweet_media)


def get_tweet_text(tweet: tweepy.Status, media_url: str) -> str:
    """Get the tweet's complete text."""
    # Because we're accessing "extended" tweets (> 140 chars),
    # we need to be sure to access the full_text property
    # that holds the non-truncated text
    return tweet.full_text.replace(media_url, "").strip()


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
