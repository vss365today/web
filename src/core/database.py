import sqlite3
from typing import Dict

from src.core.config import load_app_config


__all__ = [
    "add_tweet_to_db",
    "get_mailing_list",
    "get_latest_tweet",
    "get_writer_by_date",
    "get_uid_by_handle",
    "get_words_by_month"
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


def get_mailing_list() -> Dict[str, str]:
    """Get all emails in the subscription list."""
    sql = "SELECT email, hash FROM emails"
    with __connect_to_db() as db:
        r = db.execute(sql).fetchall()
    return {
        email: hash_val
        for email, hash_val in r
    }


def get_uid_by_handle(handle: str) -> str:
    """Get a Writer's user ID from their Twitter handle."""
    sql = "SELECT uid FROM writers WHERE handle = :handle"

    # Execute our query, returning the uid directly
    with __connect_to_db() as db:
        return db.execute(sql, {"handle": handle}).fetchone()["uid"]


def get_latest_tweet() -> dict:
    """Get the newest tweet."""
    sql = """
    SELECT tweets.*, writers.handle AS writer_handle
    FROM tweets
        JOIN writers ON tweets.uid = writers.uid
    ORDER BY date DESC
    LIMIT 1
    """
    with __connect_to_db() as db:
        return dict(db.execute(sql).fetchone())


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
