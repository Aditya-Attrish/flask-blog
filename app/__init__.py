from flask import Flask
from app.extensions import db, login_manager
from app.models.user import User
from app.routes.user_bp import user_bp
from app.routes.auth_bp import auth_bp
from app.routes.main_bp import main_bp

def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SECRET_KEY'] = 'super-secret-key'

    # Initialize extensions
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 404 error handler
    @app.errorhandler(404)
    
  
    return app