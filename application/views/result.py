from application import app, db
from flask import render_template, request
from application.models.user import User
from application.models.result import Result

@app.route("/scoreboard/index/")
def scoreboard_index():
    results = []
    usernames = User.qualifies_to_scoreboard()
    for name in usernames:
        wincount = 0
        losscount = 0
        wins = Result.scoreboard_list_wins(name)
        for w in wins:
            wincount += 1
        losses = Result.scoreboard_list_losses(name)
        for l in losses:
            losscount += 1
        results.append({"username":name, "percent":(wincount / losscount)})
    return render_template("scoreboard/index.html", userwins = Result.scoreboard_list_top_user_wins(), teamwins = Result.scoreboard_list_top_team_wins(),
                                                    userdraws = Result.scoreboard_list_top_user_draws(), teamdraws = Result.scoreboard_list_top_team_draws(),
                                                    userlosses = Result.scoreboard_list_top_user_losses(), teamlosses = Result.scoreboard_list_top_team_losses())