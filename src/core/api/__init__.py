from typing import Any

import sys_vars

from src.core.api import _api


__all__ = ["delete", "get", "post", "put"]


def __create_api_url(*args: str) -> str:
    """Construct a URL to the given v1 API endpoint."""
    endpoint = "/".join(args)
    return f"{sys_vars.get('API_DOMAIN')}/v1/{endpoint}"


def delete(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a DELETE request."""
    url = __create_api_url(*args)
    return _api.delete(url, **kwargs)


def get(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a GET request."""
    url = __create_api_url(*args)
    return _api.get(url, **kwargs)


def post(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a POST request."""
    url = __create_api_url(*args)
    return _api.post(url, **kwargs)


def put(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a PUT request."""
    url = __create_api_url(*args)
    return _api.put(url, **kwargs)
