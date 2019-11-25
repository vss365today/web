from flask import Blueprint
from flask import abort, render_template


from src.core.form import PromptSearchForm


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("/")
def index():
    abort(404)
    render_opts = {
        "form": PromptSearchForm()
    }
    return render_template("search/search.html", **render_opts)


@bp.route("/<string:word>")
def word_search(word: str):
    abort(404)
