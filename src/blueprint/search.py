from datetime import date as date_obj

from flask import Blueprint, request
from flask import abort, redirect, render_template, url_for
import requests

from src.core.form import PromptSearchForm
from src.core.filters import create_api_date
from src.core.helpers import create_api_url


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("/", methods=["GET"])
def index():
    abort(404)
    render_opts = {
        "form": PromptSearchForm()
    }
    return render_template("search/search.html", **render_opts)


@bp.route("/form", methods=["POST"])
def query_search():
    abort(404)

    # We got a valid form submission
    search_form = PromptSearchForm()
    if search_form.validate_on_submit():
        query = request.form.get("query").strip()

        try:
            # We recieved an exact (and valid) date, redirect to it
            valid = date_obj.fromisoformat(query)  # noqa
            del valid
            return redirect(url_for("root.date", date=query))

        # We got a word or partial word to search
        except ValueError:
            # Connect to the API to search
            r = requests.get(
                create_api_url("search"),
                params={"prompt": query}
            )

            # We got a successful response
            if r.ok:
                response = r.json()

                # We got many search results
                if response["total"] >= 2:
                    return {}

                # We got a single response back, go directly to the prompt
                elif response["total"] == 1:
                    date = create_api_date(response["prompts"][0]["date"])
                    date = date.strftime("%Y-%m-%d")
                    return redirect(url_for("root.date", date=date))

                # No search results were returned
                else:
                    return {}

            # The search was not successful
            return r.json()
