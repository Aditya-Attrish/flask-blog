from app.__init__ import create_app
from app.extensions import db
import os

app = create_app()

# Initialize database tables - only in development
if os.environ.get('VERCEL_ENV') != 'production':
    with app.app_context():
        db.create_all()

# This is for Vercel - the app variable will be used by the Vercel Python runtime
if __name__ == '__main__':
    app.run()