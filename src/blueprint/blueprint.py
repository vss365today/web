from flask import Blueprint, request
from flask import render_template

from src.core.database import (
    get_all_givers,
    get_latest_tweet,
    get_tweet_by_date,
    get_tweets_by_giver
)
from src.core import filters
from src.core.form import SubscribeForm
from src.core.helpers import validate_email
from src.core import subscription


bp = Blueprint("root", __name__, url_prefix="")


@bp.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    addition_success = False
    subscribe_form = SubscribeForm()
    email = request.form.get("email")

    # Get the email submitted for subscription
    if subscribe_form.validate_on_submit():
        addition_success = subscription.add_email(email)

    render_opts = {
        "email": email,
        "form": subscribe_form,
        "addition_success": addition_success,
        "page_title": "Get email notifications"
    }
    return render_template("subscribe.html", **render_opts)


@bp.route("/unsubscribe", methods=["GET"])
def unsubscribe() -> str:
    # If we have a valid email, attempt to remove it
    # We don't need to worry about it not existing,
    # that is handled in the removal method
    email = request.args.get("email")
    if email and validate_email(email):
        removal_success = True
        subscription.remove_email(email)

    # This is not a valid email address
    else:
        removal_success = False
        email = "an unspecified email"

    render_opts = {
        "email": email,
        "form": SubscribeForm(),
        "removal_success": removal_success,
        "page_title": "Cancel email notifications"
    }
    return render_template("unsubscribe.html", **render_opts)


@bp.route("/about")
def about() -> str:
    render_opts = {
        "form": SubscribeForm(),
        "page_title": "About VSS 365"
    }
    return render_template("about.html", **render_opts)


@bp.route("/browse")
def browse() -> str:
    render_opts = {
        "form": SubscribeForm(),
        "givers": get_all_givers(),
        "page_title": "Browse VSS prompts"
    }
    return render_template("browse.html", **render_opts)


@bp.route("/browse/<giver>")
def browse_by_giver(giver) -> str:
    render_opts = {
        "form": SubscribeForm(),
        "tweets": get_tweets_by_giver(giver),
        "prompt_giver": giver,
        "page_title": "Browse VSS prompts"
    }
    return render_template("browse-name.html", **render_opts)


@bp.route("/")
@bp.route("/today")
def index() -> str:
    tweet = get_latest_tweet()
    render_opts = {
        "tweet": tweet,
        "form": SubscribeForm(),
        "page_title": filters.format_date(tweet.date)
    }
    return render_template("tweet.html", **render_opts)


@bp.route("/<date>")
def date(date) -> str:
    tweet = get_tweet_by_date(date)
    render_opts = {
        "tweet": tweet,
        "form": SubscribeForm(),
        "page_title": filters.format_date(tweet.date)
    }
    return render_template("tweet.html", **render_opts)


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
