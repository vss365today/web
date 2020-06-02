from flask_google_fonts import GoogleFonts
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
fonts = GoogleFonts()


def init_extensions(app):
    """Load app extensions."""
    csrf.init_app(app)
    fonts.init_app(app)
