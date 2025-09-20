class Config:
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    FlASK_ENV = 'development'
    DEBUG = True if FlASK_ENV == 'development' else False
    HOST = '0.0.0.0'
    PORT = 4000
  