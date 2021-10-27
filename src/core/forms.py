from datetime import datetime
from src.core import api
from src.core.filters.date import format_datetime_ymd

from flask_wtf import FlaskForm
from wtforms.fields.simple import HiddenField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerField, SearchField, DateField
from wtforms.validators import InputRequired, Email
from wtforms_components import SelectField


__all__ = [
    "PromptSearchByDate",
    "PromptSearchByHost",
    "PromptSearchByWord",
    "SubscribeForm",
    "UnsubscribeForm",
]


class PromptSearchByDate(FlaskForm):
    type = HiddenField(default="date")
    query = DateField(
        "Date search",
        validators=[InputRequired()],
        render_kw={
            "placeholder": "2020-07-02",
            "pattern": r"\d{4}-\d{2}-\d{2}",
            "max": format_datetime_ymd(datetime.now()),
        },
    )


class PromptSearchByHost(FlaskForm):
    type = HiddenField(default="host")
    query = SelectField(
        "Host search",
        id="input-search-host",
        validators=[InputRequired()],
        choices=[
            (host["handle"], host["handle"])
            for host in api.get("host", params={"all": True})
        ],
    )


class PromptSearchByWord(FlaskForm):
    type = HiddenField(default="word")
    query = SearchField(
        "Word search",
        validators=[InputRequired()],
        render_kw={"placeholder": "braid"},
    )


class SubscribeForm(FlaskForm):
    """Notification email subscribe form."""

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email()],
        render_kw={
            "placeholder": "amwriting@vss365today.com",
            "autocomplete": "email",
            "inputmode": "email",
        },
    )
    number = IntegerField(
        validators=[InputRequired()],
        render_kw={"inputmode": "numeric"},
    )
    submit = SubmitField("Subscribe")


class UnsubscribeForm(FlaskForm):
    """Notification email unsubscribe form."""

    email = EmailField(
        "Unsubscribe from daily #vss365 notifications",
        validators=[InputRequired(), Email()],
        render_kw={
            "placeholder": "amwriting@vss365today.com",
            "autocomplete": "email",
            "inputmode": "email",
        },
    )
    submit = SubmitField("Unsubscribe")
