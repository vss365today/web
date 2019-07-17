from pprint import pprint

from src.core.database import get_tweets_by_date
from src.core.emails.sender import send_emails
from src.core.filters import create_date


# Get the date of the tweet we want to email out
tweet_date = input("Enter the tweet date (YYYY-MM-DD): ")
db_tweets = get_tweets_by_date(tweet_date.strip())

# We don't have a tweet for the requested day
if not db_tweets:
    print(f"There are no tweets in the database for {tweet_date}!")
    raise SystemExit(0)

print(f"\nTweets available for {tweet_date}:")
for i, prompt in enumerate(db_tweets):
    print(f"[{i}] {prompt['word']}")
print()
tweet_index = input("Which tweet would you like to send out? (default [0]): ")

# Make sure we have a valid index but default to the first tweet
tweet_index = int(tweet_index) if tweet_index.strip() != "" else 0
if tweet_index < 0 or tweet_index > len(db_tweets) - 1:
    print("That is not an available tweet!")
    raise SystemExit(0)

# Construct a dictionary with only the info we need
picked_tweet = db_tweets[tweet_index]
tweet = {
    "tweet_id": picked_tweet["tweet_id"],
    "date": create_date(tweet_date),
    "handle": picked_tweet["writer_handle"],
    "content": picked_tweet["content"],
    "word": picked_tweet["word"],
    "media": picked_tweet["media"]
}
pprint(tweet)

# Send out the emails that oh-so-didn't work earlier
print("Sending out notification emails")
send_emails(tweet)
