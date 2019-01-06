from datetime import datetime
from datetime import timedelta

from flask import Blueprint, request
from flask import render_template

from src.core.tweets import get_tweet_today, get_tweet_by_date, find_image
from src.core.form import add_email, remove_email


bp = Blueprint("root", __name__, url_prefix="")


@bp.route("/form", methods=["POST"])
def form() -> str:
    email = request.form.get("email")
    add_email(email)
    tweet = {
        "date": datetime.today(),
        "email": email
    }
    return render_template("subscribe.html", tweet=tweet)


@bp.route("/unsubscribe", methods=["GET"])
def unsubscribe() -> str:
    email = request.args.get("email")
    remove_email(email)
    tweet = {
        "date": datetime.today(),
        "email": email
    }
    return render_template("unsubscribe.html", tweet=tweet)


@bp.route("/")
@bp.route("/today")
def index() -> str:
    tweet = get_tweet_today()
    return render_template("word.html", tweet=tweet)


@bp.route("/<date>")
def date(date) -> str:
    tweet = get_tweet_by_date(date)
    return render_template("word.html", tweet=tweet)


@bp.app_errorhandler(404)
def page_not_found(e) -> str:
    # Create a dummy tweet object containing the requested date
    if request.endpoint != "static":
        tweet = {
            "date": datetime.strptime(request.path[1:], "%Y-%m-%d")
        }
        return render_template("404.html", tweet=tweet), 404


@bp.app_template_filter()
def format_date(date) -> str:
    return date.strftime("%d %B, %Y")


@bp.app_template_filter()
def format_content(content) -> str:
    return "\n".join([
        f"<p>{find_image(para)}</p>"
        for para in content.split("\r\n")
        if para
    ])


@bp.app_template_filter()
def yesterday(date) -> str:
    return datetime.strftime(date - timedelta(1), "%Y-%m-%d")


@bp.app_template_filter()
def tomorrow(date) -> str:
    return datetime.strftime(date + timedelta(1), "%Y-%m-%d")
