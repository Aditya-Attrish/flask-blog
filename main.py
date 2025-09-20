from app.__init__ import create_app
#from routes import app
from app.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
    	db.create_all()
    app.run(host=app.config['HOST'], port=app.config['PORT'])