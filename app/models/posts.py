from app.extensions import db
from datetime import datetime
from app.models.comment import Comment

# Define BlogPost model
class BlogPost(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    excerpt = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    meta_description = db.Column(db.String(160), nullable=False)
    thumbnail = db.Column(db.String(50),nullable=False)
    status = db.Column(db.String(40), nullable=False)
    views = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)