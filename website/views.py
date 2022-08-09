from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")

def home():
    return render_template("home.html", user=current_user)

@views.route("/about_us")

def about():
    return render_template("about_us.html", user=current_user)

@views.route("/community_guidelines")

def community_guidelines():
    return render_template("community_guidelines.html", user=current_user)


@views.route("/view_posts/", methods = ["GET"])
@login_required
def view_posts():
    posts = Post.query.all()
    return render_template("view_posts.html", user=current_user, posts=posts)

# get post is how we input data into the back end
@views.route("/create-post", methods=['GET', 'POST'])

@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        categ = request.form.get('categ')
        browser = request.form.get('browser')

        if not text:
            flash('Enter the details', category='error')
        else:
            post = Post(text=text,categ=categ,author=current_user.id,browser=browser)
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
    elif current_user.id == post.id:
        flash('You do not have permission to delete this post.', category='error')
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
    posts=Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment box cannot be empty', category='error')
    else:
        return redirct(url_for('views.home'))