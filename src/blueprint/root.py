from flask import abort, flash, redirect, render_template, request, url_for
from requests.exceptions import HTTPError

from src.blueprint import bp_root as root
from src.core import api, filters
from src.core.form import SubscribeForm, UnsubscribeForm
from src.core.helpers import group_month_list_of_hosts


@root.route("/subscribe", methods=["POST"])
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


@root.route("/form-unsubscribe", methods=["POST"])
def form_unsubscribe():
    # Attempt to delete the email
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


@root.route("/unsubscribe", methods=["GET"])
def unsubscribe():
    # Determine from the args if the removal happened or not
    removal_success = request.args.get("success")
    if removal_success is not None:
        removal_success = removal_success == "true"

    render_opts = {
        "removal_success": removal_success,
        "form_subscribe": SubscribeForm(),
        "form_unsubscribe": UnsubscribeForm(),
    }
    return render_template("root/unsubscribe.html", **render_opts)


@root.route("/about")
def about():
    render_opts = {"form_subscribe": SubscribeForm()}
    return render_template("root/about.html", **render_opts)


@root.route("/browse")
def browse():
    prompt_years = api.get("browse", "years")
    render_opts = {"form_subscribe": SubscribeForm(), "years": prompt_years}
    return render_template("root/browse.html", **render_opts)


@root.route("/browse/<year>")
def browse_by_year(year: str):
    # Get the host's list and group them up if needed
    try:
        hosts_in_year: dict = api.get("browse", params={"year": year})
    except HTTPError:
        abort(404)

    grouped_groups = (
        group_month_list_of_hosts(hosts_in_year["hosts"])
        if hosts_in_year["query"] == "2017"
        else hosts_in_year["hosts"]
    )

    render_opts = {
        "form_subscribe": SubscribeForm(),
        "hosts": grouped_groups,
        "year": year,
    }
    return render_template("root/browse-year.html", **render_opts)


@root.route("/browse/<year>/<month>")
def browse_by_year_month(year: str, month: str) -> str:
    try:
        month_prompts: dict = api.get("browse", params={"year": year, "month": month})
    except HTTPError:
        abort(404)

    render_opts = {
        "form_subscribe": SubscribeForm(),
        "date": filters.format_month_year(f"{year}-{month}"),
        "month_prompts": month_prompts["prompts"],
        "host": ", ".join(host["handle"] for host in month_prompts["hosts"]),
    }
    return render_template("root/browse-host.html", **render_opts)


@root.route("/donate")
def donate():
    render_opts = {"form_subscribe": SubscribeForm()}
    return render_template("root/donate.html", **render_opts)


@root.route("/")
def index():
    # Get the latest prompt and go ahead and make a proper date object
    prompts = api.get("prompt")
    prompts[0]["date"] = filters.create_api_date(prompts[0]["date"])

    render_opts = {
        "prompts": prompts,
        "previous_day": prompts[0]["previous_day"],
        "next_day": None,
        "form_subscribe": SubscribeForm(),
    }
    return render_template("root/tweet.html", **render_opts)


@root.route("/view/<date>")
def view_date(date: str):
    # Try to get the prompt for this day
    try:
        api_prompts = api.get(
            "prompt", params={"date": str(filters.create_datetime(date))}
        )

    # There is no prompt for this day
    except HTTPError:
        abort(404)

    # Create a proper date object for each prompt
    # There are some older days that have multiple prompts,
    # and we need to handle these special cases
    prompts = []
    for prompt in api_prompts:
        prompt["date"] = filters.create_api_date(prompt["date"])
        prompts.append(prompt)

    render_opts = {
        "prompts": prompts,
        "previous_day": prompts[0]["previous_day"],
        "next_day": prompts[0]["next_day"],
        "form_subscribe": SubscribeForm(),
    }
    return render_template("root/tweet.html", **render_opts)


@root.app_errorhandler(404)
def page_not_found(e) -> tuple:
    render_opts = {"form_subscribe": SubscribeForm()}
    return render_template("partials/errors/404.html", **render_opts), 404


@root.app_errorhandler(500)
def server_error(e) -> tuple:
    return render_template("partials/errors/500.html"), 500
