from flask import Blueprint
from flask import abort


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("/")
def index():
    abort(404)


@bp.route("/<string:word>")
def word_search(word: str):
    abort(404)
