from pprint import pprint

from src.core.database import get_tweet_by_date
from src.core.emails.sender import send_emails
from src.core.filters import create_date


# Get the date of the tweet we want to email out
tweet_date = input("Enter the tweet date (YYYY-MM-DD): ")
prompt_tweet = get_tweet_by_date(tweet_date.strip())

# We don't have a tweet for the requested day
if prompt_tweet is None:
    print(f"There is not tweet in the database for {tweet_date}!")
    raise SystemExit(0)

# Construct a dictionary with only the info we need
tweet = {
    "tweet_id": prompt_tweet["tweet_id"],
    "date": create_date(tweet_date),
    "handle": prompt_tweet["writer_handle"],
    "content": prompt_tweet["content"],
    "word": prompt_tweet["word"],
    "media": prompt_tweet["media"]
}
pprint(tweet)

# Send out the emails that oh-so-didn't work earlier
print("Sending out notification emails")
send_emails(tweet)
