from json import loads, dumps
from pathlib import Path
from typing import Literal


__all__ = ["load_json_config", "save_json_config"]


def load_json_config() -> dict:
    """Load the app config values from file."""
    return loads((Path("config") / "config.json").read_text())


def save_json_config(config: dict) -> Literal[True]:
    with open("config/config.json", "wt") as f:
        f.write(dumps(config, indent=2))
    return True
