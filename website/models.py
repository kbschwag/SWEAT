from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    browser = db.Column(db.String(150))
    consent = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intent = db.Column(db.String(150), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    categ = db.Column(db.Text, nullable=True)
    browser = db.Column(db.String(150), unique=False)
    consent = db.Column(db.String(150), unique=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class Browsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    categ = db.Column(db.Text, nullable=True)
    browser = db.Column(db.Text, nullable=True)
    consent = db.Column(db.Text, nullable=True)


class Consents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    categ = db.Column(db.Text, nullable=True)
    browser = db.Column(db.Text, nullable=True)
    consent = db.Column(db.Text, nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
