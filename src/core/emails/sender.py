from mailjet_rest import Client

from src.core.config import load_app_config
from src.core.database import get_all_emails
from src.core.filters import format_date
from src.core.emails.generator import render_email


def construct_email(tweet: dict, addr: str) -> dict:
    """Construct a MailJet email dictionary."""
    return {
        "Subject": f"#vss365 prompt for {tweet['date']}",
        "HTMLPart": render_email(tweet, addr),
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
    CONFIG = load_app_config()
    mailjet = Client(auth=(
        CONFIG["MJ_APIKEY_PUBLIC"],
        CONFIG["MJ_APIKEY_PRIVATE"]
    ), version="v3.1")

    # Properly format the tweet date
    tweet["date"] = format_date(tweet["date"])

    # Get the email address list
    email_list = get_all_emails()

    # Construct the emails
    email_data = {"Messages": []}
    for addr in email_list:
        msg = construct_email(tweet, addr)
        email_data["Messages"].append(msg)

    # Send the emails via MailJet
    result = mailjet.send.create(data=email_data)
    print(f"Mail status: {result.status_code}")

    # Get the sending results json
    mj_results = result.json()

    # Count the send status of each message
    status = {}
    for msg in mj_results["Messages"]:
        status[msg["Status"]] = status.get(msg["Status"], 0) + 1

    # All the emails were send successfully
    if status["success"] == len(email_list):
        print("All emails sent successfully.")

    # Everything wasn't successful, display raw count dict
    else:
        print(status)
