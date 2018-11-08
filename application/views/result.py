from application import app
from flask import render_template, request

@app.route("/scoreboard/index/")
def scoreboard_index():
    return render_template("scoreboard/index.html")