from flask import redirect, url_for

from src.blueprint import bp_shortcuts as shortcuts


@shortcuts.route("/privacy")
def privacy():
    return redirect(url_for("root.about", _anchor="privacy"))
