from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from application import app, db
from application.models.user import User
from application.models.team import Team
from application.models.bot import Bot
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

@app.route("/account/delete_account/")
@login_required
def auth_delete_account():
    return render_template("auth/delete.html")

@app.route("/auth/delete")
@login_required
def auth_delete():
    user = User.query.get(current_user.get_id())
    team = Team.query.filter_by(creator=user.account_id).first()
    if team:
        comments = Comment.query.filter_by(account_id=user.account_id)
        for c in comments:
            db.session.delete(c)
    else:
        comments = Comment.query.filter_by(team_id=team.team_id)
        for c in comments:
            db.session.delete(c)
        users = User.query.filter_by(team_id=team.team_id)
        for u in users:
            u.team_id = None
        db.session.delete(team)
    results = Result.query.filter_by(account_id=user.account_id)
    for r in results:
        db.session.delete(r)
    logout_user()
    db.session().delete(user)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/account/profile/")
@login_required
def auth_profile():
    results = Result.query.filter_by(account_id=current_user.get_id())
    wins_easy = 0
    draws_easy = 0
    loses_easy = 0
    wins_hard = 0
    draws_hard = 0
    loses_hard = 0
    for r in results:
        if r.bot_id == Bot.query.filter_by(name="Easy").first().bot_id and r.winner == 2:
            wins_easy += 1
        if r.bot_id == Bot.query.filter_by(name="Easy").first().bot_id and r.winner == 1:
            draws_easy += 1
        if r.bot_id == Bot.query.filter_by(name="Easy").first().bot_id and r.winner == 0:
            loses_easy += 1
        if r.bot_id == Bot.query.filter_by(name="Hard").first().bot_id and r.winner == 2:
            wins_hard += 1
        if r.bot_id == Bot.query.filter_by(name="Hard").first().bot_id and r.winner == 1:
            draws_hard += 1
        if r.bot_id == Bot.query.filter_by(name="Hard").first().bot_id and r.winner == 0:
            loses_hard += 1
    return render_template("auth/profile.html", easy_wins = wins_easy, easy_draws = draws_easy, easy_loses = loses_easy,
                                                hard_wins = wins_hard, hard_draws = draws_hard, hard_loses = loses_hard)