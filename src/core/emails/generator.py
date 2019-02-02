import jinja2

from src.core.filters import format_content, format_date


def create_tweet_url(tweet: dict) -> str:
    return f"https://twitter.com/{tweet['handle']}/status/{tweet['tweet_id']}"


def render_email_base(tweet: dict) -> str:
    templateLoader = jinja2.FileSystemLoader(searchpath="src/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("email.html")

    # Render the base email content
    render_vals = {
        "word": tweet["word"],
        "user_handle": tweet["handle"],
        "date": format_date(tweet["date"]),
        "tweet_url": create_tweet_url(tweet),
        "content": format_content(tweet["content"]),
        "media": tweet["media"]
    }
    return template.render(**render_vals).replace(r"{\{", "{{")


def render_email_addr(template: str, email: str) -> str:
    """Render an email address into an email template."""
    return jinja2.Template(template).render(**{"email": email})
