import jinja2

from src.core.filters import (
    create_date,
    format_content,
    format_date
)


def render_email_base(tweet: dict) -> str:
    templateLoader = jinja2.FileSystemLoader(searchpath="src/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("email.html")

    # Render the base email content
    render_vals = {
        "tweet_url": tweet["url"],
        "user_handle": tweet["user_handle"],
        "date": format_date(create_date(tweet["date"])),
        "content": format_content(tweet["content"])
    }
    return template.render(**render_vals).replace(r"{\{", "{{")


def render_email_addr(template: str, email: str) -> str:
    """Render an email address into an email template."""
    return jinja2.Template(template).render(**{"email": email})
