from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from application.models.user import User
from application.models.team import Team
from application.models.comment import Comment
from application.views.forms import CreateTeamForm, CreateCommentForm

@app.route("/team/index/")
def team_index():
    return render_template("team/index.html", user = current_user, teams = Team.list_by_score())

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

@app.route("/team/join/<teamid>/")
@login_required
def team_join(teamid):
    user = User.query.get(current_user.get_id())
    team = Team.query.get(teamid)
    user.team_id = team.get_id()
    db.session().commit()
    return redirect(url_for("team_page", teamid = user.team_id))

@app.route("/team/quit/<teamid>/")
@login_required
def team_quit(teamid):
    user = User.query.get(current_user.get_id())
    user.team_id = None
    db.session().commit()
    return redirect(url_for("team_index"))

@app.route("/team/delete/<teamid>/")
@login_required
def team_delete(teamid):
    team = Team.query.get(teamid)
    comments = Comment.query.filter_by(team_id=teamid)
    for c in comments:
        db.session.delete(c)
    users = User.query.filter_by(team_id=teamid)
    for u in users:
        u.team_id = None
    db.session.delete(team)
    db.session().commit()
    return redirect(url_for("team_index"))

@app.route("/team/<teamid>/")
@login_required
def team_page(teamid):
    return render_template("team/teampage.html", team = Team.query.get(teamid), users = User.list_by_score(team_id=teamid),
                                    form = CreateCommentForm(request.form), comments = Comment.list_team_comments(teamid),
                                    user = User.query.get(current_user.get_id()))

@app.route("/team/<teamid>/comment", methods=["POST"])
@login_required
def team_send_comment(teamid):
    form = CreateCommentForm(request.form)
    text = form.text.data
    comment = Comment(teamid, current_user.get_id(), text)
    db.session().add(comment)
    db.session().commit()
    if not form.validate():
        return render_template("team/teampage.html", team = Team.query.get(teamid), users = User.list_by_score(team_id=teamid),
                                                    form = form, comments = Comment.list_team_comments(teamid),
                                                    user = User.query.get(current_user.get_id()))
    return redirect(url_for("team_page", teamid = User.query.get(current_user.get_id()).team_id))