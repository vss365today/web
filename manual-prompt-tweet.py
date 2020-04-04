from html import escape
from pprint import pprint
from re import match

from requests.exceptions import HTTPError

from src.core import api
from src.core.filters import create_datetime
from src.core.helpers import (
    create_twitter_connection,
    find_prompt_word,
    get_tweet_media,
    get_tweet_text,
)


def extract_handle(url: str) -> str:
    regex = r"^https://(?:mobile\.|www\.)?twitter\.com/(\w+)/status"
    m = match(regex, url)[1].strip()
    return m


def extract_tweet_id(url: str) -> str:
    regex = r"^https://(?:mobile\.|www\.)?twitter\.com/\w+/status/(\d+)"
    m = match(regex, url)[1].strip()
    return m


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
        "id": tweet_id,
        "date": str(prompt_tweet.created_at),
        "uid": prompt_tweet.author.id_str,
        "handle": user_handle,
        "content": escape(tweet_text),
        "word": find_prompt_word(tweet_text),
        "media": tweet_media,
    }
    pprint(prompt)

    try:
        # Add the tweet to the database
        print("Adding tweet to database")
        api.post("prompt", json=prompt)

        # Send the email broadcast
        print("Sending out notification emails")
        api.post(
            "subscription", "broadcast", params={"date": create_datetime(tweet_date)}
        )

    except HTTPError:
        print(f"Cannot add prompt for {tweet_date} to the database!")
        raise SystemExit(0)
