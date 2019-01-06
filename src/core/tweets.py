import datetime
import re

from src.extensions import alchemy
from src.models import Tweets


def find_image(content):
    regex = re.compile(r"https://.+\.(?:jpg|png|gif)", re.MULTILINE)
    match = re.search(regex, content)
    if match:
        url = match.group(0)
        content = content.replace(url, f'<img width="500" src="{url}">')
    return content


def format_tweet(tweet):
    # Format the tweet content, attempting to display any images
    tweet.content = "\n".join([
        f"<p>{find_image(para)}</p>"
        for para in tweet.content.split("\r\n")
        if para
    ])
    return tweet


def get_tweet_today():
    return Tweets.query.order_by(Tweets.date.desc()).first()

def get_tweet_by_date(date):
    return Tweets.query.filter(Tweets.date.startswith(date)).first_or_404()
