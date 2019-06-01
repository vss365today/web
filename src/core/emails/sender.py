from mailjet_rest import Client

from src.core.database import get_all_emails
from src.core.helpers import load_env_vals
from src.core.emails.generator import render_email


def send_emails(tweet: dict):
    # Connect to the Mailjet Send API
    config = load_env_vals()
    mailjet = Client(auth=(
        config["MJ_APIKEY_PUBLIC"],
        config["MJ_APIKEY_PRIVATE"]
    ), version="v3.1")

    # Get the email addresses and send them an email
    email_list = get_all_emails()
    email_data = {"Messages": []}
    for addr in email_list:
        msg = {
            "Subject": f"#vss365 prompt for {tweet['date']}",
            "HTMLPart": render_email("email.html", tweet, addr),
            "From": {
                "Email": "noreply@vss365today.com",
                "Name": "#vss365 today"
            },
            "To": [{
                "Email": addr,
                "Name": "#vss365 today Subscriber"
            }]
        }
        email_data["Messages"].append(msg)

    # Send the emails via MailJet
    result = mailjet.send.create(data=email_data)
    print(f"Mail status: {result.status_code}")
