from flaskmarks import db, config
from sqlalchemy import (
    and_,
    or_,
    desc,
    asc,
    func,
)
from cryptacular.bcrypt import BCRYPTPasswordManager
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True, nullable=False)
    email = db.Column(db.Unicode(255), unique=True, nullable=False)
    password = db.Column(db.Unicode(255), nullable=False)
    last_logged = db.Column(db.DateTime)
    per_page = db.Column(db.SmallInteger, default=10)
    suggestion = db.Column(db.SmallInteger, default=1)
    recently = db.Column(db.SmallInteger, default=2)

    marks = db.relationship('Mark', backref='owner', lazy='dynamic')

    @classmethod
    def by_uname_or_email(self, uname):
        return self.query.filter(or_(User.username == uname,
                                     User.email == uname)).first()

    def my(self):
        return Mark.query.filter(Mark.owner_id == self.id)

    def suggestions(self):
        return self.my().filter(Mark.clicks == 0)\
                        .order_by(func.random())\
                        .limit(self.suggestion).all()

    def recent(self):
        return self.my().order_by(desc(Mark.created))\
                         .limit(self.recently).all()

    def marks(self, page):
        return self.my().order_by(desc(Mark.clicks),
                                  desc(Mark.created))\
                        .paginate(page, self.per_page, False)

    def mid(self, id):
        return self.my().filter(Mark.id == id)\
                        .first()

    def mark_count(self):
        return self.my().count()

    def bookmark_count(self):
        return self.my().filter(Mark.type == 'bookmark').count()

    def feed_count(self):
        return self.my().filter(Mark.type == 'feed').count()

    def mark_last_created(self):
        return self.my().order_by(desc(Mark.created)).first()

    def tag(self, page, tag):
        return Mark.by_tag(page, self.id, self.per_page, tag)

    def string(self, page, string):
        return Mark.by_string(page, self.id, self.per_page, string)

    def authenticate_user(self, password):
        manager = BCRYPTPasswordManager()
        return manager.check(self.password, password)

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


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Unicode(255), nullable=False)
    title = db.Column(db.Unicode(255), nullable=False)
    url = db.Column(db.Unicode(512), nullable=False)
    tags = db.Column(db.Unicode(512))
    clicks = db.Column(db.Integer, default=0)
    last_clicked = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    @classmethod
    def by_tag(self, page, oID, per_page, tag):
        tag = "%"+tag+"%"
        return self.query.filter(and_(
                                 self.tags.like(tag),
                                 self.owner_id == oID))\
                         .order_by(desc(self.clicks))\
                         .paginate(page, per_page, False)

    @classmethod
    def by_string(self, page, oID, per_page, string):
        string = "%"+string+"%"
        return self.query.filter(self.owner_id == oID)\
                         .filter(or_(self.title.like(string),
                                     self.tags.like(string),
                                     self.url.like(string)))\
                         .order_by(desc(self.clicks))\
                         .paginate(page, per_page, False)

    def __repr__(self):
        return '<Mark %r>' % (self.title)

