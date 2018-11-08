from application import db

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    botId = db.Column(db.Integer, db.ForeignKey('bot.id'), nullable=False)
    winner = db.Column(db.Boolean, nullable=False) # Player won if True, bot won if False
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name