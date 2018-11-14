from application import app
from flask import render_template, request
from flask_login import login_required

@app.route("/user/index/")
@login_required
def user_index():
    return render_template("user/index.html")