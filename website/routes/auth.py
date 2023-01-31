from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, json
from ..models import db, User, Verification
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import  re
import requests
import secrets
from ..mail.mail import send_templated_email

auth = Blueprint("auth", __name__)
    
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

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

@auth.route("/forgot-password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(16)
            new_verification = Verification(user_id=user.id, intent="reset-password", token=token)
            db.session.add(new_verification)

            send_templated_email(
                email,
                "forgot_password.html",
                {
                    "subject": "Reset your password",
                    "link": url_for('auth.reset_password', token=token, _external=True)
                }
            )

            db.session.commit()

            flash('Check your email for instructions.', category='success')
        else:
            flash('Email does not exist.', category='error')

    return render_template("forgot_password.html", user=current_user)

@auth.route("/reset-password", methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        token = request.args.get('token')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        verification = Verification.query.filter_by(token=token, intent="reset-password").first()

        if verification:
            if password1 != password2:
                flash('Passwords don\'t match!', category='error')
            elif len(password1) < 5:
                flash('password is too short.', category='error')
            else:
                user = User.query.filter_by(id=verification.user_id).first()
                user.password = generate_password_hash(password1, method='sha256')
                db.session.delete(verification)
                db.session.commit()
                flash('Password changed.', category='success')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid token.', category='error')

    return render_template("reset_password.html", user=current_user)

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
                
                token = secrets.token_urlsafe(16)
                new_verification = Verification(user_id=new_user.id, intent="verify-email", token=token)
                db.session.add(new_verification)

                send_templated_email(
                    email,
                    "new_user.html",
                    {
                        "subject": "Verify your email",
                        "link": url_for('auth.verify_email', token=token,  _external=True)
                    }
                )

                db.session.commit()

                login_user(new_user, remember=True)
                flash('Success! Verify your email before posting.', category='success')
                return redirect(url_for('views.home'))
            else:
                # Log invalid attempts
                status = "Sorry ! Bots are not allowed."
                flash(status, category='error')

    return render_template("signup.html", user=current_user)

@auth.route("/verify-email", methods=['GET', 'POST'])
def verify_email():
    token = request.args.get('token')
    verification = Verification.query.filter_by(token=token, intent="verify-email").first()
    if verification:
        user = User.query.filter_by(id=verification.user_id).first()
        user.email_confirmed = True
        db.session.delete(verification)
        db.session.commit()
        flash('Email verified!', category='success')
        return redirect(url_for('views.home'))
    else:
        flash('Invalid token!', category='error')
        return redirect(url_for('views.home'))

def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    if current_app.config['ENV'] == 'development':
        return True
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
