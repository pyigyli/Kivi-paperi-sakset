from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class CreateUserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3), validators.Length(max=144)])
    password = PasswordField("Password", [validators.Length(min=5), validators.Length(max=144)])
    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3), validators.Length(max=144)])
    password = PasswordField("Password", [validators.Length(min=5), validators.Length(max=144)])
    class Meta:
        csrf = False