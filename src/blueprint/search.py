from datetime import date

from flask import Blueprint, request
from flask import abort, redirect, render_template, url_for

from src.core.form import PromptSearchForm


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
            date.fromisoformat(query)
            return redirect(url_for("root.date", date=query))

        # We got a word or partial word to search
        except ValueError:
            pass
