from application import db

class Bot(db.Model):
    bot_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    results = db.relationship('Result', backref='bot', lazy=True)

    def __init__(self, name):
        self.name = name