from sqlalchemy.orm import sessionmaker

from src.models import Emails, Tweets, Givers
from src.core.helpers import create_db_connection, load_env_vals


__all__ = [
    "add_tweet_to_db",
    "get_all_emails",
    "get_latest_tweet",
    "get_tweet_by_date"
]


def __connect_to_db_sqlalchemy():
    # Connect to the database
    config = load_env_vals()
    _, db = create_db_connection(config)

    # Make a database session
    Session = sessionmaker(bind=db)
    return Session()


def get_all_emails() -> list:
    # Get all the emails
    session = __connect_to_db_sqlalchemy()
    all_emails = session.query(Emails).all()
    session.close()
    return all_emails


def get_uid_by_handle(handle: str):
    session = __connect_to_db_sqlalchemy()
    uid = session.query(Givers.uid).filter_by(handle=handle).first()
    session.close()
    return uid


def get_latest_tweet():
    return Tweets.query.order_by(Tweets.date.desc()).first_or_404()


def get_tweet_by_date(date: str):
    return Tweets.query.filter(Tweets.date.startswith(date)).first_or_404()


def add_giver_to_db(giver_dict: dict):
    """Add a giver to the database."""
    giver = Givers(
        uid=giver_dict["uid"],
        handle=giver_dict["handle"]
    )
    session = __connect_to_db_sqlalchemy()
    session.add(giver)
    session.commit()
    session.close()


def add_tweet_to_db(tweet: dict):
    """Add a tweet to the database."""
    word = Tweets(
        tweet_id=tweet["tweet_id"],
        date=tweet["date"],
        uid=tweet["uid"],
        content=tweet["content"],
        word=tweet["word"]
    )
    session = __connect_to_db_sqlalchemy()
    session.add(word)
    session.commit()
    session.close()
