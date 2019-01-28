from datetime import date
import re


__all__ = [
    "create_date",
    "create_proper_image_url",
    "find_prompt_word",
    "format_content",
    "format_date",
    "format_image_url"
]


def create_date(date_str: str) -> date:
    return date(*[int(d) for d in date_str.split("-")])


def create_proper_image_url(
    text: str,
    img_short_url: str,
    img_full_url: str
) -> str:
    """Replace a t.co image short link with a full image url."""
    return text.replace(img_short_url, img_full_url)


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


def format_prompt_word(word: str) -> str:
    # TODO: Do this better
    return f"<h3>{word}</h3>"


def format_image_url(text: str) -> str:
    # Find an URL, if one is present
    regex = re.compile(
        r"https://pbs\.twimg\.com/.+\.(?:jpg|png|gif)",
        re.MULTILINE
    )
    match = re.search(regex, text)

    # If we have one, put it in an HTML img tag
    if match:
        url = match.group(0)
        text = text.replace(url, f'\n<img width="500" src="{url}">')
    return text


def format_content(text: str) -> str:
    # Start by forming a proper image URL
    text = format_image_url(text)

    # Wrap all non-blank lines in paragraphs
    split_text = text.split("\n")
    split_text = [
        f"<p>{para.strip()}</p>"
        for para in split_text
        if para  # false-y value means blank line
    ]
    return "\n".join(split_text)


def format_date(date) -> str:
    return date.strftime("%d %B, %Y")
