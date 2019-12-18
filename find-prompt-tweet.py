from datetime import date, timedelta
from html import escape
from pprint import pprint

from requests.exceptions import HTTPError
import tweepy

from src.core import api
from src.core.database import (
    get_writer_by_date,
    get_uid_by_handle
)
from src.core.emails.sender import send_emails
from src.core.filters import create_date, create_api_date, format_api_date_iso
from src.core.helpers import (
    create_twitter_connection,
    find_prompt_tweet,
    find_prompt_word,
    get_tweet_media,
    get_tweet_text
)


def is_prompters_own_tweet(status: tweepy.Status) -> bool:
    """Identify if this tweet is original to the prompter.

    Currently, this means removing both retweets and
    retweeted quote tweets of the prompter's tweets.
    """
    return (
        not status.retweeted and
        not hasattr(status, "retweeted_status")
    )


def process_tweets(uid: str, tweet_id: str = None, recur_count: int = 0):
    # If we recurse too many times, stop searching
    if recur_count > 7:
        return None

    # Get the latest tweets from the prompt writer
    # We need to enable extended mode to get tweets > 140 characters
    statuses = twitter_api.user_timeline(
        uid,
        max_id=tweet_id,
        count=20,
        tweet_mode="extended"
    )

    # Start by collecting _only_ the prompter's original tweets
    own_tweets = list(filter(is_prompters_own_tweet, statuses))

    prompt_tweet = None
    for tweet in own_tweets:
        # Try to find the prompt tweet among the pulled tweets
        if find_prompt_tweet(tweet.full_text):
            prompt_tweet = tweet
            break
        continue

    # We didn't find the prompt tweet, so we need to search again,
    # but this time, older than the oldest tweet we currently have
    if prompt_tweet is None:
        return process_tweets(uid, own_tweets[-1].id_str, recur_count + 1)
    return prompt_tweet


# Get the latest tweet in the database to see if we need to do anything
LATEST_TWEET = api.get("prompt")[0]
LATEST_TWEET["date"] = create_api_date(LATEST_TWEET["date"])
TODAY = date.today()

# We already have latest tweet, don't do anything
if LATEST_TWEET["date"] == TODAY:
    print(f"Tweet for {TODAY} already found. Aborting...")
    raise SystemExit(0)

# Connect to the Twitter API
twitter_api = create_twitter_connection()

# Get an initial round of tweets to search
print("Searching for the latest prompt tweet")

# Get the Writer for this month and attempt to find the prompt
CURRENT_WRITER = get_writer_by_date(TODAY.strftime("%Y-%m"))
prompt_tweet = process_tweets(CURRENT_WRITER["uid"])

# The tweet was not found at all :(
if prompt_tweet is None:
    print("Search limit reached without finding prompt tweet! Aborting...")
    raise SystemExit(0)

# Construct a `date` object for the tweet
# The API returns a `datetime` object, which cannot be
# compared to a `date` object via operators
tweet_date = create_date(format_api_date_iso(prompt_tweet.created_at))

# The found tweet date is yesterday's date, indicating a
# time zone difference. Tweet datetimes are always expressed
# in UTC, so attempt to get to tomorrow's date
# and see if it matches the expected tweet date
if tweet_date < TODAY:
    next_day_hour_difference = 24 - prompt_tweet.created_at.hour
    tweet_date_tomorrow = prompt_tweet.created_at + timedelta(
        hours=next_day_hour_difference
    )
    tweet_date = create_date(tweet_date_tomorrow.strftime("%Y-%m-%d"))

# We already have the latest tweet, don't do anything
# This condition is hit when it is _technnically_ the next day
# but the newest tweet hasn't been sent out
if tweet_date == LATEST_TWEET["date"]:
    print(f"The latest tweet for {tweet_date} has already found. Aborting...")
    raise SystemExit(0)

# Pull out the tweet media and text content
media_url, tweet_media = get_tweet_media(prompt_tweet)
tweet_text = get_tweet_text(prompt_tweet, media_url)
del media_url

# Attempt to extract the prompt word and back out if we can't
prompt_word = find_prompt_word(tweet_text)
if prompt_word is None:
    print(f"Cannot find prompt word in tweet {prompt_tweet.id_str}!")
    raise SystemExit(0)

# Construct a dictionary with only the info we need
prompt = {
    "tweet_id": prompt_tweet.id_str,
    "date": format_api_date_iso(tweet_date),
    "uid": get_uid_by_handle(prompt_tweet.author.screen_name),
    "handle": escape(prompt_tweet.author.screen_name),
    "content": escape(tweet_text),
    "word": prompt_word,
    "media": tweet_media
}
pprint(prompt)


# Add the tweet to the database
try:
    print("Adding tweet to database")
    api.post("prompt", json=prompt)
except HTTPError:
    print(f"Cannot add prompt for {tweet_date} to the database!")
    raise SystemExit(0)

# Send the email notifications
print("Sending out notification emails")
send_emails(prompt)
