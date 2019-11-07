import json
# from random import randrange

import requests

from src.core.config import load_app_config
from src.core.database import get_mailing_list
from src.core.emails.generator import render_email
from src.core.filters import format_date


__all__ = ["send_emails"]


# Pull in the main app config
CONFIG = load_app_config()


def construct_email(date: str, content: dict, mailing_list: list) -> dict:
    """Construct a Mailgun batch sending email dictionary."""
    return {
        "from": f'{CONFIG["SITE_TITLE"]} <noreply@{CONFIG["APP_DOMAIN"]}>',
        "to": list(mailing_list),
        "subject": f'{date} (and a blog post!)',
        "text": content["text"],
        "html": content["html"],
        "recipient-variables": json.dumps(mailing_list)
    }


def construct_email2(date: str, content: dict, addr: str) -> dict:
    """Construct a Mailgun individual email dictionary."""
    return {
        "from": f'{CONFIG["SITE_TITLE"]} <noreply@{CONFIG["APP_DOMAIN"]}>',
        "to": addr,
        "subject": f'{date} (and a blog post!)',
        "text": content["text"],
        "html": content["html"]
    }


def send_emails(tweet: dict):
    mailing_list = get_mailing_list()

    # Properly format the tweet date
    tweet["date"] = format_date(tweet["date"])
    completed_email = render_email(tweet)

    # Chunk the mailing list into a nth-array level containing <= 50 emails.
    # This was done for a previous email sending service
    # and is no longer strictly required but assists in
    # transitioning from a third-party email service
    # CHUNK_SIZE = 50
    addresses_only = list(mailing_list)
    # addresses_only = [
    #     addresses_only[i:i + CHUNK_SIZE]
    #     for i in range(0, len(addresses_only ), CHUNK_SIZE)
    # ]

    # Next, break the dictionary to only have <= CHUNK_SIZE pairs.
    # When done, it'll have the following structure
    # [
    #     {
    #         addr1: hash1,
    #         addr2: hash2
    #     },
    # {
    #         addr3: hash3,
    #         addr4: hash4
    #     },
    # ]
    # chunked_mailing_list = []
    # for chunk in addresses_only:
    #     vals = {}
    #     for addr in chunk:
    #         vals[addr] = {"unique_id": mailing_list[addr]}
    #     chunked_mailing_list.append(vals)

    # Remove the old lists
    # del mailing_list
    # del addresses_only

    # Construct and send the emails in each chunk
    # for chunk in chunked_mailing_list:
    # msgs = construct_email(tweet["date"], completed_email, chunk)

    # Send the emails
    # for addr in addresses_only:
    try:
        r = requests.post(
            f'https://api.mailgun.net/v3/{CONFIG["MG_DOMAIN"]}/messages',
            auth=("api", CONFIG["MG_API_KEY"]),
            data=construct_email2(
                tweet["date"],
                completed_email,
                addresses_only
            )
        )
        r.raise_for_status()
    except Exception as exc:
        print(exc)
        # break
    else:
        print(r)

    print("Emails sent out.")
