from datetime import date
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from src.blueprint import main, admin
from src.core.filters import create_tweet_url
from src.extensions import init_extensions


def create_app():
    app = Flask(__name__)
    # https://stackoverflow.com/a/45333882
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)
    init_extensions(app)

    @app.context_processor
    def inject_site_title():
        return {"site_title": "#vss365 today"}

    @app.context_processor
    def inject_current_date():
        return {"current_date": date.today()}

    @app.context_processor
    def nav_cur_page():
        return {
            "nav_cur_page":
                lambda title, has: ("active" if has in title.lower() else "")
        }

    @app.context_processor
    def create_url():
        return {"create_url": lambda tweet: create_tweet_url(tweet)}

    return app
