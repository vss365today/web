from random import sample

from mailjet_rest import Client

from src.core.database import get_all_emails
from src.core.helpers import load_env_vals
from src.core.emails.generator import render_email


def construct_email(template: str, tweet: dict, addr: str) -> dict:
    """Construct a MailJet email dictionary."""
    return {
        "Subject": f"#vss365 prompt for {tweet['date']}",
        "HTMLPart": render_email(template, tweet, addr),
        "From": {
            "Email": "noreply@vss365today.com",
            "Name": "#vss365 today"
        },
        "To": [{
            "Email": addr,
            "Name": "#vss365 today Subscriber"
        }]
    }


def send_emails(tweet: dict):
    # Connect to the Mailjet Send API
    config = load_env_vals()
    mailjet = Client(auth=(
        config["MJ_APIKEY_PUBLIC"],
        config["MJ_APIKEY_PRIVATE"]
    ), version="v3.1")

    # Get the email address list
    email_list = set(get_all_emails())

    # In order to experiment with solving #6, we're going to
    # split the email list in half, randomly sending half the
    # population the new template and half the existing one.
    # This experiment will run until either I'm happy with
    # the new template or I scrap it and search for a different one
    sample_size = len(email_list) // 2
    new_email_template_list = set(sample(email_list, sample_size))
    old_email_template_list = email_list - new_email_template_list

    # Start with the current email template
    email_data = {"Messages": []}
    for addr in old_email_template_list:
        msg = construct_email("email.html", tweet, addr)
        email_data["Messages"].append(msg)

    # Now do the new email template
    for addr in new_email_template_list:
        msg = construct_email("new-email.html", tweet, addr)
        email_data["Messages"].append(msg)

    # Send the emails via MailJet
    result = mailjet.send.create(data=email_data)
    print(f"Mail status: {result.status_code}")
    # TODO Parse this JSON to get better results status
    print(result.json())
