from datetime import datetime
from typing import Callable, Dict

from flask import current_app, render_template


@current_app.context_processor
def inject_current_date() -> Dict[str, datetime]:
    return {"current_date": datetime.now()}


@current_app.context_processor
def nav_cur_page() -> Dict[str, Callable]:
    return {
        "nav_cur_page": lambda title, has: (
            "active" if has.strip() in title.strip().lower() else ""
        )
    }


@current_app.context_processor
def create_url() -> Dict[str, Callable]:
    def _make(prompt: dict) -> str:
        return "https://twitter.com/{0}/status/{1}".format(
            prompt["writer_handle"], prompt["id"]
        )

    return {"create_url": _make}


@current_app.errorhandler(404)
def page_not_found(exc) -> tuple:
    return render_template("partials/errors/404.html"), 404


@current_app.errorhandler(500)
def server_error(exc) -> tuple:
    return render_template("partials/errors/500.html"), 500
