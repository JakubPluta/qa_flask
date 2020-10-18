from flask import Flask
from .extensions import login_manager, db
from .commands import create_tables
from .routes import main
from .models import User, Question

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = ''

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    app.register_blueprint(main)
    app.cli.add_command(create_tables)

    return app