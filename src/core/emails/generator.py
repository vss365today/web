from os.path import join
from jinja2 import Template


__all__ = [
    "render_email"
]


def create_tweet_url(tweet: dict) -> str:
    return f"https://twitter.com/{tweet['handle']}/status/{tweet['tweet_id']}"


def render_email(tweet: dict, email: str) -> str:
    """Render a complete email template."""
    # Read the template content
    template_file = join("src", "templates", "email.html")
    with open(template_file) as f:
        template = f.read()

    # Construct a proper tweet URL
    tweet["url"] = create_tweet_url(tweet)

    # Render the thing already
    return Template(template).render(tweet=tweet, email=email)
