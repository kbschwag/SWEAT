from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from ..models import Post, Report, User, db
from os import getenv
admin = Blueprint('admin', __name__)

@login_required
@admin.route('/reported-posts')
def reported_posts():
    if (current_user.role != 'admin'):
        flash('You do not have permission to view this page', 'error')
        return redirect(url_for('views.view_posts'))
    # find all posts that have at least 1 report
    posts = Post.query.join(Report).all()
    return render_template('admin_posts.html', user=current_user, posts=posts)

@login_required
@admin.route('/void-reports/<id>')
def void_reports(id):
    callback_url = request.args.get('callback_url')
    if (current_user.role != 'admin'):
        flash('You do not have permission to view this page', 'error')
        return redirect(url_for('views.view_posts'))
    # find all reports for this post
    reports = Report.query.filter_by(post_id=id).all()
    for report in reports:
        db.session.delete(report)
    db.session.commit()
    flash('Reports voided', category='success')
    return redirect(url_for('admin.reported_posts') or callback_url)

@admin.route('/adminify/<username>')
def adminify(username):
    if getenv("FLASK_ENV") != "development":
        flash('You do not have permission to view this page', 'error')
        return redirect(url_for('views.view_posts'))
    user = User.query.filter_by(username=username).first()
    user.role = 'admin'
    db.session.commit()
    flash(f'User {username} is now an admin', category='success')
    return redirect(url_for('views.view_posts'))