from flask import Blueprint, json, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.utils.uploader import upload_image
from app.utils.helper import generate_slug
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
    if (request.method == 'POST'):
        try:
            # Rollback any existing transaction to clear the error
            db.session.rollback()
            
            # Get form data
            title = request.form.get('title')
            excerpt = request.form.get('excerpt')
            content = request.form.get('content')
            category = request.form.get('category')
            tags = request.form.get('tags', '')
            slug = request.form.get('slug')
            meta_description = request.form.get('meta_description')
            status = request.form.get('status')
            publish_date = request.form.get('publish_date')

            # Handle file upload
            featured_image = request.files.get('featured_image')
            featured_image = upload_image(featured_image, folder_name='thumbnail', current_img='')
            if not featured_image:
                flash('Featured image is required', 'error')
                return render_template('add_blog.html')

            # Save to database (pseudo-code)
            blog_post = BlogPost(
                title=title,
                excerpt=excerpt,
                content=content,
                category=category,
                #tags=tags.split(','),
                slug=slug or generate_slug(title),
                meta_description=meta_description,
                thumbnail=featured_image,
                user_id=current_user.id,
                status=status
            )

            # Save to database (you would use your actual database model)
            db.session.add(blog_post)
            db.session.commit()
                
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('/.post', slug=blog_post.slug))
        except Exception as e:
            flash(f'Error creating post: {str(e)}', 'error')
        
    return render_template('add_blog.html', params=params)

@user_bp.route('/edit/<int:sno>', methods=['GET','POST'])
def edit(sno):
  if (request.method == 'POST'):
      #slug = request.form.get('slug')
      title = request.form.get('title')
      file = request.files['thumbnail']
      con = request.form.get('content')
      if sno == 0:
          thumb = upload_image(file, folder_name='thumb', current_img='')
          post = BlogPost(title=title,
                          content=con,
                          thumb=thumb,
                          author=current_user)
          db.session.add(post)
          db.session.commit()
      else:
          post = BlogPost.query.filter_by(sno=sno).first()
          #post.slug=slug
          post.title = title
          post.thumb = upload_image(file, folder_name='thumb', current_img=post.thumb)
          post.content = con
          db.session.commit()
      return redirect(url_for('user.admin'))
  post = BlogPost.query.filter_by(sno=sno).first()
  return render_template('Edit.html', post=post, sno=sno, params=params)

@user_bp.route('/deletePost' , methods=['DELETE'])
def deletePost():
    post_sno = request.json.get('post_sno')
    print("delete", post_sno)
    post = BlogPost.query.get_or_404(int(post_sno))
    if not post:
        return jsonify({'error': 'Post not found'})

    # Check if the current user is the author of the post
    if post.user_id != current_user.id:
        abort(403)

    file_path = os.path.join('./app/static/', post.thumbnail)
    if os.path.isfile(file_path):
        os.remove(file_path)
    db.session.delete(post)
    db.session.commit()

    flash('Your blog post has been deleted!', 'success')
    return jsonify({'message': 'Post deleted successfully'})