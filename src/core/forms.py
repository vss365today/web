from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    EmailField,
    HiddenField,
    IntegerField,
    SearchField,
    SelectField,
    SubmitField,
)
from wtforms.validators import Email, InputRequired

from src.core.api import v2


__all__ = [
    "PromptSearchByDate",
    "PromptSearchByHost",
    "PromptSearchByWord",
    "SubscribeForm",
    "UnsubscribeForm",
]


def get_all_hosts() -> list[tuple[str, str]]:
    return [(host["handle"], host["handle"]) for host in v2.get("hosts/")]


class PromptSearchByDate(FlaskForm):
    type = HiddenField(default="date")
    query = DateField(
        "Date search",
        validators=[InputRequired()],
        render_kw={
            "placeholder": "2020-07-02",
            "pattern": r"\d{4}-\d{2}-\d{2}",
            "max": date.today().isoformat(),
        },
    )


class PromptSearchByHost(FlaskForm):
    type = HiddenField(default="host")
    query = SelectField(
        "Host search",
        id="input-search-host",
        validators=[InputRequired()],
        choices=get_all_hosts,
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
    number = IntegerField(
        validators=[InputRequired()],
        render_kw={"inputmode": "numeric"},
    )
    submit = SubmitField("Unsubscribe")
