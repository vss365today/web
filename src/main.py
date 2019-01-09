from flask import Flask

from src.blueprint import blueprint
from src.extensions import init_extensions


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint.bp)
    init_extensions(app)

    @app.context_processor
    def inject_site_title():
        return {"site_title": app.config["SITE_TITLE"]}

    return app
