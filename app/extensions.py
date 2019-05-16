from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_login import LoginManager
from flask_ckeditor import CKEditor


csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
ckeditor = CKEditor(app)


@login_manager.user_loader
def load_user(user_id):
    from .model import User
    user = User.query.get(int(user_id))
    return user

