from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError
from application.models.user import User
from application.models.team import Team

def check_unique_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('Username already taken')

def check_unique_teamname(form, field):
        if Team.query.filter_by(name=field.data).first() is not None:
            raise ValidationError('Name already taken')

class CreateUserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3), validators.Length(max=144), check_unique_username])
    password = PasswordField("Password", [validators.Length(min=5), validators.Length(max=144)])
    class Meta:
        csrf = False


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3), validators.Length(max=144)])
    password = PasswordField("Password", [validators.Length(min=5), validators.Length(max=144)])
    class Meta:
        csrf = False

class CreateTeamForm(FlaskForm):
    name = StringField("name", [validators.Length(min=3), validators.Length(max=144), check_unique_teamname])
    class Meta:
        csrf = False