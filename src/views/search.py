from datetime import date
from typing import TypedDict

from flask import flash, redirect, render_template, request, url_for
from requests.exceptions import HTTPError

from src.blueprints import search
from src.core import forms
from src.core.api import v2


class SearchResult(TypedDict, total=False):
    msg: str
    url: str
    error: bool
    results: dict


def by_date(query: str) -> SearchResult:
    """Search for a specific day's Prompt."""
    # We got a date to search by
    if query:
        if query == "2017-09-05":
            return SearchResult(url=url_for("root.view_one_year", d=query), error=False)
        return SearchResult(url=url_for("root.view_date", d=query), error=False)

    # Something didn't happen so we can't search
    return SearchResult(
        msg=(
            f"We were unable to find a prompt for {query}. "
            "Please select a different date."
        ),
        url=url_for("search.index"),
        error=True,
    )


def by_host(query: str) -> SearchResult:
    """Search for Prompts from a specific Host."""
    if query:
        try:
            response = v2.get("search", "host", query)

            # There doesn't appear any prompts from that Host
            if response["total"] == 0:
                raise HTTPError

        # The search was not successful
        except HTTPError:
            return SearchResult(
                msg=f"No prompts from {query} could be found.",
                url=url_for("search.index"),
                error=True,
            )

        # We got a single result, go directly to the prompt
        if response["total"] == 1:
            d = date.fromisoformat(response["prompts"][0]["date"])
            return SearchResult(
                url=url_for("root.view_date", d=d.isoformat()), error=False
            )

        # More than one result came back, display them all
        return SearchResult(results=response, error=False)

    # That Host was not provided
    return SearchResult(
        msg="A Host name must be provided to search.",
        url=url_for("search.index"),
        error=True,
    )


def by_word(query: str) -> SearchResult:
    """Search for Prompts by a specific word."""
    # Only search if we have a query and it's not a single letter
    query = query.strip()
    if query and len(query) >= 2:
        # Connect to the API to search
        try:
            response = v2.get("search", "query", query)

            # There doesn't appear any prompts with that word
            if response["total"] == 0:
                raise HTTPError

        # The search was not successful
        except HTTPError:
            return SearchResult(
                msg=f"No prompts containing {query} could be found.",
                url=url_for("search.index"),
                error=True,
            )

        # We got multiple search results
        if response["total"] >= 2:
            return SearchResult(results=response, error=False)

        # We got a single response back, go directly to the prompt
        if response["total"] == 1:
            d = date.fromisoformat(response["prompts"][0]["date"])
            return SearchResult(
                url=url_for("root.view_date", d=d.isoformat()), error=False
            )

    # No search results were returned
    return SearchResult(
        msg=(
            f"We were unable to find prompts containing '{query}'. "
            "Please try using a different term."
        ),
        url=url_for("search.index"),
        error=True,
    )


@search.get("/")
def index():
    render_opts = {
        "form_date": forms.PromptSearchByDate(),
        "form_host": forms.PromptSearchByHost(),
        "form_word": forms.PromptSearchByWord(),
    }
    return render_template("search/search.html", **render_opts)


@search.post("/do")
def do_search():
    search_types = {
        "date": forms.PromptSearchByDate(),
        "host": forms.PromptSearchByHost(),
        "word": forms.PromptSearchByWord(),
    }

    # Determine which search form was submitted
    if "type" in request.form and request.form["type"] in search_types:
        form = search_types[request.form["type"]]

        # Attempt to validate that form's data
        if form.validate_on_submit():
            return redirect(
                url_for(
                    "search.results", type=form.data["type"], query=form.data["query"]
                )
            )

    flash("Something happened and we couldn't search that. Please try again.", "error")
    return redirect(url_for("search.index"))


@search.get("/results")
def results():
    """View the results of a search."""
    # Supported searches
    search_types = {"date": by_date, "host": by_host, "word": by_word}

    # We didn't get all the info we need to search
    if (
        "type" not in request.args
        or "query" not in request.args
        or request.args["type"] not in search_types
    ):
        flash(
            "Something happened and we couldn't search that. Please try again.",
            "error",
        )
        return redirect(url_for("search.index"))

    # Search the archive on the request type
    search_results = search_types[request.args["type"]](request.args["query"])

    # An error (either an actual error or no results) was raised while searching
    if search_results["error"]:
        flash(search_results["msg"], "error")
        return redirect(search_results["url"])

    # The search returned a URL to a different page
    if "url" in search_results:
        return redirect(search_results["url"])

    # If we're here without meeting the other conditions, it means
    # there are multiple results to our search and they should be shown
    render_opts = {
        "search_type": request.args["type"],
        "form_date": forms.PromptSearchByDate(),
        "form_host": forms.PromptSearchByHost(),
        "form_word": forms.PromptSearchByWord(),
    }

    render_opts.update(search_results["results"])
    return render_template("search/results.html", **render_opts)
