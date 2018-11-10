from application import db

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('bot.bot_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    text = db.Column(db.String(128), nullable=False)
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name