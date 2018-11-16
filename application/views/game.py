from flask import render_template, request, redirect, url_for
from flask_login import login_required
from application import app
from application.views.forms import EasyBotForm

@app.route("/game/index/")
def game_index():
    return render_template("game/index.html")

@app.route("/game/easy/")
@login_required
def game_easy():
    return render_template("game/easy.html", form = EasyBotForm())

@app.route("/game/easycheck/", methods=["POST"])
@login_required
def easy_check():
    form = EasyBotForm(request.form)
    user_choice = form.choice.data
    bot_choice = "Paper"
    if user_choice == "Rock":
        return redirect(url_for("game_lose"))
    if user_choice == "Paper":
        return redirect(url_for("game_draw"))
    if user_choice == "Scissors":
        return redirect(url_for("game_win"))

@app.route("/game/lose/")
@login_required
def game_lose():
    return render_template("game/lose.html")

@app.route("/game/draw/")
@login_required
def game_draw():
    return render_template("game/lose.html")

@app.route("/game/win/")
@login_required
def game_win():
    return render_template("game/win.html")