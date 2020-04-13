from typing import Any, Dict, Union

import jwt
import requests

from src.core.config import load_app_config

__all__ = ["create_auth_token", "get", "post", "put", "delete"]


CONFIG = load_app_config()


def __create_api_url(*args: str) -> str:
    """Construct a URL to the given API endpoint."""
    endpoint = "/".join(args)
    return f"{CONFIG['API_DOMAIN']}/{endpoint}/"


def create_auth_token(payload: Dict[str, Any]) -> dict:
    token = jwt.encode(payload, CONFIG["JWT_SECRET_KEY"], algorithm="HS256")
    return {"Authorization": b"Bearer " + token}


def get(*args: str, **kwargs: Any) -> Union[list, dict]:
    url = __create_api_url(*args)
    r = requests.get(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}


def post(*args: str, **kwargs: Any) -> Union[list, dict]:
    url = __create_api_url(*args)
    r = requests.post(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}


def put(*args: str, **kwargs: Any) -> Union[list, dict]:
    url = __create_api_url(*args)
    r = requests.put(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}


def delete(*args: str, **kwargs: Any) -> Union[list, dict]:
    url = __create_api_url(*args)
    r = requests.delete(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}
