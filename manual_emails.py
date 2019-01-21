from html import escape
from pprint import pprint


from src.core.database import add_word_to_db
from src.core.emails.sender import send_emails
from src.core.filters import create_date, find_prompt_word


tweet_date = input("Enter the tweet date (YYYY-MM-DD): ")
user_handle = input("Enter the prompt giver handle: ")
tweet_url = input("Enter the tweet url: ")
tweet_text = input("Enter the tweet text: ")
tweet_image = input("Enter the tweet image (leave blank for none): ")

# Add the image to the tweet content if one was given
tweet_text = tweet_text.replace("\\n", "\n")
if tweet_image.strip():
    tweet_text = f"{tweet_text}\n\n{tweet_image}"

# Construct the tweet object
tweet = {
    "url": tweet_url,
    "date": create_date(tweet_date.strip()),
    "user_handle": escape(user_handle),
    "content": escape(tweet_text),
    "word": find_prompt_word(tweet_text)
}
pprint(tweet)

# Add the tweet to the database and send the emails
print("Adding tweet to database")
add_word_to_db(tweet)
print("Sending out notification emails")
send_emails(tweet)
