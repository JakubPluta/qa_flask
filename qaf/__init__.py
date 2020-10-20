from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_file='settings.py'):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from qaf.routes.auth import auth
    from qaf.routes.main import main

    app.register_blueprint(main)
    app.register_blueprint(auth)

    from .models import User, Question
    with app.app_context():
        db.create_all()  # Create sql tables for our data models

    return app

