from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from application import app, db
from application.models.user import User
from application.models.team import Team
from application.models.comment import Comment
from application.models.result import Result
from application.views.forms import CreateUserForm, LoginForm

@app.route("/auth/new", methods = ["GET", "POST"])
def auth_form():
    if request.method == "GET":
        return render_template("auth/newform.html", form = CreateUserForm())

@app.route("/auth/create", methods=["POST"])
def auth_create():
    form = CreateUserForm(request.form)
    if not form.validate():
        return render_template("auth/newform.html", form = form)
    user = User(form.username.data, form.password.data)
    db.session().add(user)
    db.session().commit()
    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())
    form = LoginForm(request.form)
    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, error = "No such username or password")
    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/delete")
@login_required
def auth_delete():
    user = User.query.get(current_user.get_id())
    team = Team.query.filter_by(creator=user.account_id).first()
    if team is not None:
        comments = Comment.query.filter_by(team_id=team.team_id)
        for c in comments:
            db.session.delete(c)
        users = User.query.filter_by(team_id=team.team_id)
        for u in users:
            u.team_id = None
        db.session.delete(team)
    else:
        comments = Comment.query.filter_by(account_id=user.account_id)
        for c in comments:
            db.session.delete(c)
    results = Result.query.filter_by(account_id=user.account_id)
    for r in results:
        db.session.delete(r)
    logout_user()
    db.session().delete(user)
    db.session.commit()
    return redirect(url_for("index"))