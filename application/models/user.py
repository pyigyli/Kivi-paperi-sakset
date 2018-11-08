from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    team = db.Column(db.Integer, nullable=True) # Not a Foreign Key because Foreign Key can't be null.

    def __init__(self, name):
        self.name = name