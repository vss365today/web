from random import choices  # , randrange
from json import dumps as json_dumps
from string import printable as printable_chars

import requests

from src.core.config import load_app_config  # , load_json_config
from src.core.database import get_all_emails
# from src.core.emails.codetri_sender import send_emails_codetri
from src.core.emails.generator import render_email
from src.core.filters import format_date


__all__ = ["send_emails"]


# Pull in the main app config
CONFIG = load_app_config()


def construct_email(date: str, content: dict, mailing_list: list) -> dict:
    """Construct a Mailgun email dictionary."""
    # TODO
    recipient_vars = json_dumps({
        addr: {"id": "".join(choices(printable_chars, k=15))}
        for addr in mailing_list
    })

    return {
        "from": f'{CONFIG["SITE_TITLE"]} <noreply@{CONFIG["APP_DOMAIN"]}>',
        "to": mailing_list,
        "subject": f'{date} (and a blog post!)',
        "html": content["html"],
        "recipient-variables": recipient_vars
    }


def send_emails(tweet: dict):
    # CONFIG_JSON = load_json_config()

    # Properly format the tweet date
    tweet["date"] = format_date(tweet["date"])
    completed_email = render_email(tweet)

    # Get the email address list and generate unique IDS for each one
    # to permit batch sending through Mailgun
    # TODO Consider generating and pulling these from the database
    mailing_list = get_all_emails()

    # Chunk the mailing list into a nth-array level containing <= 50 emails.
    # This was done for a previous email sending service
    # and is no longer strictly required but assists in
    # transitioning from a third-party email service
    chunk_size = 50
    mailing_list = [
        mailing_list[i:i + chunk_size]
        for i in range(0, len(mailing_list), chunk_size)
    ]
    rendered_emails = []

    # Construct and render the emails in each chunk
    for chunk in mailing_list:
        msgs = construct_email(tweet["date"], {"html": completed_email}, chunk)
        rendered_emails.append(msgs)

    # If enabled, take out a random chunk of emails to be sent out
    # using a new, self-hosted postfix server.
    # These will be sent out after Mailgun messages are
    # if CONFIG_JSON["use_new_mail_sending"]:
    #     random_chunk = randrange(0, len(rendered_emails))
    #     experimental_send_list = rendered_emails.pop(random_chunk)

    # Send the Mailgun emails
    for chunk in rendered_emails:
        requests.post(
            f'https://api.mailgun.net/v3/{CONFIG["MG_DOMAIN"]}/messages',
            auth=("api", CONFIG["MG_API_KEY"]),
            data=chunk
        )

    # Finally, send out the experimental emails if needed
    # if CONFIG_JSON["use_new_mail_sending"]:
    #     send_emails_codetri(experimental_send_list)

    print("Emails sent out.")
