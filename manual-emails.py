from pprint import pprint
from requests.exceptions import HTTPError

from src.core import api
from src.core.emails.sender import send_emails


# Get the date of the prompt we want to email out
try:
    prompt_date = input("Enter the prompt date (YYYY-MM-DD): ")
    prompt = api.get("prompt", params={"date": prompt_date.strip()})[0]

# We don't have a prompt for the requested day
except HTTPError:
    print(f"There is no prompt for {prompt_date}!")
    raise SystemExit(0)

# Construct a dictionary with only the info we need
final_prompt = {
    "tweet_id": prompt["id"],
    "date": prompt_date.strip(),
    "handle": prompt["writer_handle"],
    "content": prompt["content"],
    "word": prompt["word"],
    "media": prompt["media"]
}
pprint(final_prompt)

# Send out the emails that oh-so-didn't work earlier
print("Sending out notification emails")
send_emails(final_prompt)
