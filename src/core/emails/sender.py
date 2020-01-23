from src.core.config import load_json_config
from src.core.emails.codetri_sender import send as send_codetri
from src.core.emails.mailjet_sender import send_emails as send_emails_mailjet

__all__ = ["send_emails"]


def send_emails(tweet: dict):
    # Determine which email provider we need
    JSON_CONFIG = load_json_config()
    providers = {
        "codetri": send_codetri,
        "mailjet": send_emails_mailjet
    }

    # Send out the emails
    providers[JSON_CONFIG["email_provider"]](tweet)
