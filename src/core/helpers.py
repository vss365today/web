from os.path import abspath

from dotenv import dotenv_values, find_dotenv
from sqlalchemy import create_engine


def create_db_connection(config):
    connect_str = f"sqlite:///{abspath(config['DB_PATH'])}"
    return connect_str, create_engine(connect_str)


def find_prompt_tweet(handle: str, text: str) -> bool:
    # TODO Don't hard code the handle
    return handle == "SalnPage" and all(
        hashtag in text.upper()
        for hashtag in ("#VSS365", "#PROMPT")
    )


def load_env_vals():
    # Load the variables from the .env file
    vals = {}
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        vals[key] = (value if value != "" else None)
    return vals
