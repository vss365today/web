from flask_wtf.csrf import CSRFProtect

from src.core.config import load_app_config

csrf = CSRFProtect()


def init_extensions(app):
    # Load app extensions
    app.config.update(load_app_config())
    csrf.init_app(app)
