from flask import current_app, redirect, url_for

from src.blueprints import shortcuts


@shortcuts.get("today")
def today():
    """Shortcut link to latest Prompt."""
    return redirect(url_for("root.index"))


@shortcuts.get("privacy")
def privacy():
    """Shortcut link to site privacy notice."""
    return redirect(url_for("root.about", _anchor="privacy"))


@shortcuts.get("abuse")
def abuse():
    """Shortcut link to file an email complaint."""
    return redirect(f'mailto:{current_app.config["ABUSE_EMAIL_ADDR"]}')
