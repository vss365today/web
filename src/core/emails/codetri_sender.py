from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import localtime, make_msgid
from smtplib import SMTP
from typing import Dict, List, NewType

from src.core.config import load_app_config
from src.core.emails.generator import generate, render, EmailTemplate


__all__ = ["send"]


CONFIG = load_app_config()
EmailAddress = NewType("EmailAddress", str)


def construct(
    tweet: Dict[str, str],
    addr: EmailAddress,
    completed_email: EmailTemplate
) -> EmailMessage:

    # Instance the email message and set any headers we need
    em = EmailMessage()
    em["Message-ID"] = make_msgid(domain=CONFIG["SMTP_DOMAIN"])
    em["Date"] = localtime()

    # Set all of the message details
    em["Subject"] = tweet["date_pretty"]
    em["From"] = Address(
        CONFIG["SITE_TITLE"],
        "noreply",
        CONFIG["SMTP_DOMAIN"]
    )

    # Split the "To" address into the separate parts
    addr_to = addr.split("@")
    em["To"] = Address(
        f"{CONFIG['SITE_TITLE']} Subscriber",
        addr_to[0],
        addr_to[1]
    )

    # Provide both HTML and text versions of te email
    # TODO Correctly set both parts of the email
    em.set_content(completed_email.text)
    em.add_alternative(completed_email.html, subtype="html")
    return em


def send(tweet: dict, mailing_list: List[str]):
    # Prepare the tweet object and render out the email
    tweet = generate(tweet)
    completed_email = render(tweet)

    # Construct the email objects for sending
    messages = [
        construct(tweet, EmailAddress(addr), completed_email)
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
