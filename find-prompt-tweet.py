from datetime import date
from html import escape
from pprint import pprint

import tweepy

from src.core.database import (
    add_tweet_to_db,
    get_latest_tweet,
    get_giver_by_date,
    get_uid_by_handle
)
from src.core.emails.sender import send_emails
from src.core.filters import create_date
from src.core.helpers import (
    find_prompt_tweet,
    find_prompt_word,
    load_env_vals
)


def process_tweets(uid: str, tweet_id=None, recur_count: int = 0):
    # If we recurse too many times, stop searching
    if recur_count > 7:
        return None

    # Get the latest tweets from the prompt giver
    # We need to enable extended mode to get tweets > 140 characters
    statuses = api.user_timeline(
        uid,
        max_id=tweet_id,
        count=20,
        tweet_mode="extended"
    )

    # Start by filtering out any retweets
    own_tweets = list(filter(lambda status: not status.retweeted, statuses))

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


# Get the latest tweet in the database
# to see if we need to do anything
LATEST_TWEET = get_latest_tweet(in_flask=False)
TODAY = date.today()

# We already have latest tweet, don't do anything
if LATEST_TWEET.date == TODAY:
    print(f"Tweet for {TODAY} already found. Aborting...")
    raise SystemExit(0)

# Connect to the Twitter API
CONFIG = load_env_vals()
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

# Get an initial round of tweets to search
print("Searching for the latest prompt tweet")

# Get the giver for this month and attempt to find the prompt
CURRENT_GIVER = get_giver_by_date(TODAY.strftime("%Y-%m"))
prompt_tweet = process_tweets(CURRENT_GIVER.uid)

# The tweet was not found at all :(
if prompt_tweet is None:
    print("Search limit reached without finding prompt tweet! Aborting...")
    raise SystemExit(0)

# We already have the latest tweet, don't do anything
# This condition is hit when it is _technnically_ the next day
# but the newest tweet hasn't been sent out
tweet_date = create_date(prompt_tweet.created_at.strftime("%Y-%m-%d"))
if tweet_date == LATEST_TWEET.date:
    print(f"The latest tweet for {tweet_date} has already found. Aborting...")
    raise SystemExit(0)

# Because we're accessing "extended" tweets (> 140 chars),
# we need to be sure to access the correct property
# that holds a non-truncated version of the text
tweet_text = prompt_tweet.full_text
tweet_media = None

# If we have media in our tweet, get a proper URL to it
if prompt_tweet.entities.get("media"):
    # Get the media in the tweet
    media = prompt_tweet.entities["media"]

    # Remove the media url from the tweet
    tweet_text = tweet_text.replace(media[0]["url"], "")
    tweet_media = media[0]["media_url_https"]

# Construct a dictionary with only the info we need
tweet = {
    "tweet_id": prompt_tweet.id_str,
    "date": tweet_date,
    "uid": get_uid_by_handle(
        escape(prompt_tweet.author.screen_name),
        in_flask=False
    )[0],
    "handle": escape(prompt_tweet.author.screen_name),
    "content": escape(tweet_text),
    "word": find_prompt_word(tweet_text),
    "media": tweet_media
}
pprint(tweet)

# Add the tweet to the database and send the email notifications
print("Adding tweet to database")
add_tweet_to_db(tweet)
print("Sending out notification emails")
send_emails(tweet)
