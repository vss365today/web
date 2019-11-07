from src.core.config import load_json_config
from src.core.emails.codetri_sender import send_emails_codetri
from src.core.emails.mailjet_sender import send_emails_mailjet
from src.core.emails.mailgun_sender import send_emails_mailgun

__all__ = ["send_emails"]


def send_emails(tweet: dict):
    # Determine which email provider we need
    JSON_CONFIG = load_json_config()
    methods = {
        "codetri": send_emails_codetri,
        "mailjet": send_emails_mailjet,
        "mailgun": send_emails_mailgun
    }

    # Send out the emails
    methods[JSON_CONFIG["email_provider"]](tweet)
