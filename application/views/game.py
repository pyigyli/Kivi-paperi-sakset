from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from application.models.result import Result
from application.models.bot import Bot
from application.views.forms import GameplayForm
from random import randint

@app.route("/game/index/")
def game_index():
    return render_template("game/index.html")

@app.route("/game/easy/")
@login_required
def game_easy():
    return render_template("game/easy.html", form = GameplayForm())

@app.route("/game/easycheck/", methods=["POST"])
@login_required
def game_easycheck():
    form = GameplayForm(request.form)
    user_choice = form.choice.data
    bot_choice = "Paper"
    if user_choice == "Rock":
        result = Result(current_user.get_id(), Bot.query.filter_by(name="Easy").first().bot_id, 0)
        db.session.add(result)
        db.session.commit()
        return render_template("game/lose.html", user_choice = user_choice, bot_choice = "Paper")
    if user_choice == "Paper":
        result = Result(current_user.get_id(), Bot.query.filter_by(name="Easy").first().bot_id, 1)
        db.session.add(result)
        db.session.commit()
        return render_template("game/draw.html", user_choice = user_choice, bot_choice = "Paper")
    if user_choice == "Scissors":
        result = Result(current_user.get_id(), Bot.query.filter_by(name="Easy").first().bot_id, 2)
        db.session.add(result)
        db.session.commit()
        return render_template("game/win.html", user_choice = user_choice, bot_choice = "Paper")

@app.route("/game/hard/")
@login_required
def game_hard():
    return render_template("game/hard.html", form = GameplayForm())

@app.route("/game/hardcheck/", methods=["POST"])
@login_required
def game_hardcheck():
    form = GameplayForm(request.form)
    user_choice = form.choice.data
    bot_choices = ["Rock", "Paper", "Scissors"]
    bot_choice = bot_choices[randint(0, 2)]
    print(bot_choice)
    if (user_choice == "Rock" and bot_choice == "Paper") or (user_choice == "Paper" and bot_choice == "Scissors") or (user_choice == "Scissors" and bot_choice == "Rock"):
        result = Result(current_user.get_id(), Bot.query.filter_by(name="Hard").first().bot_id, 0)
        db.session.add(result)
        db.session.commit()
        return render_template("game/lose.html", user_choice = user_choice, bot_choice = bot_choice)
    if (user_choice == "Rock" and bot_choice == "Rock") or (user_choice == "Paper" and bot_choice == "Paper") or (user_choice == "Scissors" and bot_choice == "Scissors"):
        result = Result(current_user.get_id(), Bot.query.filter_by(name="Hard").first().bot_id, 1)
        db.session.add(result)
        db.session.commit()
        return render_template("game/draw.html", user_choice = user_choice, bot_choice = bot_choice)
    if (user_choice == "Rock" and bot_choice == "Scissors") or (user_choice == "Paper" and bot_choice == "Rock") or (user_choice == "Scissors" and bot_choice == "Paper"):
        result = Result(current_user.get_id(), Bot.query.filter_by(name="Hard").first().bot_id, 2)
        db.session.add(result)
        db.session.commit()
        return render_template("game/win.html", user_choice = user_choice, bot_choice = bot_choice)