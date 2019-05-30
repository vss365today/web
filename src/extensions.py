from flask_wtf.csrf import CSRFProtect

from src.core.database import create_new_database
from src.core.helpers import load_env_vals


csrf = CSRFProtect()


def init_extensions(app):
    # Load app extensions
    app.config.update(load_env_vals())
    csrf.init_app(app)

    # If a database is needed, one will be made
    create_new_database()
