from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.uploader import upload_thumbnail, upload_profile_photo
from app.models.user import User
from app.models.posts import BlogPost
from app.extensions import db, params

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def admin():
    return render_template("admin.html", params=params)

@user_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
  def edit_profile():
    if request.method == 'POST':
        # Handle profile photo upload
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file.filename != current_user.userImg:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app['UPOAD_USERIMG'], filename))
                # Save the filename to the user's profile in the database
                user = User.query.filter_by(id=current_user.id).first()
                user.userImg = filename
                user.username = request.form.get('username')
                db.session.commit()

        return redirect(url_for('admin'))

    return render_template('edit_profile.html',params=params)

@user_bp.route('/edit/<int:sno>', methods=['GET','POST'])
def edit(sno):
  if (request.method == 'POST'):
      #slug = request.form.get('slug')
      title = request.form.get('title')
      file = request.files['thumbnail']
      con = request.form.get('content')
      thumb = f"thumb/{file.filename}"
      upload_thumbnail(file)
      # if not os.path.exists(Path):
      #     os.makedirs(Path)
      if sno == 0:
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
          post.thumb = thumb
          post.content = con
          db.session.commit()
      return redirect("/user")
  post = BlogPost.query.filter_by(sno=sno).first()
  return render_template('Edit.html', post=post, sno=sno, params=params)

@user_bp.route('/delete/<int:post_sno>')
@login_required
def delete(post_sno):
    post = BlogPost.query.get_or_404(post_sno)

    # Check if the current user is the author of the post
    if post.author != current_user:
        abort(403)  # Forbidden

    file_path = app.config['UPOAD_THUMB'] + post.thumb
    if os.path.isfile(file_path):
        os.remove(file_path)
    db.session.delete(post)
    db.session.commit()

    flash('Your blog post has been deleted!', 'success')
    return redirect('/user')