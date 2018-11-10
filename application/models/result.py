from application import db

class Result(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.bot_id'), nullable=False)
    winner = db.Column(db.Boolean, nullable=False) # Player won if True, bot won if False
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name