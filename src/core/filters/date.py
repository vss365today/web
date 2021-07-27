from datetime import datetime
from typing import Union


__all__ = [
    "create_datetime",
    "format_datetime_ymd",
    "format_date_pretty",
    "format_month_year",
]


def create_datetime(date_str: str) -> datetime:
    """Create a datetime object from an ISO 8601 date string."""
    return datetime.fromisoformat(date_str.strip())


def format_date_pretty(datetime_obj: Union[datetime, str]) -> str:
    """Pretty format a date in MM DD, YYYY."""
    if not isinstance(datetime_obj, datetime):
        datetime_obj = create_datetime(datetime_obj)
    return datetime_obj.strftime("%B %d, %Y")


def format_month_year(date: Union[str, datetime]) -> str:
    """Format a date as MM YYYY."""
    # If the date is provided as a string, conver it to a datetime obj
    if not isinstance(date, datetime):
        # Add in a dummy day if needed
        if len(date.split("-")) == 2:
            date = f"{date}-01"
        date = create_datetime(date)
    return date.strftime("%B %Y")


def format_datetime_ymd(datetime_obj: Union[datetime, str]) -> str:
    """Format a date as YYYY-MM-DD."""
    if not isinstance(datetime_obj, datetime):
        datetime_obj = create_datetime(datetime_obj)
    return datetime_obj.strftime("%Y-%m-%d")
