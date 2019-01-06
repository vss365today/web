from src.models import Tweets


def get_tweet_today():
    # TODO: Possibly just call get_tweet_by_date()
    return Tweets.query.order_by(Tweets.date.desc()).first()


def get_tweet_by_date(date):
    # TODO: Is first_or_404() still creating an error with a favicon?
    return Tweets.query.filter(Tweets.date.startswith(date)).first_or_404()
    # return Tweets.query.filter(Tweets.date.startswith(date)).first()
