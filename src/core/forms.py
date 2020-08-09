from datetime import datetime
from src.core import api
from src.core.filters.date import format_datetime

from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, SearchField, DateField
from wtforms.validators import DataRequired, Email
from wtforms_components import SelectField


__all__ = [
    "PromptSearchByDate",
    "PromptSearchByHost",
    "PromptSearchByWord",
    "SubscribeForm",
    "UnsubscribeForm",
]


class PromptSearchByDate(FlaskForm):
    query = DateField(
        "Date search",
        id="input-search-date",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "2020-07-02",
            "pattern": r"\d{4}-\d{2}-\d{2}",
            "max": format_datetime(datetime.now()),
        },
    )


class PromptSearchByHost(FlaskForm):
    query = SelectField(
        "Host search",
        id="input-search-host",
        validators=[DataRequired()],
        choices=[(host["handle"], host["handle"]) for host in api.get("host", params={"all": True})],
    )


class PromptSearchByWord(FlaskForm):
    query = SearchField(
        "Word search",
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
