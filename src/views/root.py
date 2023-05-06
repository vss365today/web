from datetime import date
from random import randrange
from typing import NamedTuple

from flask import abort, flash, redirect, render_template, session, url_for
from num2words import num2words
from requests.exceptions import HTTPError

from src.blueprints import root
from src.core import forms
from src.core.api import v2


@root.post("form-subscribe")
def form_subscribe():
    form = forms.SubscribeForm()
    # The magic "is human" numbers do not exist, don't continue on
    if "SUBSCRIBE_NUM" not in session or not form.validate_on_submit():
        flash("We were unable to add you to #vss365 notifications.", "error")
        return redirect(url_for("root.index"))

    # The magic numbers were not summed correctly
    if form.number.data != session["SUBSCRIBE_NUM"][0] + session["SUBSCRIBE_NUM"][1]:
        flash("We were unable to add you to #vss365 notifications.", "error")
        return redirect(url_for("root.index"))

    # Attempt to record the email
    email = form.email.data
    try:
        v2.post("emails/", json={"address": [email]})
        flash(
            (
                f"{email} has been added to #vss365 notifications! "
                "Tomorrow's prompt will be in your inbox!"
            ),
            "info",
        )
    except HTTPError:
        flash(f"We were unable to add {email} to #vss365 notifications.", "error")
    return redirect(url_for("root.index"))


@root.get("subscribe")
def subscribe():
    # Generate two random numbers to use for a basic "is human" check.
    # Once generated, add them to the session for confirmation on form submit.
    # We generate these numbers on every page load unconditionally
    # so we don't persist anything
    second_num = randrange(20)
    random_nums = [randrange(1, 21), second_num, num2words(second_num)]
    session["SUBSCRIBE_NUM"] = random_nums

    # Build up the input label to contain the math equation to be solved
    # and remove any prior input the browser might have preserved (*@ Firefox...*)
    form = forms.SubscribeForm()
    form.number.data = None
    form.number.label.text = f"{random_nums[0]} + {random_nums[2]} ="
    render_opts = {"form_subscribe": form}
    return render_template("root/subscribe.html", **render_opts)


@root.post("form-unsubscribe")
def form_unsubscribe():
    form = forms.UnsubscribeForm()
    if not form.validate_on_submit():
        flash("We were unable to remove you from #vss365 notifications.", "error")
        return redirect(url_for("root.unsubscribe"))

    # Attempt to delete the email
    email = form.email.data
    try:
        v2.delete("emails/", json={"address": [email]})
        flash(f"{email} has been removed from #vss365 notifications.", "info")
        return redirect(url_for("root.index"))
    except HTTPError:
        flash(f"We were unable to remove {email} from #vss365 notifications.", "error")
        return redirect(url_for("root.unsubscribe"))


@root.get("unsubscribe")
def unsubscribe():
    render_opts = {"form_unsubscribe": forms.UnsubscribeForm()}
    return render_template("root/unsubscribe.html", **render_opts)


@root.get("about")
def about():
    return render_template("root/about.html")


@root.get("browse")
def browse():
    # Handle the archive file possibly being unavailable
    try:
        archive_name = v2.get("archive/")
    except HTTPError:
        archive_name = None

    render_opts = {
        "years": v2.get("browse", "years")["years"],
        "archive": archive_name,
    }
    return render_template("root/browse.html", **render_opts)


@root.get("browse/<int:year>")
def browse_by_year(year: int):
    """View the months in a year Prompts have been recorded."""
    try:
        # Get the host's list and group them up if needed
        prompt_months = v2.get("browse", "years", str(year))["months"]
    except HTTPError:
        abort(404)

    render_opts = {
        "months": [date(year, m, 1) for m in prompt_months],
        "year": year,
    }
    return render_template("root/browse-year.html", **render_opts)


@root.get("browse/<int:year>/<int:month>")
def browse_by_year_month(year: int, month: int) -> str:
    """View Prompts in a calendar month."""
    try:
        month_prompts: dict = v2.get("browse", str(year), str(month))
    except HTTPError:
        abort(404)

    render_opts = {
        "date": date(year, month, 1),
        "month_prompts": month_prompts["prompts"],
    }
    return render_template("root/browse-month.html", **render_opts)


@root.get("donate")
def donate() -> str:
    class Costs(NamedTuple):
        cost: float | int
        month_freq: int

    site_costs = {
        "domain": Costs(9.15, 1),
        "email": Costs(22, 12),
        "server": Costs(7.2, 12),
        "twitter": Costs(100, 12),
    }

    render_opts = {"site_costs": site_costs}
    return render_template("root/donate.html", **render_opts)


@root.get("/")
def index():
    # Create a proper date object for each prompt
    # There are some older days that have multiple prompts,
    # and we need to handle these special cases
    available_prompts = v2.get("prompts/")
    prompts = []
    for prompt in available_prompts:
        prompt["date"] = date.fromisoformat(prompt["date"])
        prompts.append(prompt)

    render_opts = {
        "prompts": prompts,
        "previous": (
            date.fromisoformat(prompts[0]["navigation"]["previous"])
            if prompts[0]["navigation"]["previous"]
            else None
        ),
        "next": None,
    }

    return render_template("root/index.html", **render_opts)


@root.get("view/2017-09-05")
def view_one_year():
    """Build out the special 1 year anniversary prompt page."""
    prompt: dict = v2.get("prompts", "date", "2017-09-05")[0]
    render_opts = {
        "prompt": prompt,
        "previous": date.fromisoformat(prompt["navigation"]["previous"]),
        "next": date.fromisoformat(prompt["navigation"]["next"]),
    }
    return render_template("root/one-year.html", **render_opts)


@root.get("view/<d>")
def view_date(d: str):
    """Build out the daily prompt page."""
    # Try to get the prompt for this day
    try:
        available_prompts: list[dict] = v2.get(
            "prompts", "date", date.fromisoformat(d).isoformat()
        )

    # There is no prompt for this day or we got a bad date string
    except (ValueError, HTTPError):
        abort(404)

    # Create a proper date object for each prompt.
    # There are some older days that have multiple prompts
    # and we need to handle these special cases
    prompts = []
    for prompt in available_prompts:
        prompt["date"] = date.fromisoformat(prompt["date"])
        prompts.append(prompt)

    render_opts = {
        "prompts": prompts,
        "previous": (
            date.fromisoformat(prompts[0]["navigation"]["previous"])
            if prompts[0]["navigation"]["previous"]
            else None
        ),
        "next": (
            date.fromisoformat(prompts[0]["navigation"]["next"])
            if prompts[0]["navigation"]["next"]
            else None
        ),
    }
    return render_template("root/index.html", **render_opts)
