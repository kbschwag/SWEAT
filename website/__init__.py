from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_wtf import RecaptchaField
from flask import *
from flask_recaptcha import ReCaptcha
from jinja2 import Markup

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf2mcMhAAAAAHPekK8_exQ5enP1db6kYKlevRyb'
    app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf2mcMhAAAAALsvyxebf4_d8gSHDE5ZkYa3hNpo'
    recaptcha = ReCaptcha(app)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")