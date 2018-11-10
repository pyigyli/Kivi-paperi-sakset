from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application.models.user import User
from application.models.team import Team
from application.views.forms import CreateTeamForm

@app.route("/team/index/")
def team_index():
    return render_template("team/index.html", teams = Team.list_by_score())

@app.route("/team/new/")
def team_new():
    return render_template("team/newform.html")

@app.route("/team/create", methods=["POST"])
def team_create():
    form = CreateTeamForm(request.form)
    if not form.validate():
        return render_template("team/newform.html", form = form)
    user = User.query.filter_by(account_id=current_user.get_id()).first()
    team = Team(form.name.data, user.username)
    db.session().add(team)
    db.session().commit()
    return redirect(url_for("team_index"))