from mailjet_rest import Client

from src.core import api
from src.core.config import load_app_config
from src.core.emails.generator import render_email
from src.core.filters import create_api_date, format_date


__all__ = ["send_emails"]


def construct_email(tweet: dict, addr: str, completed_email: dict) -> dict:
    """Construct a MailJet email dictionary."""
    return {
        "Subject": f'{tweet["date"]}',
        "HTMLPart": completed_email["html"],
        "TextPart": completed_email["text"],
        "From": {
            "Email": "noreply@fromabcthrough.xyz",
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
    tweet["date"] = format_date(create_api_date(tweet["date"]))
    completed_email = render_email(tweet)

    # Get the email address list and break it into chunks of 50
    # The MailJet Send API v3.1
    # has a limit of 50 addresses per batch, up to 200 emails a day.
    # If/when there are more than 50 emails in the db,
    # we need to chunk the addresses. This will chunk them
    # into a nth-array level containing <= 50 emails.
    chunk_size = 50
    mailing_list: list = api.get("subscription")
    mailing_list = [
        mailing_list[i:i + chunk_size]
        for i in range(0, len(mailing_list), chunk_size)
    ]
    rendered_emails = []

    # Construct and render the emails in each chunk
    for chunk in mailing_list:
        email_data: dict = {"Messages": []}
        for addr in chunk:
            msg = construct_email(tweet, addr, completed_email)
            email_data["Messages"].append(msg)
        rendered_emails.append(email_data)

    # Send the Mailjet emails
    for email_data in rendered_emails:
        result = mailjet.send.create(data=email_data)
        print(f"Mail status: {result.status_code}")

        # Get the sending results json
        mj_results = result.json()

        # There was an error sending the emails
        if result.status_code != 200:
            print(mj_results)

        # The emails were successfully sent
        else:
            # Count the send status of each message
            status: dict = {}
            for msg in mj_results["Messages"]:
                status[msg["Status"]] = status.get(msg["Status"], 0) + 1

            # All the emails were send successfully
            if status["success"] == len(mailing_list):
                print("All emails sent successfully.")

            # Everything wasn't successful, display raw count dict
            else:
                print(status)
