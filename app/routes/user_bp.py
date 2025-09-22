from flask import Blueprint, json, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.utils.uploader import upload_image, remove_image
from app.models.user import User
from app.models.posts import BlogPost
from app.extensions import db, params
import os

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@login_required
def admin():
    return render_template("admin.html", params=params)

@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        email = request.form['email']
        file = request.files['userImg']
        # Update the user's profile information
        current_user.username = username
        current_user.email = email
        current_user.userImg = upload_image(file, folder_name='userImg', current_img=current_user.userImg)
        db.session.commit()

        return redirect(url_for('user.admin'))

    return render_template('edit_profile.html',params=params)

@user_bp.route('/add', methods=['GET','POST'])
@login_required
def add():    
    return render_template('add_blog.html', params=params)

@user_bp.route('/edit/<int:sno>')
def edit(sno):
    post = BlogPost.query.filter_by(sno=sno).first()
    return render_template('edit_blog.html', post=post, sno=sno, params=params)

@user_bp.route('/deletePost/<int:post_sno>', methods=['DELETE'])
@login_required
def deletePost(post_sno):
    post = BlogPost.query.get_or_404(post_sno)
    if not post:
        return jsonify({ 'success': False, 'message': "Post not found"}), 404
    # Check if the current user is the author of the post
    if post.user_id != current_user.id:
        return jsonify({ 'success': False, 'message': "You are not authorized to delete this post"}), 403

    remove_image(post.thumbnail)
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'success': True, 'message': "Post deleted successfully"}), 200