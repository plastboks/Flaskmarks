from flask.ext.wtf import (
    Form,
    TextField,
    BooleanField,
    Required,
    PasswordField,
    SelectField,
    validators,
    HiddenField,
    )

strip_filter = lambda x: x.strip() if x else None
pmm = 'Passwords must match'


class LoginForm(Form):
    username = TextField('username',
                         [validators.Length(min=4, max=255)],
                         filters=[strip_filter])
    password = PasswordField('password',
                             [validators.Length(min=1, max=255)],
                             filters=[strip_filter])
    remember_me = BooleanField('remember_me', default=False)


class UserRegisterForm(Form):
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
                                                 message=pmm)],
                             filters=[strip_filter])
    confirm = PasswordField('confirm',
                            filters=[strip_filter])


class UserProfileForm(UserRegisterForm):
    password = PasswordField('password',
                             [validators.Optional(),
                              validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message=pmm)],
                             filters=[strip_filter])
    per_page = SelectField('per_page',
                           coerce=int,
                           choices=[(n, n) for n in range(10, 21)])
    suggestion = BooleanField('suggestion', default=True)
    recently = SelectField('recently',
                           coerce=int,
                           choices=[(n, n) for n in range(5)])


class BookmarkForm(Form):
    referrer = HiddenField([validators.URL(require_tld=False)])
    title = TextField('title',
                      [validators.Length(min=0, max=255)],
                      filters=[strip_filter])
    url = TextField('url',
                    [validators.Length(min=4, max=512),
                     validators.URL(require_tld=False,
                                    message='Not a valid URL')],
                    filters=[strip_filter])
    tags = TextField('tags',
                     [validators.Length(min=0, max=255)],
                     filters=[strip_filter])


class FeedForm(Form):
    referrer = HiddenField([validators.URL(require_tld=False)])
    title = TextField('title',
                      [validators.Length(min=0, max=255)],
                      filters=[strip_filter])
    url = TextField('url',
                    [validators.Length(min=4, max=512),
                     validators.URL(require_tld=False,
                                    message='Not a valid URL')],
                    filters=[strip_filter])
    tags = TextField('tags',
                     [validators.Length(min=0, max=255)],
                     filters=[strip_filter])
