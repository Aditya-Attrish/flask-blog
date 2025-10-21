from flask import Blueprint, json, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.utils.uploader import upload_image
from app.models.user import User
from app.forms.profile_form import ProfileForm
from app.models.posts import BlogPost
from app.extensions import db, params
import os

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@login_required
def admin():
    return render_template("admin.html", params=params)

@user_bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    # Get user's published posts with pagination
    page = request.args.get('page', 1, type=int)
    per_page = params["no_of_per_page"]

    posts_query = BlogPost.query.filter_by(
        author=user, 
        status='published'
    ).order_by(BlogPost.publish_date.desc())

    posts = posts_query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )

    # Get user statistics
    stats = {
        'total_posts': BlogPost.query.filter_by(author=user, status='published').count(),
        'total_views': db.session.query(db.func.sum(BlogPost.views)).filter_by(author=user).scalar() or 0,
        'total_likes': 0,
        'member_since': user.created_at.strftime('%B %Y'),
        'last_active': user.last_seen.strftime('%B %d, %Y') if user.last_seen else 'Recently'
    }

    # Get popular posts
    popular_posts = BlogPost.query.filter_by(
        author=user, 
        status='published'
    ).order_by(BlogPost.views.desc()).limit(3).all()
    
    return render_template('profile.html', user=user,
                           posts=posts,
                           stats=stats,
                           popular_posts=popular_posts,
                           params=params)

@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        
        current_user.twitter_url = form.twitter_url.data
        current_user.linkedin_url = form.linkedin_url.data
        current_user.github_url = form.github_url.data
        current_user.instagram_url = form.instagram_url.data
        
        current_user.newsletter = form.newsletter.data
        current_user.public_profile = form.public_profile.data
        current_user.email_notifications = form.email_notifications.data

        db.session.commit()

        return redirect(url_for('user.profile', username=current_user.username))

    return render_template('edit_profile.html',params=params, form=form)

@user_bp.route('/add', methods=['GET','POST'])
@login_required
def add():    
    return render_template('add_blog.html', params=params)

@user_bp.route('/edit/<int:sno>')
def edit(sno):
    post = BlogPost.query.filter_by(sno=sno).first()
    return render_template('edit_blog.html', post=post, sno=sno, params=params)

