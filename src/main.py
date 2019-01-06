from flask import Flask

from src.extensions import init_extensions
from src.blueprint import blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint.bp)
    init_extensions(app)

    return app
