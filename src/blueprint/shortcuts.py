from flask import current_app, redirect, url_for

from src.blueprint import bp_shortcuts as shortcuts


@shortcuts.route("today")
def today():
    """Shortcut link to latest Prompt."""
    return redirect(url_for("root.index"))


@shortcuts.route("privacy")
def privacy():
    """Shortcut link to site privacy notice."""
    return redirect(url_for("root.about", _anchor="privacy"))


@shortcuts.route("abuse")
def abuse():
    """Shortcut link to file an email complaint."""
    return redirect(f'mailto:{current_app.config["ABUSE_EMAIL_ADDR"]}')
