from typing import Any

import requests

from src.core.config import load_app_config

__all__ = ["get", "post", "put", "delete"]


CONFIG = load_app_config()


def __create_api_url(*args: str) -> str:
    """Construct a URL to the given API endpoint."""
    endpoint = "/".join(args)
    return f"{CONFIG['API_DOMAIN']}/{endpoint}/"


def get(*args: str, **kwargs: Any) -> Any:
    url = __create_api_url(*args)
    r = requests.get(url, **kwargs)
    r.raise_for_status()
    return r.json()


def post(*args: str, **kwargs: Any) -> Any:
    url = __create_api_url(*args)
    r = requests.post(url, **kwargs)
    r.raise_for_status()
    return r.json()


def put(*args: str, **kwargs: Any) -> Any:
    url = __create_api_url(*args)
    r = requests.put(url, **kwargs)
    r.raise_for_status()
    return r.json()


def delete(*args: str, **kwargs: Any) -> Any:
    url = __create_api_url(*args)
    r = requests.delete(url, **kwargs)
    r.raise_for_status()
    return r.json()
