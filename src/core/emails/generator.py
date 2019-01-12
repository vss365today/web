from os.path import abspath

from src.core.filters import (
    create_date,
    format_content,
    format_date,
    render_template,
    render_template_string
)


def render_email_base(tweet: dict) -> str:
    # Render the base email content
    render_vals = {
        "tweet_url": tweet["url"],
        "user_handle": tweet["user_handle"],
        "date": format_date(create_date(tweet["date"])),
        "content": format_content(tweet["content"])
    }
    return render_template(
        abspath("src/templates/email.html"),
        render_vals
    )


def render_email_addr(template: str, email: str) -> str:
    """Render an email address into an email template."""
    return render_template_string(template, {"email": email})
