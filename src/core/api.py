from typing import Any, Callable

import requests
import sys_vars


__all__ = ["delete", "get", "post", "put"]


def __create_api_url(*args: str) -> str:
    """Construct a URL to the given API endpoint."""
    endpoint = "/".join(args)
    return f"{sys_vars.get('API_DOMAIN')}/{endpoint}"


def __create_auth_token() -> dict:
    """Create HTTP header for accessing protected API endpoints."""
    return {"Authorization": f"Bearer {sys_vars.get('API_AUTH_TOKEN')}"}


def __make_request(method: Callable, *args: str, **kwargs: Any) -> dict:
    """Make a request to the API."""
    kwargs["headers"] = __create_auth_token()
    url = __create_api_url(*args)
    r = method(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}


def delete(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a DELETE request."""
    return __make_request(requests.delete, *args, **kwargs)


def get(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a GET request."""
    return __make_request(requests.get, *args, **kwargs)


def post(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a POST request."""
    return __make_request(requests.post, *args, **kwargs)


def put(*args: str, **kwargs: Any) -> dict:
    """Helper function for performing a PUT request."""
    return __make_request(requests.put, *args, **kwargs)
