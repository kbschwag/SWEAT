from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_wtf import RecaptchaField
from flask import *
from flask_recaptcha import ReCaptcha
from markupsafe import Markup
from jinja2.utils import markupsafe
markupsafe.Markup()
Markup('')
#from jinja2 import Markup


db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

from views import views
from auth import auth

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

from models import User, Post, Comment, Like, Browsers, Consents
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))