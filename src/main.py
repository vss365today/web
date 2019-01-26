from datetime import date
from flask import Flask

from src.blueprint import blueprint
from src.core.filters import create_tweet_url
from src.extensions import init_extensions


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint.bp)
    init_extensions(app)

    @app.context_processor
    def inject_site_title():
        return {"site_title": app.config["SITE_TITLE"]}

    @app.context_processor
    def inject_current_year():
        return {"current_year": date.today().year}

    @app.context_processor
    def create_url():
        return {"create_url": lambda tweet: create_tweet_url(tweet)}

    return app
