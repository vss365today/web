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

    # Get the email address list and break it into chunks of 50
    # The MailJet Send API, under a free account,
    # has a limit of 50 addresses per batch, up to 200 emails a day.
    # If/when there are more than 50 emails in the db,
    # we need to chunk the addresses. This will chunk them
    # into a nth-array level containing <= 50 emails.
    # That said, if there is ever > 200 emails,
    # MailJet just won't cut it anymore. :sad_face:
    chunk_size = 50
    email_list = get_all_emails()
    email_list = [
        email_list[i:i + chunk_size]
        for i in range(0, len(email_list), chunk_size)
    ]

    for chunk in email_list:
        # Construct the emails in each chunk
        email_data = {"Messages": []}
        for addr in chunk:
            msg = construct_email(tweet, addr)
            email_data["Messages"].append(msg)

        # Send the emails
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
            status = {}
            for msg in mj_results["Messages"]:
                status[msg["Status"]] = status.get(msg["Status"], 0) + 1

            # All the emails were send successfully
            if status["success"] == len(email_list):
                print("All emails sent successfully.")

            # Everything wasn't successful, display raw count dict
            else:
                print(status)
