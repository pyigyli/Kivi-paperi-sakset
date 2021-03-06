from application import db
from sqlalchemy.sql import text

class User(db.Model):
    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    team_id = db.Column(db.Integer, nullable=True) # Not a Foreign Key because Foreign Key can't be null.

    results = db.relationship('Result', backref='account', lazy=True)
    comments = db.relationship('Comment', backref='account', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def list_by_score(team_id):
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

    def get_id(self):
        return self.account_id

    def is_active(self):
        return True

    def is_authenticated(self):
        return True