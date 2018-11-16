from flask import Flask
app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

from application.models import bot, comment, result, team, user
from application.views import auth, forms, game, index, result, team, user
from application.models.user import User

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
except:
    pass

from application.models.bot import Bot
if Bot.query.filter_by(name="Easy").first() == None:
    easy_bot = Bot("Easy")
    db.session.add(easy_bot)
    db.session().commit()
if Bot.query.filter_by(name="Hard").first() == None:
    hard_bot = Bot("Hard")
    db.session.add(hard_bot)
    db.session().commit()