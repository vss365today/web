from flask import Blueprint, request
from flask import abort, render_template

from src.core import database
from src.core import filters
from src.core.form import SubscribeForm
from src.core.helpers import (
    get_month_list_of_writers,
    validate_email_addr
)


bp = Blueprint("root", __name__, url_prefix="")


@bp.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    addition_success = False
    subscribe_form = SubscribeForm()
    email = request.form.get("email")

    # Get the email submitted for subscription
    if subscribe_form.validate_on_submit():
        addition_success = database.add_subscribe_email(email)

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
    if email and validate_email_addr(email):
        database.remove_subscribe_email(email)
        removal_success = True

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
        "page_title": "About #vss365"
    }
    return render_template("about.html", **render_opts)


@bp.route("/browse")
def browse() -> str:
    render_opts = {
        "form": SubscribeForm(),
        "years": database.get_tweet_years(),
        "page_title": "Browse #vss365 prompts"
    }
    return render_template("browse.html", **render_opts)


@bp.route("/browse/<year>")
def browse_by_year(year: str) -> str:
    render_opts = {
        "form": SubscribeForm(),
        "writers": get_month_list_of_writers(year),
        "year": year,
        "page_title": f"{year} #vss365 prompts"
    }
    return render_template("browse-year.html", **render_opts)


@bp.route("/browse/<year>/<month>")
def browse_by_writer(year: str, month: str) -> str:
    # Join the date fragments into the format we need
    date = f"{year}-{month}"
    writers = database.get_writer_handle_by_date(date)
    render_opts = {
        "form": SubscribeForm(),
        "tweets": database.get_writer_tweets_by_date(writers, date),
        "writer": ", ".join(writers),
        "date": date
    }
    return render_template("browse-writer.html", **render_opts)


@bp.route("/")
@bp.route("/today")
def index() -> str:
    # Create a proper date object
    tweet = database.get_latest_tweet()

    # A tweet is not available, abort
    if tweet is None:
        abort(404)

    # Convert the tweet date into a proper date object
    tweet["date"] = create_date(tweet["date"])

    render_opts = {
        "tweets": [tweet],
        "exists_previous_day": True,
        "exists_next_day": False,
        "form": SubscribeForm(),
        "page_title": format_date(tweet["date"])
    }
    return render_template("tweet.html", **render_opts)


@bp.route("/view/<date>")
def date(date: str) -> str:
    db_tweets = database.get_tweets_by_date(date)
    # Abort if we don't have tweets for this day
    if not db_tweets:
        abort(404)

    # Create a proper date object for each tweet
    tweets = []
    for tweet in db_tweets:
        tweet = dict(tweet)
        tweet["date"] = create_date(tweet["date"])
        tweets.append(tweet)

    # Check if a tweet for the previous day existS
    exists_previous_day = database.get_tweets_by_date(
        yesterday(tweets[0]["date"])
    ) is not None

    # Check if a tweet for the next day even exists
    exists_next_day = database.get_tweets_by_date(
        tomorrow(tweets[0]["date"])
    ) is not None

    render_opts = {
        "tweets": tweets,
        "exists_previous_day": exists_previous_day,
        "exists_next_day": exists_next_day,
        "form": SubscribeForm(),
        "page_title": format_date(tweets[0]["date"])
    }
    return render_template("tweet.html", **render_opts)


@bp.app_errorhandler(404)
def page_not_found(e) -> tuple:
    render_opts = {
        "form": SubscribeForm(),
        "page_title": "Day not available"
    }
    return render_template("404.html", **render_opts), 404


@bp.app_errorhandler(500)
def server_error(e) -> tuple:
    render_opts = {
        "page_title": "Server error"
    }
    return render_template("500.html", **render_opts), 500


@bp.app_template_filter()
def create_date(date: str) -> str:
    return filters.create_date(date)


@bp.app_template_filter()
def format_date(date: date) -> str:
    return filters.format_date(date)


@bp.app_template_filter()
def format_content(content: str) -> str:
    return filters.format_content(content)


@bp.app_template_filter()
def format_month_year(date: str) -> str:
    return filters.format_month_year(date)


@bp.app_template_filter()
def yesterday(date: date) -> str:
    return filters.yesterday(date)


@bp.app_template_filter()
def tomorrow(date: date) -> str:
    return filters.tomorrow(date)
