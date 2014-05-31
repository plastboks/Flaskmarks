from flaskmarks.forms.base import (
    Form,
    strip_filter,
)

from flaskmarks import (
    db
)

from flaskmarks.models.tag import (
    Tag
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

"""
Code inspired from WTForms Documentation.
http://wtforms.simplecodes.com/docs/1.0.2/fields.html#custom-fields
"""
class TagListField(TextField):

    def _value(self):
        if self.data:
            return u' '.join([t.title for t in self.data])
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            ass_tags = []
            tag_keys = {}
            form_tags = valuelist[0].strip().replace(',', ' ').split(' ')
            for t in form_tags:
                tag_keys[t] = 1
            tags = tag_keys.keys()
            for t in tags:
                tag = Tag.check(t.lower())
                if not tag:
                    tag = Tag(t.lower())
                    db.session.add(tag)
                ass_tags.append(tag)
            self.data = ass_tags
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
    ass_tags = TagListField('Tags',
                            [validators.Length(min=0, max=255)])
    clicks = IntegerField('Clicks')
