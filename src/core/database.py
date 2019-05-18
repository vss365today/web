import sqlite3
from typing import Dict, List
from sqlalchemy.orm import sessionmaker

from src.models import Tweets, Givers
from src.core.helpers import create_db_connection, flatten_tuple_list, load_env_vals


__all__ = [
    "get_all_emails",
    "add_giver_to_db",
    "add_tweet_to_db",
    "get_latest_tweet",
    "get_giver_by_date",
    "get_giver_by_uid",
    "get_givers_by_year",
    "get_tweet_by_date",
    "get_tweets_by_giver",
    "get_tweet_years",
    "get_uid_by_handle"
]


def __connect_to_db_sqlalchemy():
    # Connect to the database
    config = load_env_vals()
    _, db = create_db_connection(config)

    # Make a database session
    Session = sessionmaker(bind=db)
    return Session()


def __connect_to_db() -> sqlite3.Connection:
    """Create a connection to the database."""
    config = load_env_vals()
    return sqlite3.connect(config["DB_PATH"])


def get_all_emails() -> List[str]:
    """Get all emails in the subscription list."""
    sql = "SELECT email FROM emails"

    # Execute our query
    with __connect_to_db() as db:
        r = db.execute(sql).fetchall()

    # Flatten the list of tuples into a list
    # of strings containing just the email addresses
    return flatten_tuple_list(r)


def get_uid_by_handle(handle: str) -> str:
    """Get a giver's user ID from their Twitter handle."""
    sql = "SELECT uid FROM givers WHERE handle = :handle"

    # Execute our query
    with __connect_to_db() as db:
        return db.execute(sql, {"handle": handle}).fetchone()[0]


def get_latest_tweet(in_flask: bool = True):
    # Use the appropriate database api depending on
    # if we are inside a Flask context or not
    if in_flask:
        return Tweets.query.order_by(Tweets.date.desc()).first_or_404()
    else:
        session = __connect_to_db_sqlalchemy()
        tweet = session.query(Tweets).order_by(Tweets.date.desc()).first()
        session.close()
        return tweet


def get_giver_by_date(date: str) -> Dict[str, str]:
    """Get a Giver by the month-year they delievered the prompts. """
    sql = "SELECT uid, handle, date FROM givers WHERE date = :date"

    # Execute our query
    with __connect_to_db() as db:
        r = db.execute(sql, {"date": date}).fetchone()

    # Create a dictionary from the giver's info
    # for easier consumption
    giver = {
        "uid": r[0],
        "handle": r[1],
        "date": r[2],
    }
    return giver


def get_giver_by_uid(uid: str):
    """"Only works outside Flask context."""
    session = __connect_to_db_sqlalchemy()
    giver = session.query(Givers).filter_by(uid=uid).first()
    session.close()
    return giver


def get_tweet_years() -> List[str]:
    """Get a list of years of recorded tweets."""
    # We only need a descending (newest on top) list
    # of the years we've been running.
    # This is done quickly by looking at the prompters list.
    sql = """
    SELECT
        DISTINCT SUBSTR(date, 1, 4)
    FROM
        givers
    ORDER BY
        date DESC
    """

    # Execute our query
    with __connect_to_db() as db:
        r = db.execute(sql).fetchall()
    return flatten_tuple_list(r)


def get_givers_by_year(year: str):
    return Givers.query.filter(Givers.date.startswith(year)).all()


def get_tweets_by_giver(handle: str) -> List[dict]:
    """Get all tweets given out by a Giver."""
    # Because we are querying the db using raw SQL,
    # and because the tables are _properly_ normalized,
    # we can do a simple join to get the correct data set. :D
    sql = """
    SELECT
        tweets.*
    FROM
        tweets
    INNER JOIN
        givers ON tweets.uid = givers.uid
    WHERE
        givers.handle = :handle
    """

    # Execute our query
    with __connect_to_db() as db:
        r = db.execute(sql, {"handle": handle}).fetchall()

    # Convert the results into a dict for easier consumption
    tweets = [
        {
            "tweet_id": tweet[0],
            "date": tweet[1],
            "uid": tweet[2],
            "content": tweet[3],
            "word": tweet[4],
            "media": tweet[4]
        }
        for tweet in r
    ]
    return tweets


def get_tweet_by_date(date: str, in_flask: bool = True):
    if in_flask:
        return Tweets.query.filter(Tweets.date == date).first()
    else:
        session = __connect_to_db_sqlalchemy()
        tweet = session.query(Tweets).filter_by(date=date).first()
        session.close()
        return tweet


def add_giver_to_db(giver_dict: dict):
    """Add a giver to the database."""
    giver = Givers(
        uid=giver_dict["uid"],
        handle=giver_dict["handle"],
        date=giver_dict["date"]
    )
    session = __connect_to_db_sqlalchemy()
    session.add(giver)
    session.commit()
    session.close()


def add_tweet_to_db(tweet_dict: dict):
    """Add a tweet to the database."""
    tweet = Tweets(
        tweet_id=tweet_dict["tweet_id"],
        date=tweet_dict["date"],
        uid=tweet_dict["uid"],
        content=tweet_dict["content"],
        word=tweet_dict["word"],
        media=tweet_dict["media"]
    )
    session = __connect_to_db_sqlalchemy()
    session.add(tweet)
    session.commit()
    session.close()
