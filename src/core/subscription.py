from src.extensions import alchemy
from src.models import Emails


def add_email(addr: str) -> bool:
    """Add an email address to the email notifications."""
    email = Emails(email=addr)
    alchemy.session.add(email)
    alchemy.session.commit()
    return bool(email)


def remove_email(addr: str):
    """Remove an email address from the email notifications."""
    # Find the record with this email (it will be unique)
    email = Emails.query.filter(Emails.email == addr).first_or_404()
    alchemy.session.delete(email)
    r = alchemy.session.commit()
    # TODO: Is this actually a return value?
    print(r)
