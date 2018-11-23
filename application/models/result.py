from application import db
from sqlalchemy.sql import text

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
    def scoreboard_list_top_user_wins():
        stmt = text("SELECT account.username, COUNT(result.result_id) "
                    "FROM account "
                    "LEFT JOIN result ON account.account_id = result.account_id "
                    "AND result.winner = 2 "
                    "GROUP BY account.account_id "
                    "ORDER BY COUNT(result.result_id) DESC "
                    "LIMIT 10;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"account":row[0], "wins":row[1]})
        return response

    @staticmethod
    def scoreboard_list_top_team_wins():
        stmt = text("SELECT team.name, COUNT(result.result_id) "
                    "FROM team "
                    "LEFT JOIN account ON team.team_id = account.team_id "
                    "LEFT JOIN result ON account.account_id = result.account_id "
                    "AND result.winner = 2 "
                    "GROUP BY team.team_id "
                    "ORDER BY COUNT(result.result_id) DESC "
                    "LIMIT 10;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"team":row[0], "wins":row[1]})
        return response

    @staticmethod
    def scoreboard_list_top_user_winpercents():
        stmt = text("SELECT account.username, "
                    "SUM(CASE WHEN result.winner = 2 THEN 1 ELSE 0 END) AS wins, "
                    "SUM(CASE WHEN result.winner = 0 THEN 1 ELSE 0 END) AS losses "
                    "FROM account, result "
                    "WHERE account.account_id = result.account_id "
                    "GROUP BY account.account_id;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            percent = "%.2f" % (row[1] / (row[1] + row[2]) * int(100))
            response.append({"account":row[0], "percent":percent})
        response.sort()
        return response[-10:]

    @staticmethod
    def scoreboard_list_top_team_winpercents():
        stmt = text("SELECT team.name, "
                    "SUM(CASE WHEN result.winner = 2 THEN 1 ELSE 0 END) AS wins, "
                    "SUM(CASE WHEN result.winner = 0 THEN 1 ELSE 0 END) AS losses "
                    "FROM team, account, result "
                    "WHERE team.team_id = account.team_id "
                    "AND account.account_id = result.account_id "
                    "GROUP BY team.team_id;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            percent = "%.2f" % (row[1] / (row[1] + row[2]) * int(100))
            response.append({"team":row[0], "percent":percent})
        response.sort()
        return response[-10:]

    @staticmethod
    def scoreboard_list_top_user_total_games():
        stmt = text("SELECT account.username, COUNT(result.result_id) "
                    "FROM account "
                    "LEFT JOIN result ON account.account_id = result.account_id "
                    "GROUP BY account.account_id "
                    "ORDER BY COUNT(result.result_id) DESC "
                    "LIMIT 10;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"account":row[0], "games":row[1]})
        return response

    @staticmethod
    def scoreboard_list_top_team_total_games():
        stmt = text("SELECT team.name, COUNT(result.result_id) "
                    "FROM team "
                    "LEFT JOIN account ON team.team_id = account.team_id "
                    "LEFT JOIN result ON account.account_id = result.account_id "
                    "GROUP BY team.team_id "
                    "ORDER BY COUNT(result.result_id) DESC "
                    "LIMIT 10;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"team":row[0], "games":row[1]})
        return response