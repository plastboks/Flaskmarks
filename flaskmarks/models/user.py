# flaskmarks/models/user.py

from sqlalchemy import or_, desc, asc, func
from sqlalchemy.orm import aliased
from ..core.setup import db, config, bcrypt
from .tag import Tag
from .mark import Mark


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True, nullable=False)
    email = db.Column(db.Unicode(255), unique=True, nullable=False)
    password = db.Column(db.Unicode(255), nullable=False)
    last_logged = db.Column(db.DateTime)
    per_page = db.Column(db.SmallInteger, default=10)
    sort_type = db.Column(db.Unicode(255), default=u'clicks')

    marks = db.relationship('Mark', backref='owner', lazy='dynamic')

    @classmethod
    def by_uname_or_email(self, uname):
        return self.query.filter(or_(User.username == uname,
                                     User.email == uname)).first()

    def my_marks(self):
        return Mark.query.filter(Mark.owner_id == self.id)

    def my_tags(self):
        return Tag.query.filter(Tag.marks.any(owner_id=self.id))

    def all_marks(self):
        return self.my_marks().all()

    def marks(self, page):
        base = self.my_marks()
        if self.sort_type == u'clicks':
            base = base.order_by(desc(Mark.clicks))\
                       .order_by(desc(Mark.created))
        if self.sort_type == u'dateasc':
            base = base.order_by(asc(Mark.created))
        if self.sort_type == u'datedesc':
            base = base.order_by(desc(Mark.created))
        return base.paginate(page, self.per_page, False)

    def recent_marks(self, page, type):
        if type == 'added':
            base = self.my_marks().order_by(desc(Mark.created))
            return base.paginate(page, self.per_page, False)
        if type == 'clicked':
            base = self.my_marks().filter(Mark.clicks > 0)\
                                  .order_by(desc(Mark.last_clicked))
            return base.paginate(page, self.per_page, False)
        return False

    def get_mark_by_id(self, id):
        return self.my_marks().filter(Mark.id == id).first()

    def get_mark_type_count(self, type):
        return self.my_marks().filter(Mark.type == type).count()

    def mark_last_created(self):
        return self.my_marks().order_by(desc(Mark.created)).first()

    def q_marks_by_tag(self, tag, page):
        return self.my_marks().filter(Mark.tags.any(title=tag))\
                              .paginate(page, self.per_page, False)

    def q_marks_by_string(self, page, string, marktype):
        string = "%"+string+"%"
        base = self.my_marks().filter(or_(Mark.title.like(string),
                                          Mark.url.like(string)))
        return base.order_by(desc(Mark.clicks))\
                   .paginate(page, self.per_page, False)

    def q_marks_by_url(self, string):
        return self.my_marks().filter(Mark.url == string).first()

    def all_tags(self):
        return self.my_tags().all()

    def tags_by_click(self, page):
        return self.my_tags().order_by(Tag.marks.any(Mark.clicks))\
                             .paginate(page, self.per_page, False)

    def authenticate_user(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
