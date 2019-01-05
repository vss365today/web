
from datetime import datetime

from flask import Blueprint
from flask import render_template

bp = Blueprint("root", __name__, url_prefix="")


@bp.route("/form", methods=["POST"])
def form() -> str:
    return "form"


@bp.route("/")
@bp.route("/today")
def index() -> str:
    date = datetime.today().strftime("%d %B, %Y")
    return render_template("word.html", date=date)


@bp.route("/<date>")
def date(date) -> str:
    return render_template("word.html", date="")
