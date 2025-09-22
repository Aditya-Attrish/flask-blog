from flask import Blueprint, jsonify, request, redirect, flash, abort
from flask_login import login_required, current_user
from flask_wtf.csrf import validate_csrf
from app.models.posts import BlogPost
from app.utils.uploader import upload_image
from app.utils.helper import generate_slug
from app.extensions import db


blogs_bp = Blueprint('api_blogs', __name__, url_prefix='/api')

# @blogs_bp.route('/')
# def index():
#     # Fetch all blog posts with status 'published', order by publish_date and paginate
#     page = request.args.get('page', 1, type=int)
#     posts = BlogPost.query.filter_by(status='published').order_by(BlogPost.publish_date.desc()).paginate(page=page, per_page=params['post_per_page'])
#     return render_template('blogs.html', posts=posts, params=params)

# @blogs_bp.route('/post/<string:slug>')
# def post(slug):
#     post = BlogPost.query.filter_by(slug=slug).first()
#     if not post:
#         abort(404)
#     return render_template('post.html', post=post, params=params)

@blogs_bp.route('/blogs', methods=['POST'])
@login_required
def create_update_post():
  try:
    # Validate CSRF token
    validate_csrf(request.headers.get('X-CSRFToken'))
    # Check if it's an update or create
    is_update = request.method == 'PUT'
    post_id = request.args.get('id') if is_update else None

    if is_update and post_id:
        post = BlogPost.query.get_or_404(post_id)
        if post.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Permission denied'}), 403
    else:
        post = BlogPost()
        post.user_id = current_user.id

    # Get form data
    post.title = request.form.get('title', '').strip()
    post.excerpt = request.form.get('excerpt', '').strip()
    post.content = request.form.get('content', '').strip()
    post.category = request.form.get('category', '').strip()
    # post.tags = request.form.get('tags', '')
    post.slug = request.form.get('slug', '').strip()
    post.meta_description = request.form.get('meta_description', '').strip()
    post.status = request.form.get('status', 'draft')
    
  # Handle file upload
    if 'featured_image' in request.files:
      file = request.files['featured_image']
      post.thumbnail = upload_image(file, folder_name='thumbnail', current_img=post.thumbnail)

    if not is_update:
      if not post.slug:
        post.slug = generate_slug(post.title)
      db.session.add(post)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Post created successfully', 'post_slug': post.slug}), 200
  except Exception as e:
    return jsonify({'success': False, 'message': str(e)}), 500