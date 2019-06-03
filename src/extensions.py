from flask_wtf.csrf import CSRFProtect
from src.core.database import create_new_database


csrf = CSRFProtect()


def init_extensions(app):
    # Load app extensions
    csrf.init_app(app)

    # If a database is needed, one will be made
    create_new_database()
