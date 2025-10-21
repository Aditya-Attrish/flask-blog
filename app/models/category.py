from app.extensions import db

class Category(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), unique=True, nullable=False)
   description = db.Column(db.String(200), nullable=True)
   icon = db.Column(db.String(50), nullable=True)
   is_active = db.Column(db.Boolean, default=True)
   posts = db.relationship('BlogPost', backref='category', lazy=True)
   created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  