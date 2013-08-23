from flask.ext.wtf import (
    Form,
    TextField,
    BooleanField,
    Required,
    PasswordField,
    SelectField,
    RadioField,
    validators,
    HiddenField,
    )

strip_filter = lambda x: x.strip() if x else None
pmm = 'Passwords must match'


class LoginForm(Form):
    username = TextField('Username or Email',
                         [validators.Length(min=4, max=255)],
                         filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=1, max=255)],
                             filters=[strip_filter])
    remember_me = BooleanField('Remember me', default=False)


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
                                                 message=pmm)],
                             filters=[strip_filter])
    confirm = PasswordField('Confirm Password',
                            filters=[strip_filter])


class UserProfileForm(UserRegisterForm):
    password = PasswordField('Password',
                             [validators.Optional(),
                              validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message=pmm)],
                             filters=[strip_filter])
    per_page = SelectField('Items per page',
                           coerce=int,
                           choices=[(n, n) for n in range(10, 21)])
    suggestion = SelectField('Show suggestions',
                             coerce=int,
                             choices=[(n, n) for n in range(5)])
    recently = SelectField('Recently added',
                           coerce=int,
                           choices=[(n, n) for n in range(5)])


class MarkForm(Form):
    referrer = HiddenField([validators.URL(require_tld=False)])
    title = TextField('Title',
                      [validators.Length(min=0, max=255)],
                      filters=[strip_filter])
    url = TextField('URL',
                    [validators.Length(min=4, max=512),
                     validators.URL(require_tld=False,
                                    message='Not a valid URL')],
                    filters=[strip_filter])
    type = RadioField('Type',
                      coerce=unicode,
                      choices=[('bookmark', 'Bookmark'), ('feed', 'Feed')],
                      default='bookmark')
    tags = TextField('Tags',
                     [validators.Length(min=0, max=255)],
                     filters=[strip_filter])
