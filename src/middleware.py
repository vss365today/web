from datetime import datetime
from typing import Callable, Dict

from flask import current_app, render_template, url_for


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
    def _func(prompt: dict) -> str:
        return "https://twitter.com/{0}/status/{1}".format(
            prompt["writer_handle"], prompt["id"]
        )

    return {"create_url": _func}


@current_app.context_processor
def get_static_url() -> Dict[str, Callable]:
    def _func(filename: str) -> str:
        # TODO Docstring
        # If this config key is present, we are running in prod,
        # which means we should pull the files from a URL
        if (static_url := current_app.config.get("STATIC_FILES_URL")) is not None:
            return f"{static_url}/{filename}"

        # Otherwise, we're running locally, so we pull the files
        # from the local filesystem
        else:
            return url_for("static", filename=filename)

    return {"get_static_url": _func}


@current_app.errorhandler(404)
def page_not_found(exc) -> tuple:
    return render_template("partials/errors/404.html"), 404


@current_app.errorhandler(500)
def server_error(exc) -> tuple:
    return render_template("partials/errors/500.html"), 500
