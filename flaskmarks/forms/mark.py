from flaskmarks.forms.base import (
    Form,
    strip_filter,
)

from wtforms import (
    Field,
    TextField,
    BooleanField,
    PasswordField,
    SelectField,
    RadioField,
    validators,
    HiddenField,
    IntegerField,
)

class TagListField(Field):
    widget = TextField()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

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
    clicks = IntegerField('Clicks')
