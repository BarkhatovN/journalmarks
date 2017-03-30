from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import Required, Email
from wtforms import PasswordField

class LoginForm(FlaskForm):
    login = TextField('login', validators=[Required(), Email()])
    password = PasswordField('password', validators=[Required()])
