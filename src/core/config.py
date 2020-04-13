from json import load, dumps
from typing import Literal


__all__ = ["load_json_config", "save_json_config"]


def load_json_config() -> dict:
    """Load the app config values from file."""
    with open("config/config.json") as f:
        return load(f)


def save_json_config(config: dict) -> Literal[True]:
    with open("config/config.json", "wt") as f:
        f.write(dumps(config, indent=2))
    return True
