from application import db
from sqlalchemy.sql import text

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)

    text = db.Column(db.String(500), nullable=False)
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, team_id, account_id, text):
        self.team_id = team_id
        self.account_id = account_id
        self.text = text

    @staticmethod
    def list_team_comments(team_id):
        stmt = text("SELECT account.username, comment.text "
                    "FROM account, comment, team "
                    "WHERE comment.account_id = account.account_id "
                    "AND account.team_id = :teamid "
                    "GROUP BY comment.comment_id "
                    "ORDER BY comment.datetime DESC;").params(teamid=team_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"user":row[0], "text":row[1]})
        return response