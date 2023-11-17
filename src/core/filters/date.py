from datetime import date

__all__ = ["format_date_pretty", "format_month_year"]


def format_date_pretty(obj: date | str) -> str:
    """Pretty format a date in MM DD, YYYY."""
    if isinstance(obj, str):
        obj = date.fromisoformat(obj.strip())
    return obj.strftime("%B %d, %Y")


def format_month_year(obj: date | str) -> str:
    """Format a date as MM YYYY."""
    # If the date is provided as a string, convert it to a datetime obj
    if isinstance(obj, str):
        # Add in a dummy day if needed
        if len(obj.split("-")) == 2:
            obj = f"{obj}-01"
        obj = date.fromisoformat(obj.strip())
    return obj.strftime("%B %Y")
