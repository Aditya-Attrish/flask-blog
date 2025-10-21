import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    # Use PostgreSQL URL from environment variable in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    
    # Static configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/userImg')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
  