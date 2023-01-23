from flask_wtf import Form, RecaptchaField
from flask_recaptcha import ReCaptcha
from flask import *
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import Post, User, Comment, Like, Browsers, Consents, db
from markupsafe import Markup
from jinja2.utils import markupsafe
from datetime import datetime, timedelta
markupsafe.Markup()
Markup('')
# from jinja2 import Markup

views = Blueprint("views", __name__)

app = Flask(__name__)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf2mcMhAAAAAHPekK8_exQ5enP1db6kYKlevRyb'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf2mcMhAAAAALsvyxebf4_d8gSHDE5ZkYa3hNpo'
recaptcha = ReCaptcha(app)


@views.route('/', methods=['GET', 'POST'])
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/about_us")
def about():
    return render_template("about_us.html", user=current_user)


@views.route("/terms")
def terms():
    return render_template("terms.html", user=current_user)


@views.route("/community_guidelines")
def community_guidelines():
    return render_template("community_guidelines.html", user=current_user)


@views.route("/contact-us")
@login_required
def contact():
    return render_template("contact-us.html", user=current_user)


@views.route("/view_posts/", methods=["GET"])
@login_required
def view_posts():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template("view_posts.html", user=current_user, posts=posts)


@views.route("/survey/")
def survey():
    return render_template("survey.html", user=current_user)


# get post is how we input data into the back end
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        categ = request.form.get('categ')
        browser = request.form.get('browser')
        consent = not request.form.get('consent')

        if not text:
            flash('Enter the details', category='error')
        else:
            if current_user.email_confirmed != True:
                flash('Please verify your email first.', category='error')
            elif Post.query.filter(Post.date_created > (datetime.now() - timedelta(minutes=1))).filter(Post.author == current_user.id).count() > 0:
                flash('You have already submitted a post in the last minute.', category='error')
            else:
                post = Post(text=text, categ=categ, author=current_user.id,
                            browser=browser, consent=consent)
                db.session.add(post)
                db.session.commit()
                flash('The data is submitted', category='success')
                return redirect(url_for('views.view_posts'))
    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', 'error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
    return redirect(url_for('views.view_posts'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.view_posts'))
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/posts_sorted/<browser>")
@login_required
def posts_sorted(browser):
    posts = Post.query.filter_by(browser=browser).all()
    if not sorted:
        flash('No user with that username broswer.', category='error')
        return redirect(url_for('views.view_posts'))
    # posts=Post.query.filter_by(browser=sorted.id).all()
    return render_template("posts_sorted.html", user=current_user, posts=posts, browser=browser)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment box cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist', category='error')

    return redirect(url_for('views.view_posts'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.view_posts'))


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})
