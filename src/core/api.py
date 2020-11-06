from typing import Any, Union

import requests
import sys_vars


__all__ = ["get", "post", "put", "delete"]


def __create_api_url(*args: str) -> str:
    """Construct a URL to the given API endpoint."""
    endpoint = "/".join(args)
    return f"{sys_vars.get('API_DOMAIN')}/{endpoint}/"


def __create_auth_token() -> dict:
    """Create HTTP header for accessing protected API endpoints."""
    return {"Authorization": f"Bearer {sys_vars.get('API_AUTH_TOKEN')}"}


def get(*args: str, **kwargs: Any) -> Union[list, dict]:
    """Helper function for performing a GET request."""
    kwargs["headers"] = __create_auth_token()
    url = __create_api_url(*args)
    r = requests.get(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}


def post(*args: str, **kwargs: Any) -> Union[list, dict]:
    """Helper function for performing a POST request."""
    kwargs["headers"] = __create_auth_token()
    url = __create_api_url(*args)
    r = requests.post(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}


def put(*args: str, **kwargs: Any) -> Union[list, dict]:
    """Helper function for performing a PUT request."""
    kwargs["headers"] = __create_auth_token()
    url = __create_api_url(*args)
    r = requests.put(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}


def delete(*args: str, **kwargs: Any) -> Union[list, dict]:
    """Helper function for performing a DELETE request."""
    kwargs["headers"] = __create_auth_token()
    url = __create_api_url(*args)
    r = requests.delete(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}
