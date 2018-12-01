from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import PasswordField, StringField, validators, ValidationError, SelectField, TextAreaField
from application.models.user import User
from application.models.team import Team

def check_unique_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('Username already taken')

def check_unique_teamname(form, field):
        if Team.query.filter_by(name=field.data).first() is not None:
            raise ValidationError('Name already taken')

def old_password_matches(form, field):
        if User.query.get(current_user.get_id()).password != field.data:
            raise ValidationError('Incorrect password')

class CreateUserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3), validators.Length(max=32), check_unique_username])
    password = PasswordField("Password", [validators.Length(min=5), validators.Length(max=32)])
    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3), validators.Length(max=32)])
    password = PasswordField("Password", [validators.Length(min=5), validators.Length(max=32)])
    class Meta:
        csrf = False

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Current password", [old_password_matches])
    new_password = PasswordField("New password", [validators.Length(min=5), validators.Length(max=32)])
    class Meta:
        csrf = False

class GameplayForm(FlaskForm):
    choice = SelectField("Pick one", choices=[('Rock', 'Rock'), ('Paper', 'Paper'), ('Scissors', 'Scissors')])
    class Meta:
        csrf = False

class CreateTeamForm(FlaskForm):
    name = StringField("name", [validators.Length(min=3), validators.Length(max=32), check_unique_teamname])
    class Meta:
        csrf = False

class CreateCommentForm(FlaskForm):
    text = TextAreaField("text", [validators.Length(min=1), validators.Length(max=500)])
    class Meta:
        csrf = False