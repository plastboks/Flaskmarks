from flaskmarks.forms.base import (
    Form,
    strip_filter
)

from wtforms import (
    TextField,
    PasswordField,
    SelectField,
    HiddenField,
    validators,
)


class UserRegisterForm(Form):
    username = TextField('Username',
                         [validators.Length(min=4, max=32)],
                         filters=[strip_filter])
    email = TextField('Email',
                      [validators.Length(min=4, max=320),
                       validators.Email(message='Not a valid email address')],
                      filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message='Passwords must\
                                                          match')],
                             filters=[strip_filter])
    confirm = PasswordField('Confirm Password',
                            filters=[strip_filter])


class UserProfileForm(UserRegisterForm):
    password = PasswordField('Password',
                             [validators.Optional(),
                              validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message='Passwords must\
                                                          match')],
                             filters=[strip_filter])
    per_page = SelectField('Items per page',
                           coerce=int,
                           choices=[(n, n) for n in range(10, 31)])
    suggestion = HiddenField('Show suggestions', 0)
    recently = HiddenField('Recently added', 0)
    sort_type = SelectField('Default sort type',
                            coerce=unicode,
                            choices=[('clicks', 'Clicks'),
                                     ('dateasc', 'Date asc'),
                                     ('datedesc', 'Date desc')])
