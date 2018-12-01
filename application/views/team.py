from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_sqlalchemy import Pagination
from application.models.user import User
from application.models.team import Team
from application.models.comment import Comment
from application.views.forms import CreateTeamForm, CreateCommentForm
from application.views.pagination import url_for_other_page

@app.route("/team/index/", defaults={'page': 1})
@app.route('/team/page/<int:page>')
def team_index(page):
    count = Team.count_teams()
    teams = Team.list_by_score(page)
    if not teams and page != 1:
        abort(404)
    return render_template("team/index.html", user = current_user, teams = teams, count = count, page = page)

@app.route("/team/new/")
@login_required
def team_new():
    return render_template("team/newform.html", form = CreateTeamForm(request.form))

@app.route("/team/create/", methods=["POST"])
@login_required
def team_create():
    user = User.query.get(current_user.get_id())
    form = CreateTeamForm(request.form)
    if (user.team_id != None) or (not form.validate()):
        return render_template("team/newform.html", form = form)
    team = Team(form.name.data, user.account_id)
    db.session().add(team)
    db.session().commit()                                           # Create team with creator's id as creator_id
    team = Team.query.filter_by(creator=user.account_id).first()
    user.team_id = team.get_id()
    db.session().commit()                                           # Link creator's team_id to this new team
    return redirect(url_for("team_page", teamid = user.team_id))

@app.route("/team/join/<teamid>/")
@login_required
def team_join(teamid):
    user = User.query.get(current_user.get_id())
    team = Team.query.get(teamid)
    user.team_id = team.get_id()
    db.session().commit()                                           # Link user's team_id to the team they are joining to
    return redirect(url_for("team_page", teamid = user.team_id))

@app.route("/team/quit/<teamid>/")
@login_required
def team_quit(teamid):
    user = User.query.get(current_user.get_id())
    user.team_id = None
    db.session().commit()                                           # Set user's team_id to none, removing the connection between user and team
    return redirect(url_for("team_index"))

@app.route("/team/delete/<teamid>/")
@login_required
def team_delete(teamid):
    team = Team.query.get(teamid)
    comments = Comment.query.filter_by(team_id=teamid)
    for c in comments:
        db.session.delete(c)                                        # Delete all the comments from team
    users = User.query.filter_by(team_id=teamid)
    for u in users:
        u.team_id = None                                            # Set team_id of everyone in team to none
    db.session.delete(team)                                         # Delete team
    db.session().commit()
    return redirect(url_for("team_index"))

@app.route("/team/<teamid>/", defaults={'page': 1})
@app.route('/team/<teamid>/<int:page>')
@login_required
def team_page(teamid, page):
    count = Comment.count_comments_of_team(teamid)
    comments = Comment.list_team_comments(teamid, page)
    if not comments and page != 1:
        abort(404)
    return render_template("team/teampage.html", team = Team.query.get(teamid), form = CreateCommentForm(request.form),
                                    users = User.list_by_score(team_id=teamid), user = User.query.get(current_user.get_id()),
                                    comments = comments, count = count, page = page)

@app.route("/team/<teamid>/comment", methods=["POST"])
@login_required
def team_send_comment(teamid):
    count = Comment.count_comments_of_team(teamid)
    form = CreateCommentForm(request.form)
    if not form.validate():
        return render_template("team/teampage.html", team = Team.query.get(teamid), form = form,
                                                    users = User.list_by_score(team_id=teamid),
                                                    user = User.query.get(current_user.get_id()),
                                                    comments = Comment.list_team_comments(teamid, 1),
                                                    count = count, page = 1)
    text = form.text.data
    comment = Comment(teamid, current_user.get_id(), text)
    db.session().add(comment)
    db.session().commit()
    return redirect(url_for("team_page", teamid = User.query.get(current_user.get_id()).team_id))