from application import db

class Result(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.bot_id'), nullable=False)

    winner = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, account_id, bot_id, winner):
        self.account_id = account_id
        self.bot_id = bot_id
        self.winner = winner

    @staticmethod
    def count_easy_wins(team_id):
        stmt = text("SELECT account.username, COUNT(result.result_id) "
                    "FROM account "
                    "LEFT JOIN result ON account.account_id = result.account_id "
                    "AND result.winner = 2 "
                    "LEFT JOIN team ON account.team_id = team.team_id "
                    "WHERE account.team_id = :teamid "
                    "GROUP BY account.account_id "
                    "ORDER BY COUNT(result.result_id) DESC;").params(teamid=team_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "score":row[1]})
        return response