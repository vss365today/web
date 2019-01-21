from html import escape
from urllib.parse import quote
from pprint import pprint


from src.core.database import add_word_to_db
from src.core.emails.sender import send_emails


user_handle = input("Enter the prompt giver handle: ")
tweet_date = input("Enter the tweet date (YYYY-MM-DD): ")
tweet_url = input("Enter the tweet url: ")
tweet_text = input("Enter the tweet text: ")
tweet_image = input("Enter the tweet image (leave blank for none): ")

# Add the image to the tweet content if one was given
tweet_text = tweet_text.replace("\\n", "\n")
if tweet_image.strip():
    tweet_text = f"{tweet_text}\n\n{tweet_image}"

# Construct the tweet object
tweet = {
    "url": quote(tweet_url),
    "date": [int(d) for d in tweet_date.split("-")],
    "user_handle": escape(user_handle),
    "content": escape(tweet_text)
}
pprint(tweet)

# Add the tweet to the database and send the emails
print("Adding tweet to database")
add_word_to_db(tweet)
print("Sending out notification emails")
send_emails(tweet)
