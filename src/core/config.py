from dotenv import dotenv_values, find_dotenv

__all__ = [
    "load_app_config"
]


def load_app_config() -> dict:
    """Load the env variables from file."""
    vals = {}
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        vals[key] = (value if value != "" else None)
    return vals
