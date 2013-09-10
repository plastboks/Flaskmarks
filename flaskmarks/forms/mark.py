from flaskmarks.forms.base import (
    Form,
    strip_filter,
)

from wtforms import (
    TextField,
    BooleanField,
    PasswordField,
    SelectField,
    RadioField,
    validators,
    HiddenField,
)


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
