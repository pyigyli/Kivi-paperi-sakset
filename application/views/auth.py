from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from application import app, db
from application.models.user import User
from application.models.team import Team
from application.models.bot import Bot
from application.models.comment import Comment
from application.models.result import Result
from application.views.forms import CreateUserForm, LoginForm, ChangePasswordForm

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
        return render_template("auth/loginform.html", form = form, error = "No such username or wrong password")
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
    if team:                                                                # If user is a creator of an existing team
        comments = Comment.query.filter_by(team_id=team.team_id)
        for c in comments:
            db.session.delete(c)                                            # Delete every comment in this team
        users = User.query.filter_by(team_id=team.team_id)
        for u in users:
            u.team_id = None                                                # Remove every user from the team
        db.session.delete(team)                                             # Delete the team
    else:
        comments = Comment.query.filter_by(account_id=user.account_id)
        for c in comments:
            db.session.delete(c)                                            # Else delete every comment made by user
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
    results = Result.query.filter_by(account_id=current_user.get_id())      # Check every game result from user
    wins_easy = 0                                                           # and count players statistics against each bot
    draws_easy = 0
    loses_easy = 0
    wins_hard = 0
    draws_hard = 0
    loses_hard = 0
    for r in results:
        if r.bot_id == Bot.query.filter_by(name="Easy").first().bot_id and r.winner == 2:
            wins_easy += 1
        elif r.bot_id == Bot.query.filter_by(name="Easy").first().bot_id and r.winner == 1:
            draws_easy += 1
        elif r.bot_id == Bot.query.filter_by(name="Easy").first().bot_id and r.winner == 0:
            loses_easy += 1
        elif r.bot_id == Bot.query.filter_by(name="Hard").first().bot_id and r.winner == 2:
            wins_hard += 1
        elif r.bot_id == Bot.query.filter_by(name="Hard").first().bot_id and r.winner == 1:
            draws_hard += 1
        elif r.bot_id == Bot.query.filter_by(name="Hard").first().bot_id and r.winner == 0:
            loses_hard += 1
    return render_template("auth/profile.html", easy_wins = wins_easy, easy_draws = draws_easy, easy_loses = loses_easy,
                                                hard_wins = wins_hard, hard_draws = draws_hard, hard_loses = loses_hard)

@app.route("/auth/password/")
@login_required
def auth_change_password_form():
    return render_template("auth/passwordform.html", form = ChangePasswordForm())

@app.route("/auth/password/change", methods=["POST"])
@login_required
def auth_change_password():
    form = ChangePasswordForm(request.form)
    if not form.validate():
        return render_template("auth/passwordform.html", form = form)
    user = User.query.get(current_user.get_id())
    user.password = form.new_password.data
    db.session().commit()
    return redirect(url_for("auth_profile"))