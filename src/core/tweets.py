from src.models import Tweets


def get_latest_word():
    return Tweets.query.order_by(Tweets.date.desc()).first()


def get_word_by_date(date):
    return Tweets.query.filter(Tweets.date.startswith(date)).first_or_404()

