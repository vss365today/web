from email.headerregistry import Address
from email.message import EmailMessage
# from smtplib import SMTP

__all__ = [
    "send_emails_codetri"
]


def rewrite_email_structure(msg: dict) -> EmailMessage:
    # Split the "To" address into the separate parts
    addr_to = msg["To"][0]["Email"].split("@")

    # Rebuild the email message to be an EmailMessage instance
    msg = EmailMessage()
    msg["subject"] = msg["Subject"]  # TODO This is not being set? Why not?
    msg["from"] = Address("#vss365 today", "noreply", "vss365today.com")
    msg["to"] = Address("#vss365 today Subscriber", addr_to[0], addr_to[1])
    # msg.set_content(msg["HTMLPart"], subtype="html")  # TODO this is raising a NoneType error
    return msg


def send_emails_codetri(msgs: list):
    # Rewrite the emails to be in the correct format
    r = rewrite_email_structure(msgs[0])
    # msgs = [
    #     rewrite_email_structure(msg)
    #     for msg in msgs
    # ]
    pass
