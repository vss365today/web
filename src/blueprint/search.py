from flask import Blueprint
from flask import abort, render_template


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("/")
def index():
    abort(404)
    return render_template("search/search.html")


@bp.route("/<string:word>")
def word_search(word: str):
    abort(404)
