from datetime import date, datetime


__all__ = [
    "create_datetime",
    "format_datetime_ymd",
    "format_date_pretty",
    "format_month_year",
]


def create_datetime(date_str: str) -> datetime:
    """Create a datetime object from an ISO 8601 date string."""
    return datetime.fromisoformat(date_str.strip())


def format_date_pretty(obj: date | datetime | str) -> str:
    """Pretty format a date in MM DD, YYYY."""
    if isinstance(obj, str):
        obj = date.fromisoformat(obj.strip())
    return obj.strftime("%B %d, %Y")


def format_month_year(obj: date | datetime | str) -> str:
    """Format a date as MM YYYY."""
    # If the date is provided as a string, convert it to a datetime obj
    if isinstance(obj, str):
        # Add in a dummy day if needed
        if len(obj.split("-")) == 2:
            obj = f"{obj}-01"
        obj = date.fromisoformat(obj.strip())
    return obj.strftime("%B %Y")


def format_datetime_ymd(obj: date | datetime | str) -> str:
    """Format a date as YYYY-MM-DD."""
    if isinstance(obj, str):
        obj = date.fromisoformat(obj.strip())
    return obj.isoformat()
