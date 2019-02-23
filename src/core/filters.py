from datetime import date, timedelta
import re


__all__ = [
    "create_date",
    "find_prompt_word",
    "format_content",
    "format_date",
    "make_urls",
    "previous",
    "next"
]


def create_date(date_str: str) -> date:
    return date(*[int(d) for d in date_str.split("-")])


def create_tweet_url(tweet: dict) -> str:
    return f"https://twitter.com/{tweet.giver.handle}/status/{tweet.tweet_id}"


def find_prompt_word(text: str) -> str:
    prompt_word = ""

    # Find all hashtags in the tweet
    regex = re.compile(
        r"(#\w+)",
        re.MULTILINE
    )
    matches = re.findall(regex, text)

    # We have hashtags
    if matches:
        remaining = list(filter(
            lambda hashtag: hashtag.upper() not in ("#VSS365", "#PROMPT"),
            matches
        ))

        # If there are any hashtags left, get the first one
        # and remove the prefixed pound sign
        if remaining:
            prompt_word = remaining[0][1:]
    return prompt_word


def format_content(text: str) -> str:
    # Wrap all non-blank lines in paragraphs
    split_text = text.split("\n")
    split_text = [
        f"<p>{para.strip()}</p>"
        for para in split_text
        if para  # false-y value means blank line
    ]

    # Rejoin the lines and make all links clickable
    new_text = "\n".join(split_text)
    new_text = make_urls(new_text)
    return new_text


def format_date(date: date) -> str:
    """Nicely format the date in a non ISO 8601 manner."""
    return date.strftime("%d %B, %Y")


def make_urls(text: str) -> str:
    """Convert all text links in a tweet into an HTML link."""
    # Start by finding all possible t.co text links
    matches = re.findall(r"(https://t\.co/[a-z0-9]+)", text, re.I)
    if matches is None:
        return text

    # Go through each url and wrap it in an HTML a tag
    for match in matches:
        url = f'<a href="{match}">{match}</a>'
        text = text.replace(match, url)
    return text


def previous(date: date) -> str:
    """Get the date prior to the given date."""
    return (date - timedelta(1)).isoformat()


def next(date: date) -> str:
    """Get the date after to the given date."""
    return (date + timedelta(1)).isoformat()
