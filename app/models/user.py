from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userImg = db.Column(db.String(50), default='userImg/default-user.jpg')
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    posts = db.relationship('BlogPost', backref='author', lazy=True)
  
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

