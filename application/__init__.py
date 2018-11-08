from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

from application.views import game, index, result, team, user
from application.models import bot, comment, result, team, user

db.create_all()