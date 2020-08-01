from flask import request
from flask import flash, redirect, render_template, url_for
import requests

from src.blueprint import bp_search as search
from src.core import api, forms
from src.core.filters.date import create_api_date, create_datetime


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
        return redirect("search.results", query=form.data["query"])
    return "error"


@search.route("/results", methods=["GET"])
def query_search():
    # We got a valid form submission
    search_form = forms.PromptSearchByWord()
    query = request.args.get("query").strip()

    try:
        # We recieved an exact (and valid) date, redirect to it
        create_datetime(query)  # noqa
        return redirect(url_for("root.view_date", date=query))

    # We got a word or partial word to search
    except ValueError:
        # Populate the input with the search term (so... it's a sticky form)
        search_form.query.data = query
        render_opts = {"form": search_form, "form_subscribe": forms.SubscribeForm()}

        # Connect to the API to search
        try:
            response = api.get("search", params={"prompt": query})

        # The search was not successful
        except requests.exceptions.HTTPError:
            render_opts["query"] = query
            render_opts["total"] = 0
            return render_template("search/results.html", **render_opts)

        # We got many search results
        if response["total"] >= 2:
            render_opts.update(response)
            return render_template("search/results.html", **render_opts)

        # We got a single response back, go directly to the prompt
        if response["total"] == 1:
            date = create_api_date(response["prompts"][0]["date"])
            date = date.strftime("%Y-%m-%d")
            return redirect(url_for("root.view_date", date=date))

        # No search results were returned
        render_opts.update(response)
        return render_template("search/results.html", **render_opts)
