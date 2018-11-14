from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from application.models.user import User
from application.models.team import Team
from application.views.forms import CreateTeamForm

@app.route("/team/index/")
def team_index():
    return render_template("team/index.html", teams = Team.list_by_score(), user = current_user)

@app.route("/team/new/")
@login_required
def team_new():
    return render_template("team/newform.html", form = CreateTeamForm(request.form))

@app.route("/team/create", methods=["POST"])
@login_required
def team_create():
    form = CreateTeamForm(request.form)
    if not form.validate():
        return render_template("team/newform.html", form = form)
    user = User.query.get(current_user.get_id())
    team = Team(form.name.data, user.account_id)
    db.session().add(team)
    db.session().commit()
    creator_id = user.account_id
    team = Team.query.filter_by(creator=creator_id).first()
    user.team_id = team.get_id()
    db.session().commit()
    return redirect(url_for("team_page", teamid = user.team_id))

@app.route("/team/<teamid>/")
@login_required
def team_page(teamid):
    return render_template("team/teampage.html", team = Team.query.get(teamid), users = User.list_by_score(team_id=teamid))