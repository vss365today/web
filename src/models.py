from src.extensions import alchemy


class Emails(alchemy.Model):
    id = alchemy.Column(alchemy.Integer, primary_key=True)
    email = alchemy.Column(alchemy.String(50), unique=True)


class Tweets(alchemy.Model):
    id = alchemy.Column(alchemy.Integer, primary_key=True)
    date = alchemy.Column(alchemy.Date)
    user_handle = alchemy.Column(alchemy.String(30))
    url = alchemy.Column(alchemy.String(128))
    content = alchemy.Column(alchemy.String(512))
    word = alchemy.Column(alchemy.String(30))
