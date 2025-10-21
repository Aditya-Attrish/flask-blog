from app.__init__ import create_app
from app.extensions import db

app = create_app()

# Initialize database tables
with app.app_context():
    db.create_all()

# This is for Vercel
if __name__ == '__main__':
    app.run()