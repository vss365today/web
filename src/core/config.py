from json import load, dumps
from typing import Literal

from dotenv import dotenv_values, find_dotenv

__all__ = [
    "load_app_config",
    "load_json_config",
    "save_json_config"
]


def load_app_config() -> dict:
    """Load the env variables from file."""
    vals = {}
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        vals[key] = (value if value != "" else None)
    return vals


def load_json_config() -> dict:
    """Load the app config values from file."""
    with open("config/config.json") as f:
        return load(f)


def save_json_config(config: dict) -> Literal[True]:
    with open("config/config.json", "wt") as f:
        f.write(dumps(config, indent=2))
    return True
