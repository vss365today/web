from datetime import date
from html import escape
from pprint import pprint
from urllib.parse import quote

import tweepy

from src.core.database import (
    add_tweet_to_db,
    get_latest_tweet,
    get_uid_by_handle
)
from src.core.emails.sender import send_emails
from src.core.filters import (
    create_date,
    find_prompt_word
)
from src.core.helpers import (
    find_prompt_tweet,
    load_env_vals
)


def process_tweets(uid: str, tweet_id=None, recur_count: int = 0):
    # If we recurse too many times, stop searching
    if recur_count > 7:
        return None

    # Get the latest tweets from the prompt giver
    statuses = api.user_timeline(uid, max_id=tweet_id, count=20)

    # Start by filtering out any retweets
    own_tweets = list(filter(lambda status: not status.retweeted, statuses))

    prompt_tweet = None
    for tweet in own_tweets:
        # Try to find the prompt tweet among the pulled tweets
        if find_prompt_tweet(tweet.text):
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
latest_tweet = get_latest_tweet(in_flask=False)
today = date.today()

# We already have latest tweet, don't do anything
if latest_tweet.date == today:
    print(f"Tweet for {today} already found. Aborting...")
    raise SystemExit(0)

# Connect to the Twitter API
config = load_env_vals()
auth = tweepy.OAuthHandler(
    config["TWITTER_APP_KEY"],
    config["TWITTER_APP_SECRET"]
)
auth.set_access_token(
    config["TWITTER_KEY"],
    config["TWITTER_SECRET"]
)
api = tweepy.API(auth)
print("Successfully connected to the Twitter API")

# Get an initial round of tweets to search
# TODO: Don't hard-code the uid
print("Searching for the latest prompt tweet")
prompt_tweet = process_tweets("936441426954653697")  # ArthurUnkTweets

# The tweet was not found at all :(
if prompt_tweet is None:
    print("Search limit reached without finding prompt tweet! Aborting...")
    raise SystemExit(0)

# We already have the latest tweet, don't do anything
# This condition is hit when it is _technnically_ the next day
# but the newest tweet hasn't been sent out
tweet_date = create_date(prompt_tweet.created_at.strftime("%Y-%m-%d"))
if tweet_date == latest_tweet.date:
    print(f"The latest tweet for {tweet_date} has already found. Aborting...")
    raise SystemExit(0)

# TODO: .text keeps getting truncated data
tweet_text = prompt_tweet.text
tweet_media = None

# This tweet was posted with TweetDeck,
# which changes the API response
# TODO: See if something can be done to handle this
# Might have to dl page the parse the image out (see: bs4)
if prompt_tweet.source == "TweetDeck":
    pass

# This tweet was not posted with TweetDeck
# If we have media in our tweet, get a proper URL to it
elif prompt_tweet.entities.get("media"):
    # Get the media in the tweet
    media = prompt_tweet.entities["media"]

    # Remove the media url from the tweet
    tweet_text = tweet_text.replace(media[0]["url"], "")
    tweet_media = quote(media[0]["media_url_https"])

# Construct a dictionary with only the info we need
tweet = {
    "tweet_id": quote(prompt_tweet.id_str),
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
