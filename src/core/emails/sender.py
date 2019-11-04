from random import randrange

import requests

from src.core.config import load_app_config, load_json_config
from src.core.database import get_all_emails
from src.core.emails.codetri_sender import send_emails_codetri
from src.core.emails.generator import render_email
from src.core.filters import format_date


__all__ = ["send_emails"]


# Pull in the main app config
CONFIG = load_app_config()


def construct_email(date: str, addr: str, content_html: str) -> dict:
    """Construct a Mailgun email dictionary."""
    return {
        "from": f'{CONFIG["SITE_TITLE"]} <noreply@vss365today.com>',
        "to": f'{CONFIG["SITE_TITLE"]} Subscriber <{addr}>',
        "subject": f'{date}',
        "html": content_html
    }


def send_emails(tweet: dict):
    CONFIG_JSON = load_json_config()

    # Properly format the tweet date
    tweet["date"] = format_date(tweet["date"])
    completed_email = render_email(tweet)

    # Get the email address list and break them
    # into a nth-array level containing <= 50 emails.
    # This was done for a previous email sending service
    # and is no longer strictly required but assists in
    # transitioning from a third-party email service
    chunk_size = 50
    email_list = get_all_emails()
    email_list = [
        email_list[i:i + chunk_size]
        for i in range(0, len(email_list), chunk_size)
    ]
    rendered_emails = []

    # Construct and render the emails in each chunk
    for chunk in email_list:
        email_data = []
        for addr in chunk:
            msg = construct_email(tweet["date"], addr, completed_email)
            email_data.append(msg)
        rendered_emails.append(email_data)

    # If enabled, take out a random chunk of emails to be sent out
    # using a new, self-hosted postfix server.
    # These will be sent out after Mailgun messages are sent
    if CONFIG_JSON["use_new_mail_sending"]:
        random_chunk = randrange(0, len(rendered_emails))
        experimental_send_list = rendered_emails.pop(random_chunk)

    # Send the Mailgun emails
    for chunk in rendered_emails:
        for email_data in chunk:
            requests.post(
                f'https://api.mailgun.net/v3/{CONFIG["MG_DOMAIN"]}/messages',
                auth=("api", CONFIG["MG_API_KEY"]),
                data=email_data
            )

    # Finally, send out the experimental emails if needed
    if CONFIG_JSON["use_new_mail_sending"]:
        send_emails_codetri(experimental_send_list)

    print("Emails sent out.")
