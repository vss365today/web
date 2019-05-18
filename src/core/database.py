import sqlite3
from typing import List, Union
from sqlalchemy.orm import sessionmaker

from src.models import Tweets
from src.core.helpers import create_db_connection, flatten_tuple_list, load_env_vals


__all__ = [
    "get_all_emails",
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
    conn = sqlite3.connect(config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


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
    """Get a Giver's user ID from their Twitter handle."""
    sql = "SELECT uid FROM givers WHERE handle = :handle"

    # Execute our query, returning the uid directly
    with __connect_to_db() as db:
        return db.execute(sql, {"handle": handle}).fetchone()["uid"]


def get_latest_tweet() -> dict:
    """Get the newest archived tweet."""
    # To preserve compat across the rest of the codebase,
    # we also include the tweet Giver's handle in the result set.
    sql = """
    SELECT tweets.*, givers.handle AS giver_handle
    FROM tweets
        INNER JOIN givers ON tweets.uid = givers.uid
    ORDER BY date DESC
    """

    # Execute our query
    with __connect_to_db() as db:
        return dict(db.execute(sql).fetchone())


def get_giver_by_date(date: str) -> sqlite3.Row:
    """Get a Giver by the month-year they delievered the prompts. """
    sql = "SELECT uid, handle FROM givers WHERE date = :date"

    # Execute our query
    with __connect_to_db() as db:
        return db.execute(sql, {"date": date}).fetchone()


def get_giver_by_uid(uid: str) -> sqlite3.Row:
    """Get a Giver by their user ID."""
    sql = "SELECT handle, date FROM givers WHERE uid = :uid"

    # Execute our query
    with __connect_to_db() as db:
        return db.execute(sql, {"uid": uid}).fetchone()


def get_tweet_years() -> List[str]:
    """Get a list of years of recorded tweets."""
    # We only need a descending (newest on top) list
    # of the years we've been running.
    # This is done quickly by looking at the Giver's list.
    sql = """
    SELECT DISTINCT SUBSTR(date, 1, 4)
    FROM givers
    ORDER BY date DESC
    """

    # Execute our query
    with __connect_to_db() as db:
        r = db.execute(sql).fetchall()
    return flatten_tuple_list(r)


def get_givers_by_year(year: str) -> List[sqlite3.Row]:
    """Get a list of all Givers for a particular year."""
    sql = """
    SELECT uid, handle, date || '-01' AS date
    FROM givers
    WHERE SUBSTR(date, 1, 4) = :year
    """

    # Execute our query
    with __connect_to_db() as db:
        return db.execute(sql, {"year": year}).fetchall()


def get_tweets_by_giver(handle: str) -> List[sqlite3.Row]:
    """Get all tweets given out by a Giver."""
    # Because we are querying the db using raw SQL,
    # and because the tables are _properly_ normalized,
    # we can do a simple join to get the correct data set. :D
    sql = """
    SELECT tweets.*
    FROM tweets
        INNER JOIN givers ON tweets.uid = givers.uid
    WHERE givers.handle = :handle
    """

    # Execute our query
    with __connect_to_db() as db:
        return db.execute(sql, {"handle": handle}).fetchall()


def get_tweet_by_date(date: str) -> Union[dict, None]:
    """Get a prompt tweet by the date it was posted."""
    # To preserve compat across the rest of the codebase,
    # we also include the tweet Giver's handle in the result set.
    sql = """
    SELECT tweets.*, givers.handle AS giver_handle
    FROM tweets
        INNER JOIN givers ON tweets.uid = givers.uid
    WHERE tweets.date = :date
    """

    # Execute our query
    with __connect_to_db() as db:
        r = db.execute(sql, {"date": date}).fetchone()
    return dict(r) if r is not None else None


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
