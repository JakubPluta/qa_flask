from qaf import models
from qaf.routes.main import main
from qaf.routes.auth import auth
from qaf import db
from qaf.models import User
from qaf import create_app

app = create_app()




with app.app_context():
    print(db.engine.table_names())
    print(User.query.all())
    user = User()