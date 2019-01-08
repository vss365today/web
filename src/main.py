from flask import Flask

from src.extensions import init_extensions
from src.blueprint import blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint.bp)
    init_extensions(app)

    @app.context_processor
    def inject_site_title():
        return {"site_title": app.config["SITE_TITLE"]}

    return app
