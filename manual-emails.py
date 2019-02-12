from html import escape
from pprint import pprint
from re import match


from src.core.database import add_tweet_to_db, get_uid_by_handle
from src.core.emails.sender import send_emails
from src.core.filters import create_date, find_prompt_word


def extract_uid(url: str) -> str:
    handle = match(r"^https://twitter\.com/(\w+)/status", url)[1]
    uid = get_uid_by_handle(handle, in_flask=False)
    return uid[0] if uid is not None else None


def extract_tweet_id(url: str) -> str:
    return match(r"^https://twitter\.com/\w+/status/(\d+)", url)[1]


tweet_date = input("Enter the tweet date (YYYY-MM-DD): ")
tweet_url = input("Enter the tweet url: ")
tweet_text = input("Enter the tweet text: ")
tweet_media = input("Enter the tweet image (leave blank for none): ")
tweet_text = tweet_text.replace("\\n", "\n")
tweet_media = tweet_media if tweet_media.strip() else None

# Construct the tweet object
tweet = {
    "tweet_id": extract_tweet_id(tweet_url),
    "date": create_date(tweet_date.strip()),
    "uid": escape(extract_uid(tweet_url)),
    "content": escape(tweet_text),
    "word": find_prompt_word(tweet_text),
    "media": tweet_media
}
pprint(tweet)

# Add the tweet to the database and send the emails
print("Adding tweet to database")
add_tweet_to_db(tweet)
print("Sending out notification emails")
send_emails(tweet)
