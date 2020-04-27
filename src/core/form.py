from flask_wtf import FlaskForm
from wtforms import Field, PasswordField
from wtforms.fields.html5 import EmailField, SearchField
from wtforms.validators import DataRequired, Email


__all__ = ["AdminSignInForm", "PromptSearchForm", "SubscribeForm", "UnsubscribeForm"]


class AdminSignInForm(FlaskForm):
    username = Field("Username", id="input-username", validators=[DataRequired()])
    password = PasswordField(
        "Password", id="input-password", validators=[DataRequired()]
    )


class PromptSearchForm(FlaskForm):
    query = SearchField(
        "",
        id="input-search-prompt",
        validators=[DataRequired()],
        render_kw={"placeholder": "braid"},
    )


class SubscribeForm(FlaskForm):
    email = EmailField(
        "Subscribe to daily #vss365 notifications",
        id="input-email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "amwriting@vss365today.com", "autocomplete": "email"},
    )


class UnsubscribeForm(FlaskForm):
    email = EmailField(
        "Unsubscribe from daily #vss365 notifications",
        id="input-email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "amwriting@vss365today.com", "autocomplete": "email"},
    )
