from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from json import load

with open("config.json", "r") as c:
    params = load(c)["params"]

db = SQLAlchemy()
login_manager = LoginManager()

