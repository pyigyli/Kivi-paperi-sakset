from application import app
from flask import render_template, request

@app.route("/game/index/")
def game_index():
    return render_template("game/index.html")