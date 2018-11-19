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