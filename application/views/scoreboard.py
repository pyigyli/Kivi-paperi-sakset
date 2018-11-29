from application import app, db
from flask import render_template, request
from application.models.user import User
from application.models.result import Result

@app.route("/scoreboard/index/")
def scoreboard_index():
    return render_template("scoreboard/index.html", userwins = Result.scoreboard_list_top_user_wins(), teamwins = Result.scoreboard_list_top_team_wins(),
                                userpercents = Result.scoreboard_list_top_user_winpercents(), teampercents = Result.scoreboard_list_top_team_winpercents(),
                                usertotals = Result.scoreboard_list_top_user_total_games(), teamtotals = Result.scoreboard_list_top_team_total_games())