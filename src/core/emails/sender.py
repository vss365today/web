from random import randrange
from typing import Callable, Dict, List

from src.core import api
from src.core.config import load_json_config
from src.core.emails.codetri_sender import send as send_codetri
from src.core.emails.mailjet_sender import send as send_mailjet
from src.core.helpers import chunk_list


__all__ = ["send_emails"]


def send_emails(tweet: dict):
    # Determine which email provider we need
    JSON_CONFIG = load_json_config()
    providers: Dict[str, Callable] = {
        "codetri": send_codetri,
        "mailjet": send_mailjet
    }

    # Get the mailing list and chunk it into groups
    mailing_list: List[List[str]] = chunk_list(
        api.get("subscription"),
        size=20
    )

    # Take out a random chunk of emails to be sent out using
    # a new, self-hosted postfix container.
    # These will be sent out after MailJet messages are sent
    random_chunk = randrange(0, len(mailing_list))
    experimental_send_list = mailing_list.pop(random_chunk)

    # Send out the emails using MailJet
    providers[JSON_CONFIG["email_provider"]](tweet, mailing_list)

    # Send out emails using postfix
    providers["codetri"](tweet, experimental_send_list)
