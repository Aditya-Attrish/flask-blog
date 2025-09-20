from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from app.models.posts import BlogPost
from app.models.contact import Contact
from app.extensions import db, params

main_bp = Blueprint('/', __name__)

@main_bp.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = params["no_of_per_page"]  # Adjust as needed
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('home.html', posts=posts, params=params)

@main_bp.route("/blogs")
def blogs():
    page = request.args.get('page', 1, type=int)
    per_page = params["no_of_per_page"]  # Adjust as needed
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    # Sample data for sidebar (you would replace this with actual database queries)
    categories = [
        {'name': 'Technology', 'icon': 'laptop', 'count': 45},
        {'name': 'Lifestyle', 'icon': 'heart', 'count': 32},
        {'name': 'Travel', 'icon': 'geo-alt', 'count': 28},
        {'name': 'Business', 'icon': 'graph-up', 'count': 38},
        {'name': 'Health', 'icon': 'activity', 'count': 29}
    ]

    popular_posts = [
        {
            'title': 'AI Revolution: What to Expect in 2024',
            'image': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=150&auto=format',
            'date': '2 days ago'
        },
        {
            'title': '10 Productivity Hacks That Changed My Life',
            'image': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=150&auto=format',
            'date': '5 days ago'
        }
    ]

    tags = ['technology', 'webdev', 'python', 'javascript', 'design', 'startup', 'productivity']

    return render_template('blogs.html',
                           posts=posts,
                           params=params,
                           categories=categories,
                           popular_posts=popular_posts,
                           tags=tags)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = params["no_of_per_page"]
    
    # If no query, show recent posts or empty results
    results = BlogPost.query.filter_by(status='published').order_by(
            BlogPost.publish_date.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('search.html', 
                            params=params,
                             results=results, 
                             query=query,
                             search_performed=False)

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


@main_bp.route('/post/<slug>')
def post(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post, params=params)
