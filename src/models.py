from src.extensions import db


class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), index=True)

    def __repr__(self):
        return '<Email {}>'.format(self.email)


class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True)
    user_handle = db.Column(db.String(30))
    tweet_url = db.Column(db.String(128))
    tweet_content = db.Column(db.String(500))
