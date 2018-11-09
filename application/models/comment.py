from application import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.Integer, db.ForeignKey('bot.id'), nullable=False)
    writer = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    text = db.Column(db.String(128), nullable=False)
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name