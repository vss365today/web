from random import randrange
from typing import Callable, Dict, List

from src.core import api
from src.core.config import load_app_config, load_json_config
from src.core.emails.codetri_sender import send as send_codetri
from src.core.emails.mailjet_sender import send as send_mailjet
from src.core.helpers import chunk_list


__all__ = ["send_emails"]


def send_emails(tweet: dict):
    # Determine which email provider we need
    JSON_CONFIG = load_json_config()
    CONFIG = load_app_config()
    providers: Dict[str, Callable] = {
        "codetri": send_codetri,
        "mailjet": send_mailjet
    }

    # Quick block for debugging local email sending
    if JSON_CONFIG["debug_codetri_emails"]:
        experimental_send_list = [
            CONFIG["SMPT_TEST_EMAIL"]
            for _ in range(JSON_CONFIG["email_chunk_size"] + 1)
        ]
        providers["codetri"](tweet, experimental_send_list)
        return True

    # Get the mailing list and chunk it into groups
    mailing_list: List[List[str]] = chunk_list(
        api.get("subscription"),
        size=JSON_CONFIG["email_chunk_size"]
    )

    # Take out a random chunk of emails to be sent out using
    # a new, self-hosted postfix container.
    # These will be sent out after MailJet messages are sent
    random_chunk = randrange(0, len(mailing_list))
    experimental_send_list = mailing_list.pop(random_chunk)

    # Regardless of the chunk selected, always send a copy
    # to the test email addr so I know it, like, works
    experimental_send_list.append(CONFIG["SMPT_TEST_EMAIL"])

    # Send out the emails using MailJet
    providers[JSON_CONFIG["email_provider"]](tweet, mailing_list)

    # Send out emails using postfix
    providers["codetri"](tweet, experimental_send_list)
