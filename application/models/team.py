from application import db
from sqlalchemy.sql import text

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    leader = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)

    def __init__(self, name, leader):
        self.name = name
        self.leader = leader

    @staticmethod
    def list_by_score():
        stmt = text("SELECT team.name, COUNT(result.result_id) "
                    "FROM team "
                    "LEFT JOIN account ON team.team_id = account.team_id "
                    "LEFT JOIN result ON account.account_id = result.account_id "
                    "GROUP BY team.team_id "
                    "ORDER BY COUNT(result.result_id);")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "score":row[1]})
        return response