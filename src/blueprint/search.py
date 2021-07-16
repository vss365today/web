from flask import flash, redirect, render_template, session, url_for
from requests.exceptions import HTTPError

from src.blueprint import bp_search as search
from src.core import api, forms
from src.core.filters.date import create_datetime, format_datetime_ymd


@search.route("/", methods=["GET"])
def index():
    render_opts = {
        "form_date": forms.PromptSearchByDate(),
        "form_host": forms.PromptSearchByHost(),
        "form_word": forms.PromptSearchByWord(),
    }
    return render_template("search/search.html", **render_opts)


@search.route("/date", methods=["POST"])
def by_date():
    """Search for a specific day's Prompt."""
    # We got a date to search by
    session["search_type"] = "date"
    form = forms.PromptSearchByDate()
    if form.validate_on_submit():
        return redirect(url_for("root.view_date", date=form.data["query"]))

    # Something didn't happen so we can't search
    flash(
        f"We were unable to find a prompt for {form.data['query']}. "
        "Please select a different date.",
        "error",
    )
    return redirect(url_for("search.index"))


@search.route("/host", methods=["POST"])
def by_host():
    """Search for Prompts from a specific Host."""
    session["search_type"] = "host"
    form = forms.PromptSearchByHost()
    if form.validate_on_submit():
        query = form.data["query"]

        try:
            response = api.get("search", params={"host": query})

            # There doesn't appear any prompts from that Host
            if response["total"] == 0:
                raise HTTPError

        # The search was not successful
        except HTTPError:
            flash(f"No prompts from {query} could be found.", "error")
            return redirect(url_for("search.index"))

        # We got a single result, go directly to the prompt
        session.update(response)
        if response["total"] == 1:
            date = create_datetime(response["prompts"][0]["date"])
            return redirect(url_for("root.view_date", date=format_datetime_ymd(date)))

        # More than one result came back, display them all
        return redirect(url_for("search.results", query=query))

    # That Host was not provided
    flash("A Host name must be provided to search.", "error")
    return redirect(url_for("search.index"))


@search.route("/word", methods=["POST"])
def by_word():
    """Search for Prompts by a specific word."""
    session["search_type"] = "word"
    form = forms.PromptSearchByWord()
    if form.validate_on_submit():
        query = form.data["query"]

        # Connect to the API to search
        try:
            response = api.get("search", params={"prompt": query})

            # There doesn't appear any prompts with that word
            if response["total"] == 0:
                raise HTTPError

        # The search was not successful
        except HTTPError:
            flash(f"No prompts containing {query} could be found.", "error")
            return redirect(url_for("search.index"))

        # We got multiple search results
        session.update(response)
        if response["total"] >= 2:
            return redirect(url_for("search.results", query=query))

        # We got a single response back, go directly to the prompt
        if response["total"] == 1:
            date = create_datetime(response["prompts"][0]["date"])
            return redirect(url_for("root.view_date", date=format_datetime_ymd(date)))

    # No search results were returned
    flash(
        f"We were unable to find prompts containing {form.data['query']}. "
        "Please try using a different term.",
        "error",
    )
    return redirect(url_for("search.index"))


@search.route("/results", methods=["GET"])
def results():
    render_opts = {
        "form_date": forms.PromptSearchByDate(),
        "form_host": forms.PromptSearchByHost(),
        "form_word": forms.PromptSearchByWord(),
    }
    render_opts.update(session)
    return render_template("search/results.html", **render_opts)
