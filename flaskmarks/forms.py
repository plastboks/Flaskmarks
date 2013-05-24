from flask.ext.wtf import (
    Form,
    TextField,
    BooleanField,
    Required,
    PasswordField,
    validators,
    )

strip_filter = lambda x: x.strip() if x else None

class LoginForm(Form):
    username = TextField('username',
                      [validators.Length(min=1, max=255)],
                      filters=[strip_filter])
    password = PasswordField('password',
                          [validators.Length(min=1, max=255)],
                          filters=[strip_filter])
    remember_me = BooleanField('remember_me', default=False)
  

class RegisterForm(Form):
    username = TextField('username',
                         [validators.Length(min=4, max=32)],
                         filters=[strip_filter])
    email = TextField('email',
                      [validators.Length(min=4, max=320),
                       validators.Email(message='Not a valid email address')],
                      filters=[strip_filter])
    password = PasswordField('password',
                             [validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message='Passwords must match')],
                             filters=[strip_filter])
    confirm = PasswordField('confirm',
                            filters=[strip_filter])


class NewBookmarkForm(Form):
    title = TextField('title',
                      [validators.Length(min=4, max=320)],
                      filters=[strip_filter])
    url = TextField('url',
                    [validators.Length(min=4, max=320),
                     validators.URL(require_tld=False,
                                    message='Not a valid URL')],
                    filters=[strip_filter])
