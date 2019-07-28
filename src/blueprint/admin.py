from flask import Blueprint
from flask import abort


bp = Blueprint("admin", __name__, url_prefix="")


@bp.route("/admin")
def index():
    abort(500)
