from datetime import datetime
from itertools import zip_longest
import re
from typing import Iterable, Optional, Tuple

import tweepy

from src.core import api
from src.core.config import (
    load_app_config,
    load_json_config
)


__all__ = [
    "create_twitter_connection",
    "find_prompt_tweet",
    "find_prompt_word",
    "get_all_hashtags",
    "group_month_list_of_hosts",
    "get_tweet_media",
    "get_tweet_text",
    "make_hashtags",
    "make_mentions",
    "make_urls"
]


CONFIG = load_app_config()
JSON_CONFIG = load_json_config()


def __filter_hashtags(hashtags: tuple) -> tuple:
    """Remove all hashtags that we don't need to process."""
    # Get the words used for this month and remove them from consideration
    right_now = datetime.now()
    month_prompts = api.get(
        "browse",
        params={
            "year": right_now.year,
            "month": right_now.month
        }
    )
    month_words = [prompt["word"] for prompt in month_prompts["prompts"]]

    # Go through each word for the month and find variations
    # of it in the tweet. Ex: the word is "motif", so find
    # "motifs" if it exists. Of course, exact word duplications
    # will also be matched. Our endgame is to filter out
    # previous prompt words in the prompt tweet
    # so they are not picked back up and recorded
    matched_variants = []
    for word in month_words:
        # Build a regex that will match exact words and suffix variations
        regex = re.compile(rf"#{word}\w*\b", re.I)

        # Search the tweet's hashtags for the words
        variants = [
            match.upper()
            for match in filter(regex.search, hashtags)
            if match
        ]

        # Record all variants we find
        if variants:
            matched_variants.extend(variants)

    # Merge the filter sets then take out all the hashtags
    hashtags_to_filter = (
        matched_variants +
        JSON_CONFIG["identifiers"] +
        JSON_CONFIG["additionals"]
    )
    return tuple(filter(
        lambda ht: ht.upper() not in hashtags_to_filter,
        hashtags
    ))


def __grouper(iterable: Iterable) -> tuple:
    """Collect data into 2-length chunks or blocks.
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * 2
    return tuple(zip_longest(*args, fillvalue={}))


def create_twitter_connection() -> tweepy.API:
    # Connect to the Twitter API
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
        for hashtag in JSON_CONFIG["identifiers"]
    )


def get_all_hashtags(text: str) -> Optional[tuple]:
    matches = re.findall(r"(#\w+)", text, re.I)
    return tuple(matches) if matches else None


def group_month_list_of_hosts(hosts: Iterable[dict]) -> list:
    """Group multiple Hosts for a single month.

    For some months in 2017, twonon-overlapping Hosts
    gave out the prompts. While these are stored distinctly
    in the database, we need to present these as the same month.
    While it adds some complexity to the app, it makes the
    user experience more smooth and easier to navigate."""
    # Group the months into chunks of two
    final = []
    hosts_grouped = __grouper(hosts)

    # If there are multiple hosts in a single month,
    # lump the two handles together.
    # Since this will only get git in historical data where
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


def find_prompt_word(text: str) -> Optional[str]:
    prompt_word = None

    # Find all hashtags in the tweet
    hashtags = get_all_hashtags(text)
    if hashtags is None:
        return prompt_word

    # Remove all identifying and unneeded hashtags
    remaining = __filter_hashtags(hashtags)

    # If there are any hashtags left, get the first one
    # and remove the prefixed pound sign
    if remaining:
        prompt_word = remaining[JSON_CONFIG["word_index"]].replace("#", "")
    return prompt_word


def get_tweet_media(tweet: tweepy.Status) -> Tuple[str, None]:
    """Get the tweet's media if it exists."""
    media_url = ""
    tweet_media = None

    # If we have media in our tweet
    if hasattr(tweet, "extended_entities"):
        media = tweet.extended_entities.get("media")
        if media:
            # We only need a static image, and it's the same route
            # to get one regardless if the media is an image
            # or an "animated GIF"
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
