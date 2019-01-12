from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class SubscribeForm(FlaskForm):
    email = EmailField(
        "Enter your email to receive daily notifications!",
        id="input-email",
        validators=[DataRequired(), Email()]
    )
