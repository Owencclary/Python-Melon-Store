from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm): # Class for login form, username and password require inputs
   username = StringField('Username', [validators.InputRequired()])
   password = PasswordField('Password', [validators.InputRequired()])