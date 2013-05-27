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
    bookmarks = db.relationship('Bookmark', backref='owner', lazy='dynamic')

    @classmethod
    def by_uname_or_email(self, uname):
        return self.query.filter(or_(User.username == uname,\
                                     User.email == uname)).first()

    def my_suggestions(self):
        return Bookmark.query.filter(and_(Bookmark.owner_id == self.id,\
                                          Bookmark.clicks == 0))\
                             .order_by(func.random())\
                             .limit(config['SUGGESTIONS_COUNT']).all()

    def my_recent(self):
        return Bookmark.query.filter(Bookmark.owner_id == self.id)\
                             .order_by(desc(Bookmark.created))\
                             .limit(config['RECENTLY_ADDED']).all()

    def my_bookmarks(self, page):
        return Bookmark.query.filter(Bookmark.owner_id == self.id)\
                             .order_by(desc(Bookmark.clicks),\
                                       desc(Bookmark.created))\
                             .paginate(page, config['ITEMS_PER_PAGE'], False)

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
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    @classmethod
    def by_id(self, oID, bID):
        return self.query.filter(and_(
                                 self.id == bID, 
                                 self.owner_id == oID))\
                         .first()

    @classmethod
    def by_tag(self, page, oID, tag):
        tag = "%"+tag+"%"
        return self.query.filter(and_(
                                 self.tags.like(tag), 
                                 self.owner_id == oID))\
                         .order_by(desc(self.clicks))\
                         .paginate(page, config['ITEMS_PER_PAGE'], False)
    
    @classmethod
    def by_string(self, page, oID, string):
        string = "%"+string+"%"
        return self.query.filter(self.owner_id == oID)\
                         .filter(or_(self.title.like(string),\
                                     self.url.like(string)))\
                         .order_by(desc(self.clicks))\
                         .paginate(page, config['ITEMS_PER_PAGE'], False)

    def __repr__(self):
        return '<Bookmark %r>' % (self.title)
