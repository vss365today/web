from datetime import date
from typing import Optional

from flask import request
from flask import abort, redirect, render_template, url_for

from src.blueprint import root
from src.core import api, database, filters
from src.core.form import SubscribeForm, UnsubscribeForm
from src.core.helpers import (
    group_month_list_of_writers,
    validate_email_addr
)


@root.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    addition_success = False
    subscribe_form = SubscribeForm()
    email: str = request.form.get("email")

    # Get the email submitted for subscription
    if subscribe_form.validate_on_submit():
        addition_success = database.add_subscribe_email(email)

    render_opts = {
        "email": email,
        "form": subscribe_form,
        "addition_success": addition_success
    }
    return render_template("root/subscribe.html", **render_opts)


@root.route("/form-unsubscribe", methods=["POST"])
def form_unsubscribe():
    removal_success = False
    email = request.form.get("email")

    # Remove the email from the database
    if email is not None and validate_email_addr(email):
        database.remove_subscribe_email(email)
        removal_success = True

    # Go back to the unsub page
    return redirect(url_for(
        "root.unsubscribe",
        success=str(removal_success).lower()
    ))


@root.route("/unsubscribe", methods=["GET"])
def unsubscribe():
    # Determine from the args if the removal happened or not
    removal_success = request.args.get("success")
    if removal_success is not None:
        removal_success = (removal_success == "true")

    render_opts = {
        "removal_success": removal_success,
        "form": SubscribeForm(),
        "form_unsubscribe": UnsubscribeForm()
    }
    return render_template("root/unsubscribe.html", **render_opts)


@root.route("/about")
def about() -> str:
    render_opts = {
        "form": SubscribeForm()
    }
    return render_template("root/about.html", **render_opts)


@root.route("/browse")
def browse() -> str:
    prompt_years: list = api.get("browse", "years")
    render_opts = {
        "form": SubscribeForm(),
        "years": prompt_years
    }
    return render_template("root/browse.html", **render_opts)


@root.route("/browse/<year>")
def browse_by_year(year: str) -> str:
    # Get the writer's list and group them up if needed
    writers_in_year: dict = api.get("browse", params={"year": year})
    grouped_writers = (
        group_month_list_of_writers(writers_in_year["writers"])
        if writers_in_year["query"] == "2017"
        else writers_in_year["writers"]
    )

    render_opts = {
        "form": SubscribeForm(),
        "writers": grouped_writers,
        "year": year
    }
    return render_template("root/browse-year.html", **render_opts)


@root.route("/browse/<year>/<month>")
def browse_by_writer(year: str, month: str) -> str:
    month_prompts: dict = api.get(
        "browse",
        params={"year": year, "month": month}
    )

    render_opts = {
        "form": SubscribeForm(),
        "month_prompts": month_prompts["prompts"],
        "writer": ", ".join(month_prompts["writers"]),
        "date": format_month_year(f"{year}-{month}")
    }
    return render_template("root/browse-writer.html", **render_opts)


@root.route("/")
def index() -> str:
    # if a tweet is not available, abort
    if (tweet := database.get_latest_tweet()) is None:  # noqa
        abort(404)

    # Convert the tweet date into a proper date object
    tweet["date"] = create_date(tweet["date"])

    render_opts = {
        "tweets": [tweet],
        "exists_previous_day": True,
        "exists_next_day": False,
        "form": SubscribeForm()
    }
    return render_template("root/tweet.html", **render_opts)


@root.route("/view/<date>")
def date(date: str) -> str:
    # Abort if we don't have tweets for this day
    if not (db_tweets := database.get_tweets_by_date(date)):  # noqa
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
        "form": SubscribeForm()
    }
    return render_template("root/tweet.html", **render_opts)


@root.app_errorhandler(404)
def page_not_found(e) -> tuple:
    render_opts = {
        "form": SubscribeForm()
    }
    return render_template("partials/errors/404.html", **render_opts), 404


@root.app_errorhandler(500)
def server_error(e) -> tuple:
    return render_template("partials/errors/500.html"), 500


@root.app_template_filter()
def create_api_date(date_str: str) -> date:
    return filters.create_api_date(date_str)


@root.app_template_filter()
def create_date(date_str: str) -> date:
    return filters.create_date(date_str)


@root.app_template_filter()
def format_api_date_iso(date_obj: date) -> str:
    return filters.format_api_date_iso(date_obj)


@root.app_template_filter()
def format_date(date_obj: date) -> str:
    return filters.format_date(date_obj)


@root.app_template_filter()
def format_content(content: str) -> str:
    return filters.format_content(content)


@root.app_template_filter()
def format_month_year(date: str) -> str:
    return filters.format_month_year(date)


@root.app_template_filter()
def yesterday(date: date) -> str:
    return filters.yesterday(date)


@root.app_template_filter()
def tomorrow(date: date) -> str:
    return filters.tomorrow(date)
