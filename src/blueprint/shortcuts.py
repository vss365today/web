from flask import redirect, url_for

from src.blueprint import bp_shortcuts as shortcuts


@shortcuts.route("today")
def today():
    """Shortcut link to latest prompt."""
    return redirect(url_for("root.index"))


@shortcuts.route("privacy")
def privacy():
    """Shortcut link to site privacy notice."""
    return redirect(url_for("root.about", _anchor="privacy"))
