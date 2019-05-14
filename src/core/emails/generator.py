import jinja2

from src.core.filters import format_date


def create_tweet_url(tweet: dict) -> str:
    return f"https://twitter.com/{tweet['handle']}/status/{tweet['tweet_id']}"


def render_email_base(tweet: dict) -> str:
    templateLoader = jinja2.FileSystemLoader(searchpath="src/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("email.html")

    # Render the base email content,
    # formatting all information as needed
    tweet["date"] = format_date(tweet["date"])
    tweet["url"] = create_tweet_url(tweet)
    return template.render(tweet=tweet).replace(r"{\{", "{{")


def render_email_addr(template: str, email: str) -> str:
    """Render an email address into an email template."""
    return jinja2.Template(template).render(email=email)
