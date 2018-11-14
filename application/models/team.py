from application import db
from sqlalchemy.sql import text

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    creator = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, name, creator):
        self.name = name
        self.creator = creator

    @staticmethod
    def list_by_score():
        stmt = text("SELECT team.team_id, team.name, COUNT(result.result_id) "
                    "FROM team "
                    "LEFT JOIN account ON team.team_id = account.team_id "
                    "LEFT JOIN result ON account.account_id = result.account_id "
                    "GROUP BY team.team_id "
                    "ORDER BY COUNT(result.result_id);")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id": row[0], "name":row[1], "score":row[2]})
        return response

    def get_id(self):
        return self.team_id