from flask import abort, flash, redirect, render_template, request, url_for
from requests.exceptions import HTTPError

from src.blueprint import bp_root as root
from src.core import api
from src.core.filters import date as date_format
from src.core.form import SubscribeForm, UnsubscribeForm
from src.core.helpers import get_unique_year_months


@root.route("subscribe", methods=["POST"])
def subscribe():
    # Attempt to record the email
    email = request.form.get("email")
    try:
        api.post("subscription", params={"email": email})
        flash(f"Successfully added {email} to the subscription list.", "info")
    except HTTPError:
        flash(
            f"We were unable to add {email} to the subscription list. "
            "Please try again shortly.",
            "error",
        )
    return redirect(url_for("root.index"))


@root.route("form-unsubscribe", methods=["POST"])
def form_unsubscribe():
    # Attempt to delete the email
    # TODO What if we don't get an email here?
    email = request.form.get("email")
    try:
        api.delete("subscription", params={"email": email})
        flash(f"Successfully removed {email} from the subscription list.", "info")
        return redirect(url_for("root.index"))
    except HTTPError:
        flash(
            f"We were unable to remove {email} to the subscription list. "
            "Please try again shortly.",
            "error",
        )
        return redirect(url_for("root.unsubscribe"))


@root.route("unsubscribe", methods=["GET"])
def unsubscribe():
    render_opts = {
        "form_subscribe": SubscribeForm(),
        "form_unsubscribe": UnsubscribeForm(),
    }
    return render_template("root/unsubscribe.html", **render_opts)


@root.route("about")
def about():
    render_opts = {"form_subscribe": SubscribeForm()}
    return render_template("root/about.html", **render_opts)


@root.route("browse")
def browse():
    # Handle the archive file possibly being unavailable
    try:
        # archive_name = api.get("archive")
        archive_name = False
    except HTTPError:
        archive_name = False

    render_opts = {
        "form_subscribe": SubscribeForm(),
        "years": api.get("browse", "years"),
        "archive": archive_name,
    }
    return render_template("root/browse.html", **render_opts)


@root.route("browse/<year>")
def browse_by_year(year: str):
    # Get the host's list and group them up if needed
    try:
        year_hosts: dict = api.get("browse", params={"year": year})
    except HTTPError:
        abort(404)

    render_opts = {
        "form_subscribe": SubscribeForm(),
        "dates": get_unique_year_months(year_hosts["hosts"]),
        "year": year,
    }
    return render_template("root/browse-year.html", **render_opts)


@root.route("browse/<year>/<month>")
def browse_by_year_month(year: str, month: str) -> str:
    try:
        month_prompts: dict = api.get("browse", params={"year": year, "month": month})
    except HTTPError:
        abort(404)

    render_opts = {
        "form_subscribe": SubscribeForm(),
        "date": date_format.format_month_year(f"{year}-{month}-01"),
        "month_prompts": month_prompts["prompts"],
    }
    return render_template("root/browse-month.html", **render_opts)


@root.route("donate")
def donate():
    render_opts = {"form_subscribe": SubscribeForm()}
    return render_template("root/donate.html", **render_opts)


@root.route("/")
def index():
    # Create a proper date object for each prompt
    # There are some older days that have multiple prompts,
    # and we need to handle these special cases
    available_prompts = api.get("prompt")
    prompts = []
    for prompt in available_prompts:
        prompt["date"] = date_format.create_api_date(prompt["date"])
        prompts.append(prompt)

    render_opts = {
        "prompts": prompts,
        "previous_day": prompts[0]["previous_day"],
        "next_day": None,
        "form_subscribe": SubscribeForm(),
    }
    return render_template("root/tweet.html", **render_opts)


@root.route("view/<date>")
def view_date(date: str):
    # Try to get the prompt for this day
    try:
        available_prompts = api.get(
            "prompt", params={"date": str(date_format.create_datetime(date))}
        )

    # There is no prompt for this day
    except HTTPError:
        abort(404)

    # Create a proper date object for each prompt
    # There are some older days that have multiple prompts,
    # and we need to handle these special cases
    prompts = []
    for prompt in available_prompts:
        prompt["date"] = date_format.create_api_date(prompt["date"])
        prompts.append(prompt)

    render_opts = {
        "prompts": prompts,
        "previous_day": prompts[0]["previous_day"],
        "next_day": prompts[0]["next_day"],
        "form_subscribe": SubscribeForm(),
    }
    return render_template("root/tweet.html", **render_opts)
