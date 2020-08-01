from flask import session
from flask import flash, redirect, render_template, url_for
import requests

from src.blueprint import bp_search as search
from src.core import api, forms
from src.core.filters.date import create_api_date, format_datetime


@search.route("/", methods=["GET"])
def index():
    render_opts = {
        "form_date": forms.PromptSearchByDate(),
        "form_word": forms.PromptSearchByWord(),
        "form_subscribe": forms.SubscribeForm(),
    }
    return render_template("search/search.html", **render_opts)


@search.route("/date", methods=["POST"])
def by_date():
    # We got a date to search by
    form = forms.PromptSearchByDate()
    if form.validate_on_submit():
        return redirect(url_for("root.view_date", date=form.data["query"]))

    # Something didn't happen so we can't search
    flash(
        f"We were unable to search for Prompts using {form.data['query']}. "
        "Please try using a different term.",
        "error",
    )
    return redirect(url_for("search.index"))


@search.route("/word", methods=["POST"])
def by_word():
    form = forms.PromptSearchByWord()
    if form.validate_on_submit():
        query = form.data["query"]

        # Connect to the API to search
        try:
            response = api.get("search", params={"prompt": query})

        # The search was not successful
        except requests.exceptions.HTTPError:
            session["query"] = query
            session["total"] = 0
            return redirect(url_for("search.results", query=query))

        # We got many search results
        session.update(response)
        if response["total"] >= 2:
            return redirect(url_for("search.results", query=query))

        # We got a single response back, go directly to the prompt
        if response["total"] == 1:
            date = create_api_date(response["prompts"][0]["date"])
            return redirect(url_for("root.view_date", date=format_datetime(date)))

    # No search results were returned
    flash("A search term must be entered in order to search for Prompts.", "error")
    return redirect(url_for("search.index"))


@search.route("/results", methods=["GET"])
def results():
    render_opts = {
        "form_date": forms.PromptSearchByDate(),
        "form_word": forms.PromptSearchByWord(),
        "form_subscribe": forms.SubscribeForm(),
    }
    render_opts.update(session)
    return render_template("search/results.html", **render_opts)
