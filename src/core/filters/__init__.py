from src.core.filters.date import (
    format_date_pretty,
    format_month_year,
)
from src.core.helpers import format_content

# Define the filters we want to export
ALL_FILTERS = {
    "format_content": format_content,
    "format_date_pretty": format_date_pretty,
    "format_month_year": format_month_year,
}
