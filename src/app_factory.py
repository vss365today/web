from importlib import import_module

from datetime import datetime
from flask import Flask

from src.blueprint import all_blueprints
from src.extensions import init_extensions


def create_app():
    app = Flask(__name__)
    init_extensions(app)

    # Register all of the blueprints
    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)

    @app.context_processor
    def inject_current_date():
        return {"current_date": datetime.now()}

    @app.context_processor
    def nav_cur_page():
        return {
            "nav_cur_page": lambda title, has: (
                "active" if has.strip() in title.strip().lower() else ""
            )
        }

    @app.context_processor
    def create_url():
        def _make(prompt: dict) -> str:
            return "https://twitter.com/{0}/status/{1}".format(
                prompt["writer_handle"], prompt["id"]
            )

        return {"create_url": _make}

    return app
