from requests.exceptions import HTTPError

from src.core import api
from src.core.filters.date import create_datetime


try:
    # Get the date of the prompt
    prompt_date = input("Enter the prompt date (YYYY-MM-DD): ")

    # Send out a broadcast
    api.post(
        "broadcast",
        headers=api.create_auth_token(),
        params={"date": create_datetime(prompt_date)},
    )
    print(f"Email broadcast for {prompt_date} successfully sent")

# A broadcast for that day couldn't be sent
except HTTPError:
    print(f"Unable to send email broadcast for {prompt_date}!")
raise SystemExit(0)
