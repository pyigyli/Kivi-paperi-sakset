from application import app
from flask import render_template, request

@app.route("/team/index/")
def team_index():
    return render_template("team/index.html")

@app.route("/team/new/")
def team_new():
    return render_template("team/new.html")

@app.route("/team/", methods=["POST"])
def team_create():
    print(request.form.get("name"))
    return "hello world!"