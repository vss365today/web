from src.extensions import alchemy


class Emails(alchemy.Model):
    id = alchemy.Column(alchemy.Integer, primary_key=True, unique=True)
    email = alchemy.Column(alchemy.String(50), unique=True)


class Tweets(alchemy.Model):
    tweet_id = alchemy.Column(
        alchemy.String(25),
        primary_key=True,
        unique=True
    )
    date = alchemy.Column(alchemy.Date)
    uid = alchemy.Column(alchemy.String(30), alchemy.ForeignKey("givers.uid"))
    content = alchemy.Column(alchemy.String(512))
    word = alchemy.Column(alchemy.String(25))
    media = alchemy.Column(alchemy.String(512))


class Givers(alchemy.Model):
    uid = alchemy.Column(alchemy.String(30), primary_key=True, unique=True)
    handle = alchemy.Column(alchemy.String(20))
    tweets = alchemy.relationship("Tweets", backref="giver", lazy="dynamic")
