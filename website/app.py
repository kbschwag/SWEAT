from flask import Flask
from flask_login import LoginManager
from routes.views import views
from routes.auth import auth
from routes.admin import admin
from os import getenv
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"

# Selects the database based on the environment (allows dev to use sqlite and prod to use postgres)
# Also chooses the domain to use for the app (localhost:5000 or sweat.io)
if getenv('FLASK_ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SERVER_NAME'] = 'localhost:5000'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SERVER_NAME'] = 'sweat.io'

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(admin, url_prefix="/")


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))