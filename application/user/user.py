from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    def __init__(self, name):
        self.name = name