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
    comments_count = db.Column(db.Integer, default=0)
    publish_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    
    @property
    def author_avatar(self):
        return self.author.userImg if self.author else '/static/userImg/default-user.jpg'
    
    @property 
    def author_name(self):
        return self.author.username if self.author else 'Unknown'

    def to_dict(self):
        return {
            'sno': self.sno,
            'excerpt': self.excerpt,
            'slug': self.slug,
            'title': self.title,
            'category': self.category,
            'content': self.content,
            'meta_description': self.meta_description,
            'thumbnail': self.thumbnail,
            'status': self.status,
            'views': self.views,
            'comments': self.comments,
            'publish_date': self.publish_date,
            'created_at': self.created_at,
            'user_id': self.user_id
        }