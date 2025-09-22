from flask import Flask, render_template
from .config import Config
from app.extensions import csrf
from app.extensions import db, login_manager
from app.models.user import User


def create_app(class_object=Config):
    app = Flask(__name__)

    # Configure the app
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    # app.config['SECRET_KEY'] = 'super-secret-key'
    app.config.from_object(class_object)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import blueprints
    from app.routes.user_bp import user_bp
    from app.routes.api_blogs_bp import blogs_bp
    from app.routes.auth_bp import auth_bp
    from app.routes.main_bp import main_bp
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blogs_bp, url_prefix='/api/blogs')
    app.register_blueprint(user_bp, url_prefix='/user')

    # 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')
  
    return app