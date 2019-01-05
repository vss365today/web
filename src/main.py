from flask import Flask

from src.blueprint import blueprint
from src.extensions import init_extensions


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint.bp)
    init_extensions(app)

    return app
