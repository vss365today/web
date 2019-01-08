from src.extensions import alchemy
from src.models import Emails


def get_existing_email(addr: str):
    """Find an existing email in the database."""
    return Emails.query.filter(Emails.email == addr).first()


def add_email(addr: str) -> bool:
    """Add an email address to the email notifications."""
    # Don't try to add the email if it already exists
    # However, tell the user that it was added
    if get_existing_email(addr) is not None:
        return False

    # Add the email to the database
    email = Emails(email=addr)
    alchemy.session.add(email)
    alchemy.session.commit()
    return bool(email)


def remove_email(addr: str):
    """Remove an email address from the email notifications."""
    # Find the record with this email (it will be unique)
    email = get_existing_email(addr)

    # Remove the email from the database,
    # still telling the user it was successful
    # even if it was already removed
    if email is not None:
        alchemy.session.delete(email)
        alchemy.session.commit()
