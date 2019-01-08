import tweepy

from filters import create_proper_image_url
from helpers import load_env_vals
from tweets import add_word_to_db


__all__ = ["Listener"]


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Take out retweets
        if status.retweeted_status:
            return False

        # If we have media in our tweet, get a proper URL to it
        tweet_text = status.tweet_text
        if status.entities.media:
            media = status.entities.media
            tweet_text = create_proper_image_url(
                tweet_text,
                media.url, media.media_url_https
            )

        # Construct a dictionary with just the info we need
        tweet = {
            "date": status.created,
            "user_handle": f"@{status.user_name}",
            "content": tweet_text,
            "url": "https://twitter.com/{}/status/{}".format(
                status.user_name, status.id_str
            )
        }

        # Add the tweet to the database
        add_word_to_db(tweet)

        # TODO Kick off the email
        return True

    def on_error(self, status_code):
        if status_code == 420:  # blaze it
            return False


class Listener:
    """@link {https://www.dataquest.io/blog/streaming-data-python/}"""
    def __init__(self):
        self.__api = None

        # Get the app settings for the Twitter secret keys
        config = load_env_vals()
        auth = tweepy.OAuthHandler(
            config["TWITTER_APP_KEY"],
            config["TWITTER_APP_SECRET"]
        )
        auth.set_access_token(
            config["TWITTER_KEY"],
            config["TWITTER_SECRET"]
        )
        self.__api = tweepy.API(auth)

    def start(self):
        stream_listener = StreamListener()
        stream = tweepy.Stream(auth=self.__api.auth, listener=stream_listener)
        # TODO I don't like having to hard-code the user IDs
        # http://gettwitterid.com/?user_name=SalnPage&submit=GET+USER+ID
        stream.filter(follow=["227230837"], track=["#vss365", "#prompt"])


# Start the scraper if we are running the script directly
if __name__ == "__main__":
    listener = Listener()
    listener.start()
