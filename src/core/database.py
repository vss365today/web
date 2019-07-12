import os.path
import sqlite3
from typing import List, Union

from src.core.config import load_app_config


__all__ = [
    "add_subscribe_email",
    "add_tweet_to_db",
    "create_new_database",
    "get_all_emails",
    "get_existing_email",
    "get_latest_tweet",
    "get_writer_by_date",
    "get_writers_by_year",
    "get_tweet_by_date",
    "get_tweet_years",
    "get_uid_by_handle",
    "get_words_by_month",
    "get_writer_tweets_by_year",
    "remove_subscribe_email"
]


def __connect_to_db() -> sqlite3.Connection:
    """Create a connection to the database."""
    config = load_app_config()
    conn = sqlite3.connect(config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


def __flatten_tuple_list(tup) -> list:
    """Flatten a list of tuples into a list of actual data."""
    return [item[0] for item in tup]


def add_subscribe_email(addr: str) -> bool:
    """Add a subscription email address."""
    try:
        sql = "INSERT INTO emails VALUES (:addr)"
        with __connect_to_db() as db:
            db.execute(sql, {"addr": addr})
        return True

    # Some error occurred
    except Exception as err:
        print(err)
        return False


def create_new_database() -> None:
    """Create a new database if needed."""
    try:
        # If the database exists and is loaded, this will succeed
        sql = "SELECT COUNT(*) FROM writers"
        with __connect_to_db() as db:
            db.execute(sql)

    # The database doesn't exist
    except sqlite3.OperationalError:
        # Get the db schema
        schema = os.path.abspath(
            os.path.join("db", "schema.sql")
        )
        with open(schema, "rt") as f:
            sql = f.read()

        # Create the database according to the schema
        db.executescript(sql)


def get_all_emails() -> List[str]:
    """Get all emails in the subscription list."""
    sql = "SELECT email FROM emails"
    with __connect_to_db() as db:
        r = db.execute(sql).fetchall()

    # Flatten the list of tuples into a list
    # of strings containing just the email addresses
    return __flatten_tuple_list(r)


def get_existing_email(addr: str) -> bool:
    """Find an existing subscription email."""
    sql = "SELECT 1 FROM emails WHERE email = :addr"
    with __connect_to_db() as db:
        return bool(db.execute(sql, {"addr": addr}).fetchone())


def get_uid_by_handle(handle: str) -> str:
    """Get a Writer's user ID from their Twitter handle."""
    sql = "SELECT uid FROM writers WHERE handle = :handle"

    # Execute our query, returning the uid directly
    with __connect_to_db() as db:
        return db.execute(sql, {"handle": handle}).fetchone()["uid"]


def get_latest_tweet() -> Union[dict, None]:
    """Get the newest archived tweet."""
    # To preserve compat across the rest of the codebase,
    # we also include the tweet Writer's handle in the result set.
    sql = """
    SELECT tweets.*, writers.handle AS writer_handle
    FROM tweets
        JOIN writers ON tweets.uid = writers.uid
    ORDER BY date DESC
    LIMIT 1
    """
    with __connect_to_db() as db:
        r = db.execute(sql).fetchone()
        return dict(r) if r else r


def get_writer_by_date(date: str) -> sqlite3.Row:
    """Get a Writer by the month-year they delievered the prompts. """
    sql = """
    SELECT writers.uid, handle
    FROM writers
        JOIN writer_dates ON writer_dates.uid = writers.uid
    WHERE writer_dates.date = :date
    """
    with __connect_to_db() as db:
        return db.execute(sql, {"date": date}).fetchone()


def get_tweet_years() -> List[str]:
    """Get a list of years of recorded tweets."""
    sql = """
    SELECT DISTINCT SUBSTR(date, 1, 4)
    FROM writer_dates
    ORDER BY date ASC
    """
    with __connect_to_db() as db:
        r = db.execute(sql).fetchall()
    return __flatten_tuple_list(r)


def get_writers_by_year(year: str) -> List[sqlite3.Row]:
    """Get a list of all Writers for a particular year."""
    sql = """
    SELECT writers.uid, handle, writer_dates.date || '-01' AS date
    FROM writers
        JOIN writer_dates ON writer_dates.uid = writers.uid
    WHERE SUBSTR(date, 1, 4) = :year
        AND SUBSTR(date, 1, 8) <= strftime('%Y-%m','now')
    ORDER BY writer_dates.date ASC
    """
    with __connect_to_db() as db:
        return db.execute(sql, {"year": year}).fetchall()


def get_writer_tweets_by_date(handle: str, date: str) -> List[sqlite3.Row]:
    """Get all tweets from a Writer in a given date range."""
    sql = """
    SELECT tweets.*
    FROM tweets
        JOIN writers ON tweets.uid = writers.uid
    WHERE writers.handle = :handle
        AND tweets.date <= date('now')
        AND SUBSTR(tweets.date, 1, 7) = :date
    ORDER BY tweets.date ASC
    """
    with __connect_to_db() as db:
        return db.execute(sql, {"date": date, "handle": handle}).fetchall()


def get_tweet_by_date(date: str) -> Optional[dict]:
    """Get a prompt tweet by the date it was posted."""
    sql = """
    SELECT tweets.*, writers.handle AS writer_handle
    FROM tweets
        JOIN writers ON writers.uid = tweets.uid
    WHERE tweets.date = :date
    """
    with __connect_to_db() as db:
        r = db.execute(sql, {"date": date}).fetchone()
    return dict(r) if r is not None else None


def add_tweet_to_db(tweet_dict: dict) -> None:
    """Add a tweet to the database."""
    sql = """
    INSERT INTO tweets (
        tweet_id, date, uid, content, word, media
    )
    VALUES (
        :tweet_id, :date, :uid, :content, :word, :media
    )
    """
    with __connect_to_db() as db:
        db.execute(sql, tweet_dict)


def get_words_by_month(date: str) -> list:
    """Get a list of words for the given month."""
    sql = """
    SELECT '#' || word
    FROM tweets
    WHERE SUBSTR(date, 1, 7) = :date
    """

    with __connect_to_db() as db:
        r = db.execute(sql, {"date": date}).fetchall()
    return __flatten_tuple_list(r)


def remove_subscribe_email(addr: str) -> True:
    """Remove a subscription email address."""
    sql = "DELETE FROM emails WHERE email = :addr"
    with __connect_to_db() as db:
        db.execute(sql, {"addr": addr})
    return True
