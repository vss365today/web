from src.extensions import alchemy
from src.models import Emails


def add_email(addr: str) -> bool:
    email = Emails(email=addr)
    alchemy.session.add(email)
    alchemy.session.commit()
    return bool(email)


def remove_email(addr: str):
    email = Emails.query.filter(Emails.email == addr).first()
    alchemy.session.delete(email)
    r = alchemy.session.commit()
    # TODO: Is this actually a return value?
    print(r)
