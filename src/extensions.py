from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def init_extensions(app):
    """Load app extensions."""
    csrf.init_app(app)
