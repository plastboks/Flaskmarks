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
  

