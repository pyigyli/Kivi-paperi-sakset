from application import app
from flask import render_template, request

@app.route("/user/index/")
def user_index():
    return render_template("user/index.html")