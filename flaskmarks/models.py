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
    suggestion = db.Column(db.Boolean, default=True)
    recently = db.Column(db.SmallInteger, default=2)
    bookmarks = db.relationship('Bookmark', backref='owner', lazy='dynamic')

    @classmethod
    def by_uname_or_email(self, uname):
        return self.query.filter(or_(User.username == uname,
                                     User.email == uname)).first()

    def bmy(self):
        return Bookmark.query.filter(Bookmark.owner_id == self.id)

    def fmy(self):
        return Feed.query.filter(Feed.owner_id == self.id)

    def bsuggestions(self):
        return self.bmy().filter(Bookmark.clicks == 0)\
                         .order_by(func.random())\
                         .limit(config['SUGGESTIONS_COUNT']).all()

    def fsuggestions(self):
        return self.fmy().filter(Feed.clicks == 0)\
                         .order_by(func.random())\
                         .limit(config['SUGGESTIONS_COUNT']).all()

    def brecent(self):
        return self.bmy().order_by(desc(Bookmark.created))\
                         .limit(self.recently).all()

    def frecent(self):
        return self.fmy().order_by(desc(Feed.created))\
                         .limit(self.recently).all()

    def bookmarks(self, page):
        return self.bmy().order_by(desc(Bookmark.clicks),
                                   desc(Bookmark.created))\
                         .paginate(page, self.per_page, False)

    def feeds(self, page):
        return self.fmy().order_by(desc(Feed.clicks),
                                   desc(Feed.created))\
                         .paginate(page, self.per_page, False)

    def bid(self, id):
        return self.bmy().filter(Bookmark.id == id)\
                         .first()

    def fid(self, id):
        return self.fmy().filter(Feed.id == id)\
                         .first()

    def bookmark_count(self):
        return self.bmy().count()

    def bookmark_last_created(self):
        return self.bmy().order_by(desc(Bookmark.created)).first()

    def feed_count(self):
        return self.fmy().count()

    def feed_last_created(self):
        return self.fmy().order_by(desc(Feed.created)).first()

    def btag(self, page, tag):
        return Bookmark.by_tag(page, self.id, self.per_page, tag)

    def bstring(self, page, string):
        return Bookmark.by_string(page, self.id, self.per_page, string)

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


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
        return '<Bookmark %r>' % (self.title)


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.Unicode(255), nullable=False)
    url = db.Column(db.Unicode(512), nullable=False)
    tags = db.Column(db.Unicode(512))
    clicks = db.Column(db.Integer, default=0)
    last_clicked = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
