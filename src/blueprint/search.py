from flask import flash, redirect, render_template, session, url_for
from requests.exceptions import HTTPError

from src.blueprint import bp_search as search
from src.core import api, forms
from src.core.filters.date import create_api_date, format_datetime


@search.route("/", methods=["GET"])
def index():
    render_opts = {
        "form_date": forms.PromptSearchByDate(),
        "form_host": forms.PromptSearchByHost(),
        "form_word": forms.PromptSearchByWord(),
        "form_subscribe": forms.SubscribeForm(),
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
        f"We were unable to search for prompts using {form.data['query']}. "
        "Please try using a different term.",
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

        # Connect to the API to search
        try:
            response = api.get("search", params={"host": query})

        # The search was not successful
        except HTTPError:
            session["query"] = query
            session["total"] = 0
            return redirect(url_for("search.results", query=query))

        # Display the results
        session.update(response)
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

        # The search was not successful
        except HTTPError:
            session["query"] = query
            session["total"] = 0
            return redirect(url_for("search.results", query=query))

        # We got multiple search results
        session.update(response)
        if response["total"] >= 2:
            return redirect(url_for("search.results", query=query))

        # We got a single response back, go directly to the prompt
        if response["total"] == 1:
            date = create_api_date(response["prompts"][0]["date"])
            return redirect(url_for("root.view_date", date=format_datetime(date)))

    # No search results were returned
    flash("A word or series of letters must be provided to search.", "error")
    return redirect(url_for("search.index"))


@search.route("/results", methods=["GET"])
def results():
    render_opts = {
        "form_date": forms.PromptSearchByDate(),
        "form_host": forms.PromptSearchByHost(),
        "form_word": forms.PromptSearchByWord(),
        "form_subscribe": forms.SubscribeForm(),
    }
    render_opts.update(session)
    return render_template("search/results.html", **render_opts)
