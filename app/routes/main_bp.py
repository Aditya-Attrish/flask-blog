from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from app.models.posts import BlogPost
from app.models.contact import Contact
from app.extensions import db, params

main_bp = Blueprint('/', __name__, template_folder='../templates', static_folder='../static')

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = params["no_of_per_page"]  # Adjust as needed
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('index.html', posts=posts, params=params)


@main_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = Contact(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()

    return render_template('contact.html', params=params)


@main_bp.route("/about")
def about():
    return render_template('about.html', params=params)


@main_bp.route('/post/<int:post_sno>')
def post(post_sno):
    post = BlogPost.query.get(post_sno)
    return render_template('post.html', post=post, params=params)
