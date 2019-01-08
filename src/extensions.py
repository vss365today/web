from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from src.core.helpers import create_db_connection, load_env_vals


db = None
alchemy = SQLAlchemy()
csrf = CSRFProtect()
email = Mail()


def init_extensions(app):
    global db

    # Load app extensions
    app.config.update(load_env_vals())
    csrf.init_app(app)
    email.init_app(app)

    # Set the database connection
    connect_str, db = create_db_connection(app.config)
    app.config["SQLALCHEMY_DATABASE_URI"] = connect_str
    alchemy.init_app(app)
    db.connect()
