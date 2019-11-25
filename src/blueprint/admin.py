from flask import Blueprint
from flask import abort


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    abort(404)


@bp.route("/config")
def config():
    abort(404)


@bp.route("/prompts/edit/<str:prompt_date>")
def prompt_edit(prompt_date: str):
    abort(404)


@bp.route("/writers")
def writers():
    abort(404)


@bp.route("/writers/edit/<int:writer_id>")
def writer_edit(writer_id: int):
    abort(404)
