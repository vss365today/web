from datetime import datetime
from src.core.filters.date import format_datetime

from flask_wtf import FlaskForm
from wtforms import Field, PasswordField
from wtforms.fields.html5 import EmailField, SearchField, DateField
from wtforms.validators import DataRequired, Email


__all__ = [
    "AdminSignInForm",
    "PromptSearchByDate",
    "PromptSearchByWord",
    "SubscribeForm",
    "UnsubscribeForm",
]


class AdminSignInForm(FlaskForm):
    username = Field("Username", id="input-username", validators=[DataRequired()])
    password = PasswordField(
        "Password", id="input-password", validators=[DataRequired()]
    )


class PromptSearchByDate(FlaskForm):
    query = DateField(
        "Search by date",
        id="input-search-date",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "2020-07-02",
            "pattern": r"\d{4}-\d{2}-\d{2}",
            "max": format_datetime(datetime.now()),
        },
    )


class PromptSearchByWord(FlaskForm):
    query = SearchField(
        "Search by word",
        id="input-search-word",
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
