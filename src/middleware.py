from datetime import date

from flask import current_app, flash, render_template, request, url_for


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


def get_static_url(filename: str) -> str:
    """Generate a URL to static assets based on dev/prod status."""
    # If this config key is present, we are running in prod,
    # which means we should pull the files from a URL
    if (static_url := current_app.config.get("STATIC_FILES_URL")) is not None:
        return f"{static_url}/{filename}"

    # Otherwise, we're running locally, so we pull the files
    # from the local filesystem
    return url_for("static", filename=filename)


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
