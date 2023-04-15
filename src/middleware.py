from datetime import date

from flask import current_app, flash, render_template, request
from src.core.helpers import get_static_url


@current_app.before_request
def global_alert():
    # Display a global alert message if
    # 1. We have one to display
    # 2. We are loading a route and not anything else
    # 3. We aren't coming from a shortcut (which are redirects)
    if (
        (alert_msg := current_app.config.get("GLOBAL_ALERT")) is not None
        and request.blueprint
        and request.blueprint != "shortcuts"
    ):
        flash(alert_msg[0], alert_msg[1])


@current_app.context_processor
def inject_context() -> dict:
    return {
        "current_date": date.today(),
        "get_static_url": get_static_url,
        "nav_cur_page": lambda title, has: (
            "active" if has.strip() in title.strip().lower() else ""
        ),
    }


@current_app.errorhandler(404)
def page_not_found(exc) -> tuple:
    return render_template("partials/errors/404.html"), 404


@current_app.errorhandler(500)
def server_error(exc) -> tuple:
    return render_template("partials/errors/500.html"), 500
