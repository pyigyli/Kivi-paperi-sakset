from application import db
from sqlalchemy.sql import text
from application.models.user import User

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
    def list_team_comments(team_id, page):
        stmt = text("SELECT comment.account_id, comment.text "
                    "FROM account, comment, team "
                    "WHERE comment.account_id = account.account_id "
                    "AND comment.team_id = :teamid "
                    "GROUP BY comment.comment_id "
                    "ORDER BY comment.datetime DESC "
                    "LIMIT 7 OFFSET :offset;").params(teamid = team_id, offset = (page - 1) * 7)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"user":User.query.get(row[0]).username, "text":row[1]})
        return response



    @staticmethod
    def count_comments_of_team(team_id):
        stmt = text("SELECT COUNT(comment.comment_id) "
                    "FROM comment, team "
                    "WHERE comment.team_id = team.team_id "
                    "AND team.team_id = :teamid;").params(teamid = team_id)
        res = db.engine.execute(stmt)
        for row in res:
            response = row[0]
        return response