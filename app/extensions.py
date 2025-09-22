from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from json import load

with open("config.json", "r") as c:
    params = load(c)["params"]

csrf = CSRFProtect()

db = SQLAlchemy()
login_manager = LoginManager()

