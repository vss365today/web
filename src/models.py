from src.extensions import alchemy


class Emails(alchemy.Model):
    email = alchemy.Column(
        alchemy.String(50),
        primary_key=True,
        unique=True,
        nullable=False
    )


class Tweets(alchemy.Model):
    tweet_id = alchemy.Column(
        alchemy.String(25),
        primary_key=True,
        unique=True,
        nullable=False
    )
    date = alchemy.Column(alchemy.Date, unique=True, nullable=False)
    uid = alchemy.Column(
        alchemy.String(30),
        alchemy.ForeignKey("givers.uid"),
        nullable=False
    )
    content = alchemy.Column(alchemy.String(512), nullable=False)
    word = alchemy.Column(alchemy.String(25), nullable=False)
    media = alchemy.Column(alchemy.String(512), nullable=True)


class Givers(alchemy.Model):
    uid = alchemy.Column(
        alchemy.String(30),
        primary_key=True,
        unique=True,
        nullable=False
    )
    handle = alchemy.Column(
        alchemy.String(20),
        unique=True,
        nullable=False
    )
    date = alchemy.Column(
        alchemy.String(7),
        unique=True,
        nullable=False
    )
    tweets = alchemy.relationship("Tweets", backref="giver", lazy="dynamic")
