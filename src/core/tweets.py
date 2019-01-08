from src.extensions import alchemy
from src.models import Tweets


__all__ = ["add_word_to_db", "get_latest_word", "get_word_by_date"]


def get_latest_word():
    return Tweets.query.order_by(Tweets.date.desc()).first()


def get_word_by_date(date):
    return Tweets.query.filter(Tweets.date.startswith(date)).first_or_404()


def add_word_to_db(tweet: dict):
    """Add a word to the database."""
    word = Tweets(
        date=tweet.date,
        user_handle=tweet.user_handle,
        url=tweet.url,
        content=tweet.content
    )
    alchemy.session.add(word)
    alchemy.session.commit()
