from json import dumps

import tweepy
from requests import post

from src.core.filters import create_proper_image_url
from src.core.helpers import find_prompt_tweet, load_env_vals
# from src.core.emails.sender import send_emails


class StreamListener(tweepy.StreamListener):
    """Based on https://www.dataquest.io/blog/streaming-data-python/"""
    def on_status(self, status):
        # Take out retweets
        if status.retweeted:
            return False

        # Don't do anything if this isn't the prompt tweet
        if not find_prompt_tweet(status.author.screen_name, status.text):
            return False

        # If we have media in our tweet, get a proper URL to it
        tweet_text = status.text
        if status.entities.get("media"):
            media = status.entities["media"]
            tweet_text = create_proper_image_url(
                tweet_text,
                media[0]["url"], media[0]["media_url_https"]
            )

        # Rewrite the date format for proper database addition
        tweet_date = [
            int(d)
            for d in status.created_at.strftime("%Y-%m-%d").split("-")
        ]

        # Construct a dictionary with only the info we need
        tweet = dumps({
            "date": tweet_date,
            "user_handle": f"{status.author.screen_name}",
            "content": tweet_text,
            "url": "https://twitter.com/{}/status/{}".format(
                status.author.screen_name, status.id_str
            )
        })

        # Add the tweet to the database
        post("http://127.0.0.1:5000/api/add", json=tweet)

        # TODO Kick off the emails
        # send_emails(tweet)

    def on_error(self, status_code):
        if status_code == 420:  # blaze it
            return False


# Connect to the Twitter api
config = load_env_vals()
auth = tweepy.OAuthHandler(
    config["TWITTER_APP_KEY"],
    config["TWITTER_APP_SECRET"]
)
auth.set_access_token(
    config["TWITTER_KEY"],
    config["TWITTER_SECRET"]
)
__api = tweepy.API(auth)
print("Successfully connected to Twitter API")

# Use the streaming api to listen for the prompt tweet
stream_listener = StreamListener()
stream = tweepy.Stream(auth=__api.auth, listener=stream_listener)
# TODO I don't like having to hard-code the user IDs,
# much less update this code monthly
# http://gettwitterid.com/?user_name=SalnPage&submit=GET+USER+ID
print("Listening for tweet...")
stream.filter(follow=["227230837"])
