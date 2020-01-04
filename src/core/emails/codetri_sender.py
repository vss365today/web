from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import localtime, make_msgid
from smtplib import SMTP

from src.core import api
from src.core.config import load_app_config
from src.core.emails.generator import render_email
from src.core.filters import create_api_date, format_date_pretty


__all__ = ["send_emails"]


CONFIG = load_app_config()


def construct_email(
    tweet: dict,
    addr: str,
    completed_email: dict
) -> EmailMessage:
    # Split the "To" address into the separate parts
    addr_to = addr.split("@")

    # Instance the email message and set any headers we need
    em = EmailMessage()
    em["Message-ID"] = make_msgid(domain="codetri.net")
    em["Date"] = localtime()

    # Set all of the message details
    em["subject"] = tweet["date"]
    em["from"] = Address(CONFIG["SITE_TITLE"], "noreply", "codetri.net")
    em["to"] = Address(
        f"{CONFIG['SITE_TITLE']} Subscriber",
        addr_to[0],
        addr_to[1]
    )
    # TODO Correctly set mimetypes
    em.set_content(completed_email["html"], subtype="html")
    em.add_alternative(completed_email["text"], subtype="plain")
    print(em)
    raise SystemExit
    return em


def send_emails(tweet: dict):
    mailing_list: list = api.get("subscription")
    tweet["date"] = format_date_pretty(create_api_date(tweet["date"]))
    completed_email = render_email(tweet)

    # Rewrite the emails to be in the correct format
    messages = [
        construct_email(tweet, addr, completed_email)
        for addr in mailing_list
    ]

    # Connect to the local running SMTP server
    with SMTP(
        CONFIG["SMTP_SERVER_ADDRESS"],
        CONFIG["SMTP_SERVER_PORT"]
    ) as server:
        server.ehlo_or_helo_if_needed()
        server.set_debuglevel(1)  # TODO Remove this line

        # Send each message
        # TODO There needs to be some form of logging in place
        # for tracking sucessful/failed messages, if at all possible
        for msg in messages:
            server.send_message(msg)
