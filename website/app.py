from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from views import views
from auth import auth
from models import User

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))