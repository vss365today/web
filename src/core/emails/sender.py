from mailjet_rest import Client

from src.core.database import get_all_emails
from src.core.filters import format_date
from src.core.helpers import load_env_vals
from src.core.emails.generator import render_email_base, render_email_addr


def send_emails(tweet):
    # Connect to the Mailjet Send API
    config = load_env_vals()
    mailjet = Client(auth=(
        config["MJ_APIKEY_PUBLIC"],
        config["MJ_APIKEY_PRIVATE"]
    ), version="v3.1")

    # Get the email addresses to send to
    email_list = get_all_emails()

    # Render a base email template
    base_template = render_email_base(tweet)
    print(base_template)

    # Go through each address and create an email
    email_data = {"Messages": []}
    for addr in email_list:
        msg = {
            "Subject": f"VSS 365 Today for {format_date(tweet.date)}",
            "HTMLPart": render_email_addr(base_template, addr),
            "From": {
                "Email": "noreply@vss365today.com",
                "Name": "VSS 365 Today"
            },
            "To": [{
                "Email": addr,
                "Name": "VSS 365 Today Subscriber"
            }]
        }
        email_data["Messages"].append(msg)

    # Send the emails via MailJet
    result = mailjet.send.create(data=email_data)
    print(result.status_code)
    print(result.json())
