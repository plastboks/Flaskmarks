from wtforms import (
    TextField,
    BooleanField,
    PasswordField,
    validators,
    SubmitField
)
from .base import Form, strip_filter


class LoginForm(Form):
    username = TextField('Username or Email',
                         [validators.Length(min=4, max=255)],
                         filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=1, max=255)],
                             filters=[strip_filter])
    remember_me = BooleanField('Remember me', default=False)
    submit_button = SubmitField('Login')
