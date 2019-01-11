from sqlalchemy.orm import sessionmaker

from src.extensions import alchemy
from src.models import Emails, Tweets
from src.core.helpers import create_db_connection, load_env_vals
from src.core.filters import create_date


__all__ = [
    "add_word_to_db",
    "get_all_emails",
    "get_latest_word",
    "get_word_by_date"
]


def get_all_emails():
    # Connect to the database
    config = load_env_vals()
    _, db = create_db_connection(config)

    # Make a database session
    Session = sessionmaker(bind=db)
    session = Session()

    # Get all the emails
    return session.query(Emails).all()


def get_latest_word():
    return Tweets.query.order_by(Tweets.date.desc()).first()


def get_word_by_date(date):
    return Tweets.query.filter(Tweets.date.startswith(date)).first_or_404()


def add_word_to_db(tweet: dict):
    """Add a word to the database."""
    word = Tweets(
        date=create_date(tweet["date"]),
        user_handle=tweet["user_handle"],
        url=tweet["url"],
        content=tweet["content"]
    )
    alchemy.session.add(word)
    alchemy.session.commit()
