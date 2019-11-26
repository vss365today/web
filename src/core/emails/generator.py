from os.path import join
from jinja2 import Template


__all__ = [
    "render_email"
]


def create_tweet_url(tweet: dict) -> str:
    return f"https://twitter.com/{tweet['handle']}/status/{tweet['tweet_id']}"


def render_email(tweet: dict) -> dict:
    """Render a complete email template."""
    # Construct a proper tweet URL
    tweet["url"] = create_tweet_url(tweet)

    # Read the templates
    html_template_file = join("src", "templates", "email", "email.html")
    text_template_file = join("src", "templates", "email", "email.txt")
    with open(html_template_file) as f:
        html_template = f.read()
    with open(text_template_file) as f:
        text_template = f.read()

    # Render the thing already
    return {
        "html": Template(html_template).render(tweet=tweet),
        "text": Template(text_template).render(tweet=tweet)
    }
