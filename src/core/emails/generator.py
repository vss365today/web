from os.path import abspath

from flask import render_template, render_template_string

from src.core.filters import (
    create_date,
    format_content,
    format_date
)


def render_email_base(tweet: dict) -> str:
    # Get the site/email CSS
    with open(abspath("src/static/style.css"), "rt") as f:
        css_styles = f.read()

    # Render the base email content
    render_opts = {
        "date": format_date(create_date(tweet["date"])),
        "content": format_content(tweet["content"]),
        "css_styles": css_styles
    }
    return render_template(
        abspath("src/templates/email.html"),
        **render_opts
    )


def render_email_addr(template: str, email: str) -> str:
    """Render an email address into an email template."""
    return render_template_string(template, email=email)
