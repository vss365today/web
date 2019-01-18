from datetime import date, datetime, timedelta
import re


__all__ = [
    "create_curly_quotes",
    "create_date",
    "create_proper_image_url",
    "format_content",
    "format_date",
    "format_image_url",
    "render_template",
    "render_template_string"
]


def __curly_replace_double_quotes(text):
    """https://stackoverflow.com/a/44336227"""
    # 1. Replace "space followed by straight double quote"
    # by "space followed by opening curly":
    text = text.replace(' "', " “")

    # 2. Replace "straight double quote followed by space"
    # by "closing curly followed by space":
    text = text.replace('" ', "” ")

    # 3. Replace "straight double quote followed by comma"
    # by "closing curly followed by comma":
    text = text.replace('",', "”,")

    # 4. Replace "straight double quote followed by semicolon"
    # by "closing curly followed by semicolon":
    text = text.replace('";', "”;")

    # 5. Replace "straight double quote followed by fullstop"
    # by "closing curly followed by fullstop":
    text = text.replace('".', "”.")
    return text


def __curly_replace_single_quotes(text):
    """https://stackoverflow.com/a/44336227"""
    # 1. Replace "space followed by straight single quote"
    # by "space followed by opening curly":
    text = text.replace(" '", " ‘")

    # 2. Replace "straight single quote followed by space"
    # by "closing curly followed by space":
    text = text.replace('" ', "” ")

    # 3. Replace "straight single quote followed by comma"
    # by "closing curly followed by comma":
    text = text.replace("',", "’,")

    # 4. Replace "straight single quote followed by semicolon"
    # by "closing curly followed by semicolon":
    text = text.replace("';", "’”;")

    # 5. Replace "straight single quote followed by fullstop"
    # by "closing curly followed by fullstop":
    text = text.replace("'.", "’.")
    return text


def create_curly_quotes(text):
    # text = body[0].decode()

    # https://stackoverflow.com/a/44336227
    # https://stackoverflow.com/a/2202835
    # regex_single_quotes = re.compile(r"", re.MULTILINE)
    # regex_double_quotes = re.compile(r"", re.MULTILINE)
    text = __curly_replace_double_quotes(text)
    text = __curly_replace_single_quotes(text)

    # body[0] = text.encode()
    return text


def create_date(date_l: list) -> date:
    return date(*date_l)


def create_proper_image_url(
    text: str,
    img_short_url: str,
    img_full_url: str
) -> str:
    """Replace a t.co image short link with a full image url."""
    return text.replace(img_short_url, img_full_url)


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
            prompt_word = remaining[0]
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
        text = text.replace(url, f'<img width="500" src="{url}">')
    return text


def format_content(text: str) -> str:
    # Start by forming a proper image URL
    text = format_image_url(text)

    # Get the prompt word, format it differently,
    # and put it back into the content
    prompt_word = find_prompt_word(text)
    formatted_word = format_prompt_word(prompt_word)
    text = text.replace(prompt_word, formatted_word)

    # Wrap all non-blank lines in paragraphs
    split_text = text.split("\n")
    split_text = [
        f"<p>{para}</p>"
        for para in split_text
        if para  # false-y value means blank line
    ]
    return "\n".join(split_text)


def format_date(date) -> str:
    return date.strftime("%d %B, %Y")


def render_template_string(template: str, render_vals: dict) -> str:
    for key, val in render_vals.items():
        template = template.replace("||{}||".format(key), val)
    return template


def render_template(fi: str, render_vals: dict) -> str:
    with open(fi, "rt") as f:
        template = f.read()
    return render_template_string(template, render_vals)


def yesterday(date) -> str:
    return datetime.strftime(date - timedelta(1), "%Y-%m-%d")


def tomorrow(date) -> str:
    return datetime.strftime(date + timedelta(1), "%Y-%m-%d")
