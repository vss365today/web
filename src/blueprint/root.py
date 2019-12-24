from datetime import date

from flask import request
from flask import abort, redirect, render_template, url_for
import requests

from src.blueprint import root
from src.core import api, filters
from src.core.form import SubscribeForm, UnsubscribeForm
from src.core.helpers import group_month_list_of_writers


@root.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    addition_success = False
    email = request.form.get("email")

    # Attempt to record the email
    try:
        api.post("subscription", params={"email": email})
        addition_success = True
    except requests.exceptions.HTTPError:
        addition_success = False

    render_opts = {
        "email": email,
        "form_subscribe": SubscribeForm(),
        "addition_success": addition_success
    }
    return render_template("root/subscribe.html", **render_opts)


@root.route("/form-unsubscribe", methods=["POST"])
def form_unsubscribe():
    removal_success = False
    email = request.form.get("email")

    try:
        api.delete("subscription", params={"email": email})
        removal_success = True
    except requests.exceptions.HTTPError:
        removal_success = False

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
        "form_subscribe": SubscribeForm(),
        "form_unsubscribe": UnsubscribeForm()
    }
    return render_template("root/unsubscribe.html", **render_opts)


@root.route("/about")
def about() -> str:
    render_opts = {
        "form_subscribe": SubscribeForm()
    }
    return render_template("root/about.html", **render_opts)


@root.route("/browse")
def browse() -> str:
    prompt_years: list = api.get("browse", "years")
    render_opts = {
        "form_subscribe": SubscribeForm(),
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
        "form_subscribe": SubscribeForm(),
        "writers": grouped_writers,
        "year": year
    }
    return render_template("root/browse-year.html", **render_opts)


@root.route("/browse/<year>/<month>")
def browse_by_year_month(year: str, month: str) -> str:
    month_prompts: dict = api.get(
        "browse",
        params={"year": year, "month": month}
    )

    render_opts = {
        "form_subscribe": SubscribeForm(),
        "date": format_month_year(f"{year}-{month}"),
        "month_prompts": month_prompts["prompts"],
        "writer": ", ".join([
            writer["handle"] for writer in month_prompts["writers"]
        ])
    }
    return render_template("root/browse-writer.html", **render_opts)


@root.route("/")
def index() -> str:
    # Get the latest prompt and go ahead and make a proper date object
    prompts: list = api.get("prompt")
    prompts[0]["date"] = create_api_date(prompts[0]["date"])

    render_opts = {
        "prompts": prompts,
        "previous_day": prompts[0]["previous_day"],
        "next_day": None,
        "form_subscribe": SubscribeForm()
    }
    return render_template("root/tweet.html", **render_opts)


@root.route("/view/<date>")
def view_date(date: str) -> str:
    # Try to get the prompt for this day
    try:
        api_prompts: list = api.get("prompt", params={"date": date})

    # There is no prompt for this day
    except requests.exceptions.HTTPError:
        abort(404)

    # Create a proper date object for each prompt
    # There are some older days that have multiple prompts,
    # and we need to handle these special cases
    prompts = []
    for prompt in api_prompts:
        prompt["date"] = create_api_date(prompt["date"])
        prompts.append(prompt)

    render_opts = {
        "prompts": prompts,
        "previous_day": prompts[0]["previous_day"],
        "next_day": prompts[0]["next_day"],
        "form_subscribe": SubscribeForm()
    }
    return render_template("root/tweet.html", **render_opts)


@root.app_errorhandler(404)
def page_not_found(e) -> tuple:
    render_opts = {
        "form_subscribe": SubscribeForm()
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
