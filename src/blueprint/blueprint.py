import json

from flask import Blueprint, request
from flask import render_template

from src.core.database import (
    add_word_to_db,
    get_latest_word,
    get_word_by_date
)
from src.core.form import SubscribeForm
from src.core import filters
from src.core import subscription
from src.extensions import csrf


bp = Blueprint("root", __name__, url_prefix="")


@bp.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    # TODO Validate form data
    subscribe_form = SubscribeForm()
    email = request.form.get("email")
    subscription.add_email(email)

    render_opts = {
        "email": email,
        "form": subscribe_form,
        "page_title": "Get email notifications"
    }
    return render_template("subscribe.html", **render_opts)


@bp.route("/unsubscribe", methods=["GET"])
def unsubscribe() -> str:
    # TODO Validate form data
    email = request.args.get("email")
    subscription.remove_email(email)

    render_opts = {
        "email": email,
        "form": SubscribeForm(),
        "page_title": "Remove email notifications"
    }
    return render_template("unsubscribe.html", **render_opts)


@bp.route("/")
@bp.route("/today")
def index() -> str:
    tweet = get_latest_word()
    render_opts = {
        "tweet": tweet,
        "form": SubscribeForm(),
        "page_title": filters.format_date(tweet.date)
    }
    return render_template("word.html", **render_opts)


@bp.route("/<date>")
def date(date) -> str:
    tweet = get_word_by_date(date)
    render_opts = {
        "tweet": tweet,
        "form": SubscribeForm(),
        "page_title": filters.format_date(tweet.date)
    }
    return render_template("word.html", **render_opts)


@csrf.exempt
@bp.route("/api/add", methods=["POST"])
def add_to_db() -> str:
    tweet = json.loads(request.json)
    add_word_to_db(tweet)
    return ""


@bp.app_errorhandler(404)
def page_not_found(e) -> tuple:
    render_opts = {
        "form": SubscribeForm(),
        "page_title": "Day not available"
    }
    return render_template("404.html", **render_opts), 404


@bp.app_template_filter()
def format_date(date) -> str:
    return filters.format_date(date)


@bp.app_template_filter()
def format_content(content) -> str:
    return filters.format_content(content)


@bp.app_template_filter()
def yesterday(date) -> str:
    return filters.yesterday(date)


@bp.app_template_filter()
def tomorrow(date) -> str:
    return filters.tomorrow(date)
