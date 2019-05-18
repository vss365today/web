from flask_wtf.csrf import CSRFProtect

from src.core.helpers import load_env_vals


csrf = CSRFProtect()


def init_extensions(app):
    # Load app extensions
    app.config.update(load_env_vals())
    csrf.init_app(app)
