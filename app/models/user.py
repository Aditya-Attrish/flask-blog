from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Profile fields
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    avatar = db.Column(db.String(100), default='avatar/default-user.jpg')
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))

    # Social links
    twitter_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    instagram_url = db.Column(db.String(200))

    # Preferences
    newsletter = db.Column(db.Boolean, default=True)
    public_profile = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)

    # Timestamps
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    profile_updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
  
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def create_user(username, email, password):
        try:
            """ checks if user already exists """
            user = User.query.filter_by(email=email).first()
            if user:
                raise ValueError("User already exists")
            
            """Helper method to create a new user"""
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None