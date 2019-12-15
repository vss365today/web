from html import escape
from pprint import pprint
from re import match

from src.core import api
from src.core.database import get_uid_by_handle
from src.core.emails.sender import send_emails
from src.core.filters import create_date
from src.core.helpers import (
    create_twitter_connection,
    find_prompt_word,
    get_tweet_media,
    get_tweet_text
)


def extract_handle(url: str) -> str:
    return match(
        r"^https://(?:mobile\.|www\.)?twitter\.com/(\w+)/status",
        url
    )[1].strip()


def extract_tweet_id(url: str) -> str:
    return match(
        r"^https://(?:mobile\.|www\.)?twitter\.com/\w+/status/(\d+)",
        url
    )[1]


# Connect to the Twitter API
twitter_api = create_twitter_connection()

# Keep prompting for tweets until told to stop
while True:
    # Get the base information we need from the user to start
    tweet_date = input("Enter the tweet date (YYYY-MM-DD): ")

    # Stop adding prompts
    if tweet_date.lower() == "exit":
        raise SystemExit(0)

    tweet_url = input("Enter the tweet url: ")
    tweet_id = extract_tweet_id(tweet_url)
    user_handle = extract_handle(tweet_url)

    # We're assuming/trusting the url is to the prompt tweet
    # so we'll skip the validity checks
    prompt_tweet = twitter_api.get_status(tweet_id, tweet_mode="extended")

    # Extract the tweet content
    media_url, tweet_media = get_tweet_media(prompt_tweet)
    tweet_text = get_tweet_text(prompt_tweet, media_url)
    del media_url

    # Construct a tweet object
    prompt = {
        "tweet_id": tweet_id,
        "date": create_date(tweet_date.strip()),
        "uid": get_uid_by_handle(user_handle),
        "handle": user_handle,
        "content": escape(tweet_text),
        "word": find_prompt_word(tweet_text),
        "media": tweet_media
    }
    pprint(prompt)

    # Add the prompt to the database and send the emails
    print("Adding prompt to database")
    api.post("prompt", json=prompt)
    print("Sending out notification emails")
    send_emails(prompt)
