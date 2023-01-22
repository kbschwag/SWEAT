from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, User
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import RecaptchaField
from flask import *
from flask_recaptcha import ReCaptcha
from werkzeug.security import generate_password_hash, check_password_hash
import  re
import requests

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        recaptcha = RecaptchaField()

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        match = re.fullmatch(regex, email)
        captcha_response = request.form['g-recaptcha-response']
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif match is None:
            flash('Email is invalid, the pattern should be real email address.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 5:
            flash('password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error')
        else:
            if is_human(captcha_response):
                # Process request here
                status = "Detail submitted successfully."
                flash(status)
                new_user = User(email=email, username=username,
                                password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('User created!', category='success')
                return redirect(url_for('views.home'))
            elif (1 == 1):
                # Log invalid attempts
                status = "Sorry ! Bots are not allowed."
                flash(status, category='error')

    return render_template("signup.html", user=current_user)

def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = "6Lf2mcMhAAAAALsvyxebf4_d8gSHDE5ZkYa3hNpo"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
