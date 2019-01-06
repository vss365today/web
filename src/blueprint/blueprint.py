from flask import Blueprint, request
from flask import render_template

from src.core.tweets import get_tweet_today, get_tweet_by_date
from src.core import filters
from src.core import subscription


bp = Blueprint("root", __name__, url_prefix="")


@bp.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    email = request.form.get("email")
    subscription.add_email(email)
    render_opts = {
        "email": email
    }
    return render_template("subscribe.html", **render_opts)


@bp.route("/unsubscribe", methods=["GET"])
def unsubscribe() -> str:
    email = request.args.get("email")
    subscription.remove_email(email)
    render_opts = {
        "email": email
    }
    return render_template("unsubscribe.html", **render_opts)


@bp.route("/")
@bp.route("/today")
def index() -> str:
    render_opts = {
        "page_title": "",
        "tweet": get_tweet_today()
    }
    return render_template("word.html", **render_opts)


@bp.route("/<date>")
def date(date) -> str:
    render_opts = {
        "page_title": "",
        "tweet": get_tweet_by_date(date)
    }
    return render_template("word.html", **render_opts)


@bp.app_errorhandler(404)
def page_not_found(e) -> str:
    if request.endpoint != "static":
        return render_template("404.html", page_title="Day not found!"), 404


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
