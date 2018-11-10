from application import db

class User(db.Model):

    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    team_id = db.Column(db.Integer, nullable=True) # Not a Foreign Key because Foreign Key can't be null.

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.account_id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True